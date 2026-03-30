import json
from pathlib import Path

from src.lambda_handlers.collection_lambda_handler import (
    collection_lambda_handler,
)
from src.repositories.db_repo import delete_record, get_record, put_record
from src.repositories.s3_repo import delete_file, write_file
from src.utils.weather_utils import decimal_converter

from tests.utils.weather_collect_utils import generate_trig_event


def test_no_db_etag_correct():
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

    put_record({"date": date, "tempMin_C": 3})

    write_file(key, content)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index-v1",
        key,
        "ckfajs;kf",
    )

    collection_lambda_handler(event, None)

    result = get_record(date)
    attri = content["events"][0]["event_attributes"]

    assert result["date"] == date
    assert result["eTag"] == "ckfajs;kf"
    assert (
        result["s3URL"]
        == f"s3://clearpath-weather-index-v1/weather_collected/{date}.json"
    )

    assert decimal_converter(result["rainfall_mm"]) == attri["rainfall_mm"]
    assert decimal_converter(result["tempMin_C"]) == attri["tempMin_C"]
    assert decimal_converter(result["tempMax_C"]) == attri["tempMax_C"]
    assert (
        decimal_converter(result["sunshineHours_hours"])
        == attri["sunshineHours_hours"]
    )
    assert (
        decimal_converter(result["maxWindSpeed_kmh"])
        == attri["maxWindSpeed_kmh"]
    )

    # Flattened 9am fields
    assert decimal_converter(result["9am_temp_C"]) == attri["9am"]["temp_C"]
    assert (
        decimal_converter(result["9am_humidity_percent"])
        == attri["9am"]["humidity_percent"]
    )

    # Flattened 3pm fields
    assert decimal_converter(result["3pm_temp_C"]) == attri["3pm"]["temp_C"]
    assert (
        decimal_converter(result["3pm_humidity_percent"])
        == attri["3pm"]["humidity_percent"]
    )

    # Flattened severity fields
    assert result["rainSeverity"] == "No rain"
    assert result["tempSeverity"] == "Mild"
    assert result["windSeverity"] == "Gale"
    assert result["sunSeverity"] is not None
    assert result["humiditySeverity"] is not None

    delete_file(key)
    delete_record(date)
