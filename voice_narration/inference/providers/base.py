from __future__ import annotations

from pathlib import Path
from typing import Any


class BaseProvider:
    def generate(self, text: str, voice_profile: dict[str, Any], output_path: Path) -> Path:
        raise NotImplementedError
