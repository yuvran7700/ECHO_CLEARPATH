import pytest
from src.lambda_handlers.raw_lambda_handler import (
    raw_lambda_handler,
)
from src.repositories.s3_repo import delete_file, read_file

from tests.utils.weather_collect_utils import generate_trig_event


def test_incorrect_event_type():
    key = "weather_raw/12-3999.csv"

    delete_file(key)
    delete_file("weather_collected/3999-12-12.json")

    event = generate_trig_event(
        "s3:ObjectRemoved:Delete",
        "clearpath-weather-index-v1",
        key,
        "ckfajs;kf",
    )

    raw_lambda_handler(event, None)

    retrieve_key = "weather_collected/3999-12-12.json"

    with pytest.raises(Exception):
        read_file(retrieve_key)
