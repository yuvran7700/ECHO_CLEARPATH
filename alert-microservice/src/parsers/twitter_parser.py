# parsers/twitter_parser.py

"""
Parser module for cleaning and formatting tweets.

Contains functions to:
- Convert Twitter date strings to YYYY-MM-DD format.
- Extract key metadata: account name, date, and text.
- Collate multiple tweets from the same account on the same day into a
single text entry.
- Prepare tweets for storage or further processing.

This module is intended to be used by the Twitter service layer before
writing to DynamoDB.
"""

from datetime import datetime
from typing import Dict, List

from src.parsers.text_normalisation import normalise_text


def is_reply(tweet: dict) -> bool:
    """
    Identify reply tweets.

    For this dataset, replies reliably begin with '@' in the tweet text.
    """
    text = tweet.get("text", "")
    return text.strip().startswith("@")


def format_date(created_at: str):
    """
    Parse Twitter date format and convert to YYYY-MM-DD.

    Args:
        created_at (str): Date string in Twitter format
        "Fri Nov 07 22:02:37 +0000 2025"

    Returns:
        str: Formatted date as YYYY-MM-DD, or 'Invalid Date' if parsing fails
    """
    try:
        date_obj = datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
        date_formatted = date_obj.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        date_formatted = "Invalid Date"

    return date_formatted


def extract_metadata(tweets: list):
    """
    Extract only essential metadata from tweets.

    Retains only: account_name, date (YYYY-MM-DD), text
    Removes replies and all other unnecessary metadata.

    Args:
        tweets (list): list of tweet objects

    Returns:
        list: List of dictionaries with account_name, date, and text fields
    """
    extracted_tweets = []

    for tweet in tweets:
        if is_reply(tweet):
            continue

        extracted_tweets.append(
            {
                "account_name": tweet.get("author", {}).get("name", "Unknown"),
                "date": format_date(tweet.get("createdAt")),
                "text": tweet.get("text", ""),
            }
        )

    return extracted_tweets


def collate_tweets(cleaned_tweets: List[Dict]) -> List[Dict]:
    """for tweets on the same day, make into one master string (with EOT \n
    between them)"""
    collated = {}

    for tweet in cleaned_tweets:
        # Create unique key: (account_name, date)
        key = (tweet["account_name"], tweet["date"])

        if key not in collated:
            # First tweet for this account on this date
            collated[key] = {
                "account_name": tweet["account_name"],
                "date": tweet["date"],
                "master_text": tweet["text"],
            }
        else:
            # Another tweet for same account on same date - append it
            collated[key]["master_text"] += "EOT\n" + tweet["text"]

    return list(collated.values())


def deduplicate_tweets(cleaned_tweets: List[Dict]) -> List[Dict]:
    """
    Remove duplicate tweets within the same day based on normalised text.
    Keeps identical tweets if they occur on different dates.
    """
    seen = set()
    unique_tweets = []

    for tweet in cleaned_tweets:
        normalized = normalise_text(tweet["text"])
        key = (tweet["date"], normalized)

        if key in seen:
            continue

        seen.add(key)
        unique_tweets.append(tweet)
    return unique_tweets


def parse_tweets(tweets: list[dict], collate: bool = True) -> list[dict]:
    extracted = extract_metadata(tweets)
    extracted = deduplicate_tweets(extracted)

    if collate:
        return collate_tweets(extracted)

    return extracted
