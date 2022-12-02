# This script runs PX4 and MavSDK at the same time

# Function that starts a new powershell instance with a given window name and command
function New-Powershell {
    param (
        $name,
        $command
    )
    return Start-Process powershell -ArgumentList "-noexit", "-noprofile", "-command", "`$host.ui.RawUI.WindowTitle = '$name'; $command"
}

# Get directory of this script and config file
$scriptPath = Split-Path -parent $MyInvocation.MyCommand.Definition
$configPath = "$scriptPath\server-config.json"

# check if config file is present
if (-not(Test-Path -Path $configPath -PathType Leaf)) {
    Write-Output "config file not present; run setup.bat and fill out the information in the created json file"
    break
}

# parse config file
$config = Get-Content $configPath | ConvertFrom-Json

# format some config-related info, which will be used more than once
$autorun = "$($config.px4_path)\autorun.bat"
$drone_uri = "udp://:$($config.drone_port)"

# create the modifed run-console.bat in the PX4 folder if it's missing
if (-not(Test-Path -Path $autorun -PathType Leaf)) {
    Get-Content $scriptPath\templates\autorun.txt | Out-File -FilePath $autorun -Encoding oem
}

# run PX4 and the MavSDK server
New-Powershell "PX4" "cd $($config.px4_path); .\autorun.bat"
New-Powershell "MavSDK Server ($drone_uri)" "cd $($config.mavsdk_server_path); .\mavsdk_server_bin.exe $drone_uri" 
