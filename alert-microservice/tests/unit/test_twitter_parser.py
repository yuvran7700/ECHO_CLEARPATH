from src.parsers.twitter_parser import (
    collate_tweets,
    extract_metadata,
    format_date,
    parse_tweets,
)


def test_parse_date_returns_correct_format():
    """
    tests the date formatter takes the correct arg and
    returns the expected value
    """

    example_created_at = "Fri Nov 07 22:02:37 +0000 2025"
    result = format_date(example_created_at)
    assert result == "2025-11-07"


def test_format_date_handles_invalid_date():
    """Test date formatter handles invalid input gracefully."""
    result = format_date("invalid date string")
    assert result == "Invalid Date"


def test_extract_data_from_tweets_returns_correct_fields(
    sample_tweet_raw_response, sample_extracted_tweet
):
    """Test that extraction pulls correct fields from raw tweet."""
    raw_tweet = sample_tweet_raw_response
    expected_processed_tweet = sample_extracted_tweet

    result = extract_metadata([raw_tweet])
    print(result)
    assert result == expected_processed_tweet


def test_tweets_on_same_day_are_collated_into_one_date(
    sample_tweets_on_same_day, sample_collated_tweets_on_same_date
):
    collate_tweets_result = collate_tweets(sample_tweets_on_same_day)
    expected_collated_tweets = sample_collated_tweets_on_same_date
    assert collate_tweets_result == expected_collated_tweets


def test_collate_tweets_did_not_lose_data(sample_tweets_on_same_day):
    """Verify no tweet content is lost during collation."""
    result = collate_tweets(sample_tweets_on_same_day)

    original_length = sum(
        len(tweet["text"]) for tweet in sample_tweets_on_same_day
    )

    collated_length = sum(len(item["master_text"]) for item in result)

    assert collated_length >= original_length


def test_collate_tweets_created_mastertext_with_eot(sample_tweets_on_same_day):
    """Verify collated output has master_text with EOT separators."""
    result = collate_tweets(sample_tweets_on_same_day)

    for item in result:
        assert "master_text" in item
        if item["master_text"].count("\n") > 0:
            assert "EOT" in item["master_text"]


def test_parse_tweets_returns_correct_output(
    sample_tweet_raw_response, sample_parsed_tweet
):
    result = parse_tweets([sample_tweet_raw_response])
    assert result == sample_parsed_tweet


def test_parse_tweets_returns_list():
    """Test parse_tweets returns a list."""
    tweet = {
        "author": {"name": "Test"},
        "createdAt": "Mon Feb 02 00:15:28 +0000 2026",
        "text": "Test",
    }
    result = parse_tweets([tweet])
    assert isinstance(result, list)


def test_parse_tweets_with_empty_list():
    """Test parse_tweets handles empty input."""
    result = parse_tweets([])
    assert result == []
