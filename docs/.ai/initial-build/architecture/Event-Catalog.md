# Event Catalog — initial-build (REVISED)

## Purpose
Define all domain events and work commands, their publishers, subscribers, payload schemas, and delivery guarantees.

## Event Naming Convention

**Domain Events** use form: `<service>.<resource>.<action>` (past tense)
- Examples: `consent.recorded`, `voice_profile.enrolled`, `narration_job.completed`
- Published for audit and eventual consistency
- Subscribers process events asynchronously

**Work Commands** use form: `<service>.<resource>.<action>` (request, not event)
- Examples: `voice_profile.enroll`, `narration.generate`
- Published to work brokers
- Consumed by async workers (Inference Worker)
- Workers report results back to owning services via APIs (they do NOT publish lifecycle events)

---

## Complete Event Catalog

### Authentication Events

#### user.verified
**Publisher:** Auth Service (via background outbox publisher)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "user.verified",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "usr_123",
  "resource_type": "User",
  "version": "1",
  "data": {
    "user_id": "usr_123",
    "email": "user@example.com",
    "verified_at": "2026-10-19T12:00:00Z"
  }
}
```
**Delivery Guarantee:** At-least-once (via transactional outbox)
**Latency:** <5 seconds (background publisher)
**Retention:** Per approved retention policy

#### user.deleted
**Publisher:** Auth Service (via background outbox publisher, on user deletion)
**Subscribers:** Consent Service, Voice Profile Service, Narration Orchestrator, Artifact Service, Usage & Policy Service, Audit Service
**Payload:**
```json
{
  "event_type": "user.deleted",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "usr_123",
  "resource_type": "User",
  "version": "1",
  "data": {
    "user_id": "usr_123",
    "deleted_at": "2026-10-19T12:00:00Z",
    "deleted_by": "user_requested | admin"
  }
}
```
**Delivery Guarantee:** At-least-once
**Latency:** <3 seconds
**Retention:** Per approved retention policy
**Cascade Consumers:**
- **Consent Service:** Soft-delete user's consent records per approved retention policy
- **Voice Profile Service:** Revoke all user profiles (publishes voice_profile.revoked events)
- **Narration Orchestrator:** Cancel all active jobs, release reservations
- **Artifact Service:** Delete user's artifacts (samples, generated audio) per approved deletion requirements
- **Usage & Policy Service:** Archive user's quota and usage records
- **Audit Service:** Record account deletion and cascade events

---

### Consent Events

#### consent.recorded
**Publisher:** Consent Service (via background outbox publisher)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "consent.recorded",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "con_abc",
  "resource_type": "Consent",
  "version": "1",
  "data": {
    "consent_id": "con_abc",
    "user_id": "usr_123",
    "consent_version": 1,
    "consenting_identity": "voice_narration_m0",
    "recorded_at": "2026-10-19T12:00:00Z"
  }
}
```
**Note:** Payload does NOT include full consent_text (store separately in database, reference by ID only)
**Delivery Guarantee:** At-least-once (via transactional outbox)
**Latency:** <1 second
**Retention:** Per approved retention policy

#### consent.revoked
**Publisher:** Consent Service (via background outbox publisher)
**Subscribers:** Voice Profile Service (determines cascade), Audit Service
**Payload:**
```json
{
  "event_type": "consent.revoked",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "con_abc",
  "resource_type": "Consent",
  "version": "1",
  "data": {
    "consent_id": "con_abc",
    "user_id": "usr_123",
    "revoked_at": "2026-10-19T12:00:00Z",
    "revocation_reason": "user_requested | policy_update | regulatory_requirement"
  }
}
```
**Note:** Does NOT include cascade_profiles or cascade_jobs (Voice Profile Service determines this)
**Delivery Guarantee:** At-least-once (must reach all subscribers)
**Latency:** <3 seconds
**Retention:** Per approved retention policy
**Critical:** Triggers cascade through Voice Profile Service

---

### Voice Profile Events

#### voice_profile.enroll (WORK COMMAND)
**Publisher:** Voice Profile Service (via background outbox publisher)
**Subscribers:** Inference Worker (consumes from work broker)
**Payload:**
```json
{
  "command_type": "voice_profile.enroll",
  "command_id": "cmd_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "prof_1",
  "resource_type": "VoiceProfile",
  "version": "1",
  "data": {
    "profile_id": "prof_1",
    "user_id": "usr_123",
    "voice_name": "My Professional Voice",
    "consent_id": "con_abc",
    "sample_artifact_ids": ["art_s1", "art_s2", "art_s3"],
    "requested_at": "2026-10-19T12:00:00Z"
  }
}
```
**Purpose:** WORK COMMAND to Inference Worker (enrollment request)
**Delivery Guarantee:** At-least-once
**Latency:** <1 second
**Note:** References artifact IDs only; Worker retrieves binary samples via Artifact Service API. Script/sensitive data not included in message.

#### voice_profile.enrolled
**Publisher:** Voice Profile Service (via background outbox publisher, after Worker completes and profile reaches ENROLLED)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "voice_profile.enrolled",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:30Z",
  "actor_id": "usr_123",
  "resource_id": "prof_1",
  "resource_type": "VoiceProfile",
  "version": "1",
  "data": {
    "profile_id": "prof_1",
    "user_id": "usr_123",
    "voice_name": "My Professional Voice",
    "model_version": "v2.1",
    "quality_override_used": false,
    "enrolled_at": "2026-10-19T12:00:30Z"
  }
}
```
**Note:** Includes model_version (FR-012, AC-HIST-001); does NOT include speaker_embedding or model-specific data (AI Gateway owns)
**Delivery Guarantee:** At-least-once
**Retention:** Per approved retention policy

#### voice_profile.enrollment_failed
**Publisher:** Voice Profile Service (via background outbox publisher, after Worker reports hard quality failure or inference failure)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "voice_profile.enrollment_failed",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:30Z",
  "actor_id": "usr_123",
  "resource_id": "prof_1",
  "resource_type": "VoiceProfile",
  "version": "1",
  "data": {
    "profile_id": "prof_1",
    "user_id": "usr_123",
    "failure_reason": "hard_quality_failure | model_inference_error",
    "failure_message": "No speech detected in samples",
    "failed_at": "2026-10-19T12:00:30Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Retention:** Per approved retention policy

#### voice_profile.quality_warning (NEW, AC-ENR-001)
**Publisher:** Voice Profile Service (via background outbox publisher, when Worker detects overrideable quality warnings)
**Subscribers:** Audit Service, Client/UI (for notification)
**Payload:**
```json
{
  "event_type": "voice_profile.quality_warning",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:15Z",
  "actor_id": "usr_123",
  "resource_id": "prof_1",
  "resource_type": "VoiceProfile",
  "version": "1",
  "data": {
    "profile_id": "prof_1",
    "user_id": "usr_123",
    "quality_findings": {
      "clipping": "mild (2-3 peaks)",
      "silence": "within acceptable range",
      "snr": "good (28 dB)",
      "speech_presence": "detected"
    },
    "recommendation": "Re-record for best quality, or override to proceed",
    "overrideable": true,
    "warning_at": "2026-10-19T12:00:15Z"
  }
}
```
**Note:** Actionable findings for user notification; stored in Voice Profile Service for user review
**Delivery Guarantee:** At-least-once
**Retention:** Per approved retention policy

#### voice_profile.revoked
**Publisher:** Voice Profile Service (via background outbox publisher)
**Subscribers:** Narration Orchestrator (cancels jobs, identifies generated audio), Artifact Service (deletes samples and generated audio per AC-RET-001), AI Gateway (purges conditioning), Audit Service
**Payload:**
```json
{
  "event_type": "voice_profile.revoked",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:05:00Z",
  "actor_id": "usr_123",
  "resource_id": "prof_1",
  "resource_type": "VoiceProfile",
  "version": "1",
  "data": {
    "profile_id": "prof_1",
    "user_id": "usr_123",
    "revocation_reason": "user_requested | consent_revoked",
    "revoked_at": "2026-10-19T12:05:00Z",
    "sample_artifact_ids": ["art_s1", "art_s2", "art_s3"]
  }
}
```
**Note:** Includes sample_artifact_ids for Artifact Service cleanup; does not include generated-audio artifact IDs (Orchestrator coordinates that separately per AC-RET-001)
**Delivery Guarantee:** At-least-once (must reach all subscribers)
**Latency:** <3 seconds
**Retention:** Per approved retention policy
**Critical:** Triggers cascades; each subscriber is idempotent; revocation overrides all retention policies

---

### Narration Job Events

#### narration.generate (WORK COMMAND)
**Publisher:** Narration Orchestrator (via background outbox publisher, when job enters QUEUED state per FR-022)
**Subscribers:** Inference Worker (consumes from work broker)
**Payload:**
```json
{
  "command_type": "narration.generate",
  "command_id": "cmd_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "job_456",
  "resource_id": "job_456",
  "resource_type": "NarrationJob",
  "version": "1",
  "data": {
    "job_id": "job_456",
    "profile_id": "prof_1",
    "language": "hindi"
  }
}
```
**Purpose:** WORK COMMAND to Inference Worker (narration request)
**Delivery Guarantee:** At-least-once
**Latency:** <1 second
**Note:** Minimal payload (job_id, profile_id, language). Worker retrieves full script, params, and model_version via GET /jobs/{job_id}/work-item from Narration Orchestrator. No script/sensitive data in message.

#### narration_job.submitted (DOMAIN EVENT)
**Publisher:** Narration Orchestrator (via background outbox publisher, when quota reservation succeeds and job enters QUEUED state per FR-022)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "narration_job.submitted",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "job_456",
  "resource_type": "NarrationJob",
  "version": "1",
  "data": {
    "job_id": "job_456",
    "user_id": "usr_123",
    "profile_id": "prof_1",
    "model_version": "v2.1",
    "language": "hindi",
    "generation_params": {
      "speech_pace": 1.0,
      "pause_strength": 0.5
    },
    "reservation_id": "res_xyz",
    "estimated_duration_seconds": 120,
    "estimated_cost_usd": 12.00,
    "submitted_at": "2026-10-19T12:00:00Z"
  }
}
```
**Purpose:** DOMAIN EVENT (audit only, not a worker command). Worker consumes narration.generate command instead, not this event.
**Delivery Guarantee:** At-least-once
**Latency:** <1 second
**Retention:** 30 days (job history), then archived
**Note:** Includes model_version snapshot (FR-023, AC-HIST-001); does NOT include script

#### narration_job.started
**Publisher:** Narration Orchestrator (via outbox, when Worker transitions job from QUEUED to PREPARING/RUNNING per FR-022)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "narration_job.started",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:30Z",
  "actor_id": "job_456",
  "resource_id": "job_456",
  "resource_type": "NarrationJob",
  "version": "1",
  "data": {
    "job_id": "job_456",
    "user_id": "usr_123",
    "started_at": "2026-10-19T12:00:30Z",
    "current_state": "PREPARING | RUNNING"
  }
}
    "user_id": "usr_123",
    "started_at": "2026-10-19T12:00:30Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Retention:** 30 days

#### narration_job.completed
**Publisher:** Narration Orchestrator (via background outbox publisher, after job reaches COMPLETED state per FR-022 and usage is successfully committed to Usage & Policy Service)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "narration_job.completed",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:01:30Z",
  "actor_id": "job_456",
  "resource_id": "job_456",
  "resource_type": "NarrationJob",
  "version": "1",
  "data": {
    "job_id": "job_456",
    "user_id": "usr_123",
    "profile_id": "prof_1",
    "model_version": "v2.1",
    "output_artifact_id": "art_gen_1",
    "output_duration_seconds": 125,
    "actual_cost_usd": 12.50,
    "completed_at": "2026-10-19T12:01:30Z"
  }
}
```
**Note:** Includes model_version snapshot (FR-023, AC-HIST-001); does NOT include script or audio binary (references artifact_id only)
**Delivery Guarantee:** At-least-once
**Idempotency:** Orchestrator ensures single event publication per job completion
**Latency:** <2 seconds
**Retention:** 30 days (active), 2 years (archived)
**CRITICAL (FR-045):** Usage commitment (POST /quotas/commit-usage) is synchronous and MUST complete successfully BEFORE this event is published. This event is for audit and lifecycle only, NOT to trigger usage recording. Usage & Policy Service does NOT consume this event for usage-commit purposes.

#### narration_job.failed
**Publisher:** Narration Orchestrator (via background outbox publisher, after Worker reports failure)
**Subscribers:** Audit Service, Admin notifications
**Payload:**
```json
{
  "event_type": "narration_job.failed",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:01:30Z",
  "actor_id": "job_456",
  "resource_id": "job_456",
  "resource_type": "NarrationJob",
  "version": "1",
  "data": {
    "job_id": "job_456",
    "user_id": "usr_123",
    "profile_id": "prof_1",
    "failure_reason": "inference_failed | cost_exceeds_budget | profile_revoked",
    "error_message": "Model inference timeout after 3 retries",
    "failed_at": "2026-10-19T12:01:30Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Retention:** 30 days (then archived per approved retention policy)
**Critical:** Triggers reservation release in Usage & Policy

#### narration_job.cancelled
**Publisher:** Narration Orchestrator (via background outbox publisher, on user cancel or cascade)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "narration_job.cancelled",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:05:00Z",
  "actor_id": "usr_123",
  "resource_id": "job_456",
  "resource_type": "NarrationJob",
  "version": "1",
  "data": {
    "job_id": "job_456",
    "user_id": "usr_123",
    "cancellation_reason": "user_requested | profile_revoked",
    "cancelled_at": "2026-10-19T12:05:00Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Idempotency:** Multiple cancellations of same job are safe (idempotent)
**Retention:** 30 days

---

### Artifact Events

#### artifact.stored
**Publisher:** Artifact Service (via background outbox publisher)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "artifact.stored",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:01:30Z",
  "actor_id": "usr_123",
  "resource_id": "art_gen_1",
  "resource_type": "Artifact",
  "version": "1",
  "data": {
    "artifact_id": "art_gen_1",
    "user_id": "usr_123",
    "artifact_type": "generated_audio | sample | preview",
    "file_size_bytes": 1024000,
    "duration_seconds": 125,
    "stored_at": "2026-10-19T12:01:30Z"
  }
}
```
**Note:** Does NOT include storage_location or bucket path (internal only)
**Delivery Guarantee:** At-least-once
**Latency:** <2 seconds
**Retention:** 30 days (metadata)

#### artifact.accessed
**Publisher:** Artifact Service (on download via signed URL)
**Subscribers:** Audit Service (optional; may be high-volume)
**Payload:**
```json
{
  "event_type": "artifact.accessed",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:30:00Z",
  "actor_id": "usr_123",
  "resource_id": "art_gen_1",
  "resource_type": "Artifact",
  "version": "1",
  "data": {
    "artifact_id": "art_gen_1",
    "user_id": "usr_123",
    "access_type": "preview | download",
    "accessed_at": "2026-10-19T12:30:00Z"
  }
}
```
**Delivery Guarantee:** Best-effort (high-volume; may be dropped)
**Retention:** Per approved retention policy

#### artifact.deleted
**Publisher:** Artifact Service (via background outbox publisher, on deletion)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "artifact.deleted",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:05:00Z",
  "actor_id": "usr_123",
  "resource_id": "art_gen_1",
  "resource_type": "Artifact",
  "version": "1",
  "data": {
    "artifact_id": "art_gen_1",
    "user_id": "usr_123",
    "artifact_type": "sample | generated_audio | preview",
    "deletion_reason": "retention_expired | user_requested | profile_revoked",
    "deleted_at": "2026-10-19T12:05:00Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Retention:** Per approved retention policy

---

### Usage & Policy Events

#### quota.exceeded
**Publisher:** Usage & Policy Service (via background outbox publisher)
**Subscribers:** Audit Service, Admin notifications
**Payload:**
```json
{
  "event_type": "quota.exceeded",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "usr_123",
  "resource_type": "User",
  "version": "1",
  "data": {
    "user_id": "usr_123",
    "quota_type": "monthly_duration_seconds",
    "requested_amount": 500,
    "limit": 3000,
    "current_usage": 2800,
    "exceeded_at": "2026-10-19T12:00:00Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Retention:** Per approved retention policy

#### budget.exceeded
**Publisher:** Usage & Policy Service (via background outbox publisher)
**Subscribers:** Audit Service, Admin notifications
**Payload:**
```json
{
  "event_type": "budget.exceeded",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:00:00Z",
  "actor_id": "usr_123",
  "resource_id": "usr_123",
  "resource_type": "User",
  "version": "1",
  "data": {
    "user_id": "usr_123",
    "monthly_budget_usd": 20.00,
    "current_spend_usd": 18.50,
    "estimated_cost_of_request_usd": 5.00,
    "exceeded_at": "2026-10-19T12:00:00Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Retention:** Per approved retention policy

#### usage.recorded
**Publisher:** Usage & Policy Service (via background outbox publisher, after job completion)
**Subscribers:** Audit Service
**Payload:**
```json
{
  "event_type": "usage.recorded",
  "event_id": "evt_<uuid>",
  "timestamp": "2026-10-19T12:01:30Z",
  "actor_id": "job_456",
  "resource_id": "usr_123",
  "resource_type": "User",
  "version": "1",
  "data": {
    "user_id": "usr_123",
    "job_id": "job_456",
    "usage_amount": 125,
    "unit": "seconds",
    "actual_cost_usd": 12.50,
    "previous_usage": 1500,
    "new_usage": 1625,
    "remaining_quota": 1375,
    "remaining_budget_usd": 7.50,
    "recorded_at": "2026-10-19T12:01:30Z"
  }
}
```
**Delivery Guarantee:** At-least-once
**Idempotency:** job_id + timestamp deduplicates retries
**Latency:** <3 seconds
**Retention:** 2 years (billing/compliance)

---

## Event Ordering & Consistency

### Per-Resource Ordering (Causal Consistency)
For events with same `resource_id`, message broker enforces ordering:

```
resource_id: prof_1
  voice_profile.enroll (work command published)
  voice_profile.enrolled / voice_profile.enrollment_failed / voice_profile.quality_warning (domain events)
  voice_profile.revoked (terminal)
```

### Per-Job Ordering (Causal Consistency)
For narration jobs:

```
resource_id: job_456
  narration.generate (work command published)
  narration_job.submitted (domain event)
  narration_job.started
  narration_job.completed / narration_job.failed / narration_job.cancelled (terminal)
```

### Cross-Service Dependencies
When Service A's event triggers Service B's consumption:

```
Consent Service publishes: consent.revoked
  ↓ (Voice Profile Service consumes, determines affected profiles)
Voice Profile Service publishes: voice_profile.revoked
  ↓ (Narration Orchestrator, Artifact Service, AI Gateway consume in parallel)
Multiple cascades proceed concurrently (eventual consistency)
```

---

## Transactional Outbox Pattern

Every state change that requires event publication follows:

1. **Database Transaction:**
   - Update business state (e.g., job status = COMPLETED)
   - Insert outbox record: `{event_type, resource_id, payload, published: false}`
   - Commit atomically
   - If commit fails, neither state nor event exists (no partial state)

2. **Background Publisher:**
   - Poll outbox table for `published: false` records
   - Send to message broker
   - Mark outbox record `published: true`
   - If send fails, retry (at-least-once)
   - If broker ACKs but mark fails, idempotent retry is safe (broker may see duplicate)

3. **Consuming Service:**
   - Receive event (may be duplicate)
   - Process idempotently (check if already processed using `event_id`)
   - If already processed, skip
   - If new, process and update inbox/deduplication table

**Result:** No "database commit succeeds but event fails" failures; exactly-once semantics via deduplication.

---

## Dead-Letter Handling

If a consuming service cannot process an event:

1. Publish to dead-letter queue: `dlq.{service}.{event_type}`
2. Record in audit: `event.processing.failed`
3. Alert ops team
4. Admin can manually retry or discard

```json
{
  "event_type": "event.processing.failed",
  "original_event": { /* full event */ },
  "service_attempting": "narration_orchestrator",
  "error": "Job job_456 not found",
  "retry_count": 5,
  "failed_at": "2026-10-19T12:05:00Z"
}
```

---

## Event Retention Policy

Retention is governed by approved requirements, not hard-coded regulatory assumptions.

**Retention periods are configuration/policy-driven; architecture defines these are stored and queryable:**

| Event Type | Suggested Retention | Archival | Purpose |
|------------|-------------------|----------|---------|
| user.* | Per approved requirements | Archive as needed | User lifecycle audit |
| consent.* | Per approved requirements | Archive as needed | Consent records (compliance) |
| voice_profile.* | Per approved requirements | Archive as needed | Profile lifecycle |
| narration_job.* | 30 days (active) → archive | S3 archive | Job history, debugging |
| artifact.* | 30 days (metadata) | Archive as needed | Artifact lifecycle |
| quota.* | 1 year | Archive as needed | Usage tracking |
| budget.* | 1 year | Archive as needed | Financial audit |

**Note:** Approved requirements are authoritative; this table reflects suggested defaults only.

---
