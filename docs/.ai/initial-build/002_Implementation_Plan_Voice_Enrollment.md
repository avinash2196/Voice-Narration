# Implementation Plan — Voice Enrollment & Cloning Flow

## Milestone

Voice Enrollment GREEN, milestone 9 of initial-build.

## Milestone Type

GREEN. Proposed execution plan for the approved behavior in requirements.md and the milestone sequence in Plan.md.

## Status

Awaiting human approval. This proposal is intentionally limited to the approved voice-enrollment and cloning scope; it does not authorize production provisioning or model deployment.

## Authoritative References

All paths below are relative to the repository unless otherwise stated. Documents inspected on 2026-11-06:

| Reference | Authority / approval |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved by avinash2196 on 2026-10-19; scope clarifications recorded 2026-10-24. |
| docs/.ai/initial-build/Plan.md | Revised Plan approved 2026-10-24; milestone 9 Pending. |
| docs/.ai/initial-build/contract/API-Contract.md | Approved contract scope for voice profile lifecycle, enrollment and generation. |
| voice_narration_PDD_requirements.md | Baseline P0 requirements preserved under scope clarification; includes FR-010 through FR-013 and R-WORK-001. |
| existing local runtime and frontend | Current repo evidence shows the app is available locally and the next missing capability is user-owned cloned voices tied into TTS generation. |

## Preconditions / Predecessor Evidence

This plan assumes the following predecessor artifacts and runtime conditions have already been satisfied before execution:

- Developer & Test Harness foundation is available and the repository has a working local test/bootstrap path.
- Contract/API-Contract.md is approved and available for the enrollment/generation workflow.
- Authentication and consent services are present and working.
- The project has a durable storage layer, a user-owned voice-profile model, and a generation job model compatible with the approved contract.
- The app can already record audio and generate audio using a current TTS pipeline; the missing gap is a clone-enabled voice enrollment flow tied to generation.

No model-specific deployment or production GPU path is approved by this plan. Any model-specific behavior must be isolated behind the existing inference adapter and remain gated by the later model approval milestone.

## Current Repository State

Current inspection confirms the repository has the PDD and developer-harness scaffolding, but the feature work for voice enrollment and clone-based generation is not in place yet. The app has a working recording path and generation pipeline, while profile persistence, sample metadata, consent linkage, and cloned-voice generation remain the next explicit feature gap.

The implementation below is scoped to that gap and remains aligned to the approved requirement set rather than ad hoc product assumptions.

## Binding Decisions for Human Review

| Decision | Concrete proposal / reason | Alternative and consequence |
| --- | --- | --- |
| Voice enrollment model | Preserve a user-owned voice profile with mandatory consent reference, sample metadata, and model/version metadata; do not promise model training or irreversible cloning beyond the selected provider contract. | Treating enrollment as a fully trained custom model without approval would violate the approved requirement boundaries. |
| Audio intake | Accept microphone recordings and uploaded WAV/MP3/M4A, with format and size validation at the API boundary and browser-level quality checks before persistence. | Accepting arbitrary files or unvalidated recordings would break P0 audio quality and retention requirements. |
| Quality override | Allow informed override only after the user has seen the warning and acknowledged it. | Silent override or automatic acceptance would bypass P0 enrollment safety. |
| Persistence boundaries | Store only the minimum voice references/artifacts the selected model needs; keep profile metadata separate from generated audio and consent records. | Persisting raw full voice corpora or unbounded samples would create privacy and retention hazards. |
| Generation linkage | Require the selected voice profile to be active, owned by the current user, and consent-associated before generation is accepted. | Allowing unapproved or deleted voices would break isolation and revocation requirements. |

## Files in Scope

### Files to Create

- `voice_narration/voices/application.py`
- `voice_narration/voices/models.py`
- `voice_narration/voices/repository.py`
- `voice_narration/voices/service.py`
- `voice_narration/voices/validation.py`
- `voice_narration/consent/client.py`
- `voice_narration/inference/providers/voice_clone_adapter.py`
- `frontend/src/components/VoiceRecorder.tsx`
- `frontend/src/components/VoiceEnrollmentPanel.tsx`
- `frontend/src/services/voiceApi.ts`
- `tests/test_voice_enrollment.py`
- `tests/test_voice_generation_integration.py`

### Files to Modify

- `voice_narration/inference/application.py`
- `voice_narration/inference/providers/__init__.py`
- `voice_narration/inference/providers/base.py`
- `voice_narration/simple_voices/application.py`
- `frontend/src/App.tsx`
- `frontend/src/services/ttsApi.ts`

### Files to Delete

None.

## Proposed Changes

1. Voice-profile domain model
   - Add durable voice profile records with fields for owner, friendly name, language, consent id, model/version, status, sample refs, and timestamps.
   - Keep profile state explicit: pending, quality-warning, enrolled, revoked, deleted.

2. Enrollment validation and recording UX
   - Validate upload type and size in browser and API.
   - Enforce WAV/MP3/M4A support and time limits.
   - Add feedback for clipping, silence, low SNR, and missing speech; allow re-record and explicit warning override.

3. Consent-aware enrollment flow
   - Require recorded consent before profile creation.
   - Validate consent is active and associated with the same user.
   - Persist immutable consent audit metadata without exposing private voice assets to unauthorized administrators.

4. Clone/artifact persistence
   - Store only the minimum artifacts required by the selected model or provider.
   - Keep generated clone artifacts distinct from ordinary audio output and add cleanup hooks matching retention and revocation requirements.

5. Generation integration for cloned voice
   - Ensure a user can select an authorized voice profile from their private library.
   - Block generation when the voice profile is revoked, deleted, or not owned by the requesting user.
   - Pass selected profile metadata and model version to the job submission layer.

6. Frontend update
   - Add voice recording/upload UI with profile save and profile selection.
   - Surface enrollment status, warnings, and active profile details.
   - Update generation UI to allow cloned voice selection and job tracking.

## Proposed Code / Tests

### Voice Model Example

```python
class VoiceProfile(BaseModel):
    id: str
    owner_id: str
    name: str
    language: str
    consent_id: str
    model_name: str
    model_version: str
    status: str
    sample_refs: list[str]
    created_at: datetime
    updated_at: datetime
    revoked_at: datetime | None = None
```

### Enrollment API Sketch

```python
POST /voices/enroll
{
  "name": "My Voice",
  "language": "hi-IN",
  "consent_id": "consent_123",
  "samples": [
    {"filename": "sample1.wav", "content_type": "audio/wav", "size_bytes": 2457600}
  ]
}
```

### Generation Job Linkage Sketch

```python
POST /jobs/generate
{
  "script": "नमस्ते, यह एक परीक्षण है।",
  "voice_profile_id": "profile_456",
  "idempotency_key": "job-abc-123",
  "pace": 1.0,
  "pause_strength": 1.0
}
```

### Tests to Add

- `test_voice_enrollment_requires_valid_consent`
- `test_voice_enrollment_rejects_unapproved_formats`
- `test_voice_profile_is_isolated_to_owner`
- `test_deleted_or_revoked_profile_blocks_generation`
- `test_generation_job_persists_selected_profile_metadata`
- `test_cloned_voice_selection_works_for_owner_only`
- `test_profile_retention_and_cleanup_flow`

## Verification Commands

The following commands should be used after implementation and before marking the milestone complete:

```bash
pytest tests/test_voice_enrollment.py tests/test_voice_generation_integration.py -q
pytest -q
```

If the repository uses the local harness, the check should also include the developer readiness/bootstrap command for the local environment:

```bash
python tools/readiness.py
```

## Implementation Notes

- This milestone does not authorize model training or weights deployment; it only ensures the product can persist and reuse a consented profile in a way the approved generation pipeline can consume.
- All voice data must remain scoped to the current authenticated user and only be used when an active profile consent reference remains valid.
- The code should be structured so that the inference provider remains swappable behind the existing provider interface. This keeps model approval separate from the enrollment and generation UX that is being implemented here.
- Existing audio-generation jobs should continue to work, and the cloned profile must be an optional enhancement rather than a breaking change to the current narration flow.

## Exit Criteria

The milestone is ready for review when the following are true:

- Users can record or upload valid voice samples and create an owned profile.
- Consent and ownership are enforced before profile creation and generation.
- Revoked or deleted profiles are rejected by the generation API.
- Selected profile metadata is persisted with the job and shown in history.
- The frontend allows the user to choose the enrolled cloned voice for narration generation.
- Core tests pass and the workflow aligns with the approved requirements and PDD boundaries.
