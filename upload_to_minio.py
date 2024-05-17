import argparse
import os
from functions import help_parser, config_client
from datetime import datetime
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error, InvalidResponseError


def upload_file_to_minio(client, bucket_name, file_path, object_name):
    try:
        client.fput_object(bucket_name, object_name, file_path)
        print(f"'{file_path}' is successfully uploaded as '{object_name}' to bucket '{bucket_name}'.")
    except InvalidResponseError as err:
        print(f"Invalid response error: {err}")
    except S3Error as err:
        print(f"Failed to upload '{file_path}' to '{bucket_name}/{object_name}': {err}")


def upload_directory_to_minio(client, bucket_name, directory_path, prefix=""):
    base_directory = os.path.basename(directory_path.rstrip('/'))
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            object_name = os.path.join(prefix, base_directory, os.path.relpath(file_path, directory_path)).replace("\\", "/")
            upload_file_to_minio(client, bucket_name, file_path, object_name)


def list_object_versions(client, bucket_name, object_name):
    try:
        versions = client.list_object_versions(bucket_name, prefix=object_name)
        version_list = []
        for version in versions:
            version_id = version.version_id
            last_modified = version.last_modified
            date_str = last_modified.strftime("%d/%m/%Y")
            version_list.append(version_id)
            print(f"Version ID: {version_id}, Last Modified: {date_str}, Is Latest: {version.is_latest}")
        return version_list
    except S3Error as err:
        print(f"Failed to list versions for '{object_name}' in bucket '{bucket_name}': {err}")
        return []


def download_object_version(client, bucket_name, object_name, version_id, download_path):
    try:
        client.fget_object(bucket_name, object_name, download_path, version_id=version_id)
        print(f"Version '{version_id}' of object '{object_name}' is successfully downloaded to '{download_path}'.")
    except S3Error as err:
        print(f"Failed to download version '{version_id}' of object '{object_name}' from bucket '{bucket_name}': {err}")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve MinIO configuration from environment variables
    server_url = os.getenv("SERVER_URL")
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")

    client = config_client(server_url=server_url, access_key=access_key, secret_key=secret_key)
    args = help_parser(parser=parser)

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
