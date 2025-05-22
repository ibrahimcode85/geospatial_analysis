import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
from folium.plugins import TimestampedGeoJson
import json

# Load the flood incidence data from the Excel file
flood_data_path = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\flood_incidence_kuala_lumpur_expanded.xlsx"
flood_df = pd.read_excel(flood_data_path, sheet_name="Sheet1")

# Load the client address data (assuming it's in another sheet)
client_data_path = (
    r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\data.xlsx"
)
client_df = pd.read_excel(client_data_path, sheet_name="Sheet1")

# Extract latitude and longitude from the 'coordinate' column
client_df[["Latitude", "Longitude"]] = (
    client_df["Coordinate"].str.split(", ", expand=True).astype(float)
)

# Coordinates for Menara Takaful Malaysia (Office)
office_longitude = 101.69612
office_latitude = 3.13935

# Initialize the map centered around Kuala Lumpur with a starting zoom level
m = folium.Map(
    location=[office_latitude, office_longitude], zoom_start=14, tiles="OpenStreetMap"
)

# Add the office location marker
folium.Marker(
    [office_latitude, office_longitude],
    popup="Menara Takaful Malaysia",
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(m)

# Add client locations and highlight those within 500m of a flood point
for i, client_row in client_df.iterrows():
    client_location = (client_row["Latitude"], client_row["Longitude"])
    client_within_flood_radius = False

    folium.Marker(
        location=[client_row["Latitude"], client_row["Longitude"]],
        popup=f"Client Location: {client_row['Branch Name']}",
        icon=folium.Icon(
            color="orange", icon="info-sign"
        ),  # Highlight clients in yellow
    ).add_to(m)


# Adding highlights to main river
gombak_river_geojson = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\river\gombak.geojson"
klang_river_geojson = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\river\klang.geojson"
batu_river_geojson = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\river\batu.geojson"

folium.GeoJson(
    gombak_river_geojson,
    name="Gombak River",
    style_function=lambda x: {
        "color": "purple",
        "weight": 5,
        "fillColor": "cyan",
        "fillOpacity": 0.3,
    },
).add_to(m)

folium.GeoJson(
    klang_river_geojson,
    name="Gombak River",
    style_function=lambda x: {
        "color": "purple",
        "weight": 5,
        "fillColor": "cyan",
        "fillOpacity": 0.3,
    },
).add_to(m)

folium.GeoJson(
    batu_river_geojson,
    name="Gombak River",
    style_function=lambda x: {
        "color": "purple",
        "weight": 5,
        "fillColor": "cyan",
        "fillOpacity": 0.3,
    },
).add_to(m)


# Prepare data for TimestampedGeoJson (Flood incidents from 2020-2024)
flood_features = []
for i, row in flood_df.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["Longitude"], row["Latitude"]],
        },
        "properties": {
            "time": f"{row['Year']}-01-01",  # Set year as the time
            "popup": f"Location: {row['Location']}, Year: {row['Year']}",
        },
    }
    flood_features.append(feature)

flood_geojson = {"type": "FeatureCollection", "features": flood_features}

# Add the TimestampedGeoJson layer to the map for flood incidents
TimestampedGeoJson(
    flood_geojson,
    period="P1Y",  # Yearly period
    add_last_point=True,
    transition_time=500,
    time_slider_drag_update=True,
).add_to(m)

# Save the map with the time slider and markers
m.save("kuala_lumpur_flood_timeline_map_with_clients.html")
