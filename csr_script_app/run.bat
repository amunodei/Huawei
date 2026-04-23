@echo off
setlocal
cd /d "%~dp0"

REM Create a local virtualenv on first run
if not exist ".venv\Scripts\python.exe" (
    echo [setup] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python is not installed or not on PATH.
        echo Install Python 3.10+ from https://www.python.org/downloads/ and try again.
        pause
        exit /b 1
    )
    call ".venv\Scripts\activate.bat"
    echo [setup] Installing dependencies...
    python -m pip install --upgrade pip >nul
    python -m pip install -r requirements.txt
) else (
    call ".venv\Scripts\activate.bat"
)

echo.
echo ============================================
echo  CSR Script Generator running at
echo    http://127.0.0.1:5000
echo  Press Ctrl+C to stop.
echo ============================================
echo.
start "" "http://127.0.0.1:5000"
python app.py
