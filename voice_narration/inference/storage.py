from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


class AudioStorage:
    """Persist generated audio to a local disk directory and keep a relative path for lookup."""

    def __init__(self, root_path: Optional[str | os.PathLike[str]] = None):
        base_root = root_path or os.getenv("AUDIO_STORAGE_PATH", str(Path(__file__).resolve().parents[2] / "audio_storage"))
        self.root = Path(base_root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "generations").mkdir(exist_ok=True)
        (self.root / "temp").mkdir(exist_ok=True)
        (self.root / "archive").mkdir(exist_ok=True)

    def save_audio(self, audio_bytes: bytes, voice_id: str, *, prefix: str = "generation") -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_voice = voice_id.replace("/", "_").replace(" ", "_")
        unique_name = f"{prefix}_{safe_voice}_{timestamp}_{uuid.uuid4().hex[:8]}.wav"

        day_dir = self.root / "generations" / datetime.utcnow().strftime("%Y-%m-%d")
        day_dir.mkdir(parents=True, exist_ok=True)

        target = day_dir / unique_name
        target.write_bytes(audio_bytes)
        return str(target.relative_to(self.root))

    def get_full_path(self, relative_path: str) -> Path:
        return (self.root / relative_path).resolve()

    def delete_file(self, relative_path: str) -> bool:
        target = self.get_full_path(relative_path)
        if target.exists():
            target.unlink()
            return True
        return False
