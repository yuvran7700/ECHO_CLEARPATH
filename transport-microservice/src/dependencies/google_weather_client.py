# src/dependencies/google_weather_client.py
import os

import requests
from dotenv import load_dotenv

from src.marshallers.weather_marshaller import extract_daily_weather

load_dotenv()

GOOGLE_WEATHER_URL = "https://weather.googleapis.com/v1/forecast/days:lookup"


def fetch_5_day_forecast(lat: float, lon: float) -> dict:
    api_key = os.getenv("GOOGLE_WEATHER_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_WEATHER_API_KEY is missing")

    response = requests.get(
        GOOGLE_WEATHER_URL,
        params={
            "key": api_key,
            "location.latitude": lat,
            "location.longitude": lon,
            "days": 5,
            "unitsSystem": "METRIC",
            "pageSize": 5,
        },
        timeout=10,
    )

    if not response.ok:
        raise RuntimeError(
            f"Google Weather request failed: "
            f"{response.status_code} {response.text}"
        )

    return response.json()


def get_5_day_daily_forecast(lat: float, lon: float) -> list[dict]:
    """
    return cleaned 5-day daily forecast with severity classifications.
    """
    raw = fetch_5_day_forecast(lat, lon)
    return extract_daily_weather(raw)
