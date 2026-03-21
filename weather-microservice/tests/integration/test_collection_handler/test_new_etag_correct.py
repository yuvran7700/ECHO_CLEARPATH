import json
from pathlib import Path

from src.lambda_handlers.collection_lambda_handler import (
    collection_lambda_handler,
)
from src.repositories.db_repo import delete_record, get_record
from src.repositories.s3_repo import delete_file, get_etag, write_file

from tests.utils.weather_collect_utils import generate_trig_event


def test_new_etag_correct():
    key = "weather_collected/3999-12-12.json"
    date = "3999-12-12"

    delete_file(key)
    delete_record(date)

    file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "3999-12-12.json"
    )

    with open(file_path, "r") as f:
        content = json.load(f)

    write_file(key, content)

    etag1 = get_etag(key)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index",
        key,
        etag1,
    )

    collection_lambda_handler(event, None)

    result1 = get_record(date)
    assert result1 is not None
    assert result1["eTag"] == etag1

    file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "3999-12-12-altered.json"
    )

    with open(file_path, "r") as f:
        content = json.load(f)

    write_file(key, content)

    etag2 = get_etag(key)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index",
        key,
        etag2,
    )

    collection_lambda_handler(event, None)

    result1 = get_record(date)
    assert result1 is not None
    assert result1["eTag"] == etag2

    delete_file(key)
    delete_record(date)
