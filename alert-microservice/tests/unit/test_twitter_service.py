# tests/test_twitter_service.py
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.services.twitter_service import (
    add_tweets_to_dynamoDB,
    fetch_tweets,
    generate_weekly_queries,
    process_tweets_and_return_to_user,
    process_tweets_and_upload_to_dynamodb,
)

BASE_QUERY = (
    "(from:T1SydneyTrains) "
    "(delay OR disruption OR cancelled OR suspended "
    "OR delayed OR allow extra time)"
)


def test_weekly_queries_generation():
    """
    Test weekly query generation creates correct weekly date windows.
    """
    start = datetime.strptime("2026-02-01", "%Y-%m-%d")
    end = datetime.strptime("2026-02-20", "%Y-%m-%d")

    queries = generate_weekly_queries(BASE_QUERY, start, end)

    assert len(queries) == 3
    assert f"{BASE_QUERY} since:2026-02-01 until:2026-02-08" == queries[0]
    assert f"{BASE_QUERY} since:2026-02-08 until:2026-02-15" == queries[1]
    assert f"{BASE_QUERY} since:2026-02-15 until:2026-02-20" == queries[2]


@patch("src.services.twitter_service.TwitterClient")
@patch("src.services.twitter_service.generate_weekly_queries")
@patch("src.services.twitter_service.time.sleep")
def test_fetch_calls_api_for_each_query(mock_sleep, mock_queries, mock_client):
    """
    Test fetch_tweets calls the Twitter API for each generated query.
    """
    mock_queries.return_value = ["q1", "q2"]

    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.fetch_tweets_by_query.return_value = []

    fetch_tweets(
        base_query=BASE_QUERY,
        start_date="2026-02-01",
        end_date="2026-02-20",
    )

    assert mock_instance.fetch_tweets_by_query.call_count == 2


@patch("src.services.twitter_service.TwitterClient")
@patch("src.services.twitter_service.generate_weekly_queries")
@patch("src.services.twitter_service.time.sleep")
def test_fetch_tweets_removes_all_duplicate_tweets(
    mock_sleep, mock_queries, mock_client, sample_tweet_raw_response
):
    """
    Test fetch_tweets returns only unique tweets.
    """
    mock_queries.return_value = ["q1", "q2"]

    mock_instance = MagicMock()
    mock_client.return_value = mock_instance

    tweet = sample_tweet_raw_response

    mock_instance.fetch_tweets_by_query.side_effect = [
        [tweet],
        [tweet],
    ]

    result = fetch_tweets(
        base_query=BASE_QUERY,
        start_date="2026-02-01",
        end_date="2026-02-20",
    )

    assert len(result) == 1


@patch("src.services.twitter_service.put_record")
def test_add_tweets_to_db_creates_correct_item(
    mock_put,
    sample_parsed_tweet,
):
    """
    Test add_tweets_to_dynamoDB uploads the correct item structure.
    """
    add_tweets_to_dynamoDB(sample_parsed_tweet)

    mock_put.assert_called_once_with(
        {
            "date": "2026-02-02",
            "account_name": "T1 Sydney Trains",
            "text": sample_parsed_tweet[0]["master_text"],
            "status": ["collected"],
        }
    )


@patch("src.services.twitter_service.TwitterClient")
@patch("src.services.twitter_service.generate_weekly_queries")
@patch("src.services.twitter_service.time.sleep")
def test_fetch_uses_timeframe_queries(mock_sleep, mock_queries, mock_client):
    """
    Test fetch_tweets uses each generated timeframe query.
    """
    queries = [
        "query since:2026-02-01 until:2026-02-08",
        "query since:2026-02-08 until:2026-02-15",
    ]
    mock_queries.return_value = queries

    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.fetch_tweets_by_query.return_value = []

    fetch_tweets(
        base_query=BASE_QUERY,
        start_date="2026-02-01",
        end_date="2026-02-15",
    )

    mock_instance.fetch_tweets_by_query.assert_any_call(queries[0])
    mock_instance.fetch_tweets_by_query.assert_any_call(queries[1])


@patch("src.services.twitter_service.fetch_tweets")
@patch("src.services.twitter_service.parse_tweets")
@patch("src.services.twitter_service.add_tweets_to_dynamoDB")
def test_process_pipeline_with_realistic_data(
    mock_add,
    mock_parse,
    mock_fetch,
    sample_tweet_raw_response,
    sample_parsed_tweet,
):
    """
    Test the full service pipeline from fetch to parse to DB upload.
    """
    mock_fetch.return_value = [sample_tweet_raw_response]
    mock_parse.return_value = sample_parsed_tweet

    process_tweets_and_upload_to_dynamodb()

    mock_fetch.assert_called_once_with(
        BASE_QUERY,
        "2026-02-01",
        "2026-03-18",
    )
    mock_parse.assert_called_once_with([sample_tweet_raw_response])
    mock_add.assert_called_once_with(sample_parsed_tweet)


@patch("src.services.twitter_service.marshal_tweets_to_adage")
@patch("src.services.twitter_service.fetch_and_format_tweets")
def test_process_tweets_and_return_to_user_calls_dependencies_correctly(
    mock_fetch_and_format,
    mock_marshal,
    sample_parsed_tweet,
):
    """
    Test that the service fetches formatted tweets and passes them
    to the ADAGE marshaller with the correct arguments.
    """
    base_query = "(from:T1SydneyTrains) (delay OR disruption)"
    start_date = "2026-02-01"
    end_date = "2026-02-20"

    expected_adage_payload = {
        "data_source": "Twitter",
        "dataset_type": "Historical Tweets",
        "dataset_id": "test-id",
        "time_object": {
            "timestamp": "2026-03-24 12:00:00",
            "timezone": "UTC",
        },
        "events": [],
    }

    mock_fetch_and_format.return_value = sample_parsed_tweet
    mock_marshal.return_value = expected_adage_payload

    result = process_tweets_and_return_to_user(
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )

    mock_fetch_and_format.assert_called_once_with(
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )

    mock_marshal.assert_called_once_with(
        tweets=sample_parsed_tweet,
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )

    assert result == expected_adage_payload
