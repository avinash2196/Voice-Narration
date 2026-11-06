# System Architecture — initial-build

## Overview

### Deployment-shape decision — 2026-10-24

The user selected option 2: retain the nine separate services described below, rather than consolidating them into a modular API plus worker. This explicit decision resolves the deployment-shape question raised in ../Contract-Review.md and takes precedence over the product baseline's default preference for a modular API. It approves this architecture choice only; the complete architecture and revised API contract still require review. The $20/month operational target, Windows/local development, model/licensing gates, and prohibition on unapproved cloud provisioning remain in effect. Deployment costs and operational feasibility have not been demonstrated.

Voice Narration Studio M0 uses an **event-driven, service-oriented distributed architecture** with explicit service ownership boundaries. Each service owns its data, business logic, and lifecycle. Services communicate via synchronous APIs (when immediate decisions are required) and asynchronous domain events (for eventual consistency and lifecycle propagation).

This architecture supports:
- Clear service boundaries and independent scaling
- Data isolation and ownership
- Testable, independently deployable services
- Event-driven distributed workflows
- Local M0 development (all services co-located)
- Optional Cloud Run L4 GPU deployment (Inference Worker)

## Architectural Principles

1. **Service Ownership:** Each service owns its database schema, business state, and API surface. No service reads/writes another service's database.

2. **Data Sharing:** Services reference other services' data only by ID. To retrieve details, services call the owning service's API.

3. **Synchronous APIs:** Used when immediate decisions are required (authentication, authorization, availability checks).

4. **Asynchronous Events:** Used for lifecycle propagation, eventual consistency, and non-blocking notifications.

5. **No Direct AI/Storage Access:** Public clients and most services access AI capabilities only through the AI Gateway. All binary storage is accessed through the Artifact Service.

6. **Audit is Eventual:** Audit events are published asynchronously; normal workflows must not depend on audit availability.

7. **Secrets Management:** All provider credentials and API keys are managed by backend secrets infrastructure; never exposed to clients.

## Core Services

### 1. Auth Service
**Owns:** User accounts, bearer tokens, account identity and status.

**Does not own:** Consent, voice profiles, jobs, quotas.

**Public API:**
- POST /auth/register
- POST /auth/verify-email
- POST /auth/login
- GET /auth/me

**Internal API:**
- GET /auth/verify-token (validate bearer token, return user_id, role)

### 2. Consent Service
**Owns:** Immutable consent records, consent versions, revocation history, consent validation.

**Does not own:** Voice profiles, audio storage.

**Public API:**
- POST /consent/record
- GET /consent/{consent_id}

**Internal API:**
- GET /consent/validate/{consent_id}
- POST /consent/revoke

**Events:** consent.recorded, consent.revoked

### 3. Voice Profile Service
**Owns:** Logical voice-profile lifecycle and metadata (including model/version reference per FR-012), profile-to-consent and profile-to-artifact references, quality assessment results and user overrides (AC-ENR-001).

**Does not own:** Raw audio storage, artifact binary content, consent records, model-specific embeddings/conditioning.

**Public API:**
- POST /voices (creates profile in PENDING state)
- GET /voices
- DELETE /voices/{profile_id}

**Internal API:**
- GET /voices/validate/{profile_id}
- PATCH /voices/{profile_id}/status (for Inference Worker to report quality assessment, user-override decision, or completion/failure)
- PATCH /voices/{profile_id}/quality-override (for user to acknowledge warning and override enrollment block)

**Profile State Lifecycle (AC-ENR-001):**
`PENDING` → `QUALITY_CHECKING` → (`AWAITING_USER_OVERRIDE` [if overrideable warning] OR `ENROLLING`) → `ENROLLED` / `FAILED` / `REVOKED`

**Events Published:**
- voice_profile.enroll (WORK COMMAND, when profile transitions to QUALITY_CHECKING; triggers Inference Worker for quality assessment)
- voice_profile.enrolled (DOMAIN EVENT, after Worker completes enrollment and profile reaches ENROLLED)
- voice_profile.enrollment_failed (DOMAIN EVENT, if Worker reports hard quality failure)
- voice_profile.quality_warning (DOMAIN EVENT, if Worker reports overrideable quality warning; triggers user UI notification)
- voice_profile.revoked (DOMAIN EVENT, when user deletes or consent revoked)

**Events Consumed:**
- consent.revoked (revokes profiles linked to revoked consent)
- user.deleted (revokes user's profiles)

### 4. Narration Orchestrator Service
**Owns:** Narration job lifecycle, durable state, idempotency, workflow coordination, job history, reservation coordination with Usage & Policy.

**Does not own:** Model inference, artifact storage, profile data, quotas.

**Public API:**
- POST /jobs (submits job, coordinates quota reservation internally, publishes narration_job.submitted only after reservation succeeds)
- GET /jobs/{job_id}
- GET /jobs
- POST /jobs/{job_id}/cancel

**Internal API:**
- GET /jobs/{job_id}/work-item (for Inference Worker to retrieve work details: script, params)
- PATCH /jobs/{job_id}/status (Worker updates status)
- POST /jobs/{job_id}/complete (Worker reports completion; Orchestrator commits usage)
- POST /jobs/{job_id}/fail (Worker reports failure; Orchestrator releases reservation)

**Job State Lifecycle (FR-022):**
Canonical states: `QUEUED` → `PREPARING` → `RUNNING` → `POST_PROCESSING` → `COMPLETED` (terminal)
Terminal states: `FAILED`, `CANCELLED`

**Events Published:**
- narration.generate (WORK COMMAND, when job created in QUEUED state)
- narration_job.submitted (DOMAIN EVENT, when quota reservation succeeds and job enters QUEUED)
- narration_job.started (DOMAIN EVENT, when job transitions from QUEUED to PREPARING/RUNNING)
- narration_job.completed (DOMAIN EVENT, when job reaches COMPLETED state, after usage committed)
- narration_job.failed (DOMAIN EVENT, when job reaches FAILED state, reservation released)
- narration_job.cancelled (DOMAIN EVENT, when job reaches CANCELLED state)

**Events Consumed:**
- voice_profile.revoked (cancels QUEUED/PREPARING/RUNNING jobs using that profile, releases reservations, publishes narration_job.cancelled; coordinates with Artifact Service to purge generated audio artifacts per AC-RET-001)
- user.deleted (cancels user's active jobs, releases reservations)

### 5. Artifact Service
**Owns:** All binary artifacts (samples, generated audio), signed access, retention, deletion.

**Does not own:** Artifact references in other services.

**Public API:**
- POST /artifacts/upload
- GET /artifacts/{artifact_id}/download-url
- GET /artifacts/{artifact_id}/preview-url
- DELETE /artifacts/{artifact_id}

**Internal API:**
- POST /artifacts/batch-delete
- GET /artifacts/{artifact_id}/metadata

**Events:** artifact.stored, artifact.deleted

**Events Consumed:**
- voice_profile.revoked (deletes/purges samples per revocation requirements, overriding retention policy per AC-RET-001)
- user.deleted (purges user's samples, generated audio, and other artifacts per R-DEL-001)

### 6. Usage & Policy Service
**Owns:** Quotas, rate-limit policy, usage accounting, budget enforcement, quota reservations.

**Does not own:** Job data, user identity, audio storage.

**Public API:**
- GET /quotas/me
- GET /admin/quotas/user/{user_id}/status (admin-only, protected by API Gateway)

**Internal API:**
- POST /quotas/reserve (atomic reservation of usage/budget; returns reservation_id)
- POST /quotas/commit-usage (records actual usage after job completion)
- POST /quotas/release-reservation (releases unused quota on failure/cancellation)

**Events Published:**
- quota.exceeded (quota check fails)
- budget.exceeded (budget check fails)
- usage.recorded (after job completion, actual usage committed)

**Events Consumed:**
- user.deleted (cascade: archive user's quota and usage)

### 7. AI Gateway
**Owns:** Approved-model routing, model capability validation, provider credentials, model-specific speaker conditioning, provider-side artifacts, normalized inference interface.

**Does not own:** Job state, audio storage, quotas, user voice profiles (references by profile_id only).

**Internal API only (consumed by Inference Worker):**
- POST /ai/infer (perform inference with speaker conditioning)
- GET /ai/models/approved
- GET /ai/models/{model_id}/validate-capability
- GET /ai/models/{model_id}/cost-estimate

**Internal API (consumed by Voice Profile Service callback):**
- PATCH /ai/speaker/{profile_id}/purge (purge provider-side conditioning and model artifacts on profile revocation)

**No public API.** Public clients cannot access AI Gateway.

**Events Consumed:**
- voice_profile.revoked (triggers purge of model-specific conditioning)
- user.deleted (triggers purge of model conditioning for user's profiles)

### 8. Inference Worker
**Owns:** Execution orchestration for voice enrollment and narration generation, linguistic chunking, inference-level retries, output assembly, cleanup on failure.

**Does not own:** Job state, audio storage, quotas, model-specific conditioning, user voice profiles. Does NOT publish job/profile lifecycle events.

**Message Broker Consumers:**
- voice_profile.enroll (WORK COMMAND: picks up enrollment work)
- narration.generate (WORK COMMAND: picks up narration generation work)

**Internal Service Calls:**
- Narration Orchestrator: GET /jobs/{job_id}/work-item (retrieve script and params)
- Voice Profile Service: GET /voices/{profile_id} (validate still active), PATCH /voices/{profile_id}/status (report enrollment completion/failure)
- AI Gateway: POST /ai/infer (perform inference)
- Narration Orchestrator: PATCH /jobs/{job_id}/status, POST /jobs/{job_id}/complete (report job completion), POST /jobs/{job_id}/fail (report job failure)
- Artifact Service: POST /artifacts/upload (store generated audio)

**Important:** Worker reports results via service APIs. It does NOT publish job or profile lifecycle events; owning services do.

**Internal API:** None (Worker is async only, no inbound API)

**No public API.** Public clients cannot access Inference Worker.

### 9. Audit Service
**Owns:** Immutable audit history. Audit is read-only, eventual, non-blocking.

**Async Event Consumption:** Consumes all domain events via message broker (at-least-once, idempotent).

**Public API:**
- None (audit ingestion is internal event-driven only)

**Admin API (protected, through API Gateway):**
- GET /admin/audit/events (query audit history with filtering)
- GET /admin/audit/user/{user_id}/timeline
- GET /admin/audit/job/{job_id}/history

**No direct audit write API.** Audit Service consumes events asynchronously only.

**Events Consumed:** All domain events (auth, consent, voice_profile, narration_job, artifact, quota/budget, usage)

## Shared Infrastructure

- **API Gateway:** Public-facing HTTP entry point; routes to Auth, Voice Profile, Narration Orchestrator, Artifact (download/preview), Usage & Policy
- **Message Broker:** Asynchronous event bus (at-least-once delivery)
- **PostgreSQL:** Shared server; each service owns schema/namespace with service-specific credentials
- **Object Storage:** Binary artifacts; accessed only through Artifact Service API
- **Secrets Infrastructure:** API keys, provider credentials, database passwords
- **Observability:** Centralized logging, metrics, distributed tracing

## Architectural Rules

| Rule | Enforcement |
|------|------------|
| No service reads/writes another service's database | Schema namespace isolation; separate credentials per service |
| Services reference other services' data only by ID | Call owning service API for details; no direct data access |
| Synchronous APIs for immediate decisions | Authentication, authorization, quota reservation |
| Asynchronous events for lifecycle propagation | Profile revocation, job completion, consent changes via events |
| Work commands separate from domain events | voice_profile.enroll (work) vs voice_profile.enrolled (event); narration.generate (work) vs narration_job.submitted/completed (events) |
| Only owning service publishes lifecycle events | Orchestrator publishes job events (Worker reports via API); Voice Profile publishes profile events (Worker reports via API) |
| Artifact Service exclusive binary-storage boundary | All artifact operations go through Artifact API; storage paths never exposed to clients |
| AI Gateway exclusive model/provider boundary | Inference Worker calls AI Gateway only; no direct provider access; AI Gateway owns model conditioning |
| Public clients cannot access internal services | No direct access to AI Gateway, Inference Worker, Audit, or internal policy operations |
| Audit is eventual and non-blocking | Normal workflows must not depend on audit availability; async consumption only |
| Narration Orchestrator owns job state, coordinates quota | Orchestrator is source of truth; Inference Worker updates via API; quota reserved before job accepted |
| Inference Worker owns execution details | Worker manages inference retries, chunking, assembly, cleanup internally; reports via API |
| Token-based auth, not service-wide Auth dependency | Auth Service issues signed tokens; services validate locally; Auth not a runtime dependency for internal calls |
| Transactional outbox for events | State changes include outbox record in same transaction; background publisher sends to broker |
| User data isolation enforced | Every operation validates user_id ownership; no cross-user data exposure |
| Retention policies do not override revocation | Approved deletion/revocation requirements purge artifacts immediately, regardless of retention policy |

## API Gateway Public and Internal Route Inventory

### Public/Protected Routes (via API Gateway)
The API Gateway routes legitimate external/user-initiated operations to:

**Authentication:**
- POST /auth/register
- POST /auth/verify-email
- POST /auth/login
- GET /auth/me

**Consent:**
- POST /consent/record
- GET /consent/{consent_id}
- DELETE /consent/{consent_id} (user-initiated revocation)

**Voice Profile:**
- POST /voices (create profile)
- GET /voices (list profiles)
- GET /voices/{profile_id} (get profile status)
- DELETE /voices/{profile_id} (user-initiated revocation)
- PATCH /voices/{profile_id}/quality-override (user-initiated override of quality warning)

**Narration Orchestrator:**
- POST /jobs (submit narration job)
- GET /jobs (list user's jobs)
- GET /jobs/{job_id} (get job status)
- POST /jobs/{job_id}/cancel (cancel job)

**Artifact Service:**
- GET /artifacts/{artifact_id}/download-url (signed URL for download)
- GET /artifacts/{artifact_id}/preview-url (signed URL for preview)

**Usage & Policy (limited access):**
- GET /quotas/me (user's quota status)

**Audit Service (admin-only):**
- GET /admin/audit/events (query audit history)
- GET /admin/audit/user/{user_id}/timeline
- GET /admin/audit/job/{job_id}/history

### Internal-Only Routes (No Public Access)
The following services and operations are NOT accessible to public clients:

**AI Gateway (internal-only):**
- POST /ai/infer (inference endpoint, consumed by Inference Worker only)
- GET /ai/models/approved (model catalog)
- GET /ai/models/{model_id}/cost-estimate (cost estimation API)
- GET /ai/models/{model_id}/validate-capability (capability validation)
- PATCH /ai/speaker/{profile_id}/purge (model-conditioning purge on revocation)

**Inference Worker (internal-only):**
- No public HTTP API; async worker only
- Consumes work commands from message broker
- Calls Narration Orchestrator, Voice Profile, AI Gateway, Artifact Service via internal APIs

**Voice Profile Service (internal-only):**
- PATCH /voices/{profile_id}/status (Inference Worker status reporting)
- GET /voices/validate/{profile_id} (profile validation)

**Narration Orchestrator (internal-only):**
- GET /jobs/{job_id}/work-item (Inference Worker retrieves work details)
- PATCH /jobs/{job_id}/status (Inference Worker status updates)
- POST /jobs/{job_id}/complete (Inference Worker reports completion)
- POST /jobs/{job_id}/fail (Inference Worker reports failure)

**Artifact Service (internal-only):**
- POST /artifacts/batch-delete (generated-audio purging on revocation)
- GET /artifacts/{artifact_id}/metadata (artifact metadata lookup)

**Usage & Policy (internal-only):**
- POST /quotas/reserve (quota reservation, called by Orchestrator)
- POST /quotas/commit-usage (usage commitment, called by Orchestrator)
- POST /quotas/release-reservation (reservation release on failure)

**Audit Ingestion (internal-only):**
- No inbound HTTP API; event-driven only via message broker

---
