@echo off
echo Starting NFCe App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with your NOTION_TOKEN and NOTION_DATABASE_ID
    echo.
    pause
)

REM Run the application
echo Running NFCe App...
echo.
cd src
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred while running the application
    pause
)

echo.
echo Application finished
pause