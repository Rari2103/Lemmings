@echo off
REM Setup Private Key for Live Trading

title AI Trading Agent - Private Key Setup

echo ============================================================
echo           PRIVATE KEY SETUP FOR LIVE TRADING
echo ============================================================
echo.
echo This will configure your wallet for live trading.
echo Your private key will be stored SECURELY in .env file.
echo.
echo NEVER share your private key or .env file!
echo.

cd /d "%~dp0"

python setup_private_key.py

echo.
pause
