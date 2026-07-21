@echo off
rem ====================================
rem   Store System - One Click Start
rem   No Chinese in this file (CMD bug)
rem ====================================

color 0E
title Store System - Starting

echo.
echo ====================================
echo   Store System Starting...
echo ====================================
echo.
echo This will open 2 black windows.
echo Browser will open automatically.
echo.

cd /d "%~dp0"

rem Start backend in new window
start "Store Backend" cmd /k "start-backend.bat"

rem Wait 3 seconds
ping -n 4 127.0.0.1 >nul

rem Start frontend in new window
start "Store Frontend" cmd /k "start-frontend.bat"

rem Wait for frontend to be ready
ping -n 10 127.0.0.1 >nul

rem Open browser
start "" "http://localhost:5173"

echo.
echo Started! Browser should open now.
echo Close the two black windows to stop.
echo.
pause
