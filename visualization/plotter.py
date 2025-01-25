import os
import matplotlib.pyplot as plt

class FireHallPlotter:
    """
    A class to plot fire hall placements on a map.

    Attributes:
        year_colors : dict; A dictionary mapping years to their respective colors for plotting.
        markers : list; A list of marker styles for plotting different years.
    """
    def __init__(self):
        """
        Initializes the FireHallPlotter with predefined year colors and markers.
        Also ensures the 'maps' directory exists.
        """
        self.year_colors = {
            1963: '#1f77b4',  # blue
            2005: '#2ca02c',  # green
            2011: '#ff7f0e'   # orange
        }
        self.markers = ['o', 's', '^']
        
        # Create maps directory if it doesn't exist
        os.makedirs('maps', exist_ok=True)

    def plot(self, boundary, halls, year, hall_years, radius_in_degrees):
        """
        Plots the fire hall placements on a map.

        Parameters:
        ----------
        boundary : object
            The boundary object with exterior coordinates for plotting.
        halls : list
            A list of tuples representing the coordinates of fire halls.
        year : int
            The year for which the plot is being generated.
        hall_years : list
            A list of years corresponding to each fire hall.
        radius_in_degrees : float
            The radius of the circle around each hall in degrees.
        """
        
        plt.figure(figsize=(15, 12), dpi=300)
        x, y = boundary.exterior.xy
        plt.plot(x, y, 'k-', linewidth=2)
        plt.fill(x, y, alpha=0.1, color='lightgray')
        
        for hall, hall_year in zip(halls, hall_years):
            color = self.year_colors[hall_year]
            marker = self.markers[list(self.year_colors.keys()).index(hall_year)]
            
            plt.scatter(hall[0], hall[1], 
                       color=color, 
                       marker=marker,
                       s=200, 
                       edgecolor='black')
            
            circle = plt.Circle(
                hall,
                radius_in_degrees,
                color=color,
                alpha=0.2
            )
            plt.gca().add_artist(circle)
        
        plt.title(f'maps/Fire Hall Placement ({year})')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.axis('equal')
        plt.tight_layout()
        
        plt.savefig(f'maps/fire_hall_optimization_{year}.png')
        plt.close()
