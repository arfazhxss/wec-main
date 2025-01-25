"""
R-Tree: https://rtree.readthedocs.io/en/latest/

"""
from rtree import index

class CoverageCalculator:
    """
    A class that calculates coverage metrics for a set of points using R-tree spatial indexing.
    Uses efficient spatial querying to determine coverage overlap between halls and points.
    """
    
    def __init__(self, boundary, coverage_radius, geometry_handler):
        """
        Initialize the CoverageCalculator with boundary and coverage parameters.
        
        Args:
            boundary: The boundary limits of the coverage area
            coverage_radius: Radius within which a hall can provide coverage
            geometry_handler: Handler object for geometric calculations
        """
        self.boundary = boundary
        self.coverage_radius = coverage_radius
        self.geometry_handler = geometry_handler
        self.spatial_index = index.Index()
        
    def build_spatial_index(self, halls):
        """
        Builds an R-tree spatial index for efficient spatial queries of halls (AI Debugs)
        
        Args:
            halls: List of hall coordinates [(x1, y1), (x2, y2), ...]
            
        Note:
            - Creates point geometries in R-tree for each hall
            - R-tree enables O(log n) spatial queries instead of O(n) linear search
        """
        self.spatial_index = index.Index()
        for idx, hall in enumerate(halls):
            self.spatial_index.insert(idx, (hall[0], hall[1], hall[0], hall[1]))

    def calculate_coverage(self, points, halls):
        """
        Calculates the coverage ratio for a set of points by the given halls.
        
        Args:
            points: List of point coordinates to check for coverage
            halls: List of hall coordinates that provide coverage
            
        Returns:
            float: Coverage ratio between 0 and 1, where:
                  0 means no points are covered
                  1 means all points have optimal coverage
                  
        Algorithm (AI Generation, Optimization and Debugs):
            1. Builds spatial index for halls
            2. For each point:
               - Queries nearby halls using R-tree within coverage radius
               - Counts halls that provide actual coverage
               - Normalizes coverage by factor of 1.1
            3. Returns average coverage across all points
        """
        self.build_spatial_index(halls)
        total_coverage = 0
        
        for point in points:
            coverage_count = 0
            nearby_halls = list(self.spatial_index.intersection((
                point[0] - self.coverage_radius/100,
                point[1] - self.coverage_radius/100,
                point[0] + self.coverage_radius/100,
                point[1] + self.coverage_radius/100
            )))
            
            for hall_idx in nearby_halls:
                if self.geometry_handler.calculate_distance(point, halls[hall_idx]) <= self.coverage_radius:
                    coverage_count += 1
            
            total_coverage += min(coverage_count / 1.1, 1.0)
                    
        return total_coverage / len(points) if points else 0
