import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt
import re

# Función para extraer longitud y latitud de la columna 'geometry'
def extract_coordinates(geometry):
    match = re.search(r'POINT \(([^ ]+) ([^ ]+)\)', geometry)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

geojson_path = 'BarcelonaCiutat_Districtes.csv'
distritos_df = pd.read_csv(geojson_path)

# Convertir la columna de geometría WGS84 a objetos geométricos
distritos_df['geometry'] = distritos_df['geometria_wgs84'].apply(wkt.loads)
gdf_distritos = gpd.GeoDataFrame(distritos_df, geometry='geometry', crs="EPSG:4326")

file_path = 'Puntuacion_Zonas_Verdes.csv'
data = pd.read_csv(file_path)

# Extraer las coordenadas de la columna 'geometry'
data['longitud'], data['latitud'] = zip(*data['geometry'].apply(extract_coordinates))

# Convertir a GeoDataFrame
data['geometry'] = gpd.points_from_xy(data['longitud'], data['latitud'])
gdf_data = gpd.GeoDataFrame(data, geometry='geometry', crs="EPSG:4326")

# Unión espacial
gdf_joined = gpd.sjoin(gdf_data, gdf_distritos, how='left', predicate='within')

# Agrupar por distrito y contar el número de zonas verdes
zonas_verdes_por_distrito = gdf_joined.groupby('nom_districte')['num_zonas_verdes'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(zonas_verdes_por_distrito['nom_districte'], zonas_verdes_por_distrito['num_zonas_verdes'])
plt.xlabel('Distrito')
plt.ylabel('Número de Zonas Verdes')
plt.title('Número de Zonas Verdes por Distrito en Barcelona')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('zonas_verdes_por_distrito.png')

plt.show()
