import pandas as pd
import json
import folium
from shapely.geometry import shape

# Load the population data from the CSV
csv_file = "population.csv"  # Replace with your CSV file name
df = pd.read_csv(csv_file, header=None)
df.columns = ["Administrative Unit", "Population"]

# Ensure Population column is numeric
df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
df = df.dropna(subset=["Population"])

# Load the GeoJSON boundary data
geojson_file = "hcm.geojson"  # Replace with your GeoJSON file name
with open(geojson_file, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Remove Point features from GeoJSON
geojson_data["features"] = [
    feature for feature in geojson_data["features"] if feature["geometry"]["type"] != "Point"
]

# Debug: Ensure 'name:en' exists or fallback
for feature in geojson_data["features"]:
    if "name:en" not in feature["properties"]:
        feature["properties"]["name:en"] = feature["properties"].get("name", "Unknown")

# Match population data with the boundaries using 'name:en'
population_map = {row["Administrative Unit"]: row["Population"] for _, row in df.iterrows()}
for feature in geojson_data["features"]:
    unit_name = feature["properties"].get("name:en")  # Extract 'name:en'
    feature["properties"]["population"] = population_map.get(unit_name, 0)

# Debug: Check for unmatched units
geojson_names = {feature["properties"].get("name:en", "") for feature in geojson_data["features"]}
csv_names = set(df["Administrative Unit"])
unmatched_in_csv = csv_names - geojson_names
unmatched_in_geojson = geojson_names - csv_names
print("Units in CSV but not in GeoJSON:", unmatched_in_csv)
print("Units in GeoJSON but not in CSV:", unmatched_in_geojson)

# Calculate bounds from GeoJSON data
all_shapes = [shape(feature["geometry"]) for feature in geojson_data["features"]]
full_bounds = [s.bounds for s in all_shapes]
minx, miny = min(b[0] for b in full_bounds), min(b[1] for b in full_bounds)
maxx, maxy = max(b[2] for b in full_bounds), max(b[3] for b in full_bounds)

# Create a folium map dynamically centered to fit bounds
hcm_map = folium.Map()
hcm_map.fit_bounds([[miny, minx], [maxy, maxx]])

# Add a choropleth layer for the population heatmap
choropleth = folium.Choropleth(
    geo_data=geojson_data,
    name="Population Heatmap",
    data=df,
    columns=["Administrative Unit", "Population"],
    key_on="feature.properties.name:en",  # Ensure correct key is used
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Population by Administrative Unit"
).add_to(hcm_map)

# Add tooltips for each administrative unit
folium.GeoJsonTooltip(
    fields=["name:en", "population"],
    aliases=["Administrative Unit (EN)", "Population"],
    localize=True
).add_to(choropleth.geojson)

# Save to HTML
output_file = "hcm_population_heatmap.html"
hcm_map.save(output_file)
print(f"Heatmap saved to {output_file}")
