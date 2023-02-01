# just some useful functions to keep between files
import airsim as _as
import numpy as _np
from nptyping import NDArray, Shape, UInt


def get_image(airsim_client: _as.MultirotorClient, image_id="down", 
              image_type=_as.ImageType.Scene, pixels_as_float=False, 
              compress=False) -> NDArray[Shape["*, *, 4"], UInt]:
    response, = airsim_client.simGetImages([
        _as.ImageRequest(image_id, image_type, pixels_as_float, compress)
    ])

    # get numpy array
    img1d = _np.frombuffer(response.image_data_uint8, dtype=_np.uint8) 

    # reshape array to 4 channel image array H X W X 4
    return img1d.reshape(response.height, response.width, 3)
