from datetime import datetime
from decimal import Decimal

FIELD_MAP = {
    "Minimum temperature (°C)": "tempMin_C",
    "Maximum temperature (°C)": "tempMax_C",
    "Rainfall (mm)": "rainfall_mm",
    "Evaporation (mm)": "evaporation_mm",
    "Sunshine (hours)": "sunshineHours_hours",
    "Direction of maximum wind gust": "maxWindDir",
    "Speed of maximum wind gust (km/h)": "maxWindSpeed_kmh",
    "Time of maximum wind gust": "maxWindTime",
    "9am Temperature (°C)": "amTemp_C",
    "9am relative humidity (%)": "amHumidity_percent",
    "9am cloud amount (oktas)": "amCloud_oktas",
    "9am wind direction": "amWindDir",
    "9am wind speed (km/h)": "amWindSpeed_kmh",
    "9am MSL pressure (hPa)": "amPressure_hPa",
    "3pm Temperature (°C)": "pmTemp_C",
    "3pm relative humidity (%)": "pmHumidity_percent",
    "3pm cloud amount (oktas)": "pmCloud_oktas",
    "3pm wind direction": "pmWindDir",
    "3pm wind speed (km/h)": "pmWindSpeed_kmh",
    "3pm MSL pressure (hPa)": "pmPressure_hPa",
}


def temperature_classification(
    tempMin_C: int, tempMax_C: int, amTemp_C: int, pmTemp_C: int
):
    temps = [tempMin_C, tempMax_C, amTemp_C, pmTemp_C]
    valid_temps = [t for t in temps if t != "Unavailable"]

    if not valid_temps:
        return "N/A"

    avgTemp = sum(valid_temps) / len(valid_temps)

    if avgTemp < 15:
        return "Cold"
    elif avgTemp < 22:
        return "Mild"
    elif avgTemp < 30:
        return "Warm"
    else:
        return "Hot"


def rainfall_classification(rainfall_mm: int):
    if rainfall_mm == "Unavailable":
        return "N/A"

    if rainfall_mm == 0.0:
        return "No rain"
    elif rainfall_mm < 10:
        return "Light rain"
    elif rainfall_mm < 25:
        return "Moderate rain"
    else:
        return "Heavy rain"


def sunshine_classification(sunshineHours_hours: int):
    if sunshineHours_hours == "Unavailable":
        return "N/A"

    sun_ratio = sunshineHours_hours / 12
    if sun_ratio < 0.2:
        return "Cloudy"
    elif sun_ratio <= 0.7:
        return "Partly Cloudy"
    else:
        return "Sunny"


def wind_classification(maxWindSpeed_kmh: int):
    if maxWindSpeed_kmh == "Unavailable":
        return "N/A"

    if maxWindSpeed_kmh < 20:
        return "Calm"
    elif maxWindSpeed_kmh < 38:
        return "Breezy"
    elif maxWindSpeed_kmh < 61:
        return "Windy"
    else:
        return "Gale"


def humidity_classification(amHumidity_percent: int, pmHumidity_percent: int):
    hums = [amHumidity_percent, pmHumidity_percent]
    valid_hums = [h for h in hums if h != "Unavailable"]

    if not valid_hums:
        return "N/A"

    avgHumidity = sum(valid_hums) / len(valid_hums)

    if avgHumidity <= 30:
        return "Low Humidity"
    elif avgHumidity <= 60:
        return "Moderate Humidity"
    elif avgHumidity <= 80:
        return "High Humidity"
    else:
        return "Extreme Humidity"


def decimal_converter(x):
    if isinstance(x, Decimal):
        return float(x)


def dynamodb_converter(x):
    if x == "Unavailable":
        return "Unavailable"
    return Decimal(str(x))


def format_date(date):
    try:
        date_split = date.split("/")
        date_split.reverse()
        date_res = "-".join(date_split)
        return date_res
    except ValueError:
        return None


def get_date(row):
    raw_date = row["Date"]
    if raw_date is None:
        raise KeyError("Missing Date column")
    date = format_date(raw_date)
    if date is None:
        raise ValueError(f"Invalid date format: {raw_date}")

    return date


def safe_value(value, field_name):
    str_expected = ["maxWindDir", "maxWindTime", "amWindDir", "pmWindDir"]
    wind_directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]

    if value is None:
        return "Unavailable"

    value = str(value).strip()
    if value == "":
        return "Unavailable"

    if field_name == "maxWindTime":
        try:
            datetime.strptime(value, "%H:%M")
            return value
        except ValueError:
            raise ValueError(f"Invalid time value for {field_name}: {value}")

    if field_name not in str_expected:
        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"Invalid numeric value for {field_name}: {value}"
            )
    else:
        if value not in wind_directions:
            return "Unavailable"
        return value
