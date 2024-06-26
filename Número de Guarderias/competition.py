#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:46:42 2024

@author: nelson
"""


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

import folium
from folium.plugins import HeatMap

censo = pd.read_csv('Número de Guarderias\censolocales.csv')

nulos = censo.isnull().sum()


censofilt = censo[censo['Nom_Local'].str.contains('guarderia|llar d\'infants|guardería|bressol|infancia|guardería|infància|infancia|infantil|parvulario', case=False, na=False)]

censofilt = censofilt[censofilt['Nom_Activitat'] == 'Ensenyament' ]


censofilt[['Nom_Barri','Nom_Districte','Latitud', 'Longitud', 'Nom_Local']].to_csv('Número de Guarderias\guarderiasfinal.csv')

# Agrupar por 'Nom_Districte' y contar las ocurrencias
districte_counts = censofilt['Nom_Districte'].value_counts().sort_index()

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
districte_counts.plot(kind='bar', color='skyblue')
plt.title('Número de guarderías por distrito')
plt.xlabel('Nombre del distrito')
plt.ylabel('total')
plt.xticks(rotation=45)
plt.show()

refpoints = gpd.read_file('Número de Guarderias\hundredpoints.geojson')

geometry = [Point(xy) for xy in zip(censofilt['Longitud'], censofilt['Latitud'])]
gdf_censofilt = gpd.GeoDataFrame(censofilt, geometry=geometry)

refpoints.set_crs(epsg=4326, inplace=True)
gdf_censofilt.set_crs(epsg=4326, inplace=True)

buffered_refpoints = refpoints.copy()
buffered_refpoints['geometry'] = buffered_refpoints.geometry.buffer(750 / 111000)  # Approximation for degrees

join_gdf = gpd.sjoin(gdf_censofilt, buffered_refpoints, op='within')

counts = join_gdf.groupby('index_right').size()

refpoints['count_within_2km'] = counts

refpoints['count_within_2km'] = refpoints['count_within_2km'].fillna(0).astype(int)

nulos = refpoints.isnull().sum()



max_score = refpoints['count_within_2km'].max()
min_score = refpoints['count_within_2km'].min()

refpoints['competencia_score'] = refpoints['count_within_2km'].apply(lambda x: 20 - ((x - min_score) * (20 / (max_score - min_score))))

puntaje = refpoints[['geometry', 'competencia_score']]

puntaje.to_csv('Número de Guarderias\Mapas\competitionpoints.csv')


# Plot de resultados
plt.figure(figsize=(8, 6))
plt.boxplot(refpoints['competencia_score'])
plt.title('Boxplot de Competencia Score')
plt.ylabel('Competencia Score')
plt.grid(True)
plt.show()



# MAPA!

map_center = [refpoints.geometry.y.mean(), refpoints.geometry.x.mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Add markers to the map
for idx, row in refpoints.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f'Count within 750m: {row["count_within_2km"]}',
        tooltip=row["count_within_2km"]
    ).add_to(m)

m.save('Número de Guarderias\Mapas\map_with_counts.html')

m

heat_data = [[row.geometry.y, row.geometry.x, row['count_within_2km']] for idx, row in refpoints.iterrows()]
m_heat = folium.Map(location=map_center, zoom_start=12)
HeatMap(heat_data).add_to(m_heat)

m_heat.save('Número de Guarderias\Mapas\heat_map.html')

# Display the heat map
m_heat






max_count = refpoints['count_within_2km'].max()
colormap = folium.LinearColormap(colors=['red', 'yellow', 'green'], vmin=0, vmax=max_count)

map_center = [refpoints.geometry.y.mean(), refpoints.geometry.x.mean()]
m = folium.Map(location=map_center, zoom_start=12)

for idx, row in refpoints.iterrows():
    num_count = row['count_within_2km']
    color = colormap(num_count)
    
    # Añadir un círculo alrededor del punto
    folium.Circle(
        location=[row.geometry.y, row.geometry.x],
        radius=750,  # Radio de 750 m
        color=None,
        fill=True,
        fill_color=color,
        fill_opacity=0.2,
        popup=f'Count within 750m: {num_count}',
        opacity=0
    ).add_to(m)
    
    # Añadir el marcador del punto
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=4,
        color='black',
        fill=True,
        fill_color='black',
        fill_opacity=1,
        popup=f'Count within 750m: {num_count}'
    ).add_to(m)

colormap.add_to(m)

m.save('map_with_counts.html')

m

heat_data = [[row.geometry.y, row.geometry.x, row['count_within_2km']] for idx, row in refpoints.iterrows()]
m_heat = folium.Map(location=map_center, zoom_start=12)
HeatMap(heat_data).add_to(m_heat)

m_heat.save('Número de Guarderias\Mapas\heat_map2.html')

m_heat




max_score = puntaje['competencia_score'].max()
min_score = puntaje['competencia_score'].min()
colormap = folium.LinearColormap(colors=['red', 'yellow', 'green'], vmin=min_score, vmax=max_score)

map_center = [puntaje.geometry.y.mean(), puntaje.geometry.x.mean()]
m = folium.Map(location=map_center, zoom_start=12)

for idx, row in puntaje.iterrows():
    competencia_score = row['competencia_score']
    color = colormap(competencia_score)
    
    # Añadir un círculo alrededor del punto
    folium.Circle(
        location=[row.geometry.y, row.geometry.x],
        radius=750,  # Radio de 750 m
        color=None,
        fill=True,
        fill_color=color,
        fill_opacity=0.2,
        popup=f'Competencia Score: {competencia_score}',
        opacity=0
    ).add_to(m)
    
    # Añadir el marcador del punto
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=4,
        color='black',
        fill=True,
        fill_color='black',
        fill_opacity=1,
        popup=f'Competencia Score: {competencia_score}'
    ).add_to(m)

colormap.add_to(m)

m.save('Número de Guarderias\Mapas\map_with_competencia_score.html')

m

heat_data = [[row.geometry.y, row.geometry.x, row['competencia_score']] for idx, row in puntaje.iterrows()]
m_heat = folium.Map(location=map_center, zoom_start=12)
HeatMap(heat_data).add_to(m_heat)

m_heat.save('Número de Guarderias\Mapas\heat_mappuntaje.html')

m_heat
