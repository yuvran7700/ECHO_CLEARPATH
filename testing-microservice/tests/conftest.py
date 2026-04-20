import boto3
import pytest


def get_ssm_parameter(name: str) -> str:
    ssm = boto3.client("ssm", region_name="us-east-1")
    response = ssm.get_parameter(Name=name)
    return response["Parameter"]["Value"]


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="staging",
        choices=["staging", "prod"],
        help="Environment to run tests against",
    )


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def api_base_url(env):
    api_id = get_ssm_parameter(f"/clearpath/{env}/api-id")
    return f"https://{api_id}.execute-api.us-east-1.amazonaws.com"


@pytest.fixture(scope="session")
def weather_preprocessed_url(api_base_url):
    return f"{api_base_url}/weather/preprocessed"


@pytest.fixture(scope="session")
def weather_collection_url(api_base_url):
    return f"{api_base_url}/weather/collection"


@pytest.fixture(scope="session")
def alert_collection_url(api_base_url):
    return f"{api_base_url}/alert/collection"


@pytest.fixture(scope="session")
def weather_table_name(env):
    if env == "staging":
        return "clearpath-weather-data-staging"
    return "clearpath-weather-data"


@pytest.fixture(scope="session")
def alert_table_name(env):
    if env == "staging":
        return "clearpath-alert-data-staging"
    return "clearpath-alert-data"


@pytest.fixture(scope="session")
def s3_bucket_name(env):
    if env == "staging":
        return "clearpath-weather-index-v1-staging"
    return "clearpath-weather-index-v1-prod"


@pytest.fixture(scope="session")
def valid_alert_params():
    return {
        "base_query": "(from:T1SydneyTrains)",
        "start_date": "2026-03-01",
        "end_date": "2026-03-07",
    }


@pytest.fixture(scope="session")
def disruption_forecast_url(api_base_url):
    return f"{api_base_url}/transport/disruption-forecast"


@pytest.fixture(scope="session")
def disruption_analytics_url(api_base_url):
    return f"{api_base_url}/transport/disruption-analytics"
