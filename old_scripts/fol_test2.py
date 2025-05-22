import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

# Load the flood incidence data from the Excel file
flood_data_path = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\flood_incidence_kuala_lumpur_expanded.xlsx"
flood_df = pd.read_excel(flood_data_path)

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
    # Add flood point marker
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"Location: {row['Location']}, Flood Depth: {row['Flood Depth (m)']}",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(marker_cluster)

    # Add 500m radius circle around the flood point
    folium.Circle(
        location=[row["Latitude"], row["Longitude"]],
        radius=1500,  # 500 meters
        color="blue",
        fill=True,
        fill_opacity=0.2,
    ).add_to(m)


# Function to check if a point (e.g., office) falls within 500 meters of a flood point
def is_within_radius(flood_point, other_point, radius=1500):
    # Calculate the distance between the flood point and the other point (e.g., office)
    distance = geodesic(flood_point, other_point).meters
    return distance <= radius


# Example: Check if the office falls within 500m of any flood points
for i, row in flood_df.iterrows():
    flood_point = (row["Latitude"], row["Longitude"])
    office_point = (office_latitude, office_longitude)
    if is_within_radius(flood_point, office_point):
        print(
            f"The office is within 1500 meters of the flood point at {row['Location']}"
        )

# Save the map as an HTML file
m.save("kuala_lumpur_flood_map_with_radius.html")
