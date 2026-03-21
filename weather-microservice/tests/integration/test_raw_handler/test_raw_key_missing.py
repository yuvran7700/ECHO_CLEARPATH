from src.lambda_handlers.raw_lambda_handler import (
    raw_lambda_handler,
)
from src.repositories.s3_repo import delete_file, read_file

from tests.utils.weather_collect_utils import generate_trig_event


def test_raw_key_missing():
    key = "weather_raw/12-9999.csv"

    delete_file(key)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-old",
        key,
        "ckfajs;kf",
    )

    raw_lambda_handler(event, None)

    retrieve_key = "weather_collected/3999-12-12.json"

    result = read_file(retrieve_key)
    assert result is None
