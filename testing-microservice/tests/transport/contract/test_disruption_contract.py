# Contract tests for GET /transport/disruption-forecast and
# GET /transport/disruption-analytics
#
# Validates response bodies against schemas defined in the Swagger spec
# using OpenAPI 3.0 structural validation.

import pytest
import requests
from jsonschema import ValidationError
from openapi_schema_validator import OAS30Validator, validate

from .schemas.disruption_analytics_schema import DISRUPTION_ANALYTICS_SCHEMA
from .schemas.disruption_forecast_schema import DISRUPTION_FORECAST_SCHEMA


def test_disruption_forecast_response_matches_schema(disruption_forecast_url):
    """
    Verify the GET /transport/disruption-forecast response structure
    matches the DisruptionForecastResponse schema defined in the Swagger spec.
    """
    response = requests.get(disruption_forecast_url)

    assert response.status_code == 200

    try:
        validate(
            instance=response.json(),
            schema=DISRUPTION_FORECAST_SCHEMA,
            cls=OAS30Validator,
        )
    except ValidationError as e:
        path = " -> ".join(str(p) for p in e.absolute_path) or "<root>"
        pytest.fail(
            f"Schema validation failed:\n"
            f"  path   : {path}\n"
            f"  message: {e.message}\n"
            f"  value  : {e.instance!r}"
        )


def test_disruption_analytics_response_matches_schema(
    disruption_analytics_url,
):
    """
    Verify the GET /transport/disruption-analytics response structure
    matches the DisruptionAnalyticsResponse schema defined in the Swagger spec.
    """
    response = requests.get(disruption_analytics_url)

    assert response.status_code == 200

    try:
        validate(
            instance=response.json(),
            schema=DISRUPTION_ANALYTICS_SCHEMA,
            cls=OAS30Validator,
        )
    except ValidationError as e:
        path = " -> ".join(str(p) for p in e.absolute_path) or "<root>"
        pytest.fail(
            f"Schema validation failed:\n"
            f"  path   : {path}\n"
            f"  message: {e.message}\n"
            f"  value  : {e.instance!r}"
        )
