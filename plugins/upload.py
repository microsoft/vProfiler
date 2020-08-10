from azure.storage.blob import BlobClient, ContainerClient
import sys
import os
import socket
from datetime import datetime

def uploadFile(container_url, file_name):
        container = ContainerClient.from_container_url(container_url=container_url)
        blob = container.get_blob_client(file_name)
        with open(file_name, "rb") as data:
                blob.upload_blob(data, overwrite=True)

def uploadLogs(container_url):
        file_name = "vProfiler_" + socket.gethostname() + "_" + datetime.now().strftime("%d%m%Y-%H%M%S") + ".tar.gz"
        os.chdir("..")
        os.system("tar -czf " + file_name + " logs")
        uploadFile(container_url, file_name)

if __name__ == "__main__":
        uploadLogs(sys.argv[1])
