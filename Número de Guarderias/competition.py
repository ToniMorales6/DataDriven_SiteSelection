#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:46:42 2024

@author: nelson
"""


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

import folium
from folium.plugins import HeatMap

# Load the censofilt DataFrame
censo = pd.read_csv('censolocales.csv')

# Filter for the relevant points
censofilt = censo[censo['Nom_Local'].str.contains('guarderia|llar d\'infants|guardería', case=False, na=False)]

# Load the refpoints GeoJSON file
refpoints = gpd.read_file('hundredpoints.geojson')

# Convert the censofilt DataFrame to a GeoDataFrame
geometry = [Point(xy) for xy in zip(censofilt['Longitud'], censofilt['Latitud'])]
gdf_censofilt = gpd.GeoDataFrame(censofilt, geometry=geometry)

# Set the same coordinate reference system (CRS) for both GeoDataFrames
refpoints.set_crs(epsg=4326, inplace=True)
gdf_censofilt.set_crs(epsg=4326, inplace=True)

# Buffer each point in refpoints by 3 km (3000 meters)
buffered_refpoints = refpoints.copy()
buffered_refpoints['geometry'] = buffered_refpoints.geometry.buffer(2000 / 111000)  # Approximation for degrees

# Perform spatial join to count points within each buffer
join_gdf = gpd.sjoin(gdf_censofilt, buffered_refpoints, op='within')

# Count the number of points within each buffer
counts = join_gdf.groupby('index_right').size()

# Add the counts back to the original refpoints
refpoints['count_within_2km'] = counts

# Fill NaN values with 0 (for points with no nearby points within 3 km)
refpoints['count_within_2km'] = refpoints['count_within_2km'].fillna(0).astype(int)


# Find the maximum and minimum scores
max_score = refpoints['count_within_2km'].max()
min_score = refpoints['count_within_2km'].min()

# Calculate new scores based on the maximum and minimum scores
refpoints['new_score'] = refpoints['count_within_2km'].apply(lambda x: 20 - ((x - min_score) * (20 / (max_score - min_score))))


# MAPA!

# Create a map centered around the average latitude and longitude
map_center = [refpoints.geometry.y.mean(), refpoints.geometry.x.mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Add markers to the map
for idx, row in refpoints.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f'Count within 3 km: {row["count_within_3km"]}',
        tooltip=row["count_within_3km"]
    ).add_to(m)

# Save the map to an HTML file
m.save('map_with_counts.html')

# Display the map
m

# Create a heat map
heat_data = [[row.geometry.y, row.geometry.x, row['count_within_3km']] for idx, row in refpoints.iterrows()]
m_heat = folium.Map(location=map_center, zoom_start=12)
HeatMap(heat_data).add_to(m_heat)

# Save the heat map to an HTML file
m_heat.save('heat_map.html')

# Display the heat map
m_heat



