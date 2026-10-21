# Architecture Revision Summary — Final Requirement-Alignment Pass

**Date:** 2026-10-20
**Work Item:** initial-build
**Revision Pass:** Requirement-Alignment and FR-022/FR-023/AC-ENR-001/AC-RET-001 Integration

---

## Revision Status

✅ **COMPLETE** — All 5 architecture artifacts updated for full requirement alignment

### Files Updated (5/5)
- System-Architecture.md (250+ lines)
- Service-Boundaries.md (280+ lines)
- Data-Ownership.md (330+ lines)
- Interaction-Flows.md (800+ lines)
- Event-Catalog.md (650+ lines)

---

## Major Corrections Applied (14 Domains)

### 1. FR-022 Job State Machine (CRITICAL)
**Requirement:** Approved states: queued → preparing → running → post-processing → completed (+ failed, cancelled)

**Change:**
- Replaced SUBMITTED/PROCESSING with canonical FR-022 states
- Added explicit state transitions: QUEUED → PREPARING → RUNNING → POST_PROCESSING → COMPLETED
- Added FAILED and CANCELLED as terminal states
- Updated all 5 artifacts with consistent state names
- narration.generate work command published when job enters QUEUED
- narration_job.started event published on QUEUED → PREPARING transition

**Files:** System-Architecture.md, Service-Boundaries.md, Data-Ownership.md, Interaction-Flows.md, Event-Catalog.md

**Impact:** Job status responses now reflect FR-022 exactly

---

### 2. FR-011 + AC-ENR-001 Quality-Check and User-Override Workflow
**Requirement:** Enrollment quality checks with actionable feedback; user explicit override for warnings

**Change:**
- Added explicit QUALITY_CHECKING state to Voice Profile lifecycle
- Added AWAITING_USER_OVERRIDE state for overrideable warnings
- Inference Worker performs quality analysis (clipping, silence, SNR, speech presence)
- Quality findings persisted in Voice Profile (not ephemeral)
- Added voice_profile.quality_warning domain event for user notification
- Added PATCH /voices/{id}/quality-override API for user decision
- Quality findings include actionable feedback (e.g., "mild clipping (2-3 peaks)")
- User choice: re-record OR acknowledge and proceed

**Files:** System-Architecture.md, Service-Boundaries.md, Data-Ownership.md, Interaction-Flows.md

**Impact:** Enrollment now supports AC-ENR-001 quality-override workflow

---

### 3. FR-012 + AC-HIST-001 Model/Version Metadata in Profiles
**Requirement:** Voice profile metadata includes model/version

**Change:**
- Voice Profile Service now stores approved model/version reference in profile metadata
- voice_profile.enrolled event includes model_version
- Narration Orchestrator job snapshot includes model_version (see #4)
- AI Gateway coordinates model selection during enrollment
- Model version used for each enrollment is auditable

**Files:** System-Architecture.md, Service-Boundaries.md, Data-Ownership.md, Event-Catalog.md

**Impact:** Complete job history remains self-describing with model versions

---

### 4. FR-023 + AC-HIST-001 Job Snapshot with Model Version
**Requirement:** Job metadata includes profile, model version, params, script snapshot, output, timestamps

**Change:**
- narration_job.submitted event now includes model_version
- narration_job.completed event now includes model_version
- Narration Orchestrator stores complete job snapshot:
  - profile_id, model_version, generation_params, language
  - script_snapshot, output_artifact_id
  - estimated cost, actual cost, timestamps
- Job snapshot is self-describing (no need to look up current profile state later)

**Files:** Service-Boundaries.md, Data-Ownership.md, Interaction-Flows.md, Event-Catalog.md

**Impact:** Complete job history with model versions enables historical reproducibility

---

### 5. AC-RET-001 + R-DEL-001 Profile Revocation Purges Generated Audio
**Requirement:** Revocation removes original samples, embeddings, AND generated audio within bounded window

**Change:**
- voice_profile.revoked cascade extended to purge generated audio
- Narration Orchestrator identifies all COMPLETED jobs using revoked profile
- Orchestrator extracts output_artifact_ids and requests batch deletion from Artifact Service
- Artifact Service deletes generated audio immediately (overrides retention)
- Artifact Service publishes artifact.deleted for each removed artifact
- Revocation overrides all retention policies

**Files:** System-Architecture.md, Data-Ownership.md, Interaction-Flows.md

**Impact:** Profile revocation is now complete deletion per AC-RET-001

---

### 6. Enrollment Quality-Check and Model-Version Lifecycle
**Coordination (FR-011, FR-012, AC-ENR-001):**

**Sequence:**
1. User uploads samples → Voice Profile created in PENDING state
2. Voice Profile transitions to QUALITY_CHECKING
3. Inference Worker analyzes quality
4. If hard failure → voice_profile.enrollment_failed, profile transitions to FAILED
5. If warning → voice_profile.quality_warning, profile transitions to AWAITING_USER_OVERRIDE
6. User acknowledges warning → profile transitions to ENROLLING
7. Inference Worker performs enrollment with selected model
8. Model version stored in profile metadata
9. voice_profile.enrolled published with model_version
10. Profile transitions to ENROLLED

**Files:** All 5 documents

---

### 7. Cost-Estimation Ownership Clarification
**Requirement:** AI Gateway owns provider-specific cost estimation; Orchestrator owns workflow

**Change:**
- AI Gateway provides internal API: GET /ai/models/{model_id}/cost-estimate
- Narration Orchestrator calls this API to obtain estimate
- Orchestrator includes estimate in Usage & Policy /quotas/reserve call
- Usage & Policy validates and enforces budget based on estimate + actual
- No cost-estimation logic duplicated in Orchestrator

**Files:** System-Architecture.md, Interaction-Flows.md

---

### 8. Safe Completion and Usage Commitment Ordering
**Requirement:** Usage must commit before job transitions to COMPLETED (FR-045)

**Change:**
- Strict sequence enforced:
  1. Inference Worker reports successful inference to Orchestrator
  2. Orchestrator calls Usage & Policy: POST /quotas/commit-usage (IDEMPOTENT)
  3. Only after commit succeeds does Orchestrator update job to COMPLETED
  4. Orchestrator publishes narration_job.completed (audit only)
- narration_job.completed is NOT a usage-commit trigger
- Usage & Policy does NOT consume this event for accounting

**Files:** Interaction-Flows.md, Event-Catalog.md, Data-Ownership.md

**Impact:** No distributed transaction; idempotent commit; crash-safe

---

### 9. Work Command/Event Terminology Cleanup
**Requirement:** Replace ambiguous names with clear distinctions

**Change:**
- voice_profile.enroll (WORK COMMAND to Inference Worker)
- voice_profile.enrolled, voice_profile.enrollment_failed, voice_profile.quality_warning (DOMAIN EVENTS)
- narration.generate (WORK COMMAND to Inference Worker)
- narration_job.submitted, narration_job.started, narration_job.completed, narration_job.failed, narration_job.cancelled (DOMAIN EVENTS)
- All references to enrollment_requested and dual-purpose job.submitted removed

**Files:** Interaction-Flows.md (intro), Event-Catalog.md, Service-Boundaries.md, System-Architecture.md

---

### 10. Removed Stale Usage & Policy Event Consumption
**Requirement:** Usage committed via synchronous API, not event

**Change:**
- Removed narration_job.completed from Usage & Policy subscriptions
- Usage & Policy only subscribes to user.deleted for cascade
- Usage commitment is synchronous: Orchestrator → POST /quotas/commit-usage

**Files:** System-Architecture.md, Event-Catalog.md

---

### 11. API Gateway Route Inventory Clarification
**Requirement:** Make external vs internal access explicit

**Change:**
- Public routes (via API Gateway):
  - Auth Service endpoints
  - Consent Service read/write
  - Voice Profile Service (profiles, status)
  - Narration Orchestrator (jobs)
  - Artifact Service (download/preview)
  - Usage & Policy (user/admin reads)
  - Audit Service (admin-only reads)
  
- Internal-only (no public access):
  - AI Gateway (model routing, conditioning)
  - Inference Worker (async worker)
  - Audit ingestion (event-driven)
  - Policy mutation APIs

**Files:** System-Architecture.md

---

### 12. Auth Dependency Statements Fixed
**Requirement:** Auth Service is not synchronous dependency per-request

**Change:**
- Removed "All services → Auth Service → on every request" statement
- Clarified: Auth Service issues tokens; services validate locally
- Service-to-service authentication deferred to CONTRACT
- No architectural dependency on Auth Service for runtime token validation

**Files:** System-Architecture.md, Architectural Rules table

---

### 13. Generated-Audio Batch-Deletion API
**Requirement:** AC-RET-001 requires deletion of generated audio on profile revocation

**Change:**
- Added internal API to Artifact Service: POST /artifacts/batch-delete
- Narration Orchestrator calls this with artifact_id list
- Artifact Service immediately purges (overrides retention)
- No sequential requirement; Orchestrator and Artifact Service coordinate independently

**Files:** System-Architecture.md, Service-Boundaries.md

---

### 14. Retention Policy Statements Aligned to Requirements
**Requirement:** Remove invented regulatory periods; align to requirement-driven defaults

**Change:**
- All events use "Retention: Per approved retention policy" OR requirement-specific value
- Approved defaults: Generated audio 30 days, profiles/consent per admin policy
- No invented "7 years (regulatory)" statements
- Revocation overrides retention immediately

**Files:** Event-Catalog.md

---

## Requirements Cross-Check

All 19 targeted requirements verified:

| Requirement | Addressed | Evidence |
|-------------|-----------|----------|
| FR-010 | ✅ | Audio format validation documented in artifact upload flows |
| FR-011 | ✅ | Quality checks with actionable feedback (clipping, SNR, etc.) in Flow 3 |
| FR-012 | ✅ | Model/version in voice_profile metadata; voice_profile.enrolled includes it |
| FR-022 | ✅ | Job states: QUEUED→PREPARING→RUNNING→POST_PROCESSING→COMPLETED per spec |
| FR-023 | ✅ | Job snapshot includes profile_id, model_version, params, output, timestamps |
| FR-024 | ✅ | Download/preview with signed URLs in Flow 6 |
| FR-025 | ✅ | Linguistic chunking at pause/line boundaries in Flow 5 |
| FR-041 | ✅ | AI Gateway as model abstraction interface |
| FR-044 | ✅ | Quota/budget enforcement documented in flow 4 |
| FR-045 | ✅ | Idempotency and durable job state; commit-usage before COMPLETED |
| R-REV-001 | ✅ | Revocation cascade purges samples, embeddings, generated audio |
| R-RET-001 | ✅ | Separate retention policies framework documented |
| R-RET-002 | ✅ | Default 30-day generated-audio retention maintained |
| R-DEL-001 | ✅ | Generated audio purged within bounded deletion window on revocation |
| AC-ENR-001 | ✅ | Quality checks pass + user override workflow explicit |
| AC-GEN-001 | ✅ | QUEUED→COMPLETED state progression; idempotent submission |
| AC-HIST-001 | ✅ | Model version in job snapshot; immutable audit history |
| AC-RET-001 | ✅ | Generated audio and samples purged on revocation within 24h window |
| AC-QUOTA-001 | ✅ | Quota/budget reservation pattern; kill-switch enforcement |

---

## Final Service List (Preserved: 9 Services)

1. Auth Service
2. Consent Service
3. Voice Profile Service (enhanced: quality-checking, model/version metadata)
4. Narration Orchestrator (enhanced: FR-022 states, safe usage commit, generated-audio cascade)
5. Artifact Service (enhanced: batch-delete, revocation override)
6. Usage & Policy Service (no event consumption of job completion)
7. AI Gateway (cost-estimation API)
8. Inference Worker (no lifecycle-event publication)
9. Audit Service

---

## Final State Machines

### Voice Profile Lifecycle (AC-ENR-001)
```
PENDING
  ↓
QUALITY_CHECKING
  ├→ AWAITING_USER_OVERRIDE (if warning) → ENROLLING (user override)
  ├→ FAILED (hard quality failure)
  └→ ENROLLING (quality pass)
       ├→ ENROLLED (enrollment success with model_version)
       └→ FAILED (enrollment failure)

Any state → REVOKED (user delete or consent revoked)
```

### Narration Job Lifecycle (FR-022)
```
QUEUED
  ↓
PREPARING
  ↓
RUNNING
  ↓
POST_PROCESSING
  ↓
COMPLETED (after usage committed)

Any of above → FAILED (inference/profile/cost failure)
Any of above → CANCELLED (user cancel or profile revoked)
```

---

## Final Work Commands

1. **voice_profile.enroll** – Enrollment request to Inference Worker
2. **narration.generate** – Narration request to Inference Worker

---

## Final Domain-Event Families

**Authentication:** user.verified, user.deleted
**Consent:** consent.recorded, consent.revoked
**Voice Profile:** voice_profile.enroll (also work command), voice_profile.enrolled, voice_profile.enrollment_failed, voice_profile.quality_warning, voice_profile.revoked
**Narration Job:** narration_job.submitted, narration_job.started, narration_job.completed, narration_job.failed, narration_job.cancelled
**Artifact:** artifact.stored, artifact.accessed, artifact.deleted
**Usage & Policy:** quota.exceeded, budget.exceeded, usage.recorded

---

## Key Sequence: Job Completion Accounting (FR-045)

1. Inference Worker → Orchestrator: POST /jobs/{job_id}/complete { output_artifact_id, actual_cost }
2. Narration Orchestrator → Usage & Policy: POST /quotas/commit-usage (IDEMPOTENT using reservation_id)
3. Usage & Policy returns success or idempotent-already-committed
4. Orchestrator: Update job status COMPLETED, insert outbox record
5. Background publisher: Publish narration_job.completed (audit only)

**Guarantee:** No job reaches COMPLETED until usage is committed.

---

## Key Sequence: Profile Revocation Cascade (AC-RET-001, R-DEL-001)

1. User: DELETE /voices/{profile_id}
2. Voice Profile Service: Transition to REVOKED, publish voice_profile.revoked
3. Parallel consumers (eventual consistency, idempotent):
   - **Orchestrator:** Cancel jobs, identify output_artifact_ids, batch-delete
   - **Artifact Service:** Delete samples immediately, await batch-delete for generated-audio
   - **AI Gateway:** Purge speaker_conditioning, embeddings, cached artifacts
   - **Audit Service:** Record cascade

**Guarantee:** All artifacts purged within bounded window (default 24h), revocation overrides retention.

---

## Blocking Issues

**NONE.** All 14 requirement-alignment corrections applied. All 19 requirements verified.

---

## Architecture Status

**✅ Architecture ready for human approval**

All five authoritative architecture artifacts now:
- ✅ Conform exactly to FR-022 (job states)
- ✅ Implement AC-ENR-001 (quality-check + override workflow)
- ✅ Include FR-012 + AC-HIST-001 (model/version snapshots)
- ✅ Satisfy FR-023 (complete job metadata)
- ✅ Support AC-RET-001 (generated-audio purging on revocation)
- ✅ Enforce FR-045 (safe, idempotent, durable completion)
- ✅ Maintain all 9 services with consistent ownership
- ✅ Clarify work commands vs domain events
- ✅ Define clear cascades with idempotency
- ✅ Remove stale regulatory assumptions
- ✅ Cross-validate all 5 documents for internal consistency

**Next Steps (after human explicit approval):**
1. Revise Plan.md to insert System Architecture milestone before CONTRACT
2. Update Execution Status and traceability matrix
3. Proceed to CONTRACT milestone (per-service contracts)
4. Begin FOUNDATION and RED/GREEN milestones

---
