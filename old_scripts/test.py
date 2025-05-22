import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

# Load the flood incidence data from the Excel file
flood_data_path = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\flood_incidence_kuala_lumpur_expanded.xlsx"
flood_df = pd.read_excel(flood_data_path)

# Convert flood data into a GeoDataFrame
flood_geometry = [Point(xy) for xy in zip(flood_df["Longitude"], flood_df["Latitude"])]
flood_gdf = gpd.GeoDataFrame(flood_df, geometry=flood_geometry, crs="EPSG:4326")

# Coordinates for Menara Takaful Malaysia (Office)
office_longitude = 101.69612
office_latitude = 3.13935

# Create a GeoDataFrame for the office location
office_location = gpd.GeoDataFrame(
    [{"geometry": Point(office_longitude, office_latitude)}], crs="EPSG:4326"
)

# Convert both the flood points and office location to web mercator (EPSG:3857) for plotting
flood_gdf = flood_gdf.to_crs(epsg=3857)
office_location = office_location.to_crs(epsg=3857)

# Plot the map
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the flood incidences
flood_gdf.plot(ax=ax, markersize=50, color="blue", marker="o", label="Flood Incidences")

# Plot the office location
office_location.plot(
    ax=ax, markersize=100, color="red", marker="o", label="Office Location"
)

# Annotate flood locations
for x, y, label in zip(
    flood_gdf.geometry.x, flood_gdf.geometry.y, flood_gdf["Location"]
):
    ax.text(x, y, label, fontsize=8, color="green")

# Annotate the office location
office_x, office_y = office_location.geometry.x[0], office_location.geometry.y[0]
ax.text(
    office_x, office_y, "Menara Takaful Malaysia", fontsize=10, color="red", ha="right"
)

# Set axis limits to zoom into Kuala Lumpur area
zoom_buffer = 100
ax.set_xlim(
    flood_gdf.geometry.x.min() - zoom_buffer, flood_gdf.geometry.x.max() + zoom_buffer
)
ax.set_ylim(
    flood_gdf.geometry.y.min() - zoom_buffer, flood_gdf.geometry.y.max() + zoom_buffer
)

# Add the basemap using contextily
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Set the plot title and show the legend
plt.title("Flood Incidences and Office Location in Kuala Lumpur")
plt.legend()
plt.show()
