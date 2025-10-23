@echo off
title Dice Dungeon Launcher
setlocal

REM --- Script folder ---
set "DIR=%~dp0"
cd /d "%DIR%"

REM --- Check Python ---
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found.
    set /p choice="Do you want to install Python now? (Y/N): "
    if /i "%choice%"=="Y" (
        ver | findstr /i "Wine" >nul
        if %errorlevel%==0 (
            echo Installing Python in Wine...
            wine msiexec /i "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe" /quiet PrependPath=1 InstallAllUsers=1
        ) else (
            powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe -OutFile python_installer.exe"
            start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
            del python_installer.exe
        )
    ) else (
        echo Installation canceled.
        exit /b
    )
)

REM --- Run game ---
python Main.py
exit
