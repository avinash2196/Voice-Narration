# Plan — chatterbox-cloud-run

## Status

Approved by avinash2196 on 2026-11-09. Approval recorded by the main conversation at the user's explicit approval ("Approve Plan"). The CONTRACT milestone (CRM-1) may proceed; every later milestone still requires its approved predecessor and its own reviewed Implementation Plan.

## Objective

Run Chatterbox voice cloning as a private Google Cloud Run service in project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, on an NVIDIA L4 GPU, while the voices service, inference service, frontend and Google TTS narration stay local. The local inference service sends the voice sample audio with each cloning request, calls Chatterbox with the existing service account's identity, bounds each cloning request by a configurable 10-minute limit, and reports why a cloning call failed. Chatterbox keeps no voice data after responding. This work item delivers the code changes and a deployment how-to; it does not perform the deployment. [Requirements: Goal, CCR-1–CCR-11]

Requirements authority: `docs/.ai/chatterbox-cloud-run/requirements.md`, Status "Approved by avinash2196 on 2026-11-09". There is no product-level `docs/requirements.md`.

## Current State

Inspected on 2026-11-09 at commit `360846e`.

Chatterbox model API (affected by CCR-5, CCR-6, CCR-10 and the Consistency and concurrency characteristic):

- The synthesize request takes text, language and an optional sample path (RF-1); a given path is opened on Chatterbox's own filesystem and a missing file is rejected (RF-2). Only `hi` and `en` are accepted (RF-3); a model generation error produces the failure answer of RF-4.
- The model is loaded lazily into one process-wide instance on first use, and generation calls are not serialized (`voice_narration/chatterbox_api/application.py:33-40`, `:63-72`).
- Generated audio is encoded into an in-memory buffer and returned; Chatterbox writes no file of its own (`voice_narration/chatterbox_api/application.py:83-86`).
- The device comes from `CHATTERBOX_DEVICE`, default `cpu` (RF-5).
- No existing test imports or exercises the Chatterbox model API (`tests/` holds `test_clone_flow.py`, `test_ai_gateway_red.py`, `test_ai_gateway_telemetry_red.py`; none references `voice_narration.chatterbox_api`).
- The Chatterbox model API imports its model runtime at module load (`voice_narration/chatterbox_api/application.py:7-13`). In the local virtual environment (CPython 3.13.17) the model runtime packages are not installed: `import torch` and `import chatterbox` both fail with `ModuleNotFoundError`, although `requirements-dev.txt:10` declares `chatterbox-tts==0.1.7`. `docs/developer-setup.md` states "No CUDA or paid cloud is needed", "Do not acquire model weights here", and "Tests may use stdlib mocks for boundaries, but mocks must not supply the behavior being proved".

Chatterbox container and deployment instructions (affected by CCR-1, CCR-3, CCR-4, CCR-7, CCR-9, CCR-11 and the Deployment characteristic):

- The image is built from `python:3.11-slim`, installs `requirements-dev.txt`, copies the application package and sets `CHATTERBOX_DEVICE=cpu` (RF-6; `cloudrun/chatterbox-service/Dockerfile:9-14`).
- The repository's build-context exclusions admit only `requirements-dev.txt` and `containers/` (`.dockerignore:1-4`), while the Chatterbox image copies the application package (`cloudrun/chatterbox-service/Dockerfile:12`).
- The existing deployment instructions use placeholder project and region values, deploy with `--allow-unauthenticated` (RF-7), set the CPU device, and set no GPU, instance-count or request-time-limit options (`cloudrun/chatterbox-service/README.md:5-14`).
- `cloudrun/inference-service/` holds artifacts for running the inference service on Cloud Run; this work item excludes moving the inference service to GCP and does not use them.

Local inference service (affected by CCR-5, CCR-7, CCR-8, CCR-9):

- The Chatterbox base URL is read from `VOICE_CLONING_API_BASE_URL`, falling back to `CHATTERBOX_API_BASE_URL` (RF-9).
- A cloning call sends the profile's local sample path and uses a 120-second timeout (RF-10); it attaches no caller identity (`voice_narration/inference/application.py:99-116`).
- Any cloning failure — no base URL configured, a transport error, or a non-success answer — produces one generic failure message (RF-11; `voice_narration/inference/application.py:102-114`, `:179-183`).
- Narration mode uses the Google TTS provider (RF-12); generated audio is written to the local filesystem (RF-13).
- The gateway execution operation passes the inference service's cloning failure message through as its error message (`voice_narration/inference/application.py:363-366`).
- The Google TTS provider locates Google credentials from `GOOGLE_APPLICATION_CREDENTIALS`, defaulting to `service-account-key.json` at the repository root (`voice_narration/inference/providers/google.py:13-35`); that file is present locally and excluded from version control (`.gitignore:10`).

Voices service and frontend:

- Uploaded voice samples are stored locally and their path recorded on the profile (RF-8).
- The frontend's generation request sends text, voice profile, voice name and user, and no mode, so it always uses the inference service's default narration mode (`frontend/src/App.jsx:116-124`, `voice_narration/inference/application.py:163`); it displays the inference service's failure message (`frontend/src/App.jsx:127-129`).

Existing tests (baseline run `.\.venv\Scripts\python.exe -m pytest tests -ra -q` on 2026-11-09: `9 passed, 1 warning in 3.31s`):

- Affected by this work item: `test_voice_cloning_returns_guidance_when_clone_backend_unavailable` asserts the generic message's wording for the no-backend case (RF-14; `tests/test_clone_flow.py:55-86`); `test_gateway_execution_returns_non_placeholder_telemetry` replaces the inference service's HTTP call to Chatterbox with a fake response accepting any arguments (RF-15; `tests/test_ai_gateway_telemetry_red.py:41-78`).
- Preserved, covering behavior this work item must not change: `test_voice_enrollment_creates_profile` and `test_generation_uses_selected_voice_profile` (`tests/test_clone_flow.py:8-52`; the latter exercises narration through Google TTS), and the five tests in `tests/test_ai_gateway_red.py`.

## In Scope

- An API/external contract for the changed Chatterbox synthesize request, the inference service's cloning-failure answer, and the local settings the inference service reads to call the private Chatterbox (CCR-5–CCR-9).
- Chatterbox accepting the voice sample audio in each synthesis request in place of a file path, holding no voice sample or generated audio after responding, and serving one cloning request at a time while others wait (CCR-6, CCR-10, Consistency and concurrency).
- The local inference service sending the voice sample audio with each cloning request, attaching the service account's Google identity token, bounding each cloning request by a configurable 10-minute limit, and reporting the reason for a cloning failure (CCR-5, CCR-7, CCR-8, CCR-9).
- A deployment document for running Chatterbox on Cloud Run in the required project, region and GPU, private to the service account, scaling to zero with at most one instance and one request at a time, and with a request time limit that accommodates CCR-9 — plus changes to the existing Chatterbox container build and deployment artifacts only where the documented steps need them (CCR-1, CCR-3, CCR-4, CCR-7, CCR-11, Deployment).

## Out of Scope

- Login and authentication of application users. [Requirements: Explicit Exclusions]
- Performing the GCP deployment. [Requirements: Explicit Exclusions, CCR-11]
- Moving the voices service, inference service, frontend or narration mode to GCP. [Requirements: Explicit Exclusions]

## Requirements and Constraints

- CCR-1–CCR-11 and AC-CCR-1–AC-CCR-8 as approved in the requirements artifact.
- Operational characteristics as recorded in the requirements: Scale not required; Deployment — scale to zero, at most 1 instance; Availability and latency — configurable 10-minute limit (CCR-9), no uptime expectation stated; Consistency and concurrency — one cloning request at a time, others wait within the time limit, a retried request produces a new clip, no duplicate detection required; Dependency failure — failure answer with the reason (CCR-8); Observability — not required beyond Cloud Run's default request logs.
- Constraint from another work item: "AGW-011 (Separate model service deployment): Chatterbox must run as a separate self-hosted Cloud Run service exposing an API consumed by the AI Gateway". [Artifact: ai-gateway-multimodel/requirements.md AGW-011]
- Constraint: the approved AI Gateway contract (`docs/.ai/ai-gateway-multimodel/contract/API-Contract.md`, approved 2026-11-08) is unchanged by this work item (see External Contract Requirements).
- Repository facts RF-1–RF-15 and the facts listed under Current State.

## Non-Blocking Open Decisions

- Deployment document location and organization (left to Plan in the requirements): the document lives with the existing Chatterbox Cloud Run deployment artifacts and replaces their current deployment instructions, so that no instruction to deploy publicly (RF-7) remains. Its section organization is left to the CRM-6 Implementation Plan.

## External Contract Requirements

A contract is required: this work item changes externally observable behavior of the Chatterbox model API and of the local inference service's cloning-failure answer, and introduces operator-set configuration.

- Contract artifact: `docs/.ai/chatterbox-cloud-run/API-Contract.md`, delivered by milestone CRM-1.
- Baseline (`prompt-driven-development` Changed Contracts): no approved contract artifact covers the Chatterbox model API or the inference service's job-creation failure answer. The baseline is the current repository behavior: the Chatterbox model API as implemented in `voice_narration/chatterbox_api/application.py` with the operations listed in `cloudrun/chatterbox-service/README.md:16-20`, and the inference service's job-creation operation and its cloning settings as implemented in `voice_narration/inference/application.py:22-24`, `:99-116`, `:157-216`. CRM-1 verifies this baseline against the repository, carries unchanged behavior over, and records only the changes below in a Changes in This Work Item section.
- Changes the contract must define, and decisions it owns (none is resolved, narrowed or presumed here):
  1. The request shape for sending the voice sample audio to Chatterbox (CCR-5, CCR-6) — deferred to the contract by the requirements.
  2. The removal of the sample path from Chatterbox's synthesize request (CCR-6), and Chatterbox's answer when the voice sample audio is missing or unusable.
  3. The caller identity Chatterbox calls require (CCR-7).
  4. The exact failure reasons and message wording of the inference service's cloning-failure answer (CCR-8), including the existing no-backend-configured case (RF-14) — deferred to the contract by the requirements.
  5. The name and form of the setting that configures the 10-minute time limit (CCR-9) — deferred to the contract by the requirements.
  6. The local settings the inference service reads to call the private Chatterbox with the service account's identity (CCR-7), starting from the existing base URL settings (RF-9) as baseline.
- Unchanged contract referenced as a constraint: the AI Gateway contract (`docs/.ai/ai-gateway-multimodel/contract/API-Contract.md`). Its request, response and error shapes stay as approved; the changed cloning-failure message reaches its error message text through the existing pass-through (`voice_narration/inference/application.py:363-366`). No CONTRACT milestone is recorded for it.

## Milestones

Decomposition: Split: independent capabilities and different verification setup — the Chatterbox service's request handling, retention and one-at-a-time serving are verified on their own without the model runtime, CUDA or weights (Current State; `docs/developer-setup.md`), while the inference service's sample sending, identity attachment, time limit and failure reporting are verified on their own against the Chatterbox boundary without network access; each pair also stays reviewable as exact code. Split: no behavior change — the deployment document and any container build and deployment artifact changes change no service behavior and are an OTHER milestone, placed last because it documents the settings CRM-1 defines and the behavior CRM-3 and CRM-5 deliver.

Prerequisite coverage (Plan Content Rule 11):

- CRM-2 (Chatterbox Service RED): after CRM-1 the repository provides the test runner with `pytest.ini` and the web-framework test client and HTTP client declared in `requirements-dev.txt:1-5` and installed in `.venv`. The model runtime is not installed locally; per `docs/developer-setup.md` local tests need no CUDA or model weights and may isolate boundaries, so the RED tests isolate the model runtime boundary within their own test code without supplying the behavior being proved. No dependency, build configuration or test infrastructure is missing, so no FOUNDATION milestone precedes CRM-2.
- CRM-4 (Inference Client RED): after CRM-3 the repository provides the same test tooling, and the existing tests already isolate the inference service's call to Chatterbox (`tests/test_ai_gateway_telemetry_red.py:46-47`). The RED tests isolate the Chatterbox call and the identity-token source within their own test code, making no network call. No prerequisite is missing, so no FOUNDATION milestone precedes CRM-4.
- No FOUNDATION milestone exists in this Plan.

### CRM-1 — Chatterbox Cloud Run Contract

- Capability / purpose: Define the changed externally observable behavior of the Chatterbox synthesize request, the inference service's cloning-failure answer, and the operator-set local settings.
- Rationale: The request shape, failure reasons and wording, and time-limit setting are deferred to the contract by the requirements; every later milestone depends on them.
- Milestone type: CONTRACT
- Predecessor: Plan approval.
- Scope: Write the contract artifact named under External Contract Requirements: verify the baseline against the repository, carry unchanged behavior over, and define changes 1–6 listed there, each traced to its requirement.
- Owned requirements / concerns: the three decisions the requirements defer to the contract (request shape for the sample audio; failure reasons and wording; time-limit setting name and form); the removal behavior of CCR-6 and the missing-sample answer; the caller identity requirement of CCR-7; the local settings for calling the private Chatterbox.
- Explicit exclusions: no Implementation Plan, test or code change; no change to the AI Gateway contract; no endpoint, field, validation or error beyond changes 1–6 and the carried-over baseline.
- Success criteria: the contract artifact exists, covers changes 1–6 and the verified baseline, and its Status records the user's approval; CRM-1's Execution Status row then points to it.

### CRM-2 — Chatterbox Service RED

- Capability / purpose: Tests that specify Chatterbox's new synthesize behavior, retention and one-at-a-time serving.
- Rationale: Chatterbox's request handling is verified on its own, with the model runtime isolated, before the inference service depends on it.
- Milestone type: RED
- Predecessor: CRM-1.
- Scope: Tests verifying that:
  - a synthesize request carrying the voice sample audio in the contract's shape is accepted and the sample conditions generation (CCR-6);
  - the sample path is no longer accepted, answered as the contract defines (CCR-6);
  - a missing or unusable voice sample is answered as the contract defines (CCR-6);
  - the carried-over text and language validation (RF-3) and generation-failure answer (RF-4) still hold under the new request shape;
  - after a response — success or failure — Chatterbox holds neither the voice sample nor the generated audio (CCR-10);
  - concurrent cloning requests are served one at a time, later requests waiting and then completing (Consistency and concurrency);
  - repeated identical requests each produce a new generation, with no duplicate detection (Consistency and concurrency — retry produces a new clip).
  The tests run without the model runtime, CUDA or model weights, isolating the model runtime boundary within test code.
- Owned requirements / concerns: none (verifies CCR-6, CCR-10, Consistency and concurrency, and the carried-over Chatterbox behavior).
- Explicit exclusions: no production change; no change to existing tests; no inference-service tests; no dependency, build or test-infrastructure change.
- Success criteria: the new tests fail because the approved Chatterbox behavior is missing — not because of import, configuration, dependency or environment errors — and every pre-existing test still passes.

### CRM-3 — Chatterbox Service GREEN

- Capability / purpose: Chatterbox accepts the voice sample audio, keeps no voice data, and serves one request at a time.
- Rationale: Smallest production change that makes CRM-2's evidence pass.
- Milestone type: GREEN
- Predecessor: CRM-2.
- Scope: The behavior that makes CRM-2's tests pass: Chatterbox's synthesize request takes the voice sample audio as the contract defines in place of the sample path; Chatterbox holds no voice sample or generated audio after responding; cloning requests are served one at a time with later requests waiting; carried-over validation and failure behavior stays as contracted.
- Owned requirements / concerns: CCR-6; CCR-10 (Chatterbox holds no voice data); Consistency and concurrency (one request at a time, others wait).
- Explicit exclusions: no inference-service change; no container, deployment or documentation change; no logging, metrics or alerts; no duplicate detection; no change to the health or metadata operations.
- Success criteria: CRM-2's tests pass and every verification command passes.

### CRM-4 — Inference Client RED

- Capability / purpose: Tests that specify the inference service's cloning call to the private Chatterbox and its failure reporting.
- Rationale: The inference service's client behavior — including the security change of attaching a caller identity — is verified on its own against the Chatterbox boundary.
- Milestone type: RED
- Predecessor: CRM-3.
- Scope: Tests verifying that, in voice cloning mode:
  - the request to Chatterbox carries the profile's locally stored voice sample audio itself in the contract's shape, and no sample path (CCR-5);
  - the request carries a Google identity token for the service account of the configured credential, for the configured Chatterbox, using the settings the contract defines (CCR-7);
  - for each failure reason the contract defines — including Chatterbox unreachable, access denied, Chatterbox error, bad response, and no backend configured — the inference service answers as CCR-8 and the contract require, with the contract's message for that reason (CCR-8, Dependency failure);
  - the cloning request is bounded by the configured time limit, 10 minutes when not otherwise set, using the setting the contract defines (CCR-9);
  - on success the generated audio is saved by the local app and served from it (CCR-10 local part, RF-13);
  - every test makes no network call.
  The existing test RF-14 describes is updated to expect the contract's no-backend message while keeping its status assertion. The existing test RF-15 describes is updated so it keeps exercising the voice cloning path under the new request and identity attachment, with all of its telemetry assertions unchanged.
- Owned requirements / concerns: none (verifies CCR-5, CCR-7, CCR-8, CCR-9, the Dependency failure characteristic, the local-save part of CCR-10, and the gateway telemetry behavior RF-15 covers).
- Explicit exclusions: no production change; no Chatterbox tests; no assertion of the existing tests weakened or removed beyond replacing RF-14's message wording with the contract's; no dependency, build or test-infrastructure change; no test of user login or authentication.
- Success criteria: the new and updated tests fail because the approved inference behavior is missing — not because of unrelated import, configuration, dependency or environment errors — and every other test passes.

### CRM-5 — Inference Client GREEN

- Capability / purpose: The inference service sends the sample audio with the service account's identity, within the configurable time limit, and reports why a cloning call failed.
- Rationale: Smallest production change that makes CRM-4's evidence pass.
- Milestone type: GREEN
- Predecessor: CRM-4.
- Scope: The behavior that makes CRM-4's tests pass: cloning requests carry the locally stored voice sample audio and the service account's Google identity token as the contract defines; each cloning request is bounded by the configurable limit defaulting to 10 minutes; each cloning failure is answered with the reason the contract defines; narration mode, local saving of generated audio, and the gateway's pass-through stay as they are.
- Owned requirements / concerns: CCR-5; CCR-7 (the inference service attaches the service account's identity token); CCR-8; CCR-9; Dependency failure characteristic.
- Explicit exclusions: no Chatterbox change; no frontend, voices-service or narration change; no AI Gateway contract change; no user login or authentication; no logging, metrics or alerts.
- Success criteria: CRM-4's tests pass and every verification command passes, including the preserved narration test listed under Current State.

### CRM-6 — Chatterbox Cloud Run Deployment Document

- Capability / purpose: A how-to for deploying Chatterbox privately to Cloud Run as the requirements specify, and for configuring the local inference service to call it.
- Rationale: Documentation and deployment-artifact work with no service behavior change; it documents settings CRM-1 defines and behavior CRM-3 and CRM-5 deliver.
- Milestone type: OTHER
- Predecessor: CRM-5.
- Scope: A deployment document, located as recorded under Non-Blocking Open Decisions, that describes how to: build the Chatterbox image; deploy it as a separate Cloud Run service (AGW-011) in project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, on an NVIDIA L4 GPU (CCR-1, CCR-3, CCR-4); make it private, callable only by `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` (CCR-7); let it scale to zero with at most 1 instance and one request at a time (Deployment, Consistency and concurrency); set a Cloud Run request time limit that accommodates the 10-minute cloning limit (CCR-9); and configure the local inference service with the settings the contract defines. Changes to the existing Chatterbox container build and deployment artifacts are included only where the documented steps cannot otherwise satisfy these items.
- Owned requirements / concerns: CCR-1; CCR-3; CCR-4; CCR-11; Deployment characteristic (scale to zero, at most 1 instance).
- No-behavior-change statement: the document and any container build or deployment artifact change alter no service's request handling, validation, failure answers or data handling; selecting the GPU device uses the existing device setting (RF-5). All behavior changes are delivered by CRM-3 and CRM-5.
- Baseline evidence: recorded before any change — the current deployment instructions' content (placeholder project and region, `--allow-unauthenticated`, CPU device, no GPU, instance-count or request-time-limit options; `cloudrun/chatterbox-service/README.md:5-14`), the image's CPU device setting (`cloudrun/chatterbox-service/Dockerfile:14`), the build-context exclusions (`.dockerignore:1-4`), and a full test-suite run passing.
- Preserved tests: the full suite — `test_voice_enrollment_creates_profile`, `test_generation_uses_selected_voice_profile`, `test_voice_cloning_returns_guidance_when_clone_backend_unavailable` and `test_gateway_execution_returns_non_placeholder_telemetry` as updated by CRM-4, the five tests in `tests/test_ai_gateway_red.py`, and the tests added by CRM-2 and CRM-4.
- Completion evidence: a checklist in the Implementation Plan's evidence showing where the document covers each item of AC-CCR-8 plus the request time limit and local configuration; no instruction to deploy publicly remains; the full suite passes; and, if this milestone changes the container build or the build-context exclusions, the Chatterbox image builds locally and, for an exclusions change, the harness image still builds and runs.
- Explicit exclusions: performing the deployment; any service behavior change; moving the voices service, inference service, frontend or narration to GCP; the inference-service Cloud Run artifacts; custom logging, metrics or alerts.
- Success criteria: the completion evidence above is recorded and every verification command passes.

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| CCR-1 (Chatterbox voice cloning on Cloud Run in the required project; only cloning on GCP) | CRM-6 | CRM-6 (completion evidence) |
| CCR-2 (voices service, inference service, frontend local; narration keeps Google TTS) | none — preserved | CRM-5 (preserved test `test_generation_uses_selected_voice_profile` in its full-suite run) |
| CCR-3 (region `asia-southeast1`) | CRM-6 | CRM-6 (completion evidence) |
| CCR-4 (NVIDIA L4 GPU) | CRM-6 | CRM-6 (completion evidence) |
| CCR-5 (sample audio sent with each request) | CRM-5 | CRM-4 |
| CCR-6 (sample path removed from Chatterbox's request; sample audio accepted instead) | CRM-3 | CRM-2 |
| CCR-7 (private Chatterbox; inference attaches the service account's identity token) | CRM-5 | CRM-4 |
| CCR-8 (failure answer states the reason) | CRM-5 | CRM-4 |
| CCR-9 (configurable 10-minute time limit) | CRM-5 | CRM-4 |
| CCR-10 (Chatterbox holds no voice sample or generated audio) | CRM-3 | CRM-2 |
| CCR-10 local part (generated audio saved by the local app, RF-13) | none — preserved | CRM-4 |
| CCR-11 (deployment document) | CRM-6 | CRM-6 (completion evidence) |
| Contract decision: request shape for the sample audio | CRM-1 | human review of CRM-1 |
| Contract decision: failure reasons and message wording | CRM-1 | human review of CRM-1 |
| Contract decision: name and form of the time-limit setting | CRM-1 | human review of CRM-1 |
| Contract: sample-path removal behavior and missing-sample answer; caller identity; local settings for the private Chatterbox | CRM-1 | human review of CRM-1 |
| Operational: Scale | none — not required | none |
| Operational: Deployment (scale to zero, at most 1 instance) | CRM-6 | CRM-6 (completion evidence) |
| Operational: Availability and latency — uptime (no expectation stated) | none — not required | none |
| Operational: Consistency and concurrency — one request at a time, others wait | CRM-3 | CRM-2 |
| Operational: Consistency and concurrency — a retried request produces a new clip | none — preserved | CRM-2 |
| Operational: Consistency and concurrency — no duplicate detection | none — exclusion | Final Review |
| Operational: Dependency failure (failure answer with reason) | CRM-5 | CRM-4 |
| Operational: Observability (beyond Cloud Run's default request logs) | none — not required | none |
| Carried-over Chatterbox validation and generation-failure behavior (RF-3, RF-4) | none — preserved | CRM-2 |
| Gateway telemetry on the voice cloning path (RF-15) | none — preserved | CRM-4 (updated existing test) |
| AGW-011 (Chatterbox as a separate Cloud Run service) — constraint | none — preserved | CRM-6 (completion evidence) |
| Exclusion: login and authentication of application users | none — exclusion | Final Review |
| Exclusion: performing the GCP deployment | none — exclusion | Final Review |
| Exclusion: moving the voices service, inference service, frontend or narration to GCP | none — exclusion | Final Review |

## Verification Commands

- Windows: `.\.venv\Scripts\python.exe -m pytest tests -ra` — source: `docs/developer-setup.md` ("Future RED commands, once approved tests exist") and `pytest.ini` (`testpaths = tests`). Used by every milestone except CRM-1.
- Linux: `.venv/bin/python -m pytest tests -ra` — source: `docs/developer-setup.md` ("Use the corresponding .venv/bin/python on Linux").
- CRM-6 only, if it changes the Chatterbox container build: `docker build -f cloudrun/chatterbox-service/Dockerfile -t chatterbox-model-api:local .` — source: `cloudrun/chatterbox-service/Dockerfile` with the image name of `cloudrun/chatterbox-service/README.md:6`, following the local `docker build` usage in `docs/developer-setup.md`.
- CRM-6 only, if it changes the build-context exclusions: `docker build -f containers/harness.Dockerfile -t vn-harness:foundation .` then `docker run --rm vn-harness:foundation` — source: `docs/developer-setup.md`.
- CRM-1 has no verification command; its deliverable is verified by human review.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| CRM-1 — Chatterbox Cloud Run Contract (CONTRACT) | Complete | `API-Contract.md` Contract Review Status: Approved by avinash2196 on 2026-11-09 (CCD-1–CCD-7 accepted). Human approval, not runtime verification, completes this CONTRACT milestone. |
| CRM-2 — Chatterbox Service RED (RED) | Complete | RED established on 2026-11-09 by `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2: C2-AC-1–C2-AC-5 met; 13 new tests fail on their own status assertions, 9 existing tests pass, in two consecutive full runs. See "CRM-2 Execution Evidence (revision 2)" below; the revision-1 stop is kept below for history. |
| CRM-3 — Chatterbox Service GREEN (GREEN) | Complete | GREEN verified on 2026-11-09 by `002_Implementation_Plan_Chatterbox_Service_GREEN.md`: C3-AC-1–C3-AC-4 met; `application.py` matches the planned content (SHA-256 `10cc955b…c54a`); 22 of 22 tests pass in two consecutive full runs; the 13 CRM-2 tests pass on their own. See "CRM-3 Execution Evidence" below. |
| CRM-4 — Inference Client RED (RED) | Complete | RED established on 2026-11-09 by `003_Implementation_Plan_Inference_Client_RED.md`: C4-AC-1–C4-AC-5 met; 4 files match the planned SHA-256; 71 collected, 51 fail on their own assertions (49 new cases, RF-14, RF-15), 20 pass, in two consecutive full runs. See "CRM-4 Execution Evidence" below. |
| CRM-5 — Inference Client GREEN (GREEN) | Complete | GREEN verified on 2026-11-10 by `004_Implementation_Plan_Inference_Client_GREEN.md`: C5-AC-1–C5-AC-4 met; `voice_narration/inference/application.py` matches the planned content (SHA-256 `4a98dafc…1088`); 71 of 71 tests pass in two consecutive full runs; the 51 CRM-4 RED tests pass on their own; the generic message no longer occurs under `voice_narration/`. See "CRM-5 Execution Evidence" below. |
| CRM-6 — Chatterbox Cloud Run Deployment Document (OTHER) | Pending | |

### CRM-2 Execution Evidence (stopped)

Executed on 2026-11-09 at commit `360846e` from `001_Implementation_Plan_Chatterbox_Service_RED.md` (approved by avinash2196 on 2026-11-09).

- Step 2: `git status --short` showed no change under `voice_narration/` or `tests/`.
- Step 3: `tests/test_chatterbox_service_red.py` was created by copying the plan's code block byte for byte (487 lines, LF, UTF-8). No other file was changed apart from this status record and the Implementation Plan's Human Review status.
- V1 `.\.venv\Scripts\python.exe -m pytest tests -ra` (exit 1):
  ```
  collected 22 items
  FAILED ... (C2-T1–C2-T13, all 13)
  ================== 13 failed, 9 passed, 1 warning in 16.62s ===================
  ```
  C2-T13 `test_synthesize_contract_answers_over_real_transport` did not fail on an assertion. It failed with `httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host`.
- V3 `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -q --tb=short` (exit 1, run before V2, see deviations): `13 failed, 1 warning in 4.10s`. Each test's first failure was a status `AssertionError`, as predicted: T1, T4, T9, T11, T12, T13 `assert 500 == 200`; T2, T6 `assert 500 == 400`; T5, T7 `assert 422 == 400`; T8, T10 `assert 500 == 503`; T3 `assert 200 == 422`.
- V2 `.\.venv\Scripts\python.exe -m pytest tests -ra` (repeat, no cleaning, exit 1): `collected 22 items`, `13 failed, 9 passed, 1 warning in 9.65s`. C2-T13 again failed with `httpx.ReadError: [WinError 10053] An established connection was aborted by the software in your host machine`, raised at `tests\test_chatterbox_service_red.py:479` (the second request, `rejected_path = client.post(...)`).
- V4 `git status --short`: the only new entries are `?? docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md`, `API-Contract.md`, `Plan.md`, and `?? tests/test_chatterbox_service_red.py`.

Result: C2-AC-1, C2-AC-2 and C2-AC-4 are met: the file is exact, 22 tests are collected, and the 9 existing tests passed in V1 and V2. C2-AC-3 and C2-AC-5 are not met. In two of three runs, C2-T13 ended with a transport error and not with its own assertion, and its result was not the same across runs.

Cause: under real `uvicorn`, the baseline route's `500` (the `UnicodeDecodeError` while building the `422` echo) makes the server close the connection. C2-T13 sends three requests on one `httpx.Client` before it asserts anything, so the second request may reuse the closed pooled connection. Whether it does is a race, which explains `assert 500 == 200` in V3 and `ReadError` in V1 and V2. The defect is in the approved test code of Implementation Plan 001, not in Plan scope or criteria.

Deviations: V3 was run before V2 (planned order V1, V2, V3), to see each test's failure after V1 showed the `ReadError`. No test, criterion or production file was changed. No pre-authorized contingency exists. Processes: only the pytest runs were started, and each exited with its uvicorn daemon threads. The new test file is left in place for review; rollback is to delete `tests/test_chatterbox_service_red.py`.

### CRM-2 Execution Evidence (revision 2)

Executed on 2026-11-09 at commit `360846e` from `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2 (Human Review: approved by avinash2196 on 2026-11-09, "Approve and re-run").

- Step 2 `git status --short`: only the four untracked entries (`001_Implementation_Plan_Chatterbox_Service_RED.md`, `API-Contract.md`, `Plan.md`, `tests/test_chatterbox_service_red.py`); no tracked file modified.
- Step 3 `sha256sum tests/test_chatterbox_service_red.py`: `7e7b443dca7f7660319723bef2d8a4e1521c23023d59e716fbc53ff1ba193921` (revision 1 content, 487 lines) — matches.
- Step 4: the plan's complete final code block was extracted (plan lines 211–700, LF) and written over the file. `sha256sum`: `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`, 490 lines — matches the plan. `diff` against the old file showed only the C2-T13 changes of the plan's unified diff.
- V1 `.\.venv\Scripts\python.exe -m pytest tests -ra` (exit 1):
  ```
  collected 22 items
  FAILED ... (C2-T1–C2-T13, all 13)
  ================== 13 failed, 9 passed, 1 warning in 21.12s ===================
  ```
  No `httpx` transport error, server start-up error or timeout in the output (count `0`). The only non-assertion error text is `uvicorn`'s captured `Exception in ASGI application` log for C2-T13 (the server-side source of the `500`, as the plan predicts).
- V2 `.\.venv\Scripts\python.exe -m pytest tests -ra` (repeat, no cleaning, exit 1): `collected 22 items`, `13 failed, 9 passed, 1 warning in 10.31s`; `FAILED` lines identical to V1 (`diff` printed nothing); transport-error count `0`; every failure location ends in `AssertionError`.
- V3 `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -q --tb=short` (exit 1): `13 failed, 1 warning in 4.54s`; first failing assertion per test, C2-T1 to C2-T13: `500 == 200`, `500 == 400`, `200 == 422`, `500 == 200`, `422 == 400`, `500 == 400`, `422 == 400`, `500 == 503`, `500 == 200`, `500 == 503`, `500 == 200`, `500 == 200`, `500 == 200` — exactly as predicted; transport-error count `0`.
- V4 `git status --short`: the same four untracked entries; no tracked file modified.

Result: C2-AC-1 (file exact, no other change), C2-AC-2 (22 collected, no collection/import/fixture error), C2-AC-3 (each new test fails with its own status `AssertionError`; no transport error), C2-AC-4 (the 9 pre-existing tests pass) and C2-AC-5 (V2 repeats V1) are met. The failures show the missing multipart request handling, `sample_path` rejection, empty-sample answer, retention and one-at-a-time serving: the unmodified route still expects a JSON body. New tests passing at RED: none, matching the plan's "Preserved-behavior tests (expected to pass at RED): none".

Deviations: one extra read-only command, `.\.venv\Scripts\python.exe -m pytest tests -q --co`, was run after V3 to list the 9 pre-existing test IDs; it changes nothing. Pre-authorized contingencies: none exist; none applied. Processes: only the pytest runs were started; each exited, and C2-T13's `uvicorn` server stopped in its own `finally`. Scratch files (extracted code block, run logs) are in the session scratchpad only. CRM-3 (GREEN) is not started and needs its own approved Implementation Plan.

### CRM-3 Execution Evidence

Executed on 2026-11-09 at commit `ac27993` from `002_Implementation_Plan_Chatterbox_Service_GREEN.md` (Human Review: approved by avinash2196 on 2026-11-09, "Approve and run").

- Step 2 `git status --short`: only `?? docs/.ai/chatterbox-cloud-run/002_Implementation_Plan_Chatterbox_Service_GREEN.md`. `git diff --quiet HEAD -- voice_narration/chatterbox_api/application.py`: exit `0`.
- Step 3 `sha256sum tests/test_chatterbox_service_red.py`: `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4` (matches).
- Step 4: the plan's complete final content (plan lines 310–454) was extracted with LF endings and written over `voice_narration/chatterbox_api/application.py`. `sha256sum`: `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a`, 145 lines (matches). `git diff` printed the expected `LF will be replaced by CRLF` warning. Its hunks have the same ranges as the plan (`@@ -2,13 +2,18 @@`, `@@ -18,19 +23,18 @@`, `@@ -40,6 +44,36 @@`, `@@ -51,39 +85,54 @@`), but Git adds function-name context to the hunk headers and aligns some lines inside the last hunk differently. The same comparison done the plan's way, `diff -u` from the committed file to the new file, matched the plan's unified diff exactly (`diff` printed nothing). Applying the plan's diff with `patch -p1` to the committed file gave SHA-256 `10cc955b…c54a`.
- C3-V1 `.\.venv\Scripts\python.exe -m pytest tests -ra` (exit 0):
  ```
  collected 22 items
  tests\test_ai_gateway_red.py .....
  tests\test_ai_gateway_telemetry_red.py .
  tests\test_chatterbox_service_red.py .............
  tests\test_clone_flow.py ...
  ======================== 22 passed, 1 warning in 5.04s ========================
  ```
  The one warning is the existing `StarletteDeprecationWarning` from `fastapi/testclient.py`.
- C3-V2 (repeat, no cleaning, exit 0): `collected 22 items`, `22 passed, 1 warning in 5.17s`; no `FAILED` or `ERROR` line.
- C3-V3 `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -q` (exit 0): `13 passed, 1 warning in 2.74s`.
- C3-V4 `git status --short`: ` M voice_narration/chatterbox_api/application.py`, `?? docs/.ai/chatterbox-cloud-run/002_Implementation_Plan_Chatterbox_Service_GREEN.md` (this checked state is before the status update).
- C3-V5 `git diff --stat`: `voice_narration/chatterbox_api/application.py | 123 ++++++++++++++++++--------`, `1 file changed, 86 insertions(+), 37 deletions(-)`. `git diff -- voice_narration/chatterbox_api/application.py` was byte-identical to the step-4 diff. No `+` or `-` line falls inside `health` or `metadata`; `def health` appears only as the hunk-header context and as an unchanged context line.

Result: C3-AC-1 (exact content; the RED test hash is unchanged; no other file changed), C3-AC-2 (22 collected and 22 passed: C2-T1–C2-T13 plus the 9 pre-existing tests), C3-AC-3 (the second run repeats the first) and C3-AC-4 (only `application.py` changed; `health` and `metadata` unchanged) are met. The 13 CRM-2 tests that failed at RED now pass, and the 9 pre-existing tests still pass. Known pre-existing failures: none named; none occurred.

Deviations: two read-only checks were added at step 4 because `git diff` lays out the hunks differently from the plan's `diff -u` output: a `diff -u` comparison and a `patch -p1` apply, both run in the session scratchpad. They change nothing in the repository. The commands planned for C3-V1–C3-V5 ran as planned, in the planned order. Pre-authorized contingencies: none exist; none applied. Processes: only the pytest runs were started; each exited, and C2-T13's `uvicorn` server stopped in its own `finally`. Scratch files are in the session scratchpad only. CRM-4 (RED) is not started and needs its own approved Implementation Plan.

### CRM-4 Execution Evidence

Executed on 2026-11-09 at commit `467b9f2` from `003_Implementation_Plan_Inference_Client_RED.md` (Human Review: approved by avinash2196 on 2026-11-09, "Approve plan").

- Step 2 `git status --short`: only `?? docs/.ai/chatterbox-cloud-run/003_Implementation_Plan_Inference_Client_RED.md`. `git diff --quiet HEAD -- tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py voice_narration/`: exit `0`. `tests/_chatterbox_boundary.py` and `tests/test_inference_client_red.py` did not exist.
- Step 3: the plan's four complete-content blocks (plan lines 196–592, 598–1177, 1202–1289, 1380–1459) were extracted with LF endings and written to `tests/_chatterbox_boundary.py` (397 lines), `tests/test_inference_client_red.py` (580), `tests/test_clone_flow.py` (88) and `tests/test_ai_gateway_telemetry_red.py` (80).
- Step 4 C4-V5 `sha256sum tests/_chatterbox_boundary.py tests/test_inference_client_red.py tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py`:
  ```
  7ef1a7bd05e3a273faf76eebca9973984000ff1ad5f408e550784865ca710608 *tests/_chatterbox_boundary.py
  fff78d051a09ec355ab465e8c2751b7c53d627d2b7d0139a8273c4691798314e *tests/test_inference_client_red.py
  84416efa942f57fd1675d4955f8e7546e6ff3c782978ee15d248d6c85870edb8 *tests/test_clone_flow.py
  ab285fd7f808bfa2358ef80c4ca6ba6e68afbbfc154d07c005f9d20455032f88 *tests/test_ai_gateway_telemetry_red.py
  ```
  All four match. `git diff -- tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py` printed the expected `LF will be replaced by CRLF` warnings and only the changed lines of the plan's two diffs (Git adds function-name context to hunk headers). `diff -u` from `git show HEAD:<file>` to each new file, compared with the plan's diff blocks (plan lines 1185–1196, 1297–1374): identical.
- C4-V1 `.\.venv\Scripts\python.exe -m pytest tests -ra` (exit 1):
  ```
  collected 71 items
  tests\test_ai_gateway_red.py .....
  tests\test_ai_gateway_telemetry_red.py F
  tests\test_chatterbox_service_red.py .............
  tests\test_clone_flow.py ..F
  tests\test_inference_client_red.py FFFF... (49 F)
  FAILED ... (51 lines: the 49 cases of tests/test_inference_client_red.py, RF-14, RF-15)
  ============= 51 failed, 20 passed, 1 warning in 61.79s (0:01:01) =============
  ```
  No `ERROR` line. The one warning is the existing `StarletteDeprecationWarning`. Count of `did not start`, `network access was attempted`, `ModuleNotFoundError`, `ImportError`, `TransportError`, `ReadError`, `ConnectError`, `RemoteProtocolError`, `fixture … not found`, `Traceback`: `0`.
- C4-V2 (repeat, no cleaning, exit 1): `collected 71 items`, `51 failed, 20 passed, 1 warning in 56.62s`; no `ERROR` line; `FAILED` lines identical to C4-V1 (`diff` printed nothing); error-text count `0`.
- C4-V3 `.\.venv\Scripts\python.exe -m pytest tests/test_inference_client_red.py tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable tests/test_ai_gateway_telemetry_red.py -q --tb=line` (exit 1): `51 failed, 1 warning in 44.39s`. First failing location per test, counted:
  ```
  42 test_inference_client_red.py:156: AssertionError   (assert_cloning_failed body: generic "Voice cloning service is unavailable. ..." != contract CFR message)
   7 test_inference_client_red.py:161: AssertionError   (assert_job_saved status: 503 generic message instead of 200)
   1 test_clone_flow.py:85: AssertionError              (exact CFR-1 comparison)
   1 test_ai_gateway_telemetry_red.py:70: AssertionError (503 instead of 202)
  ```
  The seven `:161` cases are C4-T1, the three C4-T2 cases, C4-T3, C4-T11 and C4-T18, as predicted. Error-text count `0`.
- C4-V4 `git status --short`: ` M tests/test_ai_gateway_telemetry_red.py`, ` M tests/test_clone_flow.py`, `?? docs/.ai/chatterbox-cloud-run/003_Implementation_Plan_Inference_Client_RED.md`, `?? tests/_chatterbox_boundary.py`, `?? tests/test_inference_client_red.py` (checked before this status update).

Result: C4-AC-1 (exact content of the four files; no other file changed), C4-AC-2 (71 collected, no collection, import or fixture error), C4-AC-3 (each of the 49 new cases, RF-14 and RF-15 fails with an `AssertionError` from its own or the `_Harness` assertions; no invalid-RED failure class occurred), C4-AC-4 (the 20 other tests pass: 13 CRM-2, 5 gateway, `test_voice_enrollment_creates_profile`, `test_generation_uses_selected_voice_profile`) and C4-AC-5 (C4-V2 repeats C4-V1) are met. The failures show the missing behavior: the unmodified inference service sends a tokenless JSON body, which the stand-in Chatterbox answers `401`, and answers every cloning failure with its single generic message instead of CFR-1–CFR-9. The CFR strings in the tests match `API-Contract.md` CFR-1–CFR-9 word for word. New tests passing at RED: none, matching the plan's "Preserved-behavior tests (expected to pass at RED): none". Known pre-existing failures: none named; none occurred.

Deviations: the commands were run from Git Bash as `./.venv/Scripts/python.exe -m pytest …` (same interpreter and arguments as the planned PowerShell form), with output written to session-scratchpad logs and searched with `grep`. Read-only checks added: the `diff -u` comparison with the plan's diff blocks at step 4, and the error-text and failure-location counts. Planned commands ran in the planned order (C4-V5, C4-V1, C4-V2, C4-V3, C4-V4). Pre-authorized contingencies: none exist; none applied. Processes: only the pytest runs were started; each exited, and the loopback `uvicorn` stand-ins stopped with their tests. Scratch files are in the session scratchpad only. CRM-5 (GREEN) is not started and needs its own approved Implementation Plan.

### CRM-5 Execution Evidence

Executed on 2026-11-10 at commit `575e85e` from `004_Implementation_Plan_Inference_Client_GREEN.md` (Human Review: approved by avinash2196 on 2026-11-10, "Approve plan").

- Step 2 `git status --short`: only `?? docs/.ai/chatterbox-cloud-run/004_Implementation_Plan_Inference_Client_GREEN.md`. `git diff --quiet HEAD -- voice_narration/ tests/`: exit `0`. `git show HEAD:voice_narration/inference/application.py | sha256sum`: `9d55caf9b6ff2111418e7e824608bd7bd286b1179fae806f9ac98b5373ea1caf` (matches).
- Step 3 C5-V1 (before): the five test-file hashes match the plan (`7ef1a7bd…0608`, `fff78d05…314e`, `84416efa…edb8`, `ab285fd7…2f88`, `2ce5b014…56d4`).
- Step 4: the plan's complete final content block was extracted with LF endings and written over `voice_narration/inference/application.py`. `sha256sum`: `4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088`, 473 lines (matches); no non-ASCII byte. `diff -u` from `git show HEAD:voice_narration/inference/application.py` to the new file (file-header timestamps removed) was byte-identical (`cmp`) to the plan's unified diff block.
- C5-V2 `.\.venv\Scripts\python.exe -m pytest tests -ra` (exit 0):
  ```
  collected 71 items
  tests\test_ai_gateway_red.py .....
  tests\test_ai_gateway_telemetry_red.py .
  tests\test_chatterbox_service_red.py .............
  tests\test_clone_flow.py ...
  tests\test_inference_client_red.py ..................................... (49 .)
  ======================= 71 passed, 1 warning in 58.68s ========================
  ```
  `FAILED`/`ERROR` line count `0`. The one warning is the existing `StarletteDeprecationWarning` from `fastapi/testclient.py:1`.
- C5-V3 (repeat, no cleaning, exit 0): `collected 71 items`, `71 passed, 1 warning in 42.18s`; `FAILED`/`ERROR` line count `0`.
- C5-V4 `.\.venv\Scripts\python.exe -m pytest tests/test_inference_client_red.py tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable tests/test_ai_gateway_telemetry_red.py -q` (exit 0): `51 passed, 1 warning in 38.62s`.
- C5-V1 (after): the five test-file hashes unchanged; `voice_narration/inference/application.py` `4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088`.
- C5-V5 `git status --short` (before this status update): ` M voice_narration/inference/application.py`, `?? docs/.ai/chatterbox-cloud-run/004_Implementation_Plan_Inference_Client_GREEN.md`. `git status --short` on `voice_narration/inference/providers`, `voice_narration/chatterbox_api`, `voice_narration/simple_voices`, `frontend`, `requirements-dev.txt`, `pytest.ini`, `cloudrun`, `docs/developer-setup.md` and `tests`: no output.
- C5-V6 `git diff --stat`: `voice_narration/inference/application.py | 112 ++++++++++++++++++++++++++-----`, `1 file changed, 95 insertions(+), 17 deletions(-)`, with the expected `LF will be replaced by CRLF` warning.
- C5-V7 `git grep -n "Voice cloning service is unavailable" -- voice_narration`: no output, exit `1`.

Result: C5-AC-1 (exact content; the five test hashes unchanged; no other file changed), C5-AC-2 (71 collected, 71 passed: the 51 tests that failed at CRM-4 and the 20 that passed there, including the preserved narration test `test_generation_uses_selected_voice_profile`; no `FAILED` or `ERROR` line), C5-AC-3 (the second run repeats the first) and C5-AC-4 (generic message gone) are met. The previously valid RED behavior (51 failing tests) is now GREEN. Known pre-existing failures: none named; none occurred.

Deviations: the commands were run from Git Bash as `./.venv/Scripts/python.exe -m pytest …` (same interpreter and arguments as the planned PowerShell form), with output written to session-scratchpad logs and searched with `grep`. Read-only checks added: the `cmp` of the `diff -u` output with the plan's diff block, the non-ASCII byte check, the out-of-scope-path `git status`, and the `FAILED`/`ERROR` counts. Planned commands ran in the planned order (step 2, C5-V1, step 4, C5-V2, C5-V3, C5-V4, C5-V1, C5-V5, C5-V6, C5-V7). Pre-authorized contingencies: none exist; none applied. Processes: only the pytest runs were started; each exited, and the loopback stand-ins stopped with their tests. Scratch files are in the session scratchpad only. CRM-6 (OTHER) is not started and needs its own approved Implementation Plan.

## Risks

- RSK-1 — Model runtime absent locally: the Chatterbox model API imports its model runtime at module load (`voice_narration/chatterbox_api/application.py:7-13`), and that runtime is not installed in the local environment (Current State). Mitigation: CRM-2's tests isolate the model runtime boundary within test code, as `docs/developer-setup.md` permits; CRM-2's success criteria reject import or environment failures as RED evidence.
- RSK-2 — Waiting requests rejected by the platform: with at most one instance, requests arriving while the instance is busy may be rejected by Cloud Run instead of waiting, and Chatterbox today does not serialize generation (`voice_narration/chatterbox_api/application.py:63-72`). Mitigation: one-at-a-time serving with waiting is Chatterbox behavior owned by CRM-3, and CRM-6 documents instance and per-instance request settings consistent with it.
- RSK-3 — Platform request time limit shorter than CCR-9: the existing deployment instructions set no request time limit (`cloudrun/chatterbox-service/README.md:7-13`). Mitigation: CRM-6's scope includes a Cloud Run request time limit that accommodates the 10-minute cloning limit.
- RSK-4 — Cold start inside the time limit: the model is loaded on first use (`voice_narration/chatterbox_api/application.py:36-40`) and the image does not include model weights (`cloudrun/chatterbox-service/Dockerfile:9-12`), so a cold start after scale to zero includes model loading. Mitigation: CRM-6's document states the cold-start behavior; if a cold start cannot fit within CCR-9's limit, that is a replanning question, not a change made inside a milestone.
- RSK-5 — Image build context: the build-context exclusions admit only `requirements-dev.txt` and `containers/` (`.dockerignore:1-4`) while the image copies the application package (`cloudrun/chatterbox-service/Dockerfile:12`), so the documented build may not include the application. Mitigation: CRM-6 may change the container build artifacts only where the documented steps need it, and if it changes the shared exclusions it verifies the harness image still builds and runs.
- RSK-6 — Google libraries not declared: the inference service already relies on Google client libraries (`voice_narration/inference/providers/google.py:8`) that are installed locally but not declared in `requirements-dev.txt`. This Plan does not change dependency declarations; the CRM-4 and CRM-5 Implementation Plans state which installed packages their code relies on.
- RSK-7 — Changed message seen by other consumers: the cloning-failure message is shown by the frontend (`frontend/src/App.jsx:127-129`) and passed through by the gateway (`voice_narration/inference/application.py:363-366`). Mitigation: the message wording is a CRM-1 decision under human review; the gateway's error shape stays as approved.
- RSK-8 — Voice cloning not reachable from the frontend: the frontend's generation request sends no mode (`frontend/src/App.jsx:116-124`), so it always uses narration; no requirement of this work item changes the frontend. Voice cloning is exercised through the inference service's job-creation operation or the gateway execution operation.
- RSK-9 — Retry wording and gateway replay: the requirements record that "A retried request produces a new clip; no duplicate detection is required" for Chatterbox cloning requests. The approved AI Gateway contract replays the original response for a repeated idempotency key (`docs/.ai/ai-gateway-multimodel/contract/API-Contract.md:125`, `voice_narration/inference/application.py:338-343`). This Plan applies the retry statement to Chatterbox and does not change the gateway's idempotency behavior; the user confirms or corrects this reading at Plan review.

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| Voice cloning requests from the local inference service are served by Chatterbox on Cloud Run in project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, on an NVIDIA L4 GPU, when deployed as documented | AC-CCR-1 | CRM-6 completion evidence and Final Review inspection of the deployment document (the deployment itself is excluded); CRM-5 evidence that cloning requests go to the configured Chatterbox |
| Narration keeps generating audio with Google TTS locally; voices service, inference service and frontend run locally | AC-CCR-2 | CRM-5 full-suite evidence (preserved test `test_generation_uses_selected_voice_profile`) and Final Review inspection that no local service was moved |
| A voice cloning request sends the sample audio itself; Chatterbox's synthesize request no longer accepts the sample path | AC-CCR-3 | CRM-3 (Chatterbox side) and CRM-5 (inference side) completion evidence |
| Chatterbox rejects calls without a valid identity token for the service account; the inference service attaches that account's token | AC-CCR-4 | CRM-5 completion evidence (token attached); Final Review inspection of CRM-6's document (Cloud Run rejection, since the deployment is excluded) |
| Unreachable, access denied, Chatterbox failure or bad response each produce the failure answer stating which happened | AC-CCR-5 | CRM-5 completion evidence |
| A voice cloning request is limited to a configurable 10-minute limit | AC-CCR-6 | CRM-5 completion evidence; CRM-6 completion evidence for the documented Cloud Run request time limit |
| Chatterbox keeps no voice sample or generated audio after responding; generated audio is saved by the local app | AC-CCR-7 | CRM-3 completion evidence (no retention) and CRM-5 completion evidence (local save) |
| A deployment document describes deploying Chatterbox to satisfy CCR-1, CCR-3, CCR-4, CCR-7 and the Deployment characteristic | AC-CCR-8 | CRM-6 completion evidence and Final Review inspection |
| Each milestone meets its success criteria; after CRM-6 every verification command passes | Plan success criteria | CRM-6 completion evidence (full suite) and each milestone's Execution Status evidence |
