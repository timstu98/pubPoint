from decimal import Decimal
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from algorithms.bayesian_emulation.distance_emulator import DistanceEmulator
from algorithms.bayesian_emulation.utilities.scaler import Scaler
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
        distance_entry = Distance.query.filter_by(
                    origin_id=origin.id,
                    destination_id=destination.id
                ).first()

        if not distance_entry:
            raise Exception(f"Cannot find distance for {origin} -> {destination}")
            
        return distance_entry.seconds

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
    for origin in locations:
        for destination in locations:
            x_j = to_x_input(origin, destination, transformer)
            d_j = get_distance(origin, destination)
            x_train.append(x_j)
            D.append(d_j)

    x_scaled = Scaler.scale(x_train)

    Beta = 45 # Beta = E[f(x)] : "everywhere in London is 45 minutes away" - someone, probably
    sigma = 1 # sigma = standard deviation : estimate
    theta = 0.1 # theta = correlation-scale of the gaussian process : estimate

    bayesianEmulator = BayesianEmulator(Beta, sigma, theta, x_scaled, D)

    M = bayesianEmulator.compute_M()

    for origin in locations:
        for destination in locations:
            x_j = Scaler.scale(to_x_input(origin, destination, transformer))
            emulated = bayesianEmulator.emulate(x_j)
            d_j = float(get_distance(origin, destination))

            diff = emulated - d_j

            if diff > 10:
                raise f"Error in training Bayesian Emulator - predictions of distance for training data over 10 seconds different from provided values. {origin.name}-{destination.name} returned difference of {diff}"
                
    BayesianModelExtensions.insert_bayesian_model("initial-set-16", M, x_scaled, D, Beta, sigma, theta) #TODO resave this with x_scaled not x_train

    DistanceEmulator.generate_distance_plot(
        emulator=bayesianEmulator,
        start_x=-4173,
        start_y=2407,
        start_name="Start (Warwick Ave)"
    )

