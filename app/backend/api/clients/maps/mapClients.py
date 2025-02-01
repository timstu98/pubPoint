from api.clients.apiClient import ApiClient
from abc import ABC, abstractmethod

# Abstract base class for any map API
class IMapApi(ABC):
    def __init__(self, base_url, api_key):
        self.api = ApiClient(base_url, api_key)
        super().__init__()

    @abstractmethod
    def search_places(self, query, location_restriction, max_results=20, page_token=None):
        pass

# Google API implementation
class GoogleApi(IMapApi):
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
    

# Mapbox API implementation (example placeholder)
class MapboxApi(IMapApi):
    def __init__(self, api_key):
        self.base_url = "https://api.mapbox.com"
        self.api_key = api_key

    def search_places(self, query, location_restriction, max_results=20, page_token=None):
        # Implement Mapbox-specific logic here
        print("Mapbox API called (not implemented)")
        return {"places": []}  # Placeholder