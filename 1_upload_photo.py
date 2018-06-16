
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
'''
 Step 1 - upload an image to Azure

 based off of the exmaple provided by MS here
'''
def run_sample():
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='<account_name>', account_key='<account_key>')

        # Create a container called 'quickstartblobs'.
        container_name ='quickstartblobs'
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # Create upload the fruit photo
        local_path=os.getcwd()+'\\data'
        local_file_name ='fruit.jpg'
        full_path_to_file =os.path.join(local_path, local_file_name)

        print("\nUploading to Blob storage as blob" + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)

        # Download the blob(s).
        # Add '_DOWNLOADED' as prefix to '.jpg' so you can see both files in Documents.
        full_path_to_file2 = os.path.join(local_path, str.replace(local_file_name ,'.jpg', '_DOWNLOADED.jpg'))
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file2)

        sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                         "application will exit.")
        sys.stdout.flush()
        input()

        # Clean up resources. This includes the container and the temp files
        block_blob_service.delete_container(container_name)
        os.remove(full_path_to_file2)
    except Exception as e:
        print(e)


# Main method
if __name__ == '__main__':
    run_sample()



