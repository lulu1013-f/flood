import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd

# Initialize session state to store pinned locations
if 'locations' not in st.session_state:
    st.session_state['locations'] = []

# Title and Instructions
st.title("Pin Locations on Map and Extract Latitude & Longitude")
st.write("Manually pin locations on the map. Click on the map to add a marker.")

# Create a Folium map centered on Ulaanbaatar, Mongolia
m = folium.Map(location=[47.92123, 106.918556], zoom_start=12)

# Add existing pinned locations to the map
for loc in st.session_state['locations']:
    folium.Marker([loc['Latitude'], loc['Longitude']], tooltip=loc['Address']).add_to(m)

# Function to handle map click event
def handle_click(event):
    lat, lon = event['latlng']
    st.session_state['locations'].append({'Address': f'Pinned at {lat:.5f}, {lon:.5f}', 'Latitude': lat, 'Longitude': lon})

# Add the map click handler
st_folium(m, width=700, height=500, callback=handle_click)

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

# Create a map object using streamlit-folium to capture events
m = folium.Map(location=[47.92123, 106.918556], zoom_start=12)

# Add a Folium map display in Streamlit
output = st_folium(m, width=700, height=500)
if output['last_clicked']:
    # Get the clicked location details
    lat, lon = output['last_clicked']['lat'], output['last_clicked']['lng']
    st.session_state['locations'].append({'Address': f'Pinned at {lat:.5f}, {lon:.5f}', 'Latitude': lat, 'Longitude': lon})
    st.experimental_rerun() # Rerun the app to display updated markers
