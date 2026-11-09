from __future__ import annotations

import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parents[2]
AUDIO_ROOT = ROOT / "audio_storage"
AUDIO_ROOT.mkdir(exist_ok=True)
DB_PATH = AUDIO_ROOT / "voice_profiles.db"
VOICE_DIR = AUDIO_ROOT / "voices"
VOICE_DIR.mkdir(exist_ok=True)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS voice_profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                user_id TEXT NOT NULL,
                language TEXT NOT NULL,
                consent TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'approved',
                sample_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                model TEXT NOT NULL DEFAULT 'google-tts'
            )
            """
        )
        conn.commit()


_ensure_db()

app = FastAPI(title="Simple Voices Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _serialize(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "user_id": row["user_id"],
        "language": row["language"],
        "consent": row["consent"],
        "status": row["status"],
        "sample_path": row["sample_path"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "model": row["model"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "simple_voices"}


@app.get("/voices")
def list_voices(user_id: str | None = None) -> list[dict[str, Any]]:
    with _connect() as conn:
        if user_id:
            rows = conn.execute(
                "SELECT * FROM voice_profiles WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM voice_profiles ORDER BY created_at DESC"
            ).fetchall()
    return [_serialize(row) for row in rows]


@app.post("/voices")
async def create_voice(
    name: str = Form(...),
    user_id: str = Form(...),
    language: str = Form("en-US"),
    consent: str = Form("explicit consent recorded"),
    audio_file: UploadFile = File(...),
) -> dict[str, Any]:
    if not name.strip():
        raise HTTPException(status_code=400, detail="Voice name is required")

    payload = await audio_file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Audio sample is required")

    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip()) or "voice"
    voice_dir = VOICE_DIR / user_id
    voice_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{safe_name}.wav"
    sample_path = voice_dir / filename
    sample_path.write_bytes(payload)

    voice_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO voice_profiles (
                id, name, user_id, language, consent, status, sample_path,
                created_at, updated_at, model
            ) VALUES (?, ?, ?, ?, ?, 'approved', ?, ?, ?, 'google-tts')
            """,
            (
                voice_id,
                name,
                user_id,
                language,
                consent,
                str(sample_path),
                now,
                now,
            ),
        )
        conn.commit()
        profile = _serialize(
            conn.execute("SELECT * FROM voice_profiles WHERE id = ?", (voice_id,)).fetchone()
        )
    return profile


@app.post("/voices/{voice_id}/approve")
def approve_voice(voice_id: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with _connect() as conn:
        row = conn.execute("SELECT * FROM voice_profiles WHERE id = ?", (voice_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Voice not found")
        conn.execute(
            "UPDATE voice_profiles SET status = 'approved', updated_at = ? WHERE id = ?",
            (now, voice_id),
        )
        conn.commit()
        refreshed = conn.execute("SELECT * FROM voice_profiles WHERE id = ?", (voice_id,)).fetchone()
    return _serialize(refreshed)


@app.delete("/voices/{voice_id}")
def revoke_voice(voice_id: str) -> dict[str, str]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with _connect() as conn:
        row = conn.execute("SELECT * FROM voice_profiles WHERE id = ?", (voice_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Voice not found")
        conn.execute(
            "UPDATE voice_profiles SET status = 'revoked', updated_at = ? WHERE id = ?",
            (now, voice_id),
        )
        conn.commit()
    return {"status": "revoked", "voice_id": voice_id}


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
