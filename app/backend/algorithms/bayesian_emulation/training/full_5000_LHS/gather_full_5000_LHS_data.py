import numpy as np
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from algorithms.bayesian_emulation.training.full_5000_LHS.LHS_location_generator import LHSLocationGenerator
from models import db, Location, Distance
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import RoutesRequest
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from scipy.stats import qmc

app, env = create_flask_app()

with app.app_context():
    locations = LHSLocationGenerator.generate_locations(num_samples=5000, seed=123)

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
