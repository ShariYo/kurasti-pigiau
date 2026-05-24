import os
from backend.scraper import get_all_lithuania_fuel
from backend.database import init_db, save_prices

def run_pipeline():
    # 1. Ensure the data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # 2. Setup the database
    init_db()

    # 3. Scrape the data
    print("Starting scraper...")
    data = get_all_lithuania_fuel()
    print(f"DEBUG: scraped {len(data)} station entries")

    # 4. Save to SQLite
    if data:
        save_prices(data)
    else:
        print("No data fetched. Check you API connection.")

if __name__ == "__main__":
    run_pipeline()