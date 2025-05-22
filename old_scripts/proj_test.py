import rasterio
from rasterio.windows import from_bounds
import matplotlib.pyplot as plt
import numpy as np
from folium.raster_layers import ImageOverlay
import folium

# Define the bounding box for Kuala Lumpur (in latitude/longitude)
kuala_lumpur_bbox = {
    "left": 101.60,  # Longitude of the left (west) boundary
    "bottom": 3.00,  # Latitude of the bottom (south) boundary
    "right": 101.80,  # Longitude of the right (east) boundary
    "top": 3.20,  # Latitude of the top (north) boundary
}

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

    # Replace any NaN or masked values with 0 for visualization (optional)
    window_data = np.nan_to_num(window_data)

    # Save the image using matplotlib (saved as 'kuala_lumpur_windowed.png')
    plt.imshow(window_data, cmap="Blues")
    plt.title("Windowed Data for Kuala Lumpur")
    plt.colorbar()  # Add colorbar for reference
    # plt.show()

    # Save the image using matplotlib (saved as 'malaysia_windowed.png')
    plt.imsave("malaysia_windowed.png", window_data, cmap="Blues")
    plt.close()

# Now overlay the saved PNG on the Folium map

# Initialize the Folium map centered on Kuala Lumpur
m = folium.Map(location=[3.13935, 101.69612], zoom_start=12, tiles="OpenStreetMap")

# Add the overlay (ImageOverlay) to the map using the geographic bounds
bounds = [
    [malaysia_bbox["bottom"], malaysia_bbox["left"]],
    [malaysia_bbox["top"], malaysia_bbox["right"]],
]

ImageOverlay(
    image="malaysia_windowed.png",  # Path to the saved image
    bounds=bounds,  # [[south, west], [north, east]] of the image
    opacity=0.6,  # Adjust the transparency
).add_to(m)

# Save the map with the overlay as an HTML file
m.save("kuala_lumpur_map_with_geotiff_overlay.html")
