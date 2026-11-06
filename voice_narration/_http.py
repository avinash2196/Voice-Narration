"""Stateless public HTTP validation and safe contract errors."""
from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from voice_narration._sql import PersistenceError, fail, instant


STATUS = {"INVALID_INPUT": 400, "INVALID_TOKEN": 400,
          "UNAUTHENTICATED": 401, "INVALID_CREDENTIALS": 401,
          "FORBIDDEN": 403, "EMAIL_UNVERIFIED": 403, "NOT_FOUND": 404,
          "TOKEN_CONSUMED": 409, "CONSENT_REVOKED": 409,
          "INVALID_STATE": 409, "INVALID_AUDIO": 400, "LIMIT_EXCEEDED": 400,
          "UNSUPPORTED_FORMAT": 400, "UNSUPPORTED_CAPABILITY": 400, "INVALID_CURSOR": 400,
          "INVALID_LINK": 401, "ARTIFACT_UNAVAILABLE": 409,
          "STALE_ASSESSMENT": 409, "OVERRIDE_NOT_ALLOWED": 409}


def timestamp(value):
    return instant(value).isoformat().replace("+00:00", "Z")


def closed(body, required, optional=()):
    if not isinstance(body, dict) or not set(required) <= set(body):
        fail("INVALID_INPUT")
    if set(body) - set(required) - set(optional):
        fail("INVALID_INPUT")
    return body


def text(value):
    if not isinstance(value, str) or not value.strip():
        fail("INVALID_INPUT")
    return value


async def body(request: Request):
    try:
        return await request.json()
    except (ValueError, UnicodeError):
        raise PersistenceError("INVALID_INPUT") from None


def bearer(request):
    value = request.headers.get("authorization", "")
    parts = value.split()
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        fail("UNAUTHENTICATED")
    return parts[1]


def install_errors(app, clock):
    def response(code):
        return JSONResponse(status_code=STATUS.get(code, 503), content={"error": {
            "code": code, "message": code.replace("_", " ").capitalize(),
            "details": [], "request_id": str(uuid4()), "timestamp": timestamp(clock())}})

    @app.exception_handler(PersistenceError)
    async def persistence_error(request, exc):
        return response(exc.code)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return response("INVALID_INPUT")

    @app.exception_handler(HTTPException)
    async def http_error(request, exc):
        return response("NOT_FOUND" if exc.status_code == 404 else "INVALID_INPUT")

    @app.exception_handler(Exception)
    async def unexpected_error(request, exc):
        return response("INTERNAL_UNAVAILABLE")
