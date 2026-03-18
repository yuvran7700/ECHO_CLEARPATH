def format_db_adage(record: dict, date):
    formatted = {
        "data_source": "ClearPath",
        "dataset_type": "Weather observations and severity",
        "dataset_id": "dynamodb://clearpath-weather-data/" + date,
        "events": [
            {
                "event_type": "Weather observations and severity",
                "event_time": {
                    "time_stamp": date + "T09:00:00",
                    "duration": 86400,
                    "duration_unit": "seconds",
                    "time_zone": "Australia/Sydney",
                },
                "event_attributes": {
                    "date": date,
                    "tempMin": record["tempMin"],
                    "tempMax": record["tempMax"],
                    "rainfall": record["rainfall"],
                    "sunshineHours": record["sunshineHours"],
                    "windGustSpeed": record["windGustSpeed"],
                    "9am": {
                        "temp": record["9am"]["temp"],
                        "humidity": record["9am"]["humidity"],
                    },
                    "3pm": {
                        "temp": record["3pm"]["temp"],
                        "humidity": record["3pm"]["humidity"],
                    },
                    "weatherSeverity": {
                        "sunSeverity": record["weatherSeverity"][
                            "sunSeverity"
                        ],
                        "rainSeverity": record["weatherSeverity"][
                            "rainSeverity"
                        ],
                        "tempSeverity": record["weatherSeverity"][
                            "tempSeverity"
                        ],
                        "windSeverity": record["weatherSeverity"][
                            "windSeverity"
                        ],
                        "humiditySeverity": record["weatherSeverity"][
                            "humiditySeverity"
                        ],
                    },
                },
            }
        ],
    }

    return formatted
