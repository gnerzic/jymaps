import streamlit as st
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Historian Map Generator", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Map Configuration")
map_name = st.sidebar.text_input("Output Filename", "Chesapeake")

# Coordinate Inputs
st.sidebar.subheader("Coordinates")
lon_min = st.sidebar.number_input("Min Longitude", value=-50.0)
lon_max = st.sidebar.number_input("Max Longitude", value=-50.0)
lat_min = st.sidebar.number_input("Min Latitude", value=50.0)
lat_max = st.sidebar.number_input("Max Latitude", value=50.0)

# Gridline Spacing Inputs
st.sidebar.subheader("Gridline Spacing")
options = [20, 10, 5, 1, 0]

lon_spacing = st.sidebar.selectbox("Longitude Line Spacing (degrees)", options, index=3)  # Default to 1
lat_spacing = st.sidebar.selectbox("Latitude Line Spacing (degrees)", options, index=3)  # Default to 1


# --- Map Logic ---
def generate_map(extent, lon_spc, lat_spc):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())

    # Add Features (based on your main.py)
    ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='lightblue')
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.5, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    # Calculate Gridline Locations
    # If spacing is 0, we pass an empty list to show no lines
    x_locs = np.arange(-180, 181, lon_spc) if lon_spc > 0 else []
    y_locs = np.arange(-90, 91, lat_spc) if lat_spc > 0 else []

    # Apply Gridlines
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,
                      linestyle='--', color='gray',
                      xlocs=x_locs, ylocs=y_locs)

    gl.top_labels = gl.right_labels = False
    gl.xlabel_style = {'fontsize': 8}
    gl.ylabel_style = {'fontsize': 8}

    # Set the area
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    return fig


# --- Main App Interface ---
st.title("🗺️ Custom Map Generator")

if st.button("Generate Map"):
    with st.spinner("Drawing map..."):
        map_extent = [lon_min, lon_max, lat_min, lat_max]
        fig = generate_map(map_extent, lon_spacing, lat_spacing)

        # Display in App
        st.pyplot(fig)

        # Save to buffer for download
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        st.download_button(
            label="Download High-Res Map",
            data=buf.getvalue(),
            file_name=f"{map_name}.png",
            mime="image/png"
        )
