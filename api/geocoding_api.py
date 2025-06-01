import pycountry
import requests
from requests import JSONDecodeError
import streamlit as st

class GeocodingAPI:
    def __init__(self):
        self.API_KEY = st.secrets["api"]["key"]
        self.url = "http://api.openweathermap.org/geo/1.0/direct?q="

    def convertCountryToISOCode(self, country_name):
        try:
            results = pycountry.countries.search_fuzzy(country_name)
            return results[0].alpha_2
        except LookupError:
            return

    def getLocation(self, city_name, country_code):
        request = f"{self.url}{city_name},{country_code}&limit=5&appid={self.API_KEY}"
        try:
            response = requests.get(request)
            data = response.json()
        except JSONDecodeError:
            return None

        return data



