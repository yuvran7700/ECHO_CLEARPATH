# twitter_service.py
"""
Service layer for orchestrating tweet retrieval from the Twitter client.
Handles pagination logic and exports data to local storage for analysis.
"""

import json
import os
import time
from datetime import datetime, timedelta

from src.repositories.db_repo import put_record
from src.dependencies.twitter_client import TwitterClient
from src.utils.json_helpers import create_dict_from_json

TWEETS_FILE = "TESTREFACTOR.json"
# Date range to fetch
START_DATE = datetime.strptime("2026-02-01", "%Y-%m-%d")
END_DATE = datetime.strptime("2026-03-18", "%Y-%m-%d")

BASE_QUERY = (
    "(from:T1SydneyTrains) "
    "(delay OR disruption OR cancelled OR suspended "
    "OR delayed OR allow extra time)"
)

# # SPRINT 1: CALL STATIC FILE
# CLEANED_TWEET_FILE = "processed_tweets.json"

def generate_weekly_queries(start_date: datetime, end_date: datetime):
    """
    Generate weekly query ranges from start_date to end_date.
    Each query covers 7 days.
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
    Retrieves multiple pages of tweets to ensure a larger data sample.

    Args:
        api_key: The authentication key for the Twitter API wrapper.

    Returns:
        list: A combined list of tweet objects from all fetched pages.
    """

    DATA_FOLDER = "data"
    os.makedirs(DATA_FOLDER, exist_ok=True)
    file_path = os.path.join(DATA_FOLDER, TWEETS_FILE)

    all_tweets = []
    client = TwitterClient()

    queries = generate_weekly_queries(START_DATE, END_DATE)
    print(f"DEBUG: Generated {len(queries)} weekly queries\n")

    for q in queries:
        # Fetch tweets for this week
        week_tweets = client.fetch_tweets_by_query(q)
        all_tweets.extend(week_tweets)
        print(f"DEBUG: Collected {len(week_tweets)} tweets\n")

        # Be polite to the API
        time.sleep(1)

    #For all tweets, removes all the duplicates
    unique_tweets = list({t["id"]: t for t in all_tweets}.values())
    print(f"DEBUG: Total unique tweets: {len(unique_tweets)}")


    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(unique_tweets, f, indent=2, ensure_ascii=False)

    print(f"DEBUG: Saved to {TWEETS_FILE}")

    return unique_tweets


def add_tweets_to_dynamoDB(parsed_tweets: str) -> None:
    data = create_dict_from_json(parsed_tweets)

    for record in data:
        item = {
            "Date": record["date"],
            "account_name": record["account_name"],
            "text": record["master_text"],
            "status": None,
        }
        put_record(item)


# # TEST MAIN TO CHECK IF SERVICE RETURNS TWEETS CORRECTLY FOR PAGNIATION
# if __name__ == "__main__":

#     tweets = fetch_tweets()
#     # add_tweets_to_dynamoDB(CLEANED_TWEET_FILE)

#     # print(f"Fetched {len(tweets)} tweets")
