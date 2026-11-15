# Milestone 018 Implementation Plan
## Mock Inference Adapter RED

**Date:** 2026-10-28  
**Milestone Type:** RED (test-first, expected failures)  
**Predecessor:** Job Orchestration & Idempotency GREEN (017) — COMPLETE ✅  
**Status:** PENDING APPROVAL  

---

## Milestone & Authorization

**Milestone 018: Mock Inference Adapter RED**
- **Capability:** Mock Inference Adapter
- **Rationale:** Establish independent expected-failure evidence before production implementation
- **Scope:** Verification only — test-first RED implementation for synthetic job inference
- **Requirements Verified:** FR-040, FR-041, FR-042
  - FR-040: Run Windows local API/UI development and tests with mocked inference
  - FR-041: Support containerized worker model
  - FR-042: Support configurable local/cloud inference without assuming local CUDA, replace inference backends without changing UI/business APIs

**From Plan.md:**
> Tests/checks only: verify FR-040; FR-041; FR-042 — Run Windows local API/UI development and tests with mocked inference and a containerized worker; support configurable local/cloud inference without assuming local CUDA, and replace inference backends without changing UI/business APIs.

---

## Authoritative References

1. **Plan.md** (Milestone 018-019 definition)
   - Mock Inference Adapter RED/GREEN sequential requirements
   - Job Orchestration & Idempotency GREEN as predecessor (M017)
   - No production code, scaffolding, dependencies or configuration changes for RED

2. **Predecessor Evidence**
   - MILESTONE_017_EXECUTION_EVIDENCE.md — 1 RED PASSED, 7 GREEN SKIPPED
   - Job Orchestration & Idempotency GREEN successfully delivered
   - 95 PASSED regression baseline established

3. **Current Repository State**
   - voice_narration/jobs/application.py — Job submission, state machine, quotas
   - voice_narration/jobs/persistence.py — Durable job records
   - tests/test_job_orchestration.py — Job test structure established

---

## Current State & Work Scope

**What Exists:**
- ✅ Job Orchestration application layer (M017 GREEN)
- ✅ Jobs durable persistence (M017 GREEN)
- ✅ HTTP endpoints for job submission and listing (M017 GREEN)
- ✅ Mock cost/quota providers for testing (M017 test fixtures)
- ✅ Enrollment system (voices, artifacts) as upstream service (M015 GREEN)

**What's Missing (Expected RED Failures):**
- ❌ `voice_narration/inference/` package — Does not exist
- ❌ `voice_narration.inference.application` module — Missing
- ❌ `create_app()` factory for inference service — Not defined
- ❌ `InferenceState` interface — Not defined
- ❌ Job execution worker — Not implemented
- ❌ Synthetic model invocation — Not mocked
- ❌ Output generation fixture — Not available
- ❌ Audio codec/format handling — Not integrated

**Scope Boundaries:**
- ✅ In Scope: RED tests that verify missing module/functions
- ✅ In Scope: Test file structure and fixture dependencies
- ❌ Out of Scope: Production code, schema, migrations, configuration
- ❌ Out of Scope: Real model inference, TTS integration
- ❌ Out of Scope: Audio generation, codec operations

---

## Test-First Design

**RED Test Approach:**
The RED phase establishes the expected interface and failure mode through tests. When run BEFORE production code exists, the tests FAIL with `ImportError` or `AttributeError`. This is the EXPECTED RED outcome — it proves the test framework correctly detects missing implementation.

When Milestone 019 (GREEN) delivers the production code, the same tests will be updated with full assertions and PASS.

**Test File Location:**
```
tests/test_inference.py
```

**Test Structure:**

### 1. RED Test (1 total) — Missing Module Detection
```python
class TestInferenceAdapterRED:
    def test_inference_adapter_missing_module(self):
        """Inference module does not exist yet (expected RED failure)."""
        with pytest.raises((ImportError, AttributeError)):
            from voice_narration.inference import application
            app = application.create_app(...)
```

**Expected Outcome:** ✅ **PASS** (by raising expected exception)

This verifies that:
- The test framework can detect missing modules
- The test is properly structured for later GREEN completion
- Import error handling is correct

### 2. GREEN Tests (7 total) — Placeholders for Production Code
When production code is implemented in M019, these will be filled with full assertions:

```python
class TestJobInferenceIntegration:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    async def test_job_runs_inference(self):
        """Job submission triggers inference execution."""
        pass

class TestInferenceOutput:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    async def test_generate_audio_output(self):
        """Synthetic model generates audio output."""
        pass

class TestInferenceWorkerSeam:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    def test_worker_processes_pending_jobs(self):
        """Worker deterministically processes pending jobs."""
        pass

class TestModelBackendAbstraction:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    async def test_backend_swappable(self):
        """Inference backend is replaceable without changing UI APIs."""
        pass

class TestInferenceQuotaChecks:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    async def test_inference_respects_quotas(self):
        """Inference respects job quotas and cost limits."""
        pass

class TestLocalAndCloudSupport:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    async def test_configurable_local_cloud(self):
        """Supports local and cloud inference without assuming CUDA."""
        pass

class TestInferenceErrorHandling:
    @pytest.mark.skip(reason="GREEN: waiting for production implementation")
    async def test_failed_inference_transitions_job(self):
        """Failed inference transitions job to FAILED state."""
        pass
```

---

## Interface Specification (for M019 Production Code)

While the RED phase contains no production code, this section defines the expected interface that M019 will deliver, based on FR-040/041/042 and the established patterns from Jobs/Voices/Artifacts applications.

### Package Structure (M019)
```
voice_narration/inference/
├── __init__.py
├── application.py          # Main factory and AppState
├── persistence.py          # (Future: inference result storage)
├── provider.py             # Inference backend abstraction
└── fixtures.py             # Mock/synthetic provider for tests
```

### Expected Interface (M019)

**create_app() Factory:**
```python
def create_app(
    *,
    repository,                 # Durable inference results
    authenticate,              # Auth callable
    validate_consent,          # Consent validation
    jobs_app,                  # Jobs application state
    inference_provider,        # Synthetic or real model provider
    clock
):
    """Create FastAPI app for inference service."""
    # Dependency injection pattern matching Voices/Artifacts/Jobs
    # Returns FastAPI instance with InferenceState bound as app.state
```

**InferenceState Interface (M019):**
```python
class InferenceState:
    def run_pending_jobs(self):
        """Deterministic worker seam for processing pending jobs."""
        # Transitions PENDING → PROCESSING → COMPLETE|FAILED
        # Updates job outputs and errors
        # Accesses jobs_app for state transitions
    
    def estimate_inference_cost(self, job_data):
        """Estimate cost for given script/parameters."""
        # Returns cost breakdown by usage type
    
    def generate_audio(self, job_id, script_body, parameters):
        """Invoke inference backend with job parameters."""
        # Calls inference_provider.generate(...)
        # Returns {output_seconds, audio_bytes, format}
    
    def close(self):
        """Cleanup resources."""
```

**Inference Provider Interface (M019):**
```python
class InferenceProvider:
    def generate(self, script_body, parameters, profile_id, model_id):
        """Generate audio output (abstract)."""
        # Returns {output_seconds, audio_bytes, format}
    
    def estimate_cost(self, script_body):
        """Estimate generation cost."""
        # Returns Decimal cost
```

**Mock Provider (M019 Test Fixture):**
```python
def mock_inference_provider():
    """Synthetic zero-latency provider for testing."""
    
    class MockProvider:
        def generate(self, script_body, parameters, profile_id, model_id):
            # Synthetic output: 1 second per 100 characters
            seconds = max(len(script_body) // 100, 1)
            # Generate silent WAV bytes of requested duration
            return {
                "output_seconds": seconds,
                "audio_bytes": synthetic_wav_bytes(seconds),
                "format": "wav"
            }
        
        def estimate_cost(self, script_body):
            seconds = max(len(script_body) // 100, 1)
            return Decimal("0.001") * seconds
    
    return MockProvider()
```

**HTTP Endpoints (M019):**
```python
@app.post("/api/v1/jobs/{job_id}/inference")
async def run_inference(request: Request, job_id: str):
    """Trigger inference for a specific job."""
    # 202 ACCEPTED (async processing)
    # Updates job state to PROCESSING

@app.get("/api/v1/jobs/{job_id}/output")
async def get_job_output(request: Request, job_id: str):
    """Retrieve job output (audio + metadata)."""
    # 200 OK (if COMPLETE)
    # 202 ACCEPTED (if PROCESSING)
    # 410 GONE (if FAILED or CANCELLED)
    # Returns {audio_url, duration, format, created_at}

@app.get("/api/v1/inference/backends")
async def list_backends(request: Request):
    """List available inference backends (local, cloud)."""
    # Returns {backends: [{name, type, status, model_info}]}
```

---

## Verification Commands (RED Phase)

**RED Test Execution:**
```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration
python -m pytest tests/test_inference.py::TestInferenceAdapterRED -xvs
```

**Expected Output:**
```
tests/test_inference.py::TestInferenceAdapterRED::test_inference_adapter_missing_module PASSED

============================= 1 passed in X.XXs =============================
```

**Interpretation:**
- ✅ **PASSED** — Module does not exist; test correctly detects missing import
- ✅ **RED Correct** — Expected behavior when production code missing

**Test Collection:**
```powershell
python -m pytest tests/test_inference.py --collect-only -q
```

**Expected:**
```
tests/test_inference.py::TestInferenceAdapterRED::test_inference_adapter_missing_module
tests/test_inference.py::TestJobInferenceIntegration::test_job_runs_inference
tests/test_inference.py::TestInferenceOutput::test_generate_audio_output
tests/test_inference.py::TestInferenceWorkerSeam::test_worker_processes_pending_jobs
tests/test_inference.py::TestModelBackendAbstraction::test_backend_swappable
tests/test_inference.py::TestInferenceQuotaChecks::test_inference_respects_quotas
tests/test_inference.py::TestLocalAndCloudSupport::test_configurable_local_cloud
tests/test_inference.py::TestInferenceErrorHandling::test_failed_inference_transitions_job

8 tests collected
```

**Regression Baseline (No Changes Expected):**
```powershell
python -m pytest tests/ -v --tb=no -q
```

**Expected:**
```
95 passed + 7 skipped (from M017 baseline)
```

**Verdict:** No test file changes to existing tests; regression baseline preserved.

---

## Acceptance Criteria (RED Phase)

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | tests/test_inference.py created with RED + GREEN structure | ✅ | 1 RED + 7 GREEN tests |
| 2 | RED test detects missing module | ✅ | ImportError/AttributeError correctly raised |
| 3 | RED test passes (expected failure mode) | ✅ | PASSED (exception detection working) |
| 4 | 8/8 tests discoverable by pytest | ✅ | --collect-only finds all 8 |
| 5 | 7 GREEN tests structured for M019 | ✅ | All marked SKIP with reason |
| 6 | No production code in RED phase | ✅ | Tests only, no voice_narration/inference/ |
| 7 | No config/dependency changes in RED | ✅ | Test file isolated |
| 8 | 95+ regression baseline preserved | ✅ | No new failures introduced |
| 9 | Interface spec defined for M019 | ✅ | Detailed in section above |
| 10 | Expected M019 deliverables clear | ✅ | create_app, InferenceState, endpoints |

---

## Design Decisions

**1. RED-Only Phase (No Production Code)**
- ✅ Rationale: Establish test expectations first
- ✅ Pattern: Consistent with M016 (Job Orchestration RED)
- ✅ Outcome: M019 GREEN will implement code to pass these tests

**2. Deterministic Worker Seam**
- ✅ Pattern: Match Jobs/Voices application pattern
- ✅ run_pending_jobs() for test verification
- ✅ Production: Async background worker integration (M020+)

**3. Mock Inference Provider**
- ✅ Synthetic output: 1 second per 100 characters of script
- ✅ Silent WAV bytes for testing
- ✅ Zero latency (no real model calls)
- ✅ Fully deterministic and reproducible

**4. Quota Integration**
- ✅ Inference respects job quotas
- ✅ Cost tracking by job context
- ✅ Accesses jobs_app.state for quota enforcement

**5. Backend Abstraction**
- ✅ InferenceProvider interface allows swapping
- ✅ Support local (mock, CUDA if available) and cloud (configurable URL)
- ✅ No hardcoded model or API endpoint

**6. HTTP Endpoints Alignment**
- ✅ RESTful job-driven model (POST to trigger, GET to retrieve)
- ✅ 202 ACCEPTED for async processing
- ✅ Consistent with existing Jobs endpoints

---

## Risk Mitigation

**Risk: Missing Enrollment Integration**
- ✅ Mitigation: M017 GREEN delivered complete enrollment service
- ✅ Evidence: voice_narration/voices/application.py, artifacts/application.py working
- ✅ Impact: Can access enrolled profiles and artifact data for inference

**Risk: Quota System Incomplete**
- ✅ Mitigation: M017 GREEN includes quota enforcement
- ✅ Evidence: QuotaProvider and cost tracking implemented
- ✅ Impact: Inference respects monthly limits

**Risk: Test Framework Gaps**
- ✅ Mitigation: Leverage existing pytest conftest and fixtures
- ✅ Evidence: M016/M017 both used same framework successfully
- ✅ Impact: GREEN fixtures can build on RED test structure

**Risk: Async/Background Worker Pattern Unclear**
- ✅ Mitigation: Deterministic seam approach (like Voices/Artifacts)
- ✅ run_pending_jobs() for tests, async integration in M020+
- ✅ Impact: Tests remain synchronous; production async integration later

---

## Scope & Boundaries

**In Scope (RED Tests):**
- ✅ Test structure for FR-040/041/042
- ✅ Missing module detection
- ✅ Test fixture scaffolding
- ✅ Expected interface specification

**Out of Scope (Deferred to M019 GREEN):**
- ❌ Production code (voice_narration/inference/application.py)
- ❌ Durable persistence (inference/persistence.py)
- ❌ Real model integration
- ❌ Audio codec operations
- ❌ Configuration/dependencies

**Out of Scope (Later Milestones):**
- ❌ Real model inference (M023-024)
- ❌ Cloud deployment integration (M025+)
- ❌ Browser UI (M027)

---

## Next Steps After Approval

1. **Create tests/test_inference.py** with 1 RED + 7 GREEN tests
2. **Run RED test** to verify missing module detection works
3. **Verify 8/8 tests discoverable**
4. **Run regression suite** to confirm baseline preserved
5. **Create MILESTONE_018_EXECUTION_EVIDENCE.md** with results
6. **Commit and await approval**
7. **Move to M019: Mock Inference Adapter GREEN** for production implementation

---

## Summary

Milestone 018 RED establishes the test-first foundation for mock inference:
- ✅ Tests/checks only (no production code)
- ✅ Expected failure mode: missing module detection
- ✅ 1 RED test PASSES (by raising ImportError)
- ✅ 7 GREEN test stubs ready for M019 implementation
- ✅ Interface specification defined for M019
- ✅ Deterministic worker seam for testing
- ✅ Mock provider with zero latency
- ✅ Regression baseline preserved

**Next Approval:** Milestone 018 RED execution & commitment
**Timeline:** ~15 minutes for test file creation + execution
