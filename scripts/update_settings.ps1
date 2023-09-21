# This script copies the content of the provided file into AirSim's settings
param(
    [string]$file
)

$docs = [Environment]::GetFolderPath('Personal')
$settings = "$PSScriptRoot\airsim-settings.json"

# check if a custom settings file was provided
if ($PSBoundParameters.ContainsKey('file')) {
    $settings = "$file"
}

Get-Content "$settings" > "$docs\AirSim\settings.json"

Write-Output "Settings updated!"
