from flask import Flask, render_template, request, jsonify
from requests import Response

from models import db  # User
import json
from flask_sqlalchemy import SQLAlchemy
import requests  # For geocoding API
import os
import pymysql  # Make sure to include pymysql or another MySQL driver in requirements.txt

# Get database connection details from environment variables
db_user = os.getenv("MYSQL_USER", "user")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_host = os.getenv("MYSQL_HOST", "mysql")  # "mysql" refers to the container name
db_name = os.getenv("MYSQL_DATABASE", "db_name")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/hi", methods=["GET"])
def do():
    return "hi"


@app.route("/hi/cool2", methods=["GET"])
def donot():
    return "hi, cool2!"


# @app.route("/user", methods=["POST"])
# def add_user():
#     body = request.get_json()
#     user = User(**body)
#     id = user.id
#     db.session.add(user)
#     db.session.commit()
#     return {"id": str(id)}, 200


# @app.route("/user/<user_id>", methods=["GET"])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     return jsonify(user.as_dict()), 200


# @app.route("/users", methods=["GET"])
# def get_users():
#     usersRaw = User.query.all()
#     users = []
#     for user in usersRaw:
#         users.append(user.as_dict())
#     resp = {
#         "responseObject": {
#             "results": len(users),
#             "users": users,
#         }
#     }
#     return jsonify(resp), 200


# # Geocode function to convert addresses to coordinates
# def geocode_address(address):
#     API_KEY = "AIzaSyCLYrehsXHVao80ycVIv1HMvKHW87bSAvk"  # Replace with your geocoding API key
#     url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     if "results" in data and data["results"]:
#         location = data["results"][0]["geometry"]["location"]
#         return location["lat"], location["lng"]
#     else:
#         return None


# # Calculate geometric center
# def calculate_centre(coordinates):
#     latitudes = [lat for lat, lng in coordinates]
#     longitudes = [lng for lat, lng in coordinates]
#     centre_lat = sum(latitudes) / len(latitudes)
#     centre_lng = sum(longitudes) / len(longitudes)
#     return {"lat": centre_lat, "lng": centre_lng}


# @app.route("/centre", methods=["POST"])
# def get_centre():
#     data = request.get_json()
#     addresses = data.get("addresses", [])

#     coordinated = []
#     for address in addresses:
#         coords = geocode_address(address)
#         if coords:
#             coordinates.append(coords)

#     if not coordinates:
#         return jsonify({"error": "No valid addresses provide"})

#     centre = calculate_centre(coordinates)
#     return jsonify(centre), 200


# @app.route('/users')
# def get_users():
# # users = User
# return Response(users, mimetype="application/json", status=200)
# # return render_template('home.html')
