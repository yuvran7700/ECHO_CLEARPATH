import json
import re
from datetime import datetime

from src.services.twitter_service import process_tweets_and_return_to_user


def twitter_collection_handler(event, context):
    """
    Lambda handler for retrieving tweets from the Twitter service.

    Expects query string parameters:
    - base_query
    - start_date
    - end_date

    Returns:
        dict: API Gateway response containing an ADAGE dataset
    """
    query_params = event.get("queryStringParameters") or {}

    base_query = (query_params.get("base_query") or "").strip()
    start_date = (query_params.get("start_date") or "").strip()
    end_date = (query_params.get("end_date") or "").strip()

    if not base_query or not start_date or not end_date:
        return _response(
            400,
            {"message": "base_query, start_date, and end_date are required"},
        )

    if not _has_valid_account_query(base_query):
        return _response(
            400,
            {"message": "base_query must include 'from:account_name' filter"},
        )

    if not _is_valid_date(start_date) or not _is_valid_date(end_date):
        return _response(
            400, {"message": "Dates must be in YYYY-MM-DD format"}
        )

    if start_date > end_date:
        return _response(
            400,
            {"message": "start_date must be earlier or equal to end_date"},
        )

    adage_payload = process_tweets_and_return_to_user(
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )

    return _response(200, adage_payload)


def _response(status_code: int, body: dict) -> dict:
    """Helper to standardise API responses."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _has_valid_account_query(base_query: str) -> bool:
    return re.search(r"\bfrom:[A-Za-z0-9_]+\b", base_query) is not None
