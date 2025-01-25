from rtree import index

class CoverageCalculator:
    def __init__(self, boundary, coverage_radius, geometry_handler):
        self.boundary = boundary
        self.coverage_radius = coverage_radius
        self.geometry_handler = geometry_handler
        self.spatial_index = index.Index()
        
    def build_spatial_index(self, halls):
        self.spatial_index = index.Index()
        for idx, hall in enumerate(halls):
            self.spatial_index.insert(idx, (hall[0], hall[1], hall[0], hall[1]))

    def calculate_coverage(self, points, halls):
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
