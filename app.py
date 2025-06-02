from datetime import date
import streamlit as st
from dateutil.relativedelta import relativedelta
import altair as alt

from api.geocoding_api import GeocodingAPI
from api.historical_weather_api import HistoricalWeatherAPI
from api.weather_api import WeatherAPI
from weather.weather import Weather

def show_the_weather(weather, city_name, country_name):
    """
    Wyświetla aktualną pogodę dla podanej lokalizacji w zakładce 'Current weather'.

    Args:
        weather (Weather): obiekt zawierający dane pogodowe
        city_name (str): nazwa miasta
        country_name (str): nazwa kraju
    """
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

def show_hist_weather(hist_weather,city_name,country_name,start_date,end_date):
    """
     Wyświetla wykresy z historycznymi danymi pogodowymi dla podanej lokalizacji w zakładce 'Historical weather'.

    Args:
        hist_weather (pd.DataFrame): ramka danych zawierająca historyczne dane pogodowe
        city_name (str): nazwa miasta
        country_name (str): nazwa kraju
        start_date (datetime.date): data początkowa dla danych historycznych
        end_date (datetime.date): data końcowa dla danych historycznych
    """
    st.header(f"Historical weather in {city_name}, {country_name}")
    st.caption(f"From {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")

    options = ["🌡️ Temperature","📈 Pressure","💧 Humidity","💨 Wind speed","☁️ Cloudiness","🌧️ Precipitation"]
    selection = st.pills("Choose a data type to visualize",options,selection_mode="single")

    if st.session_state.get("hist_weather") is None:
        return

    if selection:
        y_min = hist_weather[selection].min()
        y_max = hist_weather[selection].max()
        if selection == "🌡️ Temperature":
            st.line_chart(data=hist_weather.set_index("date")[selection],use_container_width=True,x_label="Date",y_label="Temperature (°C)")
        elif selection == "📈 Pressure":
            chart = alt.Chart(hist_weather).mark_line().encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("📈 Pressure:Q", title="Pressure (hPa)", scale=alt.Scale(domain=[y_min-5,y_max+5]),axis=alt.Axis(format='.2f'))
            )
            st.altair_chart(chart, use_container_width=True)
        elif selection == "💧 Humidity":
            st.line_chart(data=hist_weather.set_index("date")[selection],use_container_width=True,x_label="Date",y_label="Humidity (%)")
        elif selection == "💨 Wind speed":
            st.line_chart(data=hist_weather.set_index("date")[selection],use_container_width=True,x_label="Date",y_label="Wind speed (km/h)")
        elif selection == "☁️ Cloudiness":
            st.line_chart(data=hist_weather.set_index("date")[selection],use_container_width=True,x_label="Date",y_label="Cloudiness (%)")
        elif selection == "🌧️ Precipitation":
            st.bar_chart(data=hist_weather.set_index("date")[selection],
            use_container_width=True,x_label="Date",y_label="Precipitation (mm)")

def location_form(form_key="location_form",historical=False):
    """
    Wyświetla formularz przyjmujący nazwę miasta i kraju oraz zakres dat (dla danych historycznych).

    Args:
        form_key (str): unikalny identyfikator dla formularza st.form
        historical (bool): czy formularz ma zawierać pola do wyboru zakresu dat

    Returns:
        Jeśli `historical` jest True:
            city_input (str): nazwa miasta wprowadzona przez użytkownika
            country_input (str): nazwa kraju wprowadzona przez użytkownika
            search_button (bool): status kliknięcia przycisku 'Search'
            start_date_input (datetime.date): data początkowa zakresu
            end_date_input (datetime.date): data końcowa zakresu
        Jeśli `historical` jest False:
            city_input (str): nazwa miasta wprowadzona przez użytkownika
            country_input (str): nazwa kraju wprowadzona przez użytkownika
            search_button (bool): status kliknięcia przycisku 'Search'
    """
    with st.form(form_key):
        if historical:
            st.write("Enter city and country:")
        else:
            st.write("Search location by city and country:")
        city_input = st.text_input("City")
        country_input = st.text_input("Country")
        if historical:
            st.write("Choose date range:")
            start_date_input = st.date_input("Start date", value=date.today()-relativedelta(years=1),min_value=date.today()-relativedelta(years=20,days=1), max_value=date.today()-relativedelta(days=3), format="DD/MM/YYYY")
            end_date_input = st.date_input("End date", min_value=date.today()-relativedelta(years=20),max_value=date.today()-relativedelta(days=2), format="DD/MM/YYYY")
        search_button = st.form_submit_button("Search", type="primary")

    if historical:
        return city_input,country_input,start_date_input,end_date_input,search_button
    else:
        return city_input, country_input, search_button

def handle_weather(city_input,country_input,search_button,start_date=None,end_date=None,historical=False):
    """
    Obsługuje pobieranie i wyświetlanie danych pogodowych na podstawie wejścia użytkownika oraz zapewnia kontrolę błędów dla formularza i API.

    Args:
        city_input (str): nazwa miasta podana przez użytkownika
        country_input (str): nazwa kraju podana przez użytkownika
        search_button (bool): status kliknięcia przycisku 'Search'
        start_date (datetime.date, opcjonalny): początek zakresu dat (dla danych historycznych)
        end_date (datetime.date, opcjonalny): koniec zakresu dat (dla danych historycznych)
        historical (bool, opcjonalny): określa, czy pobierane są dane historyczne czy aktualne
    """

    geocoding = GeocodingAPI()
    weather_data = WeatherAPI()
    hist_weather_data = HistoricalWeatherAPI()

    if search_button:
        if "hist_weather" in st.session_state:
            st.session_state.pop("hist_weather", None)

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
                if not historical:
                    curr_weather_data = weather_data.getWeatherForLocation(chosen_location["lat"], chosen_location["lon"])
                    curr_weather = Weather.parseTheWeather(curr_weather_data)
                    show_the_weather(curr_weather, chosen_location["name"], chosen_location["country"])
                else:
                    hist_weather,error = hist_weather_data.getHistoricalWeatherData(chosen_location["lat"], chosen_location["lon"],start_date, end_date)
                    if hist_weather is not None:
                        st.session_state["hist_weather"] = hist_weather
                        st.session_state["city_name"] = chosen_location["name"]
                        st.session_state["country_name"] = chosen_location["country"]
                        st.session_state["start_date"] = start_date
                        st.session_state["end_date"] = end_date
                    else:
                        st.error(error)
        else:
            st.error("Please enter both city and country.")

# Podstawowa konfiguracja aplikacji
st.set_page_config(
   page_title="Weather App",
   page_icon="./img/cloudy.png"
)

# Tytuł aplikacji
st.title("Weather App")

# Zakładki: aktualna i historyczna pogoda
tab1, tab2 = st.tabs(["☀️ Current weather", "📈 Historical weather"])

with tab1:
    # Formularz do wyszukiwania aktualnej pogody
    city_input,country_input,search_button = location_form(form_key="current_form")
    handle_weather(city_input,country_input, search_button)

with tab2:
    # Formularz do wyszukiwania historycznych danych pogodowych
    city_input, country_input, start_date_input,end_date_input, search_button = location_form(form_key="historical_form",historical=True)

    # Walidacja zakresu dat
    if start_date_input == end_date_input:
        st.session_state.pop("hist_weather", None)
        st.error("Invalid date range: End date must come after start date.")
    else:
        # Obsługa zapytania o dane historyczne
        handle_weather(city_input, country_input,search_button,start_date_input,end_date_input,historical=True)

    if "hist_weather" in st.session_state:
        # Wyświetlanie wykresów historycznych, jeśli dane są dostępne
        show_hist_weather(
            st.session_state["hist_weather"],
            st.session_state["city_name"],
            st.session_state["country_name"],
            st.session_state["start_date"],
            st.session_state["end_date"]
        )





