import asyncio
from mavsdk import System
import airsim
import cv2 as cv
import utils
import math


_PORT: int = utils.get_config_port()

# Placeholder values to be replaced with actual coords
BOTTOM_LEFT = (0,0)
TOP_RIGHT = (0.01,0.01)
ALTITUDE = 24
FOV = 60

# radius from center of earth to sea level at (0, 0) in meters
sea_level_absolute_altitude = 6378137




camera_radius = ALTITUDE*math.tan(FOV/2)
square_edge_length = math.sqrt(2)*camera_radius


def take_picture():
    pass

def next_pos(i, j, dir, num_horizontal_squares):
    if i == num_horizontal_squares - 2:
        y = TOP_RIGHT[1]-(square_edge_length/2) - (j+1)*square_edge_length 
        if (dir == -1):
            x = TOP_RIGHT[0]-(square_edge_length/2)-num_horizontal_squares*square_edge_length
        else:
            x = TOP_RIGHT[0]-(square_edge_length/2)
    else:
        y = TOP_RIGHT[1] - (square_edge_length/2) - j*square_edge_length
        if (dir == -1):
            x = TOP_RIGHT[0]-(square_edge_length/2) - (i+1)*square_edge_length
        else:
            x = TOP_RIGHT[0]-(square_edge_length/2)-num_horizontal_squares*square_edge_length + (i+1)*square_edge_length
    return (i,j)

async def move_to_point(drone, pos, alt, absolute_alt, meters_to_degrees):
    degrees_to_meters = 1/meters_to_degrees
    await drone.action.goto_location(pos[1], pos[0], alt + absolute_alt, 0)
    location_reached = False
    while not location_reached:
        async for position in drone.telemetry.position():
            if (math.sqrt(math.pow(alt-position.relative_altitude_m, 2)+math.pow((pos[1]-position.latitude_deg)*degrees_to_meters, 2)+math.pow((pos[0]-position.longitude_deg)*degrees_to_meters, 2)) < 0.5):
                location_reached = True
                break

        await asyncio.sleep(1)
    return



async def run(loop: asyncio.AbstractEventLoop):
    drone: System = System(mavsdk_server_address="localhost")
    client = airsim.MultirotorClient()
    client.confirmConnection()
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
    #client.simSetCameraFov(FOV)

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

    absolute_absolute_altitude = sea_level_absolute_altitude + absolute_altitude
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    #await drone.action.goto_location(TOP_RIGHT[1]-(square_edge_length/2), TOP_RIGHT[0]-(square_edge_length/2), absolute_altitude + ALTITUDE, 0)

    absolute_absolute_altitude = sea_level_absolute_altitude + absolute_altitude
    meters_to_degrees = 180/(absolute_absolute_altitude*math.pi)
    square_edge_length_degrees = square_edge_length * meters_to_degrees
    num_vertical_squares = math.ceil((TOP_RIGHT[1]-BOTTOM_LEFT[1])/square_edge_length_degrees)
    num_horizontal_squares = math.ceil((TOP_RIGHT[0]-BOTTOM_LEFT[0])/square_edge_length_degrees)
    dir = -1
    for j in range(num_vertical_squares - 1):
        for i in range(num_horizontal_squares - 1):
            take_picture()
            pos = next_pos(i, j, dir, absolute_altitude + ALTITUDE, num_horizontal_squares)
            await move_to_point(drone, pos, ALTITUDE, absolute_altitude, meters_to_degrees)
            await asyncio.sleep(1)
        take_picture()
        pos = await next_pos(i, j, dir, num_horizontal_squares)
        await move_to_point(drone, pos, ALTITUDE, absolute_altitude, meters_to_degrees)
        dir *= -1
        await asyncio.sleep(1)
    take_picture()
    print("Update textures here")


if __name__ == "__main__":
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    loop.run_until_complete(run(loop))