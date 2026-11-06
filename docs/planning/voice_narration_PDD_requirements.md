# Voice Narration Studio — PDD-Ready Software Requirements

**Version:** 1.0  
**Status:** Proposed; architecture and model selection require human approval  
**Audience:** AI coding agent operating under repository PDD skills  
**Primary users:** Family members creating Hindi poems, stories, and video voiceovers  
**Primary environment:** Windows development; optional Google Cloud Run NVIDIA L4 GPU for inference

## 1. Objective and product principles
Build a browser-based, Hindi-first narration application that lets an authorized person enroll their own voice with consent, save a reusable voice profile, enter new Hindi or English scripts, synthesize expressive narration, preview and refine it, and export audio for use in videos. Re-enrollment must not be necessary for every poem. Design for eventual public or monetized YouTube use **without assuming that every open-source model or checkpoint permits commercial use**.

Principles: simple parent-friendly UX; correct and natural Hindi; voice ownership and consent; privacy by default; replaceable model backend; reproducible quality tests; predictable cloud spend; PDD governance and human approval gates.

## 2. Non-goals (MVP)
No video editor, automatic YouTube upload, music generation, celebrity/public-figure cloning, voice marketplace, mobile-native app, real-time voice conversion, multi-tenant SaaS billing, or guarantee of perfect emotional fidelity. No production deployment until the licensing and security gates pass.

## 3. Personas and workflows
- **Narrator/parent:** enrolls own voice, reviews consent, saves voice, pastes poem, picks style, previews and downloads narration.
- **Family administrator:** manages deployment, user access, storage, costs, and voice-profile deletion.
- **Developer/operator:** benchmarks candidate models, diagnoses quality, deploys GPU workers and monitors job outcomes.

**Happy path:** Sign in → create voice profile → record/upload clean samples → validate samples → consent confirmation → prepare profile → paste script → choose profile/style → generate → listen → revise script/pause settings → regenerate → download WAV/MP3.

**Exception paths:** low-quality recording; Hindi text normalization error; GPU cold start; inference timeout; partial chunk failure; unavailable model; insufficient GPU quota; unsupported language; storage error; revoked consent; user deletion request.

## 4. MVP scope and priorities
Priority labels: P0 = release blocking; P1 = first post-MVP; P2 = future.

### 4.1 Accounts and consent
- **FR-001 P0:** Private authenticated application with administrator and narrator roles; no anonymous generation.
- **FR-002 P0:** Before voice enrollment, display an explicit confirmation that the user owns the voice or has informed permission to clone it; record timestamp, account, consent version and profile association.
- **FR-003 P0:** Support revocation, profile deletion and removal of associated samples/derived embeddings, subject to documented retention and backup lifecycle.
- **FR-004 P0:** Restrict each profile to its owner or explicitly authorized family members; prevent enumeration and unauthorized audio access.
- **FR-005 P1:** Optional explicit family voice-sharing permission and audit trail.

### 4.2 Voice enrollment
- **FR-010 P0:** Record through browser microphone or upload WAV/MP3/M4A; define and validate supported formats, duration and size limits during architecture.
- **FR-011 P0:** Provide recording guidance, playback and sample quality checks (duration, clipping, silence, noise, levels, speech presence); actionable feedback and re-recording.
- **FR-012 P0:** Save a reusable voice profile with friendly name, language, consent reference, model/version, enrollment status and sample metadata.
- **FR-013 P0:** Model adapter may use reference audio, embeddings or fine-tuned weights; never promise that enrollment implies model training. Persist only what the selected model needs.
- **FR-014 P1:** Guided Hindi/English recording script covering phonemes, conversational speech, storytelling and emotion; support multiple samples.

### 4.3 Script preparation and generation
- **FR-020 P0:** Paste/edit UTF-8 Devanagari Hindi and English; preserve punctuation, line breaks and original script; support mixed Hindi-English when backend supports it.
- **FR-021 P0:** Choose an authorized voice profile and supported narration style (at minimum neutral; additional styles only if validated).
- **FR-022 P0:** Generate audio asynchronously and show states: queued, preparing, running, post-processing, completed, failed, cancelled.
- **FR-023 P0:** Keep a script snapshot, selected profile, model version, generation parameters, output reference, timestamps and actionable error details for each job.
- **FR-024 P0:** Allow preview, regenerate and download WAV; MP3 export if encoder/licensing permits.
- **FR-025 P0:** Chunk long scripts at linguistically sensible phrase/sentence boundaries, never mid-word; handle punctuation and line breaks as pause cues, not unconditional silence.
- **FR-026 P0:** Join chunks without clicks, dropouts, repeated words or unintended gaps; ensure stable loudness, sample rate and voice identity. Maintain exact text-to-audio chunk mapping for troubleshooting.
- **FR-027 P0:** Provide adjustable pause strength and speech pace within tested ranges; do not expose controls unsupported by the model.
- **FR-028 P0:** Preserve originals and allow regenerating a problematic section, with an explicit preview of the resulting join when supported.
- **FR-029 P1:** Optional per-line overrides for pause/emphasis/pronunciation and pronunciation dictionary for Hindi names or uncommon words.
- **FR-030 P1:** Style presets such as emotional poetry, calm storytelling and motivational; no claim of reliable emotion control until measured.
- **FR-031 P1:** History with search, replay, download, rename and delete.

### 4.4 Operational requirements
- **FR-040 P0:** Support Windows developer setup, local API/UI development, mocked inference, and containerized inference worker.
- **FR-041 P0:** Model inference behind an interface so backend models can be swapped without changing UI/business APIs.
- **FR-042 P0:** Configurable local inference and cloud inference; do not assume Windows machine has CUDA.
- **FR-043 P0:** GPU jobs on Cloud Run L4 only after confirming current region availability, quotas, GPU runtime limits, cold-start behavior and billing. Default GPU worker to scale-to-zero where supported; avoid min instances unless approved.
- **FR-044 P0:** Bound concurrency, job duration, retries, script length and spend. Expose an estimated cost/usage view to administrator and an operator-configurable budget/kill switch.
- **FR-045 P0:** Durable job state and idempotent submission; safely retry interrupted work without duplicate final artifacts or uncontrolled billing.
- **FR-046 P0:** Cloud secrets in managed secret storage; private object storage; encryption in transit/at rest; least-privilege identities; signed/authorized downloads.
- **FR-047 P1:** Optional on-device CPU preview if performance is acceptable; never block MVP on CPU voice synthesis.

## 5. Model-selection gate (must precede production implementation)
No model has been approved yet. Evaluate at least two realistic Hindi-capable inference pipelines, including their base TTS, speaker-conditioning/conversion stages, pretrained weights, adapters, vocoders, dependencies and text-processing assets. **Do not treat a repository's MIT/Apache code license as proof that downloaded model weights or generated outputs are commercially usable.**

Produce a model evaluation record for each candidate:
1. Exact source URL, commit/tag, checkpoint hash, model card and full dependency/license inventory.
2. Commercial-use and monetized-video permissions for software, weights and outputs, with citations to primary license texts; unresolved restrictions are blockers, not assumptions.
3. Explicit native Hindi/Devanagari capability; if not native, document each translation/transliteration/conversion step and its effect on quality.
4. L4 VRAM, load/cold-start time, synthesis latency, approximate cost per minute of generated speech, quality and stability.
5. Voice likeness, intelligibility, Hindi pronunciation, prosody, pause placement, long-form continuity, audio artifacts and ability to regenerate sections.
6. Risks of cloning without authorization, speaker leakage, model supply chain and retention of training/enrollment audio.

**Gate G1:** Present comparison and recommendation to human reviewer; obtain approval before implementing model-specific production code. If no candidate is commercially permissible and good enough for Hindi, stop and propose licensed alternatives rather than silently relaxing constraints.

## 6. Proposed architecture (subject to PDD review)
- **Web frontend:** responsive browser UI, Devanagari fonts, large controls, recording, playback, job status.
- **API/orchestrator:** authentication, authorization, consent, profile metadata, script normalization, job creation/status, export authorization.
- **Job execution:** durable queue and bounded GPU worker. Evaluate Cloud Run Jobs vs services against workload and actual GPU platform capabilities; do not assume one is automatically suitable.
- **Model adapter:** `prepare_voice_profile`, `synthesize_segment`, `capabilities`, `health`, `model_metadata`.
- **Audio post-processing:** segment alignment, silence control, crossfade where appropriate, loudness normalization, format conversion and artifact validation.
- **Persistence:** relational metadata store plus private object storage for reference audio and exports; local filesystem/SQLite development alternative only if migration path is explicit.
- **Observability:** structured logs, correlation/job IDs, error codes, duration, cold starts, resource usage, and cost estimates; never log raw voice or private scripts by default.

Avoid premature microservice proliferation: use a modular API plus isolated GPU worker for MVP unless architecture evidence justifies more services.

## 7. Proposed API contracts (draft; finalize in architecture)
- `POST /v1/voice-profiles` — create draft profile.
- `POST /v1/voice-profiles/{id}/samples` — upload authorized sample (direct or signed upload).
- `POST /v1/voice-profiles/{id}/consent` — record explicit consent.
- `POST /v1/voice-profiles/{id}/prepare` — validate/prepare profile.
- `GET /v1/voice-profiles` — list authorized profiles.
- `DELETE /v1/voice-profiles/{id}` — revoke and initiate deletion.
- `POST /v1/narrations` — submit script, profile, style and parameters; return job ID.
- `GET /v1/narrations/{id}` — job status, metadata and authorized output links.
- `POST /v1/narrations/{id}/cancel` — best-effort cancellation.
- `POST /v1/narrations/{id}/regenerate` — new version or selected segment.
- `GET /v1/narrations/{id}/audio` — authorized audio retrieval.

Define request/response schemas, validation, maximum lengths, state transitions, error codes, idempotency and auth in an approved contract before coding. No fabricated implementation decisions should be treated as approved.

## 8. Nonfunctional requirements and acceptance metrics
The following are **proposed acceptance targets**, to be calibrated using baseline recordings and human evaluation, not claims about existing models.
- **NFR-001 Usability:** parent can generate and download a poem using an enrolled voice without developer assistance after a short walkthrough.
- **NFR-002 Quality:** no audible clicks, unintended truncation or mid-word pauses in a fixed 10-script Hindi regression corpus; exceptions must be tracked and reviewed.
- **NFR-003 Pronunciation:** human reviewers rate intelligibility and naturalness on a 1–5 rubric; target mean >=4/5 across the agreed Hindi corpus, with critical errors individually triaged.
- **NFR-004 Voice similarity:** consented speaker evaluates recognizable identity on a 1–5 rubric; target mean >=4/5 on test corpus.
- **NFR-005 Performance:** benchmark 30-second, 2-minute and 5-minute scripts; propose measurable p50/p95 targets after initial L4 proof of concept.
- **NFR-006 Reliability:** failed/timeout jobs have actionable states and bounded retries; no stuck indefinite running jobs.
- **NFR-007 Security:** no unauthorized profile/script/audio access; upload validation and deletion tests pass.
- **NFR-008 Cost:** show measured per-run compute and storage cost; no always-on GPU without explicit approval.
- **NFR-009 Portability:** run tests locally without paid cloud resources; GPU model adapter deploys from version-pinned container.
- **NFR-010 Legal:** every shipped model/checkpoint and material dependency has reviewed license evidence, including output-use restrictions.

## 9. Test and evaluation corpus
Build a versioned, consented test suite with: Hindi poetry with punctuation and line breaks; Hindi prose; numerals, dates and abbreviations; Sanskrit-derived conjuncts; Urdu-derived vocabulary; proper nouns; mixed Hindi-English; short and long passages; leading/trailing silence; difficult pause placements; repeated generation to assess consistency. Include reference speaker audio only with consent. Never put private recordings in public repositories.

Testing layers: unit tests for normalization, chunking and authorization; contract tests for API and adapter; mocked job orchestration; integration tests with object storage and queue; GPU smoke test; acoustic signal checks for silence/clipping/seams; blinded human listening review. Compare generated audio against text and listen at chunk boundaries; signal metrics alone cannot establish narration quality.

## 10. PDD execution and human approval gates
The agent must first inspect the repository's installed PDD skills, standards, existing work items and conventions. **Follow those repository-specific rules over this document wherever they prescribe process**, and surface conflicts for human resolution. Do not invent PDD command names, file layouts or milestone status semantics.

Suggested staged work items (each independently reviewable with tests and explicit exit criteria):

**M0 — Discovery and requirements:** inventory repository, clarify unknowns, produce assumptions/decisions register and requirements traceability. **Gate:** approve scope and unresolved decisions.

**M1 — Model/legal/quality feasibility:** license matrix, candidate benchmark harness, Hindi test corpus, L4 inference proof of concept, sample listening comparison and cost evidence. **Gate:** human selects model or stops project.

**M2 — Architecture and contracts:** threat model, ADRs, API schemas, data lifecycle, queue semantics, storage and deployment plan, cost controls. **Gate:** approve architecture and contracts.

**M3 — Backend foundations:** authentication, profile lifecycle, consent, private storage, metadata and API contract tests; mocked inference. **Gate:** functional/security review.

**M4 — Inference and audio pipeline:** approved model adapter, text segmentation, asynchronous worker, synthesis, post-processing, artifact checks and quality tests. **Gate:** human listening acceptance.

**M5 — Parent-friendly UI:** guided recording, profile selection, Hindi script editor, generation, status, playback, export, error recovery. **Gate:** parent usability walkthrough.

**M6 — Deployment and hardening:** Windows setup, Cloud Run L4 deployment, observability, budgets, IAM, deletion verification, runbooks and end-to-end tests. **Gate:** production readiness approval.

**M7 — Optional enhancements (not MVP):** emotion presets, pronunciation overrides, targeted segment editing, shared family library, captions and video-cover workflow.

For every milestone: create the PDD plan/contract artifacts required by the installed skill; define RED tests before implementation; implement minimally; run GREEN tests and regression; document deviations, risk and evidence; stop for human review at designated gates. Changes to approved contracts must follow repository PDD change-control and plan-integrity procedures. Do not auto-approve gates or mark tests passed without execution evidence.

## 11. Definition of done
MVP is complete only when: a consenting parent can enroll once; generate at least three different Hindi scripts with that profile; preview and export usable audio; correct script/pause errors through regeneration; securely manage/delete the profile; recover from failures; run on the agreed infrastructure; show actual inference cost; pass automated tests and human listening review; and retain approved commercial-use evidence for all deployed model assets.

## 12. Open decisions for human approval
1. Is initial access restricted to two parents plus one administrator, or a wider family?
2. Should sample and generated audio remain only in their cloud account, or can local Windows copies be stored?
3. What maximum poem length and output retention period are desired?
4. Is bilingual Hindi/English required in MVP, or Hindi only?
5. What monthly cloud budget and acceptable cold-start wait should the system enforce?
6. What exact consent flow is appropriate when a family member assists a parent in recording?
7. Which model passes the license and Hindi-quality feasibility gate?

## 13. First instruction to the PDD coding agent
> Read the installed PDD skills and repository conventions. Treat this file as the product requirements baseline, not authorization to implement everything immediately. Begin with M0 discovery and M1 model/license/Hindi-quality feasibility planning. Identify ambiguities, propose contracts, tests, candidate evaluation and human approval gates. Do not start full implementation, provision paid cloud resources or select a model without explicit approval. Report assumptions and stop at the first required approval gate.
