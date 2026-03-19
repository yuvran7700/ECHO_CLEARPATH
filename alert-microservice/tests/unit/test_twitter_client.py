from unittest.mock import MagicMock, patch

import pytest
import requests
from src.dependencies.twitter_client import TwitterClient

pytestmark = pytest.mark.unit_client


def fetch_tweets_is_called_for_the_query_created():
    return


@patch("src.dependencies.twitter_client.requests.get")
def test_fetch_tweets_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tweets": [{"id": "1"}],
        "has_next_page": False,
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    client = TwitterClient()
    result = client.fetch_tweets_by_query("test query")

    assert result == [{"id": "1"}]
    mock_get.assert_called_once()


@patch("src.dependencies.twitter_client.requests.get")
def test_fetch_tweets_pagination(mock_get):
    response1 = MagicMock()
    response1.json.return_value = {
        "tweets": [{"id": "1"}],
        "has_next_page": True,
        "next_cursor": "abc",
    }
    response1.raise_for_status.return_value = None

    response2 = MagicMock()
    response2.json.return_value = {
        "tweets": [{"id": "2"}],
        "has_next_page": False,
    }
    response2.raise_for_status.return_value = None

    mock_get.side_effect = [response1, response2]

    client = TwitterClient()
    result = client.fetch_tweets_by_query("test query")

    assert len(result) == 2
    assert result == [{"id": "1"}, {"id": "2"}]


@patch("src.dependencies.twitter_client.time.sleep")
@patch("src.dependencies.twitter_client.requests.get")
def test_fetch_retries_then_succeeds(mock_get, mock_sleep):
    mock_get.side_effect = [
        requests.exceptions.RequestException("API error"),
        MagicMock(
            json=lambda: {"tweets": [{"id": "1"}], "has_next_page": False},
            raise_for_status=lambda: None,
        ),
    ]

    client = TwitterClient()
    result = client.fetch_tweets_by_query("test query")

    assert result == [{"id": "1"}]
    assert mock_get.call_count == 2


@patch("src.dependencies.twitter_client.time.sleep")
@patch("src.dependencies.twitter_client.requests.get")
def test_fetch_stops_after_max_retries(mock_get, mock_sleep):
    mock_get.side_effect = requests.exceptions.RequestException("API error")

    client = TwitterClient(max_retries=2)
    result = client.fetch_tweets_by_query("test query")

    assert result == []  # nothing collected
    assert mock_get.call_count == 2


@patch("src.dependencies.twitter_client.time.sleep")
@patch("src.dependencies.twitter_client.requests.get")
def test_fetch_returns_partial_data_on_failure(mock_get, mock_sleep):
    response = MagicMock()
    response.json.return_value = {
        "tweets": [{"id": "1"}],
        "has_next_page": True,
        "next_cursor": "abc",
    }
    response.raise_for_status.return_value = None

    mock_get.side_effect = [
        response,  # first page works
        requests.exceptions.RequestException("API error"),
    ]

    client = TwitterClient(max_retries=1)
    result = client.fetch_tweets_by_query("test query")

    assert result == [{"id": "1"}]
