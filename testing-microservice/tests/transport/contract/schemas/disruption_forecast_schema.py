DISRUPTION_FORECAST_SCHEMA = {
    "type": "object",
    "required": ["lat", "lon", "days"],
    "properties": {
        "lat": {"type": "number"},
        "lon": {"type": "number"},
        "days": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "date",
                    "weather_summary",
                    "tempSeverity",
                    "rainSeverity",
                    "windSeverity",
                    "humiditySeverity",
                    "sunSeverity",
                    "risk",
                    "risk_level",
                    "message",
                ],
                "properties": {
                    "date": {"type": "string", "format": "date"},
                    "weather_summary": {"type": "string"},
                    "tempSeverity": {"type": "string"},
                    "rainSeverity": {"type": "string"},
                    "windSeverity": {"type": "string"},
                    "humiditySeverity": {"type": "string"},
                    "sunSeverity": {"type": "string"},
                    "risk": {"type": "number"},
                    "risk_level": {
                        "type": "string",
                        "enum": [
                            "Low",
                            "Moderate",
                            "High",
                            "Very High",
                            "Unknown",
                        ],
                    },
                    "message": {"type": "string"},
                },
            },
        },
    },
}
