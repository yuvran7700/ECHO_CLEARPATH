# tests/unit/test_classifiers.py
from src.utils.classifiers import (
    classify_humidity,
    classify_rainfall,
    classify_sun_from_condition,
    classify_temperature,
    classify_wind,
)


class TestClassifyTemperature:
    def test_cold_when_avg_below_15(self):
        assert classify_temperature(10, 5) == "Cold"  # avg 7.5

    def test_mild_when_avg_between_15_and_22(self):
        assert classify_temperature(20, 16) == "Mild"  # avg 18

    def test_warm_when_avg_between_22_and_30(self):
        assert classify_temperature(28, 22) == "Warm"  # avg 25

    def test_hot_when_avg_above_30(self):
        assert classify_temperature(38, 32) == "Hot"  # avg 35

    def test_boundary_exactly_15_is_mild(self):
        assert classify_temperature(20, 10) == "Mild"  # avg 15

    def test_boundary_exactly_22_is_warm(self):
        assert classify_temperature(24, 20) == "Warm"  # avg 22

    def test_boundary_exactly_30_is_hot(self):
        assert classify_temperature(32, 28) == "Hot"  # avg 30


class TestClassifyRainfall:
    def test_no_rain_when_zero(self):
        assert classify_rainfall(0.0) == "No rain"

    def test_light_rain_when_below_10(self):
        assert classify_rainfall(5.0) == "Light rain"

    def test_moderate_rain_when_between_10_and_25(self):
        assert classify_rainfall(15.0) == "Moderate rain"

    def test_heavy_rain_when_above_25(self):
        assert classify_rainfall(30.0) == "Heavy rain"

    def test_boundary_exactly_10_is_moderate(self):
        assert classify_rainfall(10.0) == "Moderate rain"

    def test_boundary_exactly_25_is_heavy(self):
        assert classify_rainfall(25.0) == "Heavy rain"


class TestClassifyWind:
    def test_calm_when_below_20(self):
        assert classify_wind(10) == "Calm"

    def test_breezy_when_between_20_and_38(self):
        assert classify_wind(25) == "Breezy"

    def test_windy_when_between_38_and_61(self):
        assert classify_wind(50) == "Windy"

    def test_gale_when_above_61(self):
        assert classify_wind(70) == "Gale"

    def test_boundary_exactly_20_is_breezy(self):
        assert classify_wind(20) == "Breezy"

    def test_boundary_exactly_38_is_windy(self):
        assert classify_wind(38) == "Windy"

    def test_boundary_exactly_61_is_gale(self):
        assert classify_wind(61) == "Gale"


class TestClassifyHumidity:
    def test_low_humidity_when_at_or_below_30(self):
        assert classify_humidity(30) == "Low Humidity"

    def test_moderate_humidity_when_between_30_and_60(self):
        assert classify_humidity(45) == "Moderate Humidity"

    def test_high_humidity_when_between_60_and_80(self):
        assert classify_humidity(70) == "High Humidity"

    def test_extreme_humidity_when_above_80(self):
        assert classify_humidity(90) == "Extreme Humidity"

    def test_boundary_exactly_60_is_moderate(self):
        assert classify_humidity(60) == "Moderate Humidity"

    def test_boundary_exactly_80_is_high(self):
        assert classify_humidity(80) == "High Humidity"


class TestClassifySunFromCondition:
    def test_partly_cloudy_when_partly_in_condition(self):
        assert classify_sun_from_condition("Partly sunny") == "Partly Cloudy"

    def test_partly_cloudy_when_partly_cloudy(self):
        assert classify_sun_from_condition("Partly cloudy") == "Partly Cloudy"

    def test_cloudy_when_cloud_in_condition(self):
        assert classify_sun_from_condition("Cloudy") == "Cloudy"

    def test_cloudy_when_rain_in_condition(self):
        assert classify_sun_from_condition("Light rain") == "Cloudy"

    def test_cloudy_when_drizzle_in_condition(self):
        assert classify_sun_from_condition("Drizzle") == "Cloudy"

    def test_sunny_when_clear(self):
        assert classify_sun_from_condition("Clear") == "Sunny"

    def test_sunny_when_sunny(self):
        assert classify_sun_from_condition("Sunny") == "Sunny"

    def test_case_insensitive(self):
        assert classify_sun_from_condition("PARTLY SUNNY") == "Partly Cloudy"
