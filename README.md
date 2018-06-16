# AI Scene Description from Webcam via Azure + Cognitive
=======================================

Series of experiements to have small IoT devices have machine learning intelligence interactions.

Goals:
--------------------------------------
1. Upload image to azure
2. upload webcam frame to azure
3. Pass uploaded frame URL to cognitive services get back Speech to Text description

Command args:
---------------------------------------

-config : JSON file with authentication parameters, refer to "data_schema.json"

Command Promp Example:
>python 3_cognitiveAPI.py -config data.json

Resources
---------------------------------------

- Original Microsoft Tutorial Article [Source](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python)
- Dependency help with Cv2 via Anaconda [Source](http://www.learnopencv.com/install-opencv-3-and-dlib-on-windows-python-only/
)
- Setting up Azure Resources [Source](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-portal)

Dependencies
---------------------------------------
- [Open CV2](http://opencv-python-tutroals.readthedocs.io/en/latest/)
- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python)
- [Requests](http://docs.python-requests.org/en/master/)
- [Google Text To Speech](https://pypi.org/project/gTTS/)
- [PyGame](https://www.pygame.org/)

