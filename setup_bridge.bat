@echo off
echo [Setup] Checking Python environment...

REM Check if python is available
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [Error] Python is not installed or not in PATH. Please install Python 3.8+.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
IF NOT EXIST ".venv" (
    echo [Setup] Creating virtual environment...
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
if EXIST "requirements.txt" (
    echo [Setup] Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

REM Install DevilMCP requirements if possible
IF EXIST "C:\Users\dasbl\PycharmProjects\DevilMCP\requirements.txt" (
    echo [Setup] Installing DevilMCP dependencies...
    pip install -r "C:\Users\dasbl\PycharmProjects\DevilMCP\requirements.txt"
)

echo.
echo [Setup] Complete. To use the bridge:
echo    1. .venv\Scripts\activate
echo    2. python bridge.py [agent] [template] ...
echo.
pause
