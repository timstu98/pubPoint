import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask 
from models import db, Location, Distance
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import RoutesRequest

if "/app" not in sys.path:
    print("Ensure you set the PYTHONPATH to ensure relative imports work correctly.")

load_dotenv(dotenv_path="/app/.env")

### Env variables
DB_USER = os.getenv("MYSQL_USER", "user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_NAME = os.getenv("MYSQL_DATABASE", "DB_NAME")
API_KEY = os.getenv("API_KEY", "api_key")
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
TEST_FUNCTIONALITY_MODE = os.getenv("TEST_FUNCTIONALITY_MODE", "false").lower() == "true"

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

def get_engine():
    return create_engine(DATABASE_URI)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Wrap database operations in app context
with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    # Create or get locations
    farringdon_location, new = Location.get_or_create(
        name="Farringdon Station",
        lat=51.51996102,
        lng=-0.103582415
    )
    
    paddington_location, new = Location.get_or_create(
        name="Paddington Station",
        lat=51.51499491,
        lng=-0.173789485
    )

    # Commit once after all locations are processed
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error committing locations: {e}")
        raise
    
    try:
        api = GoogleRoutesApi(API_KEY)
        rqst = RoutesRequest([farringdon_location.coords], [paddington_location.coords])

        result = api.matrix(rqst)
        if result:
            # Get or create the distance relationship
            distance_entry = Distance.get_or_create(farringdon_location, paddington_location)
            
            # Update with API results
            distance_entry.update_distance(
                meters=result[0]['distanceMeters'],
                seconds=result[0]['staticDuration'].rstrip('s')
            )
            
            # Commit the distance update
            db.session.commit()
            print(f"Successfully wrote distance: {distance_entry.meters}m")
            
            # Verify write
            stored_distance = Distance.query.filter_by(
                origin_id=farringdon_location.id,
                destination_id=paddington_location.id
            ).first()
            
            print(f"Database contains: {stored_distance.meters}m between locations")
            
    except Exception as e:
        db.session.rollback()
        print(f"Error processing distance: {e}")
