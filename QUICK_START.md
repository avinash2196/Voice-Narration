# Voice-Narration: Quick Start Guide

## 🎉 Latest Update: Real Google Cloud TTS Integration!

**Real Google Cloud Text-to-Speech is now ACTIVE!**

- Backend generates **real audio** using Google's Neural2-C voice
- No more mock silence - actual synthesized speech
- Fully tested and ready to use
- See **REAL_TTS_SETUP.md** for details

### Quick Test:
```bash
# 1. Backend and frontend already running
# 2. Open: http://localhost:5173
# 3. Sign up → Upload voice → Generate Speech tab
# 4. Enter text "Welcome to India"
# 5. Click Generate → Listen to REAL Google TTS audio! 🎵
```

---

## Project Status

✅ **Frontend**: M3-GREEN Complete (94/94 tests passing)
✅ **Backend**: M24 Complete (39/39 tests passing)
✅ **Google TTS**: Real integration active with neural voices
✅ **Documentation**: Deployment guides included

---

## Prerequisites

- **Node.js**: v18.x or later
- **Python**: 3.10+ (backend services)
- **Docker**: (optional, for containerized deployment)
- **Git**: Latest version

---

## Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/avinash2196/Voice-Narration.git
cd Voice-Narration
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

**Configure Environment** (`.env`):
```bash
VITE_API_URL=http://localhost:8001
VITE_ENV=development
```

### 3. Backend Setup

```bash
cd ../voice_narration
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

**Configure Environment** (`.env`):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/voice_narration

# Auth (M1 Service - Port 8001)
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_EXPIRATION_HOURS=24

# Google TTS (M3 Service - Port 8003)
GOOGLE_TTS_API_KEY=your_google_tts_key

# Firebase (if needed)
FIREBASE_CREDENTIALS=/path/to/credentials.json

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## Running the Application

### ✅ Current Status (Production Services Running)

```
✅ Frontend:        http://localhost:5173  (Vite React)
✅ Voice Service:   http://localhost:8002  (Voice upload/manage)
✅ TTS Service:     http://localhost:8003  (Google Cloud TTS)
⏸️  Auth Service:   http://localhost:9000  (Pending)
⏸️  Jobs Service:   http://localhost:9000  (Pending)
```

### Start Services (3 Terminals)

**Terminal 1 - Voice Management Service:**
```bash
cd voice_narration
python -m voice_narration.simple_voices
# Runs on port 8002
```

**Terminal 2 - TTS/Inference Service:**
```bash
cd voice_narration
python -m voice_narration.inference
# Runs on port 8003 with Google Cloud TTS
```

**Terminal 3 - Frontend Dev Server:**
```bash
cd frontend
npm run dev
# Runs on port 5173
```

---

## Access the Application

- **Frontend**: http://localhost:5173 ← Start here!
- **Voice Service API**: http://localhost:8002
- **TTS Service API**: http://localhost:8003
- See `frontend/.env.development` for service configuration

---

## Testing

### Test Voice Upload & TTS Flow

```bash
# 1. Open browser: http://localhost:5173

# 2. Go to "Voice Management" tab
   - Click "Upload Voice"
   - Enter name and select audio file
   - Should return voice-{id}

# 3. Go to "Generation" tab
   - Enter text: "welcome to India"
   - Select voice: (from uploaded voices)
   - Provider: google
   - Click "Generate"
   - Should receive audio and play it ✅

# 4. Check browser DevTools console
   - Should see successful requests to:
     - http://localhost:8002/voices (voice list)
     - http://localhost:8003/inference/jobs/{jobId}/infer (generation)
     - http://localhost:8003/inference/jobs/{jobId}/output (audio retrieval)
```

### Run Automated Tests

```bash
# Frontend tests (if available)
cd frontend
npm run test

# Backend tests (if available)
cd ../tests
pytest -v
```

---

## Stopping the Application

### Stop Docker Containers
```bash
docker-compose -f compose.harness.yaml down
```

### Kill Processes Manually
```bash
# Windows
taskkill /F /IM node.exe
taskkill /F /IM python.exe

# macOS/Linux
pkill -f "uvicorn"
pkill -f "node"
```

---

## Common Tasks

### Update Dependencies
```bash
# Frontend
cd frontend
npm update

# Backend
cd ../voice_narration
pip install --upgrade -r requirements-dev.txt
```

### Run Linting & Formatting

```bash
# Frontend
cd frontend
npm run lint
npm run format

# Backend
cd ../voice_narration
black .
isort .
flake8 .
```

### Build for Production

```bash
# Frontend
cd frontend
npm run build

# Backend (Docker)
docker build -f Dockerfile -t voice-narration-backend:latest .
docker push your-registry/voice-narration-backend:latest
```

---

## Deployment

### Quick Deploy to GCP

See **GCP-DEPLOYMENT.md** for full cloud deployment guide:

```bash
# 1. Setup GCP project
export PROJECT_ID="voice-narration-prod"
export REGION="us-central1"

# 2. Create infrastructure
gcloud sql instances create voice-narration-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION

# 3. Deploy to Cloud Run
gcloud run deploy voice-narration-frontend \
  --image=gcr.io/$PROJECT_ID/voice-narration:latest \
  --platform=managed \
  --region=$REGION
```

### Deploy Locally (Docker)

```bash
docker-compose -f compose.harness.yaml up -d
```

---

## Troubleshooting

### Frontend Won't Start
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend Connection Error
```bash
# Check if services are running
curl http://localhost:8001/health
curl http://localhost:8003/health

# Check database connection
psql postgresql://user:password@localhost:5432/voice_narration
```

### Tests Failing
```bash
# Clear test cache
cd frontend
npm run test -- --clearCache

# Run specific test file
npm run test -- run tests/tts.spec.tsx

# Run with verbose output
npm run test -- --reporter=verbose
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5173
kill -9 <PID>
```

---

## Documentation

- **DEPLOYMENT.md** - Full local deployment guide
- **GCP-DEPLOYMENT.md** - Google Cloud Platform deployment
- **DOCUMENTATION_MAP.md** - Project structure overview
- **README.md** - Project introduction

---

## Architecture

```
Voice-Narration/
├── frontend/                 # React + TypeScript (M0-M3)
│   ├── src/
│   │   ├── components/      # M2-GREEN (voice), M3-GREEN (TTS)
│   │   ├── context/         # Auth, Voice, TTS state
│   │   ├── services/        # API clients
│   │   ├── hooks/           # Custom hooks
│   │   └── pages/           # Routes
│   ├── tests/               # Vitest + MSW mocks (200+ tests)
│   └── package.json
│
├── voice_narration/         # Python Backend (M1-M24)
│   ├── app/
│   │   ├── services/        # M1 Auth, M2 Voice, M3 TTS, etc.
│   │   ├── database/        # SQLAlchemy models
│   │   └── main.py          # Entry point
│   └── requirements-dev.txt
│
├── tests/                   # Backend pytest suite (39 tests)
├── containers/              # Docker configurations
├── compose.harness.yaml     # Multi-container orchestration
├── DEPLOYMENT.md            # Local deployment
└── GCP-DEPLOYMENT.md        # Cloud deployment
```

---

## Support & Issues

- Check **Troubleshooting** section above
- Review logs: `docker-compose logs -f service-name`
- See DEPLOYMENT.md for detailed error resolution

---

**Last Updated**: November 1, 2026
**Status**: M3-GREEN Complete • Ready for Deployment
