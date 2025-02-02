# Data Driven Site Selection

Este proyecto se centra en la selección de ubicaciones basada en datos para una guardería en la ciudad de Barcelona. El objetivo principal es utilizar datos demográficos y espaciales para identificar las mejores ubicaciones posibles. Se analizan varios factores clave como la densidad de niños, la competencia de guarderías existentes, las áreas verdes, el transporte público y la capacidad económica de las familias. Se han evaluado 104 puntos de referencia en la ciudad, aplicando un radio de 750 metros para cada uno. El modelo desarrollado no solo es aplicable a guarderías, sino que también puede extenderse a otros servicios y equipamientos urbanos. Este repositorio proporciona todo el código y las bases de datos necesarias, permitiendo a otros adaptar el análisis a diferentes ubicaciones y contextos.

## Diagrama Indicador Final

![Diagrama](https://github.com/ToniMorales6/DataDriven_SiteSelection/blob/main/Indicador%20Final/Diagrama/Diagrama.PNG)

## Librerias requeridas

Para instalar las librerias necesarias, ejecutar los siguientes comandos en tu consola con Python instalado:

```bash
pip3 install geopandas
pip3 install shapely
pip3 install numpy
pip3 install matplotlib
pip3 install pyproj
pip3 install geopy
pip3 install pandas
pip3 install folium
pip3 install plotly
pip3 install scikit-learn
pip3 install seaborn
pip3 install nbformat --upgrade #necesario para visualizar algun grafico
```
## Enlaces a los Mapas

### Indicador Global
- [heat_map_total_score.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Indicador%20Final/Mapas/heat_map_total_score.html)

- [map_with_total_score.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Indicador%20Final/Mapas/map_with_total_score.html)

- [puntoconrentamasalta.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Indicador%20Final/Mapas/puntoconrentamasalta.html)

### Transporte público
- [0_mapa_transporte_publico_bcn_except_bus.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Transporte%20Publico/Mapas/0_mapa_transporte_publico_bcn_except_bus.html)

- [1_mapa_bus_bcn.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Transporte%20Publico/Mapas/1_mapa_bus_bcn.html)

- [2_mapa_puntuación_análisis_final.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Transporte%20Publico/Mapas/2_mapa_puntuación_análisis_final.html)

### Capacidad Económica
- [heat_map.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Capacidad%20Econ%C3%B3mica/Mapas/heat_map.html)

- [average_rent.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Capacidad%20Econ%C3%B3mica/Mapas/average_rent.html)

- [mapa_secciones_censales.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Capacidad%20Econ%C3%B3mica/Mapas/mapa_secciones_censales.html)

### Número de Guarderías
- [map_with_competencia_score.html](https://tonimorales6.github.io/DataDriven_SiteSelection/N%C3%BAmero%20de%20Guarderias/Mapas/map_with_competencia_score.html)

- [map_with_counts.html](https://tonimorales6.github.io/DataDriven_SiteSelection/N%C3%BAmero%20de%20Guarderias/Mapas/map_with_counts.html)

- [mapanumerodepuntos.html](https://tonimorales6.github.io/DataDriven_SiteSelection/N%C3%BAmero%20de%20Guarderias/Mapas/mapanumerodepuntos.html)

### Áreas Verdes
- [mapa_solo_zonas_verdes.html](https://tonimorales6.github.io/DataDriven_SiteSelection/%C3%81reas%20Verdes/Mapas/mapa_solo_zonas_verdes.html)

- [mapa_con_ZonasVerdes.html](https://tonimorales6.github.io/DataDriven_SiteSelection/%C3%81reas%20Verdes/Mapas/mapa_con_ZonasVerdes.html)

### Menores de 3 Años
- [heat_map_score_menores3.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Menores%20de%203%20a%C3%B1os/Mapas/heat_map_score_menores3.html)

- [heat_map2_score_menores3.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Menores%20de%203%20a%C3%B1os/Mapas/heat_map2_score_menores3.html)

- [marker_map_with_numbers_white.html](https://tonimorales6.github.io/DataDriven_SiteSelection/Menores%20de%203%20a%C3%B1os/Mapas/marker_map_with_numbers_white.html)