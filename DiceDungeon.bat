@echo off
title Dice Dungeon Launcher
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

REM --- Initialize ---
set "PYTHON_CMD="
set "TMPFILE=%TEMP%\_pycheck.txt"

REM --- Test python ---
python --version >"%TMPFILE%" 2>&1
findstr /i "Python" "%TMPFILE%" >nul && (
    findstr /i "Store" "%TMPFILE%" >nul || set "PYTHON_CMD=python"
)

REM --- Test py if python failed ---
if not defined PYTHON_CMD (
    py --version >"%TMPFILE%" 2>&1
    findstr /i "Python" "%TMPFILE%" >nul && set "PYTHON_CMD=py"
)

del "%TMPFILE%" 2>nul

REM --- Handle no Python found ---
if not defined PYTHON_CMD (
    echo [!] No valid Python installation detected.
    set /p choice="Do you want to download and install Python now? (Y/N): "
    if /i "%choice%"=="Y" (
        echo Downloading Python installer...
        powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe -OutFile python_installer.exe"
        if exist python_installer.exe (
            echo Installing Python silently...
            start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
            del python_installer.exe
            echo Installation complete! Restart this launcher.
            pause
            exit /b
        ) else (
            echo [!] Download failed.
            pause
            exit /b
        )
    ) else (
        echo Installation canceled.
        pause
        exit /b
    )
)

echo Starting Dice Dungeon with !PYTHON_CMD!...
"!PYTHON_CMD!" "%~dp0Main.py"
if errorlevel 1 (
    echo.
    echo [!] The game crashed or Python returned an error.
    echo Press any key to close this window.
    pause >nul
)
exit
