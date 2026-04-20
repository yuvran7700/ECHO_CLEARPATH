# src/lambda_handlers/join_lambda_handler.py
import logging

from src.services.join_service import run_join_for_date

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def extract_dates_from_stream(event: dict) -> list[str]:
    dates = set()
    for record in event.get("Records", []):
        new_image = record.get("dynamodb", {}).get("NewImage", {})
        date = new_image.get("date", {}).get("S")
        if date:
            dates.add(date)
    return list(dates)


def join_lambda_handler(event, context):
    dates = extract_dates_from_stream(event)

    if not dates:
        logger.warning("No dates found in stream event — skipping join")
        return

    for date in dates:
        logger.info(f"Processing join for date: {date}")
        run_join_for_date(date)
