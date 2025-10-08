import boto3
import os
from botocore.config import Config

s3 = boto3.client(
    's3',
    endpoint_url='https://s3.wasabisys.com',  # Wasabi region
    aws_access_key_id=os.getenv('WASABI_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('WASABI_SECRET_KEY'),
    config=Config(signature_version='s3v4')
)

def upload_video(video_path, bucket='your-bucket', key=f"videos/{os.path.basename(video_path)}"):
    s3.upload_file(video_path, bucket, key)
    return f"https://{bucket}.s3.wasabisys.com/{key}"