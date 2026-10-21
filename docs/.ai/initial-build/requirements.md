# Requirements — initial-build

Every item ends with one source label.

- [User: brief] = stated by the user
- [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400] = established by inspecting the repository during this capture
- [User: Q1] = answers to Clarification Q1 below
- [User: Q2] = product-scope correction and revision instructions (see Clarification Log)

## Goal
Deliver the initial product-focused requirements for Voice Narration Studio (M0 initial-build) describing the user-facing, multi-user, Hindi-first narration product to be implemented in the next milestones. This artifact captures authoritative requirements for review and M0 gate decisions and does not authorize plans, implementation, or provisioning. [User: Q2]

## Status
Approved by avinash2196 on 2026-10-19. This artifact does not authorize any Plan, contract, Implementation Plan, test, code change, or cloud provisioning.

## Relationship to Product-Level Requirements
This work-item revises the product scope to a general-purpose, multi-user narration platform while preserving the product-level baseline in voice_narration_PDD_requirements.md as the primary source for functional and nonfunctional expectations. Any change to approved product-level statements will be recorded and confirmed explicitly. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400; User: Q2]

## Repository-Confirmed Facts
- Primary product baseline exists at voice_narration_PDD_requirements.md and defines MVP scope, non-goals, functional requirements and NFRs used below. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- The baseline explicitly references Windows development and an optional Cloud Run L4 GPU deployment path. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]

## Requirements
(Only requirements explicitly provided by the repository or the user are recorded below.)

User accounts, roles and isolation
- R-ACCT-001 P0: Support open registration with email verification; provide two MVP roles: User and Administrator. [User: Q2]
- R-ACCT-002 P0: Multi-user architecture with strict user-level isolation: each user's accounts, voice profiles, recordings, jobs, and private libraries must be access-controlled and logically isolated. [User: Q2]
- R-ACCT-003 P0: Each user has a private voice library and narration history; Administrators manage system-level settings but cannot read private voice data without explicit authorization. [User: Q2]

Consent and enrollment
- R-CONS-001 P0: Require explicit authorization and consent before any voice enrollment; record consent event details (account, timestamp, consent text/version, consenting identity). [User: Q2; Repo: FR-002]
- R-CONS-002 P0: For assisted recording, require documented authorization from the enrolled voice owner before using or persisting samples. [User: Q2]

Voice enrollment and profiles
- FR-010 P0: Accept browser microphone recordings or uploaded WAV/MP3/M4A; validate formats, duration and size limits during architecture. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-011 P0: Provide recording guidance and sample quality checks with actionable feedback (clipping, silence, SNR, speech presence). [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-012 P0: Save a reusable voice profile with metadata including consent reference and model/version; users own their profiles. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400; User: Q2]
- R-REV-001 P0: Voice-profile revocation and deletion: when a user requests deletion or revokes consent, the system must remove profile metadata, original samples, derived embeddings/artifacts, and disallow future synthesis from that profile. A non-deletable audit record of the deletion event (metadata only) may be retained per admin-configured retention policy. [User: Q2; Repo: FR-003]

Script preparation and generation
- FR-020 P0: Support UTF-8 Devanagari Hindi and English text input; preserve punctuation and line breaks. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-022 P0: Asynchronous job model with states (queued, preparing, running, post-processing, completed, failed, cancelled). [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-024 P0: Allow preview, regenerate and download WAV; MP3 export only if encoder/licensing permits. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-025 P0: Chunk long scripts at linguistic boundaries, never mid-word; use punctuation/line breaks as pause cues. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-023 P0: Preserve a script snapshot and job metadata for every generation job: selected profile, model version, generation parameters, output reference, timestamps, and actionable error details. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- R-EXP-001 P0: Provide basic expressive controls (pause strength and speech pace) in the UI within tested safe ranges; controls must be model-gated and only exposed when the selected model supports them. Advanced emotion controls remain P1. [User: Q3]
- R-GEN-001 P0: Configurable per-user generation quotas, rate limits and concurrency limits; administrators can adjust system-wide and per-user limits. [User: Q2]
- R-WORK-001 P0: Core generation workflow (verifiable): authenticated user → select authorized voice profile → supply Hindi/English script → submit generation job (record job snapshot: profile id, model version, params, idempotency key) → job executes through defined states → preview available → user may download or request deletion. [Derived from FR-022, FR-024, FR-012, FR-023]

Operational requirements
- FR-040 P0: Support Windows developer setup, local API/UI development, mocked inference and a containerized inference worker. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-041 P0: Model inference behind an interface so backend models can be swapped without changing UI/business APIs. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-042 P0: Configurable local and cloud inference; do not assume local CUDA availability. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-044 P0: Bound concurrency, job duration, retries, script length and spend; expose cost/usage view and operator-configurable budget/kill switch. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- FR-045 P0: Durable job state and idempotent submission: submissions must accept an idempotency key and persist job state so retries do not produce duplicate final artifacts or duplicate billing. Job state must be durable across restarts and crashes. [Repo: FR-045 — restored meaning from product baseline]
- FR-046 P0: Cloud secrets in managed secret storage; private object storage; encryption in transit/at rest; least-privilege identities; signed/authorized downloads. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]

Retention and data lifecycle
- R-RET-001 P0: Separate retention policies for voice profiles, original voice samples, generated audio, and consent/audit records; these policies and deletion workflows must be configurable and auditable. [User: Q2]
- R-RET-002 P0: Default retention values (from Clarification Q1): generated audio 30 days; profiles and consent records retention to be decided and configured by admin. [User: Q1; User: Q2]
- R-DEL-001 P0: Post-deletion behavior: upon profile deletion or consent revocation, original audio files and derived embeddings/artifacts must be purged from object storage and model stores; any cached inference artifacts that permit reconstruction of voice identity must be removed. Audit metadata (account id, deletion timestamp, operator id) may be retained per admin-configured audit-retention policy. [Derived from R-REV-001; User: Q2]

Nonfunctional targets and governance
- NFR-008 Cost: show measured per-run compute and storage cost; no always-on GPU without explicit approval. Budget target: $20/month for initial deployment, treated as an operational target not a guarantee. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400; User: Q1; User: Q2]
- R-EVAL-001 P0: Define a measurable voice-cloning evaluation protocol covering speaker identity, pronunciation, continuity, and expressive narration; baseline tests and acceptance metrics to be specified in M1. [User: Q2]
- R-LIC-001 P0: Commercial-use licensing verification is a mandatory release gate; no model or weights deploy until license/output-use is approved with citation. [Repo: Gate G1; User: Q2]

Explicit Exclusions
- No video editor, automatic YouTube upload, music generation, celebrity/public-figure cloning, mobile-native app, or real-time voice conversion in MVP. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]

## Operational Characteristics
| Characteristic | Answer | Source |
|----------------|--------|--------|
| Initial access scope | Open registration with email verification | [User: Q2]
| Local copies policy | Allow local Windows copies; primary storage in cloud bucket | [User: Q1]
| Max output duration | 3000 seconds (50 minutes) — absolute system maximum; requests must also satisfy per-user quotas, resource limits, and budget enforcement. | [User: Q1; User: Q2]
| Output retention | Generated audio: 30 days (default); profiles/consent: configurable by admin (see R-RET-001) | [User: Q1; User: Q2]
| Bilingual MVP | Hindi and English (Hindi as primary quality benchmark) | [User: Q2; Repo]
| Monthly cloud budget | $20 USD (operational target) | [User: Q1; User: Q2]
| Acceptable cold-start wait | 300 seconds (subject to feasibility) | [User: Q1]
| Consent when assisted recording | Explicit authorization from voice owner required before using/persisting samples; consent events must be recorded. | [User: Q2]

## Decisions Deferred to Later Milestones
- Final model selection and license approvals (Gate G1) remain deferred to M1. [Repo: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md:1-400]
- Exact retention durations for profiles and consent/audit records deferred to admin-configured policy in M2. [User: Q2]

## Non-Blocking Decisions
- Per-line pronunciation overrides and advanced emotion presets remain P1/P2 features (not required for MVP). [Repo]

## Acceptance Criteria
(Each acceptance criterion maps to one or more P0 requirements above; tests are to be specified in M1/M2 as required.)

- AC-ACCT-001 (Account isolation): Given two separate User accounts, A and B, when A attempts to list or access B's voice profiles, samples, or narration jobs, the system denies access (403) and no audio content is exposed. [Verifies R-ACCT-002, R-ACCT-003]

- AC-CONS-001 (Consent recording): When a user enrolls a voice profile, the system records a consent event containing account id, timestamp, consent text/version, and consenting identity; the consent record is immutable and queryable by administrators for auditing. [Verifies R-CONS-001]

- AC-ENR-001 (Enrollment): Enrollments accept only validated audio formats; enrollment completes only if quality checks pass or user explicitly overrides after informed warning; resulting voice profile metadata includes model/version, sample references, consent reference and enrollment status. [Verifies FR-010, FR-011, FR-012]

- AC-GEN-001 (Generation core workflow): An authenticated User selects an authorized voice profile, submits a script and idempotency key, receives a job id, and the job progresses through queued→running→completed (or failed). On completion, a preview URL and download link (signed, authorized) are available to the submitting user only. Retries with same idempotency key do not create duplicate final audio artifacts. [Verifies R-WORK-001, FR-022, FR-045, FR-024]

- AC-HIST-001 (History and audit): Each user has a queryable history listing past narrations with immutable metadata (profile id, model version, params, timestamps) and authorized access limited to the owner and permitted admins. [Verifies R-ACCT-003, FR-023]

- AC-RET-001 (Deletion and revocation): When a user deletes a profile or revokes consent, original samples, derived embeddings, and generated audio associated with the profile are removed from primary object storage and model stores within a bounded window (configurable, default 24 hours). Audit metadata (account id, deletion timestamp, operator id) is retained per admin-configured retention. The system must reject all future generation requests using the deleted profile. [Verifies R-REV-001, R-DEL-001]

- AC-SEC-001 (Secrets and data protection): Secrets are stored in managed secret storage; object storage enforces signed downloads; all data in transit and at rest is encrypted; access follows least privilege. [Verifies FR-046]

- AC-QUOTA-001 (Quotas and budget enforcement): Per-user quotas, rate limits and concurrency caps are enforced at submission time; administrative controls produce alerts when forecasted monthly spend exceeds $20 target; an operator-configurable kill switch prevents execution when configured spend thresholds are reached. [Verifies R-GEN-001, FR-044, NFR-008]

- AC-LIC-001 (Licensing gate): Before enabling any model for production use, a model evaluation artifact exists documenting exact source URL, license/weights permissions, and explicit approval by an Administrator; system prevents enabling models without such approval. [Verifies R-LIC-001]

- AC-EXP-001 (Expressive controls): The UI exposes pause strength and speech pace controls within tested safe ranges; when used, generated audio reflects the adjusted pause and pace without breaking voice identity. Controls are available only when the selected model supports them and pass model-feasibility validation in M1; advanced emotion controls remain P1 until validated. [Verifies basic expressive controls P0]

## Clarification Log
| Q | Question | Answer |
|---|----------|--------|
| 1 | Operational characteristics and policies required by requirements-analysis (access scope, local storage, max output duration, retention, bilingual support, budget, cold-start tolerance, consent flow when assisted). | Access: open registration/simple page, no strict limits; Local copies: allow local Windows copies, primary cloud bucket; Max duration: 3000s; Retention: 30 days; Bilingual: Hindi+English; Budget: $20 USD/month; Cold-start tolerated up to 300s; Consent: generic user-provided consent allowed (user asked to relax parent-only requirement). [User: Q1] |
| 2 | Product-scope correction and required revisions provided by user (replace parent personas, multi-user requirements, roles, quotas, retention separation, explicit consent, etc.). | Revised to general-purpose multi-user platform; open registration + email verification; roles: User and Administrator; strict user-level isolation; per-user private voice libraries and histories; explicit consent required for enrollment and assisted recording; per-user quotas/rate limits; separate retention policies; Hindi primary benchmark; 3000s cap preserved; $20/month target preserved; measurable evaluation protocol required; commercial-use licensing verification mandatory gate. [User: Q2] |
| 3 | Should basic expressive narration controls (pause strength, speech pace) be included in MVP (P0) or kept as P1? | P0 — Basic expressive controls included in MVP, subject to model feasibility and validation; advanced emotion controls remain P1. [User: Q3] |
| 4 | Confirm the 3000s (50-minute) maximum: should it be a hard system limit, or subordinate to per-user quotas and budget enforcement? | subordinate_to_quotas — 3000s is the absolute system maximum but requests must also satisfy per-user quotas, resource limits, and operational budget constraints. [User: Q4] |

## Provenance Check
- Every requirement and operational answer above carries a source label (User Q1/Q2 or Repo citations).
- `Derived` items: acceptance criteria are derived from tracked FR/NFR/R- items above and therefore trace to those items.
- `Left to` items: model selection and license approval (Gate G1) are left to M1; exact retention durations for profiles and consent/audit records left to admin-configured policy in M2.
- `Repo` citations verified against the file at C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\voice_narration_PDD_requirements.md during this capture.
- Requirements without an acceptance criterion: none (all listed P0 items now map to at least one acceptance criterion above). Where some items are intentionally deferred (M1/M2), that deferral is recorded.

---

