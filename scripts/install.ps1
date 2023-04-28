# Note: this script is mostly untested

Add-Type -AssemblyName System.Windows.Forms

$px4_installer_name = "PX4.Windows.Cygwin.Toolchain.0.9.msi"

# function to select folder graphically
function GetFolder {
    param (
        $desc
    )
    Push-Location
    $FileBrowser = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{
        ShowNewFolderButton = $true
        Description = 'Select AirSim download location...'
        RootFolder = 'Desktop'
    }
    if($FileBrowser.ShowDialog() -ne "OK") {
        break
    }
    Pop-Location

    return $FileBrowser.SelectedPath
}

# function that verifies the existence of a commmand
function VerifyCmd {
    param (
        $cmd
    )
    try {
        Get-Command $cmd -ErrorAction stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# check if git is installed (needed for getting AirSim)
if (-not(VerifyCmd git)) {
    Write-Output "git must be installed; you can install it here: https://git-scm.com/download/win"
    break
}

# Check if Poetry is installed
# Poetry is not required for downloading things, but it is used by the team

$pyCmd = "py"

if (-not(VerifyCmd poetry)) {
    $response
    $default = "Y"

    # ask if user wants to install Poetry
    if (!($response = Read-Host "Poetry is not installed. Would you like to install it? [Y/n]")) { 
        $response = $default 
    }

    if ("Y","y" -contains $response) {

        if (-not(VerifyCmd py)) {
            if (VerifyCmd python) {
                $pyCmd = "python"
            } else {
                Write-Output "python must be installed to download Poetry"
                break
            }
        }
        
        Write-Output "Installing Poetry..."
        Invoke-Expression -Command "(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | $pyCmd -"
    }
    
}

# Download AirSim and PX4

Write-Output "Select a folder to download AirSim..."
$airsim_folder = GetFolder 'Select AirSim download location...'
Write-Output "Select a folder to download the PX4 installer..."
$download_folder = GetFolder 'Select location to download PX4 installer...'

# AirSim

Invoke-Expression "cmd /c start powershell -noexit -Command 'cd $airsim_folder; git clone https://github.com/Microsoft/AirSim.git'"

# Output a guide for installing Visual Studio and building AirSim
Write-Output "" "You will need Visual Studio to build AirSim." "Download it from here (and make sure select the 'C++ Development Pack' and check 'Windows SDK 10' while installing):"
Write-Output "      https://visualstudio.microsoft.com/vs/community/"
Write-Output "" "Then, open 'x64 Native Tools Command Prompt for VS 2022' and run the following:" "" "cd $airsim_folder\AirSim; .\build.cmd" ""
Write-Output "Note: Building AirSim may take a while."

# PX4

if (-not(Test-Path -Path $download_folder\$px4_installer_name -PathType Leaf)) {
    Write-Output "" "Installing the PX4 installer!"
    Invoke-WebRequest -URI "https://github.com/PX4/PX4-windows-toolchain/releases/download/v0.9/PX4.Windows.Cygwin.Toolchain.0.9.msi" -OutFile "$download_folder\$px4_installer_name"
} else {
    Write-Output "" "You already have the PX4 installer downloaded!"
}

Write-Output "The PX4 installer was installed: opening installer now."
Invoke-Expression "Start-Process $download_folder\$px4_installer_name -Wait"

Write-Output "" "Everything is downloaded!"

Write-Output "" "You will also need Unreal Engine 4.27. Download the Epic Games Launcher and get Unreal Engine." "Note: you must get version 4.27 --- Unreal Engine 5 does not work with AirSim"