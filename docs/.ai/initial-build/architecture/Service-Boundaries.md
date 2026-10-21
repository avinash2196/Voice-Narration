# Service Boundaries — initial-build

## Purpose
Define exact boundaries, responsibilities, and interfaces for each Voice Narration Studio service. This document is authoritative for service scope.

## Service Matrix

| Service | Primary Responsibility | API Type | Public? | Database | Events Published | Events Consumed |
|---------|------------------------|----------|---------|----------|------------------|-----------------|
| Auth Service | User identity, registration, authentication, tokens | Sync | Yes | User accounts, tokens | user.verified, user.deleted | — |
| Consent Service | Immutable consent records, revocation history | Sync | Yes | Consent records, history | consent.recorded, consent.revoked | — |
| Voice Profile Service | Logical profile lifecycle, metadata | Sync | Yes | Voice profiles, profile metadata | voice_profile.enroll (cmd), voice_profile.enrolled, voice_profile.enrollment_failed, voice_profile.revoked | consent.revoked, user.deleted |
| Narration Orchestrator | Job lifecycle, idempotency, quota coordination | Sync | Yes | Narration jobs, job history | narration.generate (cmd), narration_job.submitted, narration_job.started, narration_job.completed, narration_job.failed, narration_job.cancelled | voice_profile.revoked, user.deleted |
| Artifact Service | Binary storage, signed access, retention | Sync | Yes (limited) | Artifact metadata | artifact.stored, artifact.deleted | voice_profile.revoked, user.deleted |
| Usage & Policy Service | Quotas, rate limits, budget enforcement, reservations | Sync | Yes (limited admin read) | Quota config, usage tracking, reservations | quota.exceeded, budget.exceeded, usage.recorded | user.deleted |
| AI Gateway | Model routing, capability validation, speaker conditioning | Sync | No (internal only) | Model catalog, licenses, model-specific metadata | — | voice_profile.revoked, user.deleted |
| Inference Worker | Enrollment and generation execution, chunking, assembly | Async | No | Inference state (ephemeral) | — | voice_profile.enroll, narration.generate |
| Audit Service | Immutable audit history (event-driven, eventual) | Async (event consumer) | No | Audit log | — | All domain events |

## Service Data Ownership

### Auth Service
**Owns:**
- users (user_id, email, password_hash, verified, role, created_at, updated_at)
- sessions/tokens (token, user_id, expiry, revoked)

**References:**
- None (Auth does not reference other services)

**Does not own:**
- Consent records
- Voice profiles
- Jobs
- Quotas

---

### Consent Service
**Owns:**
- consent_records (consent_id, user_id, consent_text, consent_version, created_at, consenting_identity)
- consent_history (consent_id, event_type, timestamp, details)
- consent_status (consent_id, status=active|revoked, revoked_at, revocation_reason)

**References:**
- user_id → Auth Service

**Does not own:**
- Voice profiles
- Jobs
- Audio storage

---

### Voice Profile Service
**Owns:**
- voice_profiles (profile_id, user_id, voice_name, enrollment_status=PENDING|ENROLLING|ENROLLED|FAILED|REVOKED, created_at, updated_at)
- profile_metadata (profile_id, consent_id, sample_artifact_ids[])

**References:**
- user_id → Auth Service (to verify ownership)
- consent_id → Consent Service (validate consent is active)
- sample_artifact_ids → Artifact Service (samples owned by Artifact Service, referenced by ID only)

**Does not own:**
- Consent records
- Audio sample binary content
- Model-specific embeddings (AI Gateway owns)
- Job data

**State Transitions:**
- PENDING → ENROLLING (when voice_profile.enroll work command published)
- ENROLLING → ENROLLED (when Inference Worker reports success via PATCH /voices/{id}/status, Voice Profile publishes voice_profile.enrolled)
- ENROLLING → FAILED (when Inference Worker reports failure via PATCH /voices/{id}/status, Voice Profile publishes voice_profile.enrollment_failed)
- Any state → REVOKED (when user deletes or consent.revoked consumed)

---

### Narration Orchestrator Service
**Owns:**
- narration_jobs (job_id, user_id, profile_id, status, script_snapshot, language, generation_params, idempotency_key, created_at, updated_at)
- job_status_history (job_id, status, timestamp, details)
- idempotency_state (idempotency_key, user_id, request_hash, response_snapshot, expires_at)
- job_output (job_id, output_artifact_id, duration_seconds, estimated_cost_usd, actual_cost_usd)

**References:**
- user_id → Auth Service (to verify identity)
- profile_id → Voice Profile Service (validate ownership, enrollment_status)
- output_artifact_id → Artifact Service (reference to generated audio)
- reservation_id → Usage & Policy Service (external reference for quota reservation coordination)

**Does not own:**
- Voice profiles
- Consent records
- Audio storage
- Quotas (Usage & Policy owns)
- Quota reservations (Usage & Policy Service owns)

**Job Status Transitions:**
- SUBMITTED (after quota reservation succeeds) → PROCESSING → COMPLETED / FAILED
- SUBMITTED → CANCELLED (user cancel or profile revoked)
- PROCESSING → CANCELLED (profile revoked mid-flight)

---

### Artifact Service
**Owns:**
- artifacts (artifact_id, user_id, artifact_type=sample|generated_audio|preview, file_size, format, sample_rate_hz, duration_seconds, created_at, expires_at)
- artifact_content (artifact_id, storage_path_or_reference)
- artifact_access_log (artifact_id, user_id, access_timestamp, ip_address)
- retention_policy (artifact_type, default_retention_days)

**References:**
- user_id → Auth Service
- artifact_id is referenced by other services (stored in their records, never direct access)

**Does not own:**
- User profiles
- Jobs
- Consent records

---

### Usage & Policy Service
**Owns:**
- quota_config (quota_type, default_limit, configurable)
- user_quotas (user_id, quota_type, limit, period, current_usage, reset_at)
- quota_reservations (reservation_id, user_id, job_id, reserved_amount, status, created_at, expires_at)
- usage_accounting (usage_id, user_id, job_id, usage_amount, actual_cost_usd, timestamp)
- budget_policy (monthly_budget_usd, kill_switch_enabled, threshold_usd)

**References:**
- user_id → Auth Service
- job_id → Narration Orchestrator (for cost tracking, referenced in usage records only)

**Does not own:**
- Jobs
- Voice profiles
- Audio storage

**Reservation Semantics:**
- Reservation is atomic: reserve(user_id, duration_estimate) → reservation_id or failure
- Multiple concurrent reserve() calls are serialized per user (pessimistic locking or optimistic with retry)
- Successful reservation decrements available quota
- After job completion: commit_usage(reservation_id, actual_usage) records actual cost
- On failure/cancellation: release_reservation(reservation_id) restores quota

---

### AI Gateway
**Owns:**
- approved_models (model_id, provider, model_name, version, capabilities, license_url, cost_per_unit, supported_languages)
- model_capabilities (model_id, supports_expressive_controls, supports_speaker_conditioning, max_output_duration_seconds, quality_metrics)
- provider_credentials (provider_id, api_key, api_endpoint, auth_method) — secured in secrets infrastructure
- speaker_conditioning (profile_id, model_id, model_speaker_id, conditioning_vector_reference) — provider-specific metadata or references

**References:**
- None (AI Gateway is internal; other services reference it only by inference result)

**Does not own:**
- Jobs
- User profiles
- Audio storage
- User voice profiles (references profile_id only for conditioning lookups)

**Revocation Responsibility:**
- On voice_profile.revoked: purge provider-side speaker conditioning, embeddings, cached clone data associated with profile_id
- Purge all model-specific artifacts (model_speaker_id references, conditioning vectors, cached inference artifacts)

---

### Inference Worker
**Owns:**
- (None in persistent storage; ephemeral state only)
- Local inference state (current job being processed, intermediate chunks, assembly buffer)

**References:**
- job_id → Retrieved from message broker event, then queried from Narration Orchestrator
- profile_id → Retrieved from job context
- model_id → Retrieved from AI Gateway capability check

**Does not own:**
- Jobs (Narration Orchestrator owns)
- Audio storage (Artifact Service owns)
- Quotas (Usage & Policy owns)

---

### Audit Service
**Owns:**
- audit_log (audit_id, timestamp, event_type, actor_id, resource_id, resource_type, action, metadata)
- audit_index (timestamp, resource_id, actor_id for fast queries)

**References:**
- All domain events (consumes, never calls synchronously)

**Does not own:**
- Any business data (Audit is read-only)

---

## API Boundary Matrix

| Auth Service | Provides Sync API? | Provides Async Event? | Consumes Async Event? | Public Client Access? |
|-------------|-------------------|----------------------|----------------------|-----------------------|
| Auth Service | Yes | Yes (user.verified, user.deleted) | No | Yes |
| Consent Service | Yes | Yes (consent.*) | No | Yes |
| Voice Profile Service | Yes | Yes (voice_profile.*) | Yes (consent.revoked) | Yes |
| Narration Orchestrator | Yes | Yes (narration_job.*) | Yes (voice_profile.revoked) | Yes |
| Artifact Service | Yes (limited) | Yes (artifact.*) | Yes (voice_profile.revoked) | Yes (download/preview only via signed URL) |
| Usage & Policy Service | Yes (limited admin) | Yes (quota.*, budget.*, usage.*) | Yes (narration_job.completed) | Yes (read-only for authenticated user) |
| AI Gateway | No | No | Yes (voice_profile.revoked for cleanup) | **No (internal only)** |
| Inference Worker | No | No | Yes (voice_profile.enrollment_requested, narration_job.submitted) | **No (internal only)** |
| Audit Service | No (admin read API separate) | No | Yes (all domain events) | **No (admin API through API Gateway only)** |

## Data Isolation Rules

**Rule 1: No Cross-Service Database Access**
- Each service has exclusive read/write access to its own schema/namespace
- Services authenticate to database with service-specific credentials
- In M0 local development, services may use same PostgreSQL server but different schemas
- Example: Auth uses schema `auth_dev`, Voice Profile uses schema `voice_profile_dev`, etc.

**Rule 2: Data Sharing via API Only**
- Service A that needs data from Service B must call Service B's API
- Service A may cache the response locally for performance but must validate freshness
- Service A must never query Service B's database directly

**Rule 3: Reference by ID**
- Services store only IDs of resources owned by other services
- Example: Narration Orchestrator stores `user_id` (from Auth) and `profile_id` (from Voice Profile) but never the full object
- When Orchestrator needs profile details, it calls Voice Profile Service API

**Rule 4: Eventual Consistency**
- When Service A must know about changes to Service B's data, Service B publishes a domain event
- Service A processes the event asynchronously, updating its local view if needed
- Example: When voice profile is revoked, Voice Profile Service publishes `voice_profile.revoked` event; Narration Orchestrator consumes it and rejects future jobs using that profile

## Event Contract

Every domain event includes:
```
{
  "event_type": "service.resource.action", # Examples: "consent.recorded", "voice_profile.revoked"
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "profile_id / job_id / consent_id / etc",
  "resource_type": "VoiceProfile / NarrationJob / Consent / etc",
  "version": "1",
  "data": { /* event-specific data */ }
}
```

## Service-to-Service Call Matrix

| Caller | Callee | When | Purpose |
|--------|--------|------|---------|
| All services | Auth Service | On every request | Verify bearer token, get user_id, role |
| Voice Profile Service | Consent Service | On enrollment, on validation | Validate consent is active |
| Voice Profile Service | Artifact Service | On profile creation | Reference sample artifact IDs |
| Narration Orchestrator | Voice Profile Service | On job submission | Validate profile exists, owner, capability |
| Narration Orchestrator | Usage & Policy Service | On job submission | Check quota before accepting job |
| Inference Worker | Voice Profile Service | Before inference | Validate profile still active (not revoked) |
| Inference Worker | AI Gateway | During inference | Get model, invoke inference |
| Inference Worker | Narration Orchestrator | During job execution | Update job status, mark complete/failed |
| Inference Worker | Artifact Service | After inference | Store generated audio, get artifact_id |
| Artifact Service | Narration Orchestrator | On artifact deletion cascade | Notify that artifacts were deleted (via event) |
| Usage & Policy Service | Narration Orchestrator | On policy queries | Retrieve job cost data |

---
