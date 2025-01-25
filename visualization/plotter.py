import matplotlib.pyplot as plt

class FireHallPlotter:
    def __init__(self):
        self.year_colors = {
            1963: '#1f77b4',  # blue
            2005: '#2ca02c',  # green
            2011: '#ff7f0e'   # orange
        }
        self.markers = ['o', 's', '^']

    def plot(self, boundary, halls, year, hall_years, radius_in_degrees):
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
        
        plt.title(f'Fire Hall Placement ({year})')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.axis('equal')
        plt.tight_layout()
        
        plt.savefig(f'fire_hall_optimization_{year}.png')
        plt.close()
