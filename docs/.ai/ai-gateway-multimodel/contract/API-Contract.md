# API Contract — ai-gateway-multimodel

## Contract Scope

Defines the AI Gateway external contract for model execution, routing decisions, governance checks, and deterministic fallback/error behavior for narration/voice-cloning requests. This contract is the authority for gateway interface behavior; `../Plan.md` remains authority for milestone scope and order.

## Baseline

No prior gateway contract exists in this repository. Current behavior calls a concrete provider directly from inference request handling and does not expose a gateway routing contract. [Repo: voice_narration/inference/application.py:108]

## Changes in This Work Item

Introduces a new gateway-facing contract with:
- normalized execution request/response schema;
- model-routing decision metadata;
- deterministic failure taxonomy;
- model-governance eligibility and enablement state requirements;
- migration-compatible behavior for existing consumers while direct-provider calls are replaced.

## Out of Scope

- Implementing executable gateway behavior (handled by later RED/GREEN milestones).
- Enabling non-Chatterbox adapters in this first delivery, beyond extensibility compatibility.
- Any bypass of commercial-use gate checks.

## Requirement Traceability

| Requirement | Contract coverage |
| --- | --- |
| AGW-001 | `POST /ai-gateway/v1/executions` as the execution boundary |
| AGW-002 | Adapter/model identifiers and stable gateway request/response surface |
| AGW-003 | Chatterbox represented as initial model entry and route target |
| AGW-004 | Model approval/governance schema and enablement preconditions |
| AGW-005 | Runtime mode and provider class policy fields disallowing required external API dependency |
| AGW-006 | Language fields and bilingual capability declarations |
| AGW-007 | Routing policy input and decision output objects |
| AGW-008 | Full pass-through execution context schema |
| AGW-009 | Usage/decision telemetry fields in execution result |
| AGW-010 | Deterministic error codes and fallback outcome semantics |

## Interfaces

### Shared schema types

- `ID`: lowercase UUID string.
- `Time`: RFC3339 UTC timestamp.
- `Language`: `"hi"` or `"en"`.
- `ExecutionMode`: `"narration"` or `"voice_cloning"`.
- `RuntimeClass`: `"self_hosted"` or `"external_api"`.
- `ModelState`: `"draft" | "approved" | "enabled" | "disabled" | "blocked"`.

### Core objects

`ExecutionRequest`:
- `request_id: ID`
- `mode: ExecutionMode`
- `text: string` (required, non-empty)
- `language: Language`
- `voice_profile_id: ID`
- `model_hint: string | null`
- `controls: { pause_strength: number | null, speech_pace: number | null }`
- `idempotency_key: string`
- `metadata: object` (caller context; opaque to consumers, routable by gateway policy)

`RoutingDecision`:
- `selected_model_id: string`
- `selected_model_version: string`
- `policy_name: string`
- `policy_revision: string`
- `decision_reason: string`
- `fallback_applied: boolean`
- `fallback_from_model_id: string | null`

`UsageTelemetry`:
- `latency_ms: integer`
- `queue_ms: integer | null`
- `compute_ms: integer | null`
- `cost_estimate_usd: string | null`
- `runtime_class: RuntimeClass`

`ExecutionResponse`:
- `execution_id: ID`
- `status: "accepted" | "completed" | "failed"`
- `audio_url: string | null`
- `routing: RoutingDecision`
- `usage: UsageTelemetry`
- `errors: ErrorItem[]`

`ModelApproval`:
- `model_id: string`
- `model_version: string`
- `license_evidence_uri: string`
- `weights_evidence_uri: string`
- `output_use_evidence_uri: string`
- `runtime_class: RuntimeClass`
- `languages_supported: Language[]`
- `approved_by: string | null`
- `approved_at: Time | null`
- `state: ModelState`

`ErrorItem`:
- `code: string`
- `message: string`
- `retryable: boolean`
- `fallback_attempted: boolean`

### Endpoints

#### POST `/ai-gateway/v1/executions`

Purpose: single execution ingress for model runs.

Input:
- JSON `ExecutionRequest`.

Success:
- `202` with `ExecutionResponse` (`status="accepted"` or `"completed"` depending on execution mode/path).

Deterministic failures:
- `400 INVALID_INPUT` — invalid/missing required fields.
- `400 UNSUPPORTED_LANGUAGE` — unsupported language for route/model.
- `400 IDEMPOTENCY_KEY_REQUIRED` — idempotency key missing/invalid.
- `403 MODEL_NOT_ELIGIBLE` — model lacks approved commercial evidence.
- `403 RUNTIME_POLICY_VIOLATION` — runtime requires disallowed external API for core path.
- `409 IDEMPOTENCY_CONFLICT` — same idempotency key, different effective request.
- `422 ROUTING_NO_MATCH` — no policy-compliant model candidate.
- `503 MODEL_UNAVAILABLE` — selected model unavailable.

Fallback behavior:
- If selected model fails and configured fallback exists, gateway may return success with `routing.fallback_applied=true`.
- If no compliant fallback exists, return deterministic failure with `errors[0].code` in `{ROUTING_NO_MATCH, MODEL_UNAVAILABLE, MODEL_NOT_ELIGIBLE}` and `fallback_attempted` reflecting actual attempt.

#### GET `/ai-gateway/v1/models`

Purpose: list routable models and governance state.

Success:
- `200` with `items: ModelApproval[]`.

Failures:
- `403 FORBIDDEN` for unauthorized caller.

#### POST `/ai-gateway/v1/models/{model_id}/approvals`

Purpose: register or update commercial/governance evidence for a model version.

Input:
- JSON subset of `ModelApproval` evidence fields (`model_version`, evidence URIs, runtime class, supported languages).

Success:
- `201` returns `ModelApproval` with `state="approved"` when all required evidence fields are valid.

Failures:
- `400 INVALID_EVIDENCE` for incomplete evidence.
- `409 APPROVAL_CONFLICT` for conflicting immutable evidence for the same version.

#### POST `/ai-gateway/v1/models/{model_id}/enable`

Purpose: enable model for routing after governance checks.

Input:
- `model_version`.

Success:
- `200` returns `ModelApproval` with `state="enabled"`.

Failures:
- `403 MODEL_NOT_ELIGIBLE` if commercial evidence/approval missing.
- `403 RUNTIME_POLICY_VIOLATION` if runtime class violates self-hosted requirement for core path.
- `409 MODEL_STATE_CONFLICT` if model cannot transition to enabled from current state.

## Compatibility Rules

- Existing callers may keep current request semantics, but migration target is gateway-mediated execution via `POST /ai-gateway/v1/executions`.
- Adding a new model adapter must not require request-shape changes for existing consumers.
- New optional metadata fields may be added; required field removals/renames require contract revision and review.

## Contract Review Status

- Status: Approved by avinash2196 on 2026-11-08. Recorded by the main conversation at the user's explicit approval of this contract.
- This artifact does not authorize executable changes. CONTRACT milestone completes only after explicit user approval is recorded here and reflected in `../Plan.md`.
