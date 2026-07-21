@echo off
chcp 65001 >nul
title 小卖部系统 - 一键启动
color 0E

echo ============================================
echo    小卖部销售管理系统 - 一键启动
echo ============================================
echo.
echo 即将打开两个窗口：
echo   1) 后端服务 (端口 8000)
echo   2) 前端服务 (端口 5173)
echo.
echo 两个窗口都不要关闭！
echo 几秒后浏览器会自动打开
echo 访问地址: http://localhost:5173
echo.
echo ============================================
echo 5 秒后自动开始...
echo 如果不想等，按任意键立即开始
echo.
timeout /t 5 /nointerrupt >nul

:: 启动后端（新窗口）
start "后端-小卖部系统" cmd /k "cd /d \"%~dp0\" && 启动后端.bat"

:: 等待 3 秒再启动前端
timeout /t 3 /nointerrupt >nul

:: 启动前端（新窗口）
start "前端-小卖部系统" cmd /k "cd /d \"%~dp0\" && 启动前端.bat"

:: 等待前端启动后自动打开浏览器
timeout /t 8 /nointerrupt >nul
start "" "http://localhost:5173"

echo.
echo 已启动完成！浏览器已打开
echo 关闭服务请直接关闭对应的窗口
echo.
pause
