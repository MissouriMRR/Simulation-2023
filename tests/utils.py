# A collecton of useful functions to keep between files

import airsim as _as
import numpy as _np
import cv2 as _cv
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


def detect_object(client: _as.MultirotorClient) -> None:

    # set camera name and image type to request images and detections
    camera_name = "down"
    image_type = _as.ImageType.Scene

    # set detection radius in [cm]
    client.simSetDetectionFilterRadius(camera_name, image_type, 200 * 100) 
    # add desired object name to detect in wild card/regex format
    client.simAddDetectionFilterMeshName(camera_name, image_type, "Cylinder*") 

    while True:
        rawImage = client.simGetImage(camera_name, image_type)
        if not rawImage:
            continue
        png = _cv.imdecode(_as.string_to_uint8_array(rawImage), _cv.IMREAD_UNCHANGED)
        cylinders = client.simGetDetections(camera_name, image_type)
        if cylinders:
            for cylinder in cylinders:
                s = _as.pformat(cylinder)
                print("Cylinder: %s" % s)

                _cv.rectangle(png,(int(cylinder.box2D.min.x_val),int(cylinder.box2D.min.y_val)),(int(cylinder.box2D.max.x_val),int(cylinder.box2D.max.y_val)),(255,0,0),2)
                _cv.putText(png, cylinder.name, (int(cylinder.box2D.min.x_val),int(cylinder.box2D.min.y_val - 10)), _cv.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))

    
        _cv.imshow("AirSim", png)
        if _cv.waitKey(1) & 0xFF == ord('q'):
            break
        elif _cv.waitKey(1) & 0xFF == ord('c'):
            client.simClearDetectionMeshNames(camera_name, image_type)
        elif _cv.waitKey(1) & 0xFF == ord('a'):
            client.simAddDetectionFilterMeshName(camera_name, image_type, "Cylinder*")
    _cv.destroyAllWindows() 
