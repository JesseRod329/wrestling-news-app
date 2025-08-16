@echo off
echo ========================================
echo Starting Working Wrestling Application
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: Please run this script from the prostats root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [1/3] Starting Flask backend server...
cd backend
start "Flask Backend" cmd /k "python wrestling_api.py"
echo Backend server starting... waiting 5 seconds
timeout /t 5 /nobreak > nul

echo [2/3] Installing frontend dependencies...
cd ..\frontend
npm install
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo [3/3] Starting frontend...
start "Frontend" cmd /k "npm start"
echo.
echo ========================================
echo Both servers are starting up!
echo ========================================
echo.
echo Backend: http://localhost:5001
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul
