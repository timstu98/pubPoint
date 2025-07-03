import numpy as np
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from models import db, Location, Distance
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import RoutesRequest
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from scipy.stats import qmc

app, env = create_flask_app()

with app.app_context():
    locations = []

    x_bounds = [-15000, 10000]  # for both origin_x and destination_x
    y_bounds = [-8000, 8000]    # for both origin_y and destination_y

    transformer = CoordTransformer()
    num_samples = 5000 # stick within free limit of Google API
    seed = 123 

    # Create 4D LHS
    sampler = qmc.LatinHypercube(d=4, seed=seed)
    sample = sampler.random(n=num_samples)

    # Scale each dimension
    bounds = [x_bounds, y_bounds, x_bounds, y_bounds]
    scaled_sample = qmc.scale(sample, [b[0] for b in bounds], [b[1] for b in bounds])

    for i, (ox, oy, dx, dy) in enumerate(scaled_sample):
        origin_lat, origin_lng = transformer.transformBack(ox, oy)
        dest_lat, dest_lng = transformer.transformBack(dx, dy)
    
        origin_name = f"LHS_Origin_{i}"
        dest_name = f"LHS_Dest_{i}"
        
        origin, _ = Location.get_or_create(name=origin_name, lat=origin_lat, lng=origin_lng)
        destination, _ = Location.get_or_create(name=dest_name, lat=dest_lat, lng=dest_lng)

        locations.append((origin, destination))

    # Commit once after all locations are processed
    try:
        db.session.commit()
    except Exception as e:
        #db.session.rollback()
        print(f"Error committing locations: {e}")
        raise
    
    count = len(locations)

    if count > 5000:
        raise f"cannot run {count} requests!"

    for origin, destination in locations:
        try:
            distance_entry, isNew = Distance.get_or_create(origin, destination)

            if not isNew:
                distance_in_db = distance_entry.seconds
                if distance_in_db > 0:
                    continue
            
            api = GoogleRoutesApi(env["API_KEY"])
            rqst = RoutesRequest([origin.coords], [destination.coords])

            result = api.matrix(rqst)
            if result:
                
                # Update with API results
                distance_entry.update_distance(
                    meters=result[0]['distanceMeters'],
                    seconds=result[0]['staticDuration'].rstrip('s')
                )
                
                # Commit the distance update
                db.session.commit()
                print(f"Successfully wrote distance: {distance_entry.origin_id} -> {distance_entry.destination_id} = {distance_entry.seconds}s")
                
                # Verify write
                stored_distance = Distance.query.filter_by(
                    origin_id=origin.id,
                    destination_id=destination.id
                ).first()
                
                print(f"Database contains: {stored_distance.seconds}s between locations")
                
        except Exception as e:
            #db.session.rollback()
            print(f"Error processing distance: {e}")
