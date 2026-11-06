# Enrollment interface completion — batched proposal

## Decision requested

Approve the three decisions below together, followed by the normal requirements/Plan/contract/test-plan review sequence. This proposal does not apply test changes or production implementation. The completed catalog correction and all completed milestone evidence remain history.

## Why another correction is necessary

The listing callback added under 011 provides capability data, but the broader contract audit found additional missing inputs in 010/011's reviewed factory seams:

1. `GET /voices` and `GET /models` require configured page limits. Voices receives neither those limits nor a source containing them. The fixture's `policy_snapshot()` contains only revision and enrollment_quality.
2. Model listing must follow persisted Approval time and model identity ordering. Public Capability has no approval timestamp, and the listing callback previously made no ordering guarantee.
3. Upload admission must check an approved model's duration limits, but multipart upload currently provides only consent_id and file. Its keyed `capability(model)` dependency has no model argument to resolve. Hardcoding the synthetic model or inspecting a bound callback's private object is not an acceptable implementation.

Sources inspected: current `tests/test_voice_enrollment.py` SETTINGS, TestCatalog, make_voices and upload; approved `contract/API-Contract.md` shared List, upload, Enrollment, Models and Configuration limits; 010/011 interface records; completed milestone 11 evidence. No runtime, database, package or Docker operation was needed for this audit.

## Recommended combined decisions

### A. Supply pagination explicitly

Extend only the internal Voices factory with required keyword-only `pagination`, a closed mapping `{default_page_size: Pos, max_page_size: Pos}` with default <= max. The bootstrap maps the existing public Configuration.limits.page_default/page_max to this input. Missing or invalid dependent configuration fails closed; no hidden page defaults are introduced.

The test fixture passes its already-reviewed SETTINGS values 10 and 20 explicitly. Those remain synthetic test inputs, not production defaults. Existing cursor/principal/filter/snapshot and page-limit rules remain unchanged. Tests should verify that actual handler behavior uses configured limits, not merely assert an echoed diagnostic mapping.

### B. Make catalog ordering the listing provider's explicit responsibility

Keep `list_capabilities()` zero-argument and returning public Capability records. Require the trusted catalog provider to return only enabled/approved entries in the existing contract's persisted Approval-time/model-identity order. The provider owns access to Approval metadata; the Voices handler preserves that order and applies the approved authenticated pagination/snapshot rules. No approval timestamp is added to public Capability or obtained through callback introspection.

Test inputs may include multiple synthetic catalog records whose ID order differs from approval order, so handler reordering and page-boundary mistakes are observable. These tests prove consumer ordering/pagination behavior, not the correctness of an unimplemented production approval registry or real model eligibility. Production catalog transport/evidence acquisition remains its approved later boundary.

### C. Identify the selected model at upload admission

Amend the existing upload row to the following exact input; endpoint, response and existing failure codes stay unchanged:

| Operation | Proposed exhaustive input | Success | Specific failures |
| --- | --- | --- | --- |
| POST /artifacts/upload | multipart/form-data consent_id:ID,model_id:ID,model_version:Text,file:binary | 201 sample Artifact | 400 INVALID_AUDIO/LIMIT_EXCEEDED;409 CONSENT_REVOKED;503 MODEL_NOT_READY |

The two new required scalar parts map to the existing Model `{model_id, version}`. They are exactly one value each, canonical/typed under existing multipart rules; missing, blank, duplicate or unknown parts follow existing 400 INVALID_INPUT behavior. The Artifact boundary resolves the explicitly requested model through `capability(model)` and enforces its approved sample duration bounds together with applicable configured limits before accepting the sample. Unknown, unapproved or unavailable model uses existing 503 MODEL_NOT_READY. Active owner consent, actual format/byte checks, original-byte preservation and unauthorized-stream disposal remain mandatory.

The client selects a model from the approved catalog before recording/upload, so guidance and effective duration limits refer to that model. Consent still precedes sample persistence; profile creation still follows authorized sample upload. No default model or Chatterbox sample duration is invented.

The model reference is admission context, not a new immutable public Artifact field or a permanent prohibition on sample reuse with another model. Profile admission and conditioning must independently recheck every sample against the profile's selected model and current safety/readiness gates. Public Artifact and Profile response shapes remain unchanged. Codec admission remains WAV/MP3/M4A; Capability output formats do not become new upload-format exclusions.

Existing positive upload helpers must send the explicit synthetic Model reference. Tests must retain all current safety assertions and add missing/unknown/unready model coverage alongside working positive admission. Adding the two required parts is an intentional input-contract revision, not a claim of backward compatibility. No Artifact upload implementation has shipped in the inspected repository, so no existing implemented upload consumer is claimed migrated by this document.

## Scope and review sequence

- These decisions supply missing operator/catalog/model inputs; they do not alter the acoustic algorithm, thresholds, override rules, calibration gate, model licensing gate, service ownership or retained material policy.
- After approval, record the decisions in requirements through the plugin's capture/review flow, revise the pending Plan sequence while preserving completed work, and prepare a narrow contract amendment for the explicit upload model reference and any necessary input/readiness cross-references. No approval of unwritten artifacts is inferred.
- Prepare separately reviewed test/interface changes for pagination, catalog ordering and model-aware upload. Because the upload input contract changes, use the appropriate RED verification boundary rather than labeling expected missing-feature failures a passing OTHER result. The fresh Plan must determine the exact milestone sequence and requirement ownership under PDD; this proposal does not relabel completed milestones.
- Existing 57 passing cases remain regression constraints; the six real acoustic cases and current safety assertions remain. A later GREEN plan must implement the complete corrected interface and pass its full approved suite. No hardcoded fixture model, hidden limit or private callback introspection is permitted.
- Installation, tests, source code, configuration files, database schema, Docker state, commits and publication remain unchanged by this proposal.

## Human Review

Status: Approved by avinash2196 on 2026-10-26 (America/Chicago; recorded 2026-10-26T17:10:04Z), in response to review of this exact batched interface-completion proposal and review sequence. This authorizes requirements capture and the review flow, not changes to an unwritten Plan, contract, test or production implementation.
