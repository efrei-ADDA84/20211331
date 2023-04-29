import os  # importe le module os pour interagir avec le système d'exploitation
import requests  # importe le module requests pour faire des requêtes HTTP
from dotenv import load_dotenv  # importe la fonction load_dotenv du module dotenv

load_dotenv()  # charge les variables d'environnement à partir du fichier .env

def get_weather(api_key, lat, lon):
    # définit une fonction get_weather avec trois paramètres : api_key, lat, lon
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    # construit l'URL de l'API OpenWeatherMap en utilisant les paramètres api_key, lat, et lon
    response = requests.get(url)  # fait une requête HTTP GET pour récupérer les données météorologiques
    if response.status_code == 200:  # vérifie que la requête a réussi (code de réponse HTTP 200)
        data = response.json()  # récupère les données au format JSON et les stocke dans la variable data
        return {  # retourne un dictionnaire avec les informations de température, d'humidité et de vitesse du vent
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        return None  # retourne None si la requête a échoué

if __name__ == "__main__":
    api_key = os.environ.get("OPENWEATHER_API_KEY")  # récupère la clé API OpenWeatherMap à partir des variables d'environnement
    lat = os.environ.get("LATITUDE")  # récupère la latitude à partir des variables d'environnement
    lon = os.environ.get("LONGITUDE")  # récupère la longitude à partir des variables d'environnement
    if api_key and lat and lon:  # vérifie que toutes les variables sont définies
        weather_data = get_weather(api_key, lat, lon)  # récupère les données météorologiques à partir des coordonnées
        if weather_data:  # vérifie que les données ont été récupérées avec succès
            print(f"Temperature: {weather_data['temperature']}°C")  # affiche la température en Celsius
            print(f"Humidity: {weather_data['humidity']}%")  # affiche l'humidité en pourcentage
            print(f"Wind Speed: {weather_data['wind_speed']} m/s")  # affiche la vitesse du vent en m/s
        else:
            print("Error: Unable to retrieve weather data.")  # affiche un message d'erreur si les données n'ont pas été récupérées
    else:
        print("Error: Please provide your OpenWeather API key, latitude and longitude.")  # affiche un message d'erreur si les variables d'environnement sont manquantes
