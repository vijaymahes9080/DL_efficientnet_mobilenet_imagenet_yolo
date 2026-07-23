@echo off
title Neural Synergy - Creative Adaptive React Dashboard
echo ==================================================
echo   LAUNCHING NEURAL SYNERGY REACT WEB DASHBOARD
echo ==================================================
echo.
cd /d "%~dp0"

if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies for React Vite application...
    call npm install
)

echo [INFO] Building React production distribution...
call npm run build

echo [INFO] Starting Python Inference Backend Server...
python server.py
pause
