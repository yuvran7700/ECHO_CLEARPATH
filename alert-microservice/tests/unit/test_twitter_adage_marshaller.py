# tests/unit/test_twitter_adage_marshaller.py
from src.marshallers.twitter_adage_marshaller import marshal_tweets_to_adage


def test_marshal_tweets_to_adage_returns_expected_structure(
    sample_parsed_tweet,
):
    """
    Test that parsed tweets are converted into the expected
    ADAGE 3.0 dataset structure.
    """
    result = marshal_tweets_to_adage(
        tweets=sample_parsed_tweet,
        base_query="(from:T1SydneyTrains) (delay OR disruption)",
        start_date="2026-02-01",
        end_date="2026-02-20",
    )

    assert result["data_source"] == "Twitter"
    assert result["dataset_type"] == "Historical Tweets"
    assert "dataset_id" in result

    assert "time_object" in result
    assert result["time_object"]["timezone"] == "UTC"

    assert "events" in result
    assert len(result["events"]) == 1

    event = result["events"][0]

    assert event["event_type"] == "transport disruption tweet"
    assert event["time_object"]["timestamp"] == "2026-02-02"
    assert event["time_object"]["duration"] == 0
    assert event["time_object"]["duration_unit"] == "second"
    assert event["time_object"]["timezone"] == "UTC"

    assert event["attribute"]["account_name"] == "T1 Sydney Trains"
    assert event["attribute"]["text"] == sample_parsed_tweet[0]["master_text"]
    assert event["attribute"]["date"] == "2026-02-02"
