import datetime


def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except Exception:
        return False
