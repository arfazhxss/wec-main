from models.optimizer import FireHallOptimizer
from visualization.plotter import FireHallPlotter

def main():
    """
    Main function to analyze fire hall placements over different years.
    
    This function reads CSV files containing coordinates for different years,
    optimizes fire hall placements, calculates coverage, and plots the results.
    
    Resources:
    - FireHallOptimizer: https://example.com/firehalloptimizer
    - FireHallPlotter: https://example.com/firehallplotter
    """
    csv_files = [
        (1963, 'assets/coordinates1963.csv'),
        (2005, 'assets/coordinates2005.csv'),
        (2011, 'assets/coordinates2011.csv')
    ]
    
    existing_halls = []
    hall_years = []
    plotter = FireHallPlotter()
    
    for year, csv_path in csv_files:
        print(f"\nAnalyzing {year} boundaries:")
        print("-" * 30)
        
        optimizer = FireHallOptimizer(csv_path, existing_halls=existing_halls)
        print(f"Total Map Area: {optimizer.map_area:.2f} sq km")
        
        halls = optimizer.optimize_hall_placement()
        
        hall_years.extend([year] * (len(halls) - len(existing_halls)))
        
        coverage = optimizer.coverage_calculator.calculate_coverage(
            optimizer._generate_test_points(2000),
            halls
        )
        
        print(f"Existing halls: {len(existing_halls)}")
        print(f"New halls added: {len(halls) - len(existing_halls)}")
        print(f"Total halls: {len(halls)}")
        print(f"Coverage: {coverage*100:.2f}%")
        
        plotter.plot(optimizer.boundary, halls, year, hall_years, optimizer.radius_in_degrees)
        
        existing_halls = halls

if __name__ == '__main__':
    main()
