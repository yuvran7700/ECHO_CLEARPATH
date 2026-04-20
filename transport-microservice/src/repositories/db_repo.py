"""
transport-microservice/src/repositories/db_repo.py
Reusable DynamoDB table operations.

These helper functions work with any DynamoDB table object passed in,
such as alert_table or weather_table.
"""

from typing import Any


def get_record(
    table, date: str, location: str | None = None
) -> dict[str, Any] | None:
    key = {"date": date}
    if location:
        key["location"] = location
    response = table.get_item(Key=key)
    return response.get("Item")


def put_record(table, record: dict[str, Any]) -> None:
    table.put_item(Item=record)


def update_record(
    table, date: str, updates: dict[str, Any], location: str | None = None
) -> None:
    if not updates:
        raise ValueError("updates cannot be empty")

    key = {"date": date}
    if location:
        key["location"] = location

    update_expression = "SET " + ", ".join(
        f"#k{i} = :v{i}" for i in range(len(updates))
    )
    expression_names = {f"#k{i}": key for i, key in enumerate(updates.keys())}
    expression_values = {
        f":v{i}": value for i, value in enumerate(updates.values())
    }

    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=expression_values,
    )


def delete_record(table, date: str, location: str | None = None) -> None:
    key = {"date": date}
    if location:
        key["location"] = location
    table.delete_item(Key=key)


def scan_all_items(table) -> list[dict[str, Any]]:
    """
    Scan and return all items from a DynamoDB table.
    """
    items: list[dict[str, Any]] = []

    response = table.scan()
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    return items


def batch_write_items(
    table,
    items: list[dict[str, Any]],
    overwrite_by_pkeys: list[str] | None = None,
) -> None:
    """
    Batch write items to a DynamoDB table.

    Args:
        table: A boto3 DynamoDB Table resource.
        items: List of items to write.
        overwrite_by_pkeys: Primary key fields used to overwrite existing
            items during batch writing instead of creating duplicates.
    """
    if not items:
        return

    batch_kwargs = {}
    if overwrite_by_pkeys:
        batch_kwargs["overwrite_by_pkeys"] = overwrite_by_pkeys

    with table.batch_writer(**batch_kwargs) as batch:
        for item in items:
            batch.put_item(Item=item)


def query_by_date(table, date: str) -> list[dict[str, Any]]:
    """
    Query all items with a given date partition key.
    Returns all records for that date (e.g. all locations).
    """
    response = table.query(
        KeyConditionExpression="#d = :date",
        ExpressionAttributeNames={"#d": "date"},
        ExpressionAttributeValues={":date": date},
    )
    return response.get("Items", [])
