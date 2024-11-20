import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Initialize a map centered at Ho Chi Minh City
m = folium.Map(location=[10.8231, 106.6297], zoom_start=13)

# Load GeoJSON file containing Ho Chi Minh City boundary (replace with the actual file path you downloaded)
boundary_file = '79.json'  # Replace this with the actual path to your GeoJSON file
#Reference: https://github.com/daohoangson/dvhcvn/blob/master/data/gis/79.json
folium.GeoJson(
    boundary_file,
    name="Ho Chi Minh City District Boundary",
    style_function=lambda feature: {
        'color': 'black',       # Dark line color
        'weight': 4,            # Bold line (thicker)
        'fillOpacity': 0,       # No fill, only boundary
    }
).add_to(m)

# First Dataset: 'Combined_Output.csv'
file_path_1 = 'output_visualize/Combined_Output.csv'  # Replace with the actual path to your first CSV file
data_1 = pd.read_csv(file_path_1)

# Group by the x and y coordinates to combine rows that share the same coordinates
grouped_data_1 = data_1.groupby(['x coordinate', 'y coordinate'])

# Iterate through the first dataset and add markers for each unique coordinate pair
for (x_coordinate, y_coordinate), group in grouped_data_1:
    # Display the unit once (assume all rows for the same coordinate share the same Unit)
    unit = group['Unit'].iloc[0]
    popup_content = f"Unit: {unit}<br><br>"

    # Add each Type and Value from the grouped rows
    for idx, row in group.iterrows():
        value_type = row['Type']
        value = row['Value']
        popup_content += f"Type: {value_type}<br>Value: {value}<br>"

    # Add coordinates to the popup content
    popup_content += f"<br>X Coordinate: {x_coordinate}<br>Y Coordinate: {y_coordinate}"
    
    # Create a folium popup with the combined information
    popup = folium.Popup(popup_content, max_width=300)
    
    # Add a custom yellow marker to the map for the first dataset, with a smaller size (1/10th of the original size)
    marker = folium.Marker(
        location=[x_coordinate, y_coordinate],
        popup=popup,
        icon=folium.Icon(color="yellow", icon="bolt", prefix="fa")
    ).add_to(m)

    # Apply a JavaScript bounce effect with a smaller marker size
    marker_id = f"marker_{x_coordinate}_{y_coordinate}"
    marker.get_root().html.add_child(folium.Element(f'''
        <script>
            var {marker_id} = L.marker([{x_coordinate}, {y_coordinate}], {{
                icon: L.AwesomeMarkers.icon({{
                    icon: 'bolt', markerColor: 'yellow', prefix: 'fa', iconSize: [3.6, 3.6],  // 1/10th of the original size
                }}),
                bounceOnAdd: true,
                bounceOnAddOptions: {{duration: 500, height: 100}},
                bounceOnAddCallback: function() {{console.log("done");}}
            }}).addTo({m.get_name()});
        </script>
    '''))

# Second Dataset: 'EXISTING.csv'
file_path_2 = 'EXISTING.csv'  # Replace with the actual path to your second CSV file
data_2 = pd.read_csv(file_path_2)

# Group by the x and y coordinates to combine rows that share the same coordinates
grouped_data_2 = data_2.groupby(['x coordinate', 'y coordinate'])

# Initialize a MarkerCluster for the second dataset
marker_cluster = MarkerCluster().add_to(m)

# Iterate through the second dataset and add markers for each unique coordinate pair
for (x_coordinate, y_coordinate), group in grouped_data_2:
    # Display the unit and name once (assume all rows for the same coordinate share the same Unit and Name)
    unit = group['Unit'].iloc[0]
    name = group['Name'].iloc[0]
    popup_content = f"Name: {name}<br>Unit: {unit}<br><br>"

    # Add each Type and Value from the grouped rows
    for idx, row in group.iterrows():
        value_type = row['Type']
        value = row['Value']
        popup_content += f"Type: {value_type}<br>Value: {value}<br>"

    # Add coordinates to the popup content
    popup_content += f"<br>X Coordinate: {x_coordinate}<br>Y Coordinate: {y_coordinate}"
    
    # Create a folium popup with the combined information
    popup = folium.Popup(popup_content, max_width=300)
    
    # Add a marker with a custom charging station icon and add the marker to the cluster, with a smaller size (1/10th of the original size)
    marker = folium.Marker(
        location=[x_coordinate, y_coordinate],
        popup=popup,
        icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
    ).add_to(marker_cluster)

    # Use a JavaScript function to make the marker bounce up and down (second dataset)
    marker_id = f"marker_{x_coordinate}_{y_coordinate}"
    marker.get_root().html.add_child(folium.Element(f'''
        <script>
            var {marker_id} = L.marker([{x_coordinate}, {y_coordinate}], {{
                icon: L.AwesomeMarkers.icon({{
                    icon: 'bolt', markerColor: 'blue', prefix: 'fa', iconSize: [3.6, 3.6],  // 1/10th of the original size
                }}),
                bounceOnAdd: true,
                bounceOnAddOptions: {{duration: 500, height: 100}},
                bounceOnAddCallback: function() {{console.log("done");}}
            }}).addTo({m.get_name()});
        </script>
    '''))

# Add a legend to the map
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; padding: 10px; text-align: left; display: flex; flex-direction: column; justify-content: center; width: auto; height: auto;">
    <b style="text-align: center; margin-bottom: 5px;">Note</b>
    <div style="text-align: center;">
        <i class="fa fa-bolt" style="color:red"></i> New charging station <br>
        <i class="fa fa-bolt" style="color:blue"></i> Existing charging station <br>
    </div>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save the combined map to an HTML file
output_map = 'output_map_combined_with_boundary.html'
m.save(output_map)

print(f"Map has been saved to {output_map}")
