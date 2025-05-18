import streamlit as st

from api.geocoding_api import GeocodingAPI
from api.weather_api import WeatherAPI

st.set_page_config(
   page_title="Weather App",
   page_icon="./img/cloudy.png"
)
st.title("Weather App")

with st.form('location_form'):
    st.write("Search location by city and country:")
    city_input = st.text_input("City")
    country_input = st.text_input("Country")
    search_button = st.form_submit_button("Search", type="primary")

coding = GeocodingAPI()
weather = WeatherAPI()

if search_button:
    if city_input and country_input:
        country_coded = coding.convertCountryToISOCode(city_input)
        location = coding.getLocation(city_input, country_coded)
        st.write(location)
    else:
        st.error("Please enter both city and country")

