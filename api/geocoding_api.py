import pycountry
import requests

class GeocodingAPI:
    def __init__(self):
        self.api_key = "***REMOVED***"
        self.url = "http://api.openweathermap.org/geo/1.0/direct?q="

    def convertCountryToISOCode(self, country_name):
        try:
            return pycountry.countries.search_fuzzy(country_name)
        except LookupError:
            return

    def getLocation(self, city_name, country_code):
        request = f"{self.url}{city_name},{country_code}&limit=5&appid={self.api_key}"

        response = requests.get(request)
        data = response.json()
        # print(data)
        return data
      # tu wyświetlać użytkownikowi listę znalezionych lokalizacji do wyboru czy coś





