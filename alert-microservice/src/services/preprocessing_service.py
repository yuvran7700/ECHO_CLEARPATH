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

from src.repositories.db_repo import update_record

# Configure logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def classify_tweet(text: str) -> str:
    """
    Classify tweet text into a disruption category.

    Args:
        text (str): Tweet text to classify.

    Returns:
        str: Predicted classification label.
    """
    # Normalize text for case-insensitive keyword matching
    text = text.lower()

    # Keywords that indicate full cancellation or service suspension
    cancelled_keywords = [
        "cancelled",
        "canceled",
        "suspended",
        "no service",
        "not running",
        "shutdown",
        "closed",
    ]

    # Keywords that indicate delays or partial disruption
    delayed_keywords = [
        "delayed",
        "delay",
        "slow",
        "disruption",
        "late",
        "reduced",
        "minor delays",
        "part suspended",
    ]

    # Check for cancellation-related keywords first
    for keyword in cancelled_keywords:
        if keyword in text:
            return "cancelled"

    # Check for delay-related keywords next
    for keyword in delayed_keywords:
        if keyword in text:
            return "delayed"

    # Default fallback if no keywords match
    return "unknown"


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
