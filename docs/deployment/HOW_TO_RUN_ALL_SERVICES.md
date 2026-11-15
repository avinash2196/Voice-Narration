# 🚀 How to Run All Voice-Narration Services

## 📋 Services Overview

The Voice-Narration platform has **6 modular FastAPI services** plus supporting infrastructure:

| # | Service | Port | Purpose | Status |
|---|---------|------|---------|--------|
| 1 | **Auth Service** | 8001 | User authentication & token management | ✅ M014 |
| 2 | **Voices/Artifacts Service** | 8002 | Voice sample storage & metadata | ✅ M016 |
| 3 | **Jobs Service** | 8003 | Job orchestration & persistence | ✅ M017 |
| 4 | **Consent Service** | 8004 | User consent & privacy management | ✅ M018 |
| 5 | **Inference Service** | 8005 | TTS inference with multi-provider support | ✅ M020/M024 |
| 6 | **AI Evaluation Service** | 8006 | Acoustic quality assessment | ✅ M015 |
| 🗄️ | **PostgreSQL Database** | 5432 | Persistent data storage | ✅ M013 |

---

## 🎯 Quick Start (3 Minutes)

### Option A: Run Everything at Once (Docker Compose)

```powershell
cd "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration"

# Start all services + database
docker-compose -f compose.harness.yaml up -d

# Verify they're running
docker-compose ps

# View logs
docker-compose logs -f
```

✅ **All 6 services + PostgreSQL running**  
✅ **All ports accessible**  
✅ **Database initialized**  

### Option B: Run Individual Services (Python)

```powershell
# Terminal 1: Start PostgreSQL
docker run -d -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=harness postgres:18.6

# Terminal 2: Auth Service
cd "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration"
$env:INFERENCE_PROVIDER = "mock"
python -m uvicorn voice_narration.auth.application:app --port 8001

# Terminal 3: Jobs Service
python -m uvicorn voice_narration.jobs.application:app --port 8003

# Terminal 4: Inference Service (TTS)
python -m uvicorn voice_narration.inference.application:app --port 8005

# Terminal 5: Voices/Artifacts Service
python -m uvicorn voice_narration.voices.application:app --port 8002

# Terminal 6: Consent Service
python -m uvicorn voice_narration.consent.application:app --port 8004

# Terminal 7: AI Evaluation Service
python -m uvicorn voice_narration.ai.application:app --port 8006
```

---

## 🔧 Detailed Service Setup

### **1️⃣ Database (PostgreSQL)**

**Purpose:** Persistent storage for all services

**Start database:**
```powershell
# Docker (Recommended)
docker run -d `
  -p 127.0.0.1:5432:5432 `
  -e POSTGRES_USER=harness `
  -e POSTGRES_PASSWORD=harness `
  -e POSTGRES_DB=harness `
  --name voice-narration-db `
  postgres:18.6

# Verify
docker ps | Select-String postgres
```

**Or using docker-compose:**
```powershell
docker-compose -f compose.harness.yaml up postgres -d
```

**Test connection:**
```powershell
psql -h 127.0.0.1 -U harness -d harness -c "SELECT version();"
```

---

### **2️⃣ Auth Service (Port 8001)**

**Purpose:** User authentication, tokens, credential validation

**Environment variables:**
```
AUTH_SECRET=your-secret-key-here
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

**Start:**
```powershell
cd "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration"
python -m uvicorn voice_narration.auth.application:app --port 8001 --reload
```

**Test:**
```powershell
curl -X POST http://localhost:8001/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"user@example.com\", \"password\": \"pass123\"}'
```

---

### **3️⃣ Jobs Service (Port 8003)**

**Purpose:** Job orchestration, task queuing, status tracking

**Environment variables:**
```
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

**Start:**
```powershell
python -m uvicorn voice_narration.jobs.application:app --port 8003 --reload
```

**Test:**
```powershell
curl -X POST http://localhost:8003/jobs `
  -H "Content-Type: application/json" `
  -d '{\"type\": \"inference\", \"status\": \"pending\"}'
```

---

### **4️⃣ Inference Service (Port 8005) ⭐ M024 GREEN**

**Purpose:** Text-to-Speech inference with Google TTS, Azure Speech, or Mock

**Environment variables:**
```
INFERENCE_PROVIDER=google              # or "azure" or "mock"
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
# OR for Azure:
AZURE_SPEECH_KEY=your-key
AZURE_SPEECH_REGION=eastus
```

**Start:**
```powershell
$env:INFERENCE_PROVIDER = "mock"       # Use mock for testing without credentials
python -m uvicorn voice_narration.inference.application:app --port 8005 --reload
```

**Test with Mock:**
```powershell
# List backends
curl http://localhost:8005/inference/backends

# Submit inference job
curl -X POST http://localhost:8005/inference/jobs/job-123/infer `
  -H "Content-Type: application/json" `
  -d '{
    \"script\": \"Hello, world!\",
    \"voice_id\": \"en-US-Neural2-A\"
  }'

# Get output
curl http://localhost:8005/inference/jobs/job-123/output
```

**Test with Google TTS (requires credentials):**
```powershell
# Set environment
$env:INFERENCE_PROVIDER = "google"
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"

# Start service
python -m uvicorn voice_narration.inference.application:app --port 8005

# Same tests as above will now use real Google TTS
```

---

### **5️⃣ Voices/Artifacts Service (Port 8002)**

**Purpose:** Voice sample management, metadata storage

**Environment variables:**
```
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
STORAGE_PATH=C:\voice_samples  # Local storage for audio files
```

**Start:**
```powershell
python -m uvicorn voice_narration.voices.application:app --port 8002 --reload
```

**Test:**
```powershell
# Upload voice sample
curl -X POST http://localhost:8002/voices/upload `
  -F "file=@C:\path\to\sample.wav" `
  -F "voice_id=hindi-speaker-001"

# List voices
curl http://localhost:8002/voices/list
```

---

### **6️⃣ Consent Service (Port 8004)**

**Purpose:** User consent tracking, privacy policy acknowledgment

**Environment variables:**
```
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

**Start:**
```powershell
python -m uvicorn voice_narration.consent.application:app --port 8004 --reload
```

**Test:**
```powershell
# Record consent
curl -X POST http://localhost:8004/consent/record `
  -H "Content-Type: application/json" `
  -d '{
    \"user_id\": \"user-123\",
    \"consent_type\": \"voice_usage\",
    \"accepted\": true
  }'
```

---

### **7️⃣ AI Evaluation Service (Port 8006)**

**Purpose:** Acoustic quality assessment (speech presence, SNR, clipping detection)

**Environment variables:**
```
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

**Start:**
```powershell
python -m uvicorn voice_narration.ai.application:app --port 8006 --reload
```

**Test:**
```powershell
# Evaluate audio quality
curl -X POST http://localhost:8006/evaluate `
  -H "Content-Type: application/json" `
  -d '{
    \"audio_path\": \"C:\path\to\sample.wav\",
    \"language\": \"hi\"
  }'
```

---

## 🚀 Full Stack Startup (All Services)

### **Method 1: Docker Compose (Recommended)**

```powershell
cd "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration"

# Create environment file
$env_content = @"
INFERENCE_PROVIDER=mock
DATABASE_URL=postgresql://harness:harness@postgres:5432/harness
AUTH_SECRET=dev-secret-key
"@
Set-Content -Path ".env" -Value $env_content

# Start all services
docker-compose -f compose.harness.yaml up -d

# Verify all running
docker-compose ps

# View unified logs
docker-compose logs -f
```

**What happens:**
```
✅ PostgreSQL starts on 127.0.0.1:5432
✅ Schema initialized
✅ All 6 services start on 8001-8006
✅ Services connect to database
✅ Ready for API calls
```

### **Method 2: Manual Startup (Development)**

```powershell
cd "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration"

# Terminal 1: Database
docker run -d -p 127.0.0.1:5432:5432 `
  -e POSTGRES_USER=harness `
  -e POSTGRES_PASSWORD=harness `
  -e POSTGRES_DB=harness `
  postgres:18.6

# Wait 5 seconds for DB to start
Start-Sleep -Seconds 5

# Terminal 2: Set environment (keep open)
$env:INFERENCE_PROVIDER = "mock"
$env:DATABASE_URL = "postgresql://harness:harness@127.0.0.1:5432/harness"

# Terminal 3: Auth Service
python -m uvicorn voice_narration.auth.application:app --port 8001 --reload

# Terminal 4: Jobs Service
python -m uvicorn voice_narration.jobs.application:app --port 8003 --reload

# Terminal 5: Inference Service (TTS)
python -m uvicorn voice_narration.inference.application:app --port 8005 --reload

# Terminal 6: Voices Service
python -m uvicorn voice_narration.voices.application:app --port 8002 --reload

# Terminal 7: Consent Service
python -m uvicorn voice_narration.consent.application:app --port 8004 --reload

# Terminal 8: AI Evaluation Service
python -m uvicorn voice_narration.ai.application:app --port 8006 --reload
```

---

## 📊 Service Status Check

```powershell
# Check all services are responding
@(8001, 8002, 8003, 8004, 8005, 8006) | ForEach-Object {
    $port = $_
    try {
        $response = curl -s "http://localhost:$port/docs" -o $null
        Write-Host "✅ Port $port: OK" -ForegroundColor Green
    } catch {
        Write-Host "❌ Port $port: NOT RESPONDING" -ForegroundColor Red
    }
}

# Or test with health endpoints
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
curl http://localhost:8006/health
```

---

## 🔄 Complete Workflow Example

### **Generate TTS Audio End-to-End**

```powershell
# 1. Auth: Get token
$auth_response = curl -s -X POST http://localhost:8001/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }' | ConvertFrom-Json

$token = $auth_response.token
Write-Host "✅ Got auth token: $token"

# 2. Consent: Record user consent
curl -s -X POST http://localhost:8004/consent/record `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{
    "user_id": "user-123",
    "consent_type": "voice_usage",
    "accepted": true
  }'
Write-Host "✅ Consent recorded"

# 3. Jobs: Create inference job
$job_response = curl -s -X POST http://localhost:8003/jobs `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{
    "type": "inference",
    "script": "नमस्ते। कृपया प्रतीक्षा करें।",
    "voice_id": "hi-IN-Neural2-A"
  }' | ConvertFrom-Json

$job_id = $job_response.job_id
Write-Host "✅ Created job: $job_id"

# 4. Inference: Submit TTS job
$infer_response = curl -s -X POST http://localhost:8005/inference/jobs/$job_id/infer `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{
    "script": "नमस्ते। कृपया प्रतीक्षा करें।",
    "voice_id": "hi-IN-Neural2-A"
  }' | ConvertFrom-Json

Write-Host "✅ Inference submitted: $($infer_response.status)"
Write-Host "   Duration: $($infer_response.duration_seconds)s"

# 5. Artifacts: Store generated audio
$output_response = curl -s -X GET http://localhost:8005/inference/jobs/$job_id/output `
  -H "Authorization: Bearer $token" | ConvertFrom-Json

Write-Host "✅ Got audio output: $($output_response.format), $($output_response.duration_seconds)s"

# 6. AI Evaluation: Check audio quality
$eval_response = curl -s -X POST http://localhost:8006/evaluate `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d "{
    \"audio_path\": \"output.wav\",
    \"language\": \"hi\"
  }" | ConvertFrom-Json

Write-Host "✅ Audio quality evaluation:"
Write-Host "   Speech Presence: $($eval_response.speech_presence)%"
Write-Host "   SNR: $($eval_response.snr) dB"
Write-Host "   Status: $($eval_response.quality_status)"
```

---

## 🧪 Run Tests While Services Running

```powershell
# In a separate terminal, run tests
cd "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration"

# Test M023 (Linguistic Chunking)
pytest tests/test_linguistic_chunking_and_controls.py -v

# Test M022 (Provider Registry)
pytest tests/test_provider_registry.py -v

# Test M020 (Inference Adapter)
pytest tests/test_inference_adapter.py -v

# Test all
pytest -v
```

**Services keep running while tests execute** ✅

---

## 🛑 Stopping Services

### **Docker Compose:**
```powershell
# Stop all services
docker-compose down

# Stop + remove volumes
docker-compose down -v
```

### **Manual (Ctrl+C in each terminal):**
```powershell
# Kill all Python processes
Get-Process python | Stop-Process -Force

# Stop database
docker stop voice-narration-db
docker rm voice-narration-db
```

---

## 📝 Environment Variables Summary

### **For Mock Provider (Testing - No Credentials Needed)**

```
INFERENCE_PROVIDER=mock
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

### **For Google Cloud TTS**

```
INFERENCE_PROVIDER=google
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

### **For Azure Speech**

```
INFERENCE_PROVIDER=azure
AZURE_SPEECH_KEY=your-api-key
AZURE_SPEECH_REGION=eastus
DATABASE_URL=postgresql://harness:harness@127.0.0.1:5432/harness
```

---

## 🐛 Troubleshooting

### **"Connection refused" on port 8001-8006**

```powershell
# Check if service is running
Get-Process python | Select-Object Name, Id

# Check if port is listening
netstat -ano | findstr ":8001"

# Start service manually
python -m uvicorn voice_narration.inference.application:app --port 8005
```

### **Database connection error**

```powershell
# Check postgres is running
docker ps | Select-String postgres

# Start postgres
docker run -d -p 127.0.0.1:5432:5432 `
  -e POSTGRES_PASSWORD=harness `
  postgres:18.6

# Verify connection
psql -h 127.0.0.1 -U harness -d harness -c "SELECT 1"
```

### **Module not found error**

```powershell
# Install dependencies
pip install -r requirements-dev.txt

# Or reinstall everything
pip install --upgrade -r requirements-dev.txt
```

### **Google TTS auth failing**

```powershell
# Verify credentials file exists
ls "C:\path\to\service-account.json"

# Verify environment variable is set
echo $env:GOOGLE_APPLICATION_CREDENTIALS

# Test auth manually
python -c "
from google.cloud import tts_v1
client = tts_v1.TextToSpeechClient()
print('✅ Google Cloud auth works!')
"
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│              Client Application                      │
│           (Web Browser / Mobile App)                 │
└────────────────────┬────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐    ┌──────▼──────┐   ┌─────▼─────┐
│ Auth  │    │  Jobs       │   │ Inference │
│ 8001  │    │  8003       │   │ (TTS)     │
└───┬───┘    └──────┬──────┘   │ 8005      │
    │               │          └─────┬─────┘
    │    ┌──────────┼──────────┐     │
    │    │          │          │     │
┌───▼────▼──────┐   │   ┌──────▼───┐ │
│  Consent      │   │   │ Voices/  │ │
│  8004         │   │   │ Artifacts│ │
└───────────────┘   │   │ 8002     │ │
                    │   └──────────┘ │
                ┌───▼──────┐    ┌────▼───┐
                │  AI Eval │    │ (Google│
                │  8006    │    │  TTS)  │
                └──────────┘    └────────┘
                    │               │
        ┌───────────▼───────────┬───▼────────┐
        │  PostgreSQL           │  External  │
        │  (Data Layer)         │  TTS API   │
        │  127.0.0.1:5432       │  (Real)    │
        └───────────────────────┴────────────┘
```

---

## ✅ Quick Checklist

- [ ] PostgreSQL running on 127.0.0.1:5432
- [ ] Auth Service running on 8001
- [ ] Jobs Service running on 8003
- [ ] Inference Service running on 8005
- [ ] Voices Service running on 8002
- [ ] Consent Service running on 8004
- [ ] AI Evaluation Service running on 8006
- [ ] All services responding to health checks
- [ ] Tests passing with services running
- [ ] Can submit end-to-end inference job

---

## 🚀 What's Next?

1. **Start with Docker Compose** (easiest):
   ```powershell
   docker-compose -f compose.harness.yaml up -d
   ```

2. **Set Google TTS credentials** (when ready):
   ```powershell
   $env:INFERENCE_PROVIDER = "google"
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
   # Restart Inference service
   ```

3. **Run tests to verify**:
   ```powershell
   pytest tests/test_linguistic_chunking_and_controls.py -v
   ```

4. **Test real inference**:
   ```powershell
   # Generate audio with your selected TTS provider
   curl -X POST http://localhost:8005/inference/jobs/test-123/infer \
     -H "Content-Type: application/json" \
     -d '{"script": "नमस्ते", "voice_id": "hi-IN-Neural2-A"}'
   ```

---

**You're all set! 🎉 All services are ready to run.** Start with Docker Compose and go from there!
