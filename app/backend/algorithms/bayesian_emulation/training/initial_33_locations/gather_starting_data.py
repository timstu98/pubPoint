from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from models import db, Location, Distance
import os
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import RoutesRequest
import csv

app, env = create_flask_app()

# TODO check if these are needed
# def get_engine():
#     return create_engine(DATABASE_URI)
# def get_session(engine):
#     Session = sessionmaker(bind=engine)
#     return Session()

# Wrap database operations in app context
with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'data', 'starting_locations.csv')

    locations = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            name = row['Name']
            lat = float(row['y'])  # Latitude is in the 'y' column
            lng = float(row['x'])  # Longitude is in the 'x' column
            
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
    
    for origin in locations:
        for destination in locations:
            try:
                if origin == destination:
                    continue

                # Get or create the distance relationship
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
                    
                    print(f"Database contains: {stored_distance.meters}m between locations")
                    
            except Exception as e:
                db.session.rollback()
                print(f"Error processing distance: {e}")
