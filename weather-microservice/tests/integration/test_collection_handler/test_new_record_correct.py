import json
from pathlib import Path

from src.lambda_handlers.collection_lambda_handler import (
    collection_lambda_handler,
)
from src.repositories.db_repo import delete_record, get_record
from src.repositories.s3_repo import (
    delete_file,
    write_file,
)
from src.utils.weather_utils import decimal_converter

from tests.utils.weather_collect_utils import generate_trig_event


def test_new_record_works():
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

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index",
        key,
        "ckfajs;kf",
    )

    collection_lambda_handler(event, None)

    result = get_record(date)
    attri = content["events"][0]["event_attributes"]
    assert result["date"] == date
    assert result["rainfall"] == attri["rainfall"]
    assert decimal_converter(result["tempMin"]) == attri["tempMin"]
    assert decimal_converter(result["tempMax"]) == attri["tempMax"]
    assert decimal_converter(result["sunshineHours"]) == attri["sunshineHours"]
    assert decimal_converter(result["windGustSpeed"]) == attri["windGustSpeed"]
    assert result["9am"] is not None
    assert decimal_converter(result["9am"]["temp"]) == attri["9am"]["temp"]
    assert (
        decimal_converter(result["9am"]["humidity"])
        == attri["9am"]["humidity"]
    )
    assert result["3pm"] is not None
    assert decimal_converter(result["3pm"]["temp"]) == attri["3pm"]["temp"]
    assert (
        decimal_converter(result["3pm"]["humidity"])
        == attri["3pm"]["humidity"]
    )

    assert result["weatherSeverity"] is not None
    assert result["weatherSeverity"]["rainSeverity"] == "No rain"
    assert result["weatherSeverity"]["tempSeverity"] == "Warm"
    assert result["weatherSeverity"]["sunSeverity"] == "Sunny"
    assert result["weatherSeverity"]["windSeverity"] == "Breezy"

    delete_file(key)
    delete_record(date)
