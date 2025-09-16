import boto3
import os

# 👇 env se read karo
CAREER_BUCKET = os.getenv("CAREER_S3_BUCKET", "mybucket")
CAREER_REGION = os.getenv("CAREER_AWS_REGION", "us-east-1")
CAREER_ACCESS_KEY = os.getenv("CAREER_AWS_ACCESS_KEY_ID", "test")
CAREER_SECRET_KEY = os.getenv("CAREER_AWS_SECRET_ACCESS_KEY", "test")
CAREER_ENDPOINT = os.getenv("CAREER_S3_ENDPOINT_URL", "http://localstack:4566")

s3 = boto3.client(
    "s3",
    region_name=CAREER_REGION,
    aws_access_key_id=CAREER_ACCESS_KEY,
    aws_secret_access_key=CAREER_SECRET_KEY,
    endpoint_url=CAREER_ENDPOINT
)

def init_s3():
    """Initialize Career S3 bucket if not exists"""
    existing_buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if CAREER_BUCKET not in existing_buckets:
        s3.create_bucket(Bucket=CAREER_BUCKET)
        print(f"✅ Career S3 bucket '{CAREER_BUCKET}' created.")
    else:
        print(f"✅ Career S3 bucket '{CAREER_BUCKET}' already exists.")

def upload_file(file_obj, filename, bucket_name: str = CAREER_BUCKET) -> str:
    """Upload file to Career S3 bucket and return URL"""
    try:
        s3.head_bucket(Bucket=bucket_name)
    except Exception:
        s3.create_bucket(Bucket=bucket_name)

    s3.upload_fileobj(file_obj, bucket_name, filename)
    # Localhost port jahan se tum LocalStack access karte ho:
    return f"http://localhost:4567/{bucket_name}/{filename}"
