import numpy as np
from shapely.ops import transform
from pyproj import Transformer
from geopy import distance

class GeometryHandler:
    def __init__(self):
        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        self.inv_transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
        self._distance_cache = {}

    def calculate_area(self, polygon):
        transformed_polygon = transform(self.transformer.transform, polygon)
        return transformed_polygon.area / 1_000_000

    def calculate_distance(self, point1, point2):
        cache_key = (point1, point2)
        if cache_key not in self._distance_cache:
            self._distance_cache[cache_key] = distance.distance(
                (point1[1], point1[0]), 
                (point2[1], point2[0])
            ).km
        return self._distance_cache[cache_key]
