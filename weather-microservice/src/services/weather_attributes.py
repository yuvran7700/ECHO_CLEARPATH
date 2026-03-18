from decimal import Decimal

from src.repositories.db_repo import put_record
from src.repositories.s3_repo import read_file
from src.utils.weather_utils import (
    humidity_classification,
    rainfall_classification,
    sunshine_classification,
    temperature_classification,
    wind_classification,
)


def process_collected_s3_object(key: str, eTag: str):
    content = read_file(key)
    attri = content["events"][0]["event_attributes"]

    date = attri["date"]
    tempMin = attri["tempMin"]
    tempMax = attri["tempMax"]
    rainfall = attri["rainfall"]
    sunshineHours = attri["sunshineHours"]
    windGustSpeed = attri["windGustSpeed"]
    amTemp = attri["temp"]
    amHumidity = attri["humidity"]
    pmTemp = attri["temp"]
    pmHumidity = attri["humidity"]

    temp_severity = temperature_classification(
        tempMin, tempMax, amTemp, pmTemp
    )
    rain_severity = rainfall_classification(rainfall)
    sunshine_severity = sunshine_classification(sunshineHours)
    wind_severity = wind_classification(windGustSpeed)
    humidity_severity = humidity_classification(amHumidity, pmHumidity)

    Item = {
        "Date": date,
        "eTag": eTag,
        "tempMin": Decimal(str(tempMin)),
        "tempMax": Decimal(str(tempMax)),
        "rainfall": Decimal(str(rainfall)),
        "sunshineHours": Decimal(str(sunshineHours)),
        "windGustSpeed": Decimal(str(windGustSpeed)),
        "9am": {
            "temp": Decimal(str(amTemp)),
            "humidity": Decimal(str(amHumidity)),
        },
        "3pm": {
            "temp": Decimal(str(pmTemp)),
            "humidity": Decimal(str(pmHumidity)),
        },
        "Weather_Severity": {
            "Temp_Severity": str(temp_severity),
            "Rain_Severity": str(rain_severity),
            "Sun_Severity": str(sunshine_severity),
            "Wind_Severity": str(wind_severity),
            "Humidity_Severity": str(humidity_severity),
        },
    }

    put_record(Item)
