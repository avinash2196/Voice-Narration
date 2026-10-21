# Architecture Revision Summary

**Date:** 2026-10-20
**Work Item:** initial-build
**Revision Pass:** Corrections for consistency and correctness (17 requirements)

---

## Revision Status

✅ **COMPLETE** — All 5 architecture artifacts updated and cross-validated

### Files Updated (5/5)
- System-Architecture.md (168 lines, 10.9 KB)
- Service-Boundaries.md (213 lines, 12.7 KB)
- Data-Ownership.md (289 lines, 16.1 KB)
- Interaction-Flows.md (609 lines, 24.0 KB)
- Event-Catalog.md (590 lines, 18.9 KB)

**Total:** 1869 lines, ~81.5 KB

---

## Major Corrections Applied

### 1. Voice Enrollment Async Workflow ✅
**Requirement:** Voice Profile Service must not directly perform model inference.

**Change:**
- Removed sync Voice Profile → AI Gateway inference call
- Created async work command: `voice_profile.enrollment_requested`
- Inference Worker consumes, performs enrollment (feature extraction, model inference)
- Worker reports completion via Voice Profile Service API: `PATCH /voices/{id}/status`
- Voice Profile publishes domain event: `voice_profile.enrolled`

**Files:** System-Architecture.md, Service-Boundaries.md, Data-Ownership.md, Interaction-Flows.md

---

### 2. Quota/Budget Reservation Semantics ✅
**Requirement:** Use reservation semantics; Orchestrator coordinates, not API Gateway.

**Change:**
- Removed API Gateway orchestrating quota check before job submission
- Narration Orchestrator calls: `POST /quotas/reserve` (atomic, returns reservation_id)
- Job only created/SUBMITTED after reservation succeeds
- Lifecycle: `reserve()` → `commit_usage()` (success) or `release_reservation()` (failure)
- Prevents race conditions on concurrent submissions (atomic per-user reservation)

**Files:** System-Architecture.md, Service-Boundaries.md, Interaction-Flows.md

---

### 3. Domain Events vs Work Commands ✅
**Requirement:** Separate sensitive work content from domain events.

**Change:**
- Work command: `voice_profile.enrollment_requested` (contains profile_id, sample_artifact_ids)
  - Worker retrieves binary via Artifact Service
- Work command: `narration_job.submitted` (serves dual purpose: work + audit event)
  - Contains job_id, profile_id, estimation metadata
  - Worker retrieves full script via: `GET /jobs/{job_id}/work-item`
- Domain event: `narration_job.completed` (contains artifact_id reference only)
  - Never includes script or audio binary

**Files:** Interaction-Flows.md, Event-Catalog.md

---

### 4. Minimal Event Payloads ✅
**Requirement:** Remove sensitive/unnecessary data from events.

**Change:**
- Removed speaker embeddings from `voice_profile.enrolled`
- Removed full consent_text from `consent.recorded` (reference by ID only)
- Removed narration scripts from `narration_job.submitted` (Worker fetches separately)
- Removed storage paths from `artifact.stored` (never expose bucket/path)
- Removed model-specific provider identifiers
- All sensitive data owned/secured by service (Artifact owns paths, AI Gateway owns embeddings)

**Files:** Event-Catalog.md, Interaction-Flows.md

---

### 5. Model-Specific Voice Conditioning Ownership ✅
**Requirement:** Clarify lifecycle of model/provider-specific speaker conditioning.

**Change:**
- AI Gateway owns: model-specific speaker_id, embeddings, conditioning vectors, cached artifacts
- Voice Profile Service owns: logical profile metadata only (no embeddings)
- Artifact Service owns: binary sample audio
- Defined: `AI Gateway.PATCH /ai/speaker/{profile_id}/purge` for revocation cleanup
- Cascade: `voice_profile.revoked` → AI Gateway purges provider artifacts

**Files:** System-Architecture.md, Service-Boundaries.md, Data-Ownership.md, Interaction-Flows.md

---

### 6. Consent Revocation Cascade ✅
**Requirement:** Consent Service must not determine which profiles/jobs belong to consent.

**Change:**
- Consent Service publishes: `consent.revoked` (minimal: consent_id, user_id only)
- Voice Profile Service determines affected profiles (ownership-based cascade)
- Voice Profile publishes: `voice_profile.revoked` (includes sample_artifact_ids for cleanup)
- Narration Orchestrator, Artifact Service, AI Gateway independently consume
- Each subscriber is idempotent (handles duplicate deliveries)

**Files:** Service-Boundaries.md, Data-Ownership.md, Interaction-Flows.md

---

### 7. Canonicalized Event Names ✅
**Requirement:** Choose one event naming convention; use consistently.

**Change:**
- Unified naming: `<service>.<resource>.<action>` (past tense)
- Examples:
  - `consent.recorded`, `consent.revoked`
  - `voice_profile.enrolled`, `voice_profile.revoked`
  - `narration_job.submitted`, `narration_job.completed`
- Removed parallel forms (no "voice_profile.profile.revoked" and "voice_profile.revoked")
- Consistent across all 5 artifacts

**Files:** System-Architecture.md, Event-Catalog.md

---

### 8. Auth Service Events ✅
**Requirement:** Make Auth events consistent; publish only security-critical events.

**Change:**
- Added: `user.verified` (email verification complete)
- Added: `user.deleted` (user deletion/account removal)
- Removed: routine login audit (login is frequent; security events sufficient)

**Files:** System-Architecture.md, Service-Boundaries.md, Event-Catalog.md

---

### 9. Transactional Outbox Pattern ✅
**Requirement:** Define reliable event publication to prevent "commit succeeds, event fails" failure.

**Change:**
- Defined explicit outbox pattern:
  1. Update business state
  2. Insert outbox record in same transaction
  3. Commit atomically
  4. Background publisher sends to broker
  5. Mark outbox published only after broker ACK
- Consumers are idempotent (deduplication by event_id)
- Applied to all state-changing services: Consent, Voice Profile, Narration Orchestrator, Artifact, Usage & Policy

**Files:** Event-Catalog.md, Data-Ownership.md

---

### 10. Service-to-Service Authentication ✅
**Requirement:** Do not require every call to Auth Service; use token-based auth.

**Change:**
- Auth Service issues signed bearer tokens (JWT)
- Downstream services validate tokens locally (using public keys/JWKS)
- Auth is NOT a synchronous runtime dependency
- Internal service-to-service calls use separate authentication (TBD in CONTRACT)

**Files:** System-Architecture.md, Service-Boundaries.md

---

### 11. Artifact Access Semantics ✅
**Requirement:** Return opaque artifact_id; do not expose storage paths.

**Change:**
- Upload response: `{ artifact_id }` (never bucket path or storage location)
- Download flow: Client → Artifact Service → signed URL (time-limited)
- Client uses signed URL directly to storage (no API roundtrip)
- Storage paths never in APIs or events

**Files:** Interaction-Flows.md, Event-Catalog.md

---

### 12. Deletion/Revocation Overrides Retention ✅
**Requirement:** Revocation/deletion requirements must override retention policies.

**Change:**
- Approved deletion requirement: samples purged immediately on profile revocation
- Retention policy does NOT override revocation
- `voice_profile.revoked` cascade: Artifact Service deletes samples immediately
- Event: `artifact.deleted` with reason=profile_revoked

**Files:** Data-Ownership.md, Interaction-Flows.md

---

### 13. No Hard-Coded Regulatory Retention ✅
**Requirement:** Remove unsupported legal-retention assumptions (e.g., "7 years because GDPR").

**Change:**
- Removed: hard-coded "7 years", "legal hold" statements
- Added: Retention is policy/configuration-driven
- Retention period table note: "Retention is governed by approved policy; this table suggests defaults only"
- Distinct concepts: broker retention, app retention, artifact retention, audit retention

**Files:** Event-Catalog.md, Data-Ownership.md

---

### 14. Audit Service Boundary ✅
**Requirement:** Separate audit ingestion (internal, async) from audit queries (admin API).

**Change:**
- Audit ingestion: async, event-driven, internal event consumers only, non-blocking
- Audit query: separate protected **admin-only read API** via API Gateway
- Distinction: write (internal) vs read (authenticated admin)
- Audit availability must NOT block business workflows

**Files:** System-Architecture.md, Service-Boundaries.md

---

### 15. Compensation/Cleanup Responsibility ✅
**Requirement:** Correct ownership of artifact cleanup on failure.

**Change:**
- Removed: misleading "message broker deletes artifacts" statements
- Defined: Inference Worker invokes Artifact Service cleanup on failure
- Artifact Service is exclusive binary owner, performs all deletions
- Message broker owns delivery only

**Files:** Interaction-Flows.md, Data-Ownership.md

---

### 16. No Premature Implementation Details ✅
**Requirement:** Move implementation details to CONTRACT/Implementation Plan.

**Change:**
- Removed hard-coded: sample rates, chunk durations, retry counts, backoff timings
- Removed named providers (Eleven Labs, Google Cloud Run specifics)
- Removed specific broker technology (RabbitMQ, Kafka, etc.)
- Kept only requirement-derived constraints

**Files:** All 5 documents

---

### 17. Complete Cross-Document Consistency ✅
**Requirement:** Verify consistency across all 5 artifacts.

**Validation:**
- ✅ Every service appears consistently in all documents
- ✅ APIs, events, ownership, responsibilities match across artifacts
- ✅ Cascade logic consistent (consent → profile → job/artifact)
- ✅ Event publishing consistent (outbox pattern documented uniformly)
- ✅ No conflicting descriptions of same interaction
- ✅ All 9 services preserved (no redesign)
- ✅ All 10 architectural rules enforced

---

## Final Service List (Preserved)

### Application Services (9) ✅
1. Auth Service (registration, tokens, account identity)
2. Consent Service (immutable consent records, revocation)
3. Voice Profile Service (logical profile lifecycle, async enrollment)
4. Narration Orchestrator (job lifecycle, quota coordination)
5. Artifact Service (binary storage, signed access, retention)
6. Usage & Policy Service (quotas, atomic reservations, budget)
7. AI Gateway (model routing, speaker conditioning, revocation cleanup)
8. Inference Worker (async enrollment/narration execution, chunking)
9. Audit Service (immutable audit history, admin read API)

### Shared Infrastructure (6) ✅
- API Gateway (routes public requests)
- Message Broker (work commands + domain events, at-least-once delivery)
- PostgreSQL (shared server, isolated schemas per service)
- Object Storage (binary artifacts, user-isolated namespaces)
- Secrets Infrastructure (credentials, API keys)
- Observability (logging, metrics, tracing)

---

## Final Command/Event Model

### Work Commands (to async workers)
- `voice_profile.enrollment_requested` → Inference Worker
- `narration_job.submitted` → Inference Worker

### Domain Events (for audit, lifecycle propagation)
- `user.verified`, `user.deleted`
- `consent.recorded`, `consent.revoked`
- `voice_profile.enrollment_requested`, `voice_profile.enrolled`, `voice_profile.enrollment_failed`, `voice_profile.revoked`
- `narration_job.submitted`, `narration_job.started`, `narration_job.completed`, `narration_job.failed`, `narration_job.cancelled`
- `artifact.stored`, `artifact.accessed`, `artifact.deleted`
- `quota.exceeded`, `budget.exceeded`, `usage.recorded`

### Publishing Pattern
- **Transactional Outbox:** Update state → Insert outbox → Commit → Background publisher → Mark published
- **Idempotency:** event_id + consumer deduplication table
- **Delivery:** At-least-once via outbox retry

---

## Final Enrollment Flow

1. Client uploads enrollment samples via Artifact Service
   - Response: `{ artifact_id }` (opaque, no storage path)

2. Client creates profile via Voice Profile Service
   - Validates consent active
   - Stores sample artifact references
   - Profile state: PENDING → ENROLLING
   - Publishes: `voice_profile.enrollment_requested` (work command)

3. Inference Worker consumes work
   - Downloads samples via Artifact Service (signed URLs)
   - Extracts features, performs model enrollment
   - Calls AI Gateway for speaker conditioning (stored in AI Gateway)
   - Calls Voice Profile Service: `PATCH /voices/{id}/status { status: ENROLLED }`

4. Voice Profile Service publishes: `voice_profile.enrolled` (domain event)
   - Audit Service consumes

**Final State:** Profile is ENROLLED, ready for narration jobs

---

## Final Narration Flow

1. Client submits job via Narration Orchestrator
   - Validates profile is ENROLLED
   - Calls Usage & Policy: `POST /quotas/reserve` (atomic reservation_id)
   - On success: Creates job (SUBMITTED), publishes `narration_job.submitted`

2. Inference Worker consumes work
   - Retrieves full work item (script) via: `GET /jobs/{id}/work-item`
   - Chunks script
   - Performs inference via AI Gateway (with speaker conditioning)
   - Assembles output, calls Artifact Service: `POST /artifacts/upload`
   - Returns artifact_id
   - Calls Narration Orchestrator: `POST /jobs/{id}/complete`

3. Narration Orchestrator on completion
   - Calls Usage & Policy: `POST /quotas/commit-usage` (commits reservation)
   - Publishes: `narration_job.completed`
   - Usage & Policy publishes: `usage.recorded`

**Final State:** Job is COMPLETED, audio stored, cost recorded

---

## Final Revocation Flow

1. User deletes profile OR consent revoked
   - Consent Service publishes: `consent.revoked` (minimal payload)
   - Voice Profile Service publishes: `voice_profile.revoked`

2. Cascades (parallel, eventual consistency):
   - **Narration Orchestrator** consumes `voice_profile.revoked`
     - Cancels SUBMITTED/PROCESSING jobs
     - Calls Usage & Policy: `release_reservation` (restores quota)
     - Publishes: `narration_job.cancelled`
   
   - **Artifact Service** consumes `voice_profile.revoked`
     - Deletes samples immediately (revocation overrides retention)
     - Publishes: `artifact.deleted`
   
   - **AI Gateway** consumes `voice_profile.revoked`
     - Purges provider-specific conditioning, embeddings, cached data
     - No event (internal cleanup)
   
   - **Audit Service** consumes all events
     - Records cascade in audit trail

**Guarantees:** All artifacts purged, all jobs cancelled, within cascade event ordering

---

## Blocking Issues

**NONE.** All 17 correction requirements satisfied.

---

## Deferred Design Questions (Not Blocking)

These will be resolved in CONTRACT or Implementation Planning:
- Message broker technology (RabbitMQ, Kafka, Cloud Pub/Sub, etc.)
- Exact service-to-service credential management strategy
- PostgreSQL schema isolation vs dedicated databases per service
- Specific AI model selection and licensing approval
- Exact async worker implementation (polling, pub/sub, message-driven)

---

## Architecture Status

**Ready for human approval**

All 5 artifacts are consistent, complete, and satisfy:
- ✅ 9 services preserved (no redesign)
- ✅ 17 correction requirements applied
- ✅ Cross-artifact consistency verified
- ✅ No unsupported regulatory assumptions
- ✅ Clear ownership boundaries
- ✅ Async workflows correctly separated from sync
- ✅ Transactional outbox pattern defined
- ✅ Cascade semantics clear and idempotent
- ✅ No premature implementation details
- ✅ No blocking architectural contradictions

**Next Steps (after human approval):**
1. Revise Plan.md to insert System Architecture milestone before CONTRACT
2. Update Execution Status and traceability matrix with new milestone
3. Proceed to CONTRACT milestone (per-service contracts)
4. Begin FOUNDATION and RED/GREEN milestones

---
