# src/dependencies/parramatta_weather_client.py
import requests

from src.marshallers.weather_marshaller import extract_daily_weather

PARRAMATTA_FORECAST_URL = (
    "https://pphhzz75g2.execute-api.us-east-1.amazonaws.com/dev/retrieve"
)
PARRAMATTA_SOURCE = "parramatta_forecast"


def fetch_5_day_forecast() -> dict:
    """
    Fetch the raw forecast payload from the Parramatta forecast API.

    The endpoint is fixed to a single source and requires no auth or
    co-ordinate parameters — location is implicit in the source value.
    The `lat` / `lon` parameters are accepted for interface parity with
    the previous Google Weather client but are intentionally unused; the
    API determines the location from the `source` query parameter.
    """
    response = requests.get(
        PARRAMATTA_FORECAST_URL,
        params={"source": PARRAMATTA_SOURCE},
        timeout=10,
    )

    if not response.ok:
        raise RuntimeError(
            f"Parramatta forecast request failed: "
            f"{response.status_code} {response.text}"
        )

    return response.json()


def get_5_day_daily_forecast(
    lat: float = None, lon: float = None
) -> list[dict]:
    """
    Return cleaned 5-day daily forecast with severity classifications.

    `lat` and `lon` are accepted for drop-in interface parity with the
    previous Google Weather client but are not forwarded to the API.
    """
    raw = fetch_5_day_forecast()
    return extract_daily_weather(raw, num_days=5)
