from src.utils.weather_utils import humidity_classification


def test_low():
    assert humidity_classification(25, 22) == "Low Humidity"


def test_mod():
    assert humidity_classification(40, 32) == "Moderate Humidity"


def test_high():
    assert humidity_classification(64, 76) == "High Humidity"


def test_extreme():
    assert humidity_classification(84, 91) == "Extreme Humidity"


def test_am_miss():
    assert humidity_classification("Unavailable", 12) == "Low Humidity"


def test_pm_miss():
    assert humidity_classification(12, "Unavailable") == "Low Humidity"


def test_both_miss():
    assert humidity_classification("Unavailable", "Unavailable") == "N/A"
