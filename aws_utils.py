# aws_utils.py
import boto3
import os
from uuid import uuid4

# read env
CAREER_BUCKET = os.getenv("CAREER_S3_BUCKET", "mybucket")
CAREER_REGION = os.getenv("CAREER_AWS_REGION", "us-east-1")
CAREER_ACCESS_KEY = os.getenv("CAREER_AWS_ACCESS_KEY_ID", "test")
CAREER_SECRET_KEY = os.getenv("CAREER_AWS_SECRET_ACCESS_KEY", "test")
CAREER_ENDPOINT = os.getenv("CAREER_S3_ENDPOINT_URL", "http://localstack:4566")

# Career S3 client
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
        print(f" Career S3 bucket '{CAREER_BUCKET}' created.")
    else:
        print(f" Career S3 bucket '{CAREER_BUCKET}' already exists.")

def upload_fileobj(file_obj, filename: str = None, bucket_name: str = CAREER_BUCKET) -> str:
    """
    Upload file-like object to Career S3 bucket.
    Returns the key used so you can generate presigned URLs later.
    """
    # create unique key to avoid overwrite
    ext = ""
    if filename and "." in filename:
        ext = "." + filename.rsplit(".", 1)[1]
    key = f"{uuid4().hex}{ext}"

    try:
        s3.head_bucket(Bucket=bucket_name)
    except Exception:
        s3.create_bucket(Bucket=bucket_name)

    s3.upload_fileobj(file_obj, bucket_name, key)
    return key

def generate_presigned_url(key: str, expires_in: int = 3600, bucket_name: str = CAREER_BUCKET) -> str:
    """Generate presigned GET url for Career bucket"""
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=expires_in,
    )
