import pandas as pd
import folium
from folium.plugins import HeatMap

# Example dataset
data = {
    'latitude': [37.7749, 34.0522, 40.7128],
    'longitude': [-122.4194, -118.2437, -74.0060],
    'population': [1000000, 4000000, 8000000]
}
df = pd.DataFrame(data)

# Create a base map
base_map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)

# Create a heatmap layer
heat_data = [[row['latitude'], row['longitude'], row['population']] for index, row in df.iterrows()]
HeatMap(heat_data, radius=15).add_to(base_map)

# Save or display the map
base_map.save("population_heatmap.html")
base_map
