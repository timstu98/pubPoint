from decimal import Decimal
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask 
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from api.clients.maps.routes_request import Coords
from models import BayesianModel, db
from dotenv import load_dotenv
import os
import csv
import numpy as np
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from model_extensions import BayesianModelExtensions
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm 

if "/app" not in sys.path:
    print("Ensure you set the PYTHONPATH to ensure relative imports work correctly.")

load_dotenv(dotenv_path="/app/.env")

### Env variables
DB_USER = os.getenv("MYSQL_USER", "user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_NAME = os.getenv("MYSQL_DATABASE", "DB_NAME")
API_KEY = os.getenv("API_KEY", "api_key")
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
TEST_FUNCTIONALITY_MODE = os.getenv("TEST_FUNCTIONALITY_MODE", "false").lower() == "true"

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

def to_x_input(origin, destination, transformer):
    x_origin, y_origin = transformer.transform(origin.latitude, origin.longitude)
    x_dest, y_dest = transformer.transform(destination.latitude, destination.longitude)
    return [
        Decimal(str(x_origin)),
        Decimal(str(y_origin)),
        Decimal(str(x_dest)),
        Decimal(str(y_dest))
    ]

with app.app_context():    

    transformer = CoordTransformer()

    model:BayesianModel = BayesianModelExtensions.get_bayesian_model_by_name("initial-set-4")
    
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

    emulator = BayesianEmulator(model.beta, model.sigma, model.theta, x_train, D, M)

    # origin = Coords(51.48827, -0.11138) # Kennington
    # destination = Coords(51.52118, -0.13946) # BT Tower

    # distance = emulator.emulate(to_x_input(origin, destination, transformer))  

    # x,y = transformer.transform(51.564, -0.320)
    # xb,yb = transformer.transform(51.433, 0.012)
    # xc,yc = transformer.transform(51.52328, -0.18383)
    

    x1, y1 = -15000, -8000  # grid corner 1
    x2, y2 = 10000, 8000   # grid corner 2
    start_x, start_y = -4173, 2407  # fixed starting position, Warwick Avenue

    # Create a grid of points
    grid_size = 100
    x_values = np.linspace(x1, x2, grid_size)
    y_values = np.linspace(y1, y2, grid_size)
    X, Y = np.meshgrid(x_values, y_values)

    # Calculate distances from the starting position to each grid point
    distances = np.zeros_like(X)

    for i in range(grid_size):
        for j in range(grid_size):
            distances[i,j] = (emulator.emulate([start_x, start_y, X[i,j], Y[i,j]])) / 3600 # to hrs

    # Set up a diverging colormap (blue for negative, red for positive)
    cmap = plt.get_cmap('RdBu')  # Alternatives: 'coolwarm', 'bwr', 'seismic'

    # Normalize colors around zero (critical for clarity)
    norm = TwoSlopeNorm(vmin=np.min(distances), vcenter=0, vmax=np.max(distances))

    # Plot
    plt.figure(figsize=(12, 8))
    contour = plt.contourf(X, Y, distances, levels=50, cmap=cmap, norm=norm)
    cbar = plt.colorbar(contour, label='Distance from Start (Negative vs Positive)')

    # Highlight zero distance (if it exists in your data)
    if np.any(distances == 0):
        plt.contour(X, Y, distances, levels=[0], colors='black', linewidths=2)

    # Mark start point
    plt.scatter(start_x, start_y, c='lime', s=200, marker='*', edgecolor='black', label=f'Start ({start_x}, {start_y})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Distance from Start: Negative vs Positive', pad=20)
    plt.legend()

    # Save to file (for Docker export)
    plt.savefig('/tmp/plot2.png', dpi=300, bbox_inches='tight')
    plt.show()

    banana = 0



