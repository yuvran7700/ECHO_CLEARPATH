# transport-microservice/src/scripts/backfill_weather_locations.py
from datetime import date
from decimal import Decimal

import requests

from src.dependencies.db_client import weather_location_table_staging
from src.utils.classifiers import (
    classify_humidity,
    classify_rainfall,
    classify_sun_from_condition,
    classify_temperature,
    classify_wind,
)

LOCATIONS = {
    "sydney": {"lat": -33.8688, "lon": 151.2093},
    "parramatta": {"lat": -33.8150, "lon": 151.0011},
}


def fetch_historical_range(
    lat: float, lon: float, start: date, end: date
) -> dict:
    response = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "windspeed_10m_max",
                "weathercode",
            ],
            "hourly": ["relativehumidity_2m"],
            "timezone": "Australia/Sydney",
        },
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(
            f"Open-Meteo failed: {response.status_code} {response.text}"
        )
    return response.json()


def weathercode_to_condition(code: int) -> str:
    if code == 0:
        return "clear sky"
    elif code in (1, 2):
        return "partly cloudy"
    elif code == 3:
        return "overcast clouds"
    elif code in range(51, 68) or code in range(80, 83):
        return "rain"
    elif code in range(71, 78):
        return "snow"
    elif code in range(95, 100):
        return "thunderstorm"
    else:
        return "overcast clouds"


def extract_humidity(
    hourly_humidity: list, day_index: int
) -> tuple[float, float]:
    """
    Hourly data is a flat list of 24 values per day.
    9am = day_index * 24 + 9
    3pm = day_index * 24 + 15
    """
    am_index = day_index * 24 + 9
    pm_index = day_index * 24 + 15
    return float(hourly_humidity[am_index]), float(hourly_humidity[pm_index])


def build_item(
    target_date: str,
    location: str,
    daily: dict,
    hourly_humidity: list,
    day_index: int,
) -> dict:
    temp_max = daily["temperature_2m_max"][day_index]
    temp_min = daily["temperature_2m_min"][day_index]
    rainfall_mm = daily["precipitation_sum"][day_index] or 0.0
    wind_kmh = daily["windspeed_10m_max"][day_index] or 0.0
    weathercode = daily["weathercode"][day_index]

    am_humidity, pm_humidity = extract_humidity(hourly_humidity, day_index)
    sun_condition = weathercode_to_condition(weathercode)

    return {
        "date": target_date,
        "location": location,
        "tempMin_C": Decimal(str(round(temp_min, 2))),
        "tempMax_C": Decimal(str(round(temp_max, 2))),
        "rainfall_mm": Decimal(str(round(rainfall_mm, 2))),
        "sunshineHours_hours": "Unavailable",
        "maxWindSpeed_kmh": Decimal(str(round(wind_kmh, 2))),
        "9am_temp_C": Decimal(str(round(temp_min, 2))),
        "9am_humidity_percent": Decimal(str(am_humidity)),
        "3pm_temp_C": Decimal(str(round(temp_max, 2))),
        "3pm_humidity_percent": Decimal(str(pm_humidity)),
        "tempSeverity": classify_temperature(temp_max, temp_min),
        "rainSeverity": classify_rainfall(rainfall_mm),
        "windSeverity": classify_wind(wind_kmh),
        "humiditySeverity": classify_humidity((am_humidity + pm_humidity) / 2),
        "sunSeverity": classify_sun_from_condition(sun_condition),
    }


if __name__ == "__main__":
    START = date(2024, 1, 1)
    END = date.today()

    for location, coords in LOCATIONS.items():
        print(f"\nBackfilling {location}...")
        try:
            data = fetch_historical_range(
                coords["lat"], coords["lon"], START, END
            )
            daily = data["daily"]
            hourly_humidity = data["hourly"]["relativehumidity_2m"]
            dates = daily["time"]

            success, failed = 0, []

            for i, target_date in enumerate(dates):
                try:
                    item = build_item(
                        target_date, location, daily, hourly_humidity, i
                    )
                    weather_location_table_staging.put_item(Item=item)
                    print(f"  ✓ {target_date}")
                    success += 1
                except Exception as e:
                    print(f"  ✗ {target_date}: {e}")
                    failed.append(target_date)

        except Exception as e:
            print(f"  Failed to fetch data for {location}: {e}")
            continue

        print(f"\n{location}: {success} written, {len(failed)} failed")
        if failed:
            print(f"  Failed dates: {failed}")
