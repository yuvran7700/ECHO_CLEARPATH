# tests/integration/test_disruption_forecast_service.py
import pytest
from src.services.disruption_forecast_service import (
    generate_5_day_risk_forecast,
)

VALID_RISK_LEVELS = {"Low", "Moderate", "High", "Very High", "Unknown"}


@pytest.fixture(scope="module")
def live_forecast():
    """Call the real forecast service once for all tests in this module."""
    return generate_5_day_risk_forecast(
        lat=-33.8150,
        lon=151.0011,
        location="parramatta",
    )


class TestGenerate5DayRiskForecast:
    def test_returns_lat_and_lon(self, live_forecast):
        assert "lat" in live_forecast
        assert "lon" in live_forecast

    def test_returns_5_days(self, live_forecast):
        assert len(live_forecast["days"]) == 5

    def test_each_day_has_required_fields(self, live_forecast):
        required_fields = [
            "date",
            "tempSeverity",
            "rainSeverity",
            "windSeverity",
            "risk",
            "risk_level",
            "message",
        ]
        for day in live_forecast["days"]:
            for field in required_fields:
                assert field in day, f"Missing field: {field}"

    def test_each_day_has_no_dropped_fields(self, live_forecast):
        dropped_fields = ["weather_summary", "humiditySeverity", "sunSeverity"]
        for day in live_forecast["days"]:
            for field in dropped_fields:
                assert (
                    field not in day
                ), f"Dropped field still present: {field}"

    def test_risk_level_is_valid(self, live_forecast):
        for day in live_forecast["days"]:
            assert day["risk_level"] in VALID_RISK_LEVELS

    def test_risk_is_between_0_and_1(self, live_forecast):
        for day in live_forecast["days"]:
            if day["risk"] is not None:
                assert 0 <= day["risk"] <= 1

    def test_dates_are_in_order(self, live_forecast):
        dates = [day["date"] for day in live_forecast["days"]]
        assert dates == sorted(dates)

    def test_message_is_non_empty_string(self, live_forecast):
        for day in live_forecast["days"]:
            assert isinstance(day["message"], str)
            assert len(day["message"]) > 0

    def test_severity_labels_are_valid(self, live_forecast):
        valid_temp = {"Hot", "Warm", "Mild", "Cold"}
        valid_rain = {"Heavy rain", "Moderate rain", "Light rain", "No rain"}
        valid_wind = {"Gale", "Windy", "Breezy", "Calm"}

        for day in live_forecast["days"]:
            assert day["tempSeverity"] in valid_temp
            assert day["rainSeverity"] in valid_rain
            assert day["windSeverity"] in valid_wind
