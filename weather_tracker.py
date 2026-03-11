import os
import requests
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from datetime import datetime

# 1. Database Configuration
raw_password = os.getenv("DB_PASS", "Kodathethu@26")
DB_USER = "postgres"
DB_NAME = "weather_db"
DB_HOST = os.getenv("DB_HOST", "localhost")

safe_pass = urllib.parse.quote_plus(raw_password)
engine = create_engine(f"postgresql://{DB_USER}:{safe_pass}@{DB_HOST}:5432/{DB_NAME}")

def fetch_weather():
    """Fetches live weather data for Berlin"""
    print("☁️ Fetching live weather from API...")
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
    response = requests.get(url)

    if response.status_code == 200:
       data = response.json()['current_weather']
       print(f"Success! Current Temp: {data['temperature']}°C")
       return data
    else:
       print("❌ Failed to get data")
       return None # Fixed: Needs capital N

def save_to_db(weather_data):
    """Saves the data into our PostgreSQL database AND a CSV for GitHub"""
    # Create a DataFrame
    df = pd.DataFrame([weather_data])
    df['recorded_at'] = datetime.now()

    print("📤 Saving to weather_db...")
    df.to_sql("weather_history", engine, if_exists="append", index=False)
    print("✅ Saved to 'weather_history' table!")

    # --- THE FIX: SAVE CSV HERE INSIDE THE FUNCTION ---
    df.to_csv("live_weatherdata.csv", index=False)
    print("📝 Created live_weatherdata.csv for GitHub.")

if __name__ == "__main__":
    cities = {
        "Berlin": {"lat": 52.52, "lon": 13.41},
        "Tokyo": {"lat": 35.68, "lon": 139.69},
        "New York": {"lat": 40.71, "lon": -74.00},
        "London": {"lat": 51.50, "lon": -0.12}
    }

    if os.getenv("GITHUB_ACTIONS") == "true":
        print("🤖 Running on GitHub, defaulting to Berlin.")
        choice = "Berlin"
    else:
        print("🌍 Available cities: Berlin, Tokyo, New York, London")
        choice = input("Enter city name (or press Enter for Berlin): ").title()
        if not choice:
            choice = "Berlin"

    if choice in cities:
        lat = cities[choice]["lat"]
        lon = cities[choice]["lon"]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        
        try:
            response = requests.get(url)
            data = response.json()['current_weather']
            data['city'] = choice
            save_to_db(data)
            
            # Verification: Read back from DB
            print("\n📊 --- DATABASE CONTENT ---")
            query = "SELECT * FROM weather_history"
            df_check = pd.read_sql(query, engine)
            print(df_check.tail()) # Show only the last few rows

        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"❌ City '{choice}' not found.")