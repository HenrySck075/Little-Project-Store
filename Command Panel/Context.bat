cls
@echo off
if "%1" == "add" goto contextmenu
if "%1" == "del" goto contextremove
if "%1" == "" echo wdym && timeout 69420 && exit /b

:contextmenu
echo -----------Command execution section-----------
reg add HKCR\DesktopBackground\Shell\ConCmd /v Icon /t REG_SZ /f /d control.exe
reg add HKCR\DesktopBackground\Shell\ConCmd /v MUIVerb /t REG_SZ /f /d "Control Panel with no graphics"
reg add HKCR\DesktopBackground\Shell\ConCmd /v Position /t REG_SZ /f /d Bottom
reg add HKCR\DesktopBackground\Shell\ConCmd /v SubCommands /t REG_SZ /f

:: Add this
set cdir="%~dp0ConCmd.bat

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\01Main /v Icon /t REG_SZ /f /d control.exe
reg add HKCR\DesktopBackground\Shell\ConCmd\shell\01Main /v MUIVerb /t REG_SZ /f /d Main

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\01Main\Command /ve /t REG_SZ /f /d %cdir%

:: Add Personalization section
set cdir="%~dp0Tools\Personalization\main.bat

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\02Personalization /v Icon /t REG_SZ /f /d "%systemroot%\system32\themecpl.dll,-1"
reg add HKCR\DesktopBackground\Shell\ConCmd\shell\02Personalization /v MUIVerb /t REG_SZ /f /d Personalization

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\02Personalization\Command /ve /t REG_SZ /f /d %cdir%

:: Add System Information section
set cdir="%~dp0Tools\System Propeties\menu.bat

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\03SysInfo /v Icon /t REG_SZ /f /d "%systemroot%\system32\DDORes.dll,-2102"
reg add HKCR\DesktopBackground\Shell\ConCmd\shell\03SysInfo /v MUIVerb /t REG_SZ /f /d "System Information"

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\03SysInfo\Command /ve /t REG_SZ /f /d %cdir%

:: Add User Account section
set cdir="%~dp0Tools\User Account\main.bat

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\04Users /v Icon /t REG_SZ /f /d "%systemroot%\system32\usercpl.dll,0"
reg add HKCR\DesktopBackground\Shell\ConCmd\shell\04Users /v MUIVerb /t REG_SZ /f /d "User Account"

reg add HKCR\DesktopBackground\Shell\ConCmd\shell\04Users\Command /ve /t REG_SZ /f /d %cdir%

::return
echo -------End of command execution section--------
"%~dp0ConCmd.bat"

:contextremove
reg delete HKCR\DesktopBackground\Shell\ConCmd /f
"%~dp0ConCmd.bat"
