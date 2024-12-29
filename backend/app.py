from flask import Flask, render_template, request, jsonify
from requests import Response

from models import db, Pub  # User
import json
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
import requests  # For geocoding API
import os
from dotenv import load_dotenv
import pymysql  # Make sure to include pymysql or another MySQL driver in requirements.txt
import time

### Env variables
load_dotenv(dotenv_path="/app/.env")
# Get database connection details from environment variables
db_user = os.getenv("MYSQL_USER", "user")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_host = os.getenv("MYSQL_HOST", "mysql")  # "mysql" refers to the container name
db_name = os.getenv("MYSQL_DATABASE", "db_name")
# Get other enviroment variables
API_KEY = os.getenv("API_KEY", "api_key")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
OUTPUT_PUBS_JSON = os.getenv("OUTPUT_JSON", "true").lower() == "true"


# Mock data paths
path_to_groups_json = "/app/mock_data/groups.json"
path_to_pubs_json = "/app/mock_data/pubs.json"
path_to_user_group_query_json = "/app/mock_data/userGroupQuery.json"
path_to_users_json = "/app/mock_data/users.json"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
# migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route("/test", methods=["GET"])
def do():
    return "Hello, world!"


def load_mock_json(path_to_mock_json):
    with open(path_to_mock_json) as file:
        data = json.load(file)
    return jsonify(data)


@app.route("/api/groups", methods=["GET"])
def get_groups():
    if MOCK_MODE:
        return load_mock_json(path_to_groups_json)


@app.route("/api/pubs", methods=["GET"])
def get_pubs():
    if MOCK_MODE:
        return load_mock_json(path_to_pubs_json)


@app.route("/api/user-group-query", methods=["GET"])
def get_user_group_query():
    if MOCK_MODE:
        return load_mock_json(path_to_user_group_query_json)


@app.route("/api/users", methods=["GET"])
def get_users():
    if MOCK_MODE:
        return load_mock_json(path_to_users_json)


# Geocode function to convert addresses to coordinates
def geocode_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "results" in data and data["results"]:
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None


# Calculate geometric center
def calculate_centre(coordinates):
    latitudes = [lat for lat, lng in coordinates]
    longitudes = [lng for lat, lng in coordinates]
    center_lat = sum(latitudes) / len(latitudes)
    center_lng = sum(longitudes) / len(longitudes)
    return {"lat": center_lat, "lng": center_lng}


@app.route("/api/get-centre", methods=["POST"])
def get_centre():
    response = get_users().get_json()
    for user in response:
        print(user["address"])

    coordinates = []
    for item in response:
        coords = geocode_address(item["address"])
        if coords:
            coordinates.append(coords)

    if not coordinates:
        return jsonify({"error": "No valid addresses provide"})

    centre = calculate_centre(coordinates)
    return jsonify(centre)


# https://developers.google.com/maps/documentation/routes/reference/rest
@app.route("/api/get-journey-time", methods=["GET"])
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


@app.route("/api/get-journey-times", methods=["GET"])
def get_journey_times():
    response = get_users().get_json()
    centre_response = get_centre().get_json()

    journey_times = []
    url = f"http://localhost:5001/api/get-journey-time"  # Needed due to collection of parmams
    for user_entry in response:
        coords_user = geocode_address(user_entry["address"])
        params = {"origin_lat": coords_user[0], "origin_lng": coords_user[1], "dest_lat": centre_response["lat"], "dest_lng": centre_response["lng"]}
        response = requests.get(url, params=params)
        journey_time = response.json()
        journey_times.append(journey_time)
    return jsonify(journey_times), 200


# TODO(@TS): Improve function to return full number of pubs desired
def get_place_data(query):
    # Google Maps API configuration
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,nextPageToken",
    }
    data = {"textQuery": query, "pageSize": 20}

    number_results = 200  # TODO(@TS): Move constant to a better location or use a variable
    places_json = {"places": []}
    while len(places_json["places"]) < number_results:
        response = requests.post(url, json=data, headers=headers)
        if "nextPageToken" in response.json() and response.status_code == 200:
            places_json["places"].extend(response.json()["places"])
            data["pageToken"] = response.json()["nextPageToken"]
        elif response.status_code == 200:
            places_json["places"].extend(response.json()["places"])
            print("Number of pubs requested: ", number_results)
            print(f"Number of pubs found: {len(places_json["places"])} - {number_results/len(places_json['places'])}%")
            return places_json
        else:
            print(f"{response.json()["error"]["message"]}")
            return jsonify({"error": f"Failed to retrieve journey time on page no {i}"}), 500
    return places_json


@app.route("/utils/populate-pubs", methods=["PUT"])
def populate_pubs():
    # Clear existing data
    # Pub.query.delete()

    # Get pub data from Google Maps API
    pub_data = get_place_data("pubs in London")

    duplicates = 0
    for result in pub_data["places"]:
        pub = Pub(name=result["displayName"]["text"], address=result["formattedAddress"])
        try:
            db.session.add(pub)
        except IntegrityError as e:
            db.session.rollback()  # Rollback to clear the session state
            print(f"Skipping invalid item: {pub}. Error: {e}")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            duplicates += 1

    if duplicates:
        print(f"Skipped {duplicates} duplicates")

    # Ue batch comitting when peformance is critical and errors are rare.
    # try:
    #     db.session.commit()
    # except Exception as e:
    #     db.session.rollback()
    #     print(f"Failed to commit changes. Error: {e}")

    output = pub_data.copy()
    for pub in output["places"]:
        print(pub)
        pub["displayName"] = pub["displayName"]["text"]
    output["message"] = f"Pubs successfully populated - number added {len(pub_data["places"])-duplicates} - duplicates {duplicates}"
    return jsonify(output), 200
