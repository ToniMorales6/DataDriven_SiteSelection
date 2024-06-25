import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from pyproj import Proj, transform
from geopy.distance import distance


# Load the geographical boundaries of Barcelona from the provided GeoJSON file
barcelona_boundary = gpd.read_file('limitesbarcelona.geojson')

# Find the largest polygon
largest_polygon = max(barcelona_boundary['geometry'], key=lambda polygon: polygon.area)

# Get the bounds of the largest polygon
minx, miny, maxx, maxy = largest_polygon.bounds

# Define the number of points
num_points = 290

# Generate a grid of points within the bounds of the largest polygon
x_points = np.linspace(minx, maxx, int(np.sqrt(num_points)))
y_points = np.linspace(miny, maxy, int(np.sqrt(num_points)))
grid_points = [Point(x, y) for x in x_points for y in y_points]

# Filter out points that are outside the largest polygon
uniform_points = [point for point in grid_points if largest_polygon.contains(point)]

# If there are more points than required, randomly select num_points
if len(uniform_points) > num_points:
    uniform_points = np.random.choice(uniform_points, num_points, replace=False)

# Create a GeoDataFrame for the uniform points
uniform_points_gdf = gpd.GeoDataFrame(geometry=uniform_points)

# Save the uniform points to a GeoJSON file
output_path = 'uniform_points_within_largest_polygon.geojson'
uniform_points_gdf.to_file(output_path, driver='GeoJSON')

# Plot the uniform points
base = barcelona_boundary.plot(color='white', edgecolor='black')
uniform_points_gdf.plot(ax=base, marker='o', color='red', markersize=5)
plt.show()

# Print the total number of points within the polygon
print("Total number of points within the polygon:", len(uniform_points))



# Function to calculate the distance between two points given their latitude and longitude
def calculate_distance(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    # Calculate the change in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Calculate the distance using the Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    return distance

# Calculate the closest distance for each point
closest_distances = []
for point1 in uniform_points:
    min_distance = float('inf')
    for point2 in uniform_points:
        if point1 != point2:
            lat1, lon1 = point1.y, point1.x
            lat2, lon2 = point2.y, point2.x
            dist = calculate_distance(lat1, lon1, lat2, lon2)
            min_distance = min(min_distance, dist)
    closest_distances.append(min_distance)

# Calculate the average closest distance
average_closest_distance = sum(closest_distances) / len(closest_distances)

print("Average distance to the closest points in kilometers:", average_closest_distance)



