@echo off
chcp 65001 >nul
title 小卖部系统 - 后端服务
color 0A

echo ============================================
echo    小卖部销售管理系统 - 后端服务
echo ============================================
echo.
echo [1/2] 正在启动后端 (端口 8000)...
echo.
echo 浏览器不要关闭这个窗口！
echo 后端启动后请再双击 "启动前端.bat"
echo.
echo ============================================
echo.

cd /d "%~dp0backend"
"C:\Users\37171\.workbuddy\binaries\python\envs\store-system\Scripts\python.exe" -m uvicorn main:app --reload

if errorlevel 1 (
    echo.
    echo [错误] 后端启动失败！请截图发给开发者
    pause
)
