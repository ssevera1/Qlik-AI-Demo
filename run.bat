@echo off
echo ============================================
echo  Qlik Cloud AI/ML Capabilities Demo
echo ============================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install dependencies if needed
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

:: Disable all Streamlit telemetry
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

:: Run the app (localhost only - not discoverable on LAN)
echo Starting Streamlit app on localhost only...
streamlit run app.py --server.address 127.0.0.1 --server.headless true
