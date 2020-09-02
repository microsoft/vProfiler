import sys
import os
import socket
from datetime import datetime
import glob

try:
        from azure.storage.blob import BlobClient, ContainerClient
except ModuleNotFoundError:
        print("Azure Blob Stoage module not found. Try pip install azure-storage-blob")
        sys.exit(1)

def uploadFile(container_url, file_name):
        container = ContainerClient.from_container_url(container_url=container_url)
        blob = container.get_blob_client(file_name)
        with open(file_name, "rb") as data:
                blob.upload_blob(data, overwrite=True)

def uploadLogs(container_url):
        os.chdir('..')
        list_of_tar_files = glob.glob('*.tar.gz')
        if len(list_of_tar_files) == 0:
                print("upload.py: Error no tar ball found", file=sys.stderr)
                sys.exit(2)
        latest_file = max(list_of_tar_files, key=os.path.getctime)
        uploadFile(container_url, latest_file)

if __name__ == "__main__":
        uploadLogs(sys.argv[1])
