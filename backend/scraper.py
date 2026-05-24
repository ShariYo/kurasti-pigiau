import requests
import json

# Lithuania bounding boxes split into 4 parts (min_lon,min_lat,max_lon,max_lat)
# Midpoints: lon=23.45, lat=55.15
lt_bbox_parts = [
    "20.9,53.8,23.45,55.15",    # Southwest
    "23.45,53.8,26.9,55.15",    # Southeast
    "20.9,55.15,23.45,56.5",    # Northwest
    "23.45,55.15,26.9,56.5"     # Northeast
]
api_url = "https://gas.didnt.work/api/stations"

# Headers to see me as a user
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://gas.didnt.work/?country=lt",
    "Accept": "application/json"
}

def get_all_lithuania_fuel():
    stations_found = 0
    all_stations = []
    
    for bbox in lt_bbox_parts:
        params = {
            "bbox": bbox
        }

        try:
            print(f"Requesting data for LT fuel (bbox: {bbox})...")
            print(f"Requesting: {api_url}")
            print(f"Params: {params}")
            response = requests.get(api_url, params=params, headers=headers)
            print(f"Full URL: {response.url}")

            # Check if request was successful
            if response.status_code != 200:
                print(f"Error: Server returned status {response.status_code}")
                print(f"Response: {response.text}")
                continue
            
            data = response.json()
            print(f"Data received: {len(data)} stations from this bbox")
            print(f"Sample: {data[:1] if data else 'Empty'}")
            all_stations.extend(data)

        except Exception as e:
            print(f"An error occured: {e}")
            continue
    
    # Process all collected stations
    for station in all_stations:
        name = station.get("name", "N/A")
        brand = station.get("brand", "N/A")
        address = station.get("address", "N/A")
        coords = station.get("coords", [None, None])
        prices = station.get("prices", {})

        print(f"Station: {name} ({brand})")
        for fuel_type, price in prices.items():
            price_value = price["price"] if isinstance(price, dict) else price
            print(f"    - {fuel_type}: {price_value}€")
        
        stations_found += 1

    print(f"\nSuccess! Found {stations_found} stations.")
    return all_stations

if __name__ == "__main__":
    get_all_lithuania_fuel()