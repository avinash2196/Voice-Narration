"""
Bootstrap script for Voice Narration Inference Service (TTS)
Runs on port 8003
"""

import os
import sys
import uvicorn
from concurrent.futures import ThreadPoolExecutor

from voice_narration.inference.application import create_app
from voice_narration.inference.providers import GoogleTextToSpeechProvider, MockInferenceProvider

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def _safe_init_google_provider():
    """Initialize Google TTS in a worker thread with a startup timeout."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set")

    provider = GoogleTextToSpeechProvider({
        "credentials_path": credentials_path,
    })
    return provider


def get_provider():
    """Get TTS provider based on environment."""
    provider_name = os.getenv("INFERENCE_PROVIDER", "mock")

    print(f"[Inference] Using provider: {provider_name}")

    if provider_name == "google":
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_safe_init_google_provider)
                provider = future.result(timeout=8)
            print("[Inference] [OK] Google Cloud TTS provider initialized")
            return provider
        except TimeoutError:
            print("[Inference] [WARN] Google TTS initialization timed out; falling back to mock provider")
            return MockInferenceProvider()
        except Exception as e:
            print(f"[Inference] [ERROR] Failed to initialize Google TTS: {e}")
            print("[Inference] Falling back to mock provider")
            return MockInferenceProvider()
    elif provider_name == "azure":
        print("[Inference] Azure provider not yet implemented, using mock")
        return MockInferenceProvider()
    else:
        print("[Inference] Using mock provider")
        return MockInferenceProvider()


if __name__ == "__main__":
    provider = get_provider()
    app = create_app(provider=provider)

    port = int(os.getenv("INFERENCE_PORT", "8003"))
    host = os.getenv("INFERENCE_HOST", "0.0.0.0")

    print(f"[Inference] Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
