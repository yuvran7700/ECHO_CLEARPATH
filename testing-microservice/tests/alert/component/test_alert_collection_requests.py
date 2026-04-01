# Component tests for GET /alert/collection (Staging).
#
# Verifies the full request/response cycle against the deployed staging
# endpoint — covering successful responses, missing parameters, invalid
# dates, and invalid base query formats.

import requests

VALID_PARAMS = {
    "base_query": "(from:T1SydneyTrains)",
    "start_date": "2026-03-01",
    "end_date": "2026-03-07",
}

# ─── 200 SUCCESS ─────────────────────────────────────────────────────────


def test_alert_collection_valid_request_returns_200(alert_collection_url):
    response = requests.get(
        alert_collection_url,
        params=VALID_PARAMS,
    )

    assert response.status_code == 200


def test_alert_collection_response_has_body(alert_collection_url):
    response = requests.get(
        alert_collection_url,
        params=VALID_PARAMS,
    )

    body = response.json()
    assert body is not None
    assert len(body) > 0


def test_alert_collection_response_contains_events(alert_collection_url):
    response = requests.get(
        alert_collection_url,
        params=VALID_PARAMS,
    )

    assert "events" in response.json()
    assert isinstance(response.json()["events"], list)


def test_alert_collection_response_has_correct_content_type(
    alert_collection_url,
):
    response = requests.get(
        alert_collection_url,
        params=VALID_PARAMS,
    )

    assert response.headers["Content-Type"] == "application/json"


# ─── MISSING PARAMETERS ──────────────────────────────────────────────────
def test_alert_collection_missing_all_params_returns_400(alert_collection_url):
    response = requests.get(alert_collection_url, params={})

    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "base_query, start_date, and end_date are required"
    )


def test_alert_collection_missing_start_date_returns_400(alert_collection_url):
    response = requests.get(
        alert_collection_url,
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


def test_alert_collection_missing_end_date_returns_400(alert_collection_url):
    response = requests.get(
        alert_collection_url,
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


def test_alert_collection_missing_base_query_returns_400(alert_collection_url):
    response = requests.get(
        alert_collection_url,
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


def test_alert_collection_invalid_date_range_returns_400(alert_collection_url):
    response = requests.get(
        alert_collection_url,
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


def test_alert_collection_invalid_date_format_returns_400(
    alert_collection_url,
):
    response = requests.get(
        alert_collection_url,
        params={
            "base_query": "(from:T1SydneyTrains)",
            "start_date": "23-03-2026",
            "end_date": "24-03-2026",
        },
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Dates must be in YYYY-MM-DD format"


# ─── INVALID BASE QUERY ──────────────────────────────────────────────────


def test_alert_collection_base_query_without_from_prefix_returns_400(
    alert_collection_url,
):
    response = requests.get(
        alert_collection_url,
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


def test_alert_collection_base_query_missing_from_filter_message_returns_400(
    alert_collection_url,
):
    response = requests.get(
        alert_collection_url,
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
