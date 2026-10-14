@echo off
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0start_yolo_desktop.ps1"
exit /b %errorlevel%