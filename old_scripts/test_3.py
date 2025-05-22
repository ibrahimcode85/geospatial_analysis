import pandas as pd
import plotly.express as px

# Load the flood incidence data from the Excel file
flood_data_path = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\flood_incidence_kuala_lumpur_expanded.xlsx"
flood_df = pd.read_excel(flood_data_path)

# Coordinates for Menara Takaful Malaysia (Office)
office_longitude = 101.69612
office_latitude = 3.13935

# Add a row for the office to the dataframe
office_df = pd.DataFrame(
    {
        "Location": ["Menara Takaful Malaysia"],
        "Latitude": [office_latitude],
        "Longitude": [office_longitude],
        "Flood Depth (m)": ["N/A"],  # No flood depth for the office
    }
)

# Combine the flood data and the office location
combined_df = pd.concat([flood_df, office_df], ignore_index=True)

# Plotly Express for interactive map
fig = px.scatter_mapbox(
    combined_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Location",
    hover_data=["Flood Depth (m)"],
    color_discrete_sequence=["blue"],  # Marker color
    zoom=12,  # Initial zoom level
    height=600,
)

# Customize the mapbox appearance
fig.update_layout(
    mapbox_style="open-street-map",  # Default map style
    mapbox_zoom=12,  # Zoom level to start
    mapbox_center={
        "lat": office_latitude,
        "lon": office_longitude,
    },  # Center around the office
    margin={"r": 0, "t": 0, "l": 0, "b": 0},  # No margin around the map
)

# Add a red marker for the office location
fig.add_scattermapbox(
    lat=[office_latitude],
    lon=[office_longitude],
    mode="markers",
    marker=dict(size=12, color="red"),
    name="Office Location",
)

# Show the map
fig.show()
