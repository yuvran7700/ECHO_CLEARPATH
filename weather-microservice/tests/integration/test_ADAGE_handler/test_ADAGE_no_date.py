from src.lambda_handlers.ADAGE_lambda_handler import ADAGE_lambda_handler
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import (
    delete_file,
)

from tests.utils.weather_collect_utils import generate_weather_query


def test_ADAGE_no_date():
    key = "weather_collected/3999-12-12.json"
    date = "3999-12-12"

    delete_file(key)
    delete_record(date)

    event = generate_weather_query(None)

    result = ADAGE_lambda_handler(event, None)

    assert result["statusCode"] == 400
    assert result["body"] is not None
    assert result["body"] == '{"error": "Missing date parameter"}'
