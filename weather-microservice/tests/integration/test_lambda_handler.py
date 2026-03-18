import json
import logging

from src.lambda_handlers.collection_lambda_handler import (
    collected_lambda_handler,
)
from src.lambda_handlers.weather_lambda_handler import weather_lambda_handler
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import delete_file, write_file
from tests.utils.weather_collect_utils import generate_trig_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def good_test():
    print("hi")

    key = "weather_collected/3999-12-12.json"
    delete_file(key)
    delete_record("3999-12-12")
    with open("tests/3999-12-12.json", "r") as f:
        content = json.load(f)

    write_file(key, content)
    delete_file("weather_collected/6999-12-12.json")

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index",
        key,
        "ckfajs;kf",
    )

    weather_event = {"queryStringParameters": {"date": "3999-12-12"}}

    print("hi", flush=True)
    collected_lambda_handler(event, None)

    result = weather_lambda_handler(weather_event, None)
    logger.info("weather result: %s", result)


def bad_test():
    with open("tests/test_bad_event.json", "r") as f:
        event = json.load(f)

    print(collected_lambda_handler(event, None))


def eTag_test():
    with open("tests/test_eTag_event.json", "r") as f:
        event = json.load(f)

    print(collected_lambda_handler(event, None))


if __name__ == "__main__":
    good_test()
