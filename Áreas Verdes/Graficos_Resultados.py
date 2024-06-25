import pandas as pd
import matplotlib.pyplot as plt
import re

resultados_df = pd.read_csv('Puntuacion_Zonas_Verdes.csv')

# Función para extraer longitud y latitud de la columna 'geometry'
def extract_coordinates(geometry):
    match = re.search(r'POINT \(([^ ]+) ([^ ]+)\)', geometry)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

# Aplicar la función para crear nuevas columnas de longitud y latitud
resultados_df['longitud'], resultados_df['latitud'] = zip(*resultados_df['geometry'].apply(extract_coordinates))

# Histograma de las puntuaciones
plt.figure(figsize=(10, 6))
plt.hist(resultados_df['puntuacion'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribución de las Puntuaciones de Zonas Verdes')
plt.xlabel('Puntuación')
plt.ylabel('Frecuencia')
plt.savefig('histograma_puntuaciones.png')
plt.show()

# Gráfico con los 104 puntos con colores basados en la puntuación
plt.figure(figsize=(10, 6))
sc = plt.scatter(resultados_df['longitud'], resultados_df['latitud'], c=resultados_df['puntuacion'], cmap='viridis', edgecolor='black')
plt.colorbar(sc, label='Puntuación')
plt.title('Puntos Georreferenciados y sus Puntuaciones')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.savefig('distribucion_puntuaciones.png')
plt.show()

print("Gráficas guardadas como 'histograma_puntuaciones.png' y 'distribucion_puntuaciones.png'")

