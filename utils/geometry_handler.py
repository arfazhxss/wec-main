import numpy as np
from shapely.ops import transform
from pyproj import Transformer
from geopy import distance

class GeometryHandler:
    """
    A class to handle geometric transformations and calculations.

    This class provides methods to transform geographic coordinates and calculate
    areas and distances using different coordinate reference systems.

    Attributes:
        transformer (Transformer): A transformer for converting from EPSG:4326 to EPSG:3857.
        inv_transformer (Transformer): A transformer for converting from EPSG:3857 to EPSG:4326.
        _distance_cache (dict): A cache to store calculated distances between points.
    """
    def __init__(self):
        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        self.inv_transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
        self._distance_cache = {}

    def calculate_area(self, polygon):
        """
        Calculate the area of a polygon in square kilometers.

        This method transforms the given polygon from geographic coordinates
        (EPSG:4326) to projected coordinates (EPSG:3857) and calculates its area.

        Args:
            polygon (shapely.geometry.Polygon): The polygon to calculate the area for.

        Returns:
            float: The area of the polygon in square kilometers.

        For more information on shapely and its operations, visit:
        https://shapely.readthedocs.io/en/stable/manual.html
        """
        transformed_polygon = transform(self.transformer.transform, polygon)
        return transformed_polygon.area / 1_000_000
    
    def calculate_distance(self, point1, point2):
        """
        Calculate the distance between two geographic points in kilometers.

        This method calculates the geodesic distance between two points
        specified in geographic coordinates (latitude, longitude).

        Args:
            point1 (tuple): The first point as a (longitude, latitude) tuple.
            point2 (tuple): The second point as a (longitude, latitude) tuple.

        Returns:
            float: The distance between the two points in kilometers.

        For more information on geopy and its distance calculations, visit:
        https://geopy.readthedocs.io/en/stable/#module-geopy.distance
        """
        cache_key = (point1, point2)
        if cache_key not in self._distance_cache:
            self._distance_cache[cache_key] = distance.distance(
                (point1[1], point1[0]), 
                (point2[1], point2[0])
            ).km
        return self._distance_cache[cache_key]
