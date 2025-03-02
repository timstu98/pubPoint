import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask 
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from models import db, Location, Distance
from dotenv import load_dotenv
import os
import csv

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

def get_distance(origin, destination):
    if origin == destination:
        return 0
    else:
        distance_entry = Distance.query.filter_by(
                    origin_id=origin.id,
                    destination_id=destination.id
                ).first()

        if not distance_entry:
            raise Exception(f"Cannot find distance for {origin} -> {destination}")
            
        return distance_entry.seconds

def to_xj(origin, destination):
    return [float(origin.lat), float(origin.lng), float(destination.lat), float(destination.lng)]

with app.app_context():    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'data', 'starting_locations.csv')

    locations = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            name = row['Name']
            
            location = Location.query.filter(
                db.func.lower(Location.name) == name.lower()
            ).first()

            if not location:
                raise Exception(f"Cannot find location {name}")

            locations.append(location)

    x_train = [] # Training Points, X_A
    D = [] # Known outputs, f(X_A)
    for origin in locations:
        for destination in locations:
            x_j = to_xj(origin, destination)
            d_j = float(get_distance(origin, destination))
            x_train.append(x_j)
            D.append(d_j)

    Beta = 45 * 60 * 60 # Beta = E[f(x)] : "everywhere in London is 45 minutes away" - someone, probably
    sigma = 5 * 60 * 60 # sigma = standard deviation : 5 min estimate for now

    # TODO - calculating theta shows that lat/long is not a uniform space! Need to convert it to have any chance of this working well
    theta = 0.1 # theta = correlation-scale of the gaussian process : Solution space ~=0.300, taking a third as a standard starting point

    bayesianEmulator = BayesianEmulator(Beta, sigma, theta, x_train, D)

    M = bayesianEmulator.compute_M()

    banana = 0

    # TODO - I think this is failing to match due to numerical instability. Need to fix the units, see if I can converter long lat to actual meters.
    # Maybe something fun like meters north / south of Big Ben
    for origin in locations:
        for destination in locations:
            emulated = bayesianEmulator.emulate(to_xj(origin, destination))
            d_j = float(get_distance(origin, destination))

            diff = emulated - d_j

            banana = 0
                
