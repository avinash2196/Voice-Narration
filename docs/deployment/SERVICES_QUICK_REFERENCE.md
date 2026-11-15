# 🚀 Voice-Narration Services Quick Reference

## TL;DR - Run Everything Now

```powershell
# Option 1: Docker Compose (Recommended - 1 command)
docker-compose -f compose.harness.yaml up -d

# Option 2: Just the database (if running services manually)
docker run -d -p 127.0.0.1:5432:5432 postgres:18.6
```

---

## 📊 What We Have: 7 Services Total

| Service | Port | What It Does | Status |
|---------|------|-------------|--------|
| **Auth** | 8001 | User login & tokens | ✅ Ready |
| **Voices** | 8002 | Store voice samples | ✅ Ready |
| **Jobs** | 8003 | Manage background jobs | ✅ Ready |
| **Consent** | 8004 | Privacy & consent | ✅ Ready |
| **Inference (TTS)** ⭐ | 8005 | Text-to-Speech synthesis | ✅ M024 DONE |
| **AI Evaluation** | 8006 | Audio quality checks | ✅ Ready |
| **PostgreSQL DB** | 5432 | Data storage | ✅ Ready |

---

## 🎯 Start Option 1: Docker Compose (EASIEST)

```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration

# Start all services at once
docker-compose -f compose.harness.yaml up -d

# See them running
docker-compose ps

# Stop them
docker-compose down
```

**Result:** All 7 services running, database initialized, ports ready.

---

## 🎯 Start Option 2: Manual (DEVELOPMENT)

### Terminal 1: Start Database
```powershell
docker run -d `
  -p 127.0.0.1:5432:5432 `
  -e POSTGRES_USER=harness `
  -e POSTGRES_PASSWORD=harness `
  -e POSTGRES_DB=harness `
  postgres:18.6
```

### Terminals 2-7: Start Each Service
```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration

# Terminal 2
python -m uvicorn voice_narration.auth.application:app --port 8001

# Terminal 3
python -m uvicorn voice_narration.voices.application:app --port 8002

# Terminal 4
python -m uvicorn voice_narration.jobs.application:app --port 8003

# Terminal 5
python -m uvicorn voice_narration.consent.application:app --port 8004

# Terminal 6
python -m uvicorn voice_narration.inference.application:app --port 8005

# Terminal 7
python -m uvicorn voice_narration.ai.application:app --port 8006
```

---

## ✅ Verify All Services Running

```powershell
# Check all 6 services respond
curl http://localhost:8001/docs  # Auth
curl http://localhost:8002/docs  # Voices
curl http://localhost:8003/docs  # Jobs
curl http://localhost:8004/docs  # Consent
curl http://localhost:8005/docs  # Inference ⭐
curl http://localhost:8006/docs  # AI Eval

# If you see Swagger docs, that service is running ✅
```

---

## 🧪 Test While Services Running

```powershell
# In a separate terminal (services keep running)
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration

# Run M023 tests (17 tests for linguistic chunking)
pytest tests/test_linguistic_chunking_and_controls.py -v

# Expected: 17 PASSED ✅
```

---

## 🔧 Configure TTS Provider (Pick One)

### Option A: Mock (Testing - No Credentials Needed)
```powershell
$env:INFERENCE_PROVIDER = "mock"
# Services use fake TTS - great for testing
```

### Option B: Google Cloud TTS (Real Audio)
```powershell
$env:INFERENCE_PROVIDER = "google"
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
# Restart Inference service on port 8005
```

### Option C: Azure Speech (Real Audio)
```powershell
$env:INFERENCE_PROVIDER = "azure"
$env:AZURE_SPEECH_KEY = "your-key"
$env:AZURE_SPEECH_REGION = "eastus"
# Restart Inference service on port 8005
```

---

## 📡 Test Inference (TTS) Service

```powershell
# List available backends
curl http://localhost:8005/inference/backends

# Generate audio (with mock provider)
curl -X POST http://localhost:8005/inference/jobs/job-123/infer `
  -H "Content-Type: application/json" `
  -d '{
    "script": "Hello, world!",
    "voice_id": "en-US-Neural2-A"
  }'

# Get the generated audio
curl http://localhost:8005/inference/jobs/job-123/output
```

---

## 🛑 Stop Everything

```powershell
# If using Docker Compose
docker-compose down

# If using manual startup
# Ctrl+C in each terminal, then:
docker stop postgres
docker rm postgres
```

---

## 🐛 Troubleshooting

### Service not responding on port 8001-8006
```powershell
# Check if it's running
Get-Process python | Select-Object Name, Id

# Try port directly
Test-NetConnection -ComputerName localhost -Port 8005
```

### Database connection refused
```powershell
# Check postgres running
docker ps | Select-String postgres

# Restart it
docker run -d -p 127.0.0.1:5432:5432 postgres:18.6
```

### Module not found
```powershell
# Reinstall dependencies
pip install --upgrade -r requirements-dev.txt
```

### Google TTS auth failing
```powershell
# Verify file exists
ls "C:\path\to\service-account.json"

# Test auth
python -c "from google.cloud import tts_v1; client = tts_v1.TextToSpeechClient(); print('✅ OK!')"
```

---

## 📁 Project Structure

```
voice_narration/
├── auth/
│   └── application.py         → Auth service (8001)
├── voices/
│   └── application.py         → Voices service (8002)
├── jobs/
│   └── application.py         → Jobs service (8003)
├── consent/
│   └── application.py         → Consent service (8004)
├── inference/
│   ├── application.py         → Inference service (8005) ⭐
│   ├── production.py          → M024 production code
│   ├── registry.py            → Provider registry
│   └── providers/
│       ├── base.py
│       ├── mock.py            → Mock TTS
│       ├── google.py          → Google Cloud TTS
│       └── azure.py           → Azure Speech
├── ai/
│   └── application.py         → AI Eval service (8006)
```

---

## 🎯 Common Tasks

### Generate Hindi Audio
```powershell
curl -X POST http://localhost:8005/inference/jobs/test-1/infer `
  -H "Content-Type: application/json" `
  -d '{
    "script": "नमस्ते। कृपया प्रतीक्षा करें।",
    "voice_id": "hi-IN-Neural2-A"
  }'
```

### Generate English Audio
```powershell
curl -X POST http://localhost:8005/inference/jobs/test-2/infer `
  -H "Content-Type: application/json" `
  -d '{
    "script": "Hello, this is a test.",
    "voice_id": "en-US-Neural2-A"
  }'
```

### Check Audio Quality
```powershell
curl -X POST http://localhost:8006/evaluate `
  -H "Content-Type: application/json" `
  -d '{
    "audio_path": "output.wav",
    "language": "hi"
  }'
```

---

## 📊 Service Dependencies

```
Client App
    ↓
┌───┴─────────────────────┐
│ Auth (8001)             │
│ - Login & tokens        │
└───┬─────────────────────┘
    │
    ├─→ Jobs (8003)
    │   - Queue inference
    │
    ├─→ Inference (8005) ⭐
    │   - Text→Audio
    │   - Uses Google/Azure/Mock
    │
    ├─→ Voices (8002)
    │   - Store samples
    │
    ├─→ Consent (8004)
    │   - Track permissions
    │
    └─→ AI Eval (8006)
        - Check quality
        
All ↓ depend on PostgreSQL (5432)
```

---

## ✨ What's New (M024)

**Inference Service (Port 8005) now includes:**
- ✅ Linguistic chunking (smart text splitting)
- ✅ Audio joining (seamless concatenation)
- ✅ Pause controls (model-aware)
- ✅ Model licensing (approval + validation)
- ✅ End-to-end workflow

**All 17 M023 tests passing** ✅

---

## 🚀 Next Steps

1. **Start services** with Docker Compose
   ```powershell
   docker-compose -f compose.harness.yaml up -d
   ```

2. **Verify all running** (curl docs endpoints)
   ```powershell
   curl http://localhost:8005/docs  # Inference service
   ```

3. **Run tests** (separate terminal)
   ```powershell
   pytest tests/test_linguistic_chunking_and_controls.py -v
   ```

4. **Add Google TTS credentials** (when ready)
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
   ```

5. **Generate real audio** (with credentials)
   ```powershell
   curl -X POST http://localhost:8005/inference/jobs/test/infer ...
   ```

---

## 📖 Full Documentation

See: `HOW_TO_RUN_ALL_SERVICES.md` for complete details

---

**You're ready to go! 🎉** Start with Docker Compose and everything just works.
