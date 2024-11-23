# Extract the set of administrative unit names from the GeoJSON
geojson_names = {feature["properties"].get("name:en", "") for feature in geojson_data["features"]}

# Extract the set of administrative unit names from the CSV
csv_names = set(df["Administrative Unit"])

# Find unmatched units
unmatched_in_csv = csv_names - geojson_names  # Units in CSV but not in GeoJSON
unmatched_in_geojson = geojson_names - csv_names  # Units in GeoJSON but not in CSV

# Print mismatches for debugging
print("Units in CSV but not in GeoJSON:", unmatched_in_csv)
print("Units in GeoJSON but not in CSV:", unmatched_in_geojson)
