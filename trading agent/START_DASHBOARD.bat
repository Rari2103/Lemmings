@echo off
REM AI Trading Agent - Enhanced Dashboard Launcher
REM Double-click this file to start!

title AI Trading Agent - Enhanced Dashboard

echo ============================================================
echo           AI TRADING AGENT - STARTING...
echo ============================================================
echo.
echo Features:
echo   - Real wallet balance (your 29 USDC)
echo   - Agent health (GMAC energy)
echo   - Trading signals
echo   - Performance tracking
echo   - Trade history
echo.

cd /d "%~dp0"

echo Opening web dashboard...
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo Starting enhanced server...
python enhanced_ui.py

pause
