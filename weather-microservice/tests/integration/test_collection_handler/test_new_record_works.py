import json
import logging

from src.lambda_handlers.collection_lambda_handler import (
    collected_lambda_handler,
)
from src.repositories.db_repo import delete_record, get_record
from src.repositories.s3_repo import delete_file, write_file

from tests.utils.weather_collect_utils import generate_trig_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_new_record_works():
    key = "weather_collected/3999-12-12.json"
    date = "3999-12-12"

    delete_file(key)
    delete_record(date)
    with open("weather-microservice/tests/3999-12-12.json", "r") as f:
        content = json.load(f)

    print(content)

    write_file(key, content)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index",
        key,
        "ckfajs;kf",
    )

    collected_lambda_handler(event, None)

    result = get_record(date)

    assert result["date"] == date
