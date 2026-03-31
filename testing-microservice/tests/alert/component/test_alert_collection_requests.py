import requests

"""
This test file checks for all the cases
that should trigger a bad request
"""

BASE_URL = "https://18dydsthbi.execute-api.us-east-1.amazonaws.com"

# ─── MISSING PARAMETERS ──────────────────────────────────────────────────


def test_alert_collection_missing_request_pramas_returns_400():
    response = requests.get(f"{BASE_URL}/alert/collection", params={})

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query, start_date, and end_date are required"
    )


def test_alert_collection_missing_start_date_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "base_query": "(from:T1SydneyTrains)",
            "end_date": "2026-03-23",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query, start_date, and end_date are required"
    )


def test_alert_collection_missing_end_date_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "base_query": "(from:T1SydneyTrains)",
            "start_date": "2026-03-23",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query, start_date, and end_date are required"
    )


def test_alert_collection_missing_base_query_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "start_date": "2026-03-01",
            "end_date": "2026-03-23",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query, start_date, and end_date are required"
    )


# ─── INVALID DATE QUERY ──────────────────────────────────────────────────


def test_alert_collection_invalid_date_range_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "base_query": "(from:T1SydneyTrains)",
            "start_date": "2026-03-23",
            "end_date": "2026-03-01",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "start_date must be earlier or equal to end_date"
    )


def test_alert_collection_invalid_date_format_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "base_query": "(from:T1SydneyTrains)",
            "start_date": "23-03-2026",
            "end_date": "24-03-2026",
        },
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Dates must be in YYYY-MM-DD format"


# ─── INVALID BASE QUERY ──────────────────────────────────────────────────


def test_alert_collection_base_query_without_from_prefix_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "base_query": "T1SydneyTrains",
            "start_date": "2026-03-01",
            "end_date": "2026-03-23",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query must include 'from:account_name' filter"
    )


def test_alert_collection_base_query_missing_from_filter_message_returns_400():
    response = requests.get(
        f"{BASE_URL}/alert/collection",
        params={
            "base_query": "(delay OR disruption)",
            "start_date": "2026-03-01",
            "end_date": "2026-03-23",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query must include 'from:account_name' filter"
    )


# ─── 503 SERVICE UNAVAILABLE ─────────────────────────────────────────────


def test_alert_collection_large_date_range_returns_503():
    return


def test_alert_collection_service_unavailable_contains_message_field():
    return


def test_alert_collection_service_unavailable_message_returns_503():
    return
