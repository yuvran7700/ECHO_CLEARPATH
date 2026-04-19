import logging
from datetime import datetime
from pathlib import Path

from src.dependencies.s3_client import S3_BUCKET_NAME
from src.repositories.db_repo import get_record
from src.services.weather_attributes import process_collected_s3_object

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def collection_lambda_handler(event, context):
    for record in event.get("Records", []):
        bucket = str(record["s3"]["bucket"]["name"])
        if bucket != S3_BUCKET_NAME:
            logger.error("Error: Incorrect bucket name")
            continue

        event_type = str(record["eventName"])
        if not event_type.startswith("ObjectCreated:"):
            logger.error("Error: Incorrect trigger")
            continue

        try:
            key = str(record["s3"]["object"]["key"])
        except KeyError:
            logger.error(
                "Error: Key cannot be found in record, skipping object"
            )
            continue

        if not key.startswith("weather_collected/"):
            logger.error("Error: Wrong bucket folder")
            continue

        date = Path(key).stem
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except Exception:
            logger.error("Error: Invalid date key format")
            continue

        eTag = str(record["s3"]["object"]["eTag"])
        existing = get_record(date)
        if existing is None:
            logger.error("Record does not exist, creating now")
            process_collected_s3_object(key, eTag)
            continue

        try:
            existing["eTag"]
        except Exception:
            logger.error("DynamodDB record must have eTag attached")
            process_collected_s3_object(key, eTag)
            continue

        if eTag != existing["eTag"]:
            logger.error("Updating record")
            process_collected_s3_object(key, eTag)
