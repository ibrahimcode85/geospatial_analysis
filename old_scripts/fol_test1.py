import pandas as pd
import folium
from folium.plugins import MarkerCluster

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

# Add flood points to the marker cluster
for i, row in flood_df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"Location: {row['Location']}, Flood Depth: {row['Flood Depth (m)']}",
        icon=folium.Icon(color="blue", icon="cloud"),
    ).add_to(marker_cluster)

# Save the map as an HTML file or display it in a Jupyter Notebook
m.save("kuala_lumpur_flood_map.html")
