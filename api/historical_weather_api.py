import openmeteo_requests
import pandas as pd

class HistoricalWeatherAPI:
    def __init__(self):
        self.url = "https://archive-api.open-meteo.com/v1/archive"
        self.openmeteo = openmeteo_requests.Client()

    def getHistoricalWeatherData(self, lat, lon, start_date, end_date):
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["pressure_msl_mean","relative_humidity_2m_mean","wind_speed_10m_mean","temperature_2m_mean","cloud_cover_mean","precipitation_sum"]
        }
        try:
            response = self.openmeteo.weather_api(self.url,params=params)
        except Exception as e:
            reason = e.args[0].get("reason", "Unknown error")
            return None, f"Open-Meteo API error: {reason}"

        daily = response[0].Daily()
        daily_pressure = daily.Variables(0).ValuesAsNumpy()
        daily_humidity = daily.Variables(1).ValuesAsNumpy()
        daily_wind_speed = daily.Variables(2).ValuesAsNumpy()
        daily_temperature = daily.Variables(3).ValuesAsNumpy()
        daily_cloudiness = daily.Variables(4).ValuesAsNumpy()
        daily_precipitation = daily.Variables(5).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ), "📈 Pressure": daily_pressure, "💧 Humidity": daily_humidity, "💨 Wind speed": daily_wind_speed,
            "🌡️ Temperature": daily_temperature, "☁️ Cloudiness": daily_cloudiness, "🌧️ Precipitation": daily_precipitation}

        daily_dataframe = pd.DataFrame(data = daily_data)

        return daily_dataframe,None