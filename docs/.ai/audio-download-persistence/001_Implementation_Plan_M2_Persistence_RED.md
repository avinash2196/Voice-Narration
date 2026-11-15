# Implementation Plan — Generation Persistence RED

## Milestone

Generation Persistence RED, milestone 2 of audio-download-persistence.

## Milestone Type

RED. This document proposes test coverage only and does not modify production behavior.

## Authoritative References

| Read document | Authority / disposition |
| --- | --- |
| docs/.ai/audio-download-persistence/requirements.md | Approved work item scope for F1-F6. |
| docs/.ai/audio-download-persistence/Plan.md | Approved plan for milestone sequencing and ownership. |
| voice_narration/inference/application.py | Current runtime behavior stores generation output only in memory (`_pending_inferences`). |
| voice_narration/inference/models.py | Existing persistence schema defines `Generation` and `Voice` models. |
| voice_narration/inference/storage.py | Existing file store; no DB-backed persistence yet. |
| voice_narration/inference/db.py | Database session and engine setup exist, but are not wired into generation flow. |

## Preconditions / Predecessor Evidence

The repository has scaffolding for persistence but no verified M1 execution evidence for a real Postgres-backed generation flow. The current app still keeps generation outputs in memory and does not save them to disk or a database row during generation.

## Current Repository State

- `voice_narration/inference/application.py` stores outputs in `InferenceState._pending_inferences`.
- `voice_narration/inference/models.py` defines the intended persistence schema.
- `voice_narration/inference/storage.py` can write WAV files to disk.
- `voice_narration/inference/db.py` has database connection helpers.
- No execution test currently proves that generated audio is persisted in the real service path.

## Files in Scope

### Files to Create

- `tests/test_generation_persistence_red.py` — complete content below.

### Files to Modify

- None in this RED milestone.

## Proposed Changes

1. Create a focused RED test file verifying that a generation is persisted to database and disk immediately after inference output is produced.
2. Assert the generation lifecycle uses a real persisted record keyed by `job_id`, not only the in-memory dictionary.
3. Verify the file path is written to disk and the metadata record contains text, voice, duration, and timestamps.
4. Keep the test narrow to persistence behavior only; no production code changes required in this milestone.

## Proposed Code / Tests

```python
import os
from pathlib import Path

import pytest

from voice_narration.inference.application import InferenceState


class DummyProvider:
    async def generate(self, script: str, voice_id: str, **kwargs):
        return {
            "audio_bytes": b"RIFF....WAVE",
            "format": "wav",
            "output_seconds": 2.5,
        }

    async def estimate_cost(self, script: str, voice_id: str):
        return {"cost_usd": 0.0, "estimated_seconds": 2.5}

    def list_voices(self, language=None):
        return []


@pytest.mark.asyncio
async def test_generate_persistence_saves_record_and_file(tmp_path):
    state = InferenceState(provider=DummyProvider())
    state.storage_root = tmp_path

    result = await state.submit_for_inference(
        job_id="job-123",
        script="Hello from the persistence test",
        voice_id="en-US-Neural2-A",
    )

    assert result["job_id"] == "job-123"
    assert result["status"] == "complete"
    assert result["duration_seconds"] == 2.5

    persisted = state.get_persisted_generation("job-123")
    assert persisted is not None
    assert persisted["text"] == "Hello from the persistence test"
    assert persisted["voice_id"] == "en-US-Neural2-A"
    assert persisted["duration_seconds"] == 2.5
    assert persisted["file_path"].endswith(".wav")
    assert Path(tmp_path / persisted["file_path"]).exists()


@pytest.mark.asyncio
async def test_generate_persistence_survives_restart(tmp_path):
    state = InferenceState(provider=DummyProvider())
    state.storage_root = tmp_path

    await state.submit_for_inference(
        job_id="job-456",
        script="A second persistence check",
        voice_id="hi-IN-Neural2-A",
    )

    restored_state = InferenceState(provider=DummyProvider())
    restored_state.storage_root = tmp_path

    persisted = restored_state.get_persisted_generation("job-456")
    assert persisted is not None
    assert persisted["text"] == "A second persistence check"
    assert persisted["voice_id"] == "hi-IN-Neural2-A"
    assert Path(tmp_path / persisted["file_path"]).exists()
```

## Acceptance / Completion Criteria

- The new test file exists and clearly captures the persistence requirements.
- The tests fail for the current code because generation persistence is not implemented.
- No production code is modified in this milestone.

## Verification Commands

```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration
pytest tests/test_generation_persistence_red.py -q
```

Expected milestone evidence: the tests fail because `InferenceState` has no persisted-generation behavior yet.

## Human Review

Status: Approved by user on 2026-11-06.
