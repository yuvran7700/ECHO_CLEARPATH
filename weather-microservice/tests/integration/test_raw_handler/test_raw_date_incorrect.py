from pathlib import Path

import pytest
from src.lambda_handlers.raw_lambda_handler import (
    raw_lambda_handler,
)
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import delete_file, read_file, write_file_csv

from tests.utils.weather_collect_utils import generate_trig_event


def test_raw_date_incorrect():
    key = "weather_raw/12-3999.csv"
    date = "12-3999"

    delete_file(key)
    delete_file("weather_collected/3999-12-12.json")
    delete_record(date)

    file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "12-3999-no-date.csv"
    )

    with open(file_path, "r", encoding="utf-8-sig") as f:
        csv_content = f.read()

    write_file_csv(key, csv_content)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index-v1",
        key,
        "ckfajs;kf",
    )

    raw_lambda_handler(event, None)

    retrieve_key = "weather_collected/3999-12-12.json"

    with pytest.raises(Exception):
        read_file(retrieve_key)
