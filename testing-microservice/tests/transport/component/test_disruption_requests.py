# Component tests for GET /transport/disruption-forecast and
# GET /transport/disruption-analytics (Staging).
#
# Verifies the full request/response cycle against the deployed staging
# endpoint — covering successful responses and edge cases.

import requests


# ─── DISRUPTION FORECAST 200 SUCCESS ─────────────────────────────────────
def test_disruption_forecast_valid_request_returns_200(
    disruption_forecast_url,
):
    response = requests.get(disruption_forecast_url)
    assert response.status_code == 200


def test_disruption_forecast_response_has_body(disruption_forecast_url):
    response = requests.get(disruption_forecast_url)
    body = response.json()
    assert body is not None
    assert len(body) > 0


def test_disruption_forecast_response_has_correct_content_type(
    disruption_forecast_url,
):
    response = requests.get(disruption_forecast_url)
    assert response.headers["Content-Type"] == "application/json"


def test_disruption_forecast_response_contains_days(disruption_forecast_url):
    response = requests.get(disruption_forecast_url)
    assert "days" in response.json()
    assert isinstance(response.json()["days"], list)


def test_disruption_forecast_returns_5_days(disruption_forecast_url):
    response = requests.get(disruption_forecast_url)
    assert len(response.json()["days"]) == 5


def test_disruption_forecast_accepts_lat_lon_params(disruption_forecast_url):
    response = requests.get(
        disruption_forecast_url,
        params={"lat": "-33.8150", "lon": "151.0011"},
    )
    assert response.status_code == 200


def test_disruption_forecast_each_day_has_risk_level(disruption_forecast_url):
    response = requests.get(disruption_forecast_url)
    valid_levels = {"Low", "Moderate", "High", "Very High", "Unknown"}
    for day in response.json()["days"]:
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
def test_disruption_analytics_valid_request_returns_200(
    disruption_analytics_url,
):
    response = requests.get(disruption_analytics_url)
    assert response.status_code == 200


def test_disruption_analytics_response_has_body(disruption_analytics_url):
    response = requests.get(disruption_analytics_url)
    body = response.json()
    assert body is not None
    assert len(body) > 0


def test_disruption_analytics_response_has_correct_content_type(
    disruption_analytics_url,
):
    response = requests.get(disruption_analytics_url)
    assert response.headers["Content-Type"] == "application/json"


def test_disruption_analytics_response_contains_required_keys(
    disruption_analytics_url,
):
    response = requests.get(disruption_analytics_url)
    body = response.json()
    assert "overall" in body
    assert "best_worst_day_of_week" in body
    assert "best_worst_month" in body
    assert "weather_threshold_analysis" in body


def test_disruption_analytics_overall_has_required_fields(
    disruption_analytics_url,
):
    response = requests.get(disruption_analytics_url)
    overall = response.json()["overall"]
    assert "total_days" in overall
    assert "total_disruption_days" in overall
    assert "overall_disruption_rate" in overall
    assert "data_from" in overall
    assert "data_to" in overall


def test_disruption_analytics_day_of_week_has_7_days(disruption_analytics_url):
    response = requests.get(disruption_analytics_url)
    by_day = response.json()["best_worst_day_of_week"]["all_time"]["by_day"]
    assert len(by_day) == 7


def test_disruption_analytics_has_best_and_worst_day(disruption_analytics_url):
    response = requests.get(disruption_analytics_url)
    all_time = response.json()["best_worst_day_of_week"]["all_time"]
    assert "best" in all_time
    assert "worst" in all_time


def test_disruption_analytics_has_best_and_worst_month(
    disruption_analytics_url,
):
    response = requests.get(disruption_analytics_url)
    all_time = response.json()["best_worst_month"]["all_time"]
    assert "best" in all_time
    assert "worst" in all_time


def test_disruption_analytics_weather_threshold_has_required_keys(
    disruption_analytics_url,
):
    response = requests.get(disruption_analytics_url)
    weather = response.json()["weather_threshold_analysis"]
    assert "temperature" in weather
    assert "wind" in weather
    assert "rainfall" in weather
