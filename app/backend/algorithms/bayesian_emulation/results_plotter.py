from decimal import Decimal

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
import contextily as ctx

from algorithms.bayesian_emulation.utilities.scaler import Scaler
from models import BayesianModel
from model_extensions import BayesianModelExtensions
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator
from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from api.clients.maps.routes_request import Coords

class ResultsPlotter:
    @staticmethod
    def generate_distance_plot(
        emulator: BayesianEmulator,
        start_x: int,
        start_y: int,
        start_name: str,
        output_path: str = "/tmp/plot",
        x_min: float = -15000,
        x_max: float = 10000,
        y_min: float = -8000,
        y_max: float = 8000,
        D_scaler: float = 1
    ):
        X, Y, distances = compute_distance_grid(emulator, start_x, start_y, x_min, x_max, y_min, y_max, D_scaler=D_scaler)
        distances = np.clip(distances, 0, 2)
        plot_distance_grid(X, Y, distances, start_x, start_y, output_path+".png", start_name)
        plot_map(X, Y, distances, start_x, start_y, output_path+"-map.png", start_name)
        
    @staticmethod
    def generate_diffs_plot(
        diff_x, 
        diff_y, 
        diffs,
        start_x: int,
        start_y: int,
        start_name: str,
        output_path: str = "/tmp/plot",
    ):
        plot_diffs_grid(diff_x, diff_y, diffs, start_x, start_y, output_path+".png", start_name)
        plot_diffs_map(diff_x, diff_y, diffs, start_x, start_y, output_path+"-map.png", start_name)

def plot_map(X, Y, distances, start_x, start_y, output_path, start_name):
    transformer = CoordTransformer()
    
    # Flatten grid
    x_flat = X.ravel()
    y_flat = Y.ravel()
    # Convert to EPSG
    x_flat, y_flat = transformer.transformToEPSG(x_flat, y_flat)
    # Reshape back to grid shape
    X = x_flat.reshape(X.shape)
    Y = y_flat.reshape(Y.shape)

    plt.figure(figsize=(12, 8))

    # Create normalization
    if np.min(distances) < 0:
        norm = TwoSlopeNorm(vmin=np.min(distances), vcenter=0, vmax=np.max(distances))
    else:
        norm = Normalize(vmin=0, vmax=np.max(distances))

    # Plot contour
    contour = plt.contourf(X, Y, distances, levels=50, cmap='viridis', norm=norm, alpha=0.8)
    plt.colorbar(contour, label='Travel Time from Start (hrs)')

    # Plot start point, convert to EPSG
    sx, sy = transformer.transformToEPSG(start_x, start_y)
    plt.scatter(sx, sy, c='lime', s=200, marker='*', edgecolor='black', label=start_name)

    # Add basemap (OpenStreetMap)
    ctx.add_basemap(plt.gca(), crs="EPSG:27700", source=ctx.providers.OpenStreetMap.Mapnik)

    plt.gca().set_xlabel('')
    plt.gca().set_ylabel('')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.title('Time taken to travel to destination from Warwick Avenue')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()

def plot_distance_grid(X, Y, distances, start_x, start_y, output_path, start_name):
    # Convert metres to kilometres
    X_km = X / 1000
    Y_km = Y / 1000
    start_x_km = start_x / 1000
    start_y_km = start_y / 1000

    cmap = plt.get_cmap('RdBu')
    
    if (np.min(distances) < 0):
        norm = TwoSlopeNorm(vmin=np.min(distances), vcenter=0, vmax=np.max(distances))
    else: 
        norm = TwoSlopeNorm(vmin=0, vcenter=0.001, vmax=np.max(distances))

    plt.figure(figsize=(12, 8))
    contour = plt.contourf(X_km, Y_km, distances, levels=50, cmap=cmap, norm=norm)
    plt.colorbar(contour, label='Travel Time from Start (hrs)')

    plt.scatter(start_x_km, start_y_km, c='lime', s=200, marker='*', edgecolor='black', label=start_name)
    plt.xlabel('Distance East/West from Big Ben (km)')
    plt.ylabel('Distance North/South from Big Ben (km)')
    plt.title('Travel Time from Start: Negative vs Positive', pad=20)
    plt.legend()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

def compute_distance_grid(emulator, start_x, start_y, x1, x2, y1, y2, grid_size=100, D_scaler=1):
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
            emulated =  D_scaler * emulator.emulate([start_x_scaled, start_y_scaled, X_scaled[i, j], Y_scaled[i, j]]) / 3600  # Convert to hours
            distances[i, j] = emulated
    return X, Y, distances


def plot_diffs_grid(diff_x, diff_y, diffs,start_x, start_y, output_path, start_name):
    diff_x_km = np.array(diff_x)/1000
    diff_y_km = np.array(diff_y)/1000
    start_x_km = start_x / 1000
    start_y_km = start_y / 1000

    diffs = diffs / 3600  # Convert to hours

    plt.figure(figsize=(12, 8))

    max_diff = max(np.max(np.abs(diffs)), -np.min(np.abs(diffs)))
    max_rnd = float(Decimal(max_diff * 2).to_integral_value(rounding='ROUND_CEILING') / Decimal(2))

    diff_norm = TwoSlopeNorm(vmin=-max_rnd, vcenter=0, vmax=max_rnd)

    # Create the scatter plot
    sc = plt.scatter(
        diff_x_km, diff_y_km, c=diffs, cmap='coolwarm', norm=diff_norm,
        s=250, edgecolor='black', linewidth=0.5, marker='o',
        label='Emulator–Model Δ'
    )
    plt.scatter(start_x_km, start_y_km, c='lime', s=200, marker='*', edgecolor='black', label=start_name)

    plt.colorbar(sc, label='Emulator–Model Δ (hrs)')

    plt.legend()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_diffs_map(diff_x, diff_y, diffs,start_x, start_y, output_path, start_name):
    transformer = CoordTransformer()

    diffs = diffs / 3600  # Convert to hours

    plt.figure(figsize=(12, 8))
    
    # transform to EPSG coords
    dx_epsg, dy_epsg = transformer.transformToEPSG(diff_x, diff_y)

    max_diff = max(np.max(np.abs(diffs)), -np.min(np.abs(diffs)))
    max_rnd = float(Decimal(max_diff * 2).to_integral_value(rounding='ROUND_CEILING') / Decimal(2))

    diff_norm = TwoSlopeNorm(vmin=-max_rnd, vcenter=0, vmax=max_rnd)

    # Create the scatter plot
    sc = plt.scatter(
        dx_epsg, dy_epsg, c=diffs, cmap='coolwarm', norm=diff_norm,
        s=250, edgecolor='black', linewidth=0.5, marker='o',
        label='Emulator–Model Δ'
    )

    # Plot start point, convert to EPSG
    sx, sy = transformer.transformToEPSG(start_x, start_y)
    plt.scatter(sx, sy, c='lime', s=200, marker='*', edgecolor='black', label=start_name)

    plt.colorbar(sc, label='Emulator–Model Δ (hrs)')

    # Add basemap (OpenStreetMap)
    ctx.add_basemap(plt.gca(), crs="EPSG:27700", source=ctx.providers.OpenStreetMap.Mapnik)
    plt.gca().images[-1].set_alpha(0.8)  # Set alpha to 80% transparency
    
    plt.gca().set_xlabel('')
    plt.gca().set_ylabel('')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()
