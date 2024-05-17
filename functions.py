

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
