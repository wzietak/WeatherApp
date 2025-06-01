from datetime import date

import streamlit as st
from dateutil.relativedelta import relativedelta

from api.geocoding_api import GeocodingAPI
from api.weather_api import WeatherAPI
from weather.weather import Weather

def show_the_weather(weather, city_name, country_name):
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

def location_form(form_key="location_form",historical=False):
    with st.form('location_form'):
        st.write("Search location by city and country:")
        city_input = st.text_input("City")
        country_input = st.text_input("Country")
        if historical:
            start_date_input = st.date_input("Start date", value=date.today() - relativedelta(years=1),
                                             min_value=date.today() - relativedelta(years=100), max_value="today")
            end_date_input = st.date_input("End date", min_value=date.today() - relativedelta(years=100),
                                           max_value="today")
        search_button = st.form_submit_button("Search", type="primary")

    if historical:
        return city_input,country_input,start_date_input,end_date_input,search_button
    else:
        return city_input, country_input, search_button

def handle_the_weather(city_input,country_input,search_button):
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
                show_the_weather(curr_weather, chosen_location["name"], chosen_location["country"])
        else:
            st.error("Please enter both city and country.")

st.set_page_config(
   page_title="Weather App",
   page_icon="./img/cloudy.png"
)
st.title("Weather App")

tab1, tab2 = st.tabs(["☀️ Current weather", "📈 Historical weather"])

with tab1:
    city_input,country_input,search_button = location_form(form_key="current")
    handle_the_weather(city_input,country_input, search_button)



