import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

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

# Create a marker cluster for the flood incidences
marker_cluster = MarkerCluster().add_to(m)

# Add flood points and 500m radius circles
for i, row in flood_df.iterrows():
    # Set marker color
    if row["Year"] == 2020:
        color = "blue"
    else:
        color = "pink"

    # Add flood point marker
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"Location: {row['Location']}, Flood Year: {row['Year']}",
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(marker_cluster)

    # Add 500m radius circle around the flood point
    folium.Circle(
        location=[row["Latitude"], row["Longitude"]],
        radius=200,  # 500 meters
        color=color,
        fill=True,
        fill_opacity=0.2,
    ).add_to(m)


# Function to check if a client falls within 500 meters of a flood point
def is_within_radius(flood_point, client_point, radius=200):
    distance = geodesic(flood_point, client_point).meters
    return distance <= radius


# Add client locations and highlight those within 500m of a flood point
for i, client_row in client_df.iterrows():
    client_location = (client_row["Latitude"], client_row["Longitude"])
    client_within_flood_radius = False

    for j, flood_row in flood_df.iterrows():
        flood_location = (flood_row["Latitude"], flood_row["Longitude"])
        if is_within_radius(flood_location, client_location):
            client_within_flood_radius = True
            break

    # Use yellow for clients within flood radius, otherwise orange
    marker_color = "purple" if client_within_flood_radius else "orange"

    folium.Marker(
        location=[client_row["Latitude"], client_row["Longitude"]],
        popup=f"Client Location: {client_row['Branch Name']}",
        icon=folium.Icon(
            color=marker_color, icon="info-sign"
        ),  # Highlight clients in yellow
    ).add_to(m)

# Adding the Gombak River GeoJSON file to the map
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

# Save the map as an HTML file
m.save("kuala_lumpur_flood_and_clients_map_with_river.html")
