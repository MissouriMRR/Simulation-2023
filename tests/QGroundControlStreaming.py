'''
import airsim 
import cv2
import numpy as np
import time

filename = 'file.jpg'

client = airsim.MultirotorClient()

while True:
    t1=time.time()
    png_image = client.simGetImage("0", airsim.ImageType.Scene)
    # do something with image
    pic = airsim.string_to_uint8_array(png_image)
    im = cv2.imdecode(np.array(pic, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    cv2.imwrite(filename, im)
    _,img_encode = cv2.imencode('.jpg',im)

    print(time.time()-t1)`
    '''
#!/usr/bin/env python3
# import airsim #pip install airsim
import airsim
import asyncio
import cv2
import utils
import numpy as np
import time
from subprocess import Popen, STDOUT
import subprocess
import os
client = airsim.MultirotorClient()
filename = 'file.png'

def writeToFile():
    
    client.simSetDetectionFilterRadius("3", airsim.ImageType.Scene, 80 * 100) # in [cm]
    client.simAddDetectionFilterMeshName("3", airsim.ImageType.Scene, "ODLC*") 
    print(client.simGetDetections("3", airsim.ImageType.Scene))
    #detections = client.simClearDetectionMeshNames(camera_name, image_type)
    png_image = client.simGetImage("3", airsim.ImageType.Scene)
    pic = airsim.string_to_uint8_array(png_image)
    im = cv2.imdecode(np.array(pic, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(filename, im)
    

    


writeToFile()
DEVNULL = open(os.devnull, 'wb')
sh= Popen("C:/gstreamer/1.0/msvc_x86_64/bin/gst-launch-1.0.exe -q -v multifilesrc location=file.png loop=true ! pngdec ! videoconvert ! videoscale ! videorate ! video/x-raw,framerate=5/1 ! x264enc ! rtph264pay ! udpsink host=127.0.0.1 port=6000",shell=False)

while True:
    
    writeToFile()
    time.sleep(0.5)


