# tests/integration/test_user_tweet_collection.py
from unittest.mock import patch

from src.services.twitter_service import process_tweets_and_return_to_user


@patch("src.services.twitter_service.fetch_tweets")
def test_process_tweets_and_return_to_user_returns_adage_payload(
    mock_fetch_tweets,
    sample_tweet_raw_response,
):
    """
    Test the service pipeline from raw tweet fetch to ADAGE payload output.
    """
    base_query = "(from:T1SydneyTrains) (delay OR disruption)"
    start_date = "2026-02-01"
    end_date = "2026-02-20"

    mock_fetch_tweets.return_value = [sample_tweet_raw_response]

    result = process_tweets_and_return_to_user(
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )

    assert isinstance(result, dict)

    assert result["data_source"] == "Twitter"
    assert result["dataset_type"] == "Historical Tweets"
    assert "dataset_id" in result
    assert "time_object" in result
    assert "events" in result

    assert isinstance(result["events"], list)
    assert len(result["events"]) == 1

    event = result["events"][0]

    assert event["event_type"] == "transport disruption tweet"
    assert event["time_object"]["timestamp"] == "2026-02-02"
    assert event["time_object"]["timezone"] == "UTC"

    assert event["attribute"]["account_name"] == "T1 Sydney Trains"
    assert event["attribute"]["text"] == sample_tweet_raw_response["text"]
    assert event["attribute"]["date"] == "2026-02-02"
