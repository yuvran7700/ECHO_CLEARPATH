# services/twitter_service.py
"""
Service layer for orchestrating tweet retrieval from the Twitter client
and uploading formatted tweets to DynamoDB.
This module coordinates the workflow: fetching -> parsing -> storing.
"""

import time
from datetime import datetime, timedelta

from src.dependencies.twitter_client import TwitterClient
from src.marshallers.twitter_adage_marshaller import marshal_tweets_to_adage
from src.parsers.twitter_parser import parse_tweets
from src.repositories.db_repo import put_record

# Date range for tweets to fetch (can be updated for other periods)
START_DATE = "2026-02-01"
END_DATE = "2026-03-18"

# Base search query for Sydney Trains disruptions (used for weekly
#  query generation)
BASE_QUERY = (
    "(from:T1SydneyTrains) "
    "(delay OR disruption OR cancelled OR suspended "
    "OR delayed OR allow extra time)"
)


def fetch_and_format_tweets(
    base_query: str,
    start_date: str,
    end_date: str,
) -> list[dict]:
    """
    Fetch tweets from Twitter and parse them into structured records.

    Args:
        base_query (str): Twitter search query without date filters.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        list[dict]: Parsed tweet records.
    """
    raw_tweets = fetch_tweets(base_query, start_date, end_date)
    formatted_tweets = parse_tweets(raw_tweets)
    return formatted_tweets


def generate_weekly_queries(
    base_query: str, start_date: datetime, end_date: datetime
) -> list:
    """
    Generate weekly search queries for the given date range.
    Each query spans 7 days. If the last week is shorter, it ends at end_date.

    Args:
        start_date (datetime): The beginning of the search range
        end_date (datetime): The end of the search range

    Returns:
        list[str]: List of weekly queries with correct
        'since' and 'until' dates
    """
    queries = []
    current = start_date

    while current < end_date:
        next_week = current + timedelta(days=7)

        if next_week > end_date:
            next_week = end_date

        since_date = current.strftime("%Y-%m-%d")
        until_date = next_week.strftime("%Y-%m-%d")
        q = f"{base_query} since:{since_date} until:{until_date}"

        queries.append(q)
        current = next_week
    return queries


def fetch_tweets(
    base_query: str,
    start_date: str,
    end_date: str,
) -> list[dict]:
    """
    Retrieve tweets from Twitter using weekly queries.
    Handles pagination and deduplication of tweets.

    Returns:
        list[dict]: List of unique raw tweet objects
    """
    all_tweets = []
    client = TwitterClient()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    queries = generate_weekly_queries(base_query, start, end)

    for q in queries:
        # Fetch tweets for this week
        week_tweets = client.fetch_tweets_by_query(q)
        all_tweets.extend(week_tweets)
        # print(f"DEBUG: Collected {len(week_tweets)} tweets\n")

        # Be polite to the API
        time.sleep(1)

    # For all tweets, removes all the duplicates
    unique_tweets = list({t["id"]: t for t in all_tweets}.values())
    # print(f"DEBUG: Total unique tweets: {len(unique_tweets)}")

    return unique_tweets


def add_tweets_to_dynamoDB(parsed_tweets: list) -> None:
    """
    Upload parsed tweets to DynamoDB.
    Each tweet becomes a record with Date, account_name, text, and status.

    Args:
        parsed_tweets (list[dict]): List of formatted tweets from parse_tweets
    """
    data = parsed_tweets

    for record in data:
        item = {
            "date": record["date"],
            "account_name": record["account_name"],
            "text": record["master_text"],
            "status": ["collected"],
        }
        put_record(item)


def process_tweets_and_upload_to_dynamodb():
    """
    Main pipeline to fetch tweets, parse them, and add them to DynamoDB.
    Orchestrates the three core steps of the service.
    """
    # Step 1: Retrieve raw tweets and format them
    tweets = fetch_and_format_tweets(
        base_query=BASE_QUERY,
        start_date=START_DATE,
        end_date=END_DATE,
    )
    # Step 2: Store structured tweets in DB
    add_tweets_to_dynamoDB(tweets)


def process_tweets_and_return_to_user(
    base_query: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Fetch tweets from Twitter, parse them into structured records,
    and return them in ADAGE 3.0 format.

    Args:
        base_query (str): Twitter search query without date filters.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        dict: Tweets formatted as an ADAGE 3.0 dataset object.
    """
    tweets = fetch_and_format_tweets(
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )

    return marshal_tweets_to_adage(
        tweets=tweets,
        base_query=base_query,
        start_date=start_date,
        end_date=end_date,
    )


# TEST MAIN
# If the file is run directly, execute the full pipeline
if __name__ == "__main__":
    process_tweets_and_upload_to_dynamodb()
