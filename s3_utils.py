import boto3
import os

# S3 client config with env vars (default values provided)
s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://localstack:4566"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)

BUCKET_NAME = os.getenv("S3_BUCKET", "my-bucket")


def upload_file(file_path: str, key: str):
    """Upload local file to S3"""
    s3_client.upload_file(file_path, BUCKET_NAME, key)
    return f"{os.getenv('S3_ENDPOINT_URL', 'http://localstack:4566')}/{BUCKET_NAME}/{key}"


def get_file_url(key: str) -> str:
    """Get public-like URL for file in S3"""
    return f"{os.getenv('S3_ENDPOINT_URL', 'http://localstack:4566')}/{BUCKET_NAME}/{key}"
