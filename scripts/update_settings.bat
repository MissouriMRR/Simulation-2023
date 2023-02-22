@REM This script copies the content of the provided file into AirSim's settings

@echo off&setlocal
for %%i in ("%~dp0.") do set "folder=%%~fi"

type %1 > %UserProfile%\Documents\AirSim\settings.json

echo Settings updated!
