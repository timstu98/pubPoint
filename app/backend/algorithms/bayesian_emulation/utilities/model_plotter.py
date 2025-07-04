from algorithms.bayesian_emulation.utilities.create_flask_app import create_flask_app
from algorithms.bayesian_emulation.results_plotter import ResultsPlotter
from model_extensions import BayesianModelExtensions
from models import db

app, env = create_flask_app()

with app.app_context():
    # Create tables if they don't exist
    db.create_all()    
    model = BayesianModelExtensions.get_bayesian_model_by_name("single-plane-full")  
    bayesianEmulator = BayesianModelExtensions.prepare_emulator(model)

    ResultsPlotter.generate_distance_plot(
        emulator=bayesianEmulator,
        start_x=-4173,
        start_y=2407,
        start_name="Start (Warwick Ave)"
    )
    