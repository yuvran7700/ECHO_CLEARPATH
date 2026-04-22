# src/services/preprocessing_service.py
"""
Service layer for classifying newly inserted tweet records.

This service is triggered separately from tweet collection and is
responsible for:
- extracting data from a DynamoDB Streams record
- classifying tweet text
- updating the record lifecycle state in DynamoDB
"""

import logging
import os

import joblib
from src.repositories.db_repo import update_record

# Configure logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "../ml/model/tweet_classifier.pkl"
)
_classifier = joblib.load(_MODEL_PATH)


def classify_tweet(text: str) -> str:
    """
    Classify tweet text using TF-IDF + Logistic Regression model.

    Args:
        text (str): Tweet text to classify.

    Returns:
        str: Predicted classification label (cancelled / delayed / unknown).
    """
    prediction = _classifier.predict([text])
    return prediction[0]


def classify_record(record: dict) -> bool:
    """
    Classify a DynamoDB Streams record and update its lifecycle state.

    This function:
    - extracts the primary key, text, and status from the stream record
    - skips invalid or already-classified records
    - classifies the tweet text
    - appends "classified" to the status array
    - stores the classification result in DynamoDB

    Args:
        record (dict): DynamoDB Streams NewImage payload.

    Returns:
        bool:
            True if the record was successfully processed.
            False if the record was skipped.
    """
    # Extract date, text and status from DynamoDB stream format
    date = record.get("date", {}).get("S")
    text = record.get("text", {}).get("S")
    status_values = record.get("status", {}).get("L", [])
    current_status = [
        item.get("S") for item in status_values if item.get("S") is not None
    ]

    # Skip records missing required fields
    if (not date) or (not text):
        logger.warning(
            "Skipping record due to missing required fields: Date=%s",
            date,
        )
        return False

    # Skip records that have already been classified
    if "classified" in current_status:
        logger.info("Skipping already classified record: Date=%s", date)
        return False

    # Log start of classification for observability
    logger.info("Classifying record: Date=%s", date)

    # Run the classification model on the tweet text
    classification = classify_tweet(text)

    # Create a copy of the current lifecycle status list
    updated_status = list(current_status)

    # Append the next lifecycle stage
    updated_status.append("classified")

    # Persist both classification result and updated lifecycle state
    update_record(
        date,
        {
            "classification": classification,
            "status": updated_status,
        },
    )

    # Log successful classification outcome
    logger.info(
        "Successfully classified record: Date=%s, classification=%s",
        date,
        classification,
    )

    return True
