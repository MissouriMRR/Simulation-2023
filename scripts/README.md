# Scripts

This folder contains a few scripts that aim to make using AirSim and MavSDK easier. *It is recommended that each script is ran from this folder.*

Before doing anything, make sure you have everything installed as listed in the main README.

## `setup.bat`

This script sets up your environment so other scripts may run correctly. Most importantly, it will create a file called `server-config.json`, which contains important data for running `run-servers.ps1`, which is probably the most convinient command in the folder.

This is what `server-config.json` may look like.
```json
{
    "drone_port": 14030,
    "mavsdk_server_path": "C:\\Dev\\school\\multirotor\\MavSDK\\bin",
    "px4_path": "C:\\PX4\\"
}
```

Make sure to replace `mavsdk_server_path` with the absolute path to your MavSDK download's `bin` folder. Your `px4_path` should be the absolute path to your PX4 folder. Make sure to escape backslashes (as shown above).

The `drone_port` is UDP port the MavSDK server and virtual drone will connect to.

## `update_settings.bat`

Updates your AirSim settings for you. Create a file for your AirSim settings JSON then pass it as an argument to this script. You can look at (but do not edit) `.\templates\airsim_settings.lock.json` for the default settings.

**Example:**

```ps1
.\update_settings.bat my_settings.json
```

## `run-servers.ps1`

Runs PX4 and creates a MavSDK server with one command based on your `server-config.json`. This command is meant to streamline testing by reducing the tedium spawned by manually starting and restarting PX4 and MavSDK servers. After each restart, you should close the PowerShell instances running previous PX4 and MavSDK instances.

When testing, the recommended order of launching/starting things is:

1. Start the Unreal simulation
2. Run `run-servers.ps1`
3. Run your python program