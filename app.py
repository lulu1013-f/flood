import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from folium.plugins import Fullscreen

# Initialize session state to store pinned locations
if 'locations' not in st.session_state:
    st.session_state['locations'] = []

# Title and Instructions
st.title("Pin Locations on Map and Extract Latitude & Longitude")
st.write("Manually pin locations on the map. Click on the map to add a marker.")

# Create a Folium map centered on Ulaanbaatar, Mongolia
m = folium.Map(location=[47.92123, 106.918556], zoom_start=12)

# Add Fullscreen button to the map
Fullscreen().add_to(m)

# Add existing pinned locations to the map
for loc in st.session_state['locations']:
    folium.Marker([loc['Latitude'], loc['Longitude']], tooltip=loc['Address']).add_to(m)

# Display the map and capture the click event
output = st_folium(m, width=900, height=600)  # Maximize width and height

# If a location is clicked, add it to the list
if output.get('last_clicked'):
    lat, lon = output['last_clicked']['lat'], output['last_clicked']['lng']
    st.session_state['locations'].append({'Address': f'Pinned at {lat:.5f}, {lon:.5f}', 'Latitude': lat, 'Longitude': lon})
    st.experimental_rerun()  # Rerun the app to display the updated markers

# Display the location data as a table
if st.session_state['locations']:
    df = pd.DataFrame(st.session_state['locations'])
    st.write("Pinned Locations:")
    st.dataframe(df)

    # Provide an option to download the data as CSV
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='pinned_locations.csv',
        mime='text/csv'
    )
