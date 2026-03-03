import requests
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from datetime import datetime

# --- 1. DATABASE CONFIGURATION ---
import os
# It will look for a GitHub password first, otherwise use your local one
DB_PASS = os.getenv("DB_PASS", "Kodathethu@26")
DB_NAME = "weather_db"
DB_USER = "postgres"

# This handles special characters in your password
safe_pass = urllib.parse.quote_plus(DB_PASS)
engine = create_engine(f"postgresql://{DB_USER}:{safe_pass}@localhost:5432/{DB_NAME}")

def fetch_weather():
    """Fetches live weather data for Berlin (Lat: 52.52, Lon: 13.41)"""
    print("☁️ Fetching live weather from API...")
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"

    response = requests.get(url)

    if response.status_code == 200:
       data = response.json()['current_weather']
       print(f"Success! Current Temp: {data['temperature']}°C")
       return data
    else:
       print("❌ Failed to get data")
       return none

def save_to_db(weather_data):
    """Saves the data into our PostgreSQL database"""
    # Create a DataFrame (Pandas table)
    df = pd.DataFrame([weather_data])
    
    # Add a column with the exact time we fetched the data
    df['recorded_at'] = datetime.now()

    print("📤 Saving to weather_db...")
    # 'append' means every time you run the script, it adds a NEW row
    df.to_sql("weather_history", engine, if_exists="append", index=False)
    print("✅ Saved to 'weather_history' table!")
if __name__ == "__main__":
    cities = {
        "Berlin": {"lat": 52.52, "lon": 13.41},
        "Tokyo": {"lat": 35.68, "lon": 139.69},
        "New York": {"lat": 40.71, "lon": -74.00},
        "London": {"lat": 51.50, "lon": -0.12}
    }

    # --- THE FIX ---
    # Check if we are running on GitHub (GitHub Actions sets an environment variable)
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("🤖 Running on GitHub, defaulting to Berlin.")
        choice = "Berlin"
    else:
        print("🌍 Available cities: Berlin, Tokyo, New York, London")
        choice = input("Enter city name (or press Enter for Berlin): ").title()
        if not choice:
            choice = "Berlin"
    # ---------------

    if choice in cities:
        lat = cities[choice]["lat"]
        lon = cities[choice]["lon"]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        
        try:
            response = requests.get(url)
            data = response.json()['current_weather']
            data['city'] = choice
            save_to_db(data)
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"❌ City '{choice}' not found.")