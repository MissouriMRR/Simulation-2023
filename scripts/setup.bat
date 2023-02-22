@ECHO OFF

REM server-config.json will be gitignored
REM this file is to ensure everyone easily has the correct server-config.json format in the correct location

@echo off&setlocal
for %%i in ("%~dp0.") do set "folder=%%~fi"

type %folder%\templates\server-config.lock.json > %folder%\server-config.json
type %folder%\templates\airsim_settings.lock.json > %UserProfile%\Documents\AirSim\settings.json

echo Setup complete
