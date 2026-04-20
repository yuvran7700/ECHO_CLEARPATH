DISRUPTION_ANALYTICS_SCHEMA = {
    "type": "object",
    "required": [
        "location",
        "overall",
        "best_worst_day_of_week",
        "best_worst_month",
        "weather_threshold_analysis",
    ],
    "properties": {
        "location": {"type": "string"},
        "overall": {
            "type": "object",
            "required": [
                "total_days",
                "total_disruption_days",
                "overall_disruption_rate",
                "data_from",
                "data_to",
            ],
            "properties": {
                "total_days": {"type": "integer"},
                "total_disruption_days": {"type": "integer"},
                "overall_disruption_rate": {"type": "number"},
                "data_from": {"type": "string"},
                "data_to": {"type": "string"},
            },
        },
        "best_worst_day_of_week": {
            "type": "object",
            "required": ["all_time"],
            "properties": {
                "all_time": {
                    "type": "object",
                    "required": ["by_day", "best", "worst"],
                    "properties": {
                        "by_day": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "label",
                                    "disruption_rate",
                                    "sample_size",
                                    "disruption_days",
                                    "non_disruption_days",
                                ],
                                "properties": {
                                    "label": {"type": "string"},
                                    "disruption_rate": {"type": "number"},
                                    "sample_size": {"type": "integer"},
                                    "disruption_days": {"type": "integer"},
                                    "non_disruption_days": {"type": "integer"},
                                },
                            },
                        },
                        "best": {"type": "string"},
                        "worst": {"type": "string"},
                    },
                },
            },
        },
        "best_worst_month": {
            "type": "object",
            "required": ["all_time"],
            "properties": {
                "all_time": {
                    "type": "object",
                    "required": ["by_month", "best", "worst"],
                    "properties": {
                        "by_month": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "label",
                                    "disruption_rate",
                                    "sample_size",
                                    "disruption_days",
                                    "non_disruption_days",
                                ],
                                "properties": {
                                    "label": {"type": "string"},
                                    "disruption_rate": {"type": "number"},
                                    "sample_size": {"type": "integer"},
                                    "disruption_days": {"type": "integer"},
                                    "non_disruption_days": {"type": "integer"},
                                },
                            },
                        },
                        "best": {"type": "string"},
                        "worst": {"type": "string"},
                    },
                },
            },
        },
        "weather_threshold_analysis": {
            "type": "object",
            "required": ["temperature", "wind", "rainfall"],
            "properties": {
                "temperature": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "threshold_c",
                            "disruption_rate",
                            "sample_size",
                            "disruption_days",
                        ],
                        "properties": {
                            "threshold_c": {"type": "number"},
                            "disruption_rate": {"type": "number"},
                            "sample_size": {"type": "integer"},
                            "disruption_days": {"type": "integer"},
                        },
                    },
                },
                "wind": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "threshold_kmh",
                            "disruption_rate",
                            "sample_size",
                            "disruption_days",
                        ],
                        "properties": {
                            "threshold_kmh": {"type": "number"},
                            "disruption_rate": {"type": "number"},
                            "sample_size": {"type": "integer"},
                            "disruption_days": {"type": "integer"},
                        },
                    },
                },
                "rainfall": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "threshold_mm",
                            "disruption_rate",
                            "sample_size",
                            "disruption_days",
                        ],
                        "properties": {
                            "threshold_mm": {"type": "number"},
                            "disruption_rate": {"type": "number"},
                            "sample_size": {"type": "integer"},
                            "disruption_days": {"type": "integer"},
                        },
                    },
                },
            },
        },
    },
}
