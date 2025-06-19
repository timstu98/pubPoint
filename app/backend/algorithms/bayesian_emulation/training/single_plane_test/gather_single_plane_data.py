import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from models import db, Location, Distance
import os
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import RoutesRequest
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer

app, env = create_flask_app()

with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    

    locations = []

    x_range = np.linspace(-15000, 10000, 100)
    y_range = np.linspace(-8000, 8000, 100)

    transformer = CoordTransformer()

    for x in x_range:
        for y in y_range:
            lat, lng = transformer.transformBack(x,y)
        
        name = "Plane_WA_{x}_{y}"

        # Use get_or_create to create or retrieve the Location object
        location, new = Location.get_or_create(
            name=name,
            lat=lat,
            lng=lng
        )

        locations.append(location)

    # Commit once after all locations are processed
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error committing locations: {e}")
        raise
    
        # this should work but need to test transformer works correctly first!

    # for origin in locations:
    #     for destination in locations:
    #         try:
    #             if origin == destination:
    #                 continue

    #             # Get or create the distance relationship
    #             distance_entry, isNew = Distance.get_or_create(origin, destination)

    #             if not isNew:
    #                 distance_in_db = distance_entry.seconds
    #                 if distance_in_db > 0:
    #                     continue
                
    #             api = GoogleRoutesApi(env["API_KEY"])
    #             rqst = RoutesRequest([origin.coords], [destination.coords])

    #             result = api.matrix(rqst)
    #             if result:
                    
    #                 # Update with API results
    #                 distance_entry.update_distance(
    #                     meters=result[0]['distanceMeters'],
    #                     seconds=result[0]['staticDuration'].rstrip('s')
    #                 )
                    
    #                 # Commit the distance update
    #                 db.session.commit()
    #                 print(f"Successfully wrote distance: {distance_entry.origin_id} -> {distance_entry.destination_id} = {distance_entry.seconds}s")
                    
    #                 # Verify write
    #                 stored_distance = Distance.query.filter_by(
    #                     origin_id=origin.id,
    #                     destination_id=destination.id
    #                 ).first()
                    
    #                 print(f"Database contains: {stored_distance.meters}m between locations")
                    
    #         except Exception as e:
    #             db.session.rollback()
    #             print(f"Error processing distance: {e}")
