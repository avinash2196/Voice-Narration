# Plan — ai-gateway-multimodel

## Status

Approved by avinash2196 on 2026-11-08. Revised Plan approval recorded by the main conversation after incorporating a separate Cloud Run-hosted Chatterbox model API milestone. Telemetry-remediation revision approved by avinash2196 on 2026-11-09 based on Final Review finding FR-AGW-001. Completed milestone evidence remains unchanged.

## Objective

Introduce a dedicated AI Gateway execution boundary for narration/voice-cloning model runs, starting with Chatterbox and preserving extensibility for additional models, while enforcing commercial-use gating, self-hosted runtime operation, Hindi/English support, and separate Cloud Run-hosted model API deployment. [Artifact: ai-gateway-multimodel/requirements.md AGW-001..AGW-011]

## Current State

Repository inspection shows model execution is currently hard-coded in the inference service (`GoogleVoiceProvider` is instantiated directly during job creation), with no gateway routing layer. Existing frontend and service calls target voice and inference services directly, and current tests validate enrollment/generation flow but not multi-model gateway behavior. [Repo: voice_narration/inference/application.py:14] [Repo: voice_narration/inference/application.py:108] [Repo: frontend/src/App.jsx:3] [Repo: frontend/src/App.jsx:4] [Repo: frontend/src/App.jsx:116] [Repo: tests/test_clone_flow.py:7] [Repo: tests/test_clone_flow.py:23]

## In Scope

- Dedicated AI Gateway service boundary for model execution requests (narration + cloning paths). [Artifact: ai-gateway-multimodel/requirements.md AGW-001]
- Extensible adapter/policy architecture enabling future models without consumer API break. [Artifact: ai-gateway-multimodel/requirements.md AGW-002]
- Initial production adapter targeting Chatterbox. [Artifact: ai-gateway-multimodel/requirements.md AGW-003]
- Commercial-use governance and runtime self-hosting constraints for model enablement. [Artifact: ai-gateway-multimodel/requirements.md AGW-004] [Artifact: ai-gateway-multimodel/requirements.md AGW-005]
- Hindi/English routing support and gateway decision/usage observability. [Artifact: ai-gateway-multimodel/requirements.md AGW-006] [Artifact: ai-gateway-multimodel/requirements.md AGW-009]
- Deterministic failure/fallback behavior under model unavailability/disallow states. [Artifact: ai-gateway-multimodel/requirements.md AGW-010]
- Separate Cloud Run-hosted Chatterbox model API consumed by gateway runtime routing. [Artifact: ai-gateway-multimodel/requirements.md AGW-011]

## Out of Scope

- Enabling all future models in this first work item; this starts with Chatterbox and extensibility scaffolding only. [Artifact: ai-gateway-multimodel/requirements.md Explicit Exclusions]
- Bypassing commercial-use evidence gates for any model. [Artifact: ai-gateway-multimodel/requirements.md Explicit Exclusions]
- Introducing mandatory third-party runtime model APIs for core generation. [Artifact: ai-gateway-multimodel/requirements.md Explicit Exclusions]

## Requirements and Constraints

- Requirements authority is `docs/.ai/ai-gateway-multimodel/requirements.md` (approved 2026-11-08). [Artifact: ai-gateway-multimodel/requirements.md Status]
- Gateway must become the model execution boundary and own routing policy decisions. [Artifact: ai-gateway-multimodel/requirements.md AGW-001] [Artifact: ai-gateway-multimodel/requirements.md AGW-007]
- Chatterbox is first adapter; additional adapters must be addable without consumer API break. [Artifact: ai-gateway-multimodel/requirements.md AGW-002] [Artifact: ai-gateway-multimodel/requirements.md AGW-003]
- Production model enablement requires verified commercial permissions for code, weights, and output-use terms. [Artifact: ai-gateway-multimodel/requirements.md AGW-004]
- Approved runtime must be self-hosted for core generation and support Hindi/English routing. [Artifact: ai-gateway-multimodel/requirements.md AGW-005] [Artifact: ai-gateway-multimodel/requirements.md AGW-006]
- Initial deployment topology requires a separate Cloud Run-hosted Chatterbox model API behind gateway routing. [Artifact: ai-gateway-multimodel/requirements.md AGW-011]

## Non-Blocking Open Decisions

- UI exposure of model selection controls is deferred and does not block backend gateway architecture approval. [Artifact: ai-gateway-multimodel/requirements.md Non-Blocking Decisions]
- Token-optimization strategy for non-TTS/other future model types is deferred and does not block baseline gateway delivery. [Artifact: ai-gateway-multimodel/requirements.md Non-Blocking Decisions]

## External Contract Requirements

This work item introduces a new service boundary and request/response behavior for model execution routing. A CONTRACT milestone is required first to define the gateway interface before repository-changing milestones.

Contract artifact must define:
- request/response schema for gateway execution requests carrying full generation context (script, profile/model hints, controls, metadata, idempotency context); [Artifact: ai-gateway-multimodel/requirements.md AGW-008]
- routing decision outputs and observability fields surfaced to callers/operators; [Artifact: ai-gateway-multimodel/requirements.md AGW-007] [Artifact: ai-gateway-multimodel/requirements.md AGW-009]
- deterministic error/failure taxonomy and fallback signaling behavior; [Artifact: ai-gateway-multimodel/requirements.md AGW-010]
- model enablement governance fields/states proving commercial eligibility and runtime policy compliance; [Artifact: ai-gateway-multimodel/requirements.md AGW-004] [Artifact: ai-gateway-multimodel/requirements.md AGW-005]
- backward-compatibility expectations for current consumers while migration moves direct provider use behind gateway.

## Milestones

Split: separate engineering decision (contract first), different risk (runtime deployment boundary), and ordering (tests before implementation).

### 1. AI Gateway Contract

- Capability / purpose: Define the externally consumed execution contract for the gateway boundary and migration-compatible behavior.
- Rationale: Interface/routing/error/governance semantics must be reviewed before implementation.
- Milestone type: CONTRACT.
- Predecessor: Plan approval.
- Scope:
  - Deliver gateway contract artifact covering execution request/response, routing decision metadata, deterministic error/fallback semantics, and governance states required to gate model enablement.
- Owned requirements / concerns: AGW-001, AGW-007, AGW-008, AGW-009, AGW-010 (contract decisions).
- Explicit exclusions: Executable source/test/configuration changes.
- Success criteria: Contract artifact is complete and explicitly approved by the user.

### 2. Chatterbox Commercial & Feasibility Evidence

- Capability / purpose: Produce licensing and feasibility evidence for Chatterbox under commercial/self-hosted/Hindi-English constraints.
- Rationale: This is evidence/documentation work that must complete before executable enablement behavior is implemented.
- Milestone type: OTHER.
- Predecessor: AI Gateway Contract.
- Scope:
  - Produce evidence artifact(s) for Chatterbox code/weights/output-use commercial eligibility, self-hosted runtime feasibility, and Hindi/English suitability expectations used by later executable milestones.
- Owned requirements / concerns: AGW-003, AGW-004, AGW-005, AGW-006 (evidence gating).
- Explicit exclusions: Production behavior change and runtime model-enablement behavior.
- Success criteria: Evidence artifacts and checks are complete, reviewed, and all verification commands pass.
- No-behavior-change statement: This milestone records and validates evidence only; it does not change production runtime behavior.
- Baseline evidence: Current repository contains no approved Chatterbox commercial/feasibility evidence artifact for this work item.
- Preserved tests: Existing clone flow regression command (`pytest -q tests\test_clone_flow.py`) remains passing.
- Completion evidence: Cited evidence artifact(s) plus passing preserved check output recorded in Plan execution evidence.

### 3. AI Gateway Routing & Governance RED

- Capability / purpose: Establish failing tests/checks for required gateway behavior before implementation.
- Rationale: Behavioral changes must be driven by failing RED evidence.
- Milestone type: RED.
- Predecessor: Chatterbox Commercial & Feasibility Evidence.
- Scope:
  - Tests/checks only for gateway-bound model execution path, pluggable adapter/routing policy behavior, bilingual routing support, governance rejection when commercial evidence is absent, and deterministic fallback/failure signaling.
- Owned requirements / concerns: Verification only — AGW-001..AGW-010.
- Explicit exclusions: Production implementation, dependency/bootstrap changes, runtime config migrations, and non-test behavior changes.
- Success criteria: RED checks fail for missing approved behavior only (or intentionally absent implementation interfaces), with no unrelated environment/configuration failure.

### 4. Chatterbox Cloud Run Model API Deployment

- Capability / purpose: Deploy Chatterbox as a separate Cloud Run-hosted model API and integrate it as gateway execution backend target.
- Rationale: Deployment/runtime boundary carries operational risk separate from gateway policy logic and needs an explicit gate.
- Milestone type: OTHER.
- Predecessor: AI Gateway Routing & Governance RED.
- Scope:
  - Deliver deployment/runtime integration for separate Cloud Run model API endpoint consumed by gateway execution path, with no expansion to non-Chatterbox models.
- Owned requirements / concerns: AGW-011.
- Explicit exclusions: New model features, additional model adapters, and UI changes.
- Success criteria: Deployment integration evidence and preserved checks pass; gateway execution path targets separate model API backend.
- No-behavior-change statement: This milestone changes runtime topology/integration boundary while preserving approved functional behavior and contract semantics.
- Baseline evidence: RED milestone shows gateway contract behavior missing; separate model API integration is not yet present.
- Preserved tests: `pytest -q tests\test_clone_flow.py` and gateway contract tests established by RED scope.
- Completion evidence: Deployment configuration/integration evidence plus passing preserved checks recorded in Plan execution evidence.

### 5. AI Gateway Routing & Governance GREEN

- Capability / purpose: Implement the behavior required by RED for gateway routing/governance/chatterbox-first execution.
- Rationale: Deliver only the approved behavior established by predecessor RED.
- Milestone type: GREEN.
- Predecessor: Chatterbox Cloud Run Model API Deployment.
- Scope:
  - Deliver gateway execution boundary, extensible adapter architecture, Chatterbox-first adapter path, governance checks, bilingual routing support, observability metadata, and deterministic fallback behavior as defined by approved contract and RED checks.
- Owned requirements / concerns: AGW-001..AGW-010.
- Explicit exclusions: Additional future-model implementations beyond required extensibility and unrelated feature scope.
- Success criteria: RED checks and preserved regression checks pass with evidence mapped to owned requirements.

### 6. Gateway Telemetry Fidelity RED

- Capability / purpose: Establish failing checks for telemetry quality required by AGW-009 and Final Review finding FR-AGW-001.
- Rationale: Existing telemetry placeholders need behavior-driven correction with explicit failing evidence.
- Milestone type: RED.
- Predecessor: AI Gateway Routing & Governance GREEN.
- Scope:
  - Tests/checks only for execution telemetry fidelity (non-placeholder latency/compute, structured cost estimate, deterministic runtime metadata) on successful gateway execution.
- Owned requirements / concerns: Verification only — AGW-009 follow-up finding FR-AGW-001.
- Explicit exclusions: Production behavior changes, dependency changes, and non-test modifications.
- Success criteria: RED checks fail for in-scope missing telemetry fidelity only.

### 7. Gateway Telemetry Fidelity GREEN

- Capability / purpose: Implement telemetry fidelity behavior required by RED.
- Rationale: Close FR-AGW-001 before work-item closure.
- Milestone type: GREEN.
- Predecessor: Gateway Telemetry Fidelity RED.
- Scope:
  - Replace placeholder telemetry values in gateway successful execution responses with measured latency/compute values and deterministic cost-estimate formatting, preserving existing contract fields.
- Owned requirements / concerns: AGW-009 follow-up finding FR-AGW-001.
- Explicit exclusions: New gateway APIs, routing-policy changes, and non-telemetry behavior scope.
- Success criteria: Telemetry RED checks and preserved regression checks pass with evidence.

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| AGW-001 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-002 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-003 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-004 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-005 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-006 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-007 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-008 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-009 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-010 | AI Gateway Routing & Governance GREEN | AI Gateway Routing & Governance RED |
| AGW-011 | Chatterbox Cloud Run Model API Deployment | Chatterbox Cloud Run Model API Deployment |
| FR-AGW-001 telemetry fidelity finding | Gateway Telemetry Fidelity GREEN | Gateway Telemetry Fidelity RED |
| Contract decision surface for gateway execution | AI Gateway Contract | Human review of contract artifact |
| Chatterbox evidence gate artifacts | Chatterbox Commercial & Feasibility Evidence | Same milestone evidence and preserved checks |

## Verification Commands

- `pytest -q tests\test_clone_flow.py` — source: repository existing regression command path and tests present; used as preserved behavior check in OTHER/RED/GREEN milestones where applicable. [Repo: tests/test_clone_flow.py:7] [Repo: tests/test_clone_flow.py:23]
- Milestone-specific RED/GREEN commands are established in each approved Implementation Plan using the existing pytest runner and selectors appropriate to introduced gateway tests.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| AI Gateway Contract | Complete | `contract/API-Contract.md` Contract Review Status approved by avinash2196 on 2026-11-08. |
| Chatterbox Commercial & Feasibility Evidence | Complete | Executed via `001_Implementation_Plan_Chatterbox_Commercial_and_Feasibility_Evidence.md`; evidence artifacts: `model-eval/chatterbox-commercial-evidence.md`, `model-eval/chatterbox-feasibility.md`; preserved check passed. |
| AI Gateway Routing & Governance RED | Complete | Executed via `002_Implementation_Plan_AI_Gateway_Routing_and_Governance_RED.md`; RED evidence established by failing gateway contract tests due to missing `/ai-gateway/v1/*` routes (in-scope missing behavior), while preserved checks passed. |
| Chatterbox Cloud Run Model API Deployment | Complete | Executed via `004_Implementation_Plan_Chatterbox_Cloud_Run_Model_API_Deployment.md`; separate Chatterbox API service and Cloud Run deployment artifacts added, inference integration seam implemented, preserved checks passed. |
| AI Gateway Routing & Governance GREEN | Complete | Executed via `003_Implementation_Plan_AI_Gateway_Routing_and_Governance_GREEN.md`; gateway contract endpoints, governance transitions, idempotency, deterministic error envelope, and routing behavior implemented; RED suite now passes. |
| Gateway Telemetry Fidelity RED | Complete | Executed via `005_Implementation_Plan_Gateway_Telemetry_Fidelity_RED.md`; telemetry fidelity test introduced and failed on placeholder telemetry (`latency_ms=0`). |
| Gateway Telemetry Fidelity GREEN | Complete | Executed via `006_Implementation_Plan_Gateway_Telemetry_Fidelity_GREEN.md`; telemetry values now measured/non-placeholder and telemetry test passes. |
| Final Review | Written — awaiting user decision | `Final-Review.md` created for work item verdict, FAC evidence mapping, findings, and recommendation. |

Execution Evidence — 2026-11-08 (Milestone 2)
- `pytest -q tests\test_clone_flow.py`
  - Output: `2 passed in 2.60s`

Execution Evidence — 2026-11-08 (Milestone 3 RED)
- `pytest -q tests\test_clone_flow.py`
  - Output: `2 passed in 2.24s`
- `pytest -q tests\test_ai_gateway_red.py`
  - Output summary: `5 failed in 1.90s`
  - Failure shape: all failing assertions returned `404 {"detail":"Not Found"}` for `/ai-gateway/v1/executions` and `/ai-gateway/v1/models*`, confirming missing gateway contract behavior in current implementation.

Execution Evidence — 2026-11-08 (Milestone 4 OTHER)
- `pytest -q tests\test_clone_flow.py`
  - Output: `2 passed in 4.80s`
- `pytest -q tests\test_ai_gateway_red.py`
  - Output summary: `5 failed in 6.04s`
  - Failure shape preserved from RED baseline (`404 Not Found` for `/ai-gateway/v1/*`) and accepted for this milestone because AGW-001..AGW-010 delivery remains owned by milestone 5 GREEN.
- `python -m compileall voice_narration\chatterbox_api voice_narration\inference\application.py`
  - Output: compiled `voice_narration\chatterbox_api\__init__.py`, `__main__.py`, `application.py`, and `voice_narration\inference\application.py` successfully.

Execution Evidence — 2026-11-08 (Milestone 5 GREEN)
- `pytest -q tests\test_clone_flow.py`
  - Output: `2 passed in 4.70s`
- `pytest -q tests\test_ai_gateway_red.py`
  - Output: `5 passed in 2.73s`

Execution Evidence — 2026-11-09 (Milestone 6 RED)
- `pytest -q tests\test_clone_flow.py`
  - Output: `2 passed in 4.21s`
- `pytest -q tests\test_ai_gateway_red.py`
  - Output: `5 passed in 1.97s`
- `pytest -q tests\test_ai_gateway_telemetry_red.py`
  - Output summary: `1 failed in 4.25s`
  - Failure shape: `usage["latency_ms"]` was `0`, confirming placeholder telemetry values.

Execution Evidence — 2026-11-09 (Milestone 7 GREEN)
- `pytest -q tests\test_clone_flow.py`
  - Output: `2 passed in 2.25s`
- `pytest -q tests\test_ai_gateway_red.py`
  - Output: `5 passed in 1.02s`
- `pytest -q tests\test_ai_gateway_telemetry_red.py`
  - Output: `1 passed in 2.05s`

## Risks

- Chatterbox licensing ambiguity risk: commercial eligibility may be unclear across code/weights/output-use dimensions, blocking enablement until explicit evidence is approved. [Artifact: ai-gateway-multimodel/requirements.md AGW-004]
- Runtime feasibility risk: self-hosted bilingual quality/latency may not meet expectations in current environment, requiring policy fallback or additional model onboarding. [Artifact: ai-gateway-multimodel/requirements.md AGW-005] [Artifact: ai-gateway-multimodel/requirements.md AGW-006]
- Migration risk: replacing direct provider invocation with a gateway boundary can regress existing flow if contract compatibility is incomplete. [Repo: voice_narration/inference/application.py:108] [Repo: frontend/src/App.jsx:116]

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| Model execution for narration/cloning is gateway-mediated, not direct provider invocation from product services | AC-AGW-001 | AI Gateway Routing & Governance GREEN |
| Chatterbox executes via approved gateway routing policy | AC-AGW-002 | AI Gateway Routing & Governance GREEN |
| Adding another adapter preserves consumer contract | AC-AGW-003 | AI Gateway Routing & Governance GREEN |
| Non-eligible model enablement is blocked by commercial governance checks | AC-AGW-004 | AI Gateway Routing & Governance GREEN |
| Core runtime does not depend on external model APIs | AC-AGW-005 | AI Gateway Routing & Governance GREEN |
| Hindi/English requests route with decision metadata captured | AC-AGW-006 | AI Gateway Routing & Governance GREEN |
| Deterministic fallback/failure behavior on model unavailability/disallow | AC-AGW-007 | AI Gateway Routing & Governance GREEN |
| Chatterbox is deployed as separate Cloud Run API behind gateway backend routing | AC-AGW-008 | Chatterbox Cloud Run Model API Deployment |
| Gateway execution telemetry includes non-placeholder measured values suitable for governance troubleshooting | Final Review finding FR-AGW-001 | Gateway Telemetry Fidelity GREEN |
