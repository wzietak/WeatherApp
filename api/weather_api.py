import requests
import streamlit as st

class WeatherAPI:
    def __init__(self):
        self.API_KEY = st.secrets["api"]["key"]
        self.url = "https://api.openweathermap.org/data/2.5/weather?lat="
        self.url_historic = "https://api.openweathermap.org/data/3.0/onecall/timemachine?lat="

    def getWeatherForLocation(self, lat, lon):
        request = f"{self.url}{lat}&lon={lon}&units=metric&appid={self.API_KEY}"
        response = requests.get(request)
        data = response.json()
        return data

    def getHistoricWeatherForLocation(self, lat, lon, timestamp):
        request = f"{self.url_historic}{lat}&lon={lon}&dt={timestamp}&appid={self.api_key}"
        response = requests.get(request)
        data = response.json()
        return data