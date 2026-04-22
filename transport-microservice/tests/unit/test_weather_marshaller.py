# tests/unit/test_weather_marshaller.py
from src.marshallers.weather_marshaller import extract_daily_weather

MOCK_RESPONSE = {
    "daily": {
        "time": [
            "2026-04-21",
            "2026-04-22",
            "2026-04-23",
            "2026-04-24",
            "2026-04-25",
            "2026-04-26",
            "2026-04-27",
        ],
        "temperature_2m_max": [21.2, 21.6, 22.1, 23.0, 23.4, 24.9, 22.6],
        "temperature_2m_min": [13.1, 13.5, 12.5, 13.6, 12.8, 9.8, 11.4],
        "precipitation_sum": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "windspeed_10m_max": [17.2, 14.6, 11.8, 10.5, 8.2, 7.4, 14.8],
    }
}


def test_returns_5_days_from_7_day_payload():
    result = extract_daily_weather(MOCK_RESPONSE)
    assert len(result) == 5


def test_dates_are_correct():
    result = extract_daily_weather(MOCK_RESPONSE)
    assert result[0]["date"] == "2026-04-21"
    assert result[4]["date"] == "2026-04-25"


def test_dropped_fields_are_absent():
    result = extract_daily_weather(MOCK_RESPONSE)
    for day in result:
        assert "humiditySeverity" not in day
        assert "sunSeverity" not in day
        assert "weather_summary" not in day


def test_severities_are_strings():
    result = extract_daily_weather(MOCK_RESPONSE)
    for day in result:
        assert isinstance(day["tempSeverity"], str)
        assert isinstance(day["rainSeverity"], str)
        assert isinstance(day["windSeverity"], str)


def test_empty_daily_returns_empty_list():
    result = extract_daily_weather(
        {
            "daily": {
                "time": [],
                "temperature_2m_max": [],
                "temperature_2m_min": [],
                "precipitation_sum": [],
                "windspeed_10m_max": [],
            }
        }
    )
    assert result == []
