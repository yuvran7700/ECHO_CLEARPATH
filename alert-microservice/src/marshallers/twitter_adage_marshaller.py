"""
Marshalling logic for converting parsed tweet records into
ADAGE 3.0 data model format.
"""

from datetime import datetime, timezone


def marshal_tweets_to_adage(
    tweets: list[dict],
    base_query: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Convert parsed tweets into an ADAGE 3.0 dataset response.

    Args:
        tweets (list[dict]): Parsed tweet records.
        base_query (str): Twitter search query used for collection.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        dict: Tweets formatted as an ADAGE 3.0 dataset object.
    """
    dataset_timestamp = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    events = []

    for tweet in tweets:
        event = {
            "time_object": {
                "timestamp": tweet["date"],
                "duration": 0,
                "duration_unit": "second",
                "timezone": "UTC",
            },
            "event_type": "transport disruption tweet",
            "attribute": {
                "account_name": tweet["account_name"],
                "text": tweet["text"],
                "date": tweet["date"],
            },
        }
        events.append(event)

    return {
        "data_source": "Twitter",
        "dataset_type": "Historical Tweets",
        "dataset_id": (
            f"twitter:{start_date}:{end_date}:{abs(hash(base_query))}"
        ),
        "time_object": {
            "timestamp": dataset_timestamp,
            "timezone": "UTC",
        },
        "events": events,
    }
