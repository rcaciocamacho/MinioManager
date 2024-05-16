import argparse
import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

def upload_file_to_minio(server_url, access_key, secret_key, bucket_name, file_path, object_name):
    
    # Initialize the Minio client
    client = Minio(
        server_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # Set to True if using HTTPS
    )
    
    # Check if the bucket exists
    found = client.bucket_exists(bucket_name)
    if not found:
        print(f"Bucket '{bucket_name}' does not exist.")
        print("Listing existing buckets:")
        buckets = client.list_buckets()
        for bucket in buckets:
            print(bucket.name)
        return
    
    # Upload the file
    try:
        client.fput_object(bucket_name, object_name, file_path)
        print(f"'{file_path}' is successfully uploaded as '{object_name}' to bucket '{bucket_name}'.")
    except S3Error as err:
        print(f"Failed to upload '{file_path}' to '{bucket_name}/{object_name}': {err}")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve MinIO configuration from environment variables
    server_url = os.getenv("SERVER_URL")
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")

    if not server_url or not access_key or not secret_key:
        print("Error: Missing MinIO configuration in .env file.")
        exit(1)

    # Setup argument parser
    parser = argparse.ArgumentParser(description="Upload a file to MinIO Object Store.")
    parser.add_argument("bucket_name", help="Bucket name in MinIO")
    parser.add_argument("file_path", help="Path to the file to be uploaded")
    parser.add_argument("object_name", help="Object name in MinIO")

    args = parser.parse_args()

    upload_file_to_minio(
        server_url=server_url,
        access_key=access_key,
        secret_key=secret_key,
        bucket_name=args.bucket_name,
        file_path=args.file_path,
        object_name=args.object_name
    )
