from src.utils.weather_utils import wind_classification


def test_calm():
    assert wind_classification(18) == "Calm"


def test_breezy():
    assert wind_classification(25) == "Breezy"


def test_windy():
    assert wind_classification(50) == "Windy"


def test_gale():
    assert wind_classification(70) == "Gale"


def test_na():
    assert wind_classification("Unavailable") == "N/A"
