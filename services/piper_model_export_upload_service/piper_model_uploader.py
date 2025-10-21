import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()


class PiperModelUploader:
    def __init__(self):
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client(
            's3',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

    def upload_zip(self, zip_file_path):
        zip_path = Path(zip_file_path)
        if not zip_path.exists():
            raise FileNotFoundError(f"File {zip_file_path} not found.")

        s3_key = zip_path.name

        try:
            self.s3_client.upload_file(str(zip_path), self.bucket_name, s3_key)
            print(f"✅ Successfully uploaded: {zip_path.name} → s3://{self.bucket_name}/{s3_key}")
        except ClientError as e:
            print(f"❌ Failed to upload: {e}")


