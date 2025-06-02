import requests
import streamlit as st

class WeatherAPI:
    """
    Klasa do pobierania aktualnych danych pogodowych z API OpenWeatherMap.
    """
    def __init__(self):
        """
        Inicjalizuje obiekt klasy WeatherAPI. Pobiera klucz API z konfiguracji Streamlit i ustawia podstawowy URL dla zapytań pogodowych.
        """
        self.API_KEY = st.secrets["api"]["key"]
        self.url = "https://api.openweathermap.org/data/2.5/weather?lat="

    def getWeatherForLocation(self, lat, lon):
        """
        Pobiera aktualne dane pogodowe dla podanej lokalizacji.

        Args:
            lat (float): szerokość geograficzna
            lon (float): długość geograficzna

        Returns:
            data (dict): dane pogodowe w formacie JSON z OpenWeatherMap API
        """
        request = f"{self.url}{lat}&lon={lon}&units=metric&appid={self.API_KEY}"
        response = requests.get(request)
        data = response.json()
        return data
