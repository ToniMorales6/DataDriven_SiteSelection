import pandas as pd
import geopandas as gpd

# Ruta al archivo CSV cargado
ruta_csv = 'Áreas Verdes/opendatabcn_cultura_parcs-i-jardins.csv'

# Leer el archivo CSV con la codificación detectada
parques = pd.read_csv(ruta_csv, encoding= 'utf-16')

# Crear un GeoDataFrame a partir de los datos de los árboles
gdf_parques = gpd.GeoDataFrame(
    parques, geometry=gpd.points_from_xy(parques['geo_epgs_4326_lon'], parques['geo_epgs_4326_lat']), crs="EPSG:4326"
)

# Agrupar los datos por las coordenadas (latitud y longitud)
gdf_grouped = gdf_parques.groupby(['geo_epgs_4326_lon', 'geo_epgs_4326_lat'])

# Calcular el centroide para cada grupo (en este caso, será el propio punto ya que estamos agrupando por coordenadas exactas)
centroides = gdf_grouped.geometry.apply(lambda x: x.unary_union.centroid)

# Crear un nuevo DataFrame con los centroides
df_centroides = pd.DataFrame({
    'latitud': centroides.y,
    'longitud': centroides.x
})

# Agregar información adicional si es necesario
extra_columns = ['addresses_roadtype_id', 'addresses_roadtype_name', 'addresses_road_name', 'addresses_road_id']
for col in extra_columns:
    df_centroides[col] = gdf_grouped[col].first().values

# Guardar el resultado en un nuevo archivo CSV
output_csv = 'Áreas Verdes/centroides_zonas_verdes.csv'
df_centroides.to_csv(output_csv, index=False, encoding='utf-8')

print(f"Archivo guardado en '{output_csv}'")
