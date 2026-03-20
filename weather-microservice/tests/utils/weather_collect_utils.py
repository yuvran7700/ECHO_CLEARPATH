def generate_agage_same_weather():
    return {
        "data_source": "ClearPath",
        "dataset_type": "Weather observations and severity",
        "dataset_id": "dynamodb://clearpath-weather-data/3999-12-12",
        "events": [
            {
                "event_type": "Weather observations and severity",
                "event_time": {
                    "time_stamp": "3999-12-12T09:00:00",
                    "duration": 86400,
                    "duration_unit": "seconds",
                    "time_zone": "Australia/Sydney",
                },
                "event_attributes": {
                    "date": "3999-12-12",
                    "tempMin_C": 18.2,
                    "tempMax_C": 27.4,
                    "rainfall_mm": 0.0,
                    "sunshineHours_hours": 8.4,
                    "maxWindSpeed_kmh": 35.0,
                    "9am": {"temp": 21.3, "humidity": 64.0},
                    "3pm": {"temp": 26.7, "humidity": 48.0},
                    "weatherSeverity": {
                        "sunSeverity": "Sunny",
                        "rainSeverity": "No rain",
                        "tempSeverity": "Warm",
                        "windSeverity": "Breezy",
                        "humiditySeverity": "Moderate Humidity",
                    },
                },
            }
        ],
    }


def generate_trig_event(event_name, bucket_name, key, eTag):
    return {
        "Records": [
            {
                "eventSource": "aws:s3",
                "eventName": event_name,
                "s3": {
                    "bucket": {"name": bucket_name},
                    "object": {"key": key, "eTag": eTag},
                },
            }
        ]
    }


def generate_weather_query(date):
    return {"queryStringParameters": {"date": date}}
