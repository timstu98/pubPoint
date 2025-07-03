from decimal import Decimal

import numpy as np
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from algorithms.bayesian_emulation.results_plotter import ResultsPlotter
from algorithms.bayesian_emulation.utilities.scaler import Scaler
from models import db, Location, Distance
import os
import csv
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from algorithms.bayesian_emulation.gp_hyperparameter_tuner import GPHyperparameterTuner
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

import numpy as np
import matplotlib.pyplot as plt

with app.app_context():    
    locations = []
    x_range = np.linspace(-15000, 10000, 70)
    y_range = np.linspace(-8000, 8000, 70)

    transformer = CoordTransformer()

    origin, new = Location.get_or_create(
                name="Warwick Avenue",
                lat=51.52323337318014,
                lng=-0.18382667001350628
            )
    
    # count = 1
    for x in x_range:
        for y in y_range:
            # if count == 3:
            #     count = 1
            # else:
            #     count+=1
            #     continue
            name = f"Plane_WA_{x}_{y}"
            location = Location.query.filter(
                db.func.lower(Location.name) == name.lower()
            ).first()
            if not location:
                raise Exception(f"Cannot find location {name}")
            locations.append(location)

    transformer = CoordTransformer()
    x_train = [] # Training Points, X_A
    D = [] # Known outputs, f(X_A)
    for destination in locations:
        x_j = to_x_input(origin, destination, transformer)
        d_j = get_distance(origin, destination)
        x_train.append(x_j)
        D.append(d_j)

    x_scaled = Scaler.scale(x_train)  
        
    Beta = 45*60 # "everywhere is 45 minutes away" - someone, probably
    #tuner = GPHyperparameterTuner(x_train, D, Beta)
    #theta, sigma = tuner.tune()
    theta, sigma = 0.2, 20 #hardcoded results from above optimisation
    print(f"Optimal theta: {theta}, sigma: {sigma}")
    
    bayesianEmulator = BayesianEmulator(Beta, sigma, theta, x_scaled, D)
    M = bayesianEmulator.compute_M()
    
    for destination in locations:
        x_j = to_x_input(origin, destination, transformer)
        x_j_scaled = Scaler.scale(x_j)
        emulated = bayesianEmulator.emulate(x_j_scaled)
        d_j = float(get_distance(origin, destination))
        diff = emulated - d_j
        if (diff > 20*60): # allow no more than 20 minutes difference at worst point
            raise Exception(f"Difference in emulated to training data is {diff}")


    BayesianModelExtensions.insert_bayesian_model("single-plane-full", M, x_scaled, D, Beta, sigma, theta)

    ResultsPlotter.generate_distance_plot(
        emulator=bayesianEmulator,
        start_x=-4173,
        start_y=2407,
        start_name="Start (Warwick Ave)"
    )

