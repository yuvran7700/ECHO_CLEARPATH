from src.utils.weather_utils import temperature_classification


def test_temp_cold():
    assert temperature_classification(10, 12, 11, 13) == "Cold"


def test_temp_mild():
    assert temperature_classification(15, 25, 18, 16) == "Mild"


def test_temp_warm():
    assert temperature_classification(25, 28, 21, 26) == "Warm"


def test_temp_hot():
    assert temperature_classification(28, 36, 30, 31) == "Hot"


def test_temp_na_all():
    assert (
        temperature_classification(
            "Unavailable", "Unavailable", "Unavailable", "Unavailable"
        )
        == "N/A"
    )


def test_temp_na_mild():
    assert temperature_classification(19, 21, "Unavailable", 20) == "Mild"


def test_temp_na_hot():
    assert (
        temperature_classification(
            "Unavailable", 34, "Unavailable", "Unavailable"
        )
        == "Hot"
    )
