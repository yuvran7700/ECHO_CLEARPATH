"""
transport-microservice/src/services/join_service.py
Join weather and alert DynamoDB tables on date using a LEFT JOIN
(weather as the base table), then save the result into the
clearpath-weather-alert-joined table.
"""

import logging
from typing import Any

from src.dependencies.db_client import (
    alert_table,
    joined_table,
    weather_table,
)
from src.repositories.db_repo import (
    batch_write_items,
    get_record,
    scan_all_items,
)

logger = logging.getLogger(__name__)


def build_joined_item(
    weather_item: dict[str, Any],
    alert_item: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Build one joined row using LEFT JOIN semantics.
    """
    joined_item = weather_item.copy()

    if alert_item is not None:
        joined_item["account_name"] = alert_item.get("account_name")
        joined_item["classification"] = alert_item.get("classification")
        joined_item["disruption"] = True
    else:
        joined_item["account_name"] = "Unavailable"
        joined_item["classification"] = "Unavailable"
        joined_item["disruption"] = False

    return joined_item


def run_join() -> None:
    """
    Execute the full LEFT JOIN from weather to alerts and store the result
    in the joined DynamoDB table.
    """
    logger.info("Join job started")

    try:
        # Step 1: Scan weather table
        weather_items = scan_all_items(weather_table)
        logger.info(
            "Weather scan complete", extra={"row_count": len(weather_items)}
        )

        joined_items: list[dict[str, Any]] = []
        matched_alert_count = 0
        unmatched_weather_count = 0

        # Step 2: Perform LEFT JOIN
        for weather_item in weather_items:
            date = weather_item.get("date")
            alert_item = get_record(alert_table, date)

            if alert_item:
                matched_alert_count += 1
            else:
                unmatched_weather_count += 1

            joined_item = build_joined_item(weather_item, alert_item)
            joined_items.append(joined_item)

        logger.info(
            "Join build phase complete",
            extra={
                "joined_rows": len(joined_items),
                "matched_alerts": matched_alert_count,
                "weather_only_rows": unmatched_weather_count,
            },
        )

        # Step 3: Write results
        batch_write_items(
            joined_table,
            joined_items,
            overwrite_by_pkeys=["date"],
        )

        logger.info(
            "Join job completed successfully",
            extra={"rows_written": len(joined_items)},
        )

    except Exception:
        logger.exception("Join job failed")
        raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    run_join()
