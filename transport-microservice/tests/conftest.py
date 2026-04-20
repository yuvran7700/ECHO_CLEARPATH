# tests/conftest.py
from decimal import Decimal

import boto3
import pandas as pd
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="staging",
        choices=["staging", "prod"],
        help="Environment to run tests against",
    )


@pytest.fixture(scope="session")
def dynamodb():
    return boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="session")
def live_joined_table(dynamodb, joined_table_name):
    return dynamodb.Table(joined_table_name)


@pytest.fixture(scope="session")
def live_weather_location_table(dynamodb, weather_location_table_name):
    return dynamodb.Table(weather_location_table_name)


@pytest.fixture(scope="session")
def live_alert_table(dynamodb, alert_table_name):
    return dynamodb.Table(alert_table_name)


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def joined_table_name(env):
    if env == "staging":
        return "clearpath-weather-alert-joined-staging"
    return "clearpath-weather-alert-joined"


@pytest.fixture(scope="session")
def weather_location_table_name(env):
    if env == "staging":
        return "clearpath-weather-location-data-staging"
    return "clearpath-weather-location-data"


@pytest.fixture(scope="session")
def alert_table_name(env):
    if env == "staging":
        return "clearpath-alert-data-staging"
    return "clearpath-alert-data"


@pytest.fixture(scope="session")
def disruption_forecast_url(env):
    api_id = get_ssm_parameter(f"/clearpath/{env}/api-id")
    return f"https://{api_id}.execute-api.us-east-1.amazonaws.com/transport/disruption-forecast"


@pytest.fixture(scope="session")
def disruption_analytics_url(env):
    api_id = get_ssm_parameter(f"/clearpath/{env}/api-id")
    return f"https://{api_id}.execute-api.us-east-1.amazonaws.com/transport/disruption-analytics"


def get_ssm_parameter(name: str) -> str:
    ssm = boto3.client("ssm", region_name="us-east-1")
    response = ssm.get_parameter(Name=name)
    return response["Parameter"]["Value"]


@pytest.fixture
def forecast_day_factory():
    """
    Factory fixture that returns a function to create a Google Weather API
    forecast day dict with sensible defaults that can be overridden.
    """

    def make_forecast_day(
        max_temp=25.0,
        min_temp=15.0,
        day_rainfall=2.0,
        night_rainfall=1.0,
        day_gust=30.0,
        night_gust=25.0,
        day_humidity=60,
        night_humidity=70,
        weather_condition="Sunny",
        year=2026,
        month=4,
        day=20,
    ):
        return {
            "displayDate": {"year": year, "month": month, "day": day},
            "maxTemperature": {"degrees": max_temp},
            "minTemperature": {"degrees": min_temp},
            "daytimeForecast": {
                "precipitation": {"qpf": {"quantity": day_rainfall}},
                "wind": {"gust": {"value": day_gust}},
                "relativeHumidity": day_humidity,
                "weatherCondition": {
                    "description": {"text": weather_condition}
                },
            },
            "nighttimeForecast": {
                "precipitation": {"qpf": {"quantity": night_rainfall}},
                "wind": {"gust": {"value": night_gust}},
                "relativeHumidity": night_humidity,
            },
        }

    return make_forecast_day


@pytest.fixture
def sunny_mild_day(forecast_day_factory):
    return forecast_day_factory(
        max_temp=22.0,
        min_temp=14.0,
        day_rainfall=0.0,
        night_rainfall=0.0,
        day_gust=25.0,
        night_gust=20.0,
        day_humidity=50,
        night_humidity=55,
        weather_condition="Sunny",
    )


@pytest.fixture
def cold_heavy_rain_day(forecast_day_factory):
    return forecast_day_factory(
        max_temp=10.0,
        min_temp=5.0,
        day_rainfall=15.0,
        night_rainfall=15.0,
        day_gust=65.0,
        night_gust=60.0,
        day_humidity=85,
        night_humidity=90,
        weather_condition="Heavy rain",
    )


@pytest.fixture
def hot_dry_day(forecast_day_factory):
    return forecast_day_factory(
        max_temp=38.0,
        min_temp=28.0,
        day_rainfall=0.0,
        night_rainfall=0.0,
        day_gust=20.0,
        night_gust=15.0,
        day_humidity=25,
        night_humidity=20,
        weather_condition="Sunny",
    )


@pytest.fixture
def five_day_forecast_response(forecast_day_factory):
    return {
        "forecastDays": [
            forecast_day_factory(year=2026, month=4, day=day)
            for day in range(20, 25)
        ]
    }


@pytest.fixture
def raw_dynamodb_records():
    """Raw records as they come from DynamoDB with Decimal types."""
    return [
        {
            "date": "2025-07-01",
            "rainfall_mm": Decimal("5.5"),
            "tempMax_C": Decimal("25.0"),
            "disruption": "True",
        },
        {
            "date": "2025-07-02",
            "rainfall_mm": Decimal("0.0"),
            "tempMax_C": Decimal("22.0"),
            "disruption": "False",
        },
        {
            "date": "2025-07-03",
            "rainfall_mm": Decimal("12.0"),
            "tempMax_C": Decimal("18.0"),
            "disruption": "True",
        },
    ]


@pytest.fixture
def raw_dynamodb_df(raw_dynamodb_records):
    return pd.DataFrame(raw_dynamodb_records)


@pytest.fixture
def records_with_missing_data():
    """Records with missing disruption and rainfall values."""
    return [
        {"date": "2025-08-01", "rainfall_mm": None, "disruption": "True"},
        {
            "date": "2025-08-02",
            "rainfall_mm": Decimal("5.0"),
            "disruption": None,
        },
        {
            "date": "2025-08-03",
            "rainfall_mm": Decimal("3.0"),
            "disruption": "False",
        },
    ]


@pytest.fixture
def df_with_missing_data(records_with_missing_data):
    return pd.DataFrame(records_with_missing_data)


@pytest.fixture
def sample_analytics_df():
    """A controlled DataFrame for testing analytics functions."""
    return pd.DataFrame(
        [
            {
                "date": "2025-01-06",
                "disruption": True,
                "tempMax_C": 35.0,
                "maxWindSpeed_kmh": 65.0,
                "rainfall_mm": 30.0,
                "tempSeverity": "Hot",
                "rainSeverity": "Heavy rain",
                "windSeverity": "Gale",
                "humiditySeverity": "High Humidity",
                "sunSeverity": "Cloudy",
            },
            {
                "date": "2025-01-07",
                "disruption": True,
                "tempMax_C": 32.0,
                "maxWindSpeed_kmh": 50.0,
                "rainfall_mm": 15.0,
                "tempSeverity": "Hot",
                "rainSeverity": "Moderate rain",
                "windSeverity": "Windy",
                "humiditySeverity": "High Humidity",
                "sunSeverity": "Cloudy",
            },
            {
                "date": "2025-03-01",
                "disruption": False,
                "tempMax_C": 22.0,
                "maxWindSpeed_kmh": 30.0,
                "rainfall_mm": 0.0,
                "tempSeverity": "Warm",
                "rainSeverity": "No rain",
                "windSeverity": "Breezy",
                "humiditySeverity": "Moderate Humidity",
                "sunSeverity": "Sunny",
            },
            {
                "date": "2025-03-08",
                "disruption": False,
                "tempMax_C": 20.0,
                "maxWindSpeed_kmh": 25.0,
                "rainfall_mm": 0.0,
                "tempSeverity": "Mild",
                "rainSeverity": "No rain",
                "windSeverity": "Breezy",
                "humiditySeverity": "Moderate Humidity",
                "sunSeverity": "Sunny",
            },
            {
                "date": "2025-03-15",
                "disruption": True,
                "tempMax_C": 28.0,
                "maxWindSpeed_kmh": 40.0,
                "rainfall_mm": 8.0,
                "tempSeverity": "Warm",
                "rainSeverity": "Light rain",
                "windSeverity": "Windy",
                "humiditySeverity": "High Humidity",
                "sunSeverity": "Partly Cloudy",
            },
            {
                "date": "2025-06-07",
                "disruption": False,
                "tempMax_C": 18.0,
                "maxWindSpeed_kmh": 20.0,
                "rainfall_mm": 0.0,
                "tempSeverity": "Mild",
                "rainSeverity": "No rain",
                "windSeverity": "Breezy",
                "humiditySeverity": "Moderate Humidity",
                "sunSeverity": "Sunny",
            },
            {
                "date": "2025-06-14",
                "disruption": False,
                "tempMax_C": 16.0,
                "maxWindSpeed_kmh": 15.0,
                "rainfall_mm": 0.0,
                "tempSeverity": "Mild",
                "rainSeverity": "No rain",
                "windSeverity": "Calm",
                "humiditySeverity": "Low Humidity",
                "sunSeverity": "Sunny",
            },
        ]
    )


@pytest.fixture
def sample_disruption_rates():
    """Sample blended disruption rates for testing predictions."""
    return {
        "tempSeverity": {
            "Hot": 0.72,
            "Warm": 0.50,
            "Mild": 0.25,
            "Cold": 0.30,
        },
        "rainSeverity": {
            "Heavy rain": 0.90,
            "Moderate rain": 0.70,
            "Light rain": 0.50,
            "No rain": 0.15,
        },
        "windSeverity": {
            "Gale": 0.70,
            "Windy": 0.50,
            "Breezy": 0.30,
            "Calm": 0.10,
        },
        "humiditySeverity": {
            "Extreme Humidity": 0.55,
            "High Humidity": 0.45,
            "Moderate Humidity": 0.25,
            "Low Humidity": 0.10,
        },
        "sunSeverity": {"Cloudy": 0.55, "Partly Cloudy": 0.35, "Sunny": 0.15},
    }


@pytest.fixture
def weather_item():
    """A sample weather record as it comes from the weather location table."""
    return {
        "date": "2025-07-01",
        "location": "parramatta",
        "tempMax_C": 25.0,
        "tempMin_C": 15.0,
        "rainfall_mm": 5.0,
        "tempSeverity": "Warm",
        "rainSeverity": "Light rain",
        "windSeverity": "Breezy",
        "humiditySeverity": "Moderate Humidity",
        "sunSeverity": "Sunny",
    }


@pytest.fixture
def alert_item():
    """A sample alert record as it comes from the alert table."""
    return {
        "date": "2025-07-01",
        "account_name": "T1 Sydney Trains",
        "classification": "unknown",
    }
