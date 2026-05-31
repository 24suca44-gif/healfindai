@echo off
echo Starting HealFind AI Backend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create templates directory and copy HTML file
if not exist "templates" mkdir templates
copy "index.html" "templates\" >nul 2>&1

REM Run the Flask application
echo.
echo Starting HealFind AI server...
echo Open your browser and go to: http://localhost:5000
echo.
cd backend
python app.py

pause