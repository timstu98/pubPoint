
import json

class Coords:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

class RoutesRequest:
    def __init__(self, origins, destinations, travel_mode="TRANSIT", language_code="en-GB", region_code="GB", units="METRIC"):
        self.origins = origins
        self.destinations = destinations
        self.travel_mode = travel_mode
        self.language_code = language_code
        self.region_code = region_code
        self.units = units

    def to_json(self):
        origins_list = []
        for origin in self.origins:
            origins_list.append({
                "waypoint": {
                    "location": {
                        "latLng": origin.to_dict()
                    }
                }
            })

        destinations_list = []
        for destination in self.destinations:
            destinations_list.append({
                "waypoint": {
                    "location": {
                        "latLng": destination.to_dict()
                    }
                }
            })

        request_dict = {
            "origins": origins_list,
            "destinations": destinations_list,
            "travelMode": self.travel_mode,
            "languageCode": self.language_code,
            "regionCode": self.region_code,
            "units": self.units
        }

        return request_dict 