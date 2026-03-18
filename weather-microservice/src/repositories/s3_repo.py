import json

from src.dependencies.s3_client import S3_BUCKET_NAME, s3_client


def read_file(s3_key: str) -> dict:
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
    content = response["Body"].read().decode("utf-8")
    return json.loads(content)


def write_file(s3_key: str, data: dict) -> str:
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
    )
    return f"s3://{S3_BUCKET_NAME}/{s3_key}"


def delete_file(s3_key: str):
    s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)


def get_etag(s3_key: str):
    return s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_key)[
        "ETag"
    ].strip('"')
