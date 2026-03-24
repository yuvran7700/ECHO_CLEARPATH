# handlers/classification_handler.py
"""
AWS Lambda handler for classifying newly inserted DynamoDB records.

This handler:
- detects new records uploaded to DynamoDB table "clearpath-alert-data"
- loops through the DynamoDB stream batch
- passes each new record to the service layer to classify and presist them
- logs processing outcomes for observability
"""

import logging

from src.services.preprocessing_service import classify_record

# Configure logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def classification_handler(event, context):
    """
    Process a batch of DynamoDB Streams records.

    Logs:
    - batch size
    - per-record processing outcomes
    - summary metrics (processed/skipped/failed)

    Args:
        event (dict): DynamoDB Streams event payload.
        context: AWS Lambda runtime context.

    Returns:
        dict: Summary of processed, skipped, and failed records.
    """
    processed_count = 0  # Number of successfully classified records
    skipped_count = 0  # Number of skipped records
    failed_count = 0  # Number of records that raised exceptions

    # Log batch size for observability (helps understand throughput)
    records = event.get("Records", [])
    logger.info("Received DynamoDB stream batch with %d records", len(records))

    # Iterate through all records in the stream batch
    for stream_record in records:
        try:
            # Only process newly inserted records
            if stream_record.get("eventName") != "INSERT":
                logger.info(
                    "Skipping non-INSERT event: %s",
                    stream_record.get("eventName"),
                )
                skipped_count += 1
                continue

            # Extract the inserted item image from the stream payload
            new_image = stream_record.get("dynamodb", {}).get("NewImage", {})

            # Log that we are processing a new record
            logger.info("Processing new DynamoDB record")

            # Delegate classification logic to the service layer
            was_processed = classify_record(new_image)

            # Update counters and log outcome
            if was_processed:
                processed_count += 1
            else:
                skipped_count += 1

        except Exception as error:
            # Log the error with full context for debugging
            logger.error(
                "Error processing stream record: %s",
                error,
                exc_info=True,
            )
            failed_count += 1

    # Log final batch summary
    logger.info(
        "Batch processing complete: %d processed, %d skipped, %d failed",
        processed_count,
        skipped_count,
        failed_count,
    )

    # Return summary for observability and debugging
    return {
        "statusCode": 200,
        "body": {
            "processed_count": processed_count,
            "skipped_count": skipped_count,
            "failed_count": failed_count,
        },
    }
