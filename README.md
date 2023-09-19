# Simulation-2023
Missouri S&amp;T Multirotor Design Team's simulation environments for our 2023-2024 competition: the Student Unmanned Aerial Systems Competition (SUAS)

## Table of Contents
- [Installation and Environment Setup](#installation-and-environment-setup)
- [Running Python Code](#running-python-code)
    - [Debugging](#debugging)
        - [PX4 Won't Connect](#px4-wont-connect)
        - [MavSDK Server Won't Connect to PX4](#mavsdk-server-wont-connect-to-px4)
        - [No module named 'encodings' when starting PX4 (Windows)](#no-module-named-encodings-when-starting-px4-windows)

## Installation and Environment Setup

Follow these instructions to setup your environment (Windows):

1. install [git](https://git-scm.com)
2. install [poetry (python)](https://python-poetry.org)
3. install [Visual Studio](https://visualstudio.microsoft.com)
    - make sure to select the `C++ Development Pack` and check `Windows SDK 10`. This is required for the next steps
    - download the 2022 version if possible
4. install [Unreal Engine 4.27.2](https://www.unrealengine.com/en-US/?utm_source=GoogleSearch&utm_medium=Performance&utm_campaign=%7Bcampaigname%7D&utm_id=17086214833&sub_campaign=&utm_content=&utm_term=unreal%20engine)
    - if you already have the Epic Games Launcher, you can download Unreal Engine from the 'Unreal Engine' tab
    - **make sure to run Unreal Engine from the Epic Games Launcher before moving to the next step**
5. install [Microsoft AirSim](https://github.com/Microsoft/AirSim)
    - Clone repo (`git clone https://github.com/Microsoft/AirSim`) to desired location
    - open `x64 Native Tools Command Prompt for VS 20XX` (just search 'x64 Native Tools' in the Windows search bar and the correct program should appear)
    - navigate to where you installed AirSim using `cd insert/AirSim/path/here` in `x64 Native Tools Command Prompt for VS 20XX` and run `.\build.cmd`
6. install [PX4](https://github.com/PX4/PX4-windows-toolchain/releases/download/v0.9/PX4.Windows.Cygwin.Toolchain.0.9.msi)
    - run the installer (the `.msi` file) after downloading
7. install [MavSDK](https://github.com/mavlink/MAVSDK/releases/download/v1.4.16/mavsdk-windows-x64-release.zip)
    - download the `.zip` from the above link and unzip it wherever you please
    - keep track of where you unzip it, since you'll need it for a future step
8. Open a terminal and clone this repository: `git clone https://github.com/MissouriMRR/Simulation-2023.git`
9. Navigate in your terminal to the repository root and run the command `poetry install`
10. Navigate to `\scripts\` in a command prompt or PowerShell instance and run `.\setup.bat`
    - This will create a file called `\scripts\server-config.json`. Open this file and...
        - replace `mavsdk_server_path` with the absolute path to the `\bin` directory where you unzipped MavSDK
        - replace `px4_path` with the absolute path to your PX4 folder
        - replace `drone_port` with the necessary drone port, if necessary ([click here for more info](#debugging))
            - this will become more relevant after attempting to run tests
        - the final result should look something like this:
        ```json
        {
            "drone_port": 14030,
            "mavsdk_server_path": "C:\\Dev\\school\\multirotor\\MavSDK\\bin",
            "px4_path": "C:\\PX4\\"
        }
        ```

AirSim comes with a test project called Blocks. It is located in your AirSim folder at `\AirSim\Unreal\Environments\Blocks\Blocks.uproject`

## Running Python Code

Make sure to complete all [installation and setup](#installation-and-environment-setup) steps before attempting to run code.

1. Open your AirSim Unreal Engine project
2. Open a terminal and rnavigate to the root of your cloned repository. Then, run `poetry shell`
    - This will activate a virtual environment outfitted with the necessary dependencies need to interact with the simulation with Python.
3. Start the Unreal Engine simulation using the editor's `Play` button
4. Start the PX4 and MavSDK servers by running `\scripts\servers.ps1`
5. Run your code!

Whenever you want to rerun code, you must
- stop the Unreal Simulation
- close the PX4 and MavSDK PowerShell instances
- repeat steps 3-5 in the above guide

When finished running code, run `exit` to exit your Poetry virtual environment.

**Note:** to connect to the virtual drone with Python, you must use the `mavsdk` Python package.

```python
from mavsdk import System

drone: System = System(mavsdk_server_address="localhost")
await drone.connect(system_address=f"udp://:{PORT}")  # replace {PORT} with the drone_port in \scripts\server-config.json
```

### Debugging

There are many points of failure when attempting to run your Python code unrelated to your code. Below are some solutions to common problems.

#### PX4 Won't Connect

Most often, this means you forgot to start the Unreal Engine simluation. However, if this is not the case, it's possible that PX4 is looking at the wrong TCP port.

To fix this:
1. find the TCP port PX4 is looking at
    - if you haven't already, run `\scripts\run-servers.ps1`
    - in PX4's console, locate the line `Waiting for simulator to accept connection on TCP port XXXX`
        - the port listed is what you need
2. *make a copy* of `\scripts\templates\airsim_settings.lock.json` (you can remove the `.lock` part of the extension)
    - in your copy, replace the value of `Vehicles.PX4.TcpPort` with the port you discovered
3. run `\scripts\update_settings.bat \path\to\your\settings\copy.json`
    - this will update your AirSim settings for you (AirSim has, like, five places it looks for settings files, but this will always put it in the correct location)

Now, you should be all set! You may need to restart Unreal Engine, however.

#### MavSDK Server Won't Connect to PX4

Hopefully, the default port provided in `\scripts\server-config.json`, `14030`, will be correct; however, if MavSDK won't connect to PX4, then the port is likely incorrect.

To fix this:
1. run `\scripts\run-servers.ps1` if you haven't already
2. wait until PX4 is fully loaded
    - you will have to start your Unreal Engine simulation with the `Play` button to ensure PX4 progresses far enough to accept a mavlink connection
    - if PX4 doesn't connect to anything after starting the simulation, check the [above section](#px4-wont-connect) for a possible fix
3. if MavSDK's console output remains `Waiting to discover system on udp://:insert_port_here...` even after PX4 has connected to the simulation, you likely have the incorrect port. If it connects, then nothing is wrong!
4. locate the *final occurrance* of a message similar to `mode: Onboard, data rate: 4000 B/s on udp port 14280 remote port 14030` in PX4's console output
    - the listed *remote port* is the one you need
5. replace the value of `drone_port` in your `\scripts\server-config.json` with the remote port you found
    - if you do not have `\scripts\server-config.json`, then you must first run `\scripts\setup.bat`

Now, you should be all good! Run your code as described [above](#running-python-code).

#### No module named 'encodings' when starting PX4 (Windows)

This error might be caused by window's enviroment variables interfering with PX4's virtual python enviroment. 

To fix this:
1. Search 'enviroment variables' in the window's search.
2. Delete PYTHONPATH and PYTHONHOME

Now, it should work! 





