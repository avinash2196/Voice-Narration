@echo off
REM Start Voice-Narration Services with proper environment

echo.
echo ============================================
echo Voice-Narration Service Launcher
echo ============================================
echo.

REM Set environment variables
set VOICE_SERVICE_PORT=8002

echo Environment Variables:
echo  VOICE_SERVICE_PORT=%VOICE_SERVICE_PORT%
echo.

REM Change to voice_narration directory
cd voice_narration

echo ============================================
echo Starting Voice Service on port 8002
echo ============================================
echo.

python -m voice_narration.simple_voices

pause
