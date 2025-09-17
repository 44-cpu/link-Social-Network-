import boto3
import os

# Load Blogs S3 config from environment variables
S3_ENDPOINT_URL = os.getenv("BLOGS_S3_ENDPOINT_URL", "http://localstack:4566")
BUCKET_NAME = os.getenv("BLOGS_S3_BUCKET", "my-bucket")
AWS_ACCESS_KEY_ID = os.getenv("BLOGS_AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("BLOGS_AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION = os.getenv("BLOGS_AWS_DEFAULT_REGION", "us-east-1")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def upload_file_to_s3(file_path: str, key: str) -> str:
    """Upload a local file to Blogs S3 bucket."""
    s3_client.upload_file(file_path, BUCKET_NAME, key)
    return f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/{key}"

def get_file_url(key: str) -> str:
    """Generate public-like URL for a file in Blogs S3 bucket."""
    return f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/{key}"

def init_blogs_s3():
    """Ensure the Blogs bucket exists; create if not."""
    existing_buckets = [b["Name"] for b in s3_client.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in existing_buckets:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"Blogs S3 bucket '{BUCKET_NAME}' created.")
    else:
        print(f"Blogs S3 bucket '{BUCKET_NAME}' already exists.")
