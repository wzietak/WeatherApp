# 🌤️ Weather App

A user-friendly weather application built with **Streamlit**. It allows you to:

- Check **current weather conditions** for any city and country.
- View **historical daily weather data** going back up to 20 years.

---

## ✨ Features

- 🌍 Input by **city** and **country** name.
- ☀️ Real-time weather: temperature, humidity, cloudiness, wind, pressure.
- 📊 Historical weather: daily temperature, humidity, wind speed, cloud cover, precipitation, and pressure.
- 🗓️ Date range selection for historical data.
- 🧭 Built-in country code conversion using `pycountry`.
- 📁 Uses Streamlit session state to manage responses.

---

## 📦 Tech Stack

- **Python**
- **Streamlit**
- `requests`
- `pandas`
- `openmeteo_requests`
- `pycountry`
- **APIs**: [OpenWeatherMap](https://openweathermap.org/api), [Open-Meteo](https://open-meteo.com)

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- An API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys)

### 📥 Installation

Clone the repository:
```
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

Install the required dependencies:
`pip install -r requirements.txt`

Create a .streamlit/secrets.toml file for your API key:
```
[api]
key = "your_openweathermap_api_key"
```

Run the App:
`streamlit run app.py`

> ⚠️ Please note: code comments and documentation strings are written in Polish, as this project was developed as part of a university course at Nicolaus Copernicus University in Toruń, Poland.
