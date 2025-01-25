import matplotlib.pyplot as plt
from math import pi
import numpy as np
import math


def stretching_fn(normalised_value, aggressivity):
    """Use function and then scale using max radius"""
    if not (0 <= aggressivity < 1):
        print("You've used it wrong ya idiot.")
    return math.log(1 - aggressivity * normalised_value) / math.log(1 - aggressivity)


if __name__ == "__main__":
    """Please be aware, the x and y coordinates are swapped around from google maps."""

    centre_point = (-0.132653, 51.509408)
    max_x_radius = 0.20  # km, max radius of the x-axis
    max_y_radius = 0.15  # km, max radius of the y-axis
    no_points = 5
    no_elipsses = 8
    aggresivity_stretch = 0.9  # Has to be between 0 and 1. 0 will give a linear spacing, >1 and function is not valid

    u = centre_point[0]  # x-position of the center
    v = centre_point[1]  # y-position of the center
    # stretched_max_x_radius = max_x_radius / stretching_fn(1, aggresivity_stretch)
    # stretched_max_y_radius = max_y_radius / stretching_fn(1, aggresivity_stretch)

    normalised_values = np.linspace(0, 1, no_elipsses)
    normalised_values = normalised_values[1:]
    x_radius, y_radius, stretched_values = [], [], []
    for i, norm_val in enumerate(normalised_values):
        # print(i, norm_val, stretching_fn(norm_val, aggresivity_stretch))
        stretched_values.append(stretching_fn(norm_val, aggresivity_stretch))
        # x_radius.append(norm_val * stretching_fn(norm_val, aggresivity_stretch) * stretched_max_x_radius)
        # y_radius.append(norm_val * stretching_fn(norm_val, aggresivity_stretch) * stretched_max_y_radius)
        x_radius.append(stretched_values[-1] * max_x_radius)
        y_radius.append(stretched_values[-1] * max_y_radius)
    print(x_radius)
    print(y_radius)
    # radiuss = zip(x_radius, y_radius)

    t_line = np.linspace(0, 2 * pi, 100)
    t_scatter = np.linspace(0, 2 * pi, no_points + 1)[:-1]
    scatter_offset = (2 * pi / no_points) / 2
    print("Number of searches: " + str(no_points * no_elipsses))

    fig, ax = plt.subplots()
    im_bottom_left = (51.328877, -0.437017)
    im_top_left = (51.670743, -0.497409)
    im_bottom_right = (51.373541, 0.277825)
    left = im_top_left[1]
    right = im_bottom_right[1]
    bottom = im_bottom_left[0]
    top = im_top_left[0]
    extents = [left, right, bottom, top]

    img = plt.imread("modelling/london-annotated.jpg")
    plt.grid(color="lightgray", linestyle="--")
    ax.imshow(img, extent=extents)
    search_points = []
    for i in range(len(x_radius)):
        x_rad = x_radius[i]
        y_rad = y_radius[i]
        y_line = u + x_rad * np.cos(t_line)
        x_line = v + y_rad * np.sin(t_line)
        plt.plot(y_line, x_line)
        if i % 2:
            y_scatter = u + x_rad * np.cos(t_scatter)
            x_scatter = v + y_rad * np.sin(t_scatter)
        else:
            y_scatter = u + x_rad * np.cos(t_scatter + scatter_offset)
            x_scatter = v + y_rad * np.sin(t_scatter + scatter_offset)
        search_points.extend((y_scatter, x_scatter))
        plt.scatter(y_scatter, x_scatter)
    plt.suptitle("agg:" + str(aggresivity_stretch))
    plt.show()
    print("Length search points:", len(search_points))

    """
    TODO:
    Fix first circvle
    Add 1km, 2km and 2.5km circles around points
    Add these to google map to see where they would be ???? maybe not bit complicated. Maybe test a couple out
    Checkl cost of running this search -> be more precise
    Run just the inner like 4 rings for now. 
    
    ...
    Visualise the pubs I have already got on a map.
    Visualise the dots
    """
