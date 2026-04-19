# transport-microservice/src/repositories/s3_repo.py


from src.dependencies.s3_client import ANALYSIS_BUCKET, s3_client


def read_untouched_file(s3_key: str) -> dict:
    """
    Return the raw S3 response object for a given key.
    """
    # Read the raw S3 object without decoding or parsing it.
    response = s3_client.get_object(Bucket=ANALYSIS_BUCKET, Key=s3_key)
    return response


def list_object_keys(prefix: str) -> list[str]:
    """
    List all object keys under a given S3 prefix.
    """
    keys = []

    # Call S3 to list objects that start with the supplied prefix.
    response = s3_client.list_objects_v2(
        Bucket=ANALYSIS_BUCKET,
        Prefix=prefix,
    )

    # Extract only the object keys from the S3 response.
    for obj in response.get("Contents", []):
        keys.append(obj["Key"])

    return keys


def write_csv_file(key: str, csv_content: str) -> None:
    """
    Write a CSV string to S3.

    Args:
        key: S3 object key, e.g. "cleaned/weather.csv"
        csv_content: Full CSV content as a string
    """
    s3_client.put_object(
        Bucket=ANALYSIS_BUCKET,
        Key=key,
        Body=csv_content.encode("utf-8"),
        ContentType="text/csv",
    )
