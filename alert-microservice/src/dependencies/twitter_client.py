# twitter_client.py

"""
Twitter API client for retrieving Sydney Trains disruption alerts.

This module encapsulates the external API calls for the ClearPath
alert-microservice.
It handles pagination, retries, and rate-limiting for the TwitterAPI.io
Advanced Search endpoint.

Credits:
    Initial implementation adapted from the TwitterAPI.io Advanced Search
    documentation:
    https://twitterapi.io/blog/scrape-twitter-history-tweet
"""

import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")

# The endpoint for advanced search provided by the third-party Twitter API
# wrapper.
BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"


class TwitterClient:
    """
    Client to interact with the Twitter API for fetching disruption tweets.

    Handles:
        - Constructing API requests
        - Pagination via cursors
        - Retry logic for failed requests
        - Rate limiting via sleep backoff
    """

    def __init__(self, max_retries: int = 3):
        """
        Initialize the client with default settings.

        Args:
            max_retries (int): Number of times to retry
            a failed request (default=3)
        """
        self.api_url = BASE_URL
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.headers = {"X-API-Key": self.api_key}
        self.max_retries = max_retries

    def fetch_tweets_by_query(self, query: str) -> list:
        """
        Fetch tweets from TwitterAPI.io based on a search query.

        Handles:
            - Pagination using cursor returned from API
            - Retries on network or API errors
            - Aggregation of all tweets into a single list

        Args:
            query (str): Search query containing account and keywords,
            and optional date ranges

        Returns:
            list[dict]: List of raw tweet objects returned from the API
        """
        all_tweets = []  # Stores all tweets collected across pages
        cursor = None  # Cursor for pagination; None for first page
        has_next = True  # assume there might be pages

        while True:
            # use max_id to retrive older tweet beyond pagination
            params = {"query": query, "queryType": "Top"}

            if cursor:
                params["cursor"] = cursor

            retry_count = 0

            while retry_count < self.max_retries:
                try:
                    # Perform the GET request to the advanced search endpoint
                    response = requests.get(
                        self.api_url, headers=self.headers, params=params
                    )

                    response.raise_for_status()
                    data = response.json()

                    # from raw data collects all tweets
                    tweets = data.get("tweets", [])
                    has_next = data.get("has_next_page", False)
                    cursor = data.get("next_cursor", None)

                    for t in tweets:
                        all_tweets.append(t)

                    if not has_next:
                        return all_tweets

                    break

                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    print(
                        f"  Error: {e}, retry {retry_count}/{self.max_retries}"
                    )

                    time.sleep(2**retry_count)
                    if retry_count == self.max_retries:
                        print(
                            "Max retries reached, returning collected tweets"
                        )
                        return all_tweets

            if not has_next:
                break

        return all_tweets
