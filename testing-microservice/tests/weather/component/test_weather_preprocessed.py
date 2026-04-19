# tests/weather/component/test_weather_preprocessed.py
import requests


# ─── 200 SUCCESS ─────────────────────────────────────────────────────────
def test_weather_preprocessed_returns_200(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    assert response.status_code == 200


def test_weather_preprocessed_has_body(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    body = response.json()
    assert body is not None
    assert len(body) > 0


def test_weather_preprocessed_has_events(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    body = response.json()
    assert "events" in body
    assert isinstance(body["events"], list)


def test_weather_preprocessed_has_correct_type(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    assert response.headers["Content-Type"] == "application/json"


def test_weather_preprocessed_body_check(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2026-03-18"}
    )
    body = response.json()
    attri = body["events"][0]["event_attributes"]
    assert "date" in attri
    assert attri["date"] == "2026-03-18"
    assert "rainfall_mm" in attri
    assert "weatherSeverity" in attri


# ─── MISSING PARAMETERS ──────────────────────────────────────────────────
def test_weather_preprocessed_missing_date(weather_preprocessed_url):
    response = requests.get(weather_preprocessed_url)
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Missing date parameter"


# ─── INVALID DATE QUERY ──────────────────────────────────────────────────
def test_weather_preprocessed_incorrect_date_format(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2025/12/12"}
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Invalid date format - Expected YYYY-MM-DD"


def test_weather_preprocessed_date_letters(weather_preprocessed_url):
    response = requests.get(weather_preprocessed_url, params={"date": "abc"})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Invalid date format - Expected YYYY-MM-DD"


# ─── RECORD MISSING ──────────────────────────────────────────────────
def test_weather_preprocessed_record_missing(weather_preprocessed_url):
    response = requests.get(
        weather_preprocessed_url, params={"date": "2001-12-12"}
    )
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "Record not found"
