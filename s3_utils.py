# s3_utils.py
import boto3
import os
from uuid import uuid4

# Load Blogs S3 config from environment variables
S3_ENDPOINT_URL = os.getenv("BLOGS_S3_ENDPOINT_URL", "http://localstack:4566")
BUCKET_NAME = os.getenv("BLOGS_S3_BUCKET", "my-bucket")
AWS_ACCESS_KEY_ID = os.getenv("BLOGS_AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("BLOGS_AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION = os.getenv("BLOGS_AWS_DEFAULT_REGION", "us-east-1")

# Initialize S3 client for Blogs
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def init_blogs_s3():
    """Ensure the Blogs bucket exists; create if not."""
    existing_buckets = [b["Name"] for b in s3_client.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in existing_buckets:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"Blogs S3 bucket '{BUCKET_NAME}' created.")
    else:
        print(f"Blogs S3 bucket '{BUCKET_NAME}' already exists.")

def upload_fileobj(file_obj, key: str = None) -> str:
    """
    Upload file-like object to Blogs S3 bucket.
    Returns the key used (not full url). Use generate_presigned_url for access.
    """
    if not key:
        key = f"{uuid4().hex}"
    # Ensure bucket exists (Localstack may require create)
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except Exception:
        s3_client.create_bucket(Bucket=BUCKET_NAME)

    s3_client.upload_fileobj(file_obj, BUCKET_NAME, key)
    return key

def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """Generate presigned GET URL for the blogs bucket."""
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in,
    )

def get_file_url(key: str) -> str:
    """Generate public-like URL for a file in Blogs S3 bucket (non-presigned)."""
    return f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/{key}"
