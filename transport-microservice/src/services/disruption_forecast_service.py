"""
transport-microservice/src/services/disruption_forecast_service.py

Generates a 5-day T1 disruption risk forecast for a given location.
Fetches weather forecast data, classifies each day's conditions into
severity labels, and applies weighted disruption rates from the analytics
service to produce a risk score and risk level per day.
"""

import json

from src.dependencies.s3_client import ANALYTICS_BUCKET, s3_client
from src.dependencies.weather_client import (
    get_5_day_daily_forecast,  # changed: new client
)

WEIGHTS = {
    "tempSeverity": 0.60,
    "rainSeverity": 0.25,
    "windSeverity": 0.15,
}


def classify_risk(probability: float) -> str:
    if probability < 0.3:
        return "Low"
    if probability < 0.4:
        return "Moderate"
    if probability < 0.45:
        return "High"
    return "Very High"


def predict_disruption_risk_from_conditions(
    conditions: dict, disruption_rates: dict
) -> dict:
    total_weight = 0.0
    weighted_risk = 0.0

    for factor, weight in WEIGHTS.items():
        value = conditions.get(factor)
        rate = disruption_rates.get(factor, {}).get(value)

        if rate is not None:
            weighted_risk += rate * weight
            total_weight += weight

    if total_weight == 0:
        return {"risk": None, "risk_level": "Unknown"}

    final_risk = weighted_risk / total_weight
    return {
        "risk": round(final_risk, 4),
        "risk_level": classify_risk(final_risk),
    }


def generate_5_day_risk_forecast(
    lat: float, lon: float, location: str = "parramatta"
) -> dict:
    obj = s3_client.get_object(
        Bucket=ANALYTICS_BUCKET, Key=f"{location}/disruption_rates.json"
    )
    disruption_rates = json.loads(obj["Body"].read().decode("utf-8"))
    forecast_days = get_5_day_daily_forecast(lat, lon)

    results = []

    for day in forecast_days:
        conditions = {
            "tempSeverity": day["tempSeverity"],
            "rainSeverity": day["rainSeverity"],
            "windSeverity": day["windSeverity"],
        }
        prediction = predict_disruption_risk_from_conditions(
            conditions, disruption_rates
        )

        results.append(
            {
                "date": day["date"],
                "tempSeverity": day["tempSeverity"],
                "rainSeverity": day["rainSeverity"],
                "windSeverity": day["windSeverity"],
                "risk": prediction["risk"],
                "risk_level": prediction["risk_level"],
                "message": (
                    f"Based on forecasted conditions, this train line has a "
                    f"{prediction['risk'] * 100:.0f}% estimated disruption "
                    f"risk ({prediction['risk_level']})."
                    if prediction["risk"] is not None
                    else "Unable to estimate disruption risk for this day."
                ),
            }
        )

    return {"lat": lat, "lon": lon, "days": results}
