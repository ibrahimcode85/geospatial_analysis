import geopandas as gpd

# Load the GeoJSON file (replace with your file path)
file_path = r"C:\Users\ibrah\Downloads\Kuala_Lumpur_DM_2015.geojson"
geojson_data = gpd.read_file(file_path)

# Inspect the first few rows
print(geojson_data.head())

# Check the column names
print(geojson_data.columns)

# Filter for any river-related data
river_data = geojson_data[
    geojson_data["Nama"].str.contains("Sungai", na=False, case=False)
]
print(river_data)
