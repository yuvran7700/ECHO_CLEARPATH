# tests/weather/component/test_weather_preprocessed.py
import requests


def test_weather_preprocessed_returns_200(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    assert response.status_code == 200


def test_weather_preprocessed_missing_date(weather_preprocessed_url):
    response = requests.get(weather_preprocessed_url)
    assert response.status_code == 400
