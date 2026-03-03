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

:: Run the app
echo Starting Streamlit app...
streamlit run app.py
