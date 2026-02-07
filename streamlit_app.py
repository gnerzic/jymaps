import streamlit as st
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Historian Map Generator", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Map Configuration")
map_name = st.sidebar.text_input("Output Filename", "OutputMap")

st.sidebar.subheader("Coordinates (PlateCarree)")
lon_min = st.sidebar.number_input("Min Longitude", value=-77.0)
lon_max = st.sidebar.number_input("Max Longitude", value=-75.0)
lat_min = st.sidebar.number_input("Min Latitude", value=36.0)
lat_max = st.sidebar.number_input("Max Latitude", value=38.0)


# --- Map Logic ---
def generate_map(extent, filename):
    fig = plt.figure(figsize=(10, 8))
    # We use Mercator for the display projection
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())

    # Features
    ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='lightblue')
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.5, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    # Gridlines
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,
                      linestyle='--', color='gray')
    gl.top_labels = gl.right_labels = False

    # Set the area
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    return fig


# --- Main App Interface ---
st.title("🗺️ Custom Map Generator")
st.write(f"Adjust coordinates in the sidebar to generate the **{map_name}** map.")

map_extent = [lon_min, lon_max, lat_min, lat_max]

if st.button("Generate Map"):
    with st.spinner("Drawing map..."):
        fig = generate_map(map_extent, map_name)
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