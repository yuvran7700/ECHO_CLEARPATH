ADAGE_WEATHER_RECORD_SCHEMA = {
    "type": "object",
    "required": [
        "data_source",
        "dataset_type",
        "dataset_id",
        "events",
    ],
    "properties": {
        "data_source": {"type": "string"},
        "dataset_type": {"type": "string"},
        "dataset_id": {"type": "string"},
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["event_type", "event_time", "event_attributes"],
                "properties": {
                    "event_type": {"type": "string"},
                    "event_time": {
                        "type": "object",
                        "required": [
                            "time_stamp",
                            "duration",
                            "duration_unit",
                            "time_zone",
                        ],
                        "properties": {
                            "time_stamp": {"type": "string"},
                            "duration": {"type": "integer"},
                            "duration_unit": {"type": "string"},
                            "time_zone": {"type": "string"},
                        },
                    },
                    "event_attributes": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "tempMin_C": {
                                "oneOf": [
                                    {"type": "number", "format": "float"},
                                    {"type": "string"},
                                ]
                            },
                            "tempMax_C": {
                                "oneOf": [
                                    {"type": "number", "format": "float"},
                                    {"type": "string"},
                                ]
                            },
                            "rainfall_mm": {
                                "oneOf": [
                                    {"type": "number", "format": "float"},
                                    {"type": "string"},
                                ]
                            },
                            "evaporation_mm": {
                                "oneOf": [
                                    {"type": "number", "format": "float"},
                                    {"type": "string"},
                                ]
                            },
                            "sunshineHours_hours": {
                                "oneOf": [
                                    {"type": "number", "format": "float"},
                                    {"type": "string"},
                                ]
                            },
                            "windWindDir": {"type": "string"},
                            "maxWindSpeed_kmh": {
                                "oneOf": [
                                    {"type": "number", "format": "float"},
                                    {"type": "string"},
                                ]
                            },
                            "maxWindTime": {"type": "string"},
                            "9am": {
                                "type": "object",
                                "properties": {
                                    "temp_C": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "humidity_percent": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "cloudAmount_oktas": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "windDirection": {"type": "string"},
                                    "windSpeed_kmh": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "mslp_hPa": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                },
                            },
                            "3pm": {
                                "type": "object",
                                "properties": {
                                    "temp_C": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "humidity_percent": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "cloudAmount_oktas": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "windDirection": {"type": "string"},
                                    "windSpeed_kmh": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                    "mslp_hPa": {
                                        "oneOf": [
                                            {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            {"type": "string"},
                                        ]
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
