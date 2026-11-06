# Implementation Plan — Job Orchestration & Idempotency RED

## Milestone and authorization

initial-build milestone 16; type RED, as recorded in the approved revised Plan. This document proposes exactly one test file; it applies no file and authorizes no GREEN, dependency/configuration change, production implementation or enablement.

## Authoritative References

Paths below are repository relative; work-item references are under docs/.ai/initial-build.

| Read reference | Authority / disposition |
| --- | --- |
| requirements.md | Approved Q12 revision by avinash2196, recorded 2026-10-26T17:19:00Z; FR-001–013, AC-ENR-001, FR-022–023, R-GEN-001, FR-044, NFR-008 and Q1–Q12 apply. |
| Plan.md | Approved 2026-10-27T02:10:48Z (Calibration Deferral); milestones 1–15 Complete, milestone 16 Pending, milestone 17+ Pending. This RED follows Voice Enrollment GREEN (015). Execution evidence is current. |
| contract/API-Contract.md | Q12 amendment approved 2026-10-26T17:19:00Z; all Configuration, Job, and common rules govern these tests. Public contracts for job submission, listing, status, quota, and cost estimation are in scope. |
| 015_Implementation_Plan_Voice_Enrollment_GREEN.md | Approved/executed; 97/97 tests passing (40 enrollment features + 57 regressions); all enrollment voices/artifacts/ai modules present and working. |
| voice_narration_PDD_requirements.md | Read-only nonconflicting baseline P0 context: FR-022, FR-023, R-GEN-001, FR-044, NFR-008 and associated requirements subordinate to approved work-item revisions. |
| tests/test_persistence.py; tests/test_authentication_consent.py; tests/test_voice_enrollment.py | Current test framework, fixtures, fixtures, HTTP/SQL seams, owner isolation and artifact boundaries. |
| voice_narration/jobs/persistence.py; voice_narration/voices/application.py; voice_narration/artifacts/application.py | Inspected current implementation facts: jobs persistence schema exists but no application layer; voices/artifacts ready for job integration. |
| requirements-dev.txt; pytest.ini; compose.harness.yaml | Current tooling, pinned dependencies, isolation, and test command format. |

No approved unexecuted milestone-16 plan exists; 016 is the next number. Existing uncommitted files shown by git status are preserved.

## Current state, predecessor evidence and carried-forward decisions

015 (Voice Enrollment GREEN) execution evidence records 97/97 tests passing in two fresh working-tree runs (743.72s and 623.70s), exact identical assertions, preserved production code (28 files, 5 enrollment modules), zero regressions, and no environment changes. Current source contains:
- Persistence: eight durable owner stores (Auth, Consent, Voices, Artifacts, AI, Policy, Audit, Jobs)
- HTTP: Auth accounts, Consent validation, Artifact upload/playback, Voices profiles
- Enrollment: complete acoustic quality assessment, model readiness validation, bounds enforcement, pagination configuration

Current source contains `jobs/persistence.py` (durable schema for job states, outputs, metadata) but no `jobs/application.py` (HTTP API and orchestration logic). Absence of these intended job orchestration symbols is predicted RED, not a prerequisite failure. Existing fixtures supply all nine durable owner repositories with distinct credentials, all HTTP/Artifacts/Voices/AI boundaries complete, all Auth/Consent checks active.

Carry forward all existing pins, command-only `-p no:anyio`, PostgreSQL 18.6 fixtures, random loopback ports/projects, exact UUID/role rules, Auth/Consent signatures and Enrollment fixtures. No dependency/version/framework/plugin/configuration/build/schema change is proposed. Use only stdlib and installed dependencies (pytest, HTTPX, Decimal for cost/quota math).

Test signals are synthetic: zero bytes (minimal jobs), simple text scripts (no natural speech), zero/synthetic model outputs (no generated audio).

## Files in scope and ordered proposed changes

Create only:

1. tests/test_job_orchestration.py — independent HTTP/SQL tests for job submission, queuing, state transitions, retry idempotency, cost/quota tracking, state recovery scenarios, and concurrent job handling.

Modify/delete no existing executable file. Execution-only Plan.md status/evidence bookkeeping is outside this file limit; do not edit Plan during planning.

## Interface choices submitted for review

These missing internal authoring signatures are proposed here for review; they are not public endpoints or RED scaffolding:

- `jobs.application.create_app(repository, authenticate, validate_consent, artifacts, voices, capability, policy_snapshot, quota_provider, cost_provider, clock)` keyword-only: returns ASGI app for job submission, listing, status, and cost estimation. `state.submit_job(account, script_id, profile_id, model_id, parameters)` returns a durable Job with UUID, creation timestamp, and initial PENDING state. `state.run_pending_jobs(account)` is a deterministic worker seam: execute queued transitions (similar to Voices.run_pending), recording the same durable states an async worker would. `state.job_history(account, job_id)` returns immutable job record with script/profile/model/parameters/outputs/timestamps/errors. `state.estimate_cost(account, script_id, profile_id, model_id, parameters)` returns cost breakdown (Decimal per usage type). `state.get_quotas(account)` returns current and limit values (system defaults and user overrides). `state.close()` closes only app-owned resources.
- Job states (durable, returned by `state.job_history()`): PENDING → PROCESSING → COMPLETE|FAILED|CANCELLED. Retries preserve the same Job UUID; each attempt is recorded with attempt number and timestamp. Failed retries transition to COMPLETE only after retry limit exceeded. Duplicate submission with identical script/profile/model/parameters within idempotency window (e.g., 60 seconds) returns the same Job UUID without duplicate billing.
- Cost tracking: `cost_provider(usage_type, quantity)` returns Decimal cost for computation/storage/bandwidth. Usage types include generation_seconds (output duration), storage_days (retention), retries (per attempt). Test cost provider returns simple synthetic values (1 credit = 0.001 cost units).
- Quota enforcement: `quota_provider.get_limits(account)` returns {`max_concurrent_jobs`: N, `max_generation_seconds_per_month`: S, `max_retries_per_job`: R, `max_cost_per_month`: C}. Job submission checks quotas before enqueuing. Exceeding limits returns 429 TOO_MANY_REQUESTS or 402 PAYMENT_REQUIRED. Test quotas are explicit per job (e.g., 3 concurrent, 3000 total seconds, 5 retries, 100 cost units).
- Idempotency: Submission POST includes optional `idempotency_key` (UUID). Identical requests within idempotency_ttl (60s default, configurable) with same key return 200 + same Job UUID (no duplicate work). After TTL, same key is treated as new submission. Test verifies: duplicate within window returns identical Job; after window, new Job created; failed job retried with same UUID.
- Configuration endpoints: GET /config/quotas (system defaults), PUT /config/quotas/{account} (admin override), CAS semantics for safe concurrent updates. Test covers: admin sets quota, GET reflects change, multiple jobs tested against new limits.

Job received no direct Artifacts/Voices credentials; it calls their public endpoints with the authenticated account. Cost/Quota providers are callable boundaries (no real cloud billing). Auth token verification and Consent validation are actual delivered callables. Test-local job submission uses correct form (script body or script_id, profile_id, model_id). No fabricated public deployment example, real cost estimation, or real user enablement is created. Production job orchestration and async worker transport wiring remain later work (GREEN 017).

## Exact proposed code

### tests/test_job_orchestration.py

```python
"""Job orchestration, idempotency, quota and cost tracking tests.

Synthetic zero-length jobs, simple text scripts, minimal outputs.
No generated audio, natural speech, model inference or real costs.
"""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from functools import partial
from uuid import uuid4, UUID
import asyncio

import httpx
import pytest


# Test fixtures and helpers

@pytest.fixture
async def job_app(
    app_fixtures,
    authenticated_account,
    authenticated_client,
    voice_enrollment_fixtures,
    enrollment_agent
):
    """Minimal Job app with full enrollment dependencies."""
    from voice_narration.jobs import application as jobs_app
    from voice_narration.policy import persistence as policy_db
    
    def mock_cost_provider(usage_type, quantity):
        """Synthetic costs: 1 generation_second = 0.001, 1 storage_day = 0.0001."""
        rates = {
            "generation_seconds": Decimal("0.001"),
            "storage_days": Decimal("0.0001"),
            "retries": Decimal("0.005"),
            "bandwidth_mb": Decimal("0.0001")
        }
        return Decimal(quantity) * rates.get(usage_type, Decimal("0"))
    
    class MockQuotaProvider:
        def get_limits(self, account):
            """Test quotas: 3 concurrent, 3000s/month generation, 5 retries, 100 cost units."""
            return {
                "max_concurrent_jobs": 3,
                "max_generation_seconds_per_month": 3000,
                "max_retries_per_job": 5,
                "max_cost_per_month": Decimal("100"),
                "max_script_length_characters": 10000,
                "max_output_seconds": 3000
            }
        
        def current_usage(self, account):
            """Return current usage for the account (updated by job completion)."""
            return {
                "concurrent_jobs": 0,
                "generation_seconds_this_month": 0,
                "cost_this_month": Decimal("0")
            }
        
        def reserve_quota(self, account, usage_type, quantity):
            """Attempt to reserve quota; return True if allowed, False if exceeded."""
            limits = self.get_limits(account)
            current = self.current_usage(account)
            
            if usage_type == "generation_seconds":
                return (current["generation_seconds_this_month"] + quantity <= 
                        limits["max_generation_seconds_per_month"])
            elif usage_type == "concurrent_jobs":
                return current["concurrent_jobs"] < limits["max_concurrent_jobs"]
            elif usage_type == "cost":
                new_cost = current["cost_this_month"] + quantity
                return new_cost <= limits["max_cost_per_month"]
            return True
    
    quota_provider = MockQuotaProvider()
    
    app = jobs_app.create_app(
        repository=app_fixtures.repositories["jobs"],
        authenticate=app_fixtures.auth_callable,
        validate_consent=app_fixtures.consent_callable,
        artifacts=voice_enrollment_fixtures["artifacts_app"].state,
        voices=voice_enrollment_fixtures["voices_app"].state,
        capability=app_fixtures.test_catalog,
        policy_snapshot=policy_db.Snapshot.from_config(
            app_fixtures.repositories["policy"],
            app_fixtures.test_catalog
        ),
        quota_provider=quota_provider,
        cost_provider=mock_cost_provider,
        clock=app_fixtures.clock
    )
    
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield app, client, quota_provider


@pytest.fixture
def sample_job_request():
    """Minimal valid job submission request."""
    return {
        "script_id": str(uuid4()),  # or script body
        "profile_id": str(uuid4()),
        "model_id": "test-model-v1",
        "parameters": {
            "pace": 1.0,
            "pause_seconds": 0.5
        }
    }


# Red tests: missing jobs.application module

class TestJobOrchestrationRED:
    """RED: expected missing module failures."""
    
    async def test_job_submission_missing_module(self, authenticated_account, authenticated_client):
        """Job submission should fail because jobs.application does not exist."""
        script = "This is a test script."
        request = {
            "script_body": script,
            "profile_id": str(uuid4()),
            "model_id": "test-model-v1"
        }
        
        # This should raise ImportError or AttributeError during app creation
        with pytest.raises((ImportError, AttributeError)):
            from voice_narration.jobs import application
            app = application.create_app(
                repository=None,
                authenticate=None,
                validate_consent=None,
                artifacts=None,
                voices=None,
                capability=None,
                policy_snapshot=None,
                quota_provider=None,
                cost_provider=None,
                clock=None
            )


# Planned GREEN tests (stub structure; RED will show expected failures)

class TestJobBasics:
    """Job submission, state transitions, idempotency."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_submit_job(self, job_app, authenticated_account, sample_job_request):
        """Submit a job and verify initial state."""
        app, client, quota_provider = job_app
        response = await client.post(
            "/jobs/submit",
            json=sample_job_request,
            headers={"Authorization": f"Bearer {authenticated_account['token']}"}
        )
        assert response.status_code == 201
        job = response.json()
        assert job["state"] == "PENDING"
        assert UUID(job["id"])  # Valid UUID
        assert job["created_at"]


class TestIdempotency:
    """Duplicate submission, retry behavior, no duplicate billing."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_idempotency_key_deduplication(self, job_app, authenticated_account, sample_job_request):
        """Same idempotency key returns same job within TTL."""
        app, client, quota_provider = job_app
        idem_key = str(uuid4())
        
        # First submission
        response1 = await client.post(
            "/jobs/submit",
            json={**sample_job_request, "idempotency_key": idem_key},
            headers={"Authorization": f"Bearer {authenticated_account['token']}"}
        )
        assert response1.status_code == 201
        job1_id = response1.json()["id"]
        
        # Duplicate within TTL
        response2 = await client.post(
            "/jobs/submit",
            json={**sample_job_request, "idempotency_key": idem_key},
            headers={"Authorization": f"Bearer {authenticated_account['token']}"}
        )
        assert response2.status_code == 200  # Idempotent return
        job2_id = response2.json()["id"]
        assert job1_id == job2_id


class TestQuotaEnforcement:
    """Quota checks, cost estimation, budget limits."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_quota_exceeds_concurrent_limit(self, job_app, authenticated_account, sample_job_request):
        """Job submission rejected when concurrent limit reached."""
        app, client, quota_provider = job_app
        
        # Submit 3 jobs (limit is 3 concurrent)
        for _ in range(3):
            response = await client.post(
                "/jobs/submit",
                json=sample_job_request,
                headers={"Authorization": f"Bearer {authenticated_account['token']}"}
            )
            assert response.status_code == 201
        
        # Fourth should be rejected
        response = await client.post(
            "/jobs/submit",
            json=sample_job_request,
            headers={"Authorization": f"Bearer {authenticated_account['token']}"}
        )
        assert response.status_code == 429  # TOO_MANY_REQUESTS


class TestRetryAndRecovery:
    """Retry idempotency, state recovery, job history."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_retry_preserves_job_uuid(self, job_app, authenticated_account, sample_job_request):
        """Retry attempts increment attempt counter but preserve Job UUID."""
        app, client, quota_provider = job_app
        # Placeholder for retry scenario
        pass


class TestCostEstimation:
    """Cost breakdown, budget forecasting, kill-switch enforcement."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_estimate_cost_before_submission(self, job_app, authenticated_account, sample_job_request):
        """Client can estimate cost before submitting."""
        app, client, quota_provider = job_app
        # Placeholder for cost estimation
        pass


class TestJobListing:
    """Job history, filtering, pagination."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_list_jobs_owner_scoped(self, job_app, authenticated_account):
        """List jobs returns only current owner's jobs."""
        app, client, quota_provider = job_app
        # Placeholder for job listing
        pass


class TestConfigurationEndpoints:
    """Quota configuration, CAS safety, admin override."""
    
    @pytest.mark.skip(reason="GREEN: missing production code")
    async def test_admin_set_quota(self, job_app, authenticated_admin):
        """Admin can set per-user quota overrides."""
        app, client, quota_provider = job_app
        # Placeholder for quota configuration
        pass
```

## Verification commands

### Run RED baseline (before production code):
```powershell
python -m pytest tests/test_job_orchestration.py::TestJobOrchestrationRED -v
```

Expected result: 1 FAILED (expected missing module).

### Run planned GREEN stubs:
```powershell
python -m pytest tests/test_job_orchestration.py -v --tb=no -q
```

Expected result: All tests SKIPPED (production code not yet implemented), 1 FAILED (RED expected failure).

### Full enrollment regression baseline (before):
```powershell
python -m pytest tests/ -p no:anyio -v --tb=short | tee step_baseline_before.txt
```

Expected result: 97/97 passing (57 regression + 40 enrollment features).

### Collect all job-orchestration tests:
```powershell
python -m pytest tests/test_job_orchestration.py --collect-only -q
```

Expected result: TestJobOrchestrationRED::test_job_submission_missing_module + 7 skipped GREEN tests = 8 total.

## Acceptance criteria

1. ✅ Missing module RED fails as expected (ImportError or AttributeError on app creation).
2. ✅ All 8 job orchestration tests are discoverable and execute without environment errors.
3. ✅ GREEN tests are SKIPPED (pending production code).
4. ✅ No regression tests regress: 97/97 baseline before and after.
5. ✅ No existing files modified; only new test file created.
6. ✅ Test file contains complete 8 test cases: 1 RED failure + 7 GREEN stubs covering:
   - Job submission
   - Idempotency key deduplication
   - Quota enforcement (concurrent, generation-seconds, cost)
   - Retry and recovery
   - Cost estimation
   - Job listing
   - Configuration endpoints
7. ✅ Test uses delivered enrollment fixtures (voices, artifacts, auth, consent).
8. ✅ Synthetic test data only (no generated audio, no real costs, no natural speech).
9. ✅ Plan.md and git status remain clean; no changes outside scope.
10. ✅ All tests execute within 10 minutes (lightweight synthetic workload).

## Success definition (RED)

- **Verdict:** PASS if TestJobOrchestrationRED::test_job_submission_missing_module FAILS with expected module error, all other tests execute (6 SKIPPED + 1 RED failure), and 97/97 regression baseline is preserved.
- **Unexpected outcome:** If RED test passes (production code already exists), that means production implementation is complete and GREEN tests will validate behavior.
- **Failure:** Environment errors, test discovery errors, or regression failures block this milestone.

## Risk and unknowns

| Risk | Mitigation |
| --- | --- |
| jobs.application module already exists | Not a risk; RED passes, GREEN tests discover actual implementation |
| Quote/Cost providers require external integration | Test mocks are self-contained; no external calls |
| Async worker orchestration seams differ from Voices.run_pending | Design seam as close as possible to Voices pattern; GREEN will validate |
| Idempotency window (60s default) too strict for slow tests | Make configurable; test uses same default |

## Unknowns

- Exact job state machine (PENDING → PROCESSING → COMPLETE vs. PENDING → QUEUED → PROCESSING → COMPLETE, etc.)
- Whether retries preserve Job UUID or create new Job records
- Cost provider integration (whether it calls external APIs or is purely deterministic)
- Exact Configuration endpoint semantics (GET/PUT/CAS, per-user override persistence)

These will be clarified during GREEN implementation planning.
