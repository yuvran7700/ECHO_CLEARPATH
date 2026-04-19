# transport-microservice/src/lambda_handlers/analytics_lambda_handler.py
import json

from src.services.analytics_service import generate_analytics_report

LOCATION = "parramatta"


def analytics_lambda_handler(event, context):
    try:
        result = generate_analytics_report(LOCATION)
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
