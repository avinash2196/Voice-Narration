@echo off
REM Start the voice service, the inference service (with Chatterbox) and the
REM frontend, each in its own window. Close a window to stop that service.
REM
REM Settings you can set before running this script to override the defaults:
REM   GOOGLE_APPLICATION_CREDENTIALS  service-account key (default: service-account-key.json here)
REM   CHATTERBOX_URL                  deployed Chatterbox service
REM   CHATTERBOX_TIMEOUT_SECONDS      time limit for one Chatterbox call (default 1200)
REM   INFERENCE_PROVIDER              provider used when a request names none (default google)
REM   DATABASE_URL                    database for generation records (default: local PostgreSQL)
REM   START_ALL_NO_BROWSER            set to any value to skip opening the browser

setlocal
cd /d "%~dp0"

if not defined GOOGLE_APPLICATION_CREDENTIALS set "GOOGLE_APPLICATION_CREDENTIALS=%~dp0service-account-key.json"
if not defined CHATTERBOX_URL set "CHATTERBOX_URL=https://chatterbox-model-api-177206684903.asia-southeast1.run.app"
if not defined CHATTERBOX_TIMEOUT_SECONDS set "CHATTERBOX_TIMEOUT_SECONDS=1200"
if not defined INFERENCE_PROVIDER set "INFERENCE_PROVIDER=google"
set "VOICE_SERVICE_URL=http://localhost:8002"

echo.
echo ============================================
echo Voice-Narration: starting all services
echo ============================================
echo  Voice service      http://localhost:8002
echo  Inference service  http://localhost:8003
echo  Frontend           http://localhost:5173
echo  CHATTERBOX_URL     %CHATTERBOX_URL%
echo  Key file           %GOOGLE_APPLICATION_CREDENTIALS%
echo.

if not exist "%GOOGLE_APPLICATION_CREDENTIALS%" (
  echo WARNING: key file not found. Google narration and Chatterbox cloning
  echo          will fail until GOOGLE_APPLICATION_CREDENTIALS points at it.
  echo.
)

start "Voice service (8002)" cmd /k python -m voice_narration.simple_voices
start "Inference service (8003)" cmd /k python -m voice_narration.inference
start "Frontend (5173)" /d "%~dp0frontend" cmd /k npm run dev

echo Waiting for the frontend to start...
powershell -NoProfile -Command "for ($i = 0; $i -lt 60; $i++) { try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 http://localhost:5173/ | Out-Null; exit 0 } catch { Start-Sleep -Seconds 1 } }; exit 1"
if errorlevel 1 (
  echo The frontend did not answer within 60 seconds. Check the "Frontend (5173)" window.
) else (
  if not defined START_ALL_NO_BROWSER start "" http://localhost:5173/
  echo Ready: http://localhost:5173/
)
echo.
echo Close the three service windows to stop the services.
endlocal
