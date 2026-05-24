import os
import sqlite3
from datetime import datetime

db_path = "data/fuel_prices.db"

def init_db():
    "Create DB if it doesn't exist"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT,
            brand TEXT,
            fuel_type TEXT,
            price REAL,
            last_checked TIMESTAMP,
            address TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_prices(price_list):
    """Expect a list of dictionaries from the scraper."""
    db_file = os.path.abspath(db_path)
    print(f"Saving to database: {db_file}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_inserted = 0

    for entry in price_list:
        address = entry.get("address")
        coords = entry.get("coords", [None, None])
        latitude = coords[0] if len(coords) > 0 else None
        longitude = coords[1] if len(coords) > 1 else None

        for fuel_type, price in entry["prices"].items():
            price_value = price["price"] if isinstance(price, dict) else price
            cursor.execute("""
                INSERT INTO fuel_prices (station_name, brand, fuel_type, price, last_checked, address, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("name"),
                entry.get("brand"),
                fuel_type,
                price_value,
                timestamp,
                address,
                latitude,
                longitude
            ))
            rows_inserted += 1
    
    conn.commit()
    conn.close()
    print(f"Successfully saved {rows_inserted} rows to the database.")

def get_latest_prices():
    """Retrieve the most recent prices for each fuel type at each station."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # allows accessing column by name
    cursor = conn.cursor()

    cursor.execute("""
        SELECT station_name, brand, fuel_type, price, last_checked, address, latitude, longitude
        FROM fuel_prices
        GROUP BY station_name, fuel_type
        ORDER BY last_checked DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]