# Importation des modules Flask, jsonify, request et dotenv
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests
import os

# Charge les variables d'environnement à partir du fichier .env
load_dotenv()

# Initialise l'application Flask
app = Flask(__name__)

# Définit une fonction get_weather pour récupérer les données météorologiques à partir de l'API OpenWeatherMap
def get_weather(api_key, lat, lon):
    # Construit l'URL de l'API OpenWeatherMap en utilisant les paramètres api_key, lat et lon
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    # Effectue une requête HTTP GET pour récupérer les données météorologiques
    response = requests.get(url)
    # Vérifie que la requête a réussi (code de réponse HTTP 200)
    if response.status_code == 200:
        # Récupère les données au format JSON et les stocke dans la variable data
        data = response.json()
        # Retourne un dictionnaire avec les informations de température, d'humidité et de vitesse du vent
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        # Retourne None si la requête a échoué
        return None

# Définit une route pour l'application Flask
@app.route('/')
def weather():
    # Récupère la clé API OpenWeatherMap à partir des variables d'environnement
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    # Récupère les coordonnées géographiques à partir des arguments de la requête
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if api_key and lat and lon:
        # Récupère les données météorologiques à partir de l'API OpenWeatherMap
        weather_data = get_weather(api_key, lat, lon)
        # Vérifie que les données ont été récupérées avec succès
        if weather_data:
            # Construit une chaîne de caractères avec les informations de température, d'humidité et de vitesse du vent
            temperature = f"Temperature: {weather_data['temperature']}°C"
            humidity = f"Humidity: {weather_data['humidity']}%"
            wind_speed = f"Wind Speed: {weather_data['wind_speed']} m/s"
            # Retourne la chaîne de caractères contenant les informations météorologiques
            return f"{temperature}\n{humidity}\n{wind_speed}\n"
        else:
            # Retourne une réponse JSON d'erreur si les données n'ont pas pu être récupérées
            return jsonify({'error': 'Unable to retrieve weather data.'}), 500
    else:
        # Retourne une réponse JSON d'erreur si les arguments de la requête ne sont pas corrects
        return jsonify({'error': 'Please provide your OpenWeather API key, latitude and longitude.'}), 400

# Démarre l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
