# tests/integration/test_lambda_handlers.py
import json

from src.dependencies.s3_client import ANALYTICS_BUCKET, s3_client
from src.lambda_handlers.analytics_lambda_handler import (
    analytics_lambda_handler,
)
from src.lambda_handlers.analytics_scheduled_lambda_handler import (
    analytics_scheduled_lambda_handler,
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


class TestAnalyticsScheduledLambdaHandler:
    def test_handler_completes_without_error(self):
        response = analytics_scheduled_lambda_handler({}, {})
        # handler has no return value — just assert it didn't raise
        assert response is None

    def test_analytics_json_written_to_s3(self):
        analytics_scheduled_lambda_handler({}, {})
        obj = s3_client.get_object(
            Bucket=ANALYTICS_BUCKET, Key="parramatta/analytics.json"
        )
        body = json.loads(obj["Body"].read().decode("utf-8"))
        assert "location" in body

    def test_disruption_rates_json_written_to_s3(self):
        analytics_scheduled_lambda_handler({}, {})
        obj = s3_client.get_object(
            Bucket=ANALYTICS_BUCKET, Key="parramatta/disruption_rates.json"
        )
        body = json.loads(obj["Body"].read().decode("utf-8"))
        assert "tempSeverity" in body
        assert "rainSeverity" in body
        assert "windSeverity" in body
