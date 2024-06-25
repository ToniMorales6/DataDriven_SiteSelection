import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

puntos = gpd.read_file('hundredpoints.geojson')

parques = pd.read_csv('centroides_zonas_verdes.csv', encoding='utf-8')
parques_gdf = gpd.GeoDataFrame(parques, 
                               geometry=gpd.points_from_xy(parques['longitud'], parques['latitud']),
                               crs="EPSG:4326")

mapa = folium.Map(location=[puntos.geometry.y.mean(), puntos.geometry.x.mean()], zoom_start=13)

# Función para contar las zonas verdes en un radio de 750 m
def contar_zonas_verdes(punto, parques, radio=750):
    buffer = punto.buffer(radio / 111320)  # 1 grado ~ 111.32 km en el ecuador
    zonas_verdes = parques[parques.intersects(buffer)]
    return len(zonas_verdes)

# Número máximo de zonas verdes alrededor de los puntos
max_zonas_verdes = puntos.geometry.apply(lambda geom: contar_zonas_verdes(geom, parques_gdf)).max()

colormap = folium.LinearColormap(colors=['red', 'yellow', 'green'], vmin=0, vmax=max_zonas_verdes)

# Añadir una columna para la puntuación al GeoDataFrame de puntos
puntos['num_zonas_verdes'] = puntos.geometry.apply(lambda geom: contar_zonas_verdes(geom, parques_gdf))
puntos['puntuacion'] = (puntos['num_zonas_verdes'] / max_zonas_verdes) * 10

# Añadir los puntos georreferenciados
for idx, row in puntos.iterrows():
    num_zonas_verdes = row['num_zonas_verdes']
    color = colormap(num_zonas_verdes)
    puntuacion = row['puntuacion']
    
    # Añadir un círculo alrededor del punto
    folium.Circle(
        location=[row.geometry.y, row.geometry.x],
        radius=750, 
        color=None,
        fill=True,
        fill_color=color,
        fill_opacity=0.2,
        popup=f'Zonas Verdes: {num_zonas_verdes}\nPuntuación: {round(puntuacion, 2)}',
        opacity=0
    ).add_to(mapa)
    
    # Añadir el marcador del punto
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=4,
        color='black',
        fill=True,
        fill_color='black',
        fill_opacity=1,
        popup=f'Zonas Verdes: {num_zonas_verdes}\nPuntuación: {round(puntuacion, 2)}'
    ).add_to(mapa)

colormap.add_to(mapa)

mapa.save('mapa_con_ZonasVerdes.html')

puntos.to_csv('Puntuacion_Zonas_Verdes.csv')

print("Mapa guardado en 'mapa_con_ZonasVerdes.html'")
print("GeoDataFrame guardado en 'Puntuacion_Zonas_Verdes.geojson'")