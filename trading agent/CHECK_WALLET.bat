@echo off
REM Quick Wallet Balance Check
REM Shows your current USDC balance

title Check Wallet Balance

echo ============================================================
echo           CHECKING YOUR WALLET BALANCE
echo ============================================================
echo.

cd /d "%~dp0"

python check_wallet.py

echo.
pause
