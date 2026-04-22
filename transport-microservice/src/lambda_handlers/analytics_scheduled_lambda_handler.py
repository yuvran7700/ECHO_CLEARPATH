"""
transport-microservice/src/lambda_handlers/analytics_scheduled_lambda_handler.py
Triggered weekly by EventBridge. Recomputes analytics and disruption rates,
then writes both to S3 for use by the analytics and forecast endpoints.
"""

import json
import logging

from src.dependencies.s3_client import ANALYTICS_BUCKET, s3_client
from src.services.analytics_service import (
    compute_disruption_rates,
    generate_analytics_report,
    load_joined_analysis_df,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LOCATION = "parramatta"
ANALYTICS_KEY = "parramatta/analytics.json"
DISRUPTION_RATES_KEY = "parramatta/disruption_rates.json"


def analytics_scheduled_lambda_handler(event, context):
    logger.info("Weekly analytics recalc triggered")

    df = load_joined_analysis_df(location=LOCATION)

    report = generate_analytics_report(LOCATION)
    s3_client.put_object(
        Bucket=ANALYTICS_BUCKET,
        Key=ANALYTICS_KEY,
        Body=json.dumps(report),
        ContentType="application/json",
    )
    logger.info(
        "Analytics report written to S3: %s/%s",
        ANALYTICS_BUCKET,
        ANALYTICS_KEY,
    )

    disruption_rates = compute_disruption_rates(df)
    s3_client.put_object(
        Bucket=ANALYTICS_BUCKET,
        Key=DISRUPTION_RATES_KEY,
        Body=json.dumps(disruption_rates),
        ContentType="application/json",
    )
    logger.info(
        "Disruption rates written to S3: %s/%s",
        ANALYTICS_BUCKET,
        DISRUPTION_RATES_KEY,
    )
