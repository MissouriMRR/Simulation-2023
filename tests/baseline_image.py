import os
import numpy as np
import airsim


if __name__ == "__main__":
    client = airsim.MultirotorClient()
    client.confirmConnection()

    responses = client.simGetImages([
        airsim.ImageRequest("3", airsim.ImageType.Scene, False, False),
    ])

    response = responses[0]


    # get numpy array
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 

    # reshape array to 4 channel image array H X W X 4
    img_rgb = img1d.reshape(response.height, response.width, 3)

    # write to png 
    airsim.write_png(os.path.normpath("test" + '.png'), img_rgb) 