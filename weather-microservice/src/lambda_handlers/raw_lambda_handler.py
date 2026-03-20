import csv
import logging
from io import StringIO

from src.dependencies.s3_client import S3_BUCKET_NAME
from src.marshellers.raw_adage_marshellers import format_raw_adage
from src.repositories.s3_repo import read_untouched_file
from src.services.raw_extraction import extract_attributes

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def raw_lambda_handler(event, context):
    for record in event.get("Records", []):
        bucket = str(record["s3"]["bucket"]["name"])
        if bucket != S3_BUCKET_NAME:
            print("Error: Incorrect bucket name")
            continue

        event_type = str(record["eventName"])
        if not event_type.startswith("ObjectCreated:"):
            print("Error: Incorrect trigger")
            continue

        try:
            key = str(record["s3"]["object"]["key"])
        except KeyError:
            print("Error: Key cannot be found in record, skipping object")
            continue

        if not key.startswith("weather_raw/"):
            print("Error: Wrong bucket folder")
            continue

        try:
            res = read_untouched_file(key)
            csv_content = res["Body"].read().decode("utf-8-sig")
            csv_reader = csv.DictReader(StringIO(csv_content))
        except Exception as e:
            logger.error(f"Failed to read CSV from S3: {str(e)}")

        for row in csv_reader:
            try:
                attributes = extract_attributes(row)
                collect_adage = format_raw_adage(
                    attributes, attributes["date"]
                )
                print(collect_adage)
            except Exception as e:
                logger.error(f"Skipping row {row} due to error: {e}")
                continue
