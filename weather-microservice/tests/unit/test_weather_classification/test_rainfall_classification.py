from src.utils.weather_utils import rainfall_classification


def test_no():
    assert rainfall_classification(0.0) == "No rain"


def test_light():
    assert rainfall_classification(6.1) == "Light rain"


def test_mod():
    assert rainfall_classification(15.1) == "Moderate rain"


def test_heavy():
    assert rainfall_classification(27.3) == "Heavy rain"


def test_na():
    assert rainfall_classification("Unavailable") == "N/A"
