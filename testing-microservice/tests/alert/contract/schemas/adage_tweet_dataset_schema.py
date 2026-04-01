ADAGE_TWEET_DATASET_SCHEMA = {
    "type": "object",
    "required": [
        "data_source",
        "dataset_type",
        "dataset_id",
        "time_object",
        "events",
    ],
    "properties": {
        "data_source": {"type": "string"},
        "dataset_type": {"type": "string"},
        "dataset_id": {"type": "string"},
        "time_object": {
            "type": "object",
            "required": ["timestamp", "timezone"],
            "properties": {
                "timestamp": {"type": "string"},
                "timezone": {"type": "string"},
            },
        },
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["time_object", "event_type", "attribute"],
                "properties": {
                    "time_object": {
                        "type": "object",
                        "required": ["timestamp", "timezone"],
                        "properties": {
                            "timestamp": {"type": "string"},
                            "duration": {"type": "integer"},
                            "duration_unit": {"type": "string"},
                            "timezone": {"type": "string"},
                        },
                    },
                    "event_type": {"type": "string"},
                    "attribute": {
                        "type": "object",
                        "properties": {
                            "account_name": {"type": "string"},
                            "text": {"type": "string"},
                            "date": {"type": "string", "format": "date"},
                        },
                    },
                },
            },
        },
    },
}
