from src.utils.weather_utils import sunshine_classification


def test_cloudy():
    assert sunshine_classification(2) == "Cloudy"


def test_part_cloudy():
    assert sunshine_classification(6) == "Partly Cloudy"


def test_sunny():
    assert sunshine_classification(9) == "Sunny"


def test_na():
    assert sunshine_classification("Unavailable") == "N/A"
