@echo off
REM Start Voice-Narration Services with proper environment

echo.
echo ============================================
echo Voice-Narration Service Launcher
echo ============================================
echo.

REM Set environment variables
set INFERENCE_PROVIDER=google
set GOOGLE_APPLICATION_CREDENTIALS=.\service-account-key.json
set VOICE_SERVICE_PORT=8002

echo Environment Variables:
echo  INFERENCE_PROVIDER=%INFERENCE_PROVIDER%
echo  GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS%
echo  VOICE_SERVICE_PORT=%VOICE_SERVICE_PORT%
echo.

REM Change to voice_narration directory
cd voice_narration

echo ============================================
echo Starting Inference Service (TTS) on port 8003
echo ============================================
echo.

python -m voice_narration.inference

pause
