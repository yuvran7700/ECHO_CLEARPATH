def format_raw_adage(record: dict, date):
    return {
        "data_source": "BOM",
        "dataset_type": "Daily weather observations",
        "dataset_id": f"s3://clearpath-weather-index/weather_collected/{date}.json",
        "events": [
            {
                "event_type": "Daily weather observations",
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
                    "evaporation_mm": record["evaporation_mm"],
                    "sunshineHours_hours": record["sunshineHours_hours"],
                    "windWindDir": record["maxWindDir"],
                    "maxWindSpeed_kmh": record["maxWindSpeed_kmh"],
                    "maxWindTime": record["maxWindTime"],
                    "9am": {
                        "temp_C": record["amTemp_C"],
                        "humidity_percent": record["amHumidity_percent"],
                        "cloudAmount_oktas": record["amCloud_oktas"],
                        "windDirection": record["amWindDir"],
                        "windSpeed_kmh": record["amWindSpeed_kmh"],
                        "mslp_hPa": record["amPressure_hPa"],
                    },
                    "3pm": {
                        "temp_C": record["pmTemp_C"],
                        "humidity_percent": record["pmHumidity_percent"],
                        "cloudAmount_oktas": record["pmCloud_oktas"],
                        "windDirection": record["pmWindDir"],
                        "windSpeed_kmh": record["pmWindSpeed_kmh"],
                        "mslp_hPa": record["pmPressure_hPa"],
                    },
                },
            }
        ],
    }
