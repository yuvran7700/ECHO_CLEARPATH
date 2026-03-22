from src.utils.weather_utils import FIELD_MAP, get_date, safe_value


def extract_attributes(row):
    result = {}

    try:
        date = get_date(row)
    except Exception:
        raise Exception(f"Invalid date input: {row['Date']}")

    for key, value in row.items():
        key = key.strip()
        value = value.strip()

        if key == "Date":
            result["date"] = date
            continue

        clean_key = FIELD_MAP.get(key)
        if not clean_key:
            continue

        result[clean_key] = safe_value(value, clean_key)

    return result
