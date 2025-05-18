import streamlit as st

from api.geocoding_api import GeocodingAPI
from api.weather_api import WeatherAPI
from weather.weather import Weather

def showTheWeather(weather, city_name, country_name):
    st.header(f"Weather in {city_name}, {country_name}")
    st.caption(f"Last update at: {weather.time}")
    col1, col2 = st.columns([1,10], vertical_alignment="center")
    with col1:
        st.image(f"{weather.icon_url}{weather.icon}@2x.png", width=80)
    with col2:
        st.write(f"**{weather.weather_name}** - {weather.description}")

    col3, col4 = st.columns([10,10])
    with col3:
        st.metric("Temperature", f"{round(weather.temp)}°C")
        st.caption(f"Feels like: {round(weather.temp_feels_like)}°C")
    with col4:
        st.write(f"**Pressure:** {weather.pressure} hPa")
        st.write(f"**Humidity:** {weather.humidity}%")
        st.write(f"**Wind speed:** {weather.wind_speed} m/s")
        st.write(f"**Cloudiness:** {weather.cloudiness}%")
        if weather.rain != None:
            st.write(f"**Rain:** {weather.rain} mm/h")
        if weather.snow != None:
            st.write(f"**Snow:** {weather.snow} mm/h")









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

geocoding = GeocodingAPI()
weather_data = WeatherAPI()

if search_button:
    if city_input and country_input:
        country_coded = geocoding.convertCountryToISOCode(country_input)
        location = geocoding.getLocation(city_input, country_coded)
        if location == None or len(location) == 0:
            st.error("Location not found.")
        elif "cod" in location:
            if location["cod"] == "404":
                st.error("Location not found.")
            else:
                st.error(location["message"])
        else:
            chosen_location = location[0]
            curr_weather_data = weather_data.getWeatherForLocation(chosen_location["lat"], chosen_location["lon"])
            curr_weather = Weather.parseTheWeather(curr_weather_data)
            showTheWeather(curr_weather,chosen_location["name"],chosen_location["country"])
    else:
        st.error("Please enter both city and country.")

