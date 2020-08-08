from azure.storage.blob import BlobClient, ContainerClient        

def uploadFile(container_url, file_name):
        container = ContainerClient.from_container_url(container_url=container_url)
        blob = container.get_blob_client(file_name)
        with open(file_name, "rb") as data:
                blob.upload_blob(data, overwrite=True)


if __name__ == "__main__":
        import sys
        uploadFile(sys.argv[2], sys.argv[1])
