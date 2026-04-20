import json

from src.services.disruption_forecast_service import (
    generate_5_day_risk_forecast,
)


def correlation_lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        lat = float(query_params.get("lat", -33.8150))
        lon = float(query_params.get("lon", 151.0011))
        location = query_params.get("location", "parramatta")

        result = generate_5_day_risk_forecast(lat, lon, location=location)

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
