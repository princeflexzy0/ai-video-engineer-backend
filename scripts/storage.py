import os
import boto3
from botocore.exceptions import ClientError

def upload_to_wasabi(file_path, object_name=None):
    """Uploads file to Wasabi S3 storage"""
    try:
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        s3_client = boto3.client(
            's3',
            endpoint_url='https://s3.us-east-1.wasabisys.com',
            aws_access_key_id=os.getenv('WASABI_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('WASABI_SECRET_KEY'),
            region_name=os.getenv('WASABI_REGION', 'us-east-1')
        )
        
        bucket_name = os.getenv('WASABI_BUCKET_NAME')
        
        s3_client.upload_file(
            file_path,
            bucket_name,
            object_name,
            ExtraArgs={'ACL': 'public-read'}
        )
        
        url = f"https://{bucket_name}.s3.us-east-1.wasabisys.com/{object_name}"
        
        print(f"✅ Uploaded to Wasabi: {url}")
        return url
        
    except ClientError as e:
        print(f"❌ Error uploading to Wasabi: {str(e)}")
        raise Exception(f"Wasabi upload failed: {str(e)}")
