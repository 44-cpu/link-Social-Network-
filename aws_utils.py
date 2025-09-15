import boto3
import os

# 👇 Default S3 client that points to LocalStack
s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    endpoint_url="http://localstack:4566"  # container name + port inside Docker
)


def init_s3():
    """
    Return a boto3 S3 client configured for LocalStack.
    Use this in other parts of your app instead of re-configuring.
    """
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        endpoint_url="http://localstack:4566",
    )


def upload_file(file_obj, filename, bucket_name: str = "mybucket") -> str:
    """
    Upload a file object to S3 (LocalStack) and return the public URL.
    """
    # Make sure bucket exists
    try:
        s3.head_bucket(Bucket=bucket_name)
    except Exception:
        s3.create_bucket(Bucket=bucket_name)

    # Upload the file
    s3.upload_fileobj(file_obj, bucket_name, filename)

    # Return the URL accessible from host machine
    return f"http://localhost:4567/{bucket_name}/{filename}"
