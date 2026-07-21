@echo off
rem ====================================
rem   Store System - Backend Starter
rem   No Chinese in this file (CMD bug)
rem ====================================

color 0A
title Store System - Backend

echo.
echo ====================================
echo   Backend Service (Port 8000)
echo ====================================
echo.
echo Do NOT close this window!
echo.

cd /d "%~dp0backend"

"C:\Users\37171\.workbuddy\binaries\python\envs\store-system\Scripts\python.exe" -m uvicorn main:app --reload

if errorlevel 1 (
    echo.
    echo [ERROR] Backend failed to start!
    pause
)
