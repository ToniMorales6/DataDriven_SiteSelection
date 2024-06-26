import pandas as pd
import geopandas as gpd

# Ruta al archivo CSV cargado
ruta_csv = 'Áreas Verdes/opendatabcn_cultura_parcs-i-jardins.csv'

parques = pd.read_csv(ruta_csv, encoding= 'utf-16')

# Crear un GeoDataFrame
gdf_parques = gpd.GeoDataFrame(
    parques, geometry=gpd.points_from_xy(parques['geo_epgs_4326_lon'], parques['geo_epgs_4326_lat']), crs="EPSG:4326"
)

gdf_grouped = gdf_parques.groupby(['geo_epgs_4326_lon', 'geo_epgs_4326_lat'])

# Calcular el centroide
centroides = gdf_grouped.geometry.apply(lambda x: x.unary_union.centroid)

df_centroides = pd.DataFrame({
    'latitud': centroides.y,
    'longitud': centroides.x
})

extra_columns = ['addresses_roadtype_id', 'addresses_roadtype_name', 'addresses_road_name', 'addresses_road_id']
for col in extra_columns:
    df_centroides[col] = gdf_grouped[col].first().values

output_csv = 'Áreas Verdes/centroides_zonas_verdes.csv'
df_centroides.to_csv(output_csv, index=False, encoding='utf-8')

print(f"Archivo guardado en '{output_csv}'")
