import pandas as pd
import folium

# Load the CSV file into a DataFrame
file_path = 'output_visualize/Combined_Output.csv'  # Replace with the actual path to your CSV file
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to check the structure and verify the content
print(data.head())

# Group by the x and y coordinates to combine rows that share the same coordinates
grouped_data = data.groupby(['x coordinate', 'y coordinate'])

# Initialize a map centered at a general location (e.g., Ho Chi Minh City)
m = folium.Map(location=[10.8231, 106.6297], zoom_start=13)

# Iterate through the grouped DataFrame and add markers for each unique coordinate pair
for (x_coordinate, y_coordinate), group in grouped_data:
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
    
    # Add a marker to the map
    folium.Marker(
        location=[x_coordinate, y_coordinate],
        popup=popup,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Save the map to an HTML file
output_map = 'output_map_new.html'
m.save(output_map)

print(f"Map has been saved to {output_map}")
