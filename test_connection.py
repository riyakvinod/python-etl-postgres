import urllib.parse
from sqlalchemy import create_engine

# 1. TYPE YOUR REAL PASSWORD INSIDE THE QUOTES BELOW
raw_password = "Kodathethu@26"

# 2. This part "cleans" your password so Python doesn't get confused by @ or #
safe_password = urllib.parse.quote_plus(raw_password)

# 3. We build the connection string using the safe password
DATABASE_URL = f"postgresql://postgres:{safe_password}@localhost:5432/mydb"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ SUCCESS: Python is now connected to PostgreSQL!")
    connection.close()
except Exception as e:
    print("❌ ERROR: Still could not connect.")
    print(e)