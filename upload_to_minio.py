import argparse
import os
from functions import help_parser, config_client,upload_file_to_minio, upload_directory_to_minio, list_object_versions, download_object_version
from datetime import datetime
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error, InvalidResponseError

# Load environment variables from .env file
load_dotenv()

# Retrieve MinIO configuration from environment variables
server_url = os.getenv("SERVER_URL")
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")

client = config_client(server_url=server_url, access_key=access_key, secret_key=secret_key)
args = help_parser(parser=argparse)

# Check if the bucket exists
try:
    found = client.bucket_exists(args.bucket_name)
    if not found:
        print(f"Bucket '{args.bucket_name}' does not exist.")
        print("Listing existing buckets:")
        buckets = client.list_buckets()
        for bucket in buckets:
            print(bucket.name)
        exit(1)

    if args.download:
        if not args.object_name:
            print("Error: --object_name must be specified in download mode.")
            exit(1)
        if args.version_id:
            download_object_version(client, args.bucket_name, args.object_name, args.version_id, args.file_path)
        else:
            print(f"Listing versions for object '{args.object_name}' in bucket '{args.bucket_name}':")
            version_list = list_object_versions(client, args.bucket_name, args.object_name)
            if version_list:
                print("Please specify the version ID to download using --version_id.")
    else:
        if os.path.isdir(args.file_path):
            upload_directory_to_minio(client, args.bucket_name, args.file_path, args.prefix)
        else:
            upload_file_to_minio(client, args.bucket_name, args.file_path, args.prefix or os.path.basename(args.file_path))

except InvalidResponseError as err:
    print(f"Invalid response error: {err}")
except S3Error as err:
    print(f"Failed to process request for bucket '{args.bucket_name}': {err}")
