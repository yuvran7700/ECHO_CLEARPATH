# src/marshallers/weather_marshaller.py
from src.utils.classifiers import (
    classify_humidity,
    classify_rainfall,
    classify_sun_from_condition,
    classify_temperature,
    classify_wind,
)


def extract_day_metrics(day: dict) -> dict:
    daytime = day["daytimeForecast"]
    nighttime = day["nighttimeForecast"]

    return {
        "max_temp": day["maxTemperature"]["degrees"],
        "min_temp": day["minTemperature"]["degrees"],
        "rainfall_mm": daytime["precipitation"]["qpf"]["quantity"]
        + nighttime["precipitation"]["qpf"]["quantity"],
        "max_wind": max(
            daytime["wind"]["gust"]["value"],
            nighttime["wind"]["gust"]["value"],
        ),
        "avg_humidity": (
            daytime["relativeHumidity"] + nighttime["relativeHumidity"]
        )
        / 2,
        "weather_condition": daytime["weatherCondition"]["description"][
            "text"
        ],
    }


def classify_forecast_day(day: dict) -> dict:
    metrics = extract_day_metrics(day)

    return {
        "tempSeverity": classify_temperature(
            metrics["max_temp"], metrics["min_temp"]
        ),
        "rainSeverity": classify_rainfall(metrics["rainfall_mm"]),
        "windSeverity": classify_wind(metrics["max_wind"]),
        "humiditySeverity": classify_humidity(metrics["avg_humidity"]),
        "sunSeverity": classify_sun_from_condition(
            metrics["weather_condition"]
        ),
    }


def extract_daily_weather(google_response: dict) -> list[dict]:
    days = []

    for day in google_response.get("forecastDays", []):
        date = day["displayDate"]
        date_str = f"{date['year']}-{date['month']:02d}-{date['day']:02d}"

        weather_summary = (
            day.get("daytimeForecast", {})
            .get("weatherCondition", {})
            .get("description", {})
            .get("text", "Unknown")
        )

        severities = classify_forecast_day(day)

        days.append(
            {
                "date": date_str,
                "weather_summary": weather_summary,
                **severities,
            }
        )

    return days
