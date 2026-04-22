# src/marshallers/weather_marshaller.py
from datetime import date

from src.utils.classifiers import (
    classify_rainfall,
    classify_temperature,
    classify_wind,
)


def extract_day_metrics(daily: dict, index: int) -> dict:
    """
    Extract metrics for a single day from the flat daily arrays
    returned by the Parramatta forecast API.
    """
    return {
        "max_temp": daily["temperature_2m_max"][index],
        "min_temp": daily["temperature_2m_min"][index],
        "rainfall_mm": daily["precipitation_sum"][index],
        "max_wind": daily["windspeed_10m_max"][index],
    }


def classify_forecast_day(daily: dict, index: int) -> dict:
    metrics = extract_day_metrics(daily, index)

    return {
        "tempSeverity": classify_temperature(
            metrics["max_temp"], metrics["min_temp"]
        ),
        "rainSeverity": classify_rainfall(metrics["rainfall_mm"]),
        "windSeverity": classify_wind(metrics["max_wind"]),
    }


def extract_daily_weather(api_response: dict, num_days: int = 5) -> list[dict]:
    daily = api_response.get("daily", {})
    dates = daily.get("time", [])
    today = date.today().isoformat()

    days = []
    for i, date_str in enumerate(dates):
        if date_str < today:
            continue
        if len(days) >= num_days:
            break
        severities = classify_forecast_day(daily, i)
        days.append({"date": date_str, **severities})

    return days
