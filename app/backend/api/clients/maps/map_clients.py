from api.clients.api_client import ApiClient
from abc import ABC, abstractmethod

from api.clients.maps.routes_request import RoutesRequest

# Abstract base class for any map API
class IPlacesApi(ABC):
    def __init__(self, base_url, api_key):
        self.api = ApiClient(base_url, api_key)
        super().__init__()

    @abstractmethod
    def search_places(self, query, location_restriction, max_results=20, page_token=None):
        pass

class IRoutesApi(ABC):
    def __init__(self, base_url, api_key):
        self.api = ApiClient(base_url, api_key)
        super().__init__()

    @abstractmethod
    def matrix(self):
        pass

# Google API implementation
class GooglePlacesApi(IPlacesApi):
    def __init__(self, api_key):
        super().__init__("https://places.googleapis.com/v1", api_key)

    def search_places(self, query, location_restriction, max_results=20, page_token=None):
        endpoint = "places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api.api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,nextPageToken",
        }
        data = {
            "textQuery": query,
            "maxResultCount": max_results,
            "locationRestriction": location_restriction,
        }
        if page_token:
            data["pageToken"] = page_token

        return self.api.post(endpoint, headers, data)
    
class GoogleRoutesApi(IRoutesApi):
    def __init__(self, api_key):
        super().__init__("https://routes.googleapis.com", api_key)

    def matrix(self, routes_rqst:RoutesRequest):
        endpoint = "distanceMatrix/v2:computeRouteMatrix"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api.api_key,
            "X-Goog-FieldMask": "status,condition,distanceMeters,staticDuration",
        }
        data = routes_rqst.to_json()

        return self.api.post(endpoint, headers, data)    