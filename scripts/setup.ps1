# server-config.json will be gitignored
# this file is to ensure everyone easily has the correct server-config.json format in the correct location

# get user's document folder (even if it's on OneDrive)
$docs = [Environment]::GetFolderPath('Personal')

Copy-Item "$PSScriptRoot\templates\server-config.lock.json" -Destination "$PSScriptRoot\server-config.json"
Copy-Item "$PSScriptRoot\templates\airsim_settings.lock.json" -Destination "$docs\AirSim\settings.json"
Copy-Item "$PSScriptRoot\templates\airsim_settings.lock.json" -Destination "$PSScriptRoot\airsim-settings.json"

Write-Output "Setup complete"
