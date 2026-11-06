"""
Inference Adapter – M020 & M022 Green Implementation

Provides FastAPI application for TTS inference with pluggable provider backends.
Supports mock (testing), Google Cloud, and Azure Speech providers.

M020: Mock Inference Adapter GREEN
M022: Approved Model Test Prerequisites (provider registry)
"""

import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .db import SessionLocal, create_all_tables
from .models import Generation, Voice
from .providers import InferenceProvider, MockInferenceProvider
from .registry import ProviderRegistry
from .storage import AudioStorage


def get_default_provider_name() -> str:
    """
    Get default provider name from environment or use mock.

    Returns:
        Provider name ("mock", "google", or "azure")
    """
    return os.getenv("INFERENCE_PROVIDER", "mock")


def get_default_provider_config() -> dict:
    """
    Get provider configuration from environment variables.

    Returns:
        Configuration dict for the provider
    """
    provider_name = get_default_provider_name()

    if provider_name == "google":
        return {
            "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        }
    elif provider_name == "azure":
        return {
            "api_key": os.getenv("AZURE_SPEECH_KEY"),
            "region": os.getenv("AZURE_SPEECH_REGION"),
        }
    else:
        return {}


class InferenceState:
    """
    Manages inference execution state and orchestration.

    Coordinates with the Jobs service (M017) for job persistence
    and state management. Provides deterministic worker seam for testing.
    """

    def __init__(
        self,
        provider: InferenceProvider,
        jobs_app: Optional[FastAPI] = None,
        job_repository = None,
    ):
        """
        Initialize inference state.

        Args:
            provider: InferenceProvider instance
            jobs_app: FastAPI jobs application (for future integration)
            job_repository: Job repository for persistence
        """
        self.provider = provider
        self.jobs_app = jobs_app
        self.job_repository = job_repository
        self._pending_inferences = {}
        self._storage_root = Path(
            os.getenv("AUDIO_STORAGE_PATH", str(Path(__file__).resolve().parents[2] / "audio_storage"))
        ).resolve()
        self.storage = None
        self._persisted_generations_path = self._storage_root / "generation_index.json"
        self._persisted_generations = {}
        self.storage_root = self._storage_root
        self._ensure_database()

    @property
    def storage_root(self) -> Path:
        return self._storage_root

    @storage_root.setter
    def storage_root(self, value):
        self._storage_root = Path(value).resolve()
        self.storage = AudioStorage(self._storage_root)
        self._persisted_generations_path = self._storage_root / "generation_index.json"
        self._persisted_generations = self._load_persisted_generations()

    def _ensure_database(self) -> None:
        try:
            create_all_tables()
        except Exception:
            pass

    def _load_persisted_generations(self) -> dict:
        if not self._persisted_generations_path.exists():
            return {}
        try:
            with open(self._persisted_generations_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            if isinstance(payload, dict):
                return payload
        except (json.JSONDecodeError, OSError):
            pass
        return {}

    def _save_persisted_generations(self) -> None:
        self.storage_root.mkdir(parents=True, exist_ok=True)
        with open(self._persisted_generations_path, "w", encoding="utf-8") as handle:
            json.dump(self._persisted_generations, handle, indent=2, sort_keys=True)

    def persist_generation(self, job_id: str, script: str, voice_id: str, output: dict) -> dict:
        if not job_id or not script or not voice_id:
            raise ValueError("Missing required fields: job_id, script, voice_id")

        audio_bytes = output.get("audio_bytes", b"")
        file_path = self.storage.save_audio(audio_bytes, voice_id, prefix=job_id)
        created_at = datetime.now(timezone.utc)
        duration_seconds = float(output.get("output_seconds", 0.0) or 0.0)
        entry = {
            "job_id": job_id,
            "text": script,
            "voice_id": voice_id,
            "duration_seconds": duration_seconds,
            "file_path": file_path,
            "format": output.get("format", "wav"),
            "status": "complete",
            "created_at": created_at.isoformat(),
        }
        self._persisted_generations[job_id] = entry
        self._save_persisted_generations()

        try:
            self._ensure_database()
            with SessionLocal() as db:
                voice_record = db.query(Voice).filter(Voice.id == voice_id).first()
                if voice_record is None:
                    voice_record = Voice(
                        id=voice_id,
                        name=voice_id,
                        language=(voice_id.split("-")[0] if "-" in voice_id else "unknown"),
                        gender="neutral",
                        is_active=True,
                    )
                    db.add(voice_record)

                generation_record = Generation(
                    id=str(uuid.uuid4()),
                    job_id=job_id,
                    text=script,
                    voice_id=voice_id,
                    duration_seconds=duration_seconds,
                    file_path=file_path,
                    status="completed",
                    created_at=created_at,
                    expires_at=created_at + timedelta(days=int(os.getenv("AUDIO_RETENTION_DAYS", "30"))),
                )
                db.add(generation_record)
                db.commit()
        except Exception:
            pass

        return entry

    def get_persisted_generation(self, job_id: str) -> Optional[dict]:
        if not job_id:
            return None
        self._persisted_generations = self._load_persisted_generations()
        return self._persisted_generations.get(job_id)

    def list_persisted_generations(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        voice_id: Optional[str] = None,
        created_at_from: Optional[str] = None,
        created_at_to: Optional[str] = None,
        search: Optional[str] = None,
    ) -> dict:
        self._persisted_generations = self._load_persisted_generations()
        entries = sorted(
            list(self._persisted_generations.values()),
            key=lambda item: item.get("created_at") or "",
            reverse=True,
        )

        if voice_id:
            entries = [item for item in entries if item.get("voice_id") == voice_id]
        if created_at_from:
            entries = [item for item in entries if (item.get("created_at") or "") >= created_at_from]
        if created_at_to:
            entries = [item for item in entries if (item.get("created_at") or "") <= created_at_to]
        if search:
            needle = search.lower()
            entries = [item for item in entries if needle in (item.get("text") or "").lower()]

        total = len(entries)
        page = entries[skip:skip + limit]
        return {"items": page, "total": total, "skip": skip, "limit": limit}

    def get_generation_file_bytes(self, job_id: str) -> bytes:
        entry = self.get_persisted_generation(job_id)
        if entry:
            file_path = self.storage_root / entry["file_path"]
            if file_path.exists():
                return file_path.read_bytes()

        if job_id in self._pending_inferences:
            output = self._pending_inferences[job_id]
            return output.get("audio_bytes", b"")

        raise ValueError(f"Job {job_id} not found or no output available")

    def delete_persisted_generation(self, job_id: str) -> dict:
        if not job_id:
            raise ValueError("job_id is required")

        entry = self.get_persisted_generation(job_id)
        if entry:
            file_path = entry.get("file_path")
            if file_path:
                try:
                    self.storage.delete_file(file_path)
                except Exception:
                    pass

        self._persisted_generations.pop(job_id, None)
        self._save_persisted_generations()
        self._pending_inferences.pop(job_id, None)

        try:
            with SessionLocal() as db:
                generation_record = db.query(Generation).filter(Generation.job_id == job_id).first()
                if generation_record is not None:
                    db.delete(generation_record)
                    db.commit()
        except Exception:
            pass

        return {"job_id": job_id, "deleted": True}

    async def submit_for_inference(
        self,
        job_id: str,
        script: str,
        voice_id: str,
        owner_id: Optional[str] = None,
    ) -> dict:
        """
        Submit a job for inference.

        In mock implementation, generates output immediately.
        In production, would queue for background worker processing.

        Args:
            job_id: Job identifier
            script: Text to synthesize
            voice_id: Voice identifier
            owner_id: Owner/account identifier

        Returns:
            dict with job_id, status, duration_seconds

        Raises:
            ValueError: If job not found or invalid
        """
        if not job_id or not script or not voice_id:
            raise ValueError("Missing required fields: job_id, script, voice_id")

        print(f"[TTS] Generating audio for: script='{script}' voice={voice_id}")
        
        # Generate inference output
        output = await self.provider.generate(script, voice_id)
        
        print(f"[TTS] Generated audio: {len(output.get('audio_bytes', b''))} bytes, {output['output_seconds']:.2f} seconds")

        # Store the output for later retrieval
        self._pending_inferences[job_id] = output
        self.persist_generation(job_id, script, voice_id, output)

        return {
            "job_id": job_id,
            "status": "complete",
            "duration_seconds": output["output_seconds"],
        }

    async def get_inference_output(
        self,
        job_id: str,
        owner_id: Optional[str] = None,
    ) -> dict:
        """
        Retrieve inference output for a completed job.

        Args:
            job_id: Job identifier
            owner_id: Owner/account identifier

        Returns:
            dict with audio_bytes (base64), format and duration_seconds

        Raises:
            ValueError: If job not found or has no output
        """
        if not job_id:
            raise ValueError("job_id is required")

        # Retrieve stored output from inference
        if job_id not in self._pending_inferences:
            raise ValueError(f"Job {job_id} not found or no output available")

        output = self._pending_inferences[job_id]
        
        # Encode audio_bytes as base64 for JSON transport
        import base64
        audio_b64 = base64.b64encode(output.get("audio_bytes", b"")).decode("utf-8")
        
        return {
            "audio_bytes": audio_b64,
            "format": output.get("format", "wav"),
            "duration_seconds": output.get("output_seconds", 1.0),
        }

    async def list_backends(self) -> list:
        """
        List available inference backends via provider registry.

        Enables runtime provider selection without code changes.

        Returns:
            List of backend descriptors
        """
        backends = []
        for provider_name in ProviderRegistry.list_providers():
            try:
                # Get a test instance to query capabilities
                if provider_name == "mock":
                    desc = "Deterministic mock for testing (no external deps)"
                elif provider_name == "google":
                    desc = "Google Cloud Text-to-Speech (requires GOOGLE_APPLICATION_CREDENTIALS)"
                elif provider_name == "azure":
                    desc = "Azure Cognitive Services Speech (requires AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)"
                else:
                    desc = f"Custom {provider_name} provider"

                backends.append({
                    "name": provider_name,
                    "provider_class": ProviderRegistry._providers[provider_name].__name__,
                    "description": desc,
                })
            except Exception:
                pass

        return backends

    async def run_pending(self) -> int:
        """
        Deterministic worker seam for test verification.

        In mock implementation, returns 0 (no pending work).
        In production, would process queued inference jobs asynchronously.

        Returns:
            Number of jobs processed
        """
        return 0

    async def close(self) -> None:
        """Cleanup resources on shutdown."""
        pass


def create_app(
    *,
    provider: Optional[InferenceProvider] = None,
    jobs_app: Optional[FastAPI] = None,
    job_repository = None,
) -> FastAPI:
    """
    Create FastAPI application for inference adapter.

    Follows the application factory pattern established by M017 (Jobs)
    and M016 (Voices/Artifacts). All dependencies are injected via
    keyword-only parameters.

    Args:
        provider: InferenceProvider instance (defaults to MockInferenceProvider)
        jobs_app: Jobs application for orchestration dependency
        job_repository: Repository for job persistence

    Returns:
        FastAPI application with inference routes and app.state bound to InferenceState
    """
    if provider is None:
        provider = MockInferenceProvider()

    app = FastAPI(title="Voice Narration Inference Adapter")
    
    # Add CORS middleware for frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    state = InferenceState(provider, jobs_app, job_repository)
    app.state.inference = state

    # Dependency injection helper
    async def get_inference_state() -> InferenceState:
        return app.state.inference

    # ============================================================================
    # HTTP Endpoints
    # ============================================================================

    @app.post("/inference/jobs/{job_id}/infer")
    async def submit_job_for_inference(
        job_id: str,
        request: Request,
        state: InferenceState = Depends(get_inference_state),
    ) -> JSONResponse:
        """
        Submit a job for inference.

        Request body JSON:
        {
            "script": "Text to synthesize",
            "voice_id": "voice-identifier"
        }

        Returns:
        {
            "job_id": "uuid",
            "status": "complete",
            "duration_seconds": 1.5
        }
        """
        try:
            body = await request.json()
            script = body.get("script")
            voice_id = body.get("voice_id")

            if not script or not voice_id:
                return JSONResponse(
                    content={"error": "Missing required fields: script, voice_id"},
                    status_code=400,
                )

            result = await state.submit_for_inference(job_id, script, voice_id)
            return JSONResponse(content=result, status_code=200)
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Inference failed: {str(e)}"},
                status_code=500,
            )

    @app.get("/inference/jobs/{job_id}/output")
    async def get_inference_output(
        job_id: str,
        request: Request,
        state: InferenceState = Depends(get_inference_state),
    ) -> JSONResponse:
        """
        Retrieve inference output for a completed job.

        Returns:
        {
            "audio_bytes": "base64-encoded or binary",
            "format": "wav",
            "duration_seconds": 1.5
        }
        """
        try:
            output = await state.get_inference_output(job_id)
            return JSONResponse(content=output, status_code=200)
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=404)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Output retrieval failed: {str(e)}"},
                status_code=500,
            )

    @app.get("/inference/jobs/{job_id}/download")
    async def download_generation(
        job_id: str,
        state: InferenceState = Depends(get_inference_state),
    ) -> Response:
        try:
            payload = state.get_persisted_generation(job_id)
            if not payload:
                payload = {"voice_id": "generation", "job_id": job_id}
            audio_bytes = state.get_generation_file_bytes(job_id)
            filename = f"{payload.get('voice_id', 'generation')}_{job_id}.wav"
            return Response(
                content=audio_bytes,
                media_type="audio/wav",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            )
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    @app.get("/inference/generations")
    async def list_generations(
        request: Request,
        state: InferenceState = Depends(get_inference_state),
    ) -> JSONResponse:
        try:
            params = request.query_params
            skip = max(0, int(params.get("skip", "0")))
            limit = max(1, min(100, int(params.get("limit", "20"))))
            voice_id = params.get("voice_id")
            created_at_from = params.get("created_at_from")
            created_at_to = params.get("created_at_to")
            search = params.get("search")
            result = state.list_persisted_generations(
                skip=skip,
                limit=limit,
                voice_id=voice_id,
                created_at_from=created_at_from,
                created_at_to=created_at_to,
                search=search,
            )
            return JSONResponse(content=result, status_code=200)
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)
        except Exception as e:
            return JSONResponse(content={"error": f"History listing failed: {str(e)}"}, status_code=500)

    @app.get("/inference/generations/{job_id}")
    async def get_generation_detail(
        job_id: str,
        state: InferenceState = Depends(get_inference_state),
    ) -> JSONResponse:
        try:
            entry = state.get_persisted_generation(job_id)
            if entry is None:
                raise ValueError(f"Generation {job_id} not found")
            return JSONResponse(content=entry, status_code=200)
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"error": f"Generation lookup failed: {str(e)}"}, status_code=500)

    @app.delete("/inference/generations/{job_id}")
    async def delete_generation(
        job_id: str,
        state: InferenceState = Depends(get_inference_state),
    ) -> JSONResponse:
        try:
            result = state.delete_persisted_generation(job_id)
            return JSONResponse(content=result, status_code=200)
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"error": f"Generation deletion failed: {str(e)}"}, status_code=500)

    @app.get("/inference/backends")
    async def list_backends(
        state: InferenceState = Depends(get_inference_state),
    ) -> JSONResponse:
        """
        List available inference backends.

        Returns:
        {
            "backends": [
                {
                    "name": "mock",
                    "provider_class": "MockInferenceProvider",
                    "description": "..."
                }
            ]
        }
        """
        try:
            backends = await state.list_backends()
            return JSONResponse(content={"backends": backends}, status_code=200)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Backend listing failed: {str(e)}"},
                status_code=500,
            )

    # ============================================================================
    # Lifecycle Hooks
    # ============================================================================

    @app.on_event("shutdown")
    async def shutdown_event():
        await state.close()

    return app


# Create default app instance for uvicorn
app = create_app()
