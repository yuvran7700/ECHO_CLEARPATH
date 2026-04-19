import json
from pathlib import Path

from src.lambda_handlers.collection_lambda_handler import (
    collection_lambda_handler,
)
from src.lambda_handlers.weather_lambda_handler import (
    weather_lambda_handler,
)
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import (
    delete_file,
    write_file,
)

from tests.utils.weather_collect_utils import (
    generate_trig_event,
    generate_weather_query,
)


def test_missing_atri_correct():
    key = "weather_collected/5999-12-12.json"
    date = "5999-12-12"

    delete_file(key)
    delete_record(date)

    file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "5999-12-12.json"
    )

    with open(file_path, "r") as f:
        content = json.load(f)

    write_file(key, content)

    event = generate_trig_event(
        "ObjectCreated:Put",
        "clearpath-weather-index-v1",
        key,
        "ckfajs;kf",
    )

    collection_lambda_handler(event, None)

    event = generate_weather_query(date)

    result = weather_lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert result["headers"] is not None
    assert result["body"] is not None
    body = json.loads(result["body"])
    assert (
        body["events"][0]["event_attributes"]["weatherSeverity"][
            "windSeverity"
        ]
        == "N/A"
    )
