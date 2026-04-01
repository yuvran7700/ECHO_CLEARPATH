# Contract test for GET /alert/collection (Staging).
#
# Validates the response body against the ADAGE 3.0 Tweet Dataset schema
# using OpenAPI 3.0 structural validation.

import os

import pytest
import requests
from dotenv import load_dotenv
from jsonschema import ValidationError
from openapi_schema_validator import OAS30Validator, validate

from .schemas.adage_tweet_dataset_schema import ADAGE_TWEET_DATASET_SCHEMA

load_dotenv()

BASE_URL = os.getenv("BASE_STAGING_URL")

VALID_PARAMS = {
    "base_query": "(from:T1SydneyTrains)",
    "start_date": "2026-03-01",
    "end_date": "2026-03-07",
}


def test_alert_collection_response_matches_adage_tweet_dataset_schema():
    """
    Verify the GET /alert/collection response structure matches the ADAGE
    3.0 Tweet Dataset schema defined in the Swagger spec
    """
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params=VALID_PARAMS,
    )

    assert response.status_code == 200

    try:
        # Validate the response body against the ADAGE Tweet Dataset schema.
        # OAS30Validator enforces OpenAPI 3.0 type and structure rules.
        validate(
            instance=response.json(),
            schema=ADAGE_TWEET_DATASET_SCHEMA,
            cls=OAS30Validator,
        )
    except ValidationError as e:
        # Build a readable failure message showing exactly where
        # in the response the schema violation occurred.
        path = " -> ".join(str(p) for p in e.absolute_path) or "<root>"
        pytest.fail(
            f"Schema validation failed:\n"
            f"  path   : {path}\n"
            f"  message: {e.message}\n"
            f"  value  : {e.instance!r}"
        )
