from decimal import Decimal

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from algorithms.bayesian_emulation.utilities.scaler import Scaler
from models import BayesianModel
from model_extensions import BayesianModelExtensions
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from api.clients.maps.routes_request import Coords

class DistanceEmulator:
    @staticmethod
    def generate_distance_plot(
        emulator: BayesianEmulator,
        start_x: int,
        start_y: int,
        start_name: str,
        output_path: str = "/tmp/plot.png"
    ):
        # Grid boundaries (fixed)
        x1, y1 = -15000, -8000
        x2, y2 = 10000, 8000

        X, Y, distances = compute_distance_grid(emulator, start_x, start_y, x1, x2, y1, y2)
        plot_distance_grid(X, Y, distances, start_x, start_y, output_path, start_name)



def plot_distance_grid(X, Y, distances, start_x, start_y, output_path, start_name):
    # Convert metres to kilometres
    X_km = X / 1000
    Y_km = Y / 1000
    start_x_km = start_x / 1000
    start_y_km = start_y / 1000

    distances = np.clip(distances, 0, 5)

    cmap = plt.get_cmap('RdBu')
    
    if (np.min(distances) < 0):
        norm = TwoSlopeNorm(vmin=np.min(distances), vcenter=0, vmax=np.max(distances))
    else: 
        norm = TwoSlopeNorm(vmin=0, vcenter=0.001, vmax=np.max(distances))

    plt.figure(figsize=(12, 8))
    contour = plt.contourf(X_km, Y_km, distances, levels=50, cmap=cmap, norm=norm)
    plt.colorbar(contour, label='Distance from Start (hrs)')

    plt.scatter(start_x_km, start_y_km, c='lime', s=200, marker='*', edgecolor='black', label=start_name)
    plt.xlabel('Distance East/West from Big Ben (km)')
    plt.ylabel('Distance North/South from Big Ben (km)')
    plt.title('Distance from Start: Negative vs Positive', pad=20)
    plt.legend()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

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

    start_x_scaled, start_y_scaled = Scaler.scale([start_x,start_y])
    x_vals_scaled = Scaler.scale_x(x_vals)
    y_vals_scaled = Scaler.scale_y(y_vals)
    X_scaled, Y_scaled = np.meshgrid(x_vals_scaled, y_vals_scaled)
    distances = np.zeros_like(X_scaled)

    for i in range(grid_size):
        for j in range(grid_size):
            emulated =  emulator.emulate([start_x_scaled, start_y_scaled, X_scaled[i, j], Y_scaled[i, j]]) / 3600  # Convert to hours
            distances[i, j] = emulated
    return X, Y, distances
