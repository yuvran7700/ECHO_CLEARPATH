"""
This test file checks for all the cases
that should trigger a bad request
"""

BASE_URL = "https://18dydsthbi.execute-api.us-east-1.amazonaws.com"

# ─── MISSING PARAMETERS ──────────────────────────────────────────────────


def test_alert_collection_missing_request_pramas_returns_400():
    return


def test_alert_collection_missing_start_date_returns_400():
    return


# ─── INVALID DATE QUERY ──────────────────────────────────────────────────


def test_alert_collection_invalid_date_range_returns_400():
    return


def test_alert_collection_invalid_date_format_returns_400():
    return


def test_alert_collection_invalid_date_returns_400():
    return


# ─── INVALID BASE QUERY ──────────────────────────────────────────────────


def test_alert_collection_base_query_without_from_prefix_returns_400():
    return


def test_alert_collection_base_query_missing_from_filter_message_returns_400():
    return


# ─── 503 SERVICE UNAVAILABLE ─────────────────────────────────────────────


def test_alert_collection_large_date_range_returns_503():
    return


def test_alert_collection_service_unavailable_contains_message_field():
    return


def test_alert_collection_service_unavailable_message_returns_503():
    return
