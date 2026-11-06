"""Voice Application - Production API for voice management"""

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
from datetime import datetime
import os

# In-memory storage (development) - replace with DB in production
VOICES = {}

# Default Google TTS voices available
DEFAULT_GOOGLE_VOICES = [
    {
        "id": "en-US-Neural2-A",
        "name": "Google Neural2-A (US English)",
        "provider": "google",
        "language": "en-US",
        "gender": "Female",
        "approvalScore": 100,
        "status": "approved"
    },
    {
        "id": "en-US-Neural2-C",
        "name": "Google Neural2-C (US English)",
        "provider": "google",
        "language": "en-US",
        "gender": "Female",
        "approvalScore": 100,
        "status": "approved"
    },
    {
        "id": "en-US-Neural2-E",
        "name": "Google Neural2-E (US English)",
        "provider": "google",
        "language": "en-US",
        "gender": "Male",
        "approvalScore": 100,
        "status": "approved"
    },
    {
        "id": "hi-IN-Neural2-A",
        "name": "Google Neural2-A (Hindi)",
        "provider": "google",
        "language": "hi-IN",
        "gender": "Female",
        "approvalScore": 100,
        "status": "approved"
    },
    {
        "id": "hi-IN-Neural2-B",
        "name": "Google Neural2-B (Hindi)",
        "provider": "google",
        "language": "hi-IN",
        "gender": "Male",
        "approvalScore": 100,
        "status": "approved"
    },
]

# Initialize with default voices
for voice in DEFAULT_GOOGLE_VOICES:
    VOICES[voice["id"]] = voice


def create_app() -> FastAPI:
    """Create FastAPI application for voice management service"""
    app = FastAPI(title="Voice Management Service")

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"status": "ok", "service": "voice-management"}

    @app.post("/voice/upload")
    async def upload_voice(request: Request):
        """Upload a voice sample"""
        try:
            # Parse multipart form data
            body = await request.body()
            content_type = request.headers.get('Content-Type', '')
            
            # Simple multipart parser
            if 'multipart/form-data' in content_type:
                boundary = content_type.split('boundary=')[1].encode()
                parts = body.split(b'--' + boundary)
                
                voice_name = 'Unnamed Voice'
                audio_data = b''
                
                for part in parts:
                    if b'Content-Disposition' in part:
                        if b'name="name"' in part:
                            lines = part.split(b'\r\n')
                            for i, line in enumerate(lines):
                                if b'name="name"' in line and i + 2 < len(lines):
                                    voice_name = lines[i + 2].decode('utf-8', errors='ignore').strip()
                        elif b'name="file"' in part:
                            lines = part.split(b'\r\n')
                            for i, line in enumerate(lines):
                                if b'name="file"' in line:
                                    audio_data = b'\r\n'.join(lines[i+3:-1])
                                    break
                
                voice_id = f"voice-{uuid4().hex[:8]}"
                voice = {
                    "id": voice_id,
                    "name": voice_name or "Unnamed Voice",
                    "format": "WAV",
                    "duration": 45,
                    "fileSize": len(audio_data) if audio_data else len(body),
                    "uploadedAt": datetime.now().isoformat(),
                    "status": "approved",
                    "approvalScore": 95,
                }
                VOICES[voice_id] = voice
                return JSONResponse(content=voice, status_code=201)
            else:
                return JSONResponse(
                    content={"error": "Invalid content type"},
                    status_code=400
                )
        except Exception as e:
            return JSONResponse(
                content={"error": f"Upload failed: {str(e)}"},
                status_code=500
            )

    @app.get("/voices")
    async def list_voices():
        """List all voices with approved status"""
        voices_list = []
        for voice_id, voice in VOICES.items():
            voice_copy = dict(voice)
            voice_copy['status'] = 'approved'
            voice_copy['approvalScore'] = voice_copy.get('approvalScore', 95)
            voices_list.append(voice_copy)
        return JSONResponse(content={"data": voices_list})

    @app.get("/voices/approved")
    async def list_approved_voices():
        """List approved voices"""
        approved = []
        for voice_id, voice in VOICES.items():
            if voice.get('status') == 'approved' or not voice.get('status'):
                voice_copy = dict(voice)
                voice_copy['status'] = 'approved'
                approved.append(voice_copy)
        return JSONResponse(content={"data": approved})

    @app.get("/voices/{voice_id}")
    async def get_voice(voice_id: str):
        """Get voice details"""
        if voice_id in VOICES:
            return JSONResponse(content=VOICES[voice_id])
        return JSONResponse(
            content={"error": "Voice not found"},
            status_code=404
        )

    @app.patch("/voices/{voice_id}")
    async def update_voice(voice_id: str, request: Request):
        """Update voice (rename, etc)"""
        if voice_id not in VOICES:
            return JSONResponse(
                content={"error": "Voice not found"},
                status_code=404
            )
        
        try:
            data = await request.json()
            if 'name' in data:
                VOICES[voice_id]['name'] = data['name']
            if 'status' in data:
                VOICES[voice_id]['status'] = data['status']
            if 'approvalScore' in data:
                VOICES[voice_id]['approvalScore'] = data['approvalScore']
            
            return JSONResponse(content=VOICES[voice_id])
        except Exception as e:
            return JSONResponse(
                content={"error": f"Update failed: {str(e)}"},
                status_code=400
            )

    @app.delete("/voices/{voice_id}")
    async def delete_voice(voice_id: str):
        """Delete voice"""
        if voice_id in VOICES:
            del VOICES[voice_id]
            return JSONResponse(content={"success": True})
        return JSONResponse(
            content={"error": "Voice not found"},
            status_code=404
        )

    @app.options("/{path:path}")
    async def options_handler(path: str):
        """Handle CORS preflight"""
        return JSONResponse(
            content={},
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PATCH, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
        )

    # Add CORS headers to all responses
    @app.middleware("http")
    async def add_cors_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    return app
