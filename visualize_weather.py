import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
# Forces a window to pop up on Windows
matplotlib.use('TkAgg') 
from sqlalchemy import create_engine
import urllib.parse
import os

# --- 1. DATABASE SETUP (Matches your Tracker) ---
# This uses your real password locally but works on GitHub too
raw_password = os.getenv("DB_PASS", "Kodathethu@26")
DB_USER = "postgres"
DB_NAME = "weather_db"
DB_HOST = os.getenv("DB_HOST", "localhost")

safe_pass = urllib.parse.quote_plus(raw_password)
engine = create_engine(f"postgresql://{DB_USER}:{safe_pass}@{DB_HOST}:5432/{DB_NAME}")

def create_weather_chart():
    try:
        print("📊 Reading data from PostgreSQL...")
        
        # 2. FETCH DATA
        query = "SELECT temperature, recorded_at FROM weather_history ORDER BY recorded_at ASC"
        df = pd.read_sql(query, engine)

        if df.empty:
            print("❌ ERROR: No data found in the database.")
            print("👉 Action: Run 'python weather_tracker.py' 3 times first!")
            return

        # 3. CREATE THE PLOT
        print(f"🎨 Creating chart with {len(df)} data points...")
        plt.figure(figsize=(10, 5))
        
        plt.plot(df['recorded_at'], df['temperature'], marker='o', color='tab:blue', linestyle='-')

        plt.title('Temperature History Over Time', fontsize=14)
        plt.xlabel('Date & Time', fontsize=12)
        plt.ylabel('Temperature (°C)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.gcf().autofmt_xdate()

        # 4. SAVE AND SHOW
        plt.savefig('weather_plot.png')
        print("✅ SUCCESS: Chart saved as 'weather_plot.png' in your folder!")
        
        # This will open the window
        plt.show()

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    create_weather_chart()