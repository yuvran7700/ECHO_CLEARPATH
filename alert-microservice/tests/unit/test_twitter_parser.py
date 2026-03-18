from src.parsers.twitter_parser import (
    extract_metadata,
    format_date,
)


def test_parse_date_returns_correct_format():
    """
    tests the date formatter takes the correct arg and
    returns the expected value
    """

    example_created_at = "Fri Nov 07 22:02:37 +0000 2025"
    result = format_date(example_created_at)
    assert result == "2025-11-07"


def test_extract_data_from_tweets_returns_correct_fields(
    sample_tweet_raw_response, sample_extracted_tweet
):
    raw_tweet = sample_tweet_raw_response
    expected_processed_tweet = sample_extracted_tweet

    result = extract_metadata([raw_tweet])
    print(result)
    assert result == expected_processed_tweet


def test_tweets_on_same_day_are_collated_into_one_date():
    return


def test_collate_tweets_did_not_lose_data():
    return


def test_collate_tweets_created_mastertext_with_eot():
    return


def test_parse_tweets_returns_correct_cleaned_data():
    return
