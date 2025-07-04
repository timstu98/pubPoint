from algorithms.bayesian_emulation.coord_transformer import CoordTransformer
from scipy.stats import qmc
from models import Location

class LHSLocationGenerator:
    @staticmethod
    def generate_locations(num_samples=5000, seed=123):
        locations = []

        x_bounds = [-15000, 10000]  # for both origin_x and destination_x
        y_bounds = [-8000, 8000]    # for both origin_y and destination_y

        transformer = CoordTransformer()

        # Create 4D LHS
        sampler = qmc.LatinHypercube(d=4, seed=seed)
        sample = sampler.random(n=num_samples)

        # Scale each dimension
        bounds = [x_bounds, y_bounds, x_bounds, y_bounds]
        scaled_sample = qmc.scale(sample, [b[0] for b in bounds], [b[1] for b in bounds])

        for i, (ox, oy, dx, dy) in enumerate(scaled_sample):
            origin_lat, origin_lng = transformer.transformBack(ox, oy)
            dest_lat, dest_lng = transformer.transformBack(dx, dy)
        
            origin_name = f"LHS_Origin_{i}"
            dest_name = f"LHS_Dest_{i}"
            
            origin, _ = Location.get_or_create(name=origin_name, lat=origin_lat, lng=origin_lng)
            destination, _ = Location.get_or_create(name=dest_name, lat=dest_lat, lng=dest_lng)

            locations.append((origin, destination))
        
        return locations