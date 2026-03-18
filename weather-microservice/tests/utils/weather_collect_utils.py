def generate_agage_same_weather(date):
    return {
        "data_source": "BOM",
        "dataset_type": "weather_sensor_data",
        "dataset_id": "s3://your-bucket-name/weather_collected/weather_event_test.json",
        "events": [
            {
                "event_type": "sensor_reading",
                "event_time": {
                    "time_stamp": date + "-12-12T09:00:00",
                    "duration": 0,
                    "duration_unit": "seconds",
                    "time_zone": "Australia/Sydney",
                },
                "event_attributes": {
                    "date": date,
                    "tempMin": 18.2,
                    "tempMax": 27.4,
                    "rainfall": 0.0,
                    "evaporation": 5.6,
                    "sunshineHours": 8.4,
                    "windGustDir": "NW",
                    "windGustSpeed": 35,
                    "windGustTime": "14:30",
                    "9am": {"temp": 21.3, "humidity": 64, "mslp": 1012.4},
                    "3pm": {"temp": 26.7, "humidity": 48, "mslp": 1009.8},
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
