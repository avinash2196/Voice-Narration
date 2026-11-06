@echo off
REM Start Frontend with proper environment

echo.
echo ============================================
echo Voice-Narration Frontend Launcher
echo ============================================
echo.

REM Change to frontend directory
cd frontend

echo ============================================
echo Starting Frontend on port 5173
echo ============================================
echo.

call npm run dev

pause
