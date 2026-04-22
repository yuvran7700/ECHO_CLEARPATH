# tests/integration/test_parramatta_weather_client.py
from src.dependencies.weather_client import get_5_day_daily_forecast


def test_get_5_day_daily_forecast_returns_5_days():
    result = get_5_day_daily_forecast()
    assert len(result) == 5


def test_forecast_day_has_required_keys():
    result = get_5_day_daily_forecast()
    required_keys = {"date", "tempSeverity", "rainSeverity", "windSeverity"}
    for day in result:
        assert required_keys.issubset(day.keys())


def test_forecast_day_severities_are_valid_strings():
    result = get_5_day_daily_forecast()
    for day in result:
        assert isinstance(day["tempSeverity"], str)
        assert isinstance(day["rainSeverity"], str)
        assert isinstance(day["windSeverity"], str)
