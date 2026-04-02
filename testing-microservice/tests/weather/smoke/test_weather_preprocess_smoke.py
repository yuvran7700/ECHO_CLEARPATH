# tests/smoke/test_weather_preprocess_smoke.py

import requests


def test_weather_preprocessed_is_alive(weather_preprocessed_url):
    """Smoke test: verify /weather/preprocessed is reachable in production"""
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    assert response.status_code < 500
