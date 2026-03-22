import json
from pathlib import Path

from src.lambda_handlers.ADAGE_lambda_handler import ADAGE_lambda_handler
from src.lambda_handlers.raw_lambda_handler import raw_lambda_handler
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import (
    delete_file,
    write_file_csv,
)

from tests.utils.weather_collect_utils import (
    generate_trig_event,
    generate_weather_query,
)


def test_ADAGE_missing_atri_correct():
    key = "weather_raw/12-2999.csv"
    date = "12-2999"

    delete_file(key)
    delete_record(date)

    file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "12-2999.csv"
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

    date = "2999-12-12"
    event = generate_weather_query(date)

    result = ADAGE_lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert result["headers"] is not None
    assert result["body"] is not None
    body = json.loads(result["body"])
    assert body["events"][0]["event_attributes"]["tempMin_C"] == "Unavailable"
