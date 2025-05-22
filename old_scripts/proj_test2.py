import rasterio
from rasterio.windows import from_bounds
import matplotlib.pyplot as plt
import numpy as np
from folium.raster_layers import ImageOverlay
import folium
import pandas as pd

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

    # Mask out no-data areas or irrelevant data (e.g., ocean, null values)
    masked_data = np.ma.masked_where(
        window_data <= 0, window_data
    )  # Adjust threshold as needed

    # Choose a better color map (e.g., 'RdYlBu', 'coolwarm', etc.)
    plt.imshow(masked_data, cmap="RdYlBu", vmin=min_value, vmax=max_value)
    plt.title("Flood Data for Malaysia (Masked)")
    plt.colorbar()  # Add colorbar for reference
    plt.show()

    # Save the image using matplotlib (saved as 'malaysia_windowed.png')
    plt.imsave("malaysia_windowed.png", masked_data, cmap="RdYlBu")


# Convert the windowed data (NumPy array) into a DataFrame
window_data_df = pd.DataFrame(window_data)

# Save the DataFrame to an Excel file
output_excel_path = "windowed_data_inspection.xlsx"
window_data_df.to_excel(output_excel_path, index=False)


# Now overlay the saved PNG on the Folium map

# Initialize the Folium map centered on Malaysia
m = folium.Map(location=[4.2105, 101.9758], zoom_start=6, tiles="OpenStreetMap")

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

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save the map with the overlay as an HTML file
m.save("malaysia_map_with_geotiff_overlay_improved.html")
