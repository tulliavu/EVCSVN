import geopandas as gpd
import matplotlib.pyplot as plt

# Path to the GeoJSON file
geojson_file = 'Ho Chi Minh.geojson'

# Read the GeoJSON file using GeoPandas
gdf = gpd.read_file(geojson_file)

# Plot the GeoDataFrame
gdf.plot(figsize=(10, 10), edgecolor='black')

# Set plot title and display the map
plt.title("Ho Chi Minh - GeoJSON Map")
plt.show()
