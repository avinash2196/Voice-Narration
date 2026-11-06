# M024 GREEN: Deployment & Testing Guide

**Status:** ✅ COMPLETE - All 17 M023 tests PASSING + 22 M022 regression tests still passing

**Commit:** 9150315 - M024 GREEN: Production Inference Implementation

---

## Quick Start: 3 Steps to Deploy

### Step 1: Create `.env` File

Create a file named `.env` in the project root:

```bash
# Windows: Create with PowerShell
ni .env
```

Add ONE of the following configurations:

#### Option A: Google Cloud TTS

```env
# Google Cloud TTS Configuration
INFERENCE_PROVIDER=google
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

**Steps to get credentials:**
1. Go to https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Enable "Cloud Text-to-Speech API"
4. Create a Service Account (Compute → Service Accounts)
5. Create a JSON key for the service account
6. Download the JSON key file
7. Replace `/path/to/service-account-key.json` with actual path

**Example path (Windows):**
```env
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\YourName\Downloads\service-account-key.json
```

#### Option B: Azure Speech

```env
# Azure Speech Configuration
INFERENCE_PROVIDER=azure
AZURE_SPEECH_KEY=your-api-key-here
AZURE_SPEECH_REGION=eastus
```

**Steps to get credentials:**
1. Go to https://portal.azure.com/
2. Create "Cognitive Services" → "Speech" resource
3. Get API Key from "Keys and Endpoint" section
4. Get Region from "Endpoint" (e.g., `eastus`, `westus2`)
5. Replace values above

**Example:**
```env
AZURE_SPEECH_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
AZURE_SPEECH_REGION=eastus
```

#### Option C: Mock Provider (Testing - No Credentials Needed)

```env
# Mock Provider (Testing Only)
INFERENCE_PROVIDER=mock
```

This works immediately - no setup required!

---

### Step 2: Verify .env File

```powershell
# PowerShell - Check .env exists
Get-Content .env

# Should show something like:
# INFERENCE_PROVIDER=google
# GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json
```

---

### Step 3: Run Tests

```powershell
# Test M024 implementation
pytest tests/test_linguistic_chunking_and_controls.py -v

# Expected: 17 PASSED
# Sample output:
# tests/test_linguistic_chunking_and_controls.py::test_chunk_without_word_breaks PASSED
# tests/test_linguistic_chunking_and_controls.py::test_chunk_respects_punctuation_boundaries PASSED
# ... (15 more tests)
# ====================== 17 passed in 1.08s ======================

# Test regression (M022 still works)
pytest tests/test_provider_registry.py tests/test_inference.py -v

# Expected: 22 PASSED
# This verifies no breaking changes

# Full suite
pytest tests/test_provider_registry.py tests/test_inference.py tests/test_linguistic_chunking_and_controls.py -q

# Expected: 39 PASSED ✅
```

---

## Testing with Real Model (Google TTS Example)

### Run a Full Inference Workflow

Create a test script `test_inference_workflow.py`:

```python
import asyncio
from voice_narration.inference.registry import ProviderRegistry
from voice_narration.inference.production import InferenceWorkflow

async def test_google_inference():
    """Test full inference with Google TTS."""
    
    # Get provider from registry (loads from GOOGLE_APPLICATION_CREDENTIALS)
    provider = ProviderRegistry.get_provider("google")
    
    # Create workflow
    workflow = InferenceWorkflow(provider=provider, model_name="google")
    
    # Hindi text sample
    hindi_text = "नमस्ते। कृपया प्रतीक्षा करें।"
    
    # Generate with chunking
    result = await workflow.generate_with_chunking(
        script=hindi_text,
        voice_id="hi-IN-Neural2-A",  # Google voice ID
        chunk_size=500,
    )
    
    # Save audio to file
    with open("output.wav", "wb") as f:
        f.write(result["audio_bytes"])
    
    print(f"✅ Generated {result['output_seconds']:.1f} seconds of audio")
    print(f"✅ Chunks: {result['chunks']}")
    print(f"✅ Saved to output.wav")
    
    # Print text-to-audio mapping
    for i, mapping in enumerate(result["mapping"]):
        print(f"  Chunk {i}: {mapping['text'][:30]}... ({mapping['end_time_ms']}ms)")

# Run it
if __name__ == "__main__":
    asyncio.run(test_google_inference())
```

Run the test:

```powershell
python test_inference_workflow.py

# Expected output:
# ✅ Generated 3.2 seconds of audio
# ✅ Chunks: 2
# ✅ Saved to output.wav
#   Chunk 0: नमस्ते। (...ms)
#   Chunk 1: कृपया प्रतीक्षा करें। (...ms)
```

---

## API Testing: HTTP Endpoints

### Start the Server

```powershell
# Start FastAPI server
python -m uvicorn voice_narration.inference.application:app --reload

# Server starts at: http://localhost:8000
```

### Test Inference Endpoints

#### 1. List Available Backends

```powershell
# PowerShell
$url = "http://localhost:8000/inference/backends"
Invoke-WebRequest -Uri $url | ConvertFrom-Json | ConvertTo-Json

# Expected response:
# {
#   "providers": [
#     {
#       "name": "google",
#       "model_name": "Google Cloud Text-to-Speech",
#       ...
#     },
#     {
#       "name": "mock",
#       ...
#     }
#   ]
# }
```

#### 2. Get Available Voices

```powershell
$url = "http://localhost:8000/inference/voices?language=hi"
Invoke-WebRequest -Uri $url | ConvertFrom-Json | ConvertTo-Json

# Lists Hindi voices available in current provider
```

#### 3. Estimate Cost

```powershell
$body = @{
    script = "नमस्ते। यह एक परीक्षण है।"
    voice_id = "hi-IN-Neural2-A"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/inference/estimate" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | ConvertFrom-Json | ConvertTo-Json

# Returns: estimated cost and duration
```

#### 4. Submit Inference Job

```powershell
$jobId = "job-001"
$body = @{
    script = "नमस्ते। कृपया प्रतीक्षा करें।"
    voice_id = "hi-IN-Neural2-A"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/inference/jobs/$jobId/infer" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | ConvertFrom-Json | ConvertTo-Json

# Returns: job status
```

#### 5. Get Output

```powershell
$jobId = "job-001"

# Get audio file
$output = Invoke-WebRequest -Uri "http://localhost:8000/inference/jobs/$jobId/output"

# Save to file
[System.IO.File]::WriteAllBytes("output.wav", $output.Content)

# Or get JSON with metadata
Invoke-WebRequest -Uri "http://localhost:8000/inference/jobs/$jobId/output?format=json" | ConvertFrom-Json
```

---

## Troubleshooting

### Issue: "GOOGLE_APPLICATION_CREDENTIALS not found"

**Solution:**
```powershell
# Check if .env exists
Test-Path .env

# If not, create it:
ni .env -Type File

# Add your Google credentials path
Add-Content .env "GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json"
```

### Issue: "Model google-tts not approved for production"

**Solution:** This is expected! The model must be explicitly approved. Check:

```python
from voice_narration.inference.production import ModelLicenseValidator

validator = ModelLicenseValidator()
result = validator.validate_model_approved("google-tts")
print(result)  # Should be True
```

### Issue: "Audio quality is poor / Model not generating"

**Solution:**
1. Verify credentials are correct
2. Check Google Cloud API is enabled (Text-to-Speech API)
3. Check Azure endpoint is correct (eastus, westus2, etc.)
4. Try with mock provider first to verify system works

### Issue: "Tests passing but audio not generating"

**Solution:** This is expected with mock provider! Mock provider returns:
- Silent WAV audio (for testing without real TTS service)
- Deterministic output (same input = identical output)
- Fixed cost ($0.10 per generation)

To generate real audio, use Google TTS or Azure Speech.

---

## Configuration Reference

### Environment Variables

| Variable | Provider | Required | Example |
|----------|----------|----------|---------|
| `INFERENCE_PROVIDER` | All | Yes | `google`, `azure`, `mock` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google | If google | `/path/to/key.json` |
| `AZURE_SPEECH_KEY` | Azure | If azure | `a1b2c3d4e5...` |
| `AZURE_SPEECH_REGION` | Azure | If azure | `eastus` |

### Supported Voices

#### Google Cloud TTS

```
# Hindi Voices
hi-IN-Neural2-A  (Female)
hi-IN-Neural2-B  (Male)
hi-IN-Neural2-C  (Female)

# English Voices
en-US-Neural2-A  (Female)
en-US-Neural2-C  (Male)
en-GB-Neural2-A  (Female)
en-GB-Neural2-B  (Male)
en-GB-Neural2-F  (Female)
```

#### Azure Speech

```
# Hindi Voices
hi-IN-MadhurNeural     (Female)
hi-IN-Harshit          (Male)

# English Voices
en-US-AriaNeural       (Female)
en-US-GuyNeural        (Male)
en-GB-LibbyNeural      (Female)
en-GB-RyanNeural       (Male)
```

#### Mock Provider

```
mock-hindi-female
mock-hindi-male
mock-english-female
mock-english-male
```

---

## Testing Checklist

- [ ] `.env` file created with provider choice
- [ ] Credentials verified (no errors on load)
- [ ] `pytest tests/test_linguistic_chunking_and_controls.py` passes (17/17)
- [ ] `pytest tests/test_provider_registry.py tests/test_inference.py` passes (22/22)
- [ ] Full test suite passes: `pytest -q` (39/39)
- [ ] HTTP endpoints responding (start server, test /inference/backends)
- [ ] Generated audio valid (can play output.wav)
- [ ] Text-to-audio mapping correct
- [ ] Cost estimation accurate
- [ ] Hindi pronunciation clear (if using Google/Azure)

---

## Production Deployment Checklist

- [ ] Model selection: Google TTS or Azure Speech decided
- [ ] Credentials securely stored (.env not committed to git)
- [ ] All 39 tests passing in CI/CD
- [ ] API documentation generated (`/docs` endpoint)
- [ ] Rate limiting configured
- [ ] Cost tracking enabled and monitored
- [ ] Error handling and logging configured
- [ ] Backup provider configured (mock for fallback?)
- [ ] Load testing completed
- [ ] Security review passed
- [ ] Deployment runbook created

---

## What's Next?

### M025: User Enrollment with Real Model

Now that M024 is complete, M025 will:
- Enable user enrollment with real TTS model
- Implement acoustic calibration workflow
- Validate quality against baseline
- Accept or reject user samples

### M026+: Full Feature Integration

- Frontend/browser integration
- Real-time inference with progress tracking
- Playback and feedback collection
- Production monitoring and alerting

---

## Quick Reference: Commands

```powershell
# Create .env file
ni .env

# Add Google credentials
Add-Content .env "INFERENCE_PROVIDER=google"
Add-Content .env "GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json"

# Run all M024 tests
pytest tests/test_linguistic_chunking_and_controls.py -v

# Run with real inference (requires credentials)
python test_inference_workflow.py

# Start API server
python -m uvicorn voice_narration.inference.application:app --reload

# Test endpoint
curl http://localhost:8000/inference/backends

# View API docs
# Open in browser: http://localhost:8000/docs
```

---

## Summary

✅ M024 GREEN is complete and all tests passing

✅ Both Google Cloud TTS and Azure Speech are supported

✅ Production-ready code with licensing validation

✅ No breaking changes to existing system

**You are ready to:**
1. Deploy with your chosen TTS provider
2. Test with real audio generation  
3. Enable user enrollment in M025
4. Move toward production launch

---

Generated: 2026-10-30 23:33 UTC  
Status: ✅ M024 COMPLETE - READY FOR DEPLOYMENT
