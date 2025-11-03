# storage_upload.py
from azure.storage.blob import BlobServiceClient
import os
from config import BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME

def  upload_files(folder_path="D:\Ecommerce_RAGChatbot\Ecommerce_RAGChatbot"):
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

    try:
        container_client.create_container()
    except:
        pass  # Container exists

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open("appleprice.pdf", "rb") as data:
            container_client.upload_blob("appleprice.pdf", data, overwrite=True)
            print(f"? Uploaded {file_name} to Blob Storage")

if __name__ == "__main__":
    upload_files()


