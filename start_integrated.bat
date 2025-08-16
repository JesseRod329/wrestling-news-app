@echo off
echo ========================================
echo Starting Integrated Wrestling Application
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: Please run this script from the prostats root directory
    echo Current directory: %CD%
    echo.
    echo Please navigate to the prostats folder and try again
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
cd backend
pip install -r requirements_integrated.txt
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install Python dependencies
    echo Please check your Python installation and try again
    pause
    exit /b 1
)

echo [2/4] Installing frontend dependencies...
cd ..\frontend
npm install
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    echo Please check your Node.js installation and try again
    pause
    exit /b 1
)

echo [3/4] Starting backend server...
cd ..\backend
start "Backend Server" cmd /k "python run_integrated.py"
echo Backend server starting... waiting 5 seconds
timeout /t 5 /nobreak > nul

echo [4/4] Starting frontend...
cd ..\frontend
start "Frontend" cmd /k "npm start"
echo.
echo ========================================
echo Both servers are starting up!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul
