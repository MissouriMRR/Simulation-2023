# This script runs PX4 and MavSDK at the same time

param(
    $port = $null
)

# Function that starts a new powershell instance with a given window name and command
function New-Powershell {
    param (
        $name,
        $command
    )
    return Start-Process powershell -ArgumentList "-noexit", "-noprofile", "-command", "`$host.ui.RawUI.WindowTitle = '$name'; $command" -WindowStyle Minimized
}

# Get directory of this script and config file
$configPath = "$PSScriptRoot\server-config.json"

# check if config file is present
if (-not(Test-Path -Path "$configPath" -PathType Leaf)) {
    Write-Output "config file not present; run setup.bat and fill out the information in the created json file"
    break
}

# parse config file
$config = Get-Content "$configPath" | ConvertFrom-Json

# if port wasn't provided as an argument, then use the port from the config
if ($null -eq $port) {
    $port = $config.drone_port
}

# format some config-related info, which will be used more than once
$autorun = "$($config.px4_path)\autorun.bat"
$drone_uri = "udp://:$port"

# create the modifed run-console.bat in the PX4 folder if it's missing
if (-not(Test-Path -Path "$autorun" -PathType Leaf)) {
    Get-Content "$PSScriptRoot\templates\autorun.txt" | Out-File -FilePath "$autorun" -Encoding oem
}

# TODO: make work (ues TrimEnd('\') to prevent trailing slash in path from escaping characters)
# run PX4 and the MavSDK server
Write-Output "cd `"$($config.px4_path)`"; .\autorun.bat"
Write-Output "cd `"$($config.mavsdk_server_path)`"; .\mavsdk_server_bin.exe $drone_uri"

New-Powershell "PX4" "cd `"$($config.px4_path)`" ; .\autorun.bat"
New-Powershell "MavSDK Server ($drone_uri)" "cd `"$($config.mavsdk_server_path)`"; .\mavsdk_server_bin.exe $drone_uri"

Write-Output "Started MavSDK Server at $drone_uri and PX4"
