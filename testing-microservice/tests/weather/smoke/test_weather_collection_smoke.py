# tests/smoke/test_weather_collection_smoke.py

import requests


def test_weather_collection_is_alive(weather_collection_url):
    """Smoke test: verify /weather/collection is reachable in production"""
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )
    assert response.status_code < 500
