from pyproj import Transformer

class CoordTransformer:
    def __init__(self):
        '''
        To make coordinates uniform, we measure every point in Cartesian distance using a standard projection
        We choose a transformer from WGS84 (Lat/Lon) to British National Grid (EPSG:27700)
        Then use this to calculate the distance north/east of each point from Big Ben (51.5007,0.1246)
        '''
        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700")
        self.x_base, self.y_base, _ = self.transformer.transform(51.5007,0.1246, 0)
    def transform(self, lat, lng):
        x, y, _ = self.transformer.transform(lat, lng, 0)
        return x-self.x_base, y-self.y_base