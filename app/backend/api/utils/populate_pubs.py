import sys
import time
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify
from models import Pub, db
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError


if "/app" not in sys.path:
    print("Ensure you set the PYTHONPATH to ensure relative imports work correctly.")

load_dotenv(dotenv_path="/app/.env")
### Env variables
# Get database connection details from environment variables
db_user = os.getenv("MYSQL_USER", "user")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_host = os.getenv("MYSQL_HOST", "mysql")  # "mysql" refers to the container name
db_name = os.getenv("MYSQL_DATABASE", "db_name")
# Get other environment variables
API_KEY = os.getenv("API_KEY", "api_key")
DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"


def get_engine():
    return create_engine(DATABASE_URI)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def generate_rectangles(top_left, bottom_right, num_lat_divisions, num_lng_divisions):
    """
    Divide an area into smaller rectangles and return their corner coordinates.

    :param top_left: Tuple (lat, lng) of the top-left corner of the overall area.
    :param bottom_right: Tuple (lat, lng) of the bottom-right corner of the overall area.
    :param num_lat_divisions: Number of divisions along the latitude axis.
    :param num_lng_divisions: Number of divisions along the longitude axis.
    :return: List of rectangles as tuples ((top_left_lat, top_left_lng), (bottom_right_lat, bottom_right_lng)).
    """
    top_lat, left_lng = top_left
    bottom_lat, right_lng = bottom_right

    lat_step = (top_lat - bottom_lat) / num_lat_divisions
    lng_step = (right_lng - left_lng) / num_lng_divisions

    rectangles = []

    for i in range(num_lat_divisions):
        for j in range(num_lng_divisions):
            rect_top_left = (top_lat - i * lat_step, left_lng + j * lng_step)
            rect_bottom_right = (top_lat - (i + 1) * lat_step, left_lng + (j + 1) * lng_step)
            rectangles.append((rect_top_left, rect_bottom_right))

    return rectangles


def get_place_data_search_nearby(top_left, bottom_right, place_type="bar"):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,nextPageToken",
    }
    data = {
        "textQuery": "pubs",
        "maxResultCount": 20,
        "locationRestriction": {
            "rectangle": {
                "low": {"latitude": bottom_right[0], "longitude": top_left[1]},
                "high": {"latitude": top_left[0], "longitude": bottom_right[1]},
            }
        },
    }

    places_json = {"places": []}
    while True:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            places_json["places"].extend(result["places"])
            if "nextPageToken" in result:
                data["pageToken"] = result["nextPageToken"]
            else:
                break
        else:
            print(f"Error: {response.json()['error']['message']}")
            break

    return places_json


def populate_pubs(top_left, bottom_right, num_lat_divisions, num_lng_divisions):
    # Generate rectangles.
    rectangles = generate_rectangles(top_left, bottom_right, num_lat_divisions, num_lng_divisions)

    total_pubs = set()
    api_calls = 0

    for idx, (top_left, bottom_right) in enumerate(rectangles):
        pub_data = get_place_data_search_nearby(top_left, bottom_right)
        if pub_data:
            for place in pub_data["places"]:
                pub = (place["displayName"]["text"], place["formattedAddress"])
                total_pubs.add(pub)

        # TODO(@TS): This should track the number of next page tokens as I think google maps counts this as an additional query.
        api_calls += 1
        if api_calls % 20 == 0:
            print(f"API calls made: {api_calls} UPDATE THIS IS NOT ACCURATE")
            print(f"Rectangles processed: {idx + 1}/{len(rectangles)}")
            print(f"Total pubs found: {len(total_pubs)}")
            input("Press Enter to continue...")

    # Save pubs to the database
    duplicates = 0
    for name, address in total_pubs:
        pub = Pub(name=name, address=address)
        try:
            db.session.add(pub)
        except IntegrityError as e:
            db.session.rollback()
            duplicates += 1
            print(f"Skipping duplicate item: {pub}. Error: {e}")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            duplicates += 1

    print(f"Skipped {duplicates} duplicates")
    print(f"Total pubs added: {len(total_pubs) - duplicates}")

    output = {"allPubs": []}
    for pub in Pub.query.all():
        output_pub = {"id": pub.id, "name": pub.name, "address": pub.address}
        output["allPubs"].append(output_pub)

    output["message"] = (
        f"Pubs successfully populated - number added {len(total_pubs) - duplicates} - duplicates {duplicates} - total in table {len(output['allPubs'])}"
    )
    return jsonify(output), 200


if __name__ == "__main__":

    # TODO(@TS): Refine and optimise the bounding box and number of divisions. Option to make more dense near centre.
    #            Think of a way to filter out unwanted cafes and bars.
    #            Add a way to see post search the number of pubs I got form each rectangle, and whether I hit 60 whichy I think mayb be the limit.
    
    ### London "proper" data
    # Define the bounding box for London (approximate).
    top_left = (51.6723432, -0.563)
    bottom_right = (51.3849401, 0.278)
    # Set the number of divisions.
    num_lat_divisions = 8
    num_lng_divisions = 12

    ### Test Data for db
    # top_left = (51.6723432, -0.563)
    # bottom_right = (51.649401, -0.3)
    # num_lat_divisions = 2
    # num_lng_divisions = 2
    
    from app import app
    with app.app_context():
        populate_pubs(top_left, bottom_right, num_lat_divisions, num_lng_divisions)
