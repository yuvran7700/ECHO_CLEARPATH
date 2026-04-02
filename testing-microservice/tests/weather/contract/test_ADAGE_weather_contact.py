# tests/weather/contract/test_weather_contact.py
# Contract test for GET /weather/collection (Staging).
#
# Validates the response body against the ADAGE 3.0 ADAGE Weather Record schema
# using OpenAPI 3.0 structural validation.

import pytest
import requests
from dotenv import load_dotenv
from jsonschema import ValidationError
from openapi_schema_validator import OAS30Validator, validate

from .schemas.ADAGE_weather_record_schema import ADAGE_WEATHER_RECORD_SCHEMA

load_dotenv()


def test_weather_collection_res_schema_match(weather_collection_url):
    """
    Verify the GET /weather/preprocessed response structure matches the ADAGE
    3.0 Weather Record schema defined in the Swagger spec
    """
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )

    assert response.status_code == 200

    try:
        # Validate the response body against the ADAGE Weather Record schema.
        # OAS30Validator enforces OpenAPI 3.0 type and structure rules.
        validate(
            instance=response.json(),
            schema=ADAGE_WEATHER_RECORD_SCHEMA,
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
