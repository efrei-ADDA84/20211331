import os
import requests
from dotenv import load_dotenv

load_dotenv()
def get_weather(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        return None

if __name__ == "__main__":
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    lat = os.environ.get("LATITUDE")
    lon = os.environ.get("LONGITUDE")
    if api_key and lat and lon:
        weather_data = get_weather(api_key, lat, lon)
        if weather_data:
            print(f"Temperature: {weather_data['temperature']}°C")
            print(f"Humidity: {weather_data['humidity']}%")
            print(f"Wind Speed: {weather_data['wind_speed']} m/s")
        else:
            print("Error: Unable to retrieve weather data.")
    else:
        print("Error: Please provide your OpenWeather API key, latitude and longitude.")
