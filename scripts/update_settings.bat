@REM This script copies the content of the provided file into AirSim's settings

@echo off&setlocal
for %%i in ("%~dp0.") do set "folder=%%~fi"

@REM Default settings file
set settings="%folder%\airsim-settings.json"

@REM Check if user provided file
if NOT "%~1" == "" set settings="%~1"

type %settings% > %UserProfile%\Documents\AirSim\settings.json

echo Settings updated!
