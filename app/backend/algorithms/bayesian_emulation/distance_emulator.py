import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask 
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from models import MVector, db, Location, Distance
from dotenv import load_dotenv
import os
import csv
import numpy as np
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from model_extensions import MVectorExtensions

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

def to_x_input(origin, destination, transformer):
    x_origin, y_origin = transformer.transform(origin.lat, origin.lng)
    x_dest, y_dest = transformer.transform(destination.lat, destination.lng)
    return [x_origin, y_origin, x_dest, y_dest]

with app.app_context():    

    transformer = CoordTransformer()
    

    # TODO need to complete the below, testing that the new format in DB works
    #m_vector:MVector = MVectorExtensions.get_m_vector_by_name("initial-set")
    #emulator = BayesianEmulator(m_vector.beta, m_vector.sigma, m_vector.theta)

