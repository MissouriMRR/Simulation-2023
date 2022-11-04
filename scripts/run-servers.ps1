$scriptPath = Split-Path -parent $MyInvocation.MyCommand.Definition

if (-not(Test-Path -Path $scriptPath\server-config.json -PathType Leaf)) {
    echo "config file not present; run setup.bat and fill out the information in the created json file"
    break
}

$config = Get-Content .\server-config.json | ConvertFrom-Json
$autorun = $config.px4_path + '\autorun.bat'

if (-not(Test-Path -Path $autorun -PathType Leaf)) {
    Get-Content $scriptPath\templates\autorun.txt | Out-File -FilePath $autorun -Encoding oem
}


invoke-expression "cmd /c start powershell -noexit -Command 'cd $($config.px4_path); .\autorun.bat'"
invoke-expression "cmd /c start powershell -noexit -Command 'cd $($config.mavsdk_server_path); .\mavsdk_server_bin.exe udp://:$($config.drone_port)'"
