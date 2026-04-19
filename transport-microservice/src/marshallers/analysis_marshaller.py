# transport-microservice/src/marshallers/analysis_marshaller.py

FIELDNAMES = [
    "date",
    "tempMax_C",
    "9am_temp_C",
    "9am_humidity_percent",
    "eTag",
    "maxWindSpeed_kmh",
    "3pm_humidity_percent",
    "s3URL",
    "3pm_temp_C",
    "tempMin_C",
    "sunshineHours_hours",
    "sunSeverity",  # severity feilds
    "rainSeverity",
    "rainfall_mm",
    "humiditySeverity",
    "windSeverity",
    "tempSeverity",
    "account_name",  # alert fields
    "classification",
    "disruption",
]


def normalise_record(record: dict) -> dict:
    """
    Ensure every record has the SAME schema and column order.

    - Missing fields → filled with None
    - Extra fields → ignored
    - Order → matches FIELDNAMES exactly
    """
    return {field: record.get(field, None) for field in FIELDNAMES}
