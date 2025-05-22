import rasterio
from rasterio.windows import from_bounds
import matplotlib.pyplot as plt
import numpy as np
from folium.raster_layers import ImageOverlay
import folium

# Define the bounding box for all of Malaysia
malaysia_bbox = {
    "left": 99.60,  # Longitude of the left (west) boundary
    "bottom": 0.85,  # Latitude of the bottom (south) boundary
    "right": 119.30,  # Longitude of the right (east) boundary
    "top": 7.50,  # Latitude of the top (north) boundary
}

# Open the GeoTIFF file
tiff_file = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\projection\inunriver_rcp4p5_00000NorESM1-M_2030_rp00002.tif"

with rasterio.open(tiff_file) as dataset:
    # Convert the bounding box to pixel coordinates (window)
    window = from_bounds(
        malaysia_bbox["left"],
        malaysia_bbox["bottom"],
        malaysia_bbox["right"],
        malaysia_bbox["top"],
        transform=dataset.transform,
    )

    # Read the windowed data (subset)
    window_data = dataset.read(1, window=window)

    # Check the range of values to better understand the data
    min_value = np.min(window_data)
    max_value = np.max(window_data)
    print(f"Data range: Min = {min_value}, Max = {max_value}")

    # Adjust the range for visualization (e.g., focus on depths between 0-10 meters)
    vmin, vmax = (
        0,
        0.2,
    )  # Adjust this based on the typical range of flood depths in your data

    # Mask out no-data areas or irrelevant data (e.g., ocean, null values)
    masked_data = np.ma.masked_where(
        window_data <= 0, window_data
    )  # Adjust threshold as needed

    # Use the PuBu color map (goes from dark blue to light blue) with improved contrast
    plt.imshow(masked_data, cmap="Blues", vmin=vmin, vmax=vmax)
    plt.title("Flood Inundation Depth (Meters) for Malaysia (Improved Contrast)")
    plt.colorbar(label="Flood Depth (m)")  # Add colorbar with label for flood depth
    plt.show()

    # Save the image using matplotlib with improved transparency
    plt.imsave("malaysia_windowed_improved.png", masked_data, cmap="Blues")
    plt.close()  # Close the figure to release memory

# Now overlay the saved PNG on the Folium map

# Initialize the Folium map centered on Malaysia
m = folium.Map(location=[4.2105, 101.9758], zoom_start=6, tiles="OpenStreetMap")

# Add the overlay (ImageOverlay) to the map using the geographic bounds
bounds = [
    [malaysia_bbox["bottom"], malaysia_bbox["left"]],
    [malaysia_bbox["top"], malaysia_bbox["right"]],
]

ImageOverlay(
    image="malaysia_windowed_improved.png",  # Path to the saved image
    bounds=bounds,  # [[south, west], [north, east]] of the image
    opacity=0.7,  # Lower opacity for better map visibility
).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save the map with the overlay as an HTML file
m.save("malaysia_map_with_geotiff_overlay_improved2.html")
