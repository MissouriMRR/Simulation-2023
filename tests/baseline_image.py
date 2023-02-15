import os
import numpy as np
import airsim
import cv2 as cv
import utils

if __name__ == "__main__":
    client = airsim.MultirotorClient()
    client.confirmConnection()

    img = utils.get_image(client)

    # show img 
    cv.imshow("Image", img)
    cv.waitKey(0)