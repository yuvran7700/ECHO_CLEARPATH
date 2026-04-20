# tests/integration/test_lambda_handlers.py
import json

from src.lambda_handlers.analytics_lambda_handler import (
    analytics_lambda_handler,
)
from src.lambda_handlers.correlation_lambda_handler import (
    correlation_lambda_handler,
)
from src.lambda_handlers.join_lambda_handler import join_lambda_handler


class TestCorrelationLambdaHandler:
    def test_returns_200_with_default_location(self):
        event = {"queryStringParameters": None}
        response = correlation_lambda_handler(event, {})
        assert response["statusCode"] == 200

    def test_response_body_is_valid_json(self):
        event = {"queryStringParameters": None}
        response = correlation_lambda_handler(event, {})
        body = json.loads(response["body"])
        assert "days" in body

    def test_accepts_lat_lon_params(self):
        event = {
            "queryStringParameters": {"lat": "-33.8150", "lon": "151.0011"}
        }
        response = correlation_lambda_handler(event, {})
        assert response["statusCode"] == 200

    def test_returns_500_on_invalid_params(self):
        event = {"queryStringParameters": {"lat": "invalid", "lon": "invalid"}}
        response = correlation_lambda_handler(event, {})
        assert response["statusCode"] == 500


class TestAnalyticsLambdaHandler:
    def test_returns_200(self):
        event = {}
        response = analytics_lambda_handler(event, {})
        assert response["statusCode"] == 200

    def test_response_body_is_valid_json(self):
        event = {}
        response = analytics_lambda_handler(event, {})
        body = json.loads(response["body"])
        assert "location" in body

    def test_returns_500_on_invalid_location(self):
        from unittest.mock import patch

        with patch(
            "src.lambda_handlers.analytics_lambda_handler.generate_analytics_report",
            side_effect=Exception("forced error"),
        ):
            event = {}
            response = analytics_lambda_handler(event, {})
            assert response["statusCode"] == 500
            body = json.loads(response["body"])
            assert "error" in body


class TestJoinLambdaHandler:
    def test_skips_when_no_dates_in_event(self):
        event = {"Records": []}
        response = join_lambda_handler(event, {})
        assert response is None

    def test_processes_valid_stream_event(self):
        event = {
            "Records": [
                {"dynamodb": {"NewImage": {"date": {"S": "2025-07-01"}}}}
            ]
        }
        response = join_lambda_handler(event, {})
        assert response is None
