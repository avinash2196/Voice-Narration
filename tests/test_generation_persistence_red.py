import asyncio
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
