@echo off
chcp 65001 >nul
title 视频文件整理器
color 0A

echo.
echo ========================================
echo        视频文件整理器 v1.0
echo ========================================
echo.
echo 功能说明：
echo 1. 递归查找指定目录下的所有视频文件
echo 2. 将视频文件移动到一级目录
echo 3. 删除空文件夹（仅当文件夹中无任何文件时）
echo.
echo ========================================
echo.

:check_python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python！
    echo 请先安装Python 3.x
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

:run_script
echo 正在启动视频整理器...
echo.
python "%~dp0video_organizer.py"

if %errorlevel% neq 0 (
    echo.
    echo 程序执行出错！
    pause
    exit /b 1
)

echo.
echo 程序执行完成！
pause