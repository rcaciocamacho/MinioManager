from minio import Minio
import os
import argparse
from minio.error import S3Error, InvalidResponseError

def help_parser(parser):

    # Setup argument parser
    parser = argparse.ArgumentParser(description="Upload files or directories to MinIO Object Store or download object versions.")
    parser.add_argument("bucket_name", help="The name of the bucket in MinIO where the file or directory will be uploaded or downloaded.")
    parser.add_argument("file_path", help="The path to the file or directory to be uploaded, or the path where the downloaded file will be saved.")
    parser.add_argument("--prefix", help="An optional prefix for the object names in MinIO when uploading.", default="")
    parser.add_argument("--download", action="store_true", help="Download mode. Specify the object name and optionally the version ID to download.")
    parser.add_argument("--object_name", help="The name of the object to be downloaded.")
    parser.add_argument("--version_id", help="The version ID of the object to be downloaded.")

    return parser.parse_args()


def config_client(server_url, access_key, secret_key):

    if not server_url or not access_key or not secret_key:
        print("Error: Missing MinIO configuration in .env file.")
        exit(1)

    # Remove schema (http:// or https://) from the server URL if present
    if server_url.startswith("http://"):
        server_url = server_url[len("http://"):]
        secure = False
    elif server_url.startswith("https://"):
        server_url = server_url[len("https://"):]
        secure = True
    else:
        secure = False

    # Ensure there is no path in the server URL
    if '/' in server_url:
        raise ValueError("Path in endpoint is not allowed")

    # Initialize the Minio client
    return Minio(
        server_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )

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
