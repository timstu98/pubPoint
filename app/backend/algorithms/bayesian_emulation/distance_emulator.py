import os
import sys
from decimal import Decimal

from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from flask import Flask
from models import BayesianModel, db
from model_extensions import BayesianModelExtensions
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from api.clients.maps.routes_request import Coords

# Ensure correct module path
if "/app" not in sys.path:
    print("Ensure you set the PYTHONPATH to ensure relative imports work correctly.")

def load_environment():
    load_dotenv(dotenv_path="/app/.env")
    return {
        "DB_USER": os.getenv("MYSQL_USER", "user"),
        "DB_PASSWORD": os.getenv("MYSQL_PASSWORD", "password"),
        "DB_HOST": os.getenv("MYSQL_HOST", "mysql"),
        "DB_NAME": os.getenv("MYSQL_DATABASE", "DB_NAME"),
        "API_KEY": os.getenv("API_KEY", "api_key"),
        "DATABASE_URI": f"mysql+pymysql://{os.getenv('MYSQL_USER', 'user')}:{os.getenv('MYSQL_PASSWORD', 'password')}@{os.getenv('MYSQL_HOST', 'mysql')}/{os.getenv('MYSQL_DATABASE', 'DB_NAME')}",
        "TEST_FUNCTIONALITY_MODE": os.getenv("TEST_FUNCTIONALITY_MODE", "false").lower() == "true"
    }

def create_flask_app(database_uri: str):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def to_x_input(origin: Coords, destination: Coords, transformer: CoordTransformer):
    x_origin, y_origin = transformer.transform(origin.latitude, origin.longitude)
    x_dest, y_dest = transformer.transform(destination.latitude, destination.longitude)
    return [Decimal(str(val)) for val in (x_origin, y_origin, x_dest, y_dest)]

def prepare_emulator(model: BayesianModel) -> BayesianEmulator:
    x_train = []
    row = []
    row_index = 0
    for el in model.x_train_elements:
        if el.row > row_index:
            x_train.append(row)
            row = []
            row_index += 1
        row.append(el.value)
    x_train.append(row)

    D = [el.value for el in model.d_elements]
    M = [el.value for el in model.m_vector_elements]

    return BayesianEmulator(model.beta, model.sigma, model.theta, x_train, D, M)

def compute_distance_grid(emulator, start_x, start_y, x1, x2, y1, y2, grid_size=100):
    x_vals = np.linspace(x1, x2, grid_size)
    y_vals = np.linspace(y1, y2, grid_size)
    X, Y = np.meshgrid(x_vals, y_vals)
    distances = np.zeros_like(X)

    for i in range(grid_size):
        for j in range(grid_size):
            distances[i, j] = emulator.emulate([start_x, start_y, X[i, j], Y[i, j]]) / 3600  # Convert to hours
    return X, Y, distances

def plot_distance_grid(X, Y, distances, start_x, start_y, output_path):
    cmap = plt.get_cmap('RdBu')
    norm = TwoSlopeNorm(vmin=np.min(distances), vcenter=0, vmax=np.max(distances))

    plt.figure(figsize=(12, 8))
    contour = plt.contourf(X, Y, distances, levels=50, cmap=cmap, norm=norm)
    plt.colorbar(contour, label='Distance from Start (hrs)')

    plt.scatter(start_x, start_y, c='lime', s=200, marker='*', edgecolor='black', label='Start (Warwick Ave)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Distance from Start: Negative vs Positive', pad=20)
    plt.legend()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

def main():
    env = load_environment()
    app = create_flask_app(env["DATABASE_URI"])

    with app.app_context():
        model = BayesianModelExtensions.get_bayesian_model_by_name("initial-set-5")
        emulator = prepare_emulator(model)

        # Grid boundaries and start point
        x1, y1 = -15000, -8000
        x2, y2 = 10000, 8000
        start_x, start_y = -4173, 2407 # Warwick Avenue

        X, Y, distances = compute_distance_grid(emulator, start_x, start_y, x1, x2, y1, y2)
        plot_distance_grid(X, Y, distances, start_x, start_y, "/tmp/plot.png")

if __name__ == "__main__":
    main()
