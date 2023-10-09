import airsim
import numpy as np
import cv2
import time
import pprint

from vision import flyover_vision_pipeline

print("got to here")
client =airsim.MultirotorClient(ip="192.168.137.1")
scene=airsim.ImageType.Scene
client.simSetDetectionFilterRadius("3",scene,80*100)
client.simAddDetectionFilterMeshName("3",scene,"ODLC*")

while(True):
    png_image=client.simGetImage("3",airsim.ImageType.Scene)
    pic=airsim.string_to_uint8_array(png_image)
    im=cv2.imdecode(np.array(pic,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
    
    detection=(client.simGetDetections("3",scene))[0]
    s = pprint.pformat(detection)
    cv2.rectangle(im,(int(detection.box2D.min.x_val),int(detection.box2D.min.y_val)),(int(detection.box2D.max.x_val),int(detection.box2D.max.y_val)),(255,0,0),1)
    cv2.imwrite("file.png",im)

    
    
    time.sleep(0.5)