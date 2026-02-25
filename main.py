import pandas as pd
import urllib.parse
from sqlalchemy import create_engine

# --- CONFIGURATION ---
DB_PASS = "Kodathethu@26" # <-- PUT YOUR PASSWORD HERE
DB_USER = "postgres"
DB_NAME = "mydb"

# Encode password for special characters
safe_pass = urllib.parse.quote_plus(DB_PASS)
engine = create_engine(f"postgresql://{DB_USER}:{safe_pass}@localhost:5432/{DB_NAME}")

def clean_data(df):
    """
    Intermediate cleaning steps
    """
    print("🧹 Cleaning data...")

# 1. Remove rows with missing (NaN) values
    df = df.dropna()
    
# 2. Clean 'name' column: remove extra spaces
    df['name'] = df['name'].str.strip()

# 3. Filter out rows where name became empty after stripping
    df = df[df['name'] != ""]
    
# 4. Standardize: Make all cities uppercase
    df['city'] = df['city'].str.upper()

    return df

def main():
    try:
        # STEP 1: Read
        print("📖 Reading data.csv...")
        df = pd.read_csv("data.csv")
        
        # STEP 2: Clean
        df_cleaned = clean_data(df)
        print(df_cleaned) # See the cleaned version in terminal
        
        # STEP 3: Save to PostgreSQL
        print("📤 Uploading to PostgreSQL...")
        # This creates a table named 'cleaned_users' automatically
        df_cleaned.to_sql("cleaned_users", engine, if_exists="replace", index=False)
        
        print("✅ SUCCESS! Check pgAdmin for the 'cleaned_users' table.")

    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    main()