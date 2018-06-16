'''
IoT Azure upload test series

need to have python3 compiled form source a dependency
follow this tutorial:
http://www.learnopencv.com/install-opencv-3-and-dlib-on-windows-python-only/

Part 3 !
Cognitive services + TTS
'''


import cv2
import os, uuid, sys, json
from azure.storage.blob import BlockBlobService, PublicAccess
import requests
from gtts import gTTS
import pygame

# import pyglet

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


def show_webcam(blobService, container, config, mirror=False):
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
            # create the full file path
            local_path = os.getcwd() + '\\data'
            local_file_name = 'webcam_capture'+ str(uuid.uuid4()) +'.jpg'
            full_image_path = os.path.join(local_path, local_file_name)

            # export frame
            cv2.imwrite(full_image_path, img)
            print('exporting frame to: '+ full_image_path)

            # upload to Azure
            uploadToAzure(blobService, container, local_file_name)

            # now that it's uploaded call the cognitive services and pass in the public URL
            analysis = getCognitiveAPIResponse(config, local_file_name)

            if (len(analysis['description']['captions']) > 0):
                caption = analysis['description']['captions'][0]
                # round up to percentage to make it seem more conversational
                spoken_text = str(round(caption['confidence']*100)) + ' percent sure it is ' + caption['text']
                print('response is- ' +spoken_text)

                # use gTTS to export sound to .mp3 locally
                tts = gTTS(text=spoken_text, lang='en')
                tts_fileName = 'cognitive_caption' + str(uuid.uuid4()) + '.mp3'
                tts_sound_path = os.path.join(local_path, tts_fileName)
                tts.save(tts_sound_path)
                print('output to mp3 : ' + tts_sound_path)

                # use pygame to playback the sound that was just exported
                pygame.mixer.init()
                pygame.mixer.music.load(tts_sound_path)
                pygame.mixer.music.play()

        '''
        # debug trace out new keys
        key = cv2.waitKey(1)
        if key > 0:
           print( 'key is '+ str(key))
        '''
    cv2.destroyAllWindows()


def uploadToAzure(block_blob_service, container_name, local_file_name):
    try:
        # Create upload the fruit photo
        local_path = os.getcwd() + '\\data'
        full_path_to_file = os.path.join(local_path, local_file_name)

        print("\nUploading to Blob storage as blob: " + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

    except Exception as e:
        print(e)


def getCognitiveAPIResponse(config, fileName):
    try:
        print('sending '+fileName +' to cognitive services')

        # reference
        # https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python
        # create public URL based on account info
        image_url = 'https://'+config['azure']['authentication']['account_name']+'.blob.core.windows.net/'+config['azure']['container_name']+'/' + fileName

        vision_base_url = config['cognitive']['base_URL']
        vision_analyze_url = vision_base_url + "/analyze"

        headers = {'Ocp-Apim-Subscription-Key': config['cognitive']['authentication']['subscription_key']}
        params = {'visualFeatures': 'Categories,Description,Color'}
        data = {'url': image_url}
        response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        analysis = response.json()
        return analysis
    except Exception as e:
        print(e)



def main():

    print("This is the name of the script: ", sys.argv[0])
    print("Number of arguments: ", len(sys.argv))
    print("The arguments are: ", str(sys.argv))
    argsOptions = getArgsOptionKeyPairs(sys.argv)
    if '-i' in argsOptions:  # Example usage.
        print(argsOptions['-i'])

    print(argsOptions)

    print('loading.. ' +argsOptions['-config'])
    with open(argsOptions['-config']) as json_file:
        jsonConfig = json.loads(json_file.read())

    blobService = getAzureBlobService(jsonConfig['azure']['authentication']['account_name'],
                                      jsonConfig['azure']['authentication']['account_key'],
                                      jsonConfig['azure']['container_name'])

    show_webcam(blobService, jsonConfig['azure']['container_name'], jsonConfig, mirror=True)

def getArgsOptionKeyPairs(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    main()