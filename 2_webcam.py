'''
IoT Azure upload test series

need to have opencv as a dependency
follow this tutorial:
http://www.learnopencv.com/install-opencv-3-and-dlib-on-windows-python-only/
'''

import cv2
import os, uuid, sys, json
from azure.storage.blob import BlockBlobService, PublicAccess


def getAzureBlobService( account_name,  account_key, container_name ):
    try:
        print('\n initializing azure...')
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name=account_name,
                                              account_key=account_key)

        # Create a container called 'quickstartblobs'.
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        return block_blob_service

    except Exception as e:
        print(e)


def show_webcam(blobService, container, mirror=False):
    # index refers to camera ID
    cam = cv2.VideoCapture(1)

    # infinite loop
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        # "c" key
        elif cv2.waitKey(1) == 99:
            local_path = os.getcwd() + '\\data'
            local_file_name = 'webcam_capture'+ str(uuid.uuid4()) +'.jpg'
            full_path_to_file = os.path.join(local_path, local_file_name)
            cv2.imwrite(full_path_to_file, img)
            print('exporting frame to: '+ full_path_to_file)
            uploadToAzure(blobService, container, local_file_name)
    cv2.destroyAllWindows()


def uploadToAzure(block_blob_service, container_name, local_file_name):
    try:
        local_path = os.getcwd() + '\\data'
        full_path_to_file = os.path.join(local_path, local_file_name)

        print("\nUploading to Blob storage as blob: " + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)

        # Download the blob(s).
        # Add '_DOWNLOADED' as prefix to '.jpg' so you can see both files
        full_path_to_file2 = os.path.join(local_path, str.replace(local_file_name, '.jpg', '_DOWNLOADED.jpg'))
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file2)

        sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                         "application will exit.")
        sys.stdout.flush()
    except Exception as e:
        print(e)


def main():
    # load command line args to load auth config JSON

    argsOptions = getArgsOptionKeyPairs(sys.argv)
    print('loading.. ' +argsOptions['-config'])

    # load JSON file
    with open(argsOptions['-config']) as json_file:
        json_data = json.loads(json_file.read())

    # initialize block blob service with container options
    blobService = getAzureBlobService(json_data['auth']['account_name'],
                                      json_data['auth']['account_key'],
                                      json_data['config']['container_name'])

    show_webcam(blobService, json_data['config']['container_name'], mirror=True)


def getArgsOptionKeyPairs(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    main()