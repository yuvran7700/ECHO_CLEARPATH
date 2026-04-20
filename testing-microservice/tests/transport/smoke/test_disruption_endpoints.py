# testing-microservice/tests/transport/smoke/test_disruption_endpoints.py
import requests


def test_disruption_forecast_is_alive(disruption_forecast_url):
    response = requests.get(disruption_forecast_url)
    assert response.status_code == 200


def test_disruption_analytics_is_alive(disruption_analytics_url):
    response = requests.get(disruption_analytics_url)
    assert response.status_code == 200
