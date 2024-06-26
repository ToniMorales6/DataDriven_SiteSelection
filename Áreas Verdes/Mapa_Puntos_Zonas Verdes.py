import pandas as pd
import folium

file_path = 'Áreas Verdes/centroides_zonas_verdes.csv'
df = pd.read_csv(file_path)

# Crear un mapa centrado en la primera coordenada del dataset
map_center = [df['latitud'].mean(), df['longitud'].mean()]
mapa = folium.Map(location=map_center, zoom_start=12)

for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitud'], row['longitud']],
        popup=row['addresses_road_name'],
        icon=folium.Icon(color='green')
    ).add_to(mapa)

mapa.save('Áreas Verdes/Mapas/mapa_solo_zonas_verdes.html')
