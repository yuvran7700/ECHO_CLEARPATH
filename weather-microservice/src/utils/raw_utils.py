import csv
import logging
from io import StringIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def find_row(csv_content):
    lines = csv_content.splitlines()
    for i, row in enumerate(lines):
        potential = row.strip().lstrip(",")
        if "Date" in potential and "Minimum temperature" in potential:
            index = i
            break

    if index is None:
        raise ValueError("Could not find CSV header row")

    cleaned_rows = []
    for j, row in enumerate(lines[index:]):
        stripped = row.strip()
        if not stripped:
            continue

        cleaned_rows.append(stripped.lstrip(","))

    cleaned_csv = "\n".join(cleaned_rows)
    return csv.DictReader(StringIO(cleaned_csv))
