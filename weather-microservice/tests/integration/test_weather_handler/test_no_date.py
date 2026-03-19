from src.lambda_handlers.weather_lambda_handler import (
    weather_lambda_handler,
)
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import (
    delete_file,
)

from tests.utils.weather_collect_utils import generate_weather_query


def test_new_record_works():
    key = "weather_collected/3999-12-12.json"
    date = "3999-12-12"

    delete_file(key)
    delete_record(date)

    event = generate_weather_query(None)

    result = weather_lambda_handler(event, None)

    assert result["statusCode"] == 400
    assert result["body"] is not None
    assert result["body"] == '{"error": "Missing date parameter"}'
