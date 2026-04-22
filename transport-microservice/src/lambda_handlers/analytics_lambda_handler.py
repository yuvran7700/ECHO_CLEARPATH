# transport-microservice/src/lambda_handlers/analytics_lambda_handler.py
import json

from src.dependencies.s3_client import ANALYTICS_BUCKET, s3_client

KEY = "parramatta/analytics.json"


def analytics_lambda_handler(event, context):
    try:
        obj = s3_client.get_object(Bucket=ANALYTICS_BUCKET, Key=KEY)
        body = obj["Body"].read().decode("utf-8")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": body,
        }
    except s3_client.exceptions.NoSuchKey:
        return {
            "statusCode": 503,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {"error": "Analytics not yet generated. Try again later."}
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
