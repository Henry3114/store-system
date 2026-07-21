@echo off
rem ====================================
rem   Store System - Frontend Starter
rem   No Chinese in this file (CMD bug)
rem ====================================

color 0B
title Store System - Frontend

echo.
echo ====================================
echo   Frontend Service (Port 5173)
echo   Wait 5-10 seconds for browser
echo ====================================
echo.
echo Do NOT close this window!
echo.

cd /d "%~dp0frontend"

"C:\Program Files\nodejs\npm.cmd" run dev

if errorlevel 1 (
    echo.
    echo [ERROR] Frontend failed to start!
    echo.
    echo Run 'npm install' first if you see missing packages
    pause
)
