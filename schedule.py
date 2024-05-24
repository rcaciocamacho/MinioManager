import os
from functions import config_client, upload_file_to_minio, upload_directory_to_minio, list_object_versions, download_object_version
from dotenv import load_dotenv

class MinioScheduler:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        server_url = os.getenv("SERVER_URL")
        access_key = os.getenv("ACCESS_KEY")
        secret_key = os.getenv("SECRET_KEY")

        # Initialize MinIO client
        self.client = config_client(server_url=server_url, access_key=access_key, secret_key=secret_key)

    def upload_file(self, bucket_name, file_path, prefix=""):
        if not os.path.isfile(file_path):
            print(f"Error: '{file_path}' is not a valid file.")
            return

        object_name = os.path.join(prefix, os.path.basename(file_path)).replace("\\", "/")
        upload_file_to_minio(self.client, bucket_name, file_path, object_name)

    def upload_directory(self, bucket_name, directory_path, prefix=""):
        if not os.path.isdir(directory_path):
            print(f"Error: '{directory_path}' is not a valid directory.")
            return

        upload_directory_to_minio(self.client, bucket_name, directory_path, prefix)

    def download_object(self, bucket_name, object_name, file_path):
        if not object_name:
            print("Error: 'object_name' must be specified.")
            return

        download_object_version(self.client, bucket_name, object_name, None, file_path)

    def download_object_version(self, bucket_name, object_name, version_id, file_path):
        if not object_name:
            print("Error: 'object_name' must be specified.")
            return
        if not version_id:
            print("Error: 'version_id' must be specified.")
            return

        download_object_version(self.client, bucket_name, object_name, version_id, file_path)

    def list_versions(self, bucket_name, object_name):
        if not object_name:
            print("Error: 'object_name' must be specified.")
            return

        versions = list_object_versions(self.client, bucket_name, object_name)
        if versions:
            print(f"Versions for object '{object_name}' in bucket '{bucket_name}':")
            for version in versions:
                print(version)
        else:
            print(f"No versions found for object '{object_name}' in bucket '{bucket_name}'.")

# Example usage:
if __name__ == "__main__":
    scheduler = MinioScheduler()
    
    # Upload a file
    # scheduler.upload_file("my-bucket", "path/to/your/file.txt", "optional/prefix")
    
    # Upload a directory
    # scheduler.upload_directory("my-bucket", "path/to/your/directory", "optional/prefix")
    
    # Download the latest version of an object
    # scheduler.download_object("my-bucket", "object_name", "path/to/save/file.txt")
    
    # Download a specific version of an object
    # scheduler.download_object_version("my-bucket", "object_name", "version_id", "path/to/save/file.txt")
    
    # List versions of an object
    # scheduler.list_versions("my-bucket", "object_name")
