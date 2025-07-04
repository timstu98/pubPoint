from decimal import Decimal

import numpy as np
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from algorithms.bayesian_emulation.results_plotter import ResultsPlotter
from algorithms.bayesian_emulation.utilities.scaler import Scaler
from algorithms.bayesian_emulation.training.full_5000_LHS.LHS_location_generator import LHSLocationGenerator
from algorithms.bayesian_emulation.gp_hyperparameter_tuner import GPHyperparameterTuner
from models import db, Location, Distance
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
    locations = LHSLocationGenerator.generate_locations(num_samples=5000, seed=123)

    transformer = CoordTransformer()
    x_train = [] # Training Points, X_A
    D = [] # Known outputs, f(X_A)
    for origin, destination in locations:
        x_j = to_x_input(origin, destination, transformer)
        d_j = get_distance(origin, destination)
        x_train.append(x_j)
        D.append(d_j)

    x_scaled = Scaler.scale(x_train)

    is_logged = True

    if is_logged:
        D_logged = np.log(np.array(D))
        Beta = D_logged.mean() # Beta = E[f(x)] : best estimate of the mean of the log-transformed distances
        # tuner = GPHyperparameterTuner(x_train, D_logged, Beta)
        # theta, sigma = tuner.tune()
        theta, sigma = 0.2, 0.00001 # These values are optimised from GPHyperparameterTuner
        print(f"Optimal theta: {theta}, sigma: {sigma}")
        noise = 1e-12
    else:
        Beta = 45*60 # Beta = E[f(x)] : "everywhere in London is 45 minutes away" - someone, probably
        sigma = 20 # sigma = standard deviation : optimised value from GPHyperparameterTuner
        theta = 0.2 # theta = correlation-scale of the gaussian process : optimised value from GPHyperparameterTuner
        noise = 1e-6

    bayesianEmulator = BayesianEmulator(Beta, sigma, theta, x_scaled, D, noise=noise, is_logged=is_logged)
    M = bayesianEmulator.compute_M()

    for origin, destination in locations:
        x_j = Scaler.scale(to_x_input(origin, destination, transformer))
        emulated = bayesianEmulator.emulate(x_j)
        d_j = float(get_distance(origin, destination))

        diff = emulated - d_j

        if diff > 20*60:
            print(f"Error in training Bayesian Emulator - predictions of distance for training data over 20 minutes different from provided values. {origin.name}-{destination.name} returned difference of {diff}")
            raise
    BayesianModelExtensions.insert_bayesian_model("full-5000-lhs-logged", M, x_scaled, D, Beta, sigma, theta, noise, is_logged)

    ResultsPlotter.generate_distance_plot(
        emulator=bayesianEmulator,
        start_x=-4173,
        start_y=2407,
        start_name="Start (Warwick Ave)"
    )

