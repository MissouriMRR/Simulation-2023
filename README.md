# Simulation-2023
Missouri S&amp;T Multirotor Design Team's simulation environments for our 2023 competitions: the 2023 Student Unmanned Aerial Systems Competition (SUAS 2023) and the 2023 Argonia Cup Competition.

## Environment Setup

Before doing anything, you should install all of the necessary programs. You can try running `scripts\install.ps1` if you're on Windows (or have access to PowerShell), but it hasn't been extensively tested (because downloading/building takes a *long* time). Just in case it doesn't work (or you'd rather not try it), you'll need the following programs (it is recommended you download them in the order listed):

- [git](https://git-scm.com)
- [poetry (python)](https://python-poetry.org)
- [Visual Studio](https://visualstudio.microsoft.com)
    - make sure to select the `C++ Development Pack` and check `Windows SDK 10`. This is required for the next steps
- [Microsoft AirSim](https://github.com/Microsoft/AirSim)
    - Clone repo to desired location
    - open `x64 Native Tools Command Prompt for VS 20XX` (just search 'x64 Native Tools' in the Windows search bar and the correct program should appear)
    - navigate to where you installed AirSim in `x64 Native Tools Command Prompt for VS 20XX` and run `.\build.cmd`
- [PX4](https://github.com/PX4/PX4-windows-toolchain/releases/download/v0.9/PX4.Windows.Cygwin.Toolchain.0.9.msi)
    - run the installer (the `.msi` file) after downloading
- [Unreal Engine 4.27](https://www.unrealengine.com/en-US/?utm_source=GoogleSearch&utm_medium=Performance&utm_campaign=%7Bcampaigname%7D&utm_id=17086214833&sub_campaign=&utm_content=&utm_term=unreal%20engine)
   - if you already have the Epic Games Launcher, then you can download it from there under 'Unreal Engine'
