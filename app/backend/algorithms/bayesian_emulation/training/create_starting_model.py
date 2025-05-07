from decimal import Decimal
import sys
from flask import Flask 
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from models import db, Location, Distance
from dotenv import load_dotenv
import os
import csv
import numpy as np
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from model_extensions import BayesianModelExtensions

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

def to_x_input(origin, destination, transformer):
    x_origin, y_origin = transformer.transform(origin.lat, origin.lng)
    x_dest, y_dest = transformer.transform(destination.lat, destination.lng)
    return [
        Decimal(str(x_origin)),  # Convert via string to avoid floating-point inaccuracies
        Decimal(str(y_origin)),
        Decimal(str(x_dest)),
        Decimal(str(y_dest))
    ]

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

    transformer = CoordTransformer()
    x_train = [] # Training Points, X_A
    D = [] # Known outputs, f(X_A)
    for origin in locations:
        for destination in locations:
            x_j = to_x_input(origin, destination, transformer)
            d_j = get_distance(origin, destination)
            x_train.append(x_j)
            D.append(d_j)

    Beta = 45 # Beta = E[f(x)] : "everywhere in London is 45 minutes away" - someone, probably
    sigma = 1 # sigma = standard deviation : estimate
    theta = 5000 # theta = correlation-scale of the gaussian process : estimate

    bayesianEmulator = BayesianEmulator(Beta, sigma, theta, x_train, D)

    M = bayesianEmulator.compute_M()

    for origin in locations:
        for destination in locations:
            emulated = bayesianEmulator.emulate(to_x_input(origin, destination, transformer))
            d_j = float(get_distance(origin, destination))

            diff = emulated - d_j

            if diff > 10:
                raise f"Error in training Bayesian Emulator - predictions of distance for training data over 10 seconds different from provided values. {origin.name}-{destination.name} returned difference of {diff}"
                
    BayesianModelExtensions.insert_bayesian_model("initial-set-5", M, x_train, D, Beta, sigma, theta)