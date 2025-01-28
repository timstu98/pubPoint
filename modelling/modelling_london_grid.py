import folium

# import matplotlib.pyplot as plt
from math import pi
import numpy as np
import math


def stretching_fn(normalised_value, aggressivity):
    """Use function and then scale using max radius"""
    if not (0 <= aggressivity < 1):
        print("You've used it wrong ya idiot.")
    return math.log(1 - aggressivity * normalised_value) / math.log(1 - aggressivity)


def elipsis_modelling():
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


def generate_rectangles(top_left, bottom_right, num_lat_divisions, num_lng_divisions):
    """
    Divide an area into smaller rectangles and return their corner coordinates.

    :param top_left: Tuple (lat, lng) of the top-left corner of the overall area.
    :param bottom_right: Tuple (lat, lng) of the bottom-right corner of the overall area.
    :param num_lat_divisions: Number of divisions along the latitude axis.
    :param num_lng_divisions: Number of divisions along the longitude axis.
    :return: List of rectangles as tuples ((top_left_lat, top_left_lng), (bottom_right_lat, bottom_right_lng)).
    """
    top_lat, left_lng = top_left
    bottom_lat, right_lng = bottom_right

    lat_step = (top_lat - bottom_lat) / num_lat_divisions
    lng_step = (right_lng - left_lng) / num_lng_divisions

    rectangles = []

    for i in range(num_lat_divisions):
        for j in range(num_lng_divisions):
            rect_top_left = (top_lat - i * lat_step, left_lng + j * lng_step)
            rect_bottom_right = (top_lat - (i + 1) * lat_step, left_lng + (j + 1) * lng_step)
            rectangles.append((rect_top_left, rect_bottom_right))

    return rectangles


def plot_rectangles_on_map(rectangles):
    # Create a map centered around London
    m = folium.Map(location=[51.509865, -0.118092], zoom_start=10)

    # Add rectangles to the map
    for top_left, bottom_right in rectangles:
        folium.Rectangle(bounds=[top_left, bottom_right], color="blue", fill=True, fill_color="blue", fill_opacity=0.1).add_to(m)

    # Save the map to an HTML file
    m.save("modelling/london_rectangles.html")


def get_rectangles():
    # Define the bounding box for London (approximate).
    # These coordinates can be adjusted as needed.
    london_top_left = (51.6723432, -0.563)
    london_bottom_right = (51.3849401, 0.278)

    # Set the number of divisions.
    num_lat_divisions = 8  # Adjust based on desired granularity.
    num_lng_divisions = 12  # Adjust based on desired granularity.

    # Generate rectangles.
    rectangles = generate_rectangles(london_top_left, london_bottom_right, num_lat_divisions, num_lng_divisions)

    # Plot rectangles on the map
    plot_rectangles_on_map(rectangles)


if __name__ == "__main__":
    """Please be aware, the x and y coordinates are swapped around from google maps."""
    get_rectangles()
