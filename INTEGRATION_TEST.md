# Frontend-Backend Integration Test Guide

## ✅ Integration Complete

Frontend (port 5173) is now fully integrated with production inference service (port 8003).

---

## Running Services

### Verify Both Services Are Running
```bash
# Check Frontend
netstat -ano | findstr ":5173"
# Should show: LISTENING on port 5173

# Check Inference Service
netstat -ano | findstr ":8003"
# Should show: LISTENING on port 8003
```

---

## Manual Test Flow

### Step 1: Open Frontend
```
http://localhost:5173
```

### Step 2: Log In
- Use any test email/password (auth is mocked)
- System will create mock user session

### Step 3: Upload a Voice
1. Go to "Voice Management" or "Upload Voice" page
2. Click "Upload Voice"
3. Select an audio file (any WAV/MP3)
4. Voice will be stored locally (approved status)

### Step 4: Generate TTS
1. Go to "Generation" or "Create TTS" page
2. Enter text: "Welcome to India"
3. Select voice from dropdown
4. Select provider: "Google Cloud TTS"
5. Click "Generate"

### Expected Behavior
```
Timeline:
1. POST /inference/jobs/{jobId}/infer
   → Sends text to production service
   → Google TTS generates audio
   → Audio stored on service
   → Returns: status=complete, duration=1.15s

2. GET /inference/jobs/{jobId}/output
   → Retrieves stored audio
   → Response: base64 audio_bytes, format=wav
   → Frontend converts to Blob

3. Audio Player loads
   → RIFF header verified
   → Audio plays in browser
   → Duration matches: ~1.15 seconds
```

### Success Criteria
- ✅ No console errors
- ✅ Audio generates without errors
- ✅ Audio plays in player
- ✅ Duration displayed correctly
- ✅ Status shows "complete"

---

## Network Flow Verification

### Using Browser DevTools
1. Open DevTools (F12)
2. Go to Network tab
3. Generate TTS
4. Look for requests:

```
POST http://localhost:8003/inference/jobs/gen-123456.../infer
  Status: 200
  Response: {"job_id": "...", "status": "complete", "duration_seconds": 1.15}

GET http://localhost:8003/inference/jobs/gen-123456.../output
  Status: 200
  Response: {"audio_bytes": "UklGRi8o...", "format": "wav", ...}
```

### Using Console
```javascript
// In browser DevTools console, test directly:
fetch('http://localhost:8003/inference/jobs/test-gen-1/infer', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({script: "Hello", voice_id: "en-US-Neural2-C"})
})
.then(r => r.json())
.then(d => console.log('Response:', d))

// Then get audio:
fetch('http://localhost:8003/inference/jobs/test-gen-1/output')
.then(r => r.json())
.then(d => console.log('Audio bytes length:', d.audio_bytes.length))
```

---

## Troubleshooting

### Issue: 404 on /inference/jobs/... endpoints
**Cause**: TTS_SERVICE points to wrong port
**Fix**: 
```bash
# Check .env.development
cat frontend/.env.development | grep TTS_API_BASE_URL
# Should show: VITE_TTS_API_BASE_URL=http://localhost:8003

# Restart frontend dev server
npm run dev  # in frontend/
```

### Issue: "No audio data in response"
**Cause**: Production service didn't generate audio
**Fix**:
```bash
# Test service directly:
curl -X POST http://localhost:8003/inference/jobs/test-1/infer \
  -H "Content-Type: application/json" \
  -d '{"script": "test", "voice_id": "en-US-Neural2-C"}'

# Get output:
curl http://localhost:8003/inference/jobs/test-1/output
```

### Issue: "Authorization undefined" errors
**Cause**: Token not being passed correctly
**Fix**: This is expected for mock auth. Frontend uses mock token "mock-jwt-token-123"

### Issue: Audio plays but sounds wrong/empty
**Cause**: Base64 decoding error
**Fix**:
1. Check DevTools Console for errors
2. Verify audio_bytes length > 1000 bytes
3. Try different text/voice combination

### Issue: Service says "Job not found"
**Cause**: Job ID mismatch or service restarted (lost memory)
**Fix**:
1. Generate new TTS (new job ID)
2. Get output immediately (don't wait long)
3. Restart service if needed: 
   ```bash
   taskkill /PID 645532 /F
   cd C:\...\Voice-Narration
   python -m voice_narration.inference
   ```

---

## What's Working End-to-End

```
Frontend (React)
  ↓ ttsApi.submitGeneration()
  ↓ Generates unique jobId
  
Frontend → Backend
  POST http://localhost:8003/inference/jobs/{jobId}/infer
  {
    script: "Welcome to India",
    voice_id: "en-US-Neural2-C"
  }

Production Service (FastAPI)
  ↓ Receives TTS request
  ↓ Calls GoogleTextToSpeechProvider
  
Google Cloud TTS API
  ↓ Generates real speech audio
  
Backend → Frontend
  {
    audio_bytes: "UklGRi8o...(base64)",
    format: "wav",
    duration_seconds: 1.156
  }

Frontend
  ↓ Decodes base64 → Blob
  ↓ Creates audio URL
  ↓ Plays in <audio> player
  ↓ User hears real Google TTS voice
```

---

## Files Changed

| File | Change | Purpose |
|------|--------|---------|
| `frontend/.env.development` | TTS_API_BASE_URL → :8003 | Route to production service |
| `frontend/src/services/ttsApi.ts` | Complete rewrite | Call production endpoints |

---

## Performance Notes

- Audio generation: ~1-2 seconds (Google API latency)
- Audio retrieval: ~100ms (in-memory storage)
- Total E2E: ~1-2 seconds from submit to playable audio

---

## Next Steps After Integration Verification

1. **Test with Multiple Voices**
   - Try different voice IDs
   - Verify each generates different audio
   - Check that duration varies by text length

2. **Error Handling**
   - Try invalid voice ID → should error gracefully
   - Try very long text → check if truncated
   - Network error simulation

3. **UI Polish**
   - Loading spinners while generating
   - Progress indication
   - Error messages in UI

4. **Production Hardening**
   - Add database persistence
   - Implement proper authentication
   - Add rate limiting
   - Cost tracking

---

## Success Checklist

- [ ] Frontend loads without errors
- [ ] Backend inference service running
- [ ] Can upload voice
- [ ] Can select voice from dropdown
- [ ] Can enter text for TTS
- [ ] Can click generate button
- [ ] Request goes to port 8003 (verified in DevTools)
- [ ] Audio generates successfully
- [ ] Audio blob created without errors
- [ ] Audio player displays and loads
- [ ] Audio plays and sounds correct
- [ ] Duration displayed matches actual
- [ ] Can generate multiple times
- [ ] Service doesn't crash on reload

---

**Status**: ✅ Integration Complete - Ready for Testing
