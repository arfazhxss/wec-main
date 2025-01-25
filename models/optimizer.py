import numpy as np
import pandas as pd
from shapely.geometry import Polygon, Point
from sklearn.cluster import KMeans
from utils.geometry_handler import GeometryHandler
from utils.coverage_calculator import CoverageCalculator
from visualization.plotter import FireHallPlotter

class FireHallOptimizer:
    def __init__(self, csv_path, coverage_radius=2.5, existing_halls=None):
        self.coverage_radius = coverage_radius
        self.radius_in_degrees = 0.022524807889027443
        self.geometry_handler = GeometryHandler()
        self.boundary = self._load_boundary(csv_path)
        self.map_area = self.geometry_handler.calculate_area(self.boundary)
        self.coverage_calculator = CoverageCalculator(
            self.boundary, 
            self.coverage_radius, 
            self.geometry_handler
        )
        self.existing_halls = existing_halls or []

    def _load_boundary(self, csv_path):
        df = pd.read_csv(csv_path)
        df = df.dropna()
        coords = list(zip(df['Longitude'], df['Latitude']))
        coords.append(coords[0])
        return Polygon(coords)

    def _generate_test_points(self, num_points=1000):
        minx, miny, maxx, maxy = self.boundary.bounds
        points = []
        rng = np.random.default_rng(42)
        while len(points) < num_points:
            point = Point(
                rng.uniform(minx, maxx),
                rng.uniform(miny, maxy)
            )
            if self.boundary.contains(point):
                points.append((point.x, point.y))
        return points

    def optimize_hall_placement(self):
        test_points = self._generate_test_points(1000)
        num_additional_halls = max(0, int(np.ceil(1.5 * self.map_area / (np.pi * self.coverage_radius**2))) - len(self.existing_halls))
        
        halls = list(self.existing_halls)
        
        if num_additional_halls > 0:
            uncovered_points = self._get_uncovered_points(test_points)
            
            if uncovered_points:
                halls = self._optimize_additional_halls(halls, uncovered_points, num_additional_halls, test_points)
        
        return halls

    def _get_uncovered_points(self, test_points):
        uncovered_points = []
        for point in test_points:
            coverage_count = 0
            for hall in self.existing_halls:
                if self.geometry_handler.calculate_distance(point, hall) <= self.coverage_radius:
                    coverage_count += 1
            if coverage_count < 2:
                uncovered_points.append(point)
        return uncovered_points

    def _optimize_additional_halls(self, halls, uncovered_points, num_additional_halls, test_points):
        best_coverage = 0
        best_halls = halls
        
        for n_halls in range(1, num_additional_halls + 1):
            kmeans = KMeans(
                n_clusters=min(n_halls, len(uncovered_points)),
                n_init=10
            )
            kmeans.fit(uncovered_points)
            
            current_halls = halls + [(center[0], center[1]) for center in kmeans.cluster_centers_]
            current_coverage = self.coverage_calculator.calculate_coverage(test_points, current_halls)
            
            if current_coverage > best_coverage:
                best_coverage = current_coverage
                best_halls = current_halls
            
            if current_coverage >= 1.1:
                break
        
        return best_halls
