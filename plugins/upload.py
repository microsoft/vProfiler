from azure.storage.blob import BlobClient, ContainerClient
import sys
import os
import socket
from datetime import datetime

import glob

def uploadFile(container_url, file_name):
        container = ContainerClient.from_container_url(container_url=container_url)
        blob = container.get_blob_client(file_name)
        with open(file_name, "rb") as data:
                blob.upload_blob(data, overwrite=True)

def uploadLogs(container_url):
        os.chdir('..')
        list_of_tar_files = glob.glob('*.tar.gz')
        latest_file = max(list_of_tar_files, key=os.path.getctime)
        uploadFile(container_url, latest_file)

if __name__ == "__main__":
        uploadLogs(sys.argv[1])
