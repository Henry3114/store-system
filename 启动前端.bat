@echo off
chcp 65001 >nul
title 小卖部系统 - 前端服务
color 0B

echo ============================================
echo    小卖部销售管理系统 - 前端服务
echo ============================================
echo.
echo [2/2] 正在启动前端 (端口 5173)...
echo.
echo 等待几秒后浏览器会自动打开
echo 访问地址: http://localhost:5173
echo.
echo ============================================
echo.

cd /d "%~dp0frontend"
"C:\Program Files\nodejs\npm.cmd" run dev

if errorlevel 1 (
    echo.
    echo [错误] 前端启动失败！请截图发给开发者
    pause
)
