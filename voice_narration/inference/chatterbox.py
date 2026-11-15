"""Voice cloning through the deployed Chatterbox service.

Contract: docs/.ai/chatterbox-original-app/API-Contract.md, Inference Service Chatterbox
Call, Chatterbox Failure Causes (OAF-1 to OAF-9) and Inference Service Settings.
"""

from __future__ import annotations

import asyncio
import json
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import httpx

CLOSING = "Please retry, or choose another provider."
NOT_CONFIGURED = f"Chatterbox voice cloning is not configured. {CLOSING}"
INVALID_TIME_LIMIT = (
    "The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; "
    f"it must be a positive whole number of seconds. {CLOSING}"
)
SAMPLE_UNREADABLE = f"The voice sample for the selected voice could not be read. {CLOSING}"
TOKEN_UNAVAILABLE = f"Could not obtain an identity token for Chatterbox. {CLOSING}"
TIMED_OUT = "Chatterbox did not respond within {seconds} seconds. " + CLOSING
CANNOT_CONNECT = f"Could not connect to Chatterbox. {CLOSING}"
ACCESS_DENIED = "Access to Chatterbox was denied (HTTP {status}). " + CLOSING
SERVICE_ERROR = "Chatterbox returned an error (HTTP {status}). " + CLOSING
NOT_AUDIO = f"Chatterbox returned a response that is not audio. {CLOSING}"

DESCRIPTION = "Chatterbox voice cloning (deployed Cloud Run service)"
LANGUAGES = ("en", "hi")
DEFAULT_TIME_LIMIT_SECONDS = 1200
DEFAULT_VOICE_SERVICE_URL = "http://localhost:8002"


class ChatterboxFailure(Exception):
    """A Chatterbox generation failed; the message is the contract's text for its cause."""


def trimmed_url(value: Optional[str]) -> str:
    """The URL in effect: surrounding whitespace and trailing slashes removed."""
    return (value or "").strip().rstrip("/")


def parse_time_limit(value: Optional[str]) -> Optional[int]:
    """Seconds from CHATTERBOX_TIMEOUT_SECONDS: 1200 when absent or blank, None when invalid."""
    text = (value or "").strip()
    if not text:
        return DEFAULT_TIME_LIMIT_SECONDS
    if text.isascii() and text.isdigit() and int(text) >= 1:
        return int(text)
    return None


@dataclass(frozen=True)
class ChatterboxSettings:
    url: str
    time_limit: Optional[int]
    voice_service_url: str
    credentials_path: str

    @classmethod
    def from_environment(cls) -> "ChatterboxSettings":
        return cls(
            url=trimmed_url(os.getenv("CHATTERBOX_URL")),
            time_limit=parse_time_limit(os.getenv("CHATTERBOX_TIMEOUT_SECONDS")),
            voice_service_url=trimmed_url(os.getenv("VOICE_SERVICE_URL")) or DEFAULT_VOICE_SERVICE_URL,
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "",
        )


def service_account_identity_token(credentials_path: str, audience: str) -> str:
    """A Google-signed identity token for the service account whose key file is credentials_path.

    Only a service-account key file is used. google-auth's fetch_id_token is not used,
    because it falls back to the metadata server when the key is absent or of another type.
    google-auth is imported here, as the Google provider imports its client library, so the
    inference service starts without it; its absence then means no token (OAF-4).
    """
    if not credentials_path.strip():
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set")
    info = json.loads(Path(credentials_path).read_text(encoding="utf-8"))
    if not isinstance(info, dict) or info.get("type") != "service_account":
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS does not name a service-account key")

    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    credentials = service_account.IDTokenCredentials.from_service_account_info(info, target_audience=audience)
    credentials.refresh(Request())
    return credentials.token


def wav_duration(audio: bytes) -> float:
    """Sample frames divided by sample rate, read from the RIFF chunks of a WAV file.

    The chunks are read directly because Chatterbox returns IEEE-float WAV, which the
    standard wave module rejects. Raises ValueError when the bytes are not a readable WAV file.
    """
    if len(audio) < 12 or audio[:4] != b"RIFF" or audio[8:12] != b"WAVE":
        raise ValueError("not a RIFF/WAVE file")
    sample_rate = block_align = 0
    offset = 12
    while offset + 8 <= len(audio):
        chunk_id = audio[offset:offset + 4]
        (size,) = struct.unpack_from("<I", audio, offset + 4)
        start = offset + 8
        if chunk_id == b"fmt ":
            if size < 16 or start + 16 > len(audio):
                raise ValueError("truncated fmt chunk")
            _, _, sample_rate, _, block_align = struct.unpack_from("<HHIIH", audio, start)
        elif chunk_id == b"data":
            if not sample_rate or not block_align:
                raise ValueError("no usable fmt chunk before the data chunk")
            return (min(size, len(audio) - start) // block_align) / sample_rate
        offset = start + size + (size % 2)
    raise ValueError("no data chunk")


class ChatterboxClient:
    """Produces a cloned generation from the deployed Chatterbox, or raises ChatterboxFailure."""

    def __init__(self, settings: ChatterboxSettings):
        self.settings = settings

    async def generate(self, script: str, voice_id: str, language: str) -> dict:
        if not self.settings.url:
            raise ChatterboxFailure(NOT_CONFIGURED)
        if self.settings.time_limit is None:
            raise ChatterboxFailure(INVALID_TIME_LIMIT)
        sample = await self._fetch_sample(voice_id)
        token = await self._obtain_identity_token()
        response = await self._synthesize(script, language, sample, token)
        audio = self._read_audio(response)
        try:
            seconds = wav_duration(audio)
        except ValueError:
            raise ChatterboxFailure(NOT_AUDIO) from None
        return {"output_seconds": seconds, "audio_bytes": audio, "format": "wav"}

    async def _fetch_sample(self, voice_id: str) -> bytes:
        url = f"{self.settings.voice_service_url}/voices/{quote(voice_id, safe='')}/sample"
        try:
            # The voice service is local; no proxy applies. The contract sets no limit on this fetch.
            async with httpx.AsyncClient(timeout=None, trust_env=False) as client:
                response = await client.get(url)
        except (httpx.RequestError, httpx.InvalidURL):
            raise ChatterboxFailure(SAMPLE_UNREADABLE) from None
        if response.status_code != 200 or not response.content:
            raise ChatterboxFailure(SAMPLE_UNREADABLE)
        return response.content

    async def _obtain_identity_token(self) -> str:
        try:
            return await asyncio.to_thread(
                service_account_identity_token, self.settings.credentials_path, self.settings.url
            )
        except Exception:
            # Every way of not getting a token is the one cause OAF-4.
            raise ChatterboxFailure(TOKEN_UNAVAILABLE) from None

    async def _synthesize(self, script: str, language: str, sample: bytes, token: str) -> httpx.Response:
        limit = self.settings.time_limit
        try:
            # httpx applies no limit of its own; the one bound is the time limit, from sending to the full response.
            async with httpx.AsyncClient(timeout=None, follow_redirects=False) as client:
                request = client.build_request(
                    "POST",
                    f"{self.settings.url}/v1/synthesize",
                    data={"text": script, "language": language},
                    files={"sample_audio": ("sample", sample, "application/octet-stream")},
                    headers={"Authorization": f"Bearer {token}"},
                )
                return await asyncio.wait_for(client.send(request), timeout=limit)
        except asyncio.TimeoutError:
            raise ChatterboxFailure(TIMED_OUT.format(seconds=limit)) from None
        except (httpx.RequestError, httpx.InvalidURL):
            raise ChatterboxFailure(CANNOT_CONNECT) from None

    @staticmethod
    def _read_audio(response: httpx.Response) -> bytes:
        status = response.status_code
        if status in (401, 403):
            raise ChatterboxFailure(ACCESS_DENIED.format(status=status))
        if status != 200:
            raise ChatterboxFailure(SERVICE_ERROR.format(status=status))
        media_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if media_type != "audio/wav" or not response.content:
            raise ChatterboxFailure(NOT_AUDIO)
        return response.content
