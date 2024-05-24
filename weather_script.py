import requests
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BASE_URL = 'https://weather.talkpython.fm/api/weather'

# Function to fetch weather data
def fetch_weather(city: str, country: str):
    try:
        params = {
            'city': city,
            'country': country,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from the API: {e}")
        return None

# Function to create the SQLite database and table
def create_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY,
            city TEXT,
            temperature REAL,
            humidity INTEGER,
            wind_speed REAL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to store weather data in the database
def store_weather_data(data, city):
    try:
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather (city, temperature, humidity, wind_speed, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (city, data['temperature'], data['humidity'], data['wind_speed'], data['description']))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error storing data in the database: {e}")

# Main function to orchestrate the process
def main(city, country):
    create_database()
    weather_data = fetch_weather(city, country)
    if weather_data:
        print(weather_data)  # Print the JSON response for debugging
        parsed_data = {
            'temperature': weather_data['forecast']['temp'],
            'humidity': weather_data['forecast']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'description': weather_data['weather']['description']
        }
        store_weather_data(parsed_data, city)
        logging.info(f"Weather data for {city} stored successfully.")
    else:
        logging.error("Failed to retrieve weather data.")

if __name__ == '__main__':
    city = input("Enter the city name: ")
    country = input("Enter the country code (e.g., US for United States): ")
    main(city, country)
