from src.lambda_handlers.raw_lambda_handler import (
    raw_lambda_handler,
)
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import (
    delete_file,
)

from tests.utils.weather_collect_utils import generate_trig_event


def test_raw_works():
    key = "weather_raw/12-3999.csv"
    date = "12-3999"

    delete_file(key)
    delete_record(date)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-old",
        key,
        "ckfajs;kf",
    )

    raw_lambda_handler(event, None)

    delete_file(key)
    delete_record(date)
