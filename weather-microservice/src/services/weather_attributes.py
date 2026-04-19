from src.repositories.db_repo import put_record
from src.repositories.s3_repo import read_file
from src.utils.weather_utils import (
    dynamodb_converter,
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
    tempMin_C = attri["tempMin_C"]
    tempMax_C = attri["tempMax_C"]
    rainfall_mm = attri["rainfall_mm"]
    sunshineHours_hours = attri["sunshineHours_hours"]
    maxWindSpeed_kmh = attri["maxWindSpeed_kmh"]
    amTemp_C = attri["9am"]["temp_C"]
    amHumidity_percent = attri["9am"]["humidity_percent"]
    pmTemp_C = attri["3pm"]["temp_C"]
    pmHumidity_percent = attri["3pm"]["humidity_percent"]

    temp_severity = temperature_classification(
        tempMin_C, tempMax_C, amTemp_C, pmTemp_C
    )
    rain_severity = rainfall_classification(rainfall_mm)
    sunshine_severity = sunshine_classification(sunshineHours_hours)
    wind_severity = wind_classification(maxWindSpeed_kmh)
    humidity_severity = humidity_classification(
        amHumidity_percent, pmHumidity_percent
    )

    Item = {
        "date": date,
        "eTag": eTag,
        "s3URL": f"s3://clearpath-weather-index-v1/weather_collected/{date}.json",
        "tempMin_C": dynamodb_converter(tempMin_C),
        "tempMax_C": dynamodb_converter(tempMax_C),
        "rainfall_mm": dynamodb_converter(rainfall_mm),
        "sunshineHours_hours": dynamodb_converter(sunshineHours_hours),
        "maxWindSpeed_kmh": dynamodb_converter(maxWindSpeed_kmh),
        "9am": {
            "temp_C": dynamodb_converter(amTemp_C),
            "humidity_percent": dynamodb_converter(amHumidity_percent),
        },
        "3pm": {
            "temp_C": dynamodb_converter(pmTemp_C),
            "humidity_percent": dynamodb_converter(pmHumidity_percent),
        },
        "weatherSeverity": {
            "tempSeverity": str(temp_severity),
            "rainSeverity": str(rain_severity),
            "sunSeverity": str(sunshine_severity),
            "windSeverity": str(wind_severity),
            "humiditySeverity": str(humidity_severity),
        },
    }

    put_record(Item)
