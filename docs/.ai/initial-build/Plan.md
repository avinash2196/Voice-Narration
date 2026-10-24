# Plan — initial-build

## Status

Approved by avinash2196 on 2026-10-24. Approval recorded by the main conversation at the user's explicit approval of this revised Plan. CONTRACT may proceed; every later milestone still requires its applicable approved predecessor artifacts and its own reviewed Implementation Plan. This approval does not authorize provisioning or approve the draft contract.

Approval history: the previous Plan was approved by avinash2196 on 2026-10-19T11:37:33Z. That approval is historical and does not approve this revision. All original Execution Status rows were Pending; no executed milestone or execution evidence exists to preserve.

Revision basis: requirements.md Status records approval by avinash2196 on 2026-10-19 and its Scope clarification dated 2026-10-24 records the user's retention of all non-conflicting baseline P0 requirements. The deployment-shape decision dated 2026-10-24 in architecture/System-Architecture.md records nine separate services. Contract-Review.md remains changes-requested; the draft contract and remaining architecture details are not approved.

## Objective

Deliver the multi-user Hindi-first narration product, with English support, reusable consented voices, durable asynchronous generation, safe expressive controls and private audio lifecycle. Retain every non-conflicting baseline P0 requirement, including neutral style, model-minimal enrollment artifacts, seamless audio/chunk mapping and conditional section regeneration.

## Current State

Repository inspection on 2026-10-24 found README.md, voice_narration_PDD_requirements.md and work-item documentation only: no production source, tests, dependency/build definitions, containers or runnable verification scripts. README.md contains only the repository title. No existing production behavior or tests can serve as a passing baseline.

The existing Plan's nineteen milestones are all Pending. Its draft contract is pending approval and Contract-Review.md lists unresolved contract decisions. The selected nine-service deployment shape is recorded; deployment costs, runtime feasibility, model selection and full architecture approval have not been demonstrated. No Implementation Plan exists.

## In Scope

All approved work-item requirements and non-conflicting baseline P0 functional requirements, with single delivery ownership below. The original persistence, authentication/consent, job orchestration, mock inference, real-model inference and browser sequences remain distinct. Enrollment and security/distributed integration have explicit independently testable boundaries.

Feasibility/licensing assessment, evaluation protocol, developer prerequisites, operator guidance, conditional Cloud Run readiness assessment and evidence-based final verification support these behaviors.

## Out of Scope

The work-item Explicit Exclusions apply: video editor, automatic YouTube upload, music generation, celebrity/public-figure cloning, mobile-native app and real-time voice conversion. Advanced emotion controls and per-line pronunciation overrides remain outside MVP under the recorded P1/P2 boundary. This Plan retains the previous no-cloud-provisioning execution boundary; deployment evidence must come from an independently approved, user-supplied environment.

## Requirements and Constraints

- requirements.md and its scope clarification govern over conflicting family-only baseline assumptions. FR-001 roles and FR-004 access are interpreted through the approved User/Administrator, strict isolation and explicit private-data authorization requirements; family-sharing behavior is not inferred.
- The selected deployment shape comprises nine separate services. Full architecture details and unresolved external behavior must receive their applicable human review before implementation.
- Output has a 3000-second absolute ceiling, subordinate to stricter quota/resource/budget limits. Generated audio defaults to 30-day retention; cleanup defaults to the configurable 24-hour window. Profile/consent/audit retention is administrator configured.
- The $20/month budget is an operational target, not a guarantee or a per-user allocation. The 300-second cold-start tolerance is subject to feasibility. No always-on GPU, model selection, licensing sign-off or paid provisioning is implicitly approved.
- Basic pause/pace controls remain P0 and model-gated. Unsupported feasibility is a blocker requiring a user decision, not permission to silently remove scope.
- Model-selection Gate G1 precedes all model-specific production implementation. The evaluation protocol owns calibration of proposed baseline quality targets; the baseline's proposed 10-script and 4/5 metrics are not silently promoted to approved fixed release thresholds.
- Baseline NFR-001–010 provide quality, legal, reliability, cost and portability context. Confirmed behavior is traced below; proposed quantitative acceptance targets are calibrated for human approval in the evaluation protocol, not invented here.
- Every repository-changing milestone requires its own reviewed Implementation Plan and execution evidence. Only RED may finish with an expected behavior-related failing check.

## Non-Blocking Open Decisions

Exact build/test commands and approved-stack implementation choices belong to the relevant Implementation Plan. The repository has no build from which to derive them. Model selection, safe control ranges, evaluation thresholds and compute feasibility are explicitly deferred to the assessment and approved-model prerequisites; inability to meet P0 scope stops that gate.

No unresolved contract decision is treated as an implementation default. No target user count, traffic rate, uptime, deployment replica count or new telemetry target is introduced by this revision.

## External Contract Requirements

The first milestone completes contract/API-Contract.md from the existing unapproved draft; no approved contract is being amended. It defines only the approved P0 public and stable internal consumer behavior. The contract owns authentication/bootstrap and private-data authorization, consent-before-persistence enrollment/quality override/status, profile lifecycle, supported text/styles/controls, generation and history, cancellation/retries, regeneration/original preservation/join preview, chunk-mapping availability, artifact preview/download/deletion, model approval/capability gating, quota/budget/retention administration and externally settable configuration.

It must resolve the Contract-Review.md findings: public/internal inventory alignment, enrollment/consent flow, idempotency representation/scope/comparison/concurrency/replay/expiry, validation and operational limits, state transitions, authorization/revocation retrieval, local/deployed transport boundary, exact schemas/content types, absence/null/blank/unknown handling, identifiers, errors, numeric/currency precision, lists/filtering/ordering/pagination and configuration names/shapes. Do not adopt the draft's unsupported constants or recommendations without review. No HTTP paths, methods, error mappings or limits are fixed by this Plan.

## Milestones

The order below is strictly linear. A milestone's predecessor includes the completed evidence of the entire preceding sequence. Boundaries isolate persistence/lifecycle, identity/consent, enrollment, orchestration/policy, portable inference, real audio behavior, security/service integration and browser workflow. Enrollment is separate because validated reusable profiles are required before generation. Security/integration is separate because nine services and deployed protection need independently reviewable evidence.

The final verification is OTHER for already delivered behavior, replacing the invalid duplicate catch-all RED/GREEN delivery. Cloud readiness assessment is mandatory in the sequence; actual Cloud Run use remains conditional. The selected-model FOUNDATION is necessary because its dependencies/assets/environment cannot be known before human model selection. Initial FOUNDATION covers all general test prerequisites; neither FOUNDATION creates missing production symbols or domain schema.

### 1. API & External Contract

- Capability / purpose: API & External Contract.
- Rationale: Consumer behavior must be reviewed before executable changes.
- Milestone type: CONTRACT.
- Predecessor: Plan approval.
- Scope:
  - Deliver contract/API-Contract.md defining all retained externally observable P0 behavior and every deferred contract decision listed below.
- Owned requirements / concerns: External contract decisions.
- Explicit exclusions: Executable changes and an Implementation Plan for this milestone.
- Success criteria: The complete contract has explicit human approval and all contract-review blocking findings are resolved.

### 2. Developer & Test Harness

- Capability / purpose: Developer & Test Harness.
- Rationale: Missing executable prerequisites would prevent meaningful RED evidence.
- Milestone type: FOUNDATION.
- Predecessor: API & External Contract.
- Scope:
  - Establish the minimum Windows/local build, dependency, configuration, service bootstrap, container and test-execution prerequisites for every RED milestone below, including persistence, communication, enrollment/audio checks, browser checks and deployment-security checks. Provide local/CI execution without paid cloud resources and developer setup guidance. Do not implement domain behavior, domain schema, production placeholders or tests.
- Owned requirements / concerns: Executable prerequisites.
- Explicit exclusions: Tests, domain schema, production behavior and placeholder production symbols.
- Success criteria: Every prerequisite/bootstrap/availability check passes in the intended environment and exact repeatable commands are recorded; an empty suite's nonzero exit is not a passing check.
- RED prerequisites served: every RED below; each needs its capability's build/dependencies/configuration/test execution available before tests are added. Coverage includes service communication/storage test environments and browser/audio verification infrastructure.

### 3. Model Feasibility & Licensing Assessment

- Capability / purpose: Model Feasibility & Licensing Assessment.
- Rationale: Separate evidence/documentation work from production behavior.
- Milestone type: OTHER.
- Predecessor: Developer & Test Harness.
- Scope:
  - Deliver model-eval/candidates.md, model-eval/license-matrix.md, model-eval/evaluation-protocol.md and model-eval/approved.md: compare at least two Hindi-capable pipelines, cite complete licensing/output-use evidence, document capability/section-regeneration feasibility, and obtain human selection and protocol approval before model-specific production work.
  - Define a versioned consented evaluation corpus and measurable Hindi-first/English protocol for identity, pronunciation, continuity, expressive controls and human listening; calibrate proposed baseline numerical targets rather than declaring them already approved. Assess model memory, cold start, latency and cost, including the 300-second cold-start tolerance subject to feasibility. This is documentation/evidence work only; model-specific executable work and weight acquisition require the later reviewed prerequisite and inference milestones.
- Owned requirements / concerns: R-EVAL-001; Model-selection Gate G1 evidence.
- Explicit exclusions: Production behavior changes; fixes discovered here require replanning.
- Success criteria: Every review/check and applicable preserved regression check passes, and required evidence and human decisions are recorded.
- No-behavior-change statement: Only documentation, assessment or verification evidence is delivered; no executable production change.
- Baseline evidence: The inspected baseline states no model has been approved; no evaluation artifacts currently exist.
- Preserved tests: The FOUNDATION prerequisite checks (no production test suite exists yet).
- Completion evidence: Reviewed scope artifacts plus actual passing checks, citations and recorded human decisions where required; no production changes in the diff.

### 4. Persistence & Storage RED

- Capability / purpose: Persistence & Storage.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Model Feasibility & Licensing Assessment.
- Scope:
  - Tests/checks only: verify R-ACCT-002; R-ACCT-003; FR-004 — Enforce strict owner isolation and private libraries/history, prevent enumeration, and require explicit authorization for administrator access to private voice data.
  - Tests/checks only: verify R-RET-001; R-RET-002 — Enforce separate, configurable, auditable retention policies for profiles, samples, generated audio and consent/audit records; default generated-audio retention is 30 days and profile/consent durations are administrator configured.
  - Tests/checks only: verify R-REV-001; R-DEL-001; FR-003 — Reject synthesis immediately after deletion/revocation and purge profile metadata, original samples, derived/model artifacts, reconstructive caches and associated generated audio within the configurable window, default 24 hours; retain only permitted audit metadata under its policy.
- Owned requirements / concerns: Verification only — R-ACCT-002; R-ACCT-003; FR-004; R-RET-001; R-RET-002; R-REV-001; R-DEL-001; FR-003.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 5. Persistence & Storage GREEN

- Capability / purpose: Persistence & Storage.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Persistence & Storage RED.
- Scope:
  - R-ACCT-002; R-ACCT-003; FR-004 — Enforce strict owner isolation and private libraries/history, prevent enumeration, and require explicit authorization for administrator access to private voice data.
  - R-RET-001; R-RET-002 — Enforce separate, configurable, auditable retention policies for profiles, samples, generated audio and consent/audit records; default generated-audio retention is 30 days and profile/consent durations are administrator configured.
  - R-REV-001; R-DEL-001; FR-003 — Reject synthesis immediately after deletion/revocation and purge profile metadata, original samples, derived/model artifacts, reconstructive caches and associated generated audio within the configurable window, default 24 hours; retain only permitted audit metadata under its policy.
- Owned requirements / concerns: R-ACCT-002; R-ACCT-003; FR-004; R-RET-001; R-RET-002; R-REV-001; R-DEL-001; FR-003.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 6. Authentication & Consent RED

- Capability / purpose: Authentication & Consent.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Persistence & Storage GREEN.
- Scope:
  - Tests/checks only: verify R-ACCT-001; FR-001 — Provide open registration, email verification, User and Administrator roles, and authenticated generation.
  - Tests/checks only: verify R-CONS-001; R-CONS-002; FR-002 — Require recorded explicit owner consent/assisted-recording authorization before samples are used or persisted; preserve account, timestamp, consent version, identity and profile association, with immutable consent events queryable for authorized administration.
- Owned requirements / concerns: Verification only — R-ACCT-001; FR-001; R-CONS-001; R-CONS-002; FR-002.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 7. Authentication & Consent GREEN

- Capability / purpose: Authentication & Consent.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Authentication & Consent RED.
- Scope:
  - R-ACCT-001; FR-001 — Provide open registration, email verification, User and Administrator roles, and authenticated generation.
  - R-CONS-001; R-CONS-002; FR-002 — Require recorded explicit owner consent/assisted-recording authorization before samples are used or persisted; preserve account, timestamp, consent version, identity and profile association, with immutable consent events queryable for authorized administration.
- Owned requirements / concerns: R-ACCT-001; FR-001; R-CONS-001; R-CONS-002; FR-002.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 8. Voice Enrollment RED

- Capability / purpose: Voice Enrollment.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Authentication & Consent GREEN.
- Scope:
  - Tests/checks only: verify FR-010 — Accept browser microphone recordings and uploaded WAV/MP3/M4A, validating the contract-approved format, duration and size limits.
  - Tests/checks only: verify FR-011 — Provide recording guidance, sample playback, duration/clipping/silence/noise/level/speech-presence checks, actionable feedback and re-recording; allow informed quality-warning override as required by AC-ENR-001.
  - Tests/checks only: verify FR-012 — Save and reuse owned profiles with friendly name, language, consent reference, model/version, enrollment status and sample metadata.
  - Tests/checks only: verify FR-013 — Persist only the reference audio, embeddings or weights the selected model needs; represent enrollment accurately without promising model training.
- Owned requirements / concerns: Verification only — FR-010; FR-011; FR-012; FR-013.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 9. Voice Enrollment GREEN

- Capability / purpose: Voice Enrollment.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Voice Enrollment RED.
- Scope:
  - FR-010 — Accept browser microphone recordings and uploaded WAV/MP3/M4A, validating the contract-approved format, duration and size limits.
  - FR-011 — Provide recording guidance, sample playback, duration/clipping/silence/noise/level/speech-presence checks, actionable feedback and re-recording; allow informed quality-warning override as required by AC-ENR-001.
  - FR-012 — Save and reuse owned profiles with friendly name, language, consent reference, model/version, enrollment status and sample metadata.
  - FR-013 — Persist only the reference audio, embeddings or weights the selected model needs; represent enrollment accurately without promising model training.
- Owned requirements / concerns: FR-010; FR-011; FR-012; FR-013.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 10. Job Orchestration & Idempotency RED

- Capability / purpose: Job Orchestration & Idempotency.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Voice Enrollment GREEN.
- Scope:
  - Tests/checks only: verify FR-022; FR-023; FR-045 — Persist asynchronous job states and immutable script/profile/model/parameter/output/timestamp/error history; recover after crashes and safely retry interrupted work, using durable idempotent submission without duplicate final artifacts or duplicate billing.
  - Tests/checks only: verify R-GEN-001; FR-044; NFR-008 — Enforce administrator-adjustable system/per-user quotas, rates and concurrency plus bounded duration, retries, script length and spend; provide estimated and measured compute/storage usage and cost, forecast alerts against the $20 monthly target, and configurable budget/kill-switch execution blocking. Enforce the 3000-second absolute output cap subject to stricter quota/resource/budget limits; require approval for always-on GPU use.
- Owned requirements / concerns: Verification only — FR-022; FR-023; FR-045; R-GEN-001; FR-044; NFR-008.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 11. Job Orchestration & Idempotency GREEN

- Capability / purpose: Job Orchestration & Idempotency.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Job Orchestration & Idempotency RED.
- Scope:
  - FR-022; FR-023; FR-045 — Persist asynchronous job states and immutable script/profile/model/parameter/output/timestamp/error history; recover after crashes and safely retry interrupted work, using durable idempotent submission without duplicate final artifacts or duplicate billing.
  - R-GEN-001; FR-044; NFR-008 — Enforce administrator-adjustable system/per-user quotas, rates and concurrency plus bounded duration, retries, script length and spend; provide estimated and measured compute/storage usage and cost, forecast alerts against the $20 monthly target, and configurable budget/kill-switch execution blocking. Enforce the 3000-second absolute output cap subject to stricter quota/resource/budget limits; require approval for always-on GPU use.
- Owned requirements / concerns: FR-022; FR-023; FR-045; R-GEN-001; FR-044; NFR-008.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 12. Mock Inference Adapter RED

- Capability / purpose: Mock Inference Adapter.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Job Orchestration & Idempotency GREEN.
- Scope:
  - Tests/checks only: verify FR-040; FR-041; FR-042 — Run Windows local API/UI development and tests with mocked inference and a containerized worker; support configurable local/cloud inference without assuming local CUDA, and replace inference backends without changing UI/business APIs.
- Owned requirements / concerns: Verification only — FR-040; FR-041; FR-042.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 13. Mock Inference Adapter GREEN

- Capability / purpose: Mock Inference Adapter.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Mock Inference Adapter RED.
- Scope:
  - FR-040; FR-041; FR-042 — Run Windows local API/UI development and tests with mocked inference and a containerized worker; support configurable local/cloud inference without assuming local CUDA, and replace inference backends without changing UI/business APIs.
- Owned requirements / concerns: FR-040; FR-041; FR-042.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 14. Approved Model Test Prerequisites

- Capability / purpose: Approved Model Test Prerequisites.
- Rationale: Missing executable prerequisites would prevent meaningful RED evidence.
- Milestone type: FOUNDATION.
- Predecessor: Mock Inference Adapter GREEN.
- Scope:
  - After human selection/license approval, establish only the selected model's executable test prerequisites, permitted test assets and consented evaluation corpus defined by the approved protocol, so Real-Model Inference Integration RED and subsequent integration/browser checks can run. Do not create model-specific production behavior; confirm a workable local or separately supplied approved compute environment without presuming local CUDA.
- Owned requirements / concerns: Selected-model executable prerequisites.
- Explicit exclusions: Tests, domain schema, production behavior and placeholder production symbols.
- Success criteria: Every prerequisite/bootstrap/availability check passes in the intended environment and exact repeatable commands are recorded; an empty suite's nonzero exit is not a passing check.
- RED prerequisites served: Real-Model Inference Integration RED, Security & Nine-Service Integration RED and Frontend & UX RED; selected-model dependencies/assets and a feasible authorized compute environment supplement the initial harness. If paid resources or credentials are needed, record Waiting for the named user input/action; do not provision implicitly.

### 15. Real-Model Inference Integration RED

- Capability / purpose: Real-Model Inference Integration.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Approved Model Test Prerequisites.
- Scope:
  - Tests/checks only: verify R-EXP-001; FR-027 — Generate model-supported pause strength and speech pace within evaluated safe ranges, preserving identity and exposing controls only for supported capabilities.
  - Tests/checks only: verify FR-025; FR-026 — Chunk linguistically without splitting words; treat punctuation and line breaks as contextual pause cues; join without clicks, dropouts, repeats or unintended gaps, maintaining stable loudness, sample rate and identity plus exact text-to-audio chunk mapping.
  - Tests/checks only: verify R-LIC-001 — Prevent production model enablement without cited software/weights/output-use evidence and explicit Administrator approval; use only the human-selected permissible model and demonstrate Hindi pronunciation, recognizable identity, continuity and expressive quality against the approved evaluation protocol.
- Owned requirements / concerns: Verification only — R-EXP-001; FR-027; FR-025; FR-026; R-LIC-001.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 16. Real-Model Inference Integration GREEN

- Capability / purpose: Real-Model Inference Integration.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Real-Model Inference Integration RED.
- Scope:
  - R-EXP-001; FR-027 — Generate model-supported pause strength and speech pace within evaluated safe ranges, preserving identity and exposing controls only for supported capabilities.
  - FR-025; FR-026 — Chunk linguistically without splitting words; treat punctuation and line breaks as contextual pause cues; join without clicks, dropouts, repeats or unintended gaps, maintaining stable loudness, sample rate and identity plus exact text-to-audio chunk mapping.
  - R-LIC-001 — Prevent production model enablement without cited software/weights/output-use evidence and explicit Administrator approval; use only the human-selected permissible model and demonstrate Hindi pronunciation, recognizable identity, continuity and expressive quality against the approved evaluation protocol.
- Owned requirements / concerns: R-EXP-001; FR-027; FR-025; FR-026; R-LIC-001.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 17. Security & Nine-Service Integration RED

- Capability / purpose: Security & Nine-Service Integration.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Real-Model Inference Integration GREEN.
- Scope:
  - Tests/checks only: verify FR-046 — Protect cloud secrets with managed storage, keep object storage private, encrypt transit/rest, enforce least privilege and authorized/signed retrieval, and verify revocation access behavior against the approved contract in an actual supplied deployment.
  - Tests/checks only: verify Nine-service deployment-shape decision — Deliver interoperating Auth, Consent, Voice Profile, Narration Orchestrator, Artifact, Usage & Policy, AI Gateway, Inference Worker and Audit as nine separate services, preserving the responsibilities approved through contract review; demonstrate service-boundary isolation, crash/retry correctness, revocation propagation and auditable outcomes without assigning one service another service's data ownership.
- Owned requirements / concerns: Verification only — FR-046; Nine-service deployment-shape decision.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 18. Security & Nine-Service Integration GREEN

- Capability / purpose: Security & Nine-Service Integration.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Security & Nine-Service Integration RED.
- Scope:
  - FR-046 — Protect cloud secrets with managed storage, keep object storage private, encrypt transit/rest, enforce least privilege and authorized/signed retrieval, and verify revocation access behavior against the approved contract in an actual supplied deployment.
  - Nine-service deployment-shape decision — Deliver interoperating Auth, Consent, Voice Profile, Narration Orchestrator, Artifact, Usage & Policy, AI Gateway, Inference Worker and Audit as nine separate services, preserving the responsibilities approved through contract review; demonstrate service-boundary isolation, crash/retry correctness, revocation propagation and auditable outcomes without assigning one service another service's data ownership.
- Owned requirements / concerns: FR-046; Nine-service deployment-shape decision.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.
- Deployment evidence gate: full FR-046/AC-SEC-001 requires a user-supplied independently approved environment. If absent, record Waiting — deployed protection environment/evidence from user; local configuration/design evidence alone cannot complete this milestone or final acceptance.

### 19. Frontend & UX RED

- Capability / purpose: Frontend & UX.
- Rationale: Establish independent expected-failure evidence before the matching production behavior.
- Milestone type: RED.
- Predecessor: Security & Nine-Service Integration GREEN.
- Scope:
  - Tests/checks only: verify FR-020; FR-021 — Provide Hindi/English UTF-8 script entry/editing preserving original punctuation and line breaks, conditional mixed-language support, authorized profile selection and at least neutral supported narration style; additional styles require validation.
  - Tests/checks only: verify FR-024; FR-028 — Provide preview, whole-job regeneration and WAV download, with MP3 only when encoder/licensing permits; preserve originals and support problematic-section regeneration with explicit join preview when supported.
  - Tests/checks only: verify R-WORK-001 — Complete the authenticated enrollment-once/profile-reuse/script/job/preview/download/deletion workflow through the browser, including history, actionable failures, quota feedback and supported expressive controls; demonstrate at least three different Hindi scripts with one consented profile and obtain human usability/listening acceptance.
- Owned requirements / concerns: Verification only — FR-020; FR-021; FR-024; FR-028; R-WORK-001.
- Explicit exclusions: Production code, scaffolding, dependencies, migrations, runtime/build configuration and test-infrastructure changes.
- Success criteria: Its checks execute with all predecessor prerequisites available and demonstrate an expected failure solely for missing approved behavior; missing intended production symbols are valid RED evidence, unrelated environment/configuration failures are not.

### 20. Frontend & UX GREEN

- Capability / purpose: Frontend & UX.
- Rationale: Deliver only the behavior specified by the immediately preceding RED evidence.
- Milestone type: GREEN.
- Predecessor: Frontend & UX RED.
- Scope:
  - FR-020; FR-021 — Provide Hindi/English UTF-8 script entry/editing preserving original punctuation and line breaks, conditional mixed-language support, authorized profile selection and at least neutral supported narration style; additional styles require validation.
  - FR-024; FR-028 — Provide preview, whole-job regeneration and WAV download, with MP3 only when encoder/licensing permits; preserve originals and support problematic-section regeneration with explicit join preview when supported.
  - R-WORK-001 — Complete the authenticated enrollment-once/profile-reuse/script/job/preview/download/deletion workflow through the browser, including history, actionable failures, quota feedback and supported expressive controls; demonstrate at least three different Hindi scripts with one consented profile and obtain human usability/listening acceptance.
- Owned requirements / concerns: FR-020; FR-021; FR-024; FR-028; R-WORK-001.
- Explicit exclusions: Unrelated behavior and unreviewed contract/architecture decisions.
- Success criteria: Every predecessor RED check and applicable preserved regression check passes, with behavior and evidence meeting this milestone's scope.

### 21. Documentation & Operator Controls

- Capability / purpose: Documentation & Operator Controls.
- Rationale: Separate evidence/documentation work from production behavior.
- Milestone type: OTHER.
- Predecessor: Frontend & UX GREEN.
- Scope:
  - Deliver operator guidance for existing quota/rate/concurrency, spend/kill-switch and retention/deletion controls, Windows/local setup and documented service deployment constraints; validate procedures against the previously passing behavior. Produce a verification evidence index. Introduce no executable or behavioral change.
- Owned requirements / concerns: Operator documentation.
- Explicit exclusions: Production behavior changes; fixes discovered here require replanning.
- Success criteria: Every review/check and applicable preserved regression check passes, and required evidence and human decisions are recorded.
- No-behavior-change statement: Only documentation, assessment or verification evidence is delivered; no executable production change.
- Baseline evidence: Record the completed predecessor evidence and current documentation gaps before making this milestone's changes.
- Preserved tests: All previously passing checks produced by earlier milestones; exact commands are carried into this milestone's Implementation Plan from predecessor evidence.
- Completion evidence: Reviewed scope artifacts plus actual passing checks, citations and recorded human decisions where required; no production changes in the diff.

### 22. Cloud Run L4 Deployment Validation

- Capability / purpose: Cloud Run L4 Deployment Validation.
- Rationale: Separate evidence/documentation work from production behavior.
- Milestone type: OTHER.
- Predecessor: Documentation & Operator Controls.
- Scope:
  - Deliver cloudrun/validation-plan.md and cloudrun/readiness-checklist.md with current cited region availability, quota, runtime, cold-start and billing checks before any proposed L4 use; assess scale-to-zero and avoid minimum/always-on instances without approval. Document nine-service cost feasibility against the $20 operational target. This mandatory assessment is documentation only; Cloud Run use remains conditional and provisioning requires separate approval.
- Owned requirements / concerns: FR-043.
- Explicit exclusions: Production behavior changes; fixes discovered here require replanning.
- Success criteria: Every review/check and applicable preserved regression check passes, and required evidence and human decisions are recorded.
- No-behavior-change statement: Only documentation, assessment or verification evidence is delivered; no executable production change.
- Baseline evidence: Record the completed predecessor evidence and current documentation gaps before making this milestone's changes.
- Preserved tests: All previously passing checks produced by earlier milestones; exact commands are carried into this milestone's Implementation Plan from predecessor evidence.
- Completion evidence: Reviewed scope artifacts plus actual passing checks, citations and recorded human decisions where required; no production changes in the diff.

### 23. End-to-End Verification

- Capability / purpose: End-to-End Verification.
- Rationale: Separate evidence/documentation work from production behavior.
- Milestone type: OTHER.
- Predecessor: Cloud Run L4 Deployment Validation.
- Scope:
  - Consolidate and execute preserved automated checks and the approved human listening/usability protocol across the delivered workflow, including all Final Acceptance Criteria; deliver VERIFICATION_REPORT.md and the final evidence index. This milestone adds only characterization/regression checks and evidence for already delivered behavior, with no production change. If a correct check exposes missing behavior, stop and replan a new RED/GREEN boundary instead of fixing it here.
- Owned requirements / concerns: Final verification evidence.
- Explicit exclusions: Production behavior changes; fixes discovered here require replanning.
- Success criteria: Every review/check and applicable preserved regression check passes, and required evidence and human decisions are recorded.
- No-behavior-change statement: Only regression/characterization checks and evidence for approved behavior are added; production behavior is unchanged.
- Baseline evidence: Record the completed predecessor evidence and current documentation gaps before making this milestone's changes.
- Preserved tests: All previously passing checks produced by earlier milestones; exact commands are carried into this milestone's Implementation Plan from predecessor evidence.
- Completion evidence: Reviewed scope artifacts plus actual passing checks, citations and recorded human decisions where required; no production changes in the diff.

## Requirement Traceability

Each row has one delivery owner; the named RED verifies only the listed requirements/concerns. Later regression checks preserve them without acquiring delivery ownership. Baseline IDs that clarify the same behavior remain distinct references with the same owner.

| Requirement / Concern | Owning Milestone | Verifying Milestone / scope evidence |
| --- | --- | --- |
| R-ACCT-002; R-ACCT-003; FR-004 | Persistence & Storage GREEN | Persistence & Storage RED — “Enforce strict owner isolation and private libraries/history, prevent enumeration, and require explicit authorization for administrator access to private voice data.” |
| R-RET-001; R-RET-002 | Persistence & Storage GREEN | Persistence & Storage RED — “Enforce separate, configurable, auditable retention policies for profiles, samples, generated audio and consent/audit records; default generated-audio retention is 30 days and profile/consent durations are administrator configured.” |
| R-REV-001; R-DEL-001; FR-003 | Persistence & Storage GREEN | Persistence & Storage RED — “Reject synthesis immediately after deletion/revocation and purge profile metadata, original samples, derived/model artifacts, reconstructive caches and associated generated audio within the configurable window, default 24 hours; retain only permitted audit metadata under its policy.” |
| R-ACCT-001; FR-001 | Authentication & Consent GREEN | Authentication & Consent RED — “Provide open registration, email verification, User and Administrator roles, and authenticated generation.” |
| R-CONS-001; R-CONS-002; FR-002 | Authentication & Consent GREEN | Authentication & Consent RED — “Require recorded explicit owner consent/assisted-recording authorization before samples are used or persisted; preserve account, timestamp, consent version, identity and profile association, with immutable consent events queryable for authorized administration.” |
| FR-010 | Voice Enrollment GREEN | Voice Enrollment RED — “Accept browser microphone recordings and uploaded WAV/MP3/M4A, validating the contract-approved format, duration and size limits.” |
| FR-011 | Voice Enrollment GREEN | Voice Enrollment RED — “Provide recording guidance, sample playback, duration/clipping/silence/noise/level/speech-presence checks, actionable feedback and re-recording; allow informed quality-warning override as required by AC-ENR-001.” |
| FR-012 | Voice Enrollment GREEN | Voice Enrollment RED — “Save and reuse owned profiles with friendly name, language, consent reference, model/version, enrollment status and sample metadata.” |
| FR-013 | Voice Enrollment GREEN | Voice Enrollment RED — “Persist only the reference audio, embeddings or weights the selected model needs; represent enrollment accurately without promising model training.” |
| FR-022; FR-023; FR-045 | Job Orchestration & Idempotency GREEN | Job Orchestration & Idempotency RED — “Persist asynchronous job states and immutable script/profile/model/parameter/output/timestamp/error history; recover after crashes and safely retry interrupted work, using durable idempotent submission without duplicate final artifacts or duplicate billing.” |
| R-GEN-001; FR-044; NFR-008 | Job Orchestration & Idempotency GREEN | Job Orchestration & Idempotency RED — “Enforce administrator-adjustable system/per-user quotas, rates and concurrency plus bounded duration, retries, script length and spend; provide estimated and measured compute/storage usage and cost, forecast alerts against the $20 monthly target, and configurable budget/kill-switch execution blocking. Enforce the 3000-second absolute output cap subject to stricter quota/resource/budget limits; require approval for always-on GPU use.” |
| FR-040; FR-041; FR-042 | Mock Inference Adapter GREEN | Mock Inference Adapter RED — “Run Windows local API/UI development and tests with mocked inference and a containerized worker; support configurable local/cloud inference without assuming local CUDA, and replace inference backends without changing UI/business APIs.” |
| R-EXP-001; FR-027 | Real-Model Inference Integration GREEN | Real-Model Inference Integration RED — “Generate model-supported pause strength and speech pace within evaluated safe ranges, preserving identity and exposing controls only for supported capabilities.” |
| FR-025; FR-026 | Real-Model Inference Integration GREEN | Real-Model Inference Integration RED — “Chunk linguistically without splitting words; treat punctuation and line breaks as contextual pause cues; join without clicks, dropouts, repeats or unintended gaps, maintaining stable loudness, sample rate and identity plus exact text-to-audio chunk mapping.” |
| R-LIC-001 | Real-Model Inference Integration GREEN | Real-Model Inference Integration RED — “Prevent production model enablement without cited software/weights/output-use evidence and explicit Administrator approval; use only the human-selected permissible model and demonstrate Hindi pronunciation, recognizable identity, continuity and expressive quality against the approved evaluation protocol.” |
| FR-046 | Security & Nine-Service Integration GREEN | Security & Nine-Service Integration RED — “Protect cloud secrets with managed storage, keep object storage private, encrypt transit/rest, enforce least privilege and authorized/signed retrieval, and verify revocation access behavior against the approved contract in an actual supplied deployment.” |
| Nine-service deployment-shape decision | Security & Nine-Service Integration GREEN | Security & Nine-Service Integration RED — “Deliver interoperating Auth, Consent, Voice Profile, Narration Orchestrator, Artifact, Usage & Policy, AI Gateway, Inference Worker and Audit as nine separate services, preserving the responsibilities approved through contract review; demonstrate service-boundary isolation, crash/retry correctness, revocation propagation and auditable outcomes without assigning one service another service's data ownership.” |
| FR-020; FR-021 | Frontend & UX GREEN | Frontend & UX RED — “Provide Hindi/English UTF-8 script entry/editing preserving original punctuation and line breaks, conditional mixed-language support, authorized profile selection and at least neutral supported narration style; additional styles require validation.” |
| FR-024; FR-028 | Frontend & UX GREEN | Frontend & UX RED — “Provide preview, whole-job regeneration and WAV download, with MP3 only when encoder/licensing permits; preserve originals and support problematic-section regeneration with explicit join preview when supported.” |
| R-WORK-001 | Frontend & UX GREEN | Frontend & UX RED — “Complete the authenticated enrollment-once/profile-reuse/script/job/preview/download/deletion workflow through the browser, including history, actionable failures, quota feedback and supported expressive controls; demonstrate at least three different Hindi scripts with one consented profile and obtain human usability/listening acceptance.” |
| External contract decisions | API & External Contract | Human review — “all retained externally observable P0 behavior and every deferred contract decision” |
| Executable prerequisites | Developer & Test Harness | Same milestone — “minimum Windows/local build, dependency, configuration, service bootstrap, container and test-execution prerequisites” |
| Selected-model executable prerequisites | Approved Model Test Prerequisites | Same milestone — “selected model's executable test prerequisites, permitted test assets and consented evaluation corpus” |
| R-EVAL-001; Model-selection Gate G1 evidence | Model Feasibility & Licensing Assessment | Same milestone — “versioned consented evaluation corpus and measurable Hindi-first/English protocol”; “complete licensing/output-use evidence” |
| FR-043 | Cloud Run L4 Deployment Validation | Same milestone — “current cited region availability, quota, runtime, cold-start and billing checks before any proposed L4 use” |
| Operator documentation | Documentation & Operator Controls | Same milestone — “Deliver operator guidance for existing quota/rate/concurrency, spend/kill-switch and retention/deletion controls” |
| Final verification evidence | End-to-End Verification | Same milestone — “deliver VERIFICATION_REPORT.md and the final evidence index” |
| Work-item Explicit Exclusions and recorded MVP P1/P2 boundary | none — exclusion | Final Review |
| Final Review gate decision and identification of stale product/user-facing documentation | none — Final Review obligation | Final Review |

## Verification Commands

No executable verification command is established by repository evidence: there is no build, test runner or script. The previous Plan's sample commands and nonexistent scripts are removed, including the assumption that an empty suite passes. Developer & Test Harness establishes exact Windows/local/CI build and prerequisite checks in its reviewed Implementation Plan, sourced from the approved runtime/build definitions it proposes. Approved Model Test Prerequisites establishes model-specific environment checks sourced from the human-selected model/protocol.

Each subsequent Implementation Plan carries forward the actual predecessor commands and supplies exact capability checks and expected evidence; RED adds tests only, GREEN reruns its RED and preserved checks, and OTHER reruns applicable preserved checks. Source: requirements FR-040/041/042, approved model protocol, and the build/test artifacts delivered by these FOUNDATION milestones. Contract/document reviews use their scoped artifacts; final verification uses only predecessor checks, the approved protocol and the report it owns. No nonexistent verification script is presumed.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| API & External Contract | Complete | contract/API-Contract.md Contract Review Status: Approved by avinash2196 on 2026-10-24. Q5–Q10 resolved in requirements.md; eleven contract-completeness checks and documentation diff checks recorded. Human approval, not runtime verification, completes this CONTRACT milestone. |
| Developer & Test Harness | Pending | CONTRACT predecessor complete. 001_Implementation_Plan_Foundation.md prepared by a fresh planner; Awaiting human approval. Documentation checks passed; runtime dry run not performed because the required Python runtime and Docker server are unavailable. No executable files created. |
| Model Feasibility & Licensing Assessment | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Persistence & Storage RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Persistence & Storage GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Authentication & Consent RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Authentication & Consent GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Voice Enrollment RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Voice Enrollment GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Job Orchestration & Idempotency RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Job Orchestration & Idempotency GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Mock Inference Adapter RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Mock Inference Adapter GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Approved Model Test Prerequisites | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Real-Model Inference Integration RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Real-Model Inference Integration GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Security & Nine-Service Integration RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Security & Nine-Service Integration GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Frontend & UX RED | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Frontend & UX GREEN | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Documentation & Operator Controls | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| Cloud Run L4 Deployment Validation | Pending | Requires completed predecessors and its own approved Implementation Plan. |
| End-to-End Verification | Pending | Requires completed predecessors and its own approved Implementation Plan. |

No executable milestone has run. CONTRACT is complete through the approved deliverable above; all executable milestones remain Pending. No execution evidence was removed.

## Risks

- Model/license feasibility may fail: the baseline section 5 and requirements.md deferred decisions record no selected model. The assessment and model prerequisites must stop on unsupported P0 quality or expressive capability, not weaken them.
- Nine-service operating cost and environment feasibility remain unproven: architecture/System-Architecture.md deployment-shape decision explicitly records this. Cloud readiness assessment evaluates the $20 target; it does not guarantee it or approve provisioning.
- The contract/architecture currently disagree: Contract-Review.md identifies inventory, enrollment and idempotency drift. CONTRACT must resolve those decisions before initial FOUNDATION; the Plan does not ratify draft route or configuration proposals.
- Deployed security cannot be proved from documentation: requirements.md AC-SEC-001 requires managed secrets/storage/transit/identity protection, while repository inspection finds no deployed-environment evidence. Security GREEN remains Waiting on independently supplied environment/evidence if absent; final completion cannot substitute local design checks.
- Model prerequisites cannot be pinned yet: repository inspection finds no build or approved model. Their dedicated FOUNDATION is reviewed after selection, with no assumed Windows CUDA or implicit paid resources.

## Final Acceptance Criteria

Every criterion below is demonstrated by passing GREEN/evidence milestones, then retained in End-to-End Verification's report. RED alone cannot demonstrate working behavior. The scope quotations identify the delivery/evidence bullet; the Requirement Traceability table above provides the matching RED scope for each constituent requirement.

| Criterion | Source | Demonstrated by / scope evidence |
| --- | --- | --- |
| Account isolation, denied cross-user access and no audio exposure; administrator role alone provides no private-data access | AC-ACCT-001; R-ACCT-002/003 | Persistence & Storage GREEN — “Enforce strict owner isolation and private libraries/history, prevent enumeration, and require explicit authorization for administrator access to private voice data.” |
| Consent event contains account, timestamp, text/version and identity; immutable and administratively queryable, with consent before sample use/persistence | AC-CONS-001; R-CONS-001/002 | Authentication & Consent GREEN — “Require recorded explicit owner consent/assisted-recording authorization before samples are used or persisted” and “immutable consent events queryable for authorized administration.” |
| Validated enrollment, actionable sample checks or informed override, reusable complete profile metadata | AC-ENR-001; FR-010/011/012/013 | Voice Enrollment GREEN — “validating the contract-approved format, duration and size limits”; “allow informed quality-warning override”; “Save and reuse owned profiles with friendly name, language, consent reference, model/version, enrollment status and sample metadata.” |
| Authenticated generation progresses through required states; owner-only preview/download, durable replay produces no duplicate artifacts | AC-GEN-001 | Job Orchestration & Idempotency GREEN — “Persist asynchronous job states” and “durable idempotent submission without duplicate final artifacts or duplicate billing”; Frontend & UX GREEN — “Complete the authenticated enrollment-once/profile-reuse/script/job/preview/download/deletion workflow”; Security & Nine-Service Integration GREEN — “authorized/signed retrieval”. |
| Queryable owner-authorized narration history with immutable metadata | AC-HIST-001 | Persistence & Storage GREEN — “private libraries/history”; Job Orchestration & Idempotency GREEN — “immutable script/profile/model/parameter/output/timestamp/error history”; Frontend & UX GREEN — “including history”. |
| Revocation/deletion purges all required artifacts within configured default 24-hour bound, retains only permitted audit metadata and prevents future synthesis | AC-RET-001; R-REV-001; R-DEL-001 | Persistence & Storage GREEN — “Reject synthesis immediately after deletion/revocation and purge profile metadata, original samples, derived/model artifacts, reconstructive caches and associated generated audio within the configurable window, default 24 hours”. |
| Managed secrets, private storage, signed/authorized downloads, encryption and least privilege verified in deployment | AC-SEC-001 | Security & Nine-Service Integration GREEN — “Protect cloud secrets with managed storage, keep object storage private, encrypt transit/rest, enforce least privilege and authorized/signed retrieval” and “in an actual supplied deployment”. |
| Quota/rate/concurrency enforcement, forecast alerts and configurable budget kill switch; maximum output subordinate to limits | AC-QUOTA-001; FR-044; NFR-008; Q4 | Job Orchestration & Idempotency GREEN — “forecast alerts against the $20 monthly target, and configurable budget/kill-switch execution blocking” and “3000-second absolute output cap subject to stricter quota/resource/budget limits”. |
| Cited model evaluation and explicit Administrator approval before enabling production model | AC-LIC-001; R-LIC-001 | Model Feasibility & Licensing Assessment — “cite complete licensing/output-use evidence”; Real-Model Inference Integration GREEN — “Prevent production model enablement without cited software/weights/output-use evidence and explicit Administrator approval”. |
| UI exposes only supported pause/pace controls, tested ranges affect output while preserving identity | AC-EXP-001; R-EXP-001; FR-027 | Real-Model Inference Integration GREEN — “Generate model-supported pause strength and speech pace within evaluated safe ranges, preserving identity”; Frontend & UX GREEN — “supported expressive controls”; assessment provides approved feasibility/ranges. |
| Minimum neutral style and conditional mixed-language support with preserved original text | Retained FR-020/021 | Frontend & UX GREEN — “conditional mixed-language support, authorized profile selection and at least neutral supported narration style”. |
| Linguistic chunking, seamless stable audio and exact text/audio troubleshooting mapping | Retained FR-025/026 | Real-Model Inference Integration GREEN — “join without clicks, dropouts, repeats or unintended gaps, maintaining stable loudness, sample rate and identity plus exact text-to-audio chunk mapping”. |
| Preserve originals and conditionally regenerate a problematic section with join preview | Retained FR-028; FR-024 | Frontend & UX GREEN — “preserve originals and support problematic-section regeneration with explicit join preview when supported”; assessment records actual capability rather than silently dropping the condition. |
| Configurable separate retention and default audio policy | R-RET-001/002 | Persistence & Storage GREEN — “Enforce separate, configurable, auditable retention policies” and “default generated-audio retention is 30 days”. |
| Windows/local API/UI, mocked inference, container worker, backend replacement and configurable inference with no CUDA assumption | FR-040/041/042 | Mock Inference Adapter GREEN — “Run Windows local API/UI development and tests with mocked inference and a containerized worker”; “replace inference backends without changing UI/business APIs”. |
| Measurable, human-approved Hindi-first identity/pronunciation/continuity/expressiveness protocol and passing listening acceptance | R-EVAL-001; Gate G1; proposed NFR calibration | Model Feasibility & Licensing Assessment — “Define a versioned consented evaluation corpus and measurable Hindi-first/English protocol”; Real-Model Inference Integration GREEN — “demonstrate Hindi pronunciation, recognizable identity, continuity and expressive quality against the approved evaluation protocol”; End-to-End Verification executes it. |
| Consenting user enrolls once and generates at least three different Hindi scripts, previews/exports, regenerates, deletes and recovers from failures | R-WORK-001; baseline definition of done with Q2 persona correction | Frontend & UX GREEN — “demonstrate at least three different Hindi scripts with one consented profile and obtain human usability/listening acceptance”. |
| Nine services operate with reviewed responsibilities and demonstrate retry/revocation/isolation outcomes | Deployment-shape decision, 2026-10-24 | Security & Nine-Service Integration GREEN — “Deliver interoperating Auth, Consent, Voice Profile, Narration Orchestrator, Artifact, Usage & Policy, AI Gateway, Inference Worker and Audit as nine separate services”. |
| L4 readiness/current restrictions and cost evidence assessed before conditional use | Retained FR-043 | Cloud Run L4 Deployment Validation — “current cited region availability, quota, runtime, cold-start and billing checks before any proposed L4 use”. |
| Every non-RED milestone passes its own success checks; developer/operator/evaluation/evidence artifacts exist and procedures match delivered behavior | Plan-level milestone success criteria | Each owning milestone's completion evidence; Documentation & Operator Controls — “validate procedures against the previously passing behavior”; End-to-End Verification — “deliver VERIFICATION_REPORT.md and the final evidence index”. |
| Exclusions respected; no unapproved provisioning, model selection or fixed numerical quality targets; outdated product/user documentation identified for user decision | Requirements exclusions; recorded governance gates; Plan constraints | Final Review inspection and its explicit obligation row; End-to-End Verification supplies actual results, not an approval verdict. |

## Revision and Rule Checks

The original nineteen-milestone decomposition is retained where sound; enrollment, selected-model prerequisites and nine-service/security integration are added. Duplicate final behavior delivery becomes no-behavior-change OTHER; conditional cloud assessment is placed in the strict sequence. All headings, predecessor references, ownership rows, criteria, statuses, risks and verification references are rebuilt consistently. The previous repeated approval verdict and unsupported completeness claims are removed; original approval remains only as history.

1. Order: every milestone above has exactly one predecessor, immediately prior in the written sequence; CONTRACT is first.
2. Contract decisions: external behavior is assigned to the contract; no endpoint path/method/status, schema field, excluded alternative or unsupported operational constant is introduced.
3. Internal design: milestone scopes name capability/service boundaries and required documentation artifacts, not production classes, source files, framework annotations, packages, unapproved libraries or test-isolation strategies.
4. RED: all RED scopes explicitly say tests/checks only; scaffolding/schema/configuration deliverables are removed.
5. GREEN: every GREEN delivers the preceding RED's approved behavior and requires passing evidence.
6. FOUNDATION: only executable prerequisites, with explicit served REDs; domain schema and placeholder production behavior excluded.
7. Fields: every entry has capability, rationale, type, one predecessor, scope, owned concerns, exclusions and success criteria; every OTHER also has baseline, no-behavior-change statement, preserved checks and completion evidence.
8. Ownership: atomic requirement rows have one delivery owner and one matching RED; contract, prerequisite and evidence concerns are distinct. Scope quotations provide evidence; final tests do not acquire duplicate ownership.
9. Scope: restored all baseline P0 IDs, applied Q2/Q3 conflicts, retained proposed-target calibration, and linked risks to inspected artifacts.
10. Status: original executed count was zero; all revised rows remain Pending and revision awaits human review.
11. Prerequisites: initial FOUNDATION serves all REDs; selected-model FOUNDATION supplements later real-model/integration/browser checks after selection. Missing production symbols are RED evidence, not scaffolding work.
12. Criteria/artifacts: all ten work-item acceptance criteria and retained P0/Plan success criteria appear above with scope evidence. Verification uses only scoped predecessor checks, evaluation artifacts, supplied deployment evidence and the owned report. Local security checks cannot close deployed acceptance.
13. Commands: no repository-supported commands exist; FOUNDATION must establish exact commands through reviewed Implementation Plans. Unsupported previous sample commands/scripts are removed.

No new requirement/acceptance identifier is defined; existing IDs retain their approved meanings. Milestone titles name this Plan's execution boundaries and are not new definitions of source requirement identifiers. No template comments remain.
