import sys

if "/app" not in sys.path:
    print("Ensure you set the PYTHONPATH to ensure relative imports work correctly.")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from models import Pub, db
from requests import Response
import requests  # For geocoding API
import os
import json
from dotenv import load_dotenv
import pymysql  # Make sure to include pymysql or another MySQL driver in requirements.txt
import time

load_dotenv(dotenv_path="/app/.env")
### Env variables
load_dotenv(dotenv_path="/app/.env")
# Get database connection details from environment variables
db_user = os.getenv("MYSQL_USER", "user")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_host = os.getenv("MYSQL_HOST", "mysql")  # "mysql" refers to the container name
db_name = os.getenv("MYSQL_DATABASE", "db_name")
# Get other enviroment variables
API_KEY = os.getenv("API_KEY", "api_key")
OUTPUT_PUBS_JSON = os.getenv("OUTPUT_JSON", "true").lower() == "true"
DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"


def get_engine():
    return create_engine(DATABASE_URI)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def get_place_data(lat, lng, place_type="pubs"):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,nextPageToken",
    }
    data = {"textQuery": f"{place_type} in {lat},{lng}", "pageSize": 20}

    number_results = 200
    places_json = {"places": []}
    while len(places_json["places"]) < number_results:
        response = requests.post(url, json=data, headers=headers)
        if "nextPageToken" in response.json() and response.status_code == 200:
            places_json["places"].extend(response.json()["places"])
            data["pageToken"] = response.json()["nextPageToken"]
        elif response.status_code == 200:
            places_json["places"].extend(response.json()["places"])
            print("Number of places requested: ", number_results)
            print(f"Number of places found: {len(places_json['places'])} ({100*len(places_json['places'])/number_results}%)")
            return places_json
        else:
            print(f"{response.json()['error']['message']}")
            return jsonify({"error": f"Failed to retrieve places on page no {i}"}), 500
    return places_json


def populate_pubs():
    # Clear existing data
    # Pub.query.delete()

    # Get pub data from Google Maps API
    pub_data = get_place_data(51.5074, -0.1278)  # Example coordinates for London

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

    output = {"allPubs": []}
    for pub in Pub.query.all():
        output_pub = {}
        output_pub["id"] = pub.id
        output_pub["name"] = pub.name
        output_pub["address"] = pub.address
        output["allPubs"].append(output_pub)

    output["message"] = (
        f"Pubs successfully populated - number added {len(pub_data['places']) - duplicates} - duplicates {duplicates} - total in table {len(output['allPubs'])}"
    )
    return jsonify(output), 200


# Do not include __main__ check if I eventually choose to running this script as a module to allow relative imports.
# Using python path "hack" for now.
if __name__ == "__main__":
    print("Populate pubs")
    # populate_pubs()
