import os

import requests
from openapi_schema_validator import OAS30Validator, validate
from openapi_schema_validator.exceptions import OpenAPIValidationError
from schemas.adage_tweet_dataset_schema import ADAGE_TWEET_DATASET_SCHEMA

BASE_URL = os.getenv("BASE_STAGING_URL")

VALID_PARAMS = {
    "base_query": "(from:T1SydneyTrains)",
    "start_date": "2026-03-01",
    "end_date": "2026-03-07",
}


def test_create_alert_contract():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params=VALID_PARAMS,
    )

    assert response.status_code == 200

    try:
        validate(
            instance=response.json(),
            schema=ADAGE_TWEET_DATASET_SCHEMA,
            cls=OAS30Validator,
        )
    except OpenAPIValidationError as e:
        print(f"Validation failed: {e.message}")
