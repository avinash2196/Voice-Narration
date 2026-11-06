"""Bootstrap Voice Management Service

Runs the voice management service on port 8002.

Environment:
  VOICE_SERVICE_PORT: Port to run on (default: 8002)
"""

import os
import sys
import uvicorn

from voice_narration.simple_voices.application import create_app


def main():
    """Start the voice management service"""
    port = int(os.getenv("VOICE_SERVICE_PORT", "8002"))
    
    print(f"\n[Voice Service] Creating application...", file=sys.stderr)
    app = create_app()
    
    print(f"[Voice Service] Starting server on 0.0.0.0:{port}", file=sys.stderr)
    print(f"[Voice Service] Ready to accept voice uploads", file=sys.stderr)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
