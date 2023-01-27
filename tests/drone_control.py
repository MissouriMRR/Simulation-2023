'''
Allows for rudimentary control of the drone using text input.

Controls:
- f   = forward/add lattitude
- b   = backward/subtract lattitude
- r   = right/add longitude
- l   = left/subtract longitude
- u   = up/add altitude
- d   = down/substract altitude
- die = kill the connection to the drone

You can enter multiple commands (excluding die) at once.
For example, the command "ffffuuuuu" will execute the forward command 4 times
and he up command 5 times.

'''

import asyncio
from mavsdk import System
import airsim
import os
import numpy as np
import cv2 as cv


_PORT: int = 14030


async def run():
    drone: System = System(mavsdk_server_address="localhost")
    client = airsim.MultirotorClient()

    await drone.connect(system_address=f"udp://:{_PORT}")

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

    absolute_altitude: float
    long: float
    lat: float

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
    await drone.action.set_current_speed(10)

    await asyncio.sleep(1)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(lat, long, flying_alt, 0)
    

    while True:
        command: str = input("Give instructions: ").lower()
        await asyncio.sleep(1)

        if command == 'die':
            await drone.action.kill()
            return

        for cmd in command:
            match cmd:
                case 'f':
                    lat += 0.0001
                case 'b':
                    lat -= 0.0001
                case 'r':
                    long += 0.0001
                case 'l':
                    long -= 0.0001
                case 'u':
                    flying_alt += 5
                case 'd':
                    flying_alt -= 5
                case 'p':
                    responses = client.simGetImages([
                        airsim.ImageRequest("down", airsim.ImageType.Scene, False, False),
                    ])

                    response = responses[0]

                    # get numpy array
                    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 

                    # reshape array to 4 channel image array H X W X 4
                    img_rgb = img1d.reshape(response.height, response.width, 3)

                    # write to png 
                    cv.imshow("Image", img_rgb)
                    cv.waitKey(0)
                
        await drone.action.goto_location(lat, long, flying_alt, 0)
    

if __name__ == "__main__":
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    loop.run_until_complete(run())