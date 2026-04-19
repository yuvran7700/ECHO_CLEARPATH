import json

from src.services.disruption_forecast_service import (
    generate_5_day_risk_forecast,
)


# correlation_lambda_handler.py - ONLY HTTP concerns
def correlation_lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        lat = float(query_params.get("lat", -33.8688))
        lon = float(query_params.get("lon", 151.2093))

        result = generate_5_day_risk_forecast(
            lat, lon
        )  # facade does everything

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
