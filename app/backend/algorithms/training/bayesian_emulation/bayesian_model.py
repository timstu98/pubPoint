
import os
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import Coords, RoutesRequest


API_KEY = os.getenv("API_KEY", "api_key")

api = GoogleRoutesApi(API_KEY)
farringdon = Coords(51.51996102,-0.103582415)
paddington = Coords(51.51499491,-0.173789485)
rqst = RoutesRequest([farringdon, paddington], [farringdon, paddington])

print(api.matrix(rqst))
