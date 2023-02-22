# This test just takes a picture and displays it

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