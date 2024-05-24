import os
from functions import config_client, upload_directory_to_minio
from dotenv import load_dotenv

class MinioSynchronizer:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        server_url = os.getenv("SERVER_URL")
        access_key = os.getenv("ACCESS_KEY")
        secret_key = os.getenv("SECRET_KEY")
        self.backup_directories = os.getenv("BACKUP_DIRECTORIES", "").split(";")

        # Initialize MinIO client
        self.client = config_client(server_url=server_url, access_key=access_key, secret_key=secret_key)

    def backup_directories(self, bucket_name, prefix=""):
        for directory_path in self.backup_directories:
            if os.path.isdir(directory_path):
                print(f"Backing up directory: {directory_path}")
                upload_directory_to_minio(self.client, bucket_name, directory_path, prefix)
            else:
                print(f"Error: '{directory_path}' is not a valid directory.")

# Example usage:
if __name__ == "__main__":
    synchronizer = MinioSynchronizer()
    # synchronizer.backup_directories("my-backup-bucket", "optional/prefix")
