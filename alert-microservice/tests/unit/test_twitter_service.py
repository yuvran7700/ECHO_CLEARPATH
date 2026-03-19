# tests/test_twitter_service.py
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.services.twitter_service import (
    add_tweets_to_dynamoDB,
    fetch_tweets,
    generate_weekly_queries,
    procress_tweets_and_upload_to_dynamo_db,
)


def test_weekly_queries_generation():
    """
    tests weekly queries generations creates correct weeks
    from given start to end date
    """
    start = datetime.strptime("2026-02-01", "%Y-%m-%d")
    end = datetime.strptime("2026-02-20", "%Y-%m-%d")

    queries = generate_weekly_queries(start, end)

    assert len(queries) == 3
    assert "since:2026-02-01 until:2026-02-08" in queries[0]
    assert "since:2026-02-08 until:2026-02-15" in queries[1]
    assert "since:2026-02-15 until:2026-02-20" in queries[2]


@patch("src.services.twitter_service.TwitterClient")
@patch("src.services.twitter_service.generate_weekly_queries")
@patch("src.services.twitter_service.time.sleep")
def test_fetch_calls_api_for_each_query(mock_sleep, mock_queries, mock_client):
    """
    tests fetch_tweets is called for all generated queries
    """
    # Arrange
    mock_queries.return_value = ["q1", "q2"]

    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.fetch_tweets_by_query.return_value = []

    # Act
    fetch_tweets()

    # Assert
    assert mock_instance.fetch_tweets_by_query.call_count == 2


@patch("src.services.twitter_service.TwitterClient")
@patch("src.services.twitter_service.generate_weekly_queries")
@patch("src.services.twitter_service.time.sleep")
def test_fetch_tweets_removes_all_duplicate_tweets(
    mock_sleep, mock_queries, mock_client, sample_tweet_raw_response
):
    """
    tests fetch_tweets only returns unique tweets
    """
    mock_queries.return_value = ["q1", "q2"]

    mock_instance = MagicMock()
    mock_client.return_value = mock_instance

    tweet = sample_tweet_raw_response

    mock_instance.fetch_tweets_by_query.side_effect = [
        [tweet],
        [tweet],  # duplicate
    ]

    result = fetch_tweets()

    assert len(result) == 1


@patch("src.services.twitter_service.put_record")
def test_add_tweets_to_DB_creates_correct_item(
    mock_put,
    sample_parsed_tweet,
):
    """
    tests add tweet to db uploads with correct item
    """
    add_tweets_to_dynamoDB(sample_parsed_tweet)

    mock_put.assert_called_once_with(
        {
            "Date": "2026-02-02",
            "account_name": "T1 Sydney Trains",
            "text": sample_parsed_tweet[0]["master_text"],
            "status": None,
        }
    )


@patch("src.services.twitter_service.TwitterClient")
@patch("src.services.twitter_service.generate_weekly_queries")
@patch("src.services.twitter_service.time.sleep")
def test_fetch_uses_timeframe_queries(mock_sleep, mock_queries, mock_client):
    """
    tests fetch tweets is called for each query
    """
    queries = [
        "query since:2026-02-01 until:2026-02-08",
        "query since:2026-02-08 until:2026-02-15",
    ]
    mock_queries.return_value = queries

    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.fetch_tweets_by_query.return_value = []

    fetch_tweets()

    # Check correct timeframe queries were used
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
    tests full service pipline from creation to upload to db
    """
    # Arrange
    mock_fetch.return_value = [sample_tweet_raw_response]
    mock_parse.return_value = sample_parsed_tweet

    # Act
    procress_tweets_and_upload_to_dynamo_db()

    # Assert
    mock_fetch.assert_called_once()
    mock_parse.assert_called_once_with([sample_tweet_raw_response])
    mock_add.assert_called_once_with(sample_parsed_tweet)
