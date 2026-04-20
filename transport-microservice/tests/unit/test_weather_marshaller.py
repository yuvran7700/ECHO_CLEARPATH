# tests/unit/test_weather_marshaller.py
from src.marshallers.weather_marshaller import (
    classify_forecast_day,
    extract_daily_weather,
    extract_day_metrics,
)


class TestExtractDayMetrics:
    def test_extracts_max_temp(self, forecast_day_factory):
        day = forecast_day_factory(max_temp=30.0)
        assert extract_day_metrics(day)["max_temp"] == 30.0

    def test_extracts_min_temp(self, forecast_day_factory):
        day = forecast_day_factory(min_temp=10.0)
        assert extract_day_metrics(day)["min_temp"] == 10.0

    def test_sums_daytime_and_nighttime_rainfall(self, forecast_day_factory):
        day = forecast_day_factory(day_rainfall=3.0, night_rainfall=2.0)
        assert extract_day_metrics(day)["rainfall_mm"] == 5.0

    def test_takes_max_wind_gust(self, forecast_day_factory):
        day = forecast_day_factory(day_gust=40.0, night_gust=25.0)
        assert extract_day_metrics(day)["max_wind"] == 40.0

    def test_takes_max_wind_gust_when_night_higher(self, forecast_day_factory):
        day = forecast_day_factory(day_gust=25.0, night_gust=50.0)
        assert extract_day_metrics(day)["max_wind"] == 50.0

    def test_averages_humidity(self, forecast_day_factory):
        day = forecast_day_factory(day_humidity=60, night_humidity=80)
        assert extract_day_metrics(day)["avg_humidity"] == 70.0

    def test_extracts_weather_condition(self, forecast_day_factory):
        day = forecast_day_factory(weather_condition="Light rain")
        assert extract_day_metrics(day)["weather_condition"] == "Light rain"


class TestClassifyForecastDay:
    def test_returns_all_severity_keys(self, sunny_mild_day):
        result = classify_forecast_day(sunny_mild_day)
        assert "tempSeverity" in result
        assert "rainSeverity" in result
        assert "windSeverity" in result
        assert "humiditySeverity" in result
        assert "sunSeverity" in result

    def test_sunny_mild_day_classifications(self, sunny_mild_day):
        result = classify_forecast_day(sunny_mild_day)
        assert result["tempSeverity"] == "Mild"
        assert result["rainSeverity"] == "No rain"
        assert result["sunSeverity"] == "Sunny"

    def test_cold_heavy_rain_day_classifications(self, cold_heavy_rain_day):
        result = classify_forecast_day(cold_heavy_rain_day)
        assert result["tempSeverity"] == "Cold"
        assert result["rainSeverity"] == "Heavy rain"
        assert result["windSeverity"] == "Gale"
        assert result["humiditySeverity"] == "Extreme Humidity"
        assert result["sunSeverity"] == "Cloudy"

    def test_hot_dry_day_classifications(self, hot_dry_day):
        result = classify_forecast_day(hot_dry_day)
        assert result["tempSeverity"] == "Hot"
        assert result["rainSeverity"] == "No rain"
        assert result["humiditySeverity"] == "Low Humidity"


class TestExtractDailyWeather:
    def test_returns_empty_list_for_no_forecast_days(self):
        assert extract_daily_weather({}) == []

    def test_returns_correct_number_of_days(self, five_day_forecast_response):
        assert len(extract_daily_weather(five_day_forecast_response)) == 5

    def test_formats_date_correctly(self, forecast_day_factory):
        response = {
            "forecastDays": [forecast_day_factory(year=2026, month=4, day=5)]
        }
        assert extract_daily_weather(response)[0]["date"] == "2026-04-05"

    def test_includes_weather_summary(self, forecast_day_factory):
        response = {
            "forecastDays": [forecast_day_factory(weather_condition="Sunny")]
        }
        assert extract_daily_weather(response)[0]["weather_summary"] == "Sunny"

    def test_includes_all_severity_fields(self, five_day_forecast_response):
        result = extract_daily_weather(five_day_forecast_response)
        for day in result:
            assert "tempSeverity" in day
            assert "rainSeverity" in day
            assert "windSeverity" in day
            assert "humiditySeverity" in day
            assert "sunSeverity" in day
