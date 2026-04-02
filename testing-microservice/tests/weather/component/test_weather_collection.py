# tests/weather/component/test_weather_collection.py
import requests


# ─── 200 SUCCESS ─────────────────────────────────────────────────────────
def test_weather_collection_returns_200(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )
    assert response.status_code == 200


def test_weather_collection_has_body(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )
    body = response.json()
    assert body is not None
    assert len(body) > 0


def test_weather_collection_has_events(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )
    body = response.json()
    assert "events" in body
    assert isinstance(body["events"], list)


def test_weather_collection_has_correct_type(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )
    assert response.headers["Content-Type"] == "application/json"


def test_weather_collection_body_check(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2026-03-18"}
    )
    body = response.json()
    attri = body["events"][0]["event_attributes"]
    assert "date" in attri
    assert attri["date"] == "2026-03-18"
    assert "rainfall_mm" in attri
    assert "maxWindTime" in attri


# ─── MISSING PARAMETERS ──────────────────────────────────────────────────
def test_weather_collection_missing_date(weather_collection_url):
    response = requests.get(weather_collection_url)
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Missing date parameter"


# ─── INVALID DATE QUERY ──────────────────────────────────────────────────
def test_weather_collection_incorrect_date_format(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2025/12/12"}
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Invalid date format - Expected YYYY-MM-DD"


def test_weather_collection_date_letters(weather_collection_url):
    response = requests.get(weather_collection_url, params={"date": "abc"})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Invalid date format - Expected YYYY-MM-DD"


# ─── RECORD MISSING ──────────────────────────────────────────────────
def test_weather_collection_record_missing(weather_collection_url):
    response = requests.get(
        weather_collection_url, params={"date": "2001-12-12"}
    )
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "Record not found"
