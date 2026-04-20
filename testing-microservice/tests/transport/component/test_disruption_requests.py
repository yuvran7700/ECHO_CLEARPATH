# Component tests for GET /transport/disruption-forecast and
# GET /transport/disruption-analytics (Staging).
#
# Verifies the full request/response cycle against the deployed staging
# endpoint — covering successful responses and edge cases.

import requests


# ─── DISRUPTION FORECAST 200 SUCCESS ─────────────────────────────────────
def test_disruption_forecast_valid_request_returns_200(forecast_response):
    assert forecast_response.status_code == 200


def test_disruption_forecast_response_has_body(forecast_response):
    body = forecast_response.json()
    assert body is not None
    assert len(body) > 0


def test_disruption_forecast_response_has_correct_content_type(
    forecast_response,
):
    assert forecast_response.headers["Content-Type"] == "application/json"


def test_disruption_forecast_response_contains_days(forecast_response):
    assert "days" in forecast_response.json()
    assert isinstance(forecast_response.json()["days"], list)


def test_disruption_forecast_returns_5_days(forecast_response):
    assert len(forecast_response.json()["days"]) == 5


def test_disruption_forecast_accepts_lat_lon_params(disruption_forecast_url):
    response = requests.get(
        disruption_forecast_url,
        params={"lat": "-33.8150", "lon": "151.0011"},
    )
    assert response.status_code == 200


def test_disruption_forecast_each_day_has_risk_level(forecast_response):
    valid_levels = {"Low", "Moderate", "High", "Very High", "Unknown"}
    for day in forecast_response.json()["days"]:
        assert day["risk_level"] in valid_levels


def test_disruption_forecast_invalid_lat_lon_returns_500(
    disruption_forecast_url,
):
    response = requests.get(
        disruption_forecast_url,
        params={"lat": "invalid", "lon": "invalid"},
    )
    assert response.status_code == 500


# ─── DISRUPTION ANALYTICS 200 SUCCESS ────────────────────────────────────
def test_disruption_analytics_valid_request_returns_200(analytics_response):
    assert analytics_response.status_code == 200


def test_disruption_analytics_response_has_body(analytics_response):
    body = analytics_response.json()
    assert body is not None
    assert len(body) > 0


def test_disruption_analytics_response_has_correct_content_type(
    analytics_response,
):
    assert analytics_response.headers["Content-Type"] == "application/json"


def test_disruption_analytics_response_contains_required_keys(
    analytics_response,
):
    body = analytics_response.json()
    assert "overall" in body
    assert "best_worst_day_of_week" in body
    assert "best_worst_month" in body
    assert "weather_threshold_analysis" in body


def test_disruption_analytics_overall_has_required_fields(analytics_response):
    overall = analytics_response.json()["overall"]
    assert "total_days" in overall
    assert "total_disruption_days" in overall
    assert "overall_disruption_rate" in overall
    assert "data_from" in overall
    assert "data_to" in overall


def test_disruption_analytics_day_of_week_has_7_days(analytics_response):
    by_day = analytics_response.json()["best_worst_day_of_week"]["all_time"][
        "by_day"
    ]
    assert len(by_day) == 7


def test_disruption_analytics_has_best_and_worst_day(analytics_response):
    all_time = analytics_response.json()["best_worst_day_of_week"]["all_time"]
    assert "best" in all_time
    assert "worst" in all_time


def test_disruption_analytics_has_best_and_worst_month(analytics_response):
    all_time = analytics_response.json()["best_worst_month"]["all_time"]
    assert "best" in all_time
    assert "worst" in all_time


def test_disruption_analytics_weather_threshold_has_required_keys(
    analytics_response,
):
    weather = analytics_response.json()["weather_threshold_analysis"]
    assert "temperature" in weather
    assert "wind" in weather
    assert "rainfall" in weather
