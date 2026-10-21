# Data Ownership — initial-build

## Purpose
Define which service owns each data entity, responsibility boundaries, and lifecycle rules.

## Complete Data Ownership Matrix

| Entity | Owner | Database Namespace | Lifecycle | Accessed By |
|--------|-------|-------------------|-----------|-------------|
| user | Auth Service | auth | Create at registration; update on password/profile change; soft-delete on user request | All services via token verification |
| session/token | Auth Service | auth | Create at login; update on refresh; invalidate on logout/revocation | Auth Service exclusively; services validate tokens locally |
| consent_record | Consent Service | consent | Create when user records; immutable; versioned | Consent, Voice Profile Services |
| consent_revocation | Consent Service | consent | Recorded when user revokes; immutable history | Consent Service (triggers event) |
| voice_profile | Voice Profile Service | voice_profile | Create on enrollment start (PENDING); transition ENROLLING→ENROLLED or FAILED (per Worker); soft-delete (REVOKED) on user/consent revocation | Voice Profile, Narration Orchestrator Services |
| profile_enrollment_state | Voice Profile Service | voice_profile | Owned by Voice Profile; Inference Worker updates via PATCH /voices/{profile_id}/status | Voice Profile, Inference Worker |
| voice_enrollment_samples | Artifact Service (binary), Voice Profile Service (metadata reference) | Artifact metadata in artifact schema | Created during enrollment; retained until profile deleted/revoked | Voice Profile Service (references by ID), Artifact Service (owns binary) |
| model_speaker_conditioning | AI Gateway | ai_gateway | Created during enrollment (Worker→AI Gateway); purged on voice_profile.revoked | AI Gateway exclusively |
| narration_job | Narration Orchestrator | orchestrator | Create on submission (QUEUED); progress through FR-022 states (QUEUED→PREPARING→RUNNING→POST_PROCESSING→COMPLETED, or FAILED/CANCELLED); idempotent | Narration Orchestrator, Inference Worker, Audit Service |
| job_idempotency_state | Narration Orchestrator | orchestrator | Create with job; used for deduplication; expire after TTL | Narration Orchestrator exclusively |
| quota_reservation | Usage & Policy Service | usage_policy | Create by Orchestrator (reserve call); update on completion (commit/release) | Usage & Policy, Narration Orchestrator |
| generated_audio | Artifact Service (binary) | artifact | Create by Inference Worker via Artifact Service API; retain per approved policy; delete on expiry or user request | Artifact Service (binary); referenced by Narration Orchestrator |
| artifact_metadata | Artifact Service | artifact | Create when artifact uploaded; update on access; delete on expiry/revocation | Artifact Service exclusively |
| quota_config | Usage & Policy Service | usage_policy | Create at system setup; update by admin; shared across all users | Usage & Policy Service exclusively |
| user_quota | Usage & Policy Service | usage_policy | Create when user registered or quota enabled; reset per period; update on usage | Usage & Policy Service exclusively |
| usage_record | Usage & Policy Service | usage_policy | Create for each job completion; immutable for auditing; committed from reservation on job completion | Usage & Policy Service exclusively |
| budget_policy | Usage & Policy Service | usage_policy | Create at system setup; update by admin; kill-switch state | Usage & Policy Service exclusively |
| approved_model | AI Gateway | ai_gateway | Curated by admin; versioned; includes license/cost metadata | AI Gateway exclusively |
| provider_credential | AI Gateway (secrets) | (secrets infrastructure) | Created at setup; rotated on policy; never stored in application database | AI Gateway exclusively; never exposed |
| audit_event | Audit Service | audit | Appended asynchronously from domain events; immutable; indexed for queries | Audit Service exclusively (read via admin API only) |

## Ownership Responsibility

### Auth Service
**Owns and is responsible for:**
- User identity, authentication, authorization
- Bearer token issuance, validation, revocation
- Email verification and account status
- Password hashing and storage

**Must guarantee:**
- Tokens are valid only when user exists and is active
- Passwords never logged or exposed
- Email addresses verified before activation
- Role-based access control enforced

---

### Consent Service
**Owns and is responsible for:**
- Recording user consent in immutable records
- Tracking consent revocations and reasons
- Validating consent before voice enrollment

**Must guarantee:**
- Consent records are append-only
- Revocations are timestamped and cannot be undone
- Every consent record has a version number
- Consent cannot be withdrawn retroactively (history preserved)

---

### Voice Profile Service
**Owns and is responsible for:**
- Voice profile logical lifecycle (PENDING → QUALITY_CHECKING → [AWAITING_USER_OVERRIDE] → ENROLLING → ENROLLED, or → FAILED, or → REVOKED per AC-ENR-001)
- Profile-to-consent linkage (reference only, Consent Service validates)
- Profile-to-sample linkage (reference only, Artifact Service owns binary)
- Profile metadata including approved model/version reference (FR-012)
- Quality assessment results and user-override decisions (AC-ENR-001)
- Publishing enrollment request to Worker
- Accepting enrollment completion/failure/quality-warning from Worker
- Publishing final enrollment events (enrolled, enrollment_failed, quality_warning, revoked)
- Consuming consent.revoked and revoking affected profiles

**Must guarantee:**
- Profile cannot exist without valid consent
- Profile metadata records the model/model-version used for enrollment (FR-012, AC-HIST-001)
- Quality findings are persisted when requiring user decision (not ephemeral)
- Sample artifact IDs are validated with Artifact Service
- Revocation cascades immediately to Narration Orchestrator and Artifact Service (event-driven)
- Enrollment state transitions follow approved lifecycle (AC-ENR-001)
- Profile remains immutable after REVOKED state

**Model-Specific Conditioning:** AI Gateway owns this data exclusively; Voice Profile Service does NOT store embeddings or provider-specific conditioning

---

### Narration Orchestrator
**Owns and is responsible for:**
- Job lifecycle state (QUEUED, PREPARING, RUNNING, POST_PROCESSING, COMPLETED, FAILED, CANCELLED per FR-022)
- Job idempotency (deduplication by idempotency_key)
- Job snapshots including model/model-version used for that job (FR-023, AC-HIST-001)
- Quota reservation coordination (call Usage & Policy before accepting job)
- Job retries at workflow level (re-submission to Inference Worker on failure)
- Job history and durable state (survives service restarts)

**Must guarantee:**
- Each job transitions through valid states only (FR-022 compliance)
- Idempotency is enforced (same request = same response, even after retry)
- Job state is durable (survives service restarts)
- Job cannot reference deleted or revoked profiles (validation on submission)
- Job history is immutable for compliance
- Quota reservation succeeds atomically before job QUEUED event published
- On job completion/failure, usage is committed/released atomically via idempotent API call (before transitioning to COMPLETED)
- Job cannot proceed to PREPARING until profile enrollment complete (profile status = ENROLLED)

---

### Artifact Service
**Owns and is responsible for:**
- All binary storage (samples, generated audio, previews)
- Access control (signed URLs, user isolation)
- Retention enforcement (TTL, deletion policies)
- Storage abstraction (could be local filesystem, S3, GCS, etc.)

**Must guarantee:**
- Binary artifacts are stored in user-isolated locations
- Signed URLs prevent unauthenticated access
- Deletion policies are enforced (no orphaned files)
- All artifact operations are logged
- File format and size constraints enforced

---

### Usage & Policy Service
**Owns and is responsible for:**
- Quota definition and enforcement (per-user limits)
- Quota reservation lifecycle (reserve → commit/release)
- Budget tracking and kill-switch enforcement
- Usage accounting for each job (actual cost, not estimate)
- Cost estimation and tracking

**Must guarantee:**
- Quota reservations are atomic per user (no race conditions on concurrent submissions)
- Successful reservation returns opaque reservation_id
- Budget kill-switch is atomically enforced
- Usage records are immutable (for billing)
- Cost is calculated consistently
- Quotas reset on schedule (e.g., monthly reset)
- Reservation expires if job not completed within TTL
- After job completion, actual cost committed to reservation
- On job failure/cancellation, reservation released (quota restored)

---

### AI Gateway
**Owns and is responsible for:**
- Approved-model catalog (which models are production-ready)
- Model capability validation (does model support expressive controls?)
- Provider credential management (API keys, auth tokens)
- Model-specific speaker conditioning and embeddings
- Inference cost estimation
- Purging provider-side artifacts on revocation

**Must guarantee:**
- Only approved models are exposed to Inference Worker
- Model capabilities match product requirements (language, expressive controls, duration)
- Provider credentials are never exposed in logs or APIs
- Cost estimates are accurate and used for budget enforcement
- Speaker conditioning data purged within approved revocation window
- Cached inference artifacts purged when profile revoked
- Embeddings and provider-specific voice-clone data purged immediately on revocation

---

### Inference Worker
**Owns and is responsible for:**
- Execution orchestration for voice enrollment and narration generation
- Linguistic chunking (splitting long scripts for inference)
- Inference execution (calling AI Gateway)
- Inference-level retries (handling transient failures)
- Audio assembly (stitching chunks into final output)
- Cleanup on failure (partial artifacts)
- Reporting completion/failure back to owning services

**Must guarantee:**
- Chunks are processed in order
- Failed chunks are retried without corrupting output
- Assembly produces valid audio format
- Worker completes jobs even if intermediate chunks fail (per retry policy)
- On failure, cleanup partial artifacts via Artifact Service
- Enrollment results reported to Voice Profile Service
- Job results reported to Narration Orchestrator
- No partial state persisted across worker restarts

---

### Audit Service
**Owns and is responsible for:**
- Immutable audit history (all domain events)
- Audit queries and reporting (for compliance, admin only)
- Audit retention policy
- Admin read API for querying audit history

**Must guarantee:**
- Audit events are append-only (never modified or deleted, except per regulatory requirement)
- Events are timestamped consistently
- No audit event is lost (at-least-once delivery from event bus)
- Audit availability does NOT block business workflows (eventual consistency)
- Admin API requires authentication/authorization
- Audit queries do not expose sensitive data (embeddings, scripts, credentials) unnecessarily

---

## Cascade and Revocation Rules

### When Consent is Revoked (Event: consent.revoked)
**Sequence:**
1. Consent Service publishes: consent.revoked
2. Voice Profile Service consumes: identifies profiles linked to revoked consent_id
3. For each affected profile:
   - Voice Profile Service transitions to REVOKED state
   - Voice Profile Service publishes: voice_profile.revoked
4. Narration Orchestrator consumes: voice_profile.revoked → cancels QUEUED/PREPARING/RUNNING/POST_PROCESSING jobs, releases reservations
5. Artifact Service consumes: voice_profile.revoked → deletes/purges ALL associated artifacts (samples AND generated narration audio linked to jobs using this profile per AC-RET-001), overriding retention policy
6. AI Gateway consumes: voice_profile.revoked → purges model-specific conditioning, embeddings, cached artifacts
7. Audit Service consumes: all events in sequence

**Key:** Consent Service does NOT know profile ownership; Voice Profile Service determines cascade. Generated audio purging must be coordinated with Narration Orchestrator to identify applicable job artifacts.

### When Voice Profile is Revoked (Event: voice_profile.revoked)
**Sequence:**
1. Voice Profile Service transitions profile to REVOKED
2. Voice Profile Service publishes: voice_profile.revoked with sample_artifact_ids
3. Narration Orchestrator consumes: 
   - Cancels QUEUED/PREPARING/RUNNING/POST_PROCESSING jobs using this profile
   - Publishes: narration_job.cancelled
   - Identifies historical job output_artifact_ids and requests deletion from Artifact Service
4. Artifact Service consumes:
   - Deletes/purges sample artifacts per revocation override (AC-RET-001)
   - On receipt of historical job artifacts from Orchestrator, deletes those generated audio artifacts immediately (AC-RET-001, R-DEL-001)
   - Publishes: artifact.deleted for each artifact removed
5. AI Gateway consumes: purges provider-specific conditioning, embeddings, cached model artifacts
6. Audit Service consumes: records all events

**Key:** Revocation takes precedence over all retention policies. Generated narration audio tied to revoked profiles must be purged immediately. Artifact Service must be able to delete artifacts by ID supplied by Narration Orchestrator.

### When Job is Completed (Event: narration_job.completed)
**Sequence (FR-045, FR-023 compliance):**
1. Inference Worker completes inference, calls Narration Orchestrator: POST /jobs/{job_id}/complete
2. Narration Orchestrator:
   - Calls Usage & Policy Service: POST /quotas/commit-usage (idempotent, using reservation_id)
   - Only after commit succeeds, updates job status to COMPLETED
   - Stores job snapshot (profile_id, model_version, generation_params, output_artifact_id, cost, timestamps)
   - Inserts outbox: `narration_job.completed` event
   - Background publisher sends event
3. Consumers of narration_job.completed:
   - Usage & Policy Service: No consumption as trigger (usage already committed synchronously)
   - Artifact Service: Set retention timer on generated_audio artifact
   - Audit Service: Record completion event

**Key:** Usage is committed synchronously in step 2 by Orchestrator, not triggered by event. The event is for audit only.

### When User is Deleted (Event: user.deleted)
**Sequence:**
1. Auth Service publishes: user.deleted
2. Cascade consumers (parallel, eventual consistency):
   - Consent Service: Soft-delete user's consent records per approved retention policy
   - Voice Profile Service: Revoke all user profiles (triggers voice_profile.revoked cascades)
   - Narration Orchestrator: Cancel all active jobs, release reservations
   - Artifact Service: Delete/purge all user's artifacts (samples, generated audio) per approved deletion requirements (R-DEL-001)
   - Usage & Policy Service: Archive/deactivate user's quota and usage state
   - Audit Service: Archive user's audit trail
3. Each cascade is idempotent (safe for duplicate event delivery)

**Key:** All consumers must be idempotent and able to identify their user's data independently. No sequential ordering required (eventual consistency).

---

## Data Isolation Guarantees

### Per-User Isolation
- Every data entity includes `user_id` (or is transitively owned via user_id)
- Services enforce user ownership checks (e.g., "voice profiles must belong to the authenticated user")
- No API exposes other users' data except admin operations (read-only quota/audit queries)

### Per-Service Database Isolation
- Each service's schema is separate and cannot be accessed by other services
- Each service authenticates to database with its own service credential
- Foreign keys exist only within a service's schema; cross-service references are IDs only

### Encryption at Rest
- All sensitive data (passwords, tokens, sample audio, generated audio) encrypted at rest (configuration defined in security/encryption-policy.md)

### Signed Access to Artifacts
- All artifact downloads/previews use signed URLs with expiry
- Artifacts are stored in user-isolated namespaces (e.g., S3 prefix: s3://artifacts/user_{user_id}/...)

---

## Reference Semantics

When Service A references Service B's data:

1. **Store:** Store only the resource ID (e.g., profile_id, artifact_id)
   ```sql
   narration_jobs.profile_id → voice_profiles.profile_id
   ```

2. **Validate:** When needed, call Service B's API to validate
   ```
   GET /voices/validate/{profile_id}
   ```

3. **Cache:** May cache the response (with TTL) for performance, but re-validate if stale
   ```
   cached_profile_metadata expires after 5 minutes
   ```

4. **Never Query:** NEVER query Service B's database directly
   ```
   ❌ SELECT * FROM voice_profile_service.voice_profiles WHERE profile_id = ?
   ✅ GET /voices/{profile_id}
   ```

---

## Lifecycle State Machines

### Voice Profile Lifecycle
```
enrolled --[user_revokes]--> revoked --[retention_expires]--> deleted
  ^                                                            |
  |___________________[user_re-enrolls]________________________|
```

### Narration Job Lifecycle
```
submitted --[user_cancels]--> cancelled
    |
    v
processing --[profile_revoked]--> cancelled
    |
    v
completed --[retention_expires]--> archived
    |
    v
  failed --[retry]--> submitted (resubmitted)
```

### Artifact Lifecycle
```
stored --[uploaded_by_user]--> active
  |                              |
  |                              v
  |---[retention_timer_starts]-->[expiring]
  |                              |
  +--[user_deletes]---------->[deleted]
  |
  +--[retention_expires]----->[deleted]
```

---

## Shared PostgreSQL Schema Isolation (M0 Local)

In M0 local development, all services use the same PostgreSQL server but different schemas:

```sql
CREATE SCHEMA auth_dev;
CREATE SCHEMA consent_dev;
CREATE SCHEMA voice_profile_dev;
CREATE SCHEMA orchestrator_dev;
CREATE SCHEMA artifact_dev;
CREATE SCHEMA usage_policy_dev;
CREATE SCHEMA ai_gateway_dev;
CREATE SCHEMA audit_dev;
```

Each service connects with:
```
postgresql://service_user:password@localhost/voice_narration
  search_path = service_schema_dev
```

In production, each service may use a dedicated database and/or fully isolated PostgreSQL instance.

---
