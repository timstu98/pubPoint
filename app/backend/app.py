from flask import Flask, render_template, request, jsonify
from requests import Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models import db, Pub, Group, User, UserGroupQuery
import json
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
import requests  # For geocoding API
import os
from dotenv import load_dotenv
import pymysql  # Make sure to include pymysql or another MySQL driver in requirements.txt
import time

from api.routes.pubs_routes import pubs_routes
from api.routes.users_routes import users_routes
from api.routes.groups_routes import groups_routes
from api.routes.user_group_queries_routes import user_group_queries_routes
from api.routes.auth_routes import auth_routes
from api.routes.common import geocode_address

### Env variables
load_dotenv(dotenv_path="/app/.env")
# Get database connection details from environment variables
db_user = os.getenv("MYSQL_USER", "user")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_host = os.getenv("MYSQL_HOST", "mysql")  # "mysql" refers to the container name
db_name = os.getenv("MYSQL_DATABASE", "db_name")
# Get other enviroment variables
API_KEY = os.getenv("API_KEY", "api_key")
API_VERSION = os.getenv("API_VERSION", "vX")  # Add this line
OUTPUT_PUBS_JSON = os.getenv("OUTPUT_JSON", "true").lower() == "true"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")  # Add a secret key for JWT

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY  # Set JWT secret key
CORS(app)  # Enables CORS for all routes and origins
db.init_app(app)
jwt = JWTManager(app)  # Initialize JWT
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    
api_url_prefix = f"/api/{API_VERSION}"

# Register the api routes blueprints
app.register_blueprint(pubs_routes, url_prefix=api_url_prefix)
app.register_blueprint(users_routes, url_prefix=api_url_prefix)
app.register_blueprint(groups_routes, url_prefix=api_url_prefix)
app.register_blueprint(user_group_queries_routes, url_prefix=api_url_prefix)
app.register_blueprint(auth_routes, url_prefix=api_url_prefix)


@app.route("/test", methods=["GET"])
def do():
    return "Hello, world!"


def load_mock_json(path_to_mock_json):
    with open(path_to_mock_json) as file:
        data = json.load(file)
    return data


def get_table_data(table_object):
    table_data = table_object.query.all()
    return [item.get_as_dict() for item in table_data]


# Calculate geometric center
def calculate_centre(coordinates):
    latitudes = [lat for lat, lng in coordinates]
    longitudes = [lng for lat, lng in coordinates]
    center_lat = sum(latitudes) / len(latitudes)
    center_lng = sum(longitudes) / len(longitudes)
    return {"lat": center_lat, "lng": center_lng}


@app.route(f"{api_url_prefix}/get-centre", methods=["POST"])
def get_centre():
    users = get_table_data(User)

    coordinates = []
    for item in users:
        coords = geocode_address(item["address"])
        if coords:
            coordinates.append(coords)

    if not coordinates:
        return jsonify({"error": "No valid addresses provide"})

    centre = calculate_centre(coordinates)
    return jsonify(centre)


@app.route(f"{api_url_prefix}/geocode", methods=["GET"])
def get_geocode():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    print(address)
    
    coords = geocode_address(address)
    if coords:
        print("coords")
        return jsonify({"lat": coords[0], "lng": coords[1]})
    print("end fail")
    return jsonify({"error": "Could not geocode address"}), 400


# https://developers.google.com/maps/documentation/routes/reference/rest
@app.route(f"{api_url_prefix}/get-journey-time", methods=["GET"])
def get_journey_time():
    origin_lat = request.args.get("origin_lat")
    origin_lng = request.args.get("origin_lng")
    dest_lat = request.args.get("dest_lat")
    dest_lng = request.args.get("dest_lng")

    if not origin_lat or not origin_lng or not dest_lat or not dest_lng:
        return jsonify({"error": "Missing or invalid query parameters"}), 400

    try:
        origin_lat = float(origin_lat)
        origin_lng = float(origin_lng)
        dest_lat = float(dest_lat)
        dest_lng = float(dest_lng)
    except ValueError:
        return jsonify({"error": "Query parameters must be valid floats"}), 400

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {"Content-Type": "application/json", "X-Goog-Api-Key": API_KEY, "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"}
    data = {
        "origin": {"location": {"latLng": {"latitude": float(origin_lat), "longitude": float(origin_lng)}}},
        "destination": {"location": {"latLng": {"latitude": float(dest_lat), "longitude": float(dest_lng)}}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        duration = round(float(result["routes"][0]["duration"][:-1]) / 60)
        return jsonify(
            {"origin": {"lat": origin_lat, "lng": origin_lng}, "destination": {"lat": dest_lat, "lng": dest_lng}, "duration/mins": duration}
        )
    else:
        print(response.json()["error"]["message"])
        return jsonify({"error": "Failed to retrieve journey time"}), 500


@app.route(f"{api_url_prefix}/get-journey-times", methods=["GET"])
def get_journey_times():
    users = get_table_data(User)
    centre_response = get_centre().get_json()

    journey_times = []
    url = f"http://localhost:5001/api/get-journey-time"  # Needed due to collection of parmams
    for user_entry in users:
        coords_user = geocode_address(user_entry["address"])
        params = {"origin_lat": coords_user[0], "origin_lng": coords_user[1], "dest_lat": centre_response["lat"], "dest_lng": centre_response["lng"]}
        response = requests.get(url, params=params)
        journey_time = response.json()
        journey_times.append(journey_time)
    return jsonify(journey_times), 200