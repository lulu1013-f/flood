import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from folium.plugins import Fullscreen

# Set Streamlit page layout to wide mode
st.set_page_config(layout="wide")

# Initialize session state to store pinned locations
if 'locations' not in st.session_state:
    st.session_state['locations'] = []

# Title and Instructions
st.title("Pin Locations on Map and Extract Latitude & Longitude")
st.write("Manually pin locations on the map. Click on the map to add a marker and provide a description for each location.")

# Create a Folium map centered on Ulaanbaatar, Mongolia
m = folium.Map(location=[47.92123, 106.918556], zoom_start=12)

# Add Fullscreen button to the map
Fullscreen().add_to(m)

# Add existing pinned locations to the map
for loc in st.session_state['locations']:
    folium.Marker([loc['Latitude'], loc['Longitude']],
                  tooltip=loc['Description']).add_to(m)

# Display the map and capture the click event
output = st_folium(m, width=1100, height=700)  # Increase width and height

# If a location is clicked, allow user to add a description
if output.get('last_clicked'):
    lat = output['last_clicked']['lat']
    lon = output['last_clicked']['lng']
    
    # Create input fields for description
    with st.form(key='location_form'):
        description = st.text_input('Enter a description for the pinned location:')
        submit_button = st.form_submit_button(label='Add Pin')

        if submit_button:
            # Add the new pin to the session state
            st.session_state['locations'].append({
                'Description': description,
                'Latitude': lat,
                'Longitude': lon
            })
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

# Add custom CSS to make the map full height
st.markdown(
    """
    <style>
    .st-folium {
        height: 85vh !important; /* Make map height 85% of the viewport height */
    }
    </style>
    """,
    unsafe_allow_html=True
)
