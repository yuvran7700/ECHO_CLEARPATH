from src.lambda_handlers.collection_lambda_handler import (
    collection_lambda_handler,
)
from src.repositories.db_repo import delete_record, get_record
from src.repositories.s3_repo import (
    delete_file,
)

from tests.utils.weather_collect_utils import generate_trig_event


def test_key_missing():
    key = "weather_collected/9999-12-12.json"
    date = "9999-12-12"

    delete_file(key)
    delete_record(date)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index",
        None,
        "ckfajs;kf",
    )

    collection_lambda_handler(event, None)

    result = get_record(date)
    assert result is None

    delete_file(key)
    delete_record(date)
