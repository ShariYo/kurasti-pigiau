from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import backend.database as database

app = FastAPI()

# Allows React app to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stations")
async def get_stations():
    # Returns the JSON data from database.py function
    return database.get_latest_prices()