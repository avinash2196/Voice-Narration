# Plugin & Agent Review: Decision Gaps and Corrections

## Problem Statement
During development, an AI agent created and worked on `simple_backend.py` (a mock backend with direct Google TTS integration) instead of focusing on the **production microservices** that already exist in `voice_narration/`. This diverted effort from the real issue and created confusion about which codebase was authoritative.

**Root Cause:** The plugin/agent lacked architectural context and didn't recognize that:
1. The project has a **real production backend** in `voice_narration/` with microservices architecture
2. The `simple_backend.py` was an experimental mock, not the canonical implementation
3. User's original request was to fix the **production services**, not enhance mocks

---

## Architecture Context (For Plugins/Agents)

### Production Backend Structure
```
voice_narration/
├── inference/           # TTS inference service (port 8003)
│   ├── __main__.py      # Entry point (bootstraps provider)
│   ├── application.py   # FastAPI endpoints
│   ├── providers/       # Pluggable TTS backends
│   │   ├── google_tts.py
│   │   ├── azure_tts.py
│   │   └── mock.py
│   └── registry.py
├── auth/                # Authentication service (port 8001)
├── voices/              # Voice management service (port 8002)
├── jobs/                # Job orchestration service (port 8007)
└── audit/               # Audit logging service
```

### Experimental/Development
```
simple_backend.py       # ARCHIVED - Do not use. Was experimental mock.
frontend/               # React SPA (port 5173) - production code
```

---

## Key Decision Gaps Fixed

### 1. Mock vs Production Services
**Gap:** Agent created `simple_backend.py` enhancement instead of fixing production services.

**Rule for Plugins/Agents:**
- ✅ **DO**: Work on services in `voice_narration/` directory
- ❌ **DON'T**: Create or enhance mock backends when production equivalents exist
- ❌ **DON'T**: Assume `simple_backend.py` or similar experimental files are the canonical implementation

**Check:**
```bash
# Before proposing changes, verify:
1. Is there a voice_narration/{service}/ directory?
2. Does it have create_app() factory and __main__.py?
3. If yes → MUST work on production service
4. If no → Ask user for clarification before creating mock
```

---

### 2. Architecture Discovery
**Gap:** Agent didn't identify the microservices architecture before proposing solutions.

**Rule for Plugins/Agents:**
- ✅ **DO**: Run architectural discovery first:
  ```bash
  # Check what services exist
  ls -la voice_narration/
  
  # Check for create_app() pattern
  grep -r "def create_app" voice_narration/
  
  # Check for __main__.py entry points
  find voice_narration -name "__main__.py"
  ```
- ✅ **DO**: Understand the factory pattern:
  - Services use `create_app(provider=...)` dependency injection
  - Bootstrap requires instantiating provider + calling create_app()
- ❌ **DON'T**: Assume services can be run with `python -m module` without proper bootstrap

---

### 3. Provider Pattern Understanding
**Gap:** Agent didn't understand pluggable providers until late in the process.

**Rule for Plugins/Agents:**
Each service with pluggable backends needs:
1. **Provider interface** (abstract base class)
2. **Multiple implementations** (Google, Azure, Mock, etc.)
3. **Registry/factory** to select provider by name
4. **Bootstrap code** to instantiate chosen provider and inject into create_app()

**Example for TTS (Inference Service):**
```python
# voice_narration/inference/providers/__init__.py
# Base interface

# voice_narration/inference/providers/google_tts.py
class GoogleTextToSpeechProvider(InferenceProvider):
    def __init__(self, credentials_path):
        # Load credentials from GOOGLE_APPLICATION_CREDENTIALS
        ...
    async def generate(self, text, voice_id):
        # Call Google Cloud TTS API
        return audio_bytes

# voice_narration/inference/__main__.py
# Bootstrap - select provider and create app
provider_name = os.getenv("INFERENCE_PROVIDER", "mock")
if provider_name == "google":
    provider = GoogleTextToSpeechProvider(...)
else:
    provider = MockInferenceProvider()

app = create_app(provider=provider)
uvicorn.run(app, host="0.0.0.0", port=8003)
```

---

### 4. Endpoint Design Mismatch
**Gap:** Frontend API (`/generate`, `/generate/{id}/audio`) doesn't match production service API (`/inference/jobs/{job_id}/infer`, `/inference/jobs/{job_id}/output`).

**Rule for Plugins/Agents:**
When services have different endpoint patterns:
- ✅ **DO**: Update frontend to call production endpoints directly (better long-term)
- ✅ **DO**: Create adapter layer ONLY if frontend refactoring isn't feasible
- ❌ **DON'T**: Enhance mock backend as a "solution"

**Current Status:**
- Production inference service: `/inference/jobs/{job_id}/infer`, `/inference/jobs/{job_id}/output`
- Frontend still expects: `/generate`, `/generate/{id}/audio`
- **Next step**: Update frontend to call production endpoints OR create proper adapter if needed

---

## What Should Have Been Done

### Correct Workflow
1. **Discover** the production architecture
   ```bash
   grep -r "def create_app" voice_narration/
   find voice_narration -type f -name "application.py"
   ```

2. **Understand** the provider pattern
   ```bash
   ls voice_narration/inference/providers/
   cat voice_narration/inference/providers/google_tts.py  # Check interface
   ```

3. **Bootstrap** the service with correct provider
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json \
   INFERENCE_PROVIDER=google \
   python -m voice_narration.inference
   ```

4. **Test** the production service directly
   ```bash
   curl -X POST http://localhost:8003/inference/jobs/test-1/infer \
     -H "Content-Type: application/json" \
     -d '{"script": "Hello world", "voice_id": "voice-1"}'
   ```

5. **Update frontend** to match production endpoints
   - OR create proper adapter that proxies correctly

### What Actually Happened ❌
1. Agent looked at `simple_backend.py` and thought that was the backend
2. Enhanced `simple_backend.py` with Google TTS
3. Missed the entire `voice_narration/` production codebase
4. User had to manually redirect: "why are you working on simple_backend...should we not be working on production files"
5. Only then did agent discover and bootstrap the real service

---

## Rules for Future Work

### Before Proposing Any Solution
- [ ] Verify if production service exists in `voice_narration/{service}/`
- [ ] Check if `create_app()` factory pattern is used
- [ ] Look for `__main__.py` entry point
- [ ] Understand the provider/plugin architecture if applicable
- [ ] Identify the authoritative endpoint structure

### When Multiple Implementations Exist
- [ ] Prioritize: Production > Experimental > Mock
- [ ] Ask user for clarification if ambiguous: "I see both `simple_backend.py` and `voice_narration/`. Which should I work on?"
- [ ] Document the decision in commit message and comments

### When Services Have Different APIs
- [ ] Frontend should ideally call production endpoints directly
- [ ] Only create adapters/proxies if refactoring frontend isn't feasible
- [ ] Document the adapter's purpose: "Maps frontend /generate API → production /inference/jobs API"

### Code Review Checklist
- [ ] Changes are on production services, not mock backends
- [ ] Provider pattern is respected (don't hardcode providers)
- [ ] Factory/bootstrap code is present
- [ ] Environment variables for provider selection are used
- [ ] Documentation explains which service/endpoint was changed

---

## Archived Files

### simple_backend.py → simple_backend.py.archived
**Why archived:** Created as experimental mock during early development. Should not be used since production microservices exist.

**If you need a mock backend:**
- Use `INFERENCE_PROVIDER=mock` with production service
- Run: `INFERENCE_PROVIDER=mock python -m voice_narration.inference`
- This gets you production endpoints with mock data (better than mock backend with production endpoints)

---

## Current Status

✅ **Production Inference Service:** Running on port 8003 with Google TTS provider
✅ **Architecture:** Microservices with pluggable providers
❌ **Frontend Integration:** Still calls port 9000 mock endpoints (needs update)

### Next Steps
1. Update frontend `src/services/ttsApi.ts` to call `/inference/jobs/{job_id}/infer` directly
2. OR create proper adapter mapping `/generate` → `/inference/jobs/{job_id}/infer`
3. Test end-to-end: Frontend (5173) → Production Inference Service (8003) → Google TTS API

---

## References
- `voice_narration/inference/__main__.py` - Bootstrap entry point (shows provider pattern)
- `voice_narration/inference/application.py` - Production endpoints
- `voice_narration/inference/providers/google_tts.py` - Provider implementation
- `.env` - Provider configuration (GOOGLE_APPLICATION_CREDENTIALS, INFERENCE_PROVIDER)
