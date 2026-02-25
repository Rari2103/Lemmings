@echo off
REM Safety Check Before Git Commit

title Git Safety Check

echo ============================================================
echo           GIT SAFETY CHECK - SENSITIVE FILES
echo ============================================================
echo.

cd /d "%~dp0"

echo Checking for sensitive files that should NOT be committed:
echo.

REM Check for .env files
if exist .env (
    echo WARNING: .env file found!
    echo   This contains your API key!
    echo   Make sure .gitignore is protecting it!
    echo.
)

REM Check git status
echo Running git status...
echo.
git status --short

echo.
echo ============================================================
echo IMPORTANT: DO NOT COMMIT THESE FILES:
echo ============================================================
echo   X .env
echo   X Any files with "private_key" in name
echo   X agent_state_*.json
echo   X *.key files
echo.
echo SAFE TO COMMIT:
echo   OK .py files (code)
echo   OK .bat files (launchers)
echo   OK .md/.txt files (docs)
echo   OK requirements.txt
echo   OK templates/*.html
echo.
echo ============================================================
echo To commit safely:
echo   1. Verify .gitignore is protecting secrets
echo   2. git add [specific files]
echo   3. git commit -m "your message"
echo   4. git push
echo ============================================================
echo.
pause
