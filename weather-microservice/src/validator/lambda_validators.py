from datetime import datetime


def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except Exception:
        raise ValueError(f"Invalid date format: {date}. Expected YYYY-MM-DD")
