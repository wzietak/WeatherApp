from datetime import datetime as dt

class Weather:
    def __init__(self, weather_name, description, icon, temp, temp_feels_like, pressure, humidity, cloudiness, wind_speed, time, rain=None, snow=None):
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
        self.icon_url = "https://openweathermap.org/img/wn/"

    @classmethod
    def parseTheWeather(cls, json_data):
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
        converted = dt.fromtimestamp(int(timestamp))
        return converted.strftime("%d/%m/%Y %H:%M:%S")



