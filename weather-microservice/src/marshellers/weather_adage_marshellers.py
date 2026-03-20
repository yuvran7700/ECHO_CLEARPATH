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
                    "tempMin_C": record["tempMin_C"],
                    "tempMax_C": record["tempMax_C"],
                    "rainfall_mm": record["rainfall_mm"],
                    "sunshineHours_hours": record["sunshineHours_hours"],
                    "maxWindSpeed_kmh": record["maxWindSpeed_kmh"],
                    "9am": {
                        "temp_C": record["9am"]["temp"],
                        "humidity_percent": record["9am"]["humidity"],
                    },
                    "3pm": {
                        "temp_C": record["3pm"]["temp"],
                        "humidity_percent": record["3pm"]["humidity"],
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
