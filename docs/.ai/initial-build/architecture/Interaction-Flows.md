# Interaction Flows — initial-build (REVISED)

## Purpose
Describe critical end-to-end workflows showing synchronous API calls, asynchronous work commands and domain events, service boundaries, and data ownership.

## Key Distinctions

**Domain Events** describe something that already happened. They are published for audit and eventual consistency (examples: `consent.recorded`, `narration_job.completed`, `voice_profile.enrolled`).

**Work Commands** request a worker to perform something. They are published on a work queue consumed by async workers (examples: `voice_profile.enrollment_requested`, `narration_job.submitted`).

In this architecture:
- `voice_profile.enrollment_requested` is a WORK COMMAND (to Inference Worker)
- `voice_profile.enrolled` is a DOMAIN EVENT (for audit)
- `narration_job.submitted` serves as both: WORK COMMAND (to Inference Worker) and DOMAIN EVENT (for audit)

---

## Flow 1: User Registration and Login

### Registration
```
User (Client)
  |
  +→ API Gateway
       |
       +→ Auth Service: POST /auth/register
            {
              email: "user@example.com",
              password: "secret"
            }
            |
            +→ Validate email format
            +→ Hash password
            +→ Create user record (verified=false)
            +→ Send verification email (async via background job)
            |
            └→ Response: { user_id, verification_required: true }
       |
       └→ Client: Store user_id locally
```

**Important:** Registration does NOT create outbox record for user.verified event yet.

### Email Verification
```
User receives verification link → Browser redirects to client

Client
  |
  +→ API Gateway
       |
       +→ Auth Service: POST /auth/verify-email?token=<token>
            |
            +→ Validate token (time-bounded, one-time-use)
            +→ Atomic transaction:
            |   1. Update user.verified = true
            |   2. Insert outbox record: {event: "user.verified", user_id, timestamp}
            |   3. Commit transaction
            |
            +→ Background publisher: Send user.verified event to broker
            |
            └→ Response: { status: verified }
       |
       └→ Client: Ready to login
```

**Critical:** user.verified outbox record created ONLY upon successful email verification, in same DB transaction.

### Login
```
User (Client)
  |
  +→ API Gateway
       |
       +→ Auth Service: POST /auth/login
            {
              email: "user@example.com",
              password: "secret"
            }
            |
            +→ Verify email/password
            +→ Generate signed bearer token (JWT with expiry)
            +→ Create session record
            |
            └→ Response: { bearer_token, user_id, role }
       |
       └→ Client: Store bearer_token, use in all future requests
```

**Data Ownership:**
- Auth Service owns: users, sessions, tokens
- No other service directly accesses user data

**Synchronous Path:** Registration → Verification → Login (all synchronous)

**Event Publication (Async):**
- user.verified (published by background outbox publisher after email verification)

---

## Flow 2: Consent Recording

### User Initiates Consent
```
User (Client)
  |
  +→ Presents consent form (UI describes voice-cloning use)
  |
  +→ User reviews and clicks "I consent"
  |
  +→ API Gateway
       |
       +→ Consent Service: POST /consent/record
            {
              user_id: from_bearer_token,
              consent_text: "I consent to my voice being used for AI voice cloning...",
              consenting_identity: "voice_narration_m0"
            }
            |
            +→ Validate user_id from bearer token
            +→ Create consent_record (immutable)
            +→ Assign consent_version: 1
            +→ Insert outbox record: {event: "consent.recorded", consent_id, user_id, timestamp}
            +→ Background publisher: Send consent.recorded event
            |
            └→ Response: { consent_id, consent_version: 1 }
       |
       └→ Client: Store consent_id (user can now enroll voices)
```

**Data Ownership:**
- Consent Service owns: consent_records, consent_history, consent_status
- Voice Profile Service references: consent_id (validates via Consent Service API)

**Synchronous Path:** Consent Form → POST /consent/record → Response with consent_id
**Async Events:** consent.recorded published (consumed by Audit Service)

---

## Flow 3: Voice Enrollment (Async, Inference-Worker-Driven)

### Step 1: Client Uploads Enrollment Samples

```
User (Client)
  |
  +→ Prepares audio samples (quality and format per approved requirements)
  |
  +→ API Gateway
       |
       +→ Artifact Service: POST /artifacts/upload
            {
              artifact_type: "sample",
              user_id: from_bearer_token,
              file_content: <binary audio>
            }
            |
            +→ Validate user_id ownership
            +→ Validate audio format/duration/quality
            +→ Store in user-isolated namespace
            +→ Generate artifact_id (opaque, no storage path exposed)
            +→ Create artifact_metadata
            +→ Insert outbox record: {event: "artifact.stored", artifact_id, user_id}
            +→ Background publisher: Send artifact.stored event
            |
            └→ Response: { artifact_id }  # Only artifact_id returned, never storage path
       |
       └→ Client: Receives artifact_id
```

### Step 2: Client Creates Voice Profile (Non-Terminal State)

```
User (Client)
  |
  +→ API Gateway
       |
       +→ Voice Profile Service: POST /voices
            {
              user_id: from_bearer_token,
              voice_name: "My Professional Voice",
              consent_id: <from previous consent flow>,
              sample_artifact_ids: [artifact_id_1, artifact_id_2, ...]
            }
            |
            +→ Validate user ownership
            +→ Call Consent Service: GET /consent/validate/{consent_id}
            |   Confirm consent is active
            |
            +→ Create voice_profile record (enrollment_status: PENDING)
            +→ Transition to ENROLLING state
            +→ Insert outbox record: {event: "voice_profile.enroll", profile_id, user_id, sample_artifact_ids}
            +→ Background publisher: Send voice_profile.enroll (WORK COMMAND) to work broker
            |
            └→ Response: { profile_id, enrollment_status: ENROLLING }
       |
       └→ Client: Profile created, waiting for enrollment to complete
```

### Step 3: Inference Worker Processes Enrollment (Async)

```
Message Broker (work topic)
  |
  +→ Inference Worker (consumes voice_profile.enroll WORK COMMAND)
       |
       +→ Retrieve enrollment work from message
       |   (profile_id, user_id, sample_artifact_ids)
       |
       +→ Validate profile still in ENROLLING state (call Voice Profile Service)
       |
       +→ For each sample artifact:
       |   ├→ Call Artifact Service: GET /artifacts/{artifact_id}/metadata
       |   ├→ Download sample audio from signed URL (Artifact Service provides)
       |   └→ Validate sample quality
       |
       +→ Extract speaker embeddings/features from samples
       |
       +→ Call AI Gateway: POST /ai/infer
       |   {
       |     operation: "enroll",
       |     profile_id: profile_id,
       |     samples: <sample_features>
       |   }
       |   |
       |   +→ AI Gateway performs model-specific enrollment
       |   +→ Returns provider-specific speaker_id, conditioning metadata
       |
       +→ AI Gateway stores: speaker_conditioning (profile_id, model_id, model_speaker_id, conditioning_reference)
       |
       +→ Call Voice Profile Service: PATCH /voices/{profile_id}/status
       |   {
       |     status: "ENROLLED",
       |     model_version: "v2.1",
       |     quality_score: 0.92
       |   }
       |   |
       |   +→ Voice Profile Service transitions ENROLLING → ENROLLED
       |   +→ Voice Profile Service inserts outbox: {event: "voice_profile.enrolled", profile_id, ...}
       |   +→ Background publisher: Send voice_profile.enrolled DOMAIN EVENT
       |
       └→ Message Broker: Acknowledge work item
```

**If Enrollment Fails:**

```
Inference Worker
  |
  +→ Catches error (invalid samples, model inference failure)
  |
  +→ Call Voice Profile Service: PATCH /voices/{profile_id}/status
       {
         status: "FAILED",
         error_reason: "insufficient_sample_quality | model_inference_error"
       }
       |
       +→ Voice Profile Service transitions ENROLLING → FAILED
       +→ Voice Profile Service inserts outbox: {event: "voice_profile.enrollment_failed", profile_id, ...}
       +→ Background publisher: Send voice_profile.enrollment_failed DOMAIN EVENT
       |
       └→ Message Broker: Acknowledge work item (do not retry)
```

**Data Ownership:**
- Voice Profile Service owns: profile lifecycle state
- Artifact Service owns: sample binary audio
- Inference Worker owns: execution and feature extraction
- AI Gateway owns: model-specific speaker conditioning

**Asynchronous Path:**
- voice_profile.enrollment_requested (WORK COMMAND to Inference Worker)
- voice_profile.enrolled OR voice_profile.enrollment_failed (DOMAIN EVENTS)

---

## Flow 4: Narration Submission and Quota Reservation

### User Submits Narration Job

```
User (Client)
  |
  +→ API Gateway
       |
       +→ Narration Orchestrator: POST /jobs
            {
              user_id: from_bearer_token,
              profile_id: <voice profile to use>,
              script: "In Hindi: नमस्ते दोस्त...",
              language: "hindi",
              generation_params: {
                speech_pace: 1.0,
                pause_strength: 0.5
              },
              idempotency_key: <client-generated UUID>
            }
            |
            +→ Validate user_id, profile_id ownership
            +→ Check idempotency: if idempotency_key exists, return cached response
            |
            +→ Call Voice Profile Service: GET /voices/validate/{profile_id}
            |   Confirm profile enrollment_status = ENROLLED
            |
            +→ Estimate duration and cost
            |
            +→ Call Usage & Policy Service: POST /quotas/reserve
            |   {
            |     user_id: user_id,
            |     estimated_duration_seconds: 120,
            |     estimated_cost_usd: 12.00
            |   }
            |   |
            |   +→ Usage & Policy atomically reserves quota/budget
            |   +→ Returns: { reservation_id: "res_xyz" }
            |   |
            |   └→ If reservation fails (quota/budget exceeded):
            |       Usage & Policy Service publishes: quota.exceeded or budget.exceeded
            |       Return: { status: 429, reason: "quota_exceeded" }
            |       Job is NOT created
            |
            +→ IF reservation succeeded:
            |   ├→ Create narration_job record (status: SUBMITTED)
            |   ├→ Store: reservation_id, idempotency_key, request snapshot
            |   ├→ Insert outbox records:
            |   |   - {event: "narration_job.submitted", job_id, profile_id, ...}
            |   |   - {command: "narration.generate", job_id, ...} (WORK COMMAND)
            |   ├→ Background publisher: Send narration.generate to work broker
            |   ├→ Background publisher: Send narration_job.submitted to audit broker
            |   |
            |   └→ Response: { job_id, status: SUBMITTED, polling_url }
       |
       └→ Client: Poll job status OR subscribe to completion event
```

**Quota Failure Path:**

```
Usage & Policy Service
  |
  +→ Check user's quota: remaining_quota < requested_duration
  +→ Check budget: estimated_cost > remaining_budget
  +→ Check kill-switch enabled
  |
  +→ If any check fails:
       ├→ Return: { reservation_result: FAILED, reason: "quota_exceeded" or "budget_exceeded" }
       ├→ Publish event: quota.exceeded or budget.exceeded
       └→ NO reservation_id returned; NO reservation made
```

**Data Ownership:**
- Narration Orchestrator owns: job lifecycle, reservation coordination
- Voice Profile Service owns: profile validation
- Usage & Policy Service owns: quota/budget reservation (atomic)

**Synchronous Path:** Profile validation → Quota reservation → Job creation
**Async Events:** narration_job.submitted (WORK COMMAND to Inference Worker)

---

## Flow 5: Narration Inference and Execution

### Inference Worker Processes Job

```
Message Broker (work topic)
  |
  +→ Inference Worker (consumes narration.generate WORK COMMAND)
       |
       +→ Retrieve job_id from work command
       |
       +→ Call Narration Orchestrator: GET /jobs/{job_id}/work-item
       |   Returns: { job_id, script, profile_id, generation_params, ... }
       |
       +→ Call Voice Profile Service: GET /voices/validate/{profile_id}
       |   Confirm profile still ENROLLED (not revoked mid-flight)
       |   If revoked: Call Narration Orchestrator: POST /jobs/{job_id}/fail
       |              (Worker does NOT publish job events; Orchestrator does)
       |
       +→ Linguistic Chunking:
       |   Split script into manageable chunks
       |   (chunk size and boundaries per approved requirements)
       |
       +→ For each chunk:
       |   |
       |   +→ Call AI Gateway: POST /ai/infer
       |   |   {
       |   |     operation: "narration",
       |   |     profile_id: profile_id,
       |   |     text: chunk,
       |   |     generation_params: { speech_pace, pause_strength }
       |   |   }
       |   |   |
       |   |   +→ AI Gateway:
       |   |   |   Retrieve model-specific speaker conditioning
       |   |   |   Invoke model provider with text + speaker_id
       |   |   |   Return: audio_bytes
       |   |   |
       |   |   └→ Response: { audio_bytes, duration_seconds }
       |   |
       |   +→ Handle inference failures (retry up to N times with backoff)
       |   +→ Store chunk audio to assembly buffer
       |
       +→ Audio Assembly:
       |   Concatenate chunks into seamless output
       |   Validate output format and duration
       |
       +→ Call Artifact Service: POST /artifacts/upload
       |   {
       |     artifact_type: "generated_audio",
       |     user_id: job.user_id,
       |     file_content: <assembled_audio_bytes>
       |   }
       |   |
       |   +→ Store in user-isolated namespace
       |   +→ Generate artifact_id (opaque)
       |   +→ Insert outbox: {event: "artifact.stored", artifact_id, ...}
       |   +→ Background publisher: Send artifact.stored event
       |   |
       |   └→ Response: { artifact_id }
       |
       +→ Call Narration Orchestrator: POST /jobs/{job_id}/complete
       |   {
       |     status: "COMPLETED",
       |     output_artifact_id: artifact_id,
       |     duration_seconds: <actual_output_duration>,
       |     actual_cost_usd: <cost_from_AI_gateway>
       |   }
       |   |
       |   +→ Narration Orchestrator (Worker does NOT publish events; Orchestrator owns this):
       |   |   - Update job status: COMPLETED
       |   |   - Store output_artifact_id
       |   |   - Call Usage & Policy Service: POST /quotas/commit-usage
       |   |     {
       |   |       reservation_id: res_xyz,
       |   |       actual_usage: duration_seconds,
       |   |       actual_cost: actual_cost_usd
       |   |     }
       |   |   - Usage & Policy commits actual cost to reservation (idempotent)
       |   |   - Narration Orchestrator inserts outbox: {event: "narration_job.completed", job_id, ...}
       |   |   - Background publisher: Send narration_job.completed event
       |   |
       |   └→ Response: { job_id, status: COMPLETED }
       |
       └→ Message Broker: Acknowledge work item
```

**If Inference Fails:**

```
Inference Worker
  |
  +→ Catches inference error after retries exhausted
  |
  +→ Call Narration Orchestrator: POST /jobs/{job_id}/fail
       {
         status: "FAILED",
         failure_reason: "inference_failed | cost_exceeds_budget",
         error_message: "Model inference timeout after 3 retries"
       }
       |
       +→ Narration Orchestrator (owns job lifecycle):
       |   - Update job status: FAILED
       |   - Call Usage & Policy Service: POST /quotas/release-reservation
       |     {
       |       reservation_id: res_xyz
       |     }
       |   - Usage & Policy releases unused quota (idempotent)
       |   - Delete partial artifacts via Artifact Service cleanup
       |   - Insert outbox: {event: "narration_job.failed", job_id, ...}
       |   - Background publisher: Send narration_job.failed event
       |
       └→ Response: { job_id, status: FAILED }

+→ Message Broker: Acknowledge work item (do not retry; Orchestrator retries workflow)
```

**Data Ownership:**
- Inference Worker owns: execution, chunking, assembly, cleanup
- Narration Orchestrator owns: job state, publication of job lifecycle events
- Usage & Policy owns: actual cost commitment
- Artifact Service owns: binary storage
- AI Gateway owns: model inference

**Asynchronous Path:** narration.generate (WORK COMMAND) → Inference execution → narration_job.completed/failed (DOMAIN EVENTS published by Orchestrator)

---

## Flow 6: Narration Completion and Download

### User Polls Job Status

```
User (Client)
  |
  +→ Periodically calls: API Gateway
       |
       +→ Narration Orchestrator: GET /jobs/{job_id}
            |
            +→ Validate user_id ownership
            +→ Return job status and details
            |
            └→ Response: { job_id, status: SUBMITTED|PROCESSING|COMPLETED|FAILED|CANCELLED, ... }
       |
       └→ Client: If status == COMPLETED, request download
```

### Download Generated Audio

```
User (Client)
  |
  +→ Narration Orchestrator: GET /jobs/{job_id}
       Response: { ..., output_artifact_id: "art_xyz" }
  |
  +→ API Gateway
       |
       +→ Artifact Service: GET /artifacts/{artifact_id}/download-url
            {
              user_id: from_bearer_token
            }
            |
            +→ Validate user ownership (user_id must match artifact.user_id)
            +→ Validate artifact type is "generated_audio"
            +→ Generate time-limited signed URL (expires in 1 hour)
            +→ Insert outbox: {event: "artifact.accessed", artifact_id, access_type: "download"}
            +→ Background publisher: Send artifact.accessed event
            |
            └→ Response: { download_url: "https://storage.../art_xyz?token=<signed>" }
       |
       └→ Client: Use signed URL to download audio (direct to storage, not through API)
```

**Data Ownership:**
- Narration Orchestrator owns: job state and output_artifact_id reference
- Artifact Service owns: binary audio and signed access control

**Synchronous Path:** Status Poll → Download URL Request → Signed URL → Direct download

---

## Flow 7: Voice Profile Revocation and Cascade

### User Initiates Profile Revocation

```
User (Client)
  |
  +→ API Gateway
       |
       +→ Voice Profile Service: DELETE /voices/{profile_id}
            {
              user_id: from_bearer_token
            }
            |
            +→ Validate user_id ownership
            +→ Transition profile status: → REVOKED
            +→ Insert outbox: {event: "voice_profile.revoked", profile_id, user_id, sample_artifact_ids}
            +→ Background publisher: Send voice_profile.revoked event
            |
            └→ Response: { profile_id, status: REVOKED }
       |
       └→ Client: Profile revoked
```

### Cascade 1: Narration Orchestrator Receives Event

```
Message Broker (event topic)
  |
  +→ Narration Orchestrator (consumes voice_profile.revoked)
       |
       +→ Query all jobs where profile_id == revoked_profile AND status IN [SUBMITTED, PROCESSING]
       +→ For each such job:
       |   ├→ Call Usage & Policy Service: POST /quotas/release-reservation
       |   |   { reservation_id: job.reservation_id }
       |   |   (restores quota on cancellation)
       |   |
       |   ├→ Update job status: CANCELLED
       |   ├→ Insert outbox: {event: "narration_job.cancelled", job_id, ...}
       |   └→ Background publisher: Send narration_job.cancelled event
       |
       └→ Continue processing next event
```

### Cascade 2: Artifact Service Receives Event

```
Message Broker (event topic)
  |
  +→ Artifact Service (consumes voice_profile.revoked)
       |
       +→ For each sample_artifact_id in voice_profile.revoked event:
       |   ├→ Call Artifact Service cleanup: DELETE artifact
       |   |   (Approved requirement: samples must be deleted on revocation)
       |   |
       |   └→ Insert outbox: {event: "artifact.deleted", artifact_id, ...}
       |       Background publisher: Send artifact.deleted event
       |
       └→ Continue processing
```

### Cascade 3: AI Gateway Receives Event

```
Message Broker (event topic)
  |
  +→ AI Gateway (consumes voice_profile.revoked)
       |
       +→ Query speaker_conditioning table for profile_id
       +→ For each model-specific conditioning record:
       |   ├→ Purge provider-side speaker_id, cached inference artifacts
       |   ├→ Delete local speaker_conditioning record
       |   └→ Publish: (internal cleanup only, may not generate event)
       |
       └→ Continue processing
```

**Cascade Guarantees:**
- All cascades triggered by single voice_profile.revoked event
- Cascades proceed in parallel (eventual consistency)
- Each service idempotent (multiple deliveries of same event handled safely)

---

## Flow 8: Quota and Budget Rejection

### Job Submission Fails Quota Check

```
User (Client)
  |
  +→ API Gateway
       |
       +→ Narration Orchestrator: POST /jobs (submit narration)
            |
            +→ Call Usage & Policy Service: POST /quotas/reserve
            |   (estimate: user's remaining quota: 100s; job requests 300s)
            |
            +→ Usage & Policy returns: { reservation_result: FAILED, reason: "quota_exceeded" }
            |
            +→ Publish event: quota.exceeded
            |
            └→ Response: { status: 429, reason: "quota_exceeded", remaining_quota: 100 }
       |
       └→ Client: Display error "You have 100s remaining; this job requires 300s"
```

### Job Submission Fails Budget Check

```
User (Client)
  |
  +→ API Gateway
       |
       +→ Narration Orchestrator: POST /jobs (submit narration)
            |
            +→ Call Usage & Policy Service: POST /quotas/reserve
            |   (estimate cost: $12.00; monthly budget: $10, spent: $8.50, remaining: $1.50)
            |
            +→ Usage & Policy returns: { reservation_result: FAILED, reason: "budget_exceeded" }
            |
            +→ Publish event: budget.exceeded
            |
            └→ Response: { status: 429, reason: "budget_exceeded", monthly_limit: 10, spent: 8.50, estimated_cost: 12.00 }
       |
       └→ Client: Display error "Monthly budget exceeded"
```

**Rejection Timing:** Before job created; job never transitions to SUBMITTED

---

## Cross-Service Guarantees

### Idempotency
Every client request (registration, consent, job submission) includes `idempotency_key`.
- Duplicate request = duplicate idempotency_key → same response (no duplicate side effects)
- Orchestrator caches idempotency responses for configured TTL (e.g., 24 hours)

### Eventual Consistency
All async events use at-least-once delivery; consuming services must be idempotent.
- Example: voice_profile.revoked may be published twice; Narration Orchestrator checks job status first, only cancels if not already cancelled

### Data Isolation
All multi-tenant operations enforce user_id ownership.
- Voice Profile Service: User can only access their own profiles
- Artifact Service: User can only access their own artifacts
- Narration Orchestrator: User can only access their own jobs

### Transactional Outbox
State changes include outbox record in same database transaction:
1. Update business state (e.g., update job status)
2. Insert outbox record in same transaction
3. Commit atomically
4. Background publisher polls outbox, sends to broker, marks as published
5. No "database commit succeeds but event fails" failures

### Non-Blocking Audit
Audit Service may be down; workflows must not block on audit.
- Job completion succeeds even if Audit Service unavailable
- Audit event is eventually retried and consumed asynchronously

---
