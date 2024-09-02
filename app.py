import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import folium
import pandas as pd

# Initialize the session state to store the locations
if 'locations' not in st.session_state:
    st.session_state['locations'] = []

# Function to get latitude and longitude from an address
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Streamlit web app
st.title("Location Pinning Web App")
st.write("Enter an address to pin the location and get latitude and longitude.")

# User input for address
address = st.text_input("Enter the address:")

if address:
    lat, lon = get_coordinates(address)
    if lat and lon:
        # Store the location
        st.session_state['locations'].append({'Address': address, 'Latitude': lat, 'Longitude': lon})
        st.write(f"Location pinned: {address} (Latitude: {lat}, Longitude: {lon})")
    else:
        st.write("Address not found. Please try a different one.")

# If there are pinned locations, create a map
if st.session_state['locations']:
    # Initialize a folium map centered at the first location
    m = folium.Map(location=[st.session_state['locations'][0]['Latitude'], st.session_state['locations'][0]['Longitude']], zoom_start=5)

    # Add all locations to the map
    for loc in st.session_state['locations']:
        folium.Marker([loc['Latitude'], loc['Longitude']], tooltip=loc['Address']).add_to(m)

    # Display the map in Streamlit
    st_data = st_folium(m, width=700, height=500)

    # Display the location data as a table
    df = pd.DataFrame(st.session_state['locations'])
    st.write("Pinned Locations:")
    st.dataframe(df)

    # Provide an option to download the data as CSV or Excel
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(index=False),
        file_name='locations.csv',
        mime='text/csv'
    )

    # Download as Excel
    @st.cache_data
    def convert_df_to_excel(df):
        return df.to_excel(index=False, engine='xlsxwriter')

    excel_data = convert_df_to_excel(df)

    st.download_button(
        label="Download data as Excel",
        data=excel_data,
        file_name='locations.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
