# src/lambda_handlers/join_lambda_handler.py
import logging

from src.services.join_service import run_join

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def join_lambda_handler(event, context):
    logger.info("DynamoDB stream triggered join job")
    run_join()
