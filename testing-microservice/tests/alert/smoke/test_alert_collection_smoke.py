# tests/smoke/test_alert_collection_smoke.py

import requests


def test_alert_collection_is_alive(alert_collection_url, valid_alert_params):
    """Smoke test: verify /alert/collection is reachable in production"""
    response = requests.get(
        alert_collection_url,
        valid_alert_params,
    )
    assert response.status_code < 500
