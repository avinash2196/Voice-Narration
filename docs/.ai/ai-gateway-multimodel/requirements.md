# Requirements — ai-gateway-multimodel

Every item ends with one source label:

- `[User: brief]` = stated by the user in this work item request.
- `[User: Qn]` = answer to clarification question n in this work item.
- `[Repo: path:line]` = established by repository inspection during this capture.

## Goal

Define requirements for a dedicated AI Gateway service that becomes the single model-execution boundary for narration/voice-cloning requests, starts with Chatterbox, remains extensible for additional models, supports Hindi and English, and can be used commercially without third-party runtime model APIs. [User: brief]

## Status

Approved by avinash2196 on 2026-11-08. Revised artifact approval recorded by the main conversation after adding the separate Cloud Run-hosted Chatterbox API deployment requirement. This artifact does not authorize a Plan, contract, Implementation Plan, test, or code change.

## Repository-Confirmed Facts

- The current inference service directly instantiates `GoogleVoiceProvider` in request handling (`provider = GoogleVoiceProvider()`), so model routing is hard-coded today. [Repo: voice_narration/inference/application.py:14] [Repo: voice_narration/inference/application.py:108]
- The current inference provider export list includes only `GoogleVoiceProvider` as the active provider surface. [Repo: voice_narration/inference/providers/__init__.py:2] [Repo: voice_narration/inference/providers/__init__.py:4]
- A mock provider class exists (`MockVoiceCloneProvider`) but is not the active inference path. [Repo: voice_narration/inference/providers/mock.py:14] [Repo: voice_narration/inference/application.py:108]
- Frontend currently calls voice and inference services directly over separate base URLs, with no gateway endpoint in between. [Repo: frontend/src/App.jsx:3] [Repo: frontend/src/App.jsx:4] [Repo: frontend/src/App.jsx:116]
- Existing tests cover enrollment and generation flow but do not verify multi-model routing/governance behavior. [Repo: tests/test_clone_flow.py:7] [Repo: tests/test_clone_flow.py:23]

## Requirements

- AGW-001 (Gateway boundary): All model-execution requests for narration generation and voice cloning must go through a dedicated AI Gateway service; product services must not call model runtimes directly once migrated. [User: brief]
- AGW-002 (Extensible multi-model architecture): The gateway must support pluggable model adapters and policy-based model selection so additional models can be added later without breaking consumer APIs. [User: brief]
- AGW-003 (Initial model): The first supported production adapter in this work item is Chatterbox. [User: brief]
- AGW-004 (Commercial-use gate): A model cannot be enabled for production unless code, weights, and output-use terms are verified as commercially permissible with cited evidence. [User: brief]
- AGW-005 (No third-party runtime dependency): Runtime inference for approved models must be self-hosted in project-controlled infrastructure; external model APIs are not required for core generation. [User: brief]
- AGW-006 (Bilingual support): The gateway must support Hindi and English generation requests, including mixed operational support needed for both languages. [User: brief]
- AGW-007 (Routing policy ownership): The gateway must own model selection/routing decisions using configurable policy inputs (for example capability, latency, quality tier, cost guardrails, availability). [User: brief]
- AGW-008 (Pass-through context): Upstream services must be able to pass all required generation context (script, profile/model hints, controls, request metadata, idempotency identifiers) to the gateway in one contract-defined request. [User: brief]
- AGW-009 (Cost/usage observability): The gateway must emit per-request usage and decision metadata sufficient for cost/latency/quality governance and operator troubleshooting. [User: brief]
- AGW-010 (Failure/fallback behavior): The gateway must expose deterministic failure classification and support policy-defined fallback behavior when a selected model is unavailable or disallowed. [User: brief]
- AGW-011 (Separate model service deployment): Chatterbox must run as a separate self-hosted Cloud Run service exposing an API consumed by the AI Gateway, so model runtime can evolve independently from gateway policy logic. [User: Q2]

## Operational Characteristics

| Characteristic | Answer | Source |
|----------------|--------|--------|
| Initial enabled model | Chatterbox | [User: brief] |
| Future model support | Required; add without consumer API break | [User: brief] |
| Runtime dependency policy | Self-hosted inference; no required external model API | [User: brief] |
| Language scope | Hindi and English | [User: brief] |
| Commercial readiness gate | Mandatory license/output-use verification before enablement | [User: brief] |
| Initial deployment topology | Separate Cloud Run-hosted Chatterbox model API behind AI Gateway | [User: Q2] |
| Current architecture starting point | Direct service-to-provider call, no gateway boundary | [Repo: voice_narration/inference/application.py:108] |

## Decisions Deferred to Later Milestones

- Final gateway request/response schema, error taxonomy, and compatibility guarantees are deferred to a CONTRACT milestone if API surface changes are introduced. [User: brief]
- Concrete model-routing algorithm and thresholds are deferred to implementation milestones after baseline policy requirements are approved. [User: brief]
- Chatterbox benchmarking thresholds (Hindi/English quality, latency, cost envelopes) are deferred to a model-feasibility/evaluation milestone. [User: brief]

## Explicit Exclusions

- This work item does not authorize immediate migration to all possible model backends in one step; it starts with Chatterbox and extensibility scaffolding. [User: brief]
- This work item does not authorize bypassing the commercial-use gate for any model. [User: brief]
- This work item does not authorize introducing mandatory third-party runtime model APIs for core generation. [User: brief]

## Non-Blocking Decisions

- Token-optimization strategy details for non-TTS models are left to later optimization work once gateway baseline routing is in place. [Left to optimization phase — non-blocking]
- UI-level model-selection exposure (if any) is left to later UX decisions; this work item requires backend policy support first. [Left to UX phase — non-blocking]

## Acceptance Criteria

- AC-AGW-001: Given a generation request, the request reaches the AI Gateway and model execution is invoked through gateway adapter logic rather than direct provider calls from product services. [Verifies AGW-001, AGW-008]
- AC-AGW-002: Chatterbox can be selected and executed through the gateway adapter under approved policy. [Verifies AGW-003, AGW-007]
- AC-AGW-003: A second adapter can be added behind the same gateway contract without breaking existing upstream API consumers. [Verifies AGW-002]
- AC-AGW-004: Attempting to enable a model without recorded commercial-use evidence is rejected by gateway governance controls. [Verifies AGW-004]
- AC-AGW-005: Gateway runtime operation does not require external model API calls for approved core generation paths. [Verifies AGW-005]
- AC-AGW-006: Hindi and English requests are accepted and routed through the gateway with recorded model decision metadata. [Verifies AGW-006, AGW-007, AGW-009]
- AC-AGW-007: When the selected model is unavailable, gateway behavior follows defined fallback/failure policy and returns deterministic error classification. [Verifies AGW-010]
- AC-AGW-008: Chatterbox is deployed as a separate Cloud Run API service, and gateway model execution requests target that service through configured internal backend routing rather than in-process model execution. [Verifies AGW-011, AGW-001]

## Clarification Log

| Q | Question | Answer |
|---|----------|--------|
| 1 | Work item folder name and immediate artifact scope? | `ai-gateway-multimodel`; create `requirements.md` only at this stage. [User: Q1] |
| 2 | Should Chatterbox be deployed as a separate Cloud Run API service behind the gateway? | Yes — revise this work item to include separate Cloud Run-hosted Chatterbox API deployment and gateway consumption of that API. [User: Q2] |

## Provenance Check

- Every requirement and exclusion carries a source label.
- `Derived` items, each with confirming `Qn`: none.
- `Left to` items: token-optimization details; UI model-selection exposure.
- `Repo` citations verified during this capture: `voice_narration/inference/application.py:14,108`; `voice_narration/inference/providers/__init__.py:2,4`; `voice_narration/inference/providers/mock.py:14`; `frontend/src/App.jsx:3,4,116`; `tests/test_clone_flow.py:7,23`.
- Requirements without an acceptance criterion: none.
