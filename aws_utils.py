import boto3
import os

# Load Career S3 config from environment variables
S3_ENDPOINT_URL = os.getenv("CAREER_S3_ENDPOINT_URL", "http://localstack:4566")
BUCKET_NAME = os.getenv("CAREER_S3_BUCKET", "my-career-bucket")
AWS_ACCESS_KEY_ID = os.getenv("CAREER_AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("CAREER_AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION = os.getenv("CAREER_AWS_REGION", "us-east-1")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def upload_file(file_path: str, key: str):
    """Upload local file to Career S3."""
    s3_client.upload_file(file_path, BUCKET_NAME, key)
    return f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/{key}"

def get_file_url(key: str) -> str:
    """Get public-like URL for file in Career S3."""
    return f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/{key}"

def init_s3():
    """Ensure the Career bucket exists; create if not."""
    existing_buckets = [b["Name"] for b in s3_client.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in existing_buckets:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"✅ Career S3 bucket '{BUCKET_NAME}' created.")
    else:
        print(f"✅ Career S3 bucket '{BUCKET_NAME}' already exists.")
