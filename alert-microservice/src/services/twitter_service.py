# services/twitter_service.py
"""
Service layer for orchestrating tweet retrieval from the Twitter client
and uploading formatted tweets to DynamoDB.
This module coordinates the workflow: fetching -> parsing -> storing.
"""

import time
from datetime import datetime, timedelta

from src.dependencies.twitter_client import TwitterClient
from src.parsers.twitter_parser import parse_tweets
from src.repositories.db_repo import put_record

# Date range for tweets to fetch (can be updated for other periods)
START_DATE = datetime.strptime("2026-02-01", "%Y-%m-%d")
END_DATE = datetime.strptime("2026-03-18", "%Y-%m-%d")

# Base search query for Sydney Trains disruptions (used for weekly
#  query generation)
BASE_QUERY = (
    "(from:T1SydneyTrains) "
    "(delay OR disruption OR cancelled OR suspended "
    "OR delayed OR allow extra time)"
)


def procress_tweets_and_upload_to_dynamo_db():
    """
    Main pipeline to fetch tweets, parse them, and add them to DynamoDB.
    Orchestrates the three core steps of the service.
    """
    all_tweets = fetch_tweets()  # Step 1: Retrieve raw tweets
    formatted_tweets = parse_tweets(
        all_tweets
    )  # Step 2: Format tweets into structured data
    add_tweets_to_dynamoDB(
        formatted_tweets
    )  # Step 3: Store structured tweets in DB


def generate_weekly_queries(start_date: datetime, end_date: datetime) -> list:
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
        q = f"{BASE_QUERY} since:{since_date} until:{until_date}"

        queries.append(q)
        current = next_week
    return queries


def fetch_tweets() -> list:
    """
    Retrieve tweets from Twitter using weekly queries.
    Handles pagination and deduplication of tweets.

    Returns:
        list[dict]: List of unique raw tweet objects
    """
    all_tweets = []
    client = TwitterClient()

    queries = generate_weekly_queries(START_DATE, END_DATE)
    print(f"DEBUG: Generated {len(queries)} weekly queries\n")

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
            "Date": record["date"],
            "account_name": record["account_name"],
            "text": record["master_text"],
            "status": None,
        }
        put_record(item)


# TEST MAIN
# If the file is run directly, execute the full pipeline
if __name__ == "__main__":
    procress_tweets_and_upload_to_dynamo_db()
