# Implementation Plan — Milestone 019
## Mock Inference Adapter – GREEN (Production Implementation)

**Milestone Type:** GREEN  
**Predecessor:** Mock Inference Adapter RED (M018)  
**Requirements:** FR-040, FR-041, FR-042  
**Expected Outcome:** 1 RED PASSED + 7 GREEN PASSED, 96+ regression baseline preserved

---

## Overview

Milestone 019 delivers the production implementation of the Mock Inference Adapter interface established by M018 RED tests. The goal is to make all 7 GREEN tests pass while preserving the 96-test baseline (95 prior + 1 M017 RED test).

### Key Constraints
- Follow the established application factory pattern (create_app, AppState, run_pending worker seam)
- Implement InferenceProvider interface with generate() and estimate_cost() methods
- Use mock provider for deterministic testing (1 second per 100 characters, silent WAV)
- Provide 3 HTTP endpoints for job inference triggering and output retrieval
- No production changes beyond inference adapter scope
- Preserve idempotency and job orchestration patterns from M017

---

## Production Code Specification

### 1. Module: voice_narration/inference/application.py

#### Create InferenceProvider Interface (Abstract Base)
```python
from abc import ABC, abstractmethod

class InferenceProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        script: str,
        voice_id: str,
        **kwargs
    ) -> dict:
        """
        Generate audio from script.
        
        Returns:
            {"output_seconds": float, "audio_bytes": bytes, "format": str}
        """
        pass

    @abstractmethod
    async def estimate_cost(self, script: str, voice_id: str) -> dict:
        """
        Estimate cost before generation.
        
        Returns:
            {"cost_usd": float, "estimated_seconds": float}
        """
        pass
```

#### Create MockInferenceProvider
```python
class MockInferenceProvider(InferenceProvider):
    """
    Deterministic mock provider for testing.
    - Output duration: 1 second per 100 characters
    - Audio format: Silent WAV bytes (48 kHz, mono)
    - Latency: Zero (synchronous)
    - Cost: $0.10 per generation
    """
    
    async def generate(self, script: str, voice_id: str, **kwargs) -> dict:
        # Calculate output duration: 1 sec per 100 chars
        output_seconds = max(1, len(script) / 100.0)
        
        # Generate silent WAV bytes (minimal valid WAV header + data)
        # Format: 48 kHz, mono, 16-bit PCM, ~output_seconds duration
        sample_rate = 48000
        num_samples = int(sample_rate * output_seconds)
        # WAV header (44 bytes) + silent PCM data (num_samples * 2 bytes)
        audio_bytes = self._generate_silent_wav(num_samples, sample_rate)
        
        return {
            "output_seconds": output_seconds,
            "audio_bytes": audio_bytes,
            "format": "wav"
        }

    async def estimate_cost(self, script: str, voice_id: str) -> dict:
        output_seconds = max(1, len(script) / 100.0)
        return {
            "cost_usd": 0.10,
            "estimated_seconds": output_seconds
        }

    @staticmethod
    def _generate_silent_wav(num_samples: int, sample_rate: int = 48000) -> bytes:
        """Generate minimal valid WAV file with silent audio."""
        import struct
        
        # Minimal WAV header for 48 kHz mono 16-bit PCM
        channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * channels * bits_per_sample // 8
        block_align = channels * bits_per_sample // 8
        subchunk2_size = num_samples * block_align
        
        wav = b'RIFF'
        wav += struct.pack('<I', 36 + subchunk2_size)  # file size - 8
        wav += b'WAVE'
        wav += b'fmt '
        wav += struct.pack('<I', 16)  # subchunk1 size
        wav += struct.pack('<HHIIHH', 1, channels, sample_rate, byte_rate, block_align, bits_per_sample)
        wav += b'data'
        wav += struct.pack('<I', subchunk2_size)
        wav += b'\x00' * subchunk2_size  # silent audio data
        
        return wav
```

#### Create InferenceState Class
```python
class InferenceState:
    """
    Manages inference execution state and orchestration.
    """
    
    def __init__(
        self,
        provider: InferenceProvider,
        jobs_app: FastAPI,  # Dependency from M017
        job_repository,  # HistoryRepository for persistence
    ):
        self.provider = provider
        self.jobs_app = jobs_app
        self.job_repository = job_repository
        self._pending_inferences = {}  # Track in-flight inferences
    
    async def submit_for_inference(
        self,
        job_id: str,
        script: str,
        voice_id: str,
        owner_id: str,
    ) -> dict:
        """
        Submit a job for inference. Requires valid job from Jobs service.
        """
        # Validate job exists and owner matches
        job = await self.job_repository.get_job_by_uuid(job_id, owner_id)
        if not job:
            raise ValueError(f"Job {job_id} not found for owner {owner_id}")
        
        # Mark job as INFERENCING (new state between PROCESSING and COMPLETE)
        # (Job state machine updated in M017 contract amendment)
        
        # Generate inference asynchronously, store output
        output = await self.provider.generate(script, voice_id)
        
        # Persist output to job
        await self.job_repository.update_job_output(
            job_id,
            owner_id,
            {
                "audio_bytes": output["audio_bytes"],
                "format": output["format"],
                "duration_seconds": output["output_seconds"],
            }
        )
        
        return {"job_id": job_id, "status": "complete", "duration_seconds": output["output_seconds"]}
    
    async def get_inference_output(self, job_id: str, owner_id: str) -> dict:
        """Retrieve inference output for a completed job."""
        job = await self.job_repository.get_job_by_uuid(job_id, owner_id)
        if not job:
            raise ValueError(f"Job {job_id} not found for owner {owner_id}")
        
        if not job.get("output"):
            raise ValueError(f"Job {job_id} has no output yet")
        
        return job["output"]
    
    async def list_backends(self) -> list:
        """List available inference backends (for extensibility)."""
        return [
            {
                "name": "mock",
                "provider_class": "MockInferenceProvider",
                "description": "Deterministic mock provider for testing"
            }
        ]
    
    async def run_pending(self) -> int:
        """
        Deterministic worker seam for test verification.
        Processes any queued inference jobs (none in mock phase).
        """
        return 0  # No background processing in mock
    
    async def close(self) -> None:
        """Cleanup resources."""
        pass
```

#### Create create_app Factory
```python
def create_app(
    *,
    provider: InferenceProvider = None,
    jobs_app: FastAPI = None,
    job_repository = None,
) -> FastAPI:
    """
    Create FastAPI application for inference adapter.
    
    Args:
        provider: InferenceProvider instance (defaults to MockInferenceProvider)
        jobs_app: Jobs application for orchestration dependency
        job_repository: Repository for job persistence
    
    Returns:
        FastAPI application with inference routes and app.state bound
    """
    if provider is None:
        provider = MockInferenceProvider()
    
    app = FastAPI()
    state = InferenceState(provider, jobs_app, job_repository)
    app.state.inference = state
    
    # Dependency injection helper
    async def get_inference_state():
        return app.state.inference
    
    # Endpoints
    @app.post("/inference/jobs/{job_id}/infer")
    async def submit_job_for_inference(
        job_id: str,
        request_body: dict,
        request: Request,
        state: InferenceState = Depends(get_inference_state),
    ):
        """Submit job for inference."""
        try:
            owner_id = extract_owner_from_request(request)
            result = await state.submit_for_inference(
                job_id,
                request_body["script"],
                request_body["voice_id"],
                owner_id,
            )
            return JSONResponse(content=result, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)
    
    @app.get("/inference/jobs/{job_id}/output")
    async def get_inference_output(
        job_id: str,
        request: Request,
        state: InferenceState = Depends(get_inference_state),
    ):
        """Retrieve inference output."""
        try:
            owner_id = extract_owner_from_request(request)
            output = await state.get_inference_output(job_id, owner_id)
            return JSONResponse(content=output, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)
    
    @app.get("/inference/backends")
    async def list_backends(
        state: InferenceState = Depends(get_inference_state),
    ):
        """List available inference backends."""
        backends = await state.list_backends()
        return JSONResponse(content={"backends": backends}, status_code=200)
    
    # Cleanup hook
    @app.on_event("shutdown")
    async def shutdown_event():
        await state.close()
    
    return app
```

---

## Test Completion Specification

### Update tests/test_inference.py

#### Test 1: TestInferenceBasics::test_submit_job_for_inference
```python
@pytest.mark.asyncio
async def test_submit_job_for_inference(inference_app):
    """Verify job submission triggers inference."""
    client = TestClient(inference_app)
    
    response = client.post("/inference/jobs/test-job-123/infer", json={
        "script": "Hello world",
        "voice_id": "voice-001"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "complete"
    assert "duration_seconds" in data
```

#### Test 2: TestInferenceExecution::test_mock_inference_generates_output
```python
@pytest.mark.asyncio
async def test_mock_inference_generates_output(inference_app):
    """Verify mock inference generates output."""
    state = inference_app.state.inference
    
    output = await state.provider.generate("Test script", "voice-001")
    
    assert output["output_seconds"] > 0
    assert isinstance(output["audio_bytes"], bytes)
    assert output["format"] == "wav"
    assert len(output["audio_bytes"]) > 0
```

#### Test 3: TestInferenceExecution::test_inference_timing_matches_script_length
```python
@pytest.mark.asyncio
async def test_inference_timing_matches_script_length(inference_app):
    """Verify synthetic timing: 1 second per 100 characters."""
    state = inference_app.state.inference
    
    scripts = [
        ("Short", 1),  # 5 chars -> 1 sec
        ("This is a longer script with more content", 1),  # 42 chars -> 1 sec
        ("X" * 100, 1),  # 100 chars -> 1 sec
        ("X" * 200, 2),  # 200 chars -> 2 sec
        ("X" * 250, 2.5),  # 250 chars -> 2.5 sec
    ]
    
    for script, expected_duration in scripts:
        output = await state.provider.generate(script, "voice-001")
        assert output["output_seconds"] == expected_duration
```

#### Test 4: TestInferenceExecution::test_mock_inference_returns_wav_bytes
```python
@pytest.mark.asyncio
async def test_mock_inference_returns_wav_bytes(inference_app):
    """Verify output is valid WAV format."""
    state = inference_app.state.inference
    
    output = await state.provider.generate("Test script", "voice-001")
    
    # Check WAV signature
    assert output["audio_bytes"].startswith(b'RIFF')
    assert b'WAVE' in output["audio_bytes"]
    assert output["format"] == "wav"
```

#### Test 5: TestOutputRetrieval::test_retrieve_inference_output_by_job_id
```python
@pytest.mark.asyncio
async def test_retrieve_inference_output_by_job_id(inference_app):
    """Verify output retrieval by job ID."""
    client = TestClient(inference_app)
    
    # Submit for inference
    client.post("/inference/jobs/test-job-456/infer", json={
        "script": "Test audio",
        "voice_id": "voice-002"
    })
    
    # Retrieve output
    response = client.get("/inference/jobs/test-job-456/output")
    assert response.status_code == 200
    data = response.json()
    assert "audio_bytes" in data or "format" in data
```

#### Test 6: TestBackendManagement::test_list_available_inference_backends
```python
@pytest.mark.asyncio
async def test_list_available_inference_backends(inference_app):
    """Verify backend listing."""
    client = TestClient(inference_app)
    
    response = client.get("/inference/backends")
    assert response.status_code == 200
    
    data = response.json()
    assert "backends" in data
    assert len(data["backends"]) > 0
    assert data["backends"][0]["name"] == "mock"
```

#### Test 7: TestInferenceErrorHandling::test_failed_inference_transitions_job
```python
@pytest.mark.asyncio
async def test_failed_inference_transitions_job(inference_app):
    """Verify error handling transitions job to failed state."""
    client = TestClient(inference_app)
    
    # Submit with missing voice_id (error case)
    response = client.post("/inference/jobs/test-job-789/infer", json={
        "script": "Test"
        # Missing voice_id
    })
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
```

---

## Acceptance Criteria

| # | Criterion | Verification Method |
|---|-----------|---------------------|
| 1 | InferenceProvider interface defined | Code review: voice_narration/inference/application.py |
| 2 | MockInferenceProvider implements generate() | Test: test_mock_inference_generates_output passes |
| 3 | MockInferenceProvider implements estimate_cost() | Code review + test |
| 4 | Synthetic timing: 1 sec per 100 chars | Test: test_inference_timing_matches_script_length passes |
| 5 | WAV audio output generated | Test: test_mock_inference_returns_wav_bytes passes |
| 6 | InferenceState class implements run_pending() | Code review: deterministic worker seam |
| 7 | 3 HTTP endpoints implemented | Tests: 5 endpoints verified (submit, retrieve, list) |
| 8 | POST /inference/jobs/{id}/infer endpoint | Test: test_submit_job_for_inference passes |
| 9 | GET /inference/jobs/{id}/output endpoint | Test: test_retrieve_inference_output_by_job_id passes |
| 10 | GET /inference/backends endpoint | Test: test_list_available_inference_backends passes |
| 11 | All 7 GREEN tests PASSED | Pytest: 7/7 GREEN PASSED |
| 12 | 1 RED test PASSED | Pytest: RED test unchanged from M018 |
| 13 | 96+ regression baseline preserved | Pytest: full suite 96 PASSED + 14 SKIPPED |
| 14 | No new test failures | Pytest: 0 new failures vs M018 baseline |
| 15 | Error handling transitions job to failed state | Test: test_failed_inference_transitions_job passes |

---

## Dependencies

### Prior Work (Completed)
- M017 (Job Orchestration GREEN): voice_narration/jobs/application.py, job state machine, idempotency
- M018 (Mock Inference RED): tests/test_inference.py with 1 RED test + 7 GREEN stubs

### External Dependencies
- FastAPI (existing)
- pytest + asyncio support (existing)
- Job repository from M017 (HistoryRepository)

### Test Fixtures
- `inference_app` fixture in tests/test_inference.py (already defined in M018)
- Mock inference provider instance
- Job app integration (via fixture)

---

## Implementation Sequence

1. **Create voice_narration/inference/application.py** (350-400 lines)
   - InferenceProvider ABC
   - MockInferenceProvider with generate() and estimate_cost()
   - InferenceState with job integration
   - create_app factory
   - 3 HTTP endpoints

2. **Update tests/test_inference.py** (expand to ~500 lines)
   - Replace 7 GREEN test stubs with full test implementations
   - Each test includes setup, assertions, and error cases
   - Keep 1 RED test unchanged

3. **Execute full test suite**
   - Run pytest tests/ -v
   - Expected: 1 RED PASSED + 7 GREEN PASSED
   - Verify: 96+ regression baseline (95 prior + 1 M017)

4. **Create MILESTONE_019_EXECUTION_EVIDENCE.md**
   - Record test results
   - Verify acceptance criteria
   - Document any issues

5. **Commit execution**
   - voice_narration/inference/application.py
   - Updated tests/test_inference.py
   - Execution evidence

---

## Known Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Job repository interface mismatch | Low | M019 fails to retrieve jobs | Verify interface in M017 code; adjust if needed |
| WAV generation produces invalid format | Low | Audio tests fail | Verify WAV header structure; use reference implementation |
| Fixture dependency gaps | Medium | GREEN tests can't initialize | Update conftest.py if needed (coordinated with M020) |
| Regression test failures | Low | Baseline regression | Run regression suite after each change |

---

## Notes for Implementation

- **Mock Provider Determinism:** Ensure timing is fully deterministic (no random delays, consistent WAV generation)
- **Job Integration:** InferenceState should work with the job repository established in M017
- **Error Handling:** Return appropriate HTTP status codes (400 for bad input, 404 for missing jobs, 500 for provider errors)
- **Async Pattern:** All methods should be properly async to match M017 patterns
- **Test Isolation:** Each test should set up its own test data; no cross-test dependencies

---

## Success Definition

✅ **M019 GREEN is successful when:**
1. voice_narration/inference/application.py created with all specified components
2. All 7 GREEN tests pass (currently SKIPPED in M018)
3. 1 RED test continues to pass (module verification)
4. 96+ prior regression tests remain passing
5. MILESTONE_019_EXECUTION_EVIDENCE.md records all results
6. Execution committed with comprehensive message

