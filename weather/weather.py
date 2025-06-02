from datetime import datetime as dt

class Weather:
    """
    Klasa reprezentująca bieżące dane pogodowe dla danej lokalizacji.
    """
    def __init__(self, weather_name, description, icon, temp, temp_feels_like, pressure, humidity, cloudiness, wind_speed, time, rain=None, snow=None):
        """
        Inicjalizuje obiekt klasy Weather z danymi pogodowymi

        Args:
            weather_name (str): główne określenie pogody (np. "Rain", "Clear")
            description (str): krótki opis pogody (np. "light rain")
            icon (str): kod ikony pogody z API
            temp (float): temperatura w stopniach Celsjusza
            temp_feels_like (float): odczuwalna temperatura w stopniach Celsjusza
            pressure (int): ciśnienie atmosferyczne w hPa
            humidity (int): wilgotność powietrza w procentach
            cloudiness (int): zachmurzenie w procentach
            wind_speed (float): prędkość wiatru w m/s
            rain (float or None): opady deszczu (mm/h) - jeśli dostępne
            snow (float or None): Opady śniegu (mm/h) - jeśli dostępne
            time (str): czas pomiaru w formacie "DD/MM/YYYY HH:MM:SS"
        """
        self.weather_name = weather_name
        self.description = description
        self.icon = icon
        self.temp = temp
        self.temp_feels_like = temp_feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.cloudiness = cloudiness
        self.wind_speed = wind_speed
        self.rain = rain #if available
        self.snow = snow #if available
        self.time = time
        self.icon_url = "https://openweathermap.org/img/wn/" #ogólny link do ikon z API

    @classmethod
    def parseTheWeather(cls, json_data):
        """
        Tworzy instancję klasy Weather na podstawie danych JSON z API.

        Args:
            json_data (dict): dane pogodowe w formacie JSON z API OpenWeatherMap

        Returns:
            Weather: obiekt klasy Weather z wypełnionymi atrybutami
        """
        weather_name = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        icon = json_data["weather"][0]["icon"]
        temp = json_data["main"]["temp"] #Celsius
        temp_feels_like = json_data["main"]["feels_like"] #Celsius
        pressure = json_data["main"]["pressure"] #hPa
        humidity = json_data["main"]["humidity"] #%
        wind_speed = json_data["wind"]["speed"] #meter/sec
        cloudiness = json_data["clouds"]["all"] #%
        rain = json_data.get("rain", {}).get("1h") #mm/h
        snow = json_data.get("snow", {}).get("1h")  #mm/h
        time = cls.convertUnixTimestamp(json_data["dt"])

        return cls(weather_name, description, icon, temp, temp_feels_like, pressure, humidity, cloudiness, wind_speed, time, rain, snow)

    @staticmethod
    def convertUnixTimestamp(timestamp):
        """
        Konwertuje znacznik czasu Unix na czytelny format daty i godziny

        Args:
            timestamp (int): znacznik czasu Unix

        Returns:
            str: sformatowany czas w postaci "DD/MM/YYYY HH:MM:SS"
        """
        converted = dt.fromtimestamp(int(timestamp))
        return converted.strftime("%d/%m/%Y %H:%M:%S")



