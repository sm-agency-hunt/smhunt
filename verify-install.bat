@echo off
REM SMHUNT Platform - Installation Verification Script
REM This script checks if all components are properly installed

echo ============================================
echo   SMHUNT Platform Installation Check
echo ============================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python is installed
    python --version
) else (
    echo ✗ Python not found! Please install Python 3.9+
    goto :python_error
)
echo.

REM Check Node.js
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Node.js is installed
    node --version
) else (
    echo ✗ Node.js not found! Please install Node.js
    goto :node_error
)
echo.

REM Check frontend dependencies
echo [3/5] Checking frontend dependencies...
cd frontend
if exist "node_modules" (
    echo ✓ Frontend dependencies installed
) else (
    echo ✗ Frontend dependencies missing!
    echo Installing...
    call npm install
    if %errorlevel% equ 0 (
        echo ✓ Installation complete
    ) else (
        echo ✗ Installation failed!
        goto :npm_error
    )
)
cd ..
echo.

REM Check backend dependencies
echo [4/5] Checking backend dependencies...
python -c "import fastapi" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend dependencies installed
) else (
    echo ✗ Backend dependencies missing!
    echo Installing...
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✓ Installation complete
    ) else (
        echo ✗ Installation failed!
        goto :pip_error
    )
)
echo.

REM Check file structure
echo [5/5] Verifying file structure...
set "errors=0"

if not exist "frontend\src\components\Navbar.js" (
    echo ✗ Missing: Navbar component
    set /a errors+=1
) else (
    echo ✓ Found: Navbar component
)

if not exist "frontend\src\pages\LeadSearch.js" (
    echo ✗ Missing: Lead Search page
    set /a errors+=1
) else (
    echo ✓ Found: Lead Search page
)

if not exist "frontend\src\pages\AIAgent.js" (
    echo ✗ Missing: AI Agent page
    set /a errors+=1
) else (
    echo ✓ Found: AI Agent page
)

if not exist "src\services\ai\ai_lead_agent.py" (
    echo ✗ Missing: AI Lead Agent service
    set /a errors+=1
) else (
    echo ✓ Found: AI Lead Agent service
)

if not exist "src\api\v1\routers\ai_agent.py" (
    echo ✗ Missing: AI Agent API router
    set /a errors+=1
) else (
    echo ✓ Found: AI Agent API router
)

echo.
echo ============================================
echo   Installation Check Complete
echo ============================================
echo.

if %errors% equ 0 (
    echo ✓ ALL CHECKS PASSED!
    echo.
    echo Your SMHUNT platform is ready!
    echo.
    echo Next steps:
    echo 1. Start frontend: cd frontend ^&^& npm start
    echo 2. Start backend: python main.py
    echo 3. Open browser: http://localhost:3000
    echo.
) else (
    echo ✗ %errors% check(s) failed!
    echo Please review the errors above.
    echo.
)

echo ============================================
pause
exit /b 0

:python_error
echo.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
pause
exit /b 1

:node_error
echo.
echo Please install Node.js from https://nodejs.org/
pause
exit /b 1

:npm_error
echo.
echo Failed to install npm dependencies
echo Try running: cd frontend ^&^& npm install
pause
exit /b 1

:pip_error
echo.
echo Failed to install pip dependencies
echo Try running: pip install -r requirements.txt
pause
exit /b 1
