"""
transport-microservice/src/services/join_service.py
Join weather-location and alert DynamoDB tables on date using a LEFT JOIN
(weather-location as the base table), then save the result into the
clearpath-weather-alert-joined table with composite PK (date + location).
"""

import logging
from typing import Any

from src.dependencies.db_client import (
    alert_table,
    joined_table,
    weather_location_table,
)
from src.repositories.db_repo import (
    batch_write_items,
    get_record,
    query_by_date,
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


def run_join() -> None:  # pragma: no cover
    """
    BACKFILL ONLY — do not use in production stream triggers.
    Execute the full LEFT JOIN from weather-location to alerts and store
    the result in the joined DynamoDB table.
    """
    logger.info("Join job started")

    try:
        # Step 1: Scan weather location table (has both sydney + parramatta)
        weather_items = scan_all_items(weather_location_table)
        logger.info(
            f"Weather location scan complete: {len(weather_items)} rows"
        )

        joined_items: list[dict[str, Any]] = []
        matched_alert_count = 0
        unmatched_weather_count = 0

        # Step 2: LEFT JOIN — for each weather record, look up alert by date
        # Alerts apply to the whole T1 line regardless of location
        for weather_item in weather_items:
            date = weather_item.get("date")
            location = weather_item.get("location")

            alert_item = get_record(alert_table, date)

            if alert_item:
                matched_alert_count += 1
            else:
                unmatched_weather_count += 1

            joined_item = build_joined_item(weather_item, alert_item)
            joined_items.append(joined_item)

            logger.info(
                f"Joined {date} ({location}) — "
                f"disruption={joined_item['disruption']}"
            )

        logger.info(
            f"Join complete — {len(joined_items)} rows, "
            f"{matched_alert_count} matched alerts, "
            f"{unmatched_weather_count} unmatched"
        )

        # Step 3: Write results — composite PK is date + location
        batch_write_items(
            joined_table,
            joined_items,
            overwrite_by_pkeys=["date", "location"],
        )

        logger.info(f"Join job completed — {len(joined_items)} rows written")

    except Exception:
        logger.exception("Join job failed")
        raise


def run_join_for_date(
    date: str,
    weather_table=None,
    alerts_table=None,
    target_joined_table=None,
) -> None:
    logger.info(f"Running targeted join for date: {date}")

    wt = weather_table or weather_location_table
    at = alerts_table or alert_table
    jt = target_joined_table or joined_table

    try:
        weather_items_for_date = query_by_date(wt, date)

        if not weather_items_for_date:
            logger.warning(f"No weather records found for date: {date}")
            return

        alert_item = get_record(at, date)
        joined_items = [
            build_joined_item(weather_item, alert_item)
            for weather_item in weather_items_for_date
        ]

        batch_write_items(
            jt,
            joined_items,
            overwrite_by_pkeys=["date", "location"],
        )

        logger.info(
            f"Join complete for {date} - {len(joined_items)} rows written"
        )

    except Exception:
        logger.exception(f"Targeted join failed for date: {date}")
        raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    run_join()
