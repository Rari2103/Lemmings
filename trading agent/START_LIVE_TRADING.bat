@echo off
REM Start Live Trading with $10 Limit

title AI Trading Agent - LIVE MODE

echo ============================================================
echo           AI TRADING AGENT - LIVE TRADING MODE
echo ============================================================
echo.
echo WARNING: This uses REAL money!
echo.
echo Features:
echo   - $10 spending limit
echo   - Manual confirmation required
echo   - Emergency stop (Ctrl+C)
echo   - Real blockchain transactions
echo.
echo Make sure you have run SETUP_WALLET.bat first!
echo.

cd /d "%~dp0"

python live_trading.py

echo.
pause
