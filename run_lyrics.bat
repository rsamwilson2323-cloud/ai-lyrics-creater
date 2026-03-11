@echo off
cd /d "%~dp0"
start cmd /k py -3.10 app.py
timeout /t 3 >nul
start http://127.0.0.1:5000
