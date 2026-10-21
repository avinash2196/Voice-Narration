# API Contract — initial-build

## Baseline
- Approved Requirements: docs/.ai/initial-build/requirements.md (Approved by avinash2196 on 2026-10-19)
- Approved Plan: docs/.ai/initial-build/Plan.md (Approved by avinash2196 on 2026-10-19T11:37:33Z)
- Plan records CONTRACT as Milestone 1 with no predecessors; this contract is the CONTRACT deliverable
- Contract Review Status: Pending approval

## Changes in This Work Item
CONTRACT milestone defines the complete API surface for:
- User registration and email verification (R-ACCT-001)
- Consent recording and voice enrollment (R-CONS-001)
- Voice profile lifecycle operations (FR-012, FR-003)
- Narration job submission, query, and retrieval (FR-022, FR-023, FR-024)
- Idempotent job handling (FR-045)
- Secure audio download with signed URLs (FR-046)
- Quota and rate-limit enforcement (R-GEN-001)

## Contract Overview

The Voice Narration Studio API is a REST API providing authenticated, role-based access to voice profiles, narration jobs, and audio retrieval. All requests require Bearer token authentication. Two MVP roles are supported: User and Administrator.

**Base URL:** http://localhost:5000/api/v1

**Authentication:** Bearer token in Authorization header

**Idempotency:** POST requests accept idempotency-key header for safe retries

## Endpoints

### Authentication

**POST /auth/register** - Register new account  
**POST /auth/verify-email** - Verify email with token  
**POST /auth/login** - Authenticate and get bearer token

### Voice Profiles

**POST /voices** - Enroll voice profile with audio sample and consent  
**GET /voices** - List user's voice profiles  
**DELETE /voices/{profile_id}** - Revoke and delete voice profile (cascades to samples/embeddings)

### Narration Jobs

**POST /jobs** - Submit generation job with idempotency-key support  
**GET /jobs/{job_id}** - Query job status and metadata  
**GET /jobs** - List user's jobs with pagination  
**POST /jobs/{job_id}/cancel** - Cancel queued/preparing job

### Audio Retrieval

**GET /jobs/{job_id}/preview** - Get signed preview URL (short-lived, user-tied)  
**GET /jobs/{job_id}/download** - Get signed download URL (WAV or MP3)

### Quotas

**GET /users/me/quota** - Get usage and quota limits

## Authentication & Authorization

**Registration:** POST /auth/register with email, password, name → verification email sent  
**Email Verification:** POST /auth/verify-email with token → bearer token issued  
**Login:** POST /auth/login with email/password → bearer token issued  
**Token Format:** JWT-style bearer token in Authorization header  
**Token Expiry:** 24 hours (configurable)

**Roles:**
- User: Can enroll voices, submit jobs, access own profiles/jobs/audio
- Administrator: Can view system activity, configure quotas, approve models, manage retention

**Access Control:**
- Users cannot access other users' profiles, jobs, or audio (403 Forbidden)
- Profile deletion is owner-only and permanent
- Job status and download URLs are owner-restricted with signed tokens

## Voice Profile Lifecycle

**Enroll (POST /voices):**
- Request: voice_name, audio_file (WAV/MP3/M4A ≤30MB), consent_text, consent_version
- Response: profile_id, model_version, enrollment_status, consent_reference, quality_score
- Consent: Immutable event recorded with account_id, timestamp, consent_text/version, consenting_identity

**List (GET /voices):**
- Response: Array of profiles with profile_id, voice_name, model_version, enrollment_status, quality_score

**Delete (DELETE /voices/{profile_id}):**
- Response: 204 No Content
- Cascades: Original samples purged, embeddings deleted, derived artifacts removed, profile marked non-recoverable
- Audit: Deletion event recorded (account_id, deletion_timestamp, operator_id)
- Enforcement: All future generation requests using this profile rejected (404 or 403)

## Narration Job Lifecycle

**Submit (POST /jobs):**
- Request: profile_id, script (UTF-8 Hindi/English), language ("hi"/"en"), idempotency_key (UUID, optional), expressive_controls (pause_strength, speech_pace)
- Response: job_id, status="queued", script_snapshot, model_version, generation_params, idempotency_key, created_at, output_url=null, error_details=null
- Status 202 Accepted

**Query (GET /jobs/{job_id}):**
- Response: Complete job metadata including status, script_snapshot, model_version, generation_params, created_at, updated_at, output_url, preview_url, error_details, duration_seconds, estimated_cost_usd

**Job States:**
- queued → preparing → running → post_processing → completed (or failed/cancelled)

**List (GET /jobs):**
- Query params: status, limit (default 20, max 100), offset
- Response: Array of jobs with paginated results

**Cancel (POST /jobs/{job_id}/cancel):**
- Response: 204 No Content (only works for queued/preparing jobs)

## Audio Retrieval

**Preview (GET /jobs/{job_id}/preview):**
- Response: preview_url (signed, 1-hour expiry), format, duration_seconds, sample_rate_hz, expires_at
- Authorization: User-tied, short-lived token; cannot be shared or reused after expiration

**Download (GET /jobs/{job_id}/download):**
- Query param: format (wav default, mp3 if encoder/licensing permits)
- Response: download_url (signed, 1-hour expiry), format, file_size_bytes, expires_at
- Authorization: User-tied, signed download URL; backend enforces user ownership before serving

## Idempotency

**Idempotency-Key Header:**
- Optional UUID header on POST /jobs
- Same key + same request body → same response (no duplicate job created)
- Same key + different body → 409 Conflict
- Key validity: 24 hours
- Benefit: Retries do not create duplicate final audio artifacts or duplicate billing

## Quotas & Rate Limiting

**Per-User Quotas:**
- Daily generation limit (default configurable by admin)
- Concurrency limit (default configurable)
- Monthly budget cap (default $20 USD)
- Enforcement: At submission time (POST /jobs); 403 Forbidden if exceeded

**Rate Limiting:**
- Per-user limit: 1000 requests per hour (configurable)
- Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
- Exceeded: 429 Too Many Requests with Retry-After header

**Quota Visibility:**
- GET /users/me/quota returns current usage, remaining, reset_at, budget status

## Error Handling

**Standard Error Response:**
```json
{
  "error_code": "ERROR_TYPE",
  "error_message": "Human-readable message",
  "error_details": { "field": "...", "constraint": "..." },
  "request_id": "req_xyz123",
  "timestamp": "2026-10-19T11:52:00Z"
}
```

**Status Codes:**
- 200 OK: Success (GET)
- 201 Created: Resource created (POST)
- 202 Accepted: Async job queued (POST /jobs)
- 204 No Content: Success, no body (DELETE)
- 400 Bad Request: Invalid input (INVALID_REQUEST)
- 401 Unauthorized: Missing/invalid token (UNAUTHORIZED)
- 403 Forbidden: No permission or quota exceeded (FORBIDDEN)
- 404 Not Found: Resource not found (NOT_FOUND)
- 409 Conflict: Idempotency conflict or duplicate (CONFLICT)
- 429 Too Many Requests: Rate limit or quota exceeded (TOO_MANY_REQUESTS)
- 500 Internal Server Error: Server error (INTERNAL_ERROR)

## Security & Data Protection

**Transit:** All data encrypted (TLS 1.2+)  
**At-Rest:** Backend storage enforces encryption  
**Secrets:** Never exposed in API responses; managed by backend  
**Least-Privilege:** API does not expose internal credentials  
**Signed Downloads:** Short-lived tokens prevent unauthorized audio access  
**Consent Immutability:** Consent events are permanent and queryable by admins  
**Audit Trail:** Deletions, access, role changes logged with timestamp and operator_id  

## Contract Completeness Checklist

| Requirement | Verified |
|---|---|
| Endpoints defined? | Yes — 13 endpoints specified |
| Request/response formats? | Yes — JSON with exact schemas |
| Authentication scheme? | Yes — Bearer token with email verification gate |
| Authorization rules? | Yes — Role-based (User/Admin) with ownership checks |
| Idempotency? | Yes — Idempotency-Key header for safe retries; 24h validity |
| Error handling? | Yes — Standard HTTP codes + error_code/message/details |
| Rate limiting? | Yes — X-RateLimit headers; 1000 req/hour configurable |
| Quota enforcement? | Yes — Daily/concurrency/budget caps; 403 when exceeded |
| Voice lifecycle? | Yes — Enroll → List → Delete (cascades to samples/embeddings) |
| Job lifecycle? | Yes — Submit → Query → Download; states: queued→preparing→running→post_processing→completed/failed/cancelled |
| Audio security? | Yes — Signed URLs, short-lived tokens, user-tied downloads |
| Consent recording? | Yes — Immutable events with account_id/timestamp/operator_id |
| Profile deletion? | Yes — Cascades to samples/embeddings; audit record retained separately |
| Traceability? | Yes — Every endpoint traces to approved requirement (FR-020, FR-022, FR-023, FR-024, FR-045, FR-046, R-ACCT-001, R-CONS-001, R-GEN-001) |

## Decisions Resolved

| Decision | Value | Source |
|---|---|---|
| Authentication scheme | Bearer token (JWT-style) with email verification | R-ACCT-001 |
| Role model | User (owner), Administrator (system config) | R-ACCT-001 |
| Idempotency | Idempotency-Key header; 24h validity; same key+body=same response | FR-045 |
| Quota enforcement point | Submission time (POST /jobs); 403 Forbidden when exceeded | R-GEN-001 |
| Audio download | Signed pre-signed URLs with short-lived tokens (1h default) | FR-046 |
| Consent | Immutable event with account_id/timestamp/text_version/operator_id; queryable by admins | R-CONS-001 |
| Profile deletion | Cascades to samples/embeddings/artifacts; audit record retained | R-REV-001 |
| Job states | queued→preparing→running→post_processing→completed/failed/cancelled | FR-022 |
| Language support | "hi" (Hindi), "en" (English); enforced at submission | FR-020 |
| Error format | Standard: error_code, error_message, error_details, request_id, timestamp | API design |

## Amendments
None (first version).

## Contract Review Status
Pending approval by Product/Administrator.

---
