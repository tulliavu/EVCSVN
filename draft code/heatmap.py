import pandas as pd
import folium
from folium.plugins import HeatMap

# Initialize the map centered on Ho Chi Minh City
m = folium.Map(location=[10.8231, 106.6297], zoom_start=13)

# First Dataset: 'Combined_Output.csv' (New Charging Stations)
file_path_1 = 'output_visualize/Combined_Output.csv'  # Replace with the actual path to your first CSV file
data_1 = pd.read_csv(file_path_1)

# Second Dataset: 'EXISTING.csv' (Existing Charging Stations)
file_path_2 = 'EXISTING.csv'  # Replace with the actual path to your second CSV file
data_2 = pd.read_csv(file_path_2)

# Function to add a heatmap layer and color scale for a specific dataset
def add_heatmap(dataset, label, color_gradient, map_object):
    # Calculate the number of POIs in each region (density)
    poi_density_per_region = dataset.groupby(['x coordinate', 'y coordinate']).size()

    # Extract heatmap data (with the number of POIs) for the heatmap
    heat_data = [[row['x coordinate'], row['y coordinate'], 1] for _, row in dataset.iterrows()]

    # Add heatmap to the map
    HeatMap(heat_data, name=label, gradient=color_gradient, max_zoom=16, blur=20, radius=15).add_to(map_object)

    # Determine min and max POI density to create dynamic scale
    min_poi_density = round(poi_density_per_region.min(), 3)
    max_poi_density = round(poi_density_per_region.max(), 3)

    # Generate descending intermediate values for the scale based on min and max POI density
    scale_values = [round(min_poi_density + i * (max_poi_density - min_poi_density) / 6, 3) for i in range(6, -1, -1)]

    # Add a color scale (legend) to the map with POI density numbers, styled like the image
    color_scale_html = f'''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 100px; height: 300px; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; padding: 10px; text-align: left;">
        <div style="height: 250px; width: 20px; float: left; margin-right: 5px;
                    background: linear-gradient(to bottom, #000000, #440154, #31688e, #35b779, #fde725);">
        </div>
        <div style="height: 250px; display: flex; flex-direction: column; 
                    justify-content: space-between; float: left; margin-left: 10px; font-size: 12px;">
            {''.join([f'<span>{val}</span>' for val in scale_values])}
        </div>
    </div>
    '''
    map_object.get_root().html.add_child(folium.Element(color_scale_html))

# Define the new color gradient that includes black
color_gradient_with_black = {0.0: '#000000', 0.25: '#440154', 0.5: '#31688e', 0.75: '#35b779', 1: '#fde725'}

# Add heatmap and color scale for the new charging stations (Dataset 1)
add_heatmap(data_1, "New Charging Stations", color_gradient_with_black, m)

# Add heatmap and color scale for the existing charging stations (Dataset 2)
add_heatmap(data_2, "Existing Charging Stations", color_gradient_with_black, m)

# Add layer control to switch between datasets
folium.LayerControl().add_to(m)

# Save the map to an HTML file
output_heat = 'output_heat_map_with_black_color_scale.html'
m.save(output_heat)

print(f"Heatmap has been saved to {output_heat}")
