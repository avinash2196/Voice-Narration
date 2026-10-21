# Plan — initial-build

Status: Approved by avinash2196 on 2026-10-19T11:37:33Z (requirements approved: docs/.ai/initial-build/requirements.md — Approved by avinash2196 on 2026-10-19)

Scope summary
- Deliver M0 plan that sequences work into CONTRACT, FOUNDATION, RED/GREEN milestone pairs and OTHER milestones to implement the approved requirements for Voice Narration Studio. This Plan keeps model selection and licensing decisions gated by explicit evaluation milestones and avoids provisioning cloud resources.

Milestones (ordered)

1. CONTRACT: API & External Contract (Pending)
   - Type: CONTRACT
   - Predecessors: none
   - Objective: Produce an authoritative API/external contract that defines authentication, registration/email-verification, voice-profile lifecycle, narration job creation/status, idempotency, authorized audio retrieval, and quota semantics. The CONTRACT artifact is authoritative for subsequent implementation milestones. It does not implement code.
   - Delivers: docs/.ai/initial-build/contract/API-Contract.md
   - Responsible for: FR-020, FR-022, FR-023, FR-024, FR-045, FR-046, R-ACCT-001 (registration/email verification)
   - Success criteria: Contract reviewed and signed by Product/Administrator; artifact present at docs/.ai/initial-build/contract/API-Contract.md

2. FOUNDATION: Developer & Test Harness (Pending)
   - Type: FOUNDATION
   - Predecessors: CONTRACT
   - Objective: Provide CI/test scaffolding, Windows developer setup instructions, mock inference harness, test fixtures for RED milestones, and baseline security guidance.
   - Delivers: tests/, docs/developer/windows-setup.md, scripts/mock_inference/README.md, ci/config
   - Success criteria: Test harness runs on Windows and CI; `python -m pytest -q` executes (empty runnable suite) locally.

3. OTHER: Model Feasibility & Licensing Assessment (Pending)
   - Type: OTHER
   - Predecessors: FOUNDATION
   - Objective: Non-code analysis of candidate models: evaluate at least two realistic Hindi-capable inference pipelines for speaker-conditioning, expressive control support, long-form continuity, GPU memory, inference cost, and licensing (software, weights, output permissions). Define and approve an evaluation protocol that will govern quality assessment in Real-Model RED. No model weights downloaded; evaluation uses public docs/model cards and reference comparisons only.
   - Delivers: 
     * docs/.ai/initial-build/model-eval/candidates.md (comparison table of at least 2 candidate models)
     * docs/.ai/initial-build/model-eval/license-matrix.md (license/output-use findings with citations)
     * docs/.ai/initial-build/model-eval/evaluation-protocol.md (approved evaluation criteria, test samples, metrics, acceptance thresholds, human-review procedures)
     * docs/.ai/initial-build/model-eval/approved.md (human-approved model selection with licensing sign-off)
   - Verifies: R-EVAL-001, R-LIC-001 (evidence basis for AC-LIC-001)
   - Success criteria: All evaluation artifacts present with citations and human approval recorded; evaluation protocol pre-approved before Real-Model RED begins; human-approved model selection documented in approved.md.
   - Note: This milestone produces evidence and recommendations only; no executable behavior change (OTHER). Requires explicit human approval to unblock Real-Model RED. The evaluation protocol must define fixed representative samples, test coverage (Hindi/English), speaker-similarity evaluation method, pronunciation approach, expressive-control evaluation criteria, long-form continuity assessment, objective metrics where applicable, human-review procedures, and explicit acceptance thresholds or decision rules.

4. RED: Persistence & Storage RED (Pending)
   - Type: RED
   - Predecessors: FOUNDATION
   - Objective: Add failing tests that assert correct per-user isolation, retention policy enforcement, deletion and purge behaviors, and audit behaviors; implement minimal persistence scaffolding to run those tests (mocks/stubs allowed). RED must contain failing tests first. Retention configuration must be runtime-configurable.
   - Delivers: tests/integration/test_persistence.py (failing), persistence stubs, migration helpers, retention-policy schema.
   - Verifies (failing tests): R-ACCT-002, R-ACCT-003, R-RET-001, R-RET-002, R-DEL-001, AC-ACCT-001, AC-RET-001

5. GREEN: Persistence & Storage GREEN (Pending)
   - Type: GREEN
   - Predecessors: Persistence RED
   - Objective: Implement persistence behavior so persistence tests pass against mock or local storage; ensure purge, audit metadata, and access controls complete. Retention policies are operator-configurable; separate policies for voice profiles, samples, generated audio, and audit/consent records.
   - Success criteria: Persistence tests from RED pass locally; retention policies are configurable at runtime; audit and deletion workflows functional.

6. RED: Authentication & Consent RED (Pending)
   - Type: RED
   - Predecessors: Persistence GREEN
   - Objective: Add failing service-level tests for user registration, email verification, authentication, per-user authorization, and consent recording; provide minimal service/auth scaffolding to run tests per CONTRACT.
   - Delivers: tests/integration/test_auth_and_consent.py (failing), auth handlers, consent schema.
   - Verifies (failing tests): R-ACCT-001, R-CONS-001, R-CONS-002, AC-CONS-001

7. GREEN: Authentication & Consent GREEN (Pending)
   - Type: GREEN
   - Predecessors: Authentication & Consent RED
   - Objective: Implement auth, email verification, and consent recording so tests pass. Integrate with persistence and CONTRACT.
   - Success criteria: Auth and consent tests pass locally; consent records are immutable and queryable.

8. RED: Job Orchestration & Idempotency RED (Pending)
   - Type: RED
   - Predecessors: Authentication & Consent GREEN
   - Objective: Add failing tests for durable job state, idempotent submission (with idempotency keys), job metadata, job lifecycle states, quota enforcement at submission time, and budget enforcement with spend tracking. Minimal service/queue code allowed (mock adapters allowed).
   - Delivers: tests/integration/test_job_orchestration.py (failing), job schema, queue interface stubs, quota/budget enforcement hooks.
   - Verifies (failing tests): R-WORK-001, FR-022, FR-023, FR-024, FR-025, FR-044, FR-045, R-GEN-001, AC-GEN-001, AC-HIST-001, AC-QUOTA-001

9. GREEN: Job Orchestration & Idempotency GREEN (Pending)
   - Type: GREEN
   - Predecessors: Job Orchestration & Idempotency RED
   - Objective: Implement durable job state, idempotency, job lifecycle, quota enforcement (per-user quotas, rate limits, concurrency limits) and budget enforcement (spend tracking, kill-switch blocking) so tests pass. Retries do not duplicate artifacts or billing. Operator controls (budget kill-switch, quota configuration) are runtime-configurable.
   - Success criteria: Job orchestration tests pass; idempotency tests verify no duplicate artifacts; quota and budget enforcement tests pass; quotas and budgets are operator-configurable at runtime.

10. RED: Mock Inference Adapter RED (Pending)
    - Type: RED
    - Predecessors: Job Orchestration & Idempotency GREEN
    - Objective: Add failing tests for mock model adapter interface (pause strength, speech pace controls exposed); ensure model-gating hooks exist for later real-model enablement.
    - Delivers: tests/unit/test_mock_adapter.py (failing), mock adapter stubs with expressive-control hooks.
    - Verifies (failing tests): AC-EXP-001 (mock behavior), adapter interface contract.
    - Note: This milestone establishes the mock inference interface; real models are integrated later in Real-Model RED/GREEN.

11. GREEN: Mock Inference Adapter GREEN (Pending)
    - Type: GREEN
    - Predecessors: Mock Inference Adapter RED
    - Objective: Implement mock adapter so tests pass; expressive controls (pause, pace) reflected in mock output; interface ready for approved real-model integration.
    - Success criteria: Mock adapter tests pass; expressive controls produce observable output changes.

12. RED: Real-Model Inference Integration RED (Pending)
    - Type: RED
    - Predecessors: Mock Inference Adapter GREEN, Model Feasibility Assessment (approval required)
    - Objective: Add failing integration tests that assert real-model inference behavior (correct Hindi pronunciation, speaker identity, expressive control effects, long-form continuity) using approved model artifacts in a local test environment (no cloud provision).
    - Delivers: tests/integration/test_real_model_inference.py (failing), real-model adapter scaffolding.
    - Verifies (failing tests): R-EXP-001, AC-EXP-001 (with real model), quality assertions for AC-LIC-001

13. GREEN: Real-Model Inference GREEN (Pending)
    - Type: GREEN
    - Predecessors: Real-Model Inference RED
    - Objective: Integrate approved model (weights under approved license) so real-model tests pass locally; quality metrics and limitations documented.
    - Success criteria: Real-model tests pass; model enabling is gated by AC-LIC-001 (model evaluation approval).

14. RED: Frontend & UX RED (Pending)
    - Type: RED
    - Predecessors: Job Orchestration & Idempotency GREEN, Mock Inference Adapter GREEN
    - Objective: Add failing E2E tests for registration/email, consent & enrollment, profile reuse, generation submission, preview/download, quotas, deletion, and expressive controls.
    - Delivers: tests/e2e/test_user_flows.py (failing), frontend scaffolding.
    - Verifies (failing tests): R-ACCT-001, R-CONS-001, R-CONS-002, FR-010, FR-011, FR-012, FR-020, FR-025, AC-GEN-001, AC-HIST-001, AC-RET-001

15. GREEN: Frontend & UX GREEN (Pending)
    - Type: GREEN
    - Predecessors: Frontend & UX RED
    - Objective: Implement frontend behavior so E2E tests pass against service and adapters. Usability checklist validated; expressive controls UI gated by model support.
    - Success criteria: E2E tests pass; UI responsive and general-user-friendly.

16. OTHER: Documentation & Operator Controls (Pending)
    - Type: OTHER
    - Predecessors: Frontend & UX GREEN, Job Orchestration & Idempotency GREEN, Persistence & Storage GREEN
    - Objective: Produce non-behavioral operational documentation and verification evidence. This milestone introduces no executable production behavior; behavioral implementations for quotas, budget controls, and retention configuration are completed in Job Orchestration GREEN and Persistence GREEN.
    - Delivers: 
      * docs/operations/quota-operator-guide.md (how to configure and monitor per-user quotas, rate limits, concurrency caps)
      * docs/operations/budget-killswitch-guide.md (how to monitor spend and activate budget kill-switch)
      * docs/operations/retention-policy-guide.md (how to configure and audit retention policies for profiles, samples, audio, and consent/audit records)
      * docs/operations/runbooks/ (alert procedures, troubleshooting, incident response)
      * Verification evidence: operator controls functional test runs, configuration schema validation, documentation completeness check
    - Verifies (non-behavioral): Documentation of R-GEN-001, NFR-008, R-RET-001, R-RET-002, AC-QUOTA-001 operational use
    - Success criteria: All operational documentation present and reviewed; operator procedures validated against configured system behavior from Job Orchestration GREEN and Persistence GREEN; no new executable behavior introduced (verify via diff/code review).
    - Note: This milestone is OTHER because it produces documentation, guides, and operational verification evidence only. All production behavior for quota enforcement, budget kill-switch, and retention configuration is delivered by Job Orchestration GREEN and Persistence GREEN, respectively.

17. OTHER: Optional Cloud Run L4 Deployment Validation (Pending)
    - Type: OTHER
    - Predecessors: Real-Model Inference GREEN
    - Objective: Produce validation plan and checklist for Cloud Run L4 compatibility (cold-start, scale-to-zero, quotas, cost projections) without provisioning resources. No code changes (OTHER).
    - Delivers: docs/.ai/initial-build/cloudrun/validation-plan.md, cloudrun-readiness-checklist.md
    - Success criteria: Validation checklist complete; human signoff required before any cloud provisioning.
    - Note: Optional; does not block M0 completion.

18. RED: End-to-End Verification RED (Pending)
    - Type: RED
    - Predecessors: Frontend & UX GREEN, Real-Model Inference GREEN, Documentation & Operator Controls OTHER (all mandatory implementations)
    - Objective: Compose failing end-to-end verification tests covering registration/auth, consent & enrollment, profile reuse, Hindi/English narration, speaker similarity and pronunciation, expressive controls, long-form generation, job durability/idempotency, data isolation/deletion, quotas/retention/budget enforcement, licensing gating. AC-SEC-001 verification includes local/M0 aspects (secret-provider abstraction, no secrets in source, authorized-access semantics, encryption configuration, least-privilege design, IAM configuration validation); deployment-level aspects (managed secret store, deployed storage encryption, deployed IAM, deployed transport configuration) are noted as requiring environment deployment for full verification.
    - Delivers: tests/e2e/test_end_to_end_verification.py (failing)
    - Verifies (failing tests): all approved P0 requirements and acceptance criteria, including AC-SEC-001 local/M0 verification aspects

19. GREEN: End-to-End Verification GREEN (Pending)
    - Type: GREEN
    - Predecessors: End-to-End Verification RED
    - Objective: Resolve defects so end-to-end verification tests pass; produce final verification report and M0 completion evidence.
    - Success criteria: End-to-end tests pass; verification report in docs/.ai/initial-build/VERIFICATION_REPORT.md documents test outcomes and evidence for M0 gate approval.

Traceability: requirement→milestone matrix (complete)

| Requirement/Acceptance Criterion | Milestone(s) Delivery | Milestone(s) Verification |
|---|---|---|
| R-ACCT-001 (registration, email verification) | CONTRACT, Authentication & Consent RED/GREEN, Frontend RED/GREEN | Authentication & Consent RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| R-ACCT-002 (per-user isolation) | Persistence RED/GREEN, Authentication & Consent RED/GREEN, Job Orchestration RED/GREEN | Persistence RED/GREEN, E2E RED/GREEN |
| R-ACCT-003 (private voice libraries) | Persistence RED/GREEN, Authentication & Consent RED/GREEN | Persistence RED/GREEN, E2E RED/GREEN |
| R-CONS-001 (explicit consent before enrollment) | CONTRACT, Authentication & Consent RED/GREEN, Frontend RED/GREEN | Authentication & Consent RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| R-CONS-002 (consent for assisted recording) | Persistence RED/GREEN, Authentication & Consent RED/GREEN | Authentication & Consent RED/GREEN, Persistence RED/GREEN, E2E RED/GREEN |
| FR-002 (consent recording—referenced by R-CONS-001) | Authentication & Consent RED/GREEN, Persistence RED/GREEN | Authentication & Consent RED/GREEN, E2E RED/GREEN |
| FR-003 (profile revocation—referenced by R-REV-001) | Persistence RED/GREEN, Frontend RED/GREEN | Persistence RED/GREEN, E2E RED/GREEN |
| FR-010 (voice enrollment: accept/validate audio formats) | Frontend RED/GREEN, Job Orchestration RED/GREEN, Persistence RED/GREEN | Frontend RED/GREEN, E2E RED/GREEN |
| FR-011 (recording quality checks with actionable feedback) | Model Feasibility Assessment, Real-Model RED/GREEN, Frontend RED/GREEN | Real-Model RED/GREEN, E2E RED/GREEN |
| FR-012 (persistent voice profiles with metadata) | Persistence RED/GREEN, Job Orchestration RED/GREEN | Persistence RED/GREEN, E2E RED/GREEN |
| FR-020 (UTF-8 Hindi/English text input; preserve punctuation/line breaks) | CONTRACT, Job Orchestration RED/GREEN, Frontend RED/GREEN | Job Orchestration RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| FR-022 (asynchronous job model with defined states) | CONTRACT, Job Orchestration RED/GREEN | Job Orchestration RED/GREEN, E2E RED/GREEN |
| FR-023 (preserve script snapshot and job metadata) | CONTRACT, Job Orchestration RED/GREEN, Persistence RED/GREEN | Job Orchestration RED/GREEN, Persistence RED/GREEN, E2E RED/GREEN |
| FR-024 (allow preview, regenerate, download WAV; MP3 if licensing permits) | CONTRACT, Job Orchestration RED/GREEN, Frontend RED/GREEN | Job Orchestration RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| FR-025 (chunk scripts at linguistic boundaries; use punctuation/breaks as pause cues) | Job Orchestration RED/GREEN, Frontend RED/GREEN | Job Orchestration RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| FR-040 (support Windows setup, local dev, mocked inference, containerized worker) | FOUNDATION | FOUNDATION, E2E RED/GREEN |
| FR-041 (model inference behind interface; swappable backends) | FOUNDATION, Mock Adapter RED/GREEN, Real-Model RED/GREEN | Mock Adapter RED/GREEN, Real-Model RED/GREEN, E2E RED/GREEN |
| FR-042 (configurable local/cloud inference; no local CUDA assumption) | FOUNDATION, Mock Adapter RED/GREEN, Real-Model RED/GREEN | FOUNDATION, Real-Model RED/GREEN, E2E RED/GREEN |
| FR-044 (bound concurrency, duration, retries, script length, spend) | Job Orchestration RED/GREEN | Job Orchestration RED/GREEN, E2E RED/GREEN |
| FR-045 (durable job state, idempotent submission with keys) | CONTRACT, Job Orchestration RED/GREEN, Persistence RED/GREEN | Job Orchestration RED/GREEN, Persistence RED/GREEN, E2E RED/GREEN |
| FR-046 (cloud secrets, private storage, encryption, least-privilege, signed downloads) | CONTRACT, FOUNDATION, Persistence RED/GREEN | FOUNDATION, Persistence RED/GREEN, E2E RED/GREEN |
| R-WORK-001 (core generation workflow: user→profile→script→job→preview→download) | Contract, Job Orchestration RED/GREEN, Frontend RED/GREEN, Persistence RED/GREEN | Job Orchestration RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| R-GEN-001 (per-user quotas, rate limits, concurrency limits) | Job Orchestration RED/GREEN | Job Orchestration RED/GREEN, E2E RED/GREEN |
| R-EXP-001 (basic expressive controls: speech pace, pause strength) | Model Feasibility Assessment, Mock Adapter RED/GREEN, Real-Model RED/GREEN, Frontend RED/GREEN | Mock Adapter RED/GREEN, Real-Model RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| R-EVAL-001 (measurable voice-cloning evaluation protocol) | Model Feasibility Assessment OTHER | Model Feasibility Assessment OTHER, Real-Model RED/GREEN (quality metrics), E2E RED/GREEN |
| R-LIC-001 (commercial licensing verification mandatory gate) | Model Feasibility Assessment OTHER, Real-Model RED/GREEN | Model Feasibility Assessment OTHER, Real-Model RED/GREEN, E2E RED/GREEN |
| R-RET-001 (separate retention policies for profiles/samples/audio/audit) | Persistence RED/GREEN | Persistence RED/GREEN, E2E RED/GREEN |
| R-RET-002 (default retention: audio 30d, profiles/consent configurable) | Persistence RED/GREEN | Persistence RED/GREEN, E2E RED/GREEN |
| R-DEL-001 (post-deletion: purge samples, embeddings, cached artifacts) | Persistence RED/GREEN, Frontend RED/GREEN | Persistence RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| R-REV-001 (profile revocation: remove metadata, samples, embeddings, disallow synthesis) | Persistence RED/GREEN, Frontend RED/GREEN, Job Orchestration RED/GREEN | Persistence RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| NFR-008 (cost: show per-run cost, no always-on GPU without approval; $20/month target) | Job Orchestration RED/GREEN | Job Orchestration RED/GREEN, E2E RED/GREEN |
| AC-ACCT-001 (account isolation: users cannot access others' profiles/samples/jobs) | Authentication & Consent RED/GREEN, Frontend RED/GREEN, Persistence RED/GREEN | Authentication & Consent RED/GREEN, Persistence RED/GREEN, E2E RED/GREEN |
| AC-CONS-001 (consent recording: immutable consent events queryable by admins) | Authentication & Consent RED/GREEN, Frontend RED/GREEN, Persistence RED/GREEN | Authentication & Consent RED/GREEN, Persistence RED/GREEN, E2E RED/GREEN |
| AC-ENR-001 (enrollment: validated formats, quality checks, metadata includes model/version/consent) | Frontend RED/GREEN, Persistence RED/GREEN | Frontend RED/GREEN, E2E RED/GREEN |
| AC-GEN-001 (generation workflow: authenticated user→profile→script→job→preview/download) | Job Orchestration RED/GREEN, Real-Model RED/GREEN, Frontend RED/GREEN, Persistence RED/GREEN | Job Orchestration RED/GREEN, Real-Model RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| AC-HIST-001 (job history: queryable per user, immutable metadata, authorized access) | Persistence RED/GREEN, Job Orchestration RED/GREEN, Frontend RED/GREEN | Persistence RED/GREEN, Job Orchestration RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| AC-QUOTA-001 (quotas enforced at submission; operator alerts/kill-switch) | Job Orchestration RED/GREEN, Frontend RED/GREEN | Job Orchestration RED/GREEN, E2E RED/GREEN |
| AC-RET-001 (deletion/revocation: samples/embeddings removed within 24h; audit retained) | Persistence RED/GREEN, Frontend RED/GREEN | Persistence RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| AC-SEC-001 (secrets in managed storage; signed downloads; encryption in transit/at rest; least-privilege) | FOUNDATION, Persistence RED/GREEN | FOUNDATION, Persistence RED/GREEN, E2E RED/GREEN (M0/local aspects: secret-provider abstraction, no secrets in source, authorized-access design, encryption config, IAM config validation; deployment aspects noted for environment validation) |
| AC-EXP-001 (expressive controls (pause, pace) operable, model-gated, reflected in output) | Mock Adapter RED/GREEN, Real-Model RED/GREEN, Frontend RED/GREEN | Mock Adapter RED/GREEN, Real-Model RED/GREEN, Frontend RED/GREEN, E2E RED/GREEN |
| AC-LIC-001 (model licensing: approval artifact required before production enablement) | Model Feasibility Assessment OTHER, Real-Model RED/GREEN | Model Feasibility Assessment OTHER, Real-Model RED/GREEN, E2E RED/GREEN |

Execution Status (initial)
| Milestone | Type | Status | Blockers |
|-----------|------|--------|---------|
| CONTRACT | CONTRACT | Pending | None |
| FOUNDATION | FOUNDATION | Pending | CONTRACT |
| Model Feasibility & Licensing Assessment | OTHER | Pending | FOUNDATION |
| Persistence RED | RED | Pending | FOUNDATION |
| Persistence GREEN | GREEN | Pending | Persistence RED |
| Authentication & Consent RED | RED | Pending | Persistence GREEN |
| Authentication & Consent GREEN | GREEN | Pending | Authentication & Consent RED |
| Job Orchestration & Idempotency RED | RED | Pending | Authentication & Consent GREEN |
| Job Orchestration & Idempotency GREEN | GREEN | Pending | Job Orchestration & Idempotency RED |
| Mock Inference Adapter RED | RED | Pending | Job Orchestration & Idempotency GREEN |
| Mock Inference Adapter GREEN | GREEN | Pending | Mock Inference Adapter RED |
| Real-Model Inference Integration RED | RED | Pending | Mock Adapter GREEN, Model Feasibility Assessment (approval required) |
| Real-Model Inference Integration GREEN | GREEN | Pending | Real-Model Inference Integration RED |
| Frontend & UX RED | RED | Pending | Job Orchestration & Idempotency GREEN, Mock Adapter GREEN |
| Frontend & UX GREEN | GREEN | Pending | Frontend & UX RED |
| Documentation & Operator Controls | OTHER | Pending | Frontend & UX GREEN, Job Orchestration & Idempotency GREEN, Persistence & Storage GREEN |
| Cloud Run L4 Validation (Optional, non-blocking) | OTHER | Pending | Real-Model Inference GREEN |
| End-to-End Verification RED | RED | Pending | Frontend & UX GREEN, Real-Model Inference GREEN, Documentation & Operator Controls OTHER (all mandatory) |
| End-to-End Verification GREEN | GREEN | Pending | End-to-End Verification RED |

Verification Commands (source)
- Foundation: `python -m pytest -q` — FOUNDATION
- Persistence: `pytest tests/integration/test_persistence.py::test_delete_purges_storage -q` — Persistence RED/GREEN
- Auth & Consent: `pytest tests/integration/test_auth_and_consent.py::test_registration_and_email_verification -q` — Authentication & Consent RED/GREEN
- Job Orchestration: `pytest tests/integration/test_job_orchestration.py::test_idempotency -q` — Job Orchestration RED/GREEN
- Mock Adapter: `pytest tests/unit/test_mock_adapter.py::test_expressive_controls -q` — Mock Adapter RED/GREEN
- Model Feasibility: Evaluation documents produced (no code test) — Model Feasibility Assessment OTHER
- Real-Model: `pytest tests/integration/test_real_model_inference.py::test_hindi_pronunciation -q` — Real-Model RED/GREEN (local, no cloud)
- Frontend E2E: `scripts/run_e2e_verification.sh` — Frontend RED/GREEN
- End-to-End: `scripts/run_comprehensive_e2e.sh` — End-to-End RED/GREEN

Plan Content Rules self-check (rule-by-rule)
1) CONTRACT required? — Pass. CONTRACT milestone present as milestone 1.
2) RED semantics (failing tests first)? — Pass. Every RED milestone explicitly states failing tests/artifacts added before implementation.
3) GREEN semantics (implements until tests pass)? — Pass. Every GREEN milestone depends on its RED and implements to pass those tests.
4) No milestone depends on unapproved model assumptions? — Pass: Real-Model RED depends on explicit Model Feasibility Assessment OTHER (with pre-approved evaluation protocol) and signed approval before proceeding.
5) All P0 requirements assigned to milestones? — Pass: Complete traceability matrix covers all 41 approved requirements (31 R-/FR-/NFR + 10 AC) with both delivery and verification assignments. All approved items from requirements.md are represented.
6) Authentication/email/consent/account isolation assigned? — Pass: CONTRACT and Authentication & Consent RED/GREEN; Persistence RED/GREEN covers isolation and audit; AC-ACCT-001 and AC-CONS-001 verified.
7) End-to-end verification included? — Pass: End-to-End Verification RED/GREEN milestones (18-19) depend on all mandatory implementations and cover all requirements.
8) Inference Adapter resolved? — Pass: Mock Inference Adapter RED/GREEN (milestones 10-11) explicitly defined; dependencies clarified (Real-Model RED depends on Mock Adapter GREEN); FR-041/FR-042 assigned.
9) Cloud Run classification and blocking? — Pass: Cloud Run L4 Validation (milestone 17) is classified as OTHER (no behavior change, only validation plan); listed as optional/non-blocking in Execution Status; not a predecessor to E2E RED.
10) OTHER milestones contain no executable behavior? — Pass: Model Feasibility Assessment (3) produces evaluation/documentation only; Cloud Run L4 Validation (17) produces validation plan/checklist only; Documentation & Operator Controls (16) produces guides/procedures/verification evidence only (behavioral implementations for quotas/retention/budget live in Job Orchestration GREEN and Persistence GREEN).
11) Behavioral implementations in correct RED/GREEN milestones? — Pass: Quota enforcement and budget kill-switch behavior in Job Orchestration RED/GREEN (not OTHER); Retention configuration behavior in Persistence RED/GREEN (not OTHER); Frontend quota/retention UI in Frontend RED/GREEN.
12) Model Feasibility milestone defines evaluation protocol? — Pass: Milestone 3 delivers evaluation-protocol.md pre-approving test coverage, metrics, thresholds, human-review procedures; Real-Model RED consumes these criteria.
13) AC-SEC-001 verification semantics correct? — Pass: Traceability matrix distinguishes M0/local verification (secret-provider abstraction, encryption config, IAM design, no secrets in source) from deployment verification (managed secrets, deployed IAM, deployed encryption); E2E RED explicitly states which aspects are M0-verifiable vs require environment deployment.
14) No cloud provisioning during M0? — Pass; no cloud milestone provisioning steps included; Cloud Run validation is checklist-only.
15) Preservation of provenance and clarification history? — Pass: requirements artifact remains authoritative; Plan references approval on 2026-10-19; clarification decisions (Q1-Q4) preserved in requirements.
16) Requirement descriptions corrected? — Pass: FR-020 (Hindi/English text), FR-024 (preview/download/WAV), FR-025 (linguistic chunking), FR-040 (Windows setup/local dev), FR-041 (pluggable inference), FR-042 (local/cloud config) all corrected to match requirements.md. Missing AC-ENR-001, AC-SEC-001, FR-002, FR-003 added to matrix.

Risks & blockers
- Model feasibility and licensing may block real-model integration until models with acceptable licenses and Hindi quality are approved by human decision-maker.
- Expressive controls (pause strength, speech pace) are approved P0 (per User: Q3). If model feasibility evaluation cannot support them, stop and request explicit human approval for a scope change. Do not automatically defer them to P1.
- $20/month budget target likely requires strict quotas; quota design must validate feasibility against actual model inference costs (validated in Real-Model GREEN).

Resolved decisions to record
None (all prior decisions captured in requirements.md Clarification Log: Q1-Q4 recorded by user on 2026-10-19)

Verified constraints preserved
- ✓ 19-milestone structure maintained
- ✓ CONTRACT → FOUNDATION sequencing
- ✓ Separate Persistence RED/GREEN (now includes retention configuration behavior)
- ✓ Separate Authentication & Consent RED/GREEN
- ✓ Separate Job Orchestration & Idempotency RED/GREEN (now includes quota/budget behavior)
- ✓ Separate Mock Inference Adapter RED/GREEN
- ✓ Model feasibility/licensing as explicit human gate with pre-approved evaluation protocol
- ✓ Separate Real-Model RED/GREEN consuming evaluation criteria
- ✓ Frontend RED/GREEN
- ✓ Final E2E RED/GREEN with only mandatory predecessors (Cloud Run is optional/non-blocking)
- ✓ Optional/non-blocking Cloud Run validation
- ✓ No cloud provisioning
- ✓ No implementation work at this stage
- ✓ No weakening of approved P0 requirements; expressive controls remain P0 with model-feasibility gate

Verdict: ✅ APPROVED by avinash2196 on 2026-10-19T11:37:33Z

Blocking items: None

Next step: Begin CONTRACT milestone workflow. CONTRACT produces API-Contract.md, which is then authoritative for implementation-level Implementation Plans per milestone.