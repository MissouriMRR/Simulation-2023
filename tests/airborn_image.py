import airsim
import numpy as np
import asyncio
import os
from mavsdk import System

import cv2 as cv

_PORT: int = 14030

async def run():
    drone: System = System(mavsdk_server_address="localhost")
    await drone.connect(system_address=f"udp://:{_PORT}")

    client = airsim.MultirotorClient()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        long = terrain_info.longitude_deg
        lat = terrain_info.latitude_deg
        break
    
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(1)
    # To fly drone 20m above the ground plane
    flying_alt: float = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(lat, long, flying_alt, 0)

    responses = client.simGetImages([
        airsim.ImageRequest("down", airsim.ImageType.Scene, False, False),
    ])

    response = responses[0]

    # get numpy array
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 

    # reshape array to 4 channel image array H X W X 4
    img_rgb = img1d.reshape(response.height, response.width, 3)

    cv.imshow("Image", img_rgb)
    cv.waitKey(0)


if __name__ == "__main__":
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    loop.run_until_complete(run())

    