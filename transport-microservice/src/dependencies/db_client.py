"""
DynamoDB client initialisation and connection testing.

"""

import os

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
WEATHER_LOCATION_DB = "clearpath-weather-location-data"
ALERT_DB = "clearpath-alert-data"
JOINED_DB = "clearpath-weather-alert-joined"

# Initialise DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

# Reference your table
alert_table = dynamodb.Table(ALERT_DB)
joined_table = dynamodb.Table(JOINED_DB)
weather_location_table = dynamodb.Table(WEATHER_LOCATION_DB)


def check_table_status() -> bool:
    try:
        _ = alert_table.table_status
        print(f"DynamoDB connected: {ALERT_DB}")
        _ = joined_table.table_status
        print(f"DynamoDB connected: {JOINED_DB}")
        return True
    except Exception as e:
        print(f"DynamoDB connection failed: {e}")
        return False


if __name__ == "__main__":
    check_table_status()
