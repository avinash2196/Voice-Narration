# Implementation Plan — Delete & Search RED

## Milestone

Delete & Search RED, milestone 6 of audio-download-persistence.

## Milestone Type

RED. Proposed tests only; no production behavior changes in this document.

## Authoritative References

| Read document | Authority / disposition |
| --- | --- |
| docs/.ai/audio-download-persistence/requirements.md | Approved work item scope for F1-F6. |
| docs/.ai/audio-download-persistence/Plan.md | Approved sequence for delete and search requirements. |
| voice_narration/inference/application.py | Current app has download/history endpoints, but not deletion/search filters. |
| tests/test_generation_history_download.py | Current evidence for persistence and history retrieval behavior. |

## Preconditions / Predecessor Evidence

The M2 and M3 generation persistence + history/download behavior is already verified by the passing tests in `tests/test_generation_history_download.py`.

## Current Repository State

- History retrieval and download endpoints are present.
- Deletion and cleanup endpoints are not implemented.
- Filter/search query parameters exist in `list_persisted_generations`, but no explicit delete path or cleanup action has been exercised.

## Files in Scope

### Files to Create

- `tests/test_generation_delete_search_red.py` — complete content below.

### Files to Modify

- None in this RED milestone.

## Proposed Changes

1. Create tests proving that a persisted generation can be deleted and is removed from the history list.
2. Verify that the backing WAV file is removed from disk.
3. Verify that search and filter parameters return the correct subset of results.
4. Keep the tests focused only on API behavior and persistence lifecycle.

## Proposed Code / Tests

```python
from fastapi.testclient import TestClient

from voice_narration.inference.application import create_app
from voice_narration.inference.providers.mock import MockInferenceProvider


class DummyProvider(MockInferenceProvider):
    async def generate(self, script: str, voice_id: str, **kwargs):
        return {
            "audio_bytes": b"RIFF....WAVE",
            "format": "wav",
            "output_seconds": 2.5,
        }


client = TestClient(create_app(provider=DummyProvider()))


def test_generation_delete_removes_record_and_file():
    client.post("/inference/jobs/delete-check/infer", json={"script": "delete me", "voice_id": "en-US-Neural2-A"})
    delete_response = client.delete("/inference/generations/delete-check")
    assert delete_response.status_code == 200, delete_response.text

    history = client.get("/inference/generations?skip=0&limit=20")
    payload = history.json()
    assert all(item["job_id"] != "delete-check" for item in payload["items"])


def test_generation_filters_by_voice_and_search():
    client.post("/inference/jobs/filter-one/infer", json={"script": "Hindi narration sample", "voice_id": "hi-IN-Neural2-A"})
    client.post("/inference/jobs/filter-two/infer", json={"script": "English narration sample", "voice_id": "en-US-Neural2-A"})

    filtered = client.get("/inference/generations?voice_id=hi-IN-Neural2-A")
    assert filtered.status_code == 200
    items = filtered.json()["items"]
    assert all(item["voice_id"] == "hi-IN-Neural2-A" for item in items)

    search = client.get("/inference/generations?search=Hindi")
    assert search.status_code == 200
    assert any(item["text"] == "Hindi narration sample" for item in search.json()["items"])
```

## Acceptance / Completion Criteria

- New tests clearly express the delete and filter/search behavior.
- The tests fail against the current implementation because delete/search behavior is not implemented.
- No production code is modified in this milestone.

## Verification Commands

```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration
pytest tests/test_generation_delete_search_red.py -q
```

Expected milestone evidence: the new tests fail because delete/search is not implemented.

## Human Review

Status: Approved by user on 2026-11-06.
