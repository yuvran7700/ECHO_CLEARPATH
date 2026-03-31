import json

import boto3

client = boto3.client("cloudwatch", region_name="us-east-1")

dashboards = [
    {
        "name": "clearpath-weather-dashboard-staging",
        "title": "ClearPath Weather Microservice - Staging",
        "functions": [
            "collection-lambda-staging",
            "raw-lambda-staging",
            "weather-lambda-staging",
            "adage-lambda-staging",
        ],
        "api_id": "18dydsthbi",
    },
    {
        "name": "clearpath-weather-dashboard-prod",
        "title": "ClearPath Weather Microservice - Production",
        "functions": [
            "collection-lambda-prod",
            "raw-lambda-prod",
            "weather-lambda-prod",
            "adage-lambda-prod",
        ],
        "api_id": "nv2ymlpynf",
    },
    {
        "name": "clearpath-alert-dashboard-staging",
        "title": "ClearPath Alert Microservice - Staging",
        "functions": [
            "classification-lambda-staging",
            "twitter-collection-lambda-staging",
        ],
        "api_id": "18dydsthbi",
    },
    {
        "name": "clearpath-alert-dashboard-prod",
        "title": "ClearPath Alert Microservice - Production",
        "functions": [
            "classification-lambda-prod",
            "twitter-collection-lambda-prod",
        ],
        "api_id": "nv2ymlpynf",
    },
]


def make_metric(title, metric_name, functions, stat="Sum"):
    metrics = [
        ["AWS/Lambda", metric_name, "FunctionName", fn] for fn in functions
    ]
    return {
        "type": "metric",
        "width": 8,
        "height": 6,
        "properties": {
            "title": title,
            "metrics": metrics,
            "period": 300,
            "stat": stat,
            "view": "timeSeries",
            "region": "us-east-1",
        },
    }


def make_apigw_metric(title, metric_name, api_id, stat="Sum"):
    return {
        "type": "metric",
        "width": 8,
        "height": 6,
        "properties": {
            "title": title,
            "metrics": [
                [
                    "AWS/ApiGateway",
                    metric_name,
                    "ApiId",
                    api_id,
                    "Stage",
                    "$default",
                ]
            ],
            "period": 300,
            "stat": stat,
            "view": "timeSeries",
            "region": "us-east-1",
        },
    }


def make_log_widget(title, functions):
    sources = " | ".join([f"SOURCE '/aws/lambda/{fn}'" for fn in functions])
    return {
        "type": "log",
        "width": 24,
        "height": 6,
        "properties": {
            "title": title,
            "query": (
                f"{sources} | fields @timestamp, @message"
                " | filter @message like /ERROR/"
                " | sort @timestamp desc | limit 20"
            ),
            "region": "us-east-1",
            "view": "table",
        },
    }


def make_all_logs_widget(title, functions):
    sources = " | ".join([f"SOURCE '/aws/lambda/{fn}'" for fn in functions])
    return {
        "type": "log",
        "width": 24,
        "height": 6,
        "properties": {
            "title": title,
            "query": (
                f"{sources} | fields @timestamp, @message"
                " | sort @timestamp desc | limit 50"
            ),
            "region": "us-east-1",
            "view": "table",
        },
    }


def build_dashboard(config):
    functions = config["functions"]
    api_id = config["api_id"]
    title = config["title"]

    widgets = [
        {
            "type": "text",
            "width": 24,
            "height": 1,
            "properties": {"markdown": f"# {title}"},
        },
        make_metric("Lambda Invocations", "Invocations", functions, "Sum"),
        make_metric("Lambda Errors", "Errors", functions, "Sum"),
        make_metric("Lambda Duration (ms)", "Duration", functions, "Average"),
        make_apigw_metric("API Gateway Requests", "Count", api_id, "Sum"),
        make_apigw_metric("API Gateway 4XX Errors", "4xx", api_id, "Sum"),
        make_apigw_metric("API Gateway 5XX Errors", "5xx", api_id, "Sum"),
        make_log_widget("Error Logs", functions),
        make_all_logs_widget("Recent Logs", functions),
    ]

    # assign x/y positions
    x = 0
    y = 0
    for i, widget in enumerate(widgets):
        widget["x"] = x
        widget["y"] = y
        width = widget.get("width", 8)
        x += width
        if x >= 24:
            x = 0
            y += widget.get("height", 6)

    return {"widgets": widgets}


for dashboard in dashboards:
    body = build_dashboard(dashboard)
    client.put_dashboard(
        DashboardName=dashboard["name"],
        DashboardBody=json.dumps(body),
    )
    print(f" Created: {dashboard['name']}")

print("\nAll dashboards created!")
print(
    "View at: "
    "https://us-east-1.console.aws.amazon.com/cloudwatch/home#dashboards"
)
