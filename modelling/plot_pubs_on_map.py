import sys
import os
import folium
import requests

# Ensure the app directory is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "backend")))

from models import db, Pub
from app import app

# load_dotenv(dotenv_path="/app/.env")
# API_KEY = os.getenv("API_KEY", "api_key")
API_KEY = "DON'T BUT DO ADD A KEY HERE YOU IDIOT"


def plot_pubs_on_map():
    # Create a map centered around London
    m = folium.Map(location=[51.509865, -0.118092], zoom_start=10)

    # Get all pubs from the database
    with app.app_context():
        print(app.app_context())
        pubs = Pub.query.all()

    # Add pubs to the map
    for pub in pubs:
        coords = geocode_address(pub.address)
        if coords:
            folium.Marker(
                location=[coords[0], coords[1]],
                popup=folium.Popup(f"<b>{pub.name}</b><br>{pub.address}", max_width=300),
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

    # Save the map to an HTML file
    m.save("modelling/london_pubs.html")


def geocode_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "results" in data and data["results"]:
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None


if __name__ == "__main__":
    plot_pubs_on_map()
