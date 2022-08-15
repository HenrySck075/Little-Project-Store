cls
@echo off
title Command Panel
set cdir="%~dp0
goto main

:main
cls
set cdir=%~dp0
echo Adjust your computer's settings
cmdmenusel  f0f0 "Advanced: Add this shit to Desktop context menu" "Advanced: Remove this madlad from Desktop context menu" "Personalization" "System Information" "User Accounts"
if %ERRORLEVEL%  == 1 context add
if %ERRORLEVEL%  == 2 context del
if %ERRORLEVEL%  == 3 "%cdir%/Tools/Personalization/main.bat"
if %ERRORLEVEL%  == 4 "%cdir%/Tools/System Propeties/main.bat"
if %ERRORLEVEL%  == 5 "%cdir%/Tools/User Account/main.bat"