# import requests

# BASE_URL = "https://18dydsthbi.execute-api.us-east-1.amazonaws.com"


# # returns body
# def test_alert_collection_response_has_body():
#     """
#     Verifies alerts were collected and returned in the body.
#     """
#     response = requests.get(f"{BASE_URL}/alert/collection")

#     body = response.json()
#     assert body is not None
#     assert len(body) > 0

#     # returns 200


# def test_alert_collection_returns_200():
#     """
#     Hits the real API Gateway → Lambda → alert source → S3/DynamoDB.
#     Verifies the alert collection pipeline executes end to end.
#     """
#     response = requests.get(f"{BASE_URL}/alert/collection")

#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
