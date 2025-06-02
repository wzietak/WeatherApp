import pycountry
import requests
from requests import JSONDecodeError
import streamlit as st

class GeocodingAPI:
    """
    Klasa do obsługi zapytań geokodowania do API OpenWeatherMap oraz konwersji nazw krajów na kody ISO.
    """
    def __init__(self):
        """
        Inicjalizuje instancję GeocodingAPI z kluczem API i adresem endpointu OpenWeatherMap.
        """
        self.API_KEY = st.secrets["api"]["key"]
        self.url = "http://api.openweathermap.org/geo/1.0/direct?q="

    def convertCountryToISOCode(self, country_name):
        """
        Konwertuje nazwę kraju na dwuliterowy kod ISO 3166.

        Args:
            country_name (str): nazwa kraju wprowadzona przez użytkownika

        Returns:
            str or None: dwuliterowy kod ISO, jeśli znaleziony, w przeciwnym razie None
        """
        try:
            results = pycountry.countries.search_fuzzy(country_name)
            return results[0].alpha_2
        except LookupError:
            return

    def getLocation(self, city_name, country_code):
        """
        Wysyła zapytanie do OpenWeatherMap API w celu uzyskania współrzędnych geograficznych na podstawie nazwy miasta i kodu kraju.

        Args:
            city_name (str): nazwa miasta
            country_code (str): kod ISO 3166 kraju

        Returns:
            list or None: lista lokalizacji w formacie JSON, jeśli zapytanie się powiedzie, w przeciwnym razie None
        """
        request = f"{self.url}{city_name},{country_code}&limit=5&appid={self.API_KEY}"
        try:
            response = requests.get(request)
            data = response.json()
        except JSONDecodeError:
            return None

        return data



