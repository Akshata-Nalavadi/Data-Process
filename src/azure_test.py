import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# required: install azure cli: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli


try:  
    print ("Azure Blob Storage Python quickstart sample")
    # Quickstart code goes here
    account_url = "https://consatml.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
# Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_name = "quickstart" + str(uuid.uuid4())
    container_client = blob_service_client.create_container("test_container")
except Exception as ex:
    print ('Exception:')
    print (ex)