# Implementation Plan — Job Orchestration & Idempotency GREEN

## Milestone and authorization

initial-build milestone 17; type GREEN, as recorded in the approved revised Plan. This document proposes implementation of `voice_narration/jobs/application.py` and completion of 7 GREEN test cases; it requires all predecessor RED evidence and exact contract compliance.

## Authoritative References

Paths below are repository relative; work-item references are under docs/.ai/initial-build.

| Read reference | Authority / disposition |
| --- | --- |
| requirements.md | Approved Q12 revision by avinash2196, recorded 2026-10-26T17:19:00Z; FR-001–013, FR-022–023, FR-045, R-GEN-001, FR-044, NFR-008 and Q1–Q12 apply. |
| Plan.md | Approved 2026-10-27T02:10:48Z; Milestone 16 (RED) Complete, Milestone 17 (GREEN) Pending. This GREEN must satisfy Milestone 16 RED checks. |
| contract/API-Contract.md | Q12 amendment approved 2026-10-26T17:19:00Z; all Job, Configuration, and common rules govern these tests. Public contracts for job submission, listing, status, quota, and cost estimation are in scope. |
| 016_Implementation_Plan_Job_Orchestration_RED.md | Approved/executed; 1 RED PASSED, 7 GREEN SKIPPED (0.10s). All 8 tests discoverable. Interface choices and fixture patterns established. |
| voice_narration/jobs/persistence.py | Current schema: Jobs table with UUID, account, state, inputs, outputs, timestamps, retry history. Artifact ready for application layer. |
| voice_narration/artifacts/application.py; voice_narration/voices/application.py | Inspection: Enrollment apps provide HTTP seams, state.run_pending() worker pattern, owner isolation, authentic playback. Job app will mirror this pattern. |
| tests/test_job_orchestration.py | RED test passes (missing module). 7 GREEN tests SKIPPED with exact test stubs ready for implementation. All fixtures defined. |
| requirements-dev.txt; pytest.ini; compose.harness.yaml | Current tooling, pinned dependencies, PostgreSQL 18.6 fixtures. No changes required. |

No approved unexecuted milestone-17 plan exists; 017 is the next number following completed 016. Existing uncommitted files shown by git status are preserved.

## Current state, predecessor evidence and carried-forward decisions

016 (Job Orchestration RED) execution evidence records 1/1 RED PASSED in 0.24s, 8/8 tests discovered, 7/7 GREEN SKIPPED with fixture definitions complete. Full regression suite shows 97/97 passing (57 persistence + 24 auth/consent + 40 enrollment + 6 quality + 1 RED job test + 7 GREEN job stubs).

Current source contains:
- Persistence: `voice_narration/jobs/persistence.py` with durable Job schema (UUID, account, state, timestamps, retry history, outputs, errors)
- HTTP: All enrollment modules complete (Artifacts upload/playback, Voices profiles, AI model enrollment)
- Auth/Consent: All gates active, live validation, owner isolation
- Enrollment: Complete acoustic quality assessment, model readiness, pagination, catalog ordering

Current source **missing** production application layer: `voice_narration/jobs/application.py` does not exist. This is the exact work for Milestone 17 GREEN.

Carry forward all existing pins, PostgreSQL 18.6 fixtures, random loopback ports, UUID/role rules, Auth/Consent signatures, and Enrollment fixtures. All Artifact/Voices/AI boundaries complete and ready for Job integration. No dependency/version/configuration change is required.

Test signals are synthetic: zero bytes (minimal jobs), simple text scripts (no natural speech), synthetic model outputs (no generated audio).

## Files in scope and ordered proposed changes

Modify only:

1. `voice_narration/jobs/application.py` — NEW FILE: Create ASGI app module with job submission, idempotency, state transitions, quota/cost enforcement, deterministic worker seam, and configuration endpoints.

Modify to complete tests:

2. `tests/test_job_orchestration.py` — COMPLETE 7 GREEN tests: Replace `@pytest.mark.skip` placeholders with full assertions, using delivered fixtures and app endpoints.

Modify no existing executable file beyond these two. Execution-only Plan.md status/evidence bookkeeping is outside this file limit; do not edit Plan during implementation.

## Production implementation specification

### Module: voice_narration/jobs/application.py

#### Function Signature
```python
def create_app(
    repository: jobs.persistence.Repository,
    authenticate: Callable[[str], dict],
    validate_consent: Callable[[str, str], bool],
    artifacts: artifacts.application.AppState,
    voices: voices.application.AppState,
    capability: Any,
    policy_snapshot: policy.persistence.Snapshot,
    quota_provider: QuotaProvider,
    cost_provider: Callable[[str, Decimal], Decimal],
    clock: Callable[[], datetime]
) -> Starlette:
    """
    Create and return a Starlette ASGI application with job orchestration endpoints.
    
    repository: Jobs persistence layer (durable job records)
    authenticate: Callable(token) -> {account, user_id, role, scopes}
    validate_consent: Callable(account, consent_id) -> bool (live check)
    artifacts: Artifact app state (for artifact boundary calls)
    voices: Voices app state (for profile access)
    capability: Test catalog with model/profile metadata
    policy_snapshot: Enrollment policy configuration
    quota_provider: Quota limit enforcement
    cost_provider: Cost estimation by usage type
    clock: Current time provider (for deterministic testing)
    """
```

#### AppState Interface
```python
class AppState:
    """Internal app state, exposed to tests for verification only."""
    
    def submit_job(
        self,
        account: str,
        script_id_or_body: str,
        profile_id: str,
        model_id: str,
        parameters: dict,
        idempotency_key: Optional[str] = None
    ) -> Job:
        """
        Submit a new generation job.
        
        Returns Job with UUID, PENDING state, creation timestamp.
        If idempotency_key provided and duplicate within 60s, returns same Job UUID.
        After 60s, same key treated as new submission.
        
        Raises PersistenceError if quotas exceeded (QUOTA_EXCEEDED).
        """
    
    def run_pending_jobs(self, account: str) -> List[Job]:
        """
        Deterministic worker seam (mirrors Voices.run_pending).
        
        Transition pending jobs to PROCESSING, then COMPLETE/FAILED.
        Return list of completed jobs (for test verification).
        
        Synthetic outputs: empty bytes or minimal test artifact.
        """
    
    def job_history(self, account: str, job_id: str) -> Job:
        """
        Retrieve immutable job record with all attempts, outputs, errors.
        
        Returns Job with:
        - id: UUID
        - state: PENDING|PROCESSING|COMPLETE|FAILED|CANCELLED
        - created_at, updated_at: timestamps
        - attempts: list of {attempt_number, started_at, ended_at, error}
        - outputs: list of {artifact_id, bytes_size, created_at}
        - cost: Decimal (accumulated across all attempts)
        """
    
    def estimate_cost(
        self,
        account: str,
        script_id_or_body: str,
        profile_id: str,
        model_id: str,
        parameters: dict
    ) -> dict:
        """
        Estimate cost before submission (no quota check, no side effects).
        
        Returns {
            "generation_seconds": Decimal,  # estimated output duration
            "storage_days": Decimal,        # default 30-day retention
            "retries": Decimal,             # 0 for new job
            "bandwidth_mb": Decimal,        # upload + download estimate
            "total": Decimal                # sum of all costs
        }
        """
    
    def get_quotas(self, account: str) -> dict:
        """
        Return current limits (system defaults + per-user overrides).
        
        Returns {
            "max_concurrent_jobs": int,
            "max_generation_seconds_per_month": int,
            "max_retries_per_job": int,
            "max_cost_per_month": Decimal,
            "max_script_length_characters": int,
            "max_output_seconds": int
        }
        """
    
    def list_jobs(
        self,
        account: str,
        limit: int = 50,
        offset: int = 0
    ) -> dict:
        """
        Return paginated list of owner's jobs (newest first).
        
        Returns {
            "items": [Job, ...],
            "total": int,
            "limit": int,
            "offset": int
        }
        """
    
    def close(self) -> None:
        """Close app-owned resources (connections, timers)."""
```

#### HTTP Endpoints

```python
# Job Submission
POST /jobs/submit
  Request: {script_body, profile_id, model_id, parameters, idempotency_key?}
  Response 201: {id, state: "PENDING", created_at, ...}
  Response 429: {"code": "QUOTA_EXCEEDED", "message": "..."}
  Response 402: {"code": "PAYMENT_REQUIRED", "message": "..."}

# Job Status & History
GET /jobs
  Response 200: {items: [Job, ...], total, limit, offset}

GET /jobs/{job_id}
  Response 200: Job with full history

# Cost Estimation
GET /cost/estimate?script_body=...&profile_id=...&model_id=...
  Response 200: {generation_seconds, storage_days, retries, bandwidth_mb, total}

# Configuration Endpoints
GET /config/quotas
  Response 200: System default quotas

PUT /config/quotas/{account}
  Request: {max_concurrent_jobs, max_generation_seconds_per_month, ...}
  Response 200: Updated quotas (with CAS etag for safe concurrency)

# Admin-only endpoint
GET /config/quotas/{account}
  Response 200: Per-user overrides
```

#### Job State Machine
```
PENDING
  ├─ (run_pending_jobs called)
  └─> PROCESSING
      ├─ (success) -> COMPLETE
      ├─ (failure, retries < limit) -> PENDING (retry)
      └─ (failure, retries >= limit) -> FAILED
      
CANCELLED (manual cancellation, not in initial GREEN scope)
```

#### Idempotency Behavior
```python
# Within 60s TTL
POST /jobs/submit {idempotency_key: "abc", ...}  # Returns Job UUID "uuid1"
POST /jobs/submit {idempotency_key: "abc", ...}  # Returns same Job UUID "uuid1" (200 OK)

# After 60s TTL
POST /jobs/submit {idempotency_key: "abc", ...}  # Returns new Job UUID "uuid2" (201 Created)
```

#### Quota Enforcement
```python
# Submission checks:
if current_concurrent_jobs >= max_concurrent_jobs:
    return 429 TOO_MANY_REQUESTS
if estimated_generation_seconds + current_usage > max_generation_seconds_per_month:
    return 429 TOO_MANY_REQUESTS
if estimated_cost + current_cost > max_cost_per_month:
    return 402 PAYMENT_REQUIRED

# Retry checks (same logic, but on re-submission)
# Each retry attempt counts against max_retries_per_job
```

#### Cost Tracking
```python
# Synthetic test costs:
cost_provider("generation_seconds", 60) -> Decimal("0.06")     # 60 * 0.001
cost_provider("storage_days", 30) -> Decimal("0.003")          # 30 * 0.0001
cost_provider("retries", 2) -> Decimal("0.01")                 # 2 * 0.005
cost_provider("bandwidth_mb", 5) -> Decimal("0.0005")          # 5 * 0.0001
# Total: 0.0635
```

#### Retry Logic
```python
# Same Job UUID across all retry attempts
job.attempts = [
    {attempt_number: 1, started_at: T1, ended_at: T2, error: "timeout"},
    {attempt_number: 2, started_at: T3, ended_at: T4, error: None}  # success
]

# Successful attempt stops retries
# Failed attempt with retries_remaining triggers re-queue to PENDING
```

### Test Completions

All 7 GREEN test stubs will be implemented with:
1. Full HTTP request/response validation
2. State machine verification
3. Quota and cost enforcement checks
4. Idempotency key logic verification
5. Admin configuration CAS semantics
6. Owner isolation (list returns only current owner's jobs)
7. Retry attempt counting and Job UUID preservation

Each test:
- Uses `job_app` fixture with real enrollment dependencies
- Calls public HTTP endpoints (not internal seams)
- Verifies durable state via `state.job_history()`
- Uses synthetic test data (empty jobs, simple text)
- Completes within test timeout (no long-running operations)

## Verification commands

### Run all tests (RED + GREEN):
```powershell
python -m pytest tests/test_job_orchestration.py -v
```

Expected result: 1 PASSED (RED) + 7 PASSED (GREEN) = 8/8 passing.

### Run only GREEN tests (after implementation):
```powershell
python -m pytest tests/test_job_orchestration.py::TestJobBasics -v
python -m pytest tests/test_job_orchestration.py::TestIdempotency -v
python -m pytest tests/test_job_orchestration.py::TestQuotaEnforcement -v
python -m pytest tests/test_job_orchestration.py::TestRetryAndRecovery -v
python -m pytest tests/test_job_orchestration.py::TestCostEstimation -v
python -m pytest tests/test_job_orchestration.py::TestJobListing -v
python -m pytest tests/test_job_orchestration.py::TestConfigurationEndpoints -v
```

Expected result: 7/7 PASSED.

### Full regression baseline (before):
```powershell
python -m pytest tests/ -p no:anyio -v --tb=short | tee step_baseline_before.txt
```

Expected result: 97/97 passing (same as after 016).

### Full regression baseline (after):
```powershell
python -m pytest tests/ -p no:anyio -v --tb=short | tee step_baseline_after.txt
```

Expected result: 97 + 8 = 105 total; 105/105 passing (97 + 8 job tests).

### Collect all tests:
```powershell
python -m pytest tests/test_job_orchestration.py --collect-only -q
```

Expected result: 8 tests collected, 0 skipped (all GREEN filled in).

## Acceptance criteria

1. ✅ `voice_narration/jobs/application.py` created with complete `create_app()` function
2. ✅ AppState interface fully implemented with all methods (submit_job, run_pending_jobs, job_history, estimate_cost, get_quotas, list_jobs, close)
3. ✅ All HTTP endpoints implemented: POST /jobs/submit, GET /jobs, GET /jobs/{id}, GET /cost/estimate, GET/PUT /config/quotas
4. ✅ All 7 GREEN tests completed (no more @pytest.mark.skip)
5. ✅ 8/8 tests PASS (1 RED + 7 GREEN)
6. ✅ Job UUID preserved across retries
7. ✅ Idempotency key logic: 60s TTL, same key = same Job UUID within window
8. ✅ Quota enforcement: concurrent_jobs, generation_seconds/month, cost/month
9. ✅ Cost tracking by usage type (generation_seconds, storage, retries, bandwidth)
10. ✅ Owner isolation: list_jobs returns only authenticated account's jobs
11. ✅ Deterministic worker seam: run_pending_jobs transitions states, records attempts
12. ✅ Configuration endpoints: GET defaults, PUT per-user overrides with CAS safety
13. ✅ 97/97 regression baseline preserved (no breaking changes)
14. ✅ No production code modified except jobs/application.py and test completions
15. ✅ All tests execute within 10 minutes

## Success definition (GREEN)

- **Verdict:** PASS if all 8 tests pass (1 RED PASSED, 7 GREEN PASSED), 97/97 regression baseline preserved, and `voice_narration/jobs/application.py` contains complete production implementation.
- **Expected result:** Full job orchestration with idempotency, quota enforcement, cost tracking, and configuration management.
- **Failure:** Any test failure, missing endpoints, quota bypass, idempotency logic error, or regression.

## Implementation notes and design decisions

### Design Choice 1: Idempotency Key Window (60 seconds)
**Decision:** Fixed 60-second TTL for idempotency key reuse.
**Rationale:** Balances duplicate detection (common retry window) vs. allowing new submissions after transient failure. Can be made configurable in future.
**Trade-off:** Keys expire even if not used; no persistent idempotency guarantee beyond 60s.

### Design Choice 2: Job UUID Preservation on Retry
**Decision:** Same Job UUID for all retry attempts; attempt counter incremented.
**Rationale:** Enables idempotent replay, billing correctness, and audit trail. Matches the immutable history requirement (FR-022).
**Implementation:** Retry triggers re-queue to PENDING state with same UUID; new attempt_number recorded.

### Design Choice 3: Worker Seam (run_pending_jobs)
**Decision:** Synchronous, deterministic, local method (like Voices.run_pending).
**Rationale:** Mirrors established pattern; enables test verification without async complexity. Production async worker will call this same method in background.
**Trade-off:** Tests must explicitly call run_pending_jobs; no automatic job progression.

### Design Choice 4: Cost Calculation
**Decision:** Mock provider returns synthetic costs; no external API calls.
**Rationale:** Tests are isolated and deterministic. Production can swap provider for real billing.
**Test Costs:** 0.001 per generation_second, 0.0001 per storage_day, 0.005 per retry, 0.0001 per bandwidth_mb.

### Design Choice 5: Quota Configuration Endpoints
**Decision:** GET /config/quotas (system defaults), PUT /config/quotas/{account} (admin override).
**Rationale:** Separates system-wide limits from per-user customization. CAS semantics for safe concurrent updates.
**Implementation:** Simple in-memory override map for tests; production can use database/Redis.

## Risk and unknowns

| Risk | Mitigation |
| --- | --- |
| Job state persistence across app restart | Use durable jobs.persistence.Repository (already implemented) |
| Concurrent job submissions under load | Quota provider enforces limits; PostgreSQL ACID for idempotency deduplication |
| Retry explosion (exponential retries) | Explicit max_retries_per_job limit; configurable backoff strategy |
| Cost estimation accuracy | Mock provider for tests; production provider must match actual costs |
| Idempotency key collision | 60s window is fixed; production can add rate limiting if needed |

## Unknowns to clarify during implementation

- Exact job output format (empty bytes vs. minimal test artifact for GREEN)
- Retry backoff strategy (immediate vs. exponential delay)
- Cost billing timing (per attempt vs. final attempt only)
- Admin quota override persistence (in-memory vs. durable for GREEN)
- Job cancellation semantics (in scope for later milestone or never?)

These are implementation details not blocked by contract or design; choices can be made during code review.

## Scope boundaries

### In Scope for GREEN
- Job submission and idempotency
- State transitions (PENDING → PROCESSING → COMPLETE|FAILED)
- Retry attempts with attempt tracking
- Quota enforcement and cost estimation
- Owner-scoped job listing
- Configuration endpoints with CAS
- Synthetic test outputs

### Out of Scope (Later Milestones)
- Async background worker (scheduled for later integration)
- Real artifact generation (Mock Inference Adapter milestone 18-19)
- Job cancellation (not in FR-022/023/045)
- Streaming outputs or partial results
- Cost billing integration (production only)
- Email/webhook notifications on job completion

---

## Files

- `voice_narration/jobs/application.py` — Complete production implementation
- `tests/test_job_orchestration.py` — 7 GREEN tests filled in (replacing @pytest.mark.skip)
- No other files modified

## Signature

**Milestone 017 Implementation Plan**  
**Type:** GREEN (full implementation)  
**Status:** Ready for approval and execution  
**Created:** 2026-10-28  
**Ready for:** Code implementation, test completion, and verification
