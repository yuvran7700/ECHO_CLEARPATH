from src.lambda_handlers.ADAGE_lambda_handler import ADAGE_lambda_handler
from src.repositories.db_repo import delete_record
from src.repositories.s3_repo import delete_file

from tests.utils.weather_collect_utils import generate_weather_query


def test_ADAGE_no_record():
    key = "weather_collected/1111-12-12.json"
    date = "1111-12-12"

    delete_file(key)
    delete_record(date)

    event = generate_weather_query(date)

    result = ADAGE_lambda_handler(event, None)

    assert result["statusCode"] == 404
    assert result["body"] is not None
    assert result["body"] == '{"error": "Record not found"}'
