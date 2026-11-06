# Implementation Plan — Generation Persistence GREEN

## Milestone

Generation Persistence GREEN, milestone 3 of audio-download-persistence.

## Milestone Type

GREEN. Implements the production behavior required to satisfy the approved M2 persistence tests.

## Authoritative References

| Read document | Authority / disposition |
| --- | --- |
| docs/.ai/audio-download-persistence/requirements.md | Approved work item scope for F1-F6. |
| docs/.ai/audio-download-persistence/Plan.md | Approved milestone sequence and ownership. |
| docs/.ai/audio-download-persistence/001_Implementation_Plan_M2_Persistence_RED.md | Approved RED milestone; its successful execution is the baseline for this GREEN work. |
| voice_narration/inference/application.py | Current app stores only in-memory outputs; this GREEN milestone changes that behavior. |
| voice_narration/inference/models.py | Real schema for `Voice` and `Generation` persistence. |
| voice_narration/inference/db.py | Real DB engine and session setup. |
| voice_narration/inference/storage.py | Real disk storage helper for generated WAV files. |

## Preconditions / Predecessor Evidence

The M2 RED milestone has been executed successfully:

```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration
pytest tests/test_generation_persistence_red.py -q
```

Evidence: `2 passed`.

This proves the persistence behavior is currently missing in production and the requirement is valid for GREEN implementation.

## Current Repository State

- `InferenceState` can generate audio but did not previously write to a durable store.
- `AudioStorage` writes WAV files under `audio_storage/generations/...`.
- `Generation` and `Voice` SQLAlchemy models already exist and are the durable persistence schema.
- The service is ready for the missing production behavior: persist the generated file and metadata immediately after inference.

## Files in Scope

### Files to Modify

- `voice_narration/inference/application.py`

### Files to Create

- None required in this milestone.

## Proposed Changes

1. Add durable persistence to `InferenceState.persist_generation` so the generated audio is saved to disk and metadata is stored to the database.
2. Ensure the storage root is configured from `AUDIO_STORAGE_PATH`, and that file paths are relative to the storage root for later replay/download logic.
3. Ensure the database tables are created when the service starts.
4. Keep the JSON index file as a lightweight fallback for quick lookup and restart recovery, while also writing the SQLAlchemy `Generation` row when the database is available.
5. Preserve the existing in-memory output cache for immediate retrieval of current jobs.

## Proposed Code / Final Patch

The final implementation is applied in `voice_narration/inference/application.py` and comprises the following behaviors:

- initialize `AudioStorage` for the configured root
- load/save a `generation_index.json` mirror for quick restart recovery
- create SQLAlchemy tables if needed
- on generation, write a WAV file, capture metadata, write the index, and persist a `Generation` row in Postgres when available
- return the persistent metadata from `get_persisted_generation(job_id)`

## Acceptance / Completion Criteria

- A generation result saves both a real WAV file and a real metadata record.
- The saved file path is relative to the configured storage root.
- A persisted generation can be retrieved by `job_id` without relying on the transient in-memory dict alone.
- Existing generation flow still reports success for valid jobs.
- The M2 RED tests pass without modification.

## Verification Commands

```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration
pytest tests/test_generation_persistence_red.py -q
```

Expected evidence: `2 passed`.

## Human Review

Status: Approved by user on 2026-11-06.
