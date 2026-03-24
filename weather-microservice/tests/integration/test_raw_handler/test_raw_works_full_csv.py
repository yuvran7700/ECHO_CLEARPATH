from pathlib import Path

from src.lambda_handlers.raw_lambda_handler import (
    raw_lambda_handler,
)
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import delete_file, read_file, write_file_csv

from tests.utils.weather_collect_utils import generate_trig_event


def test_raw_works_full_csv():
    key = "weather_raw/12-4999.csv"
    date = "12-4999"

    delete_file(key)
    delete_record(date)
    delete_file("weather_collected/4999-12-01.json")

    file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "12-4999.csv"
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

    result = raw_lambda_handler(event, None)

    retrieve_key = "weather_collected/4999-12-01.json"

    result = read_file(retrieve_key)

    assert result is not None

    attri = result["events"][0]["event_attributes"]
    assert attri["date"] == "4999-12-01"
    assert attri["rainfall_mm"] == 0
    assert attri["tempMin_C"] == 15.0
    assert attri["tempMax_C"] == 24.6
    assert attri["9am"] is not None
    assert attri["9am"]["temp_C"] == 20.7
    assert attri["3pm"] is not None
    assert attri["3pm"]["temp_C"] == 22.8
