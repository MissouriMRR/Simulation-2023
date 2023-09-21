# server-config.json will be gitignored
# this file is to ensure everyone easily has the correct server-config.json format in the correct location

# get user's document folder (even if it's on OneDrive)
$docs = [Environment]::GetFolderPath('Personal')

Get-Content "$PSScriptRoot\templates\server-config.lock.json" > "$PSScriptRoot\server-config.json"
Get-Content "$PSScriptRoot\templates\airsim_settings.lock.json" > "$docs\AirSim\settings.json"
Get-Content "$PSScriptRoot\templates\airsim_settings.lock.json" > "$PSScriptRoot\airsim-settings.json"

Write-Output "Setup complete"
