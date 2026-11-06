# Architecture Revision Summary — Final Consistency Pass

**Date:** 2026-10-20
**Work Item:** initial-build
**Revision Pass:** Final Consistency and Requirement-Alignment Correction

---

## Revision Status

✅ **COMPLETE** — All 5 architecture artifacts are now internally consistent and requirement-aligned.

### Files Updated (5/5)
1. **System-Architecture.md** — Added API Gateway public/internal route inventory; clarified Auth non-dependency
2. **Service-Boundaries.md** — Updated Voice Profile and Narration Job schemas with FR-023 fields; removed duplicate job state rows; fixed Inference Worker event consumption (voice_profile.enroll, narration.generate); removed stale "All services → Auth on every request"; added Orchestrator→AI Gateway cost-estimation call
3. **Data-Ownership.md** — Updated job lifecycle from SUBMITTED/PROCESSING to FR-022 states; clarified Orchestrator commitment timing
4. **Interaction-Flows.md** — Previously corrected; remains consistent
5. **Event-Catalog.md** — Fixed ordering examples (removed enrollment_requested, added quality_warning); replaced all unsupported fixed retention values with "Per approved retention policy"

---

## Summary of Stale Terminology Removed

| Issue | Removed | Replaced With |
|-------|---------|--------------|
| Job state naming | SUBMITTED, PROCESSING | QUEUED, PREPARING, RUNNING, POST_PROCESSING, COMPLETED |
| Enrollment workflow | enrollment_requested (worker command) | voice_profile.enroll (work command); voice_profile.enrolled (domain event) |
| Narration workflow | narration_job.submitted as worker command | narration.generate (work command); narration_job.submitted (domain event only) |
| Voice Profile states | PENDING, ENROLLING, ENROLLED, FAILED, REVOKED | PENDING, QUALITY_CHECKING, AWAITING_USER_OVERRIDE, ENROLLING, ENROLLED, FAILED, REVOKED |
| Retention assumptions | "90 days access logs", "1 year audit", "2 years compliance" | "Per approved retention policy" (except required values: 30 days generated-audio, max 3000 seconds output) |
| Auth dependency | "All services → Auth Service → On every request" | Auth issues tokens; services validate locally; no per-request dependency |
| Usage trigger | "Usage & Policy consumes narration_job.completed" | Orchestrator calls synchronous commit-usage API before COMPLETED transition |

---

## Final Service Responsibilities (9 Services, Frozen)

1. **Auth Service** — User identity, token issuance, local validation material (JWKS)
2. **Consent Service** — Immutable consent records, revocation tracking, user-facing revoke API
3. **Voice Profile Service** — Profile lifecycle (PENDING→QUALITY_CHECKING→AWAITING_USER_OVERRIDE→ENROLLING→ENROLLED/FAILED/REVOKED), quality findings, model/version metadata, user-facing quality-override API
4. **Narration Orchestrator** — Job lifecycle (FR-022 states), idempotency, quota coordination, usage commitment sequencing, generated-audio cascade on profile revocation
5. **Artifact Service** — Binary storage, signed URL access, retention enforcement, revocation-driven deletion (overrides retention)
6. **Usage & Policy Service** — Quota reservation (idempotent), usage commitment (idempotent), budget enforcement
7. **AI Gateway** — Model routing, speaker conditioning, cost-estimation API for Orchestrator
8. **Inference Worker** — Execution orchestration, quality analysis, enrollment/generation processing, status reporting via API (does NOT publish events)
9. **Audit Service** — Immutable event log, read-only async consumption

---

## Final API Routing (via API Gateway)

**Public/Protected Routes:**
- Auth: register, verify, login, get-me
- Consent: record, get, revoke (user-initiated)
- Voice Profile: create, list, get, delete (revoke), quality-override
- Narration Orchestrator: submit, list, get, cancel
- Artifact: download-url, preview-url
- Usage & Policy: user quota status (read-only)
- Audit: admin-only event queries

**Internal-Only (No Public Access):**
- AI Gateway (inference, model validation, cost estimation, conditioning purge)
- Inference Worker (async only)
- Internal service callbacks (status updates, work retrieval)
- Quota reservation/commit/release APIs
- Audit ingestion (event-driven only)

---

## Canonical State Machines

### Voice Profile (AC-ENR-001, FR-011)
```
PENDING → QUALITY_CHECKING
  ├→ AWAITING_USER_OVERRIDE (overrideable warning)
  │   └→ ENROLLING (user override)
  ├→ FAILED (hard quality failure)
  └→ ENROLLING (quality pass)
       ├→ ENROLLED (success; includes model_version)
       └→ FAILED (enrollment error)

Any state → REVOKED (user delete or consent revoke)
```

### Narration Job (FR-022, AC-GEN-001)
```
QUEUED → PREPARING → RUNNING → POST_PROCESSING → COMPLETED
  ↓         ↓          ↓            ↓
  └─ FAILED (any non-terminal state)
  └─ CANCELLED (any non-terminal state)
```

---

## Work Commands vs Domain Events

**Work Commands** (requests to async workers):
- `voice_profile.enroll` — Enrollment request to Inference Worker
- `narration.generate` — Narration request to Inference Worker

**Domain Events** (for audit and eventual consistency):
- `voice_profile.enrolled`, `voice_profile.enrollment_failed`, `voice_profile.quality_warning`, `voice_profile.revoked`
- `narration_job.submitted`, `narration_job.started`, `narration_job.completed`, `narration_job.failed`, `narration_job.cancelled`
- `consent.recorded`, `consent.revoked`
- `user.verified`, `user.deleted`
- `artifact.stored`, `artifact.accessed`, `artifact.deleted`
- `quota.exceeded`, `budget.exceeded`, `usage.recorded`

---

## Key Architectural Guarantees

### Safe Job Completion (FR-045)
1. Inference Worker reports completion with cost
2. Narration Orchestrator calls Usage & Policy: POST /quotas/commit-usage (idempotent by reservation_id)
3. Commit succeeds or returns already-committed success
4. Only then does Orchestrator transition job to COMPLETED and publish narration_job.completed
5. Event is for audit only; does NOT trigger usage recording

### Profile Revocation Cascade (AC-RET-001, R-DEL-001)
1. Voice Profile Service: profile → REVOKED; publish voice_profile.revoked with sample_artifact_ids
2. Parallel idempotent consumers:
   - **Orchestrator:** cancel active jobs, release reservations, batch-delete generated-audio
   - **Artifact Service:** delete samples and generated-audio (overrides retention)
   - **AI Gateway:** purge speaker conditioning, embeddings
   - **Audit Service:** record cascade

### Model/Version Immutability (FR-023, AC-HIST-001)
- Voice Profile stores approved_model_version used for enrollment
- Narration Job stores model_version used at submission time
- Job snapshot is self-describing; no need to look up current model later
- Historical reproducibility preserved

---

## Retention Policies

All retention values are **requirement-driven** only:

**Explicitly Requirement-Derived:**
- Generated audio: 30 days (default; overrideable by retention policy)
- Max output duration: 3000 seconds
- AC-RET bounded deletion window: 24 hours (revocation overrides all retention)
- $20/month operational target (cost constraint)

**All Other Retention:**
- Configured per approved retention policy
- No invented "7 years (regulatory)" or "1 year (compliance)" without explicit requirement
- Revocation purges artifacts immediately, regardless of stated retention

---

## Service-to-Service Synchronous Calls

| Caller | Callee | Purpose |
|--------|--------|---------|
| Narration Orchestrator | Voice Profile Service | Validate profile exists, ownership, enrollment status |
| Narration Orchestrator | AI Gateway | Get cost estimate for model before quota reservation |
| Narration Orchestrator | Usage & Policy Service | Reserve quota (atomic), commit usage (idempotent) |
| Narration Orchestrator | Artifact Service | Batch-delete generated-audio on profile revocation |
| Inference Worker | Voice Profile Service | Validate profile, update enrollment status/quality findings |
| Inference Worker | AI Gateway | Perform inference with speaker conditioning |
| Inference Worker | Narration Orchestrator | Retrieve work details, report status/completion/failure |
| Inference Worker | Artifact Service | Store generated audio |
| Voice Profile Service | Consent Service | Validate consent is active |

---

## Cross-File Consistency Verified

✅ Job state names: **QUEUED, PREPARING, RUNNING, POST_PROCESSING, COMPLETED, FAILED, CANCELLED** (consistent across all 5 files)

✅ Voice Profile state names: **PENDING, QUALITY_CHECKING, AWAITING_USER_OVERRIDE, ENROLLING, ENROLLED, FAILED, REVOKED** (consistent across all 5 files)

✅ Work commands: **voice_profile.enroll, narration.generate** (consistent; no stale naming)

✅ Domain events: All 16+ events named consistently across System-Architecture, Service-Boundaries, Data-Ownership, Interaction-Flows, Event-Catalog

✅ API routes: Public routes in System-Architecture match service descriptions in Service-Boundaries; internal-only consistency verified

✅ Retention: No unsupported fixed retention values remain (except requirement-derived)

✅ Cascades: voice_profile.revoked cascade consistent across Data-Ownership, Interaction-Flows, Event-Catalog

✅ Idempotency: Usage commit, job completion, cascades all marked idempotent

✅ Event ordering: Examples updated to reflect canonical commands/events (removed enrollment_requested, narration_job.submitted as command)

---

## Requirements Alignment Summary

| Requirement | Status | Evidence |
|-------------|--------|----------|
| FR-022 (job states) | ✅ | Canonical states: QUEUED→PREPARING→RUNNING→POST_PROCESSING→COMPLETED |
| FR-023 (job snapshot) | ✅ | model_version, profile_id, script_snapshot, output, timestamps stored |
| FR-011 (quality checks) | ✅ | Actionable findings; clipping, SNR, silence, speech presence |
| FR-012 (model metadata) | ✅ | model_version in voice_profile.enrolled and job snapshot |
| AC-ENR-001 (quality pass/override) | ✅ | QUALITY_CHECKING + AWAITING_USER_OVERRIDE states; user-facing PATCH API |
| AC-RET-001 (revocation purge) | ✅ | Generated-audio and samples purged within 24h window |
| FR-045 (idempotent completion) | ✅ | Synchronous, idempotent usage commit before job COMPLETED |
| R-DEL-001 (generated-audio cascade) | ✅ | Orchestrator identifies jobs, batch-deletes artifacts |

---

## Blocking Issues

**NONE.** All stale terminology removed. All 5 files internally consistent. All routes clarified. All retention values requirement-driven.

---

## Architecture Status

**✅ Architecture ready for human approval**

All 14 consistency and requirement-alignment corrections applied:

1. ✅ API Gateway route inventory added and clarified
2. ✅ Consent revocation moved to user-facing API
3. ✅ Quality-override moved to user-facing API
4. ✅ Voice Profile schema updated with quality findings and model/version
5. ✅ Narration Job schema updated with FR-023 fields
6. ✅ Duplicate job state transitions removed
7. ✅ Service Boundary matrix cleaned (stale rows removed)
8. ✅ Service-to-Service matrix fixed (Auth dependency, cost-estimation, artifact-deletion calls)
9. ✅ Data-Ownership lifecycle updated to FR-022 states
10. ✅ Interaction-Flows stale terminology removed
11. ✅ Event-Catalog ordering examples updated
12. ✅ All unsupported fixed retention values replaced
13. ✅ Failure-safe completion ordering preserved
14. ✅ Revocation cleanup ownership preserved

---
