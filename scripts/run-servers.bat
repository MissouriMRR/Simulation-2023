@echo off

: modify these based on your configuration
: note that all paths must be absolute

: this is the port on PX4 that the drone connects to
set drone_port=14030

: directory .\mavsdk_server_bin.exe is located in
set mavsdk_server_path=C:\Dev\school\multirotor\MavSDK\bin\

: location of PX4 
set px4_path=C:\PX4\

: DO NOT MODIFY THE CODE BELOW

pushd %~dp0
set script_dir=%CD%
popd

if NOT EXIST %px4_path%\autorun.bat (
    type %script_dir%\autorun.txt > %px4_path%\autorun.bat
)

start powershell -noexit -Command "cd %mavsdk_server_path%; .\mavsdk_server_bin.exe udp://:%drone_port%"
start powershell -noexit -Command "cd %px4_path%; .\autorun.bat"
