from decimal import Decimal

import numpy as np
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from algorithms.bayesian_emulation.results_plotter import ResultsPlotter
from algorithms.bayesian_emulation.utilities.scaler import Scaler
from api.clients.maps.map_clients import GoogleRoutesApi
from api.clients.maps.routes_request import Coords, RoutesRequest
from models import db, Location, Distance
import os
import csv
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from model_extensions import BayesianModelExtensions

app, env = create_flask_app()

def get_distance(origin, destination):
    if origin == destination:
        return 0
    else:
        return get_distance_from_db_or_api(origin, destination)

def get_distance_from_db_or_api(origin, destination):

    distance_entry, isNew = Distance.get_or_create(origin, destination)

    if not isNew:
        distance_in_db = distance_entry.seconds
        if distance_in_db > 0:
            return distance_in_db
    
    raise Exception(f"Cannot find distance for {origin} -> {destination}")
    # Commented out to avoid API calls if something goes wrong

    # api = GoogleRoutesApi(env["API_KEY"])
    # rqst = RoutesRequest([origin.coords], [destination.coords])

    # result = api.matrix(rqst)
    # if result:
        
    #     # Update with API results
    #     distance_entry.update_distance(
    #         meters=result[0]['distanceMeters'],
    #         seconds=result[0]['staticDuration'].rstrip('s')
    #     )
        
    #     # Commit the distance update
    #     db.session.commit()
    #     print(f"Successfully wrote distance: {distance_entry.origin_id} -> {distance_entry.destination_id} = {distance_entry.seconds}s")

def to_x_input(origin, destination, transformer):
    x_origin, y_origin = transformer.transform(origin.lat, origin.lng)
    x_dest, y_dest = transformer.transform(destination.lat, destination.lng)
    return [
        Decimal(str(x_origin)),  # Convert via string to avoid floating-point inaccuracies
        Decimal(str(y_origin)),
        Decimal(str(x_dest)),
        Decimal(str(y_dest))
    ]

with app.app_context():    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'data', 'starting_locations.csv')

    locations = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name']
            location = Location.query.filter(
                db.func.lower(Location.name) == name.lower()
            ).first()
            if not location:
                raise Exception(f"Cannot find location {name}")
            locations.append(location)

    transformer = CoordTransformer()
    x_train = [] # Training Points, X_A
    D = [] # Known outputs, f(X_A)
    
    origin, new = Location.get_or_create(
                name="Warwick Avenue",
                lat=51.52323337318014,
                lng=-0.18382667001350628
            )

    transformer = CoordTransformer()
    x_train = [] # Training Points, X_A
    D = [] # Known outputs, f(X_A)
    for destination in locations:
        x_j = to_x_input(origin, destination, transformer)
        d_j = get_distance(origin, destination)
        x_train.append(x_j)
        D.append(d_j)

    x_scaled = Scaler.scale(x_train)

    model = BayesianModelExtensions.get_bayesian_model_by_name("single-plane-full")  
    bayesianEmulator = BayesianModelExtensions.prepare_emulator(model)
    
    diffs = []

    for destination in locations:
        x_j = to_x_input(origin, destination, transformer)
        x_j_scaled = Scaler.scale(x_j)
        emulated = bayesianEmulator.emulate(x_j_scaled)
        d_j = float(get_distance(origin, destination))
        diff = emulated - d_j
        diffs.append((destination.name, diff))

    sorted = diffs.copy()
    sorted.sort(key=lambda x: abs(x[1]), reverse=True)

    print("Top 10 largest differences:")
    for name, diff in sorted[:10]:
        print(f"{name}: {diff:.2f} seconds")

    ResultsPlotter.generate_diffs_plot(
        np.array(x_train, dtype=float)[:, 2],
        np.array(x_train, dtype=float)[:, 3],
        np.array([d[1] for d in diffs]),
        np.array(x_train, dtype=float)[0, 0],
        np.array(x_train, dtype=float)[0, 1],
        "Start (Warwick Ave)"
    )
        
    

