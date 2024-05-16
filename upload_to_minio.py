import argparse
import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error, InvalidResponseError


def upload_file_to_minio(client, bucket_name, file_path, object_name):
    try:
        client.fput_object(bucket_name, object_name, file_path)
        print(
            f"'{file_path}' is successfully uploaded as '{object_name}' to bucket '{bucket_name}'."
        )
    except InvalidResponseError as err:
        print(f"Invalid response error: {err}")
    except S3Error as err:
        print(f"Failed to upload '{file_path}' to '{bucket_name}/{object_name}': {err}")


def upload_directory_to_minio(client, bucket_name, directory_path, prefix=""):
    base_directory = os.path.basename(directory_path.rstrip("/"))
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            object_name = os.path.join(
                prefix, base_directory, os.path.relpath(file_path, directory_path)
            ).replace("\\", "/")
            upload_file_to_minio(client, bucket_name, file_path, object_name)


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

    # Remove schema (http:// or https://) from the server URL if present
    if server_url.startswith("http://"):
        server_url = server_url[len("http://") :]
        secure = False
    elif server_url.startswith("https://"):
        server_url = server_url[len("https://") :]
        secure = True
    else:
        secure = False

    # Ensure there is no path in the server URL
    if "/" in server_url:
        raise ValueError("Path in endpoint is not allowed")

    # Initialize the Minio client
    client = Minio(
        server_url, access_key=access_key, secret_key=secret_key, secure=secure
    )

    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Upload files or directories to MinIO Object Store."
    )
    parser.add_argument(
        "bucket_name",
        help="The name of the bucket in MinIO where the file or directory will be uploaded.",
    )
    parser.add_argument(
        "file_path", help="The path to the file or directory to be uploaded."
    )
    parser.add_argument(
        "--prefix",
        help="An optional prefix for the object names in MinIO. If uploading a directory, the directory name will be used as a prefix.",
        default="",
    )

    args = parser.parse_args()

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

        if os.path.isdir(args.file_path):
            upload_directory_to_minio(
                client, args.bucket_name, args.file_path, args.prefix
            )
        else:
            upload_file_to_minio(
                client,
                args.bucket_name,
                args.file_path,
                args.prefix or os.path.basename(args.file_path),
            )

    except InvalidResponseError as err:
        print(f"Invalid response error: {err}")
    except S3Error as err:
        print(f"Failed to upload to '{args.bucket_name}': {err}")
