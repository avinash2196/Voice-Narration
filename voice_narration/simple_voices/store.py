"""Durable storage of uploaded voices and their samples, with 5-day retention.

Uploaded voices are kept in upload order in one index file under the storage
root, and each sample is kept unencoded in its own file named by the voice id.
The preloaded Google voices are not stored here.
"""

from datetime import datetime, timedelta
import json
import os
from pathlib import Path

RETENTION = timedelta(hours=120)
INDEX_FILE = "voices.json"
SAMPLES_DIRECTORY = "samples"


class VoiceStore:
    def __init__(self, root, clock):
        self._index = Path(root) / INDEX_FILE
        self._samples = Path(root) / SAMPLES_DIRECTORY
        self._samples.mkdir(parents=True, exist_ok=True)
        self._clock = clock
        self._voices = self._load()
        self.remove_expired()
        self._remove_unindexed_samples()

    def __contains__(self, voice_id):
        return voice_id in self._voices

    def voices(self):
        return list(self._voices.values())

    def get(self, voice_id):
        return self._voices.get(voice_id)

    def sample(self, voice_id):
        """The stored sample's bytes, or None for an unknown voice or one without a sample."""
        if voice_id not in self._voices:
            return None
        path = self._samples / voice_id
        return path.read_bytes() if path.is_file() else None

    def add(self, voice, sample):
        if sample:
            (self._samples / voice["id"]).write_bytes(sample)
        self._voices[voice["id"]] = voice
        self._save()

    def update(self, voice_id, changes):
        self._voices[voice_id].update(changes)
        self._save()
        return self._voices[voice_id]

    def delete(self, voice_id):
        self._remove([voice_id])

    def remove_expired(self):
        now = self._clock()
        expired = [
            voice_id for voice_id, voice in self._voices.items()
            if datetime.fromisoformat(voice["uploadedAt"]) + RETENTION <= now
        ]
        if expired:
            self._remove(expired)

    def _remove(self, voice_ids):
        for voice_id in voice_ids:
            del self._voices[voice_id]
        self._save()
        for voice_id in voice_ids:
            (self._samples / voice_id).unlink(missing_ok=True)

    def _remove_unindexed_samples(self):
        for path in self._samples.iterdir():
            if path.name not in self._voices:
                path.unlink()

    def _load(self):
        if not self._index.is_file():
            return {}
        voices = json.loads(self._index.read_text(encoding="utf-8"))
        return {voice["id"]: voice for voice in voices}

    def _save(self):
        temporary = self._index.with_name(INDEX_FILE + ".tmp")
        temporary.write_text(json.dumps(list(self._voices.values())), encoding="utf-8")
        os.replace(temporary, self._index)
