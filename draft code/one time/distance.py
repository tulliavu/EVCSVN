import pandas as pd
import numpy as np
import math

# Haversine formula to calculate distance between two lat/lon points
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth
    using the Haversine formula.
    
    Parameters:
    lat1, lon1: Latitude and longitude of the first point.
    lat2, lon2: Latitude and longitude of the second point.
    
    Returns:
    Distance between the two points in kilometers.
    """
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    # Distance in kilometers
    return R * c

# Load the people and POI data from CSV files
people_df = pd.read_csv('PEOPLE_OLD.csv')
poi_df = pd.read_csv('output_visualize/Combined_Output.csv')

# Merge people and POI dataframes on the 'Unit' column
merged_df = pd.merge(people_df, poi_df, on='Unit', suffixes=('_people', '_poi'))

# Calculate the distance for each pair of people and POI using Haversine formula
# We apply the haversine function row-wise for each pair of lat/lon
merged_df['distance_km'] = merged_df.apply(lambda row: haversine(row['Lat2'], row['Lon2'], row['x coordinate'], row['y coordinate']), axis=1)

# Group by 'Unit' and calculate the average distance
average_distance_per_unit = merged_df.groupby('Unit')['distance_km'].mean().reset_index()

# Output the result
print(average_distance_per_unit)
# Save the result to a CSV file
average_distance_per_unit.to_csv('distance.csv', index=False)
