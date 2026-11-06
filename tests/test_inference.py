"""Mock inference adapter tests.

Synthetic zero-latency model invocation, silent audio output.
No real TTS, model inference, or audio codecs.
"""

import pytest
from fastapi.testclient import TestClient
from voice_narration.inference import application as inference_app_module


@pytest.fixture
def inference_app():
    """Minimal Inference app with mock provider for testing."""
    app = inference_app_module.create_app()
    return app


@pytest.fixture
def inference_client(inference_app):
    """Test client for inference app."""
    return TestClient(inference_app)


# RED Test: Module verification

class TestInferenceAdapterRED:
    """RED: Module exists and can be imported."""

    def test_inference_module_missing(self):
        """Verify voice_narration.inference module exists and is importable."""
        try:
            from voice_narration.inference import application
            from voice_narration.inference import MockInferenceProvider, InferenceProvider, InferenceState, create_app

            assert callable(create_app)
            assert MockInferenceProvider is not None
            assert InferenceProvider is not None
            assert InferenceState is not None
        except ImportError as e:
            pytest.fail(f"Failed to import inference module: {e}")


# GREEN Tests: Production implementation

class TestInferenceBasics:
    """Basic inference functionality."""

    @pytest.mark.asyncio
    async def test_submit_job_for_inference(self, inference_app, inference_client):
        """Submit a job for inference."""
        response = inference_client.post(
            "/inference/jobs/test-job-123/infer",
            json={
                "script": "Hello world",
                "voice_id": "voice-001"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == "test-job-123"
        assert data["status"] == "complete"
        assert "duration_seconds" in data
        assert data["duration_seconds"] >= 1.0


class TestInferenceExecution:
    """Inference execution and output generation."""

    @pytest.mark.asyncio
    async def test_mock_inference_generates_output(self, inference_app):
        """Mock inference provider generates output."""
        state = inference_app.state.inference
        provider = state.provider

        output = await provider.generate("Test script", "voice-001")

        assert isinstance(output, dict)
        assert "output_seconds" in output
        assert "audio_bytes" in output
        assert "format" in output
        assert output["output_seconds"] > 0
        assert isinstance(output["audio_bytes"], bytes)
        assert output["format"] == "wav"
        assert len(output["audio_bytes"]) > 0

    @pytest.mark.asyncio
    async def test_inference_timing_matches_script_length(self, inference_app):
        """Verify synthetic timing: 1 second per 100 characters."""
        state = inference_app.state.inference
        provider = state.provider

        test_cases = [
            ("Short", 1.0),  # 5 chars -> 1 sec
            ("This is a longer script with more content", 1.0),  # 42 chars -> 1 sec
            ("X" * 100, 1.0),  # 100 chars -> 1 sec
            ("X" * 200, 2.0),  # 200 chars -> 2 sec
            ("X" * 250, 2.5),  # 250 chars -> 2.5 sec
            ("X" * 500, 5.0),  # 500 chars -> 5 sec
        ]

        for script, expected_seconds in test_cases:
            output = await provider.generate(script, "voice-001")
            assert output["output_seconds"] == expected_seconds, \
                f"Script length {len(script)} should produce {expected_seconds}s"

    @pytest.mark.asyncio
    async def test_mock_inference_returns_wav_bytes(self, inference_app):
        """Mock inference returns valid WAV format."""
        state = inference_app.state.inference
        provider = state.provider

        output = await provider.generate("Test script", "voice-001")

        # Check WAV file signature
        assert output["audio_bytes"].startswith(b"RIFF"), "WAV must start with RIFF"
        assert b"WAVE" in output["audio_bytes"], "WAV must contain WAVE marker"
        assert output["format"] == "wav"


class TestOutputRetrieval:
    """Output retrieval from completed jobs."""

    @pytest.mark.asyncio
    async def test_retrieve_inference_output_by_job_id(self, inference_client):
        """Retrieve inference output by job ID."""
        # Submit for inference
        submit_response = inference_client.post(
            "/inference/jobs/test-job-456/infer",
            json={
                "script": "Test audio content",
                "voice_id": "voice-002"
            }
        )
        assert submit_response.status_code == 200

        # Retrieve output
        response = inference_client.get("/inference/jobs/test-job-456/output")
        assert response.status_code == 200

        data = response.json()
        assert "format" in data
        assert "duration_seconds" in data
        assert data["format"] == "wav"


class TestBackendManagement:
    """Backend listing and management."""

    @pytest.mark.asyncio
    async def test_list_available_inference_backends(self, inference_client):
        """List available inference backends."""
        response = inference_client.get("/inference/backends")
        assert response.status_code == 200

        data = response.json()
        assert "backends" in data
        assert isinstance(data["backends"], list)
        assert len(data["backends"]) >= 3

        # Check that mock backend exists (may not be first due to alphabetical sorting)
        backend_names = [b["name"] for b in data["backends"]]
        assert "mock" in backend_names
        assert "google" in backend_names
        assert "azure" in backend_names

        # Verify each backend has required fields
        for backend in data["backends"]:
            assert "name" in backend
            assert "provider_class" in backend
            assert "description" in backend


class TestInferenceErrorHandling:
    """Error handling and state transitions."""

    @pytest.mark.asyncio
    async def test_failed_inference_transitions_job(self, inference_client):
        """Error handling returns appropriate error response."""
        # Submit without required voice_id (should fail)
        response = inference_client.post(
            "/inference/jobs/test-job-789/infer",
            json={
                "script": "Test"
                # Missing voice_id
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    @pytest.mark.asyncio
    async def test_missing_script_returns_error(self, inference_client):
        """Missing script returns 400 error."""
        response = inference_client.post(
            "/inference/jobs/test-job-999/infer",
            json={
                "voice_id": "voice-001"
                # Missing script
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    @pytest.mark.asyncio
    async def test_invalid_job_id_returns_error(self, inference_client):
        """Invalid job_id handling."""
        # Empty job_id should be handled gracefully
        response = inference_client.post(
            "/inference/jobs//infer",
            json={
                "script": "Test",
                "voice_id": "voice-001"
            }
        )

        # Should return 404 or 400 depending on routing
        assert response.status_code in [400, 404, 405]
