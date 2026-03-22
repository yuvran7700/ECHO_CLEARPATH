import json
from datetime import datetime

from src.repositories.s3_repo import read_file


def ADAGE_lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    date = params.get("date", None)

    key = f"weather_collected/{date}.json"

    if not date:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing date parameter"}),
        }

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid date format - {e}"}),
        }

    try:
        rec = read_file(key)
    except ValueError:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Record not found"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(rec),
    }
