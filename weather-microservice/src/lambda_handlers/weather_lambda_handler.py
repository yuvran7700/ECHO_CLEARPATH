import json
from datetime import datetime

from src.marshellers.weather_adage_marshellers import format_db_adage
from src.repositories.db_repo import get_record
from src.utils.weather_utils import decimal_converter


def weather_lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    date = params.get("date", None)

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
            "body": json.dumps(
                {"error": "Invalid date format - Expected YYYY-MM-DD"}
            ),
        }

    rec = get_record(date)
    if rec is None:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Record not found"}),
        }

    formatted = format_db_adage(rec, date)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(formatted, default=decimal_converter),
    }
