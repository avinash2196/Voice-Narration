"""Consent public boundary; persistence remains owned by ConsentRepository."""
from functools import wraps
from threading import RLock
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from voice_narration._http import bearer, body, closed, install_errors, text, timestamp
from voice_narration._sql import actor, fail, identity, instant


def create_app(*, repository, authenticate, clock):
    if not callable(authenticate) or not callable(clock):
        fail("INVALID_CONFIGURATION")
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)

    lock = RLock()

    def serialized(operation):
        @wraps(operation)
        def invoke(*args, **kwargs):
            with lock:
                return operation(*args, **kwargs)
        return invoke

    def principal(account):
        if not isinstance(account, dict) or account.get("email_verified") is not True:
            fail("UNAUTHENTICATED")
        who = {"user_id": account.get("user_id"), "role": account.get("role")}
        actor(who)
        return who

    def result(record):
        if record["category"] != "consent":
            fail("NOT_FOUND")
        return dict(record["payload"])

    @serialized
    def record_consent(account, value):
        who = principal(account)
        closed(value, {"consenting_identity", "text", "version", "assisted"}, {"authorization"})
        for field in ("consenting_identity", "text", "version"):
            text(value[field])
        if type(value["assisted"]) is not bool:
            fail("INVALID_INPUT")
        if value["assisted"]:
            text(value.get("authorization"))
        elif "authorization" in value:
            fail("INVALID_INPUT")
        consent_id, now = str(uuid4()), instant(clock())
        consent = {"consent_id": consent_id, "owner_id": who["user_id"],
                   "consenting_identity": value["consenting_identity"], "text": value["text"],
                   "version": value["version"], "assisted": value["assisted"],
                   "authorization": value.get("authorization"), "status": "active",
                   "created_at": timestamp(now), "revoked_at": None}
        repository.save({"id": consent_id, "owner_id": who["user_id"],
                         "profile_id": consent_id, "consent_id": consent_id,
                         "category": "consent", "created_at": now, "payload": consent})
        return consent

    @serialized
    def read_consent(account, consent_id, owner_id):
        who = principal(account)
        identity(consent_id)
        now = instant(clock())
        if owner_id is None:
            reader = {"user_id": who["user_id"], "role": "User"}
        else:
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
            identity(owner_id)
            repository.permit(who, owner_id, "consents:read", now)
            reader = who
        record = repository.read(reader, consent_id, now=now)
        if owner_id is not None and record["owner_id"] != owner_id:
            fail("FORBIDDEN")
        return result(record)

    @serialized
    def validate_owner_consent(account, consent_id):
        who = principal(account)
        identity(consent_id)
        # Validation never consumes an administrator's read grant as owner consent.
        reader = {"user_id": who["user_id"], "role": "User"}
        record = repository.read(reader, consent_id, now=instant(clock()))
        consent = result(record)
        if consent["owner_id"] != who["user_id"]:
            fail("FORBIDDEN")
        if consent["status"] != "active":
            fail("CONSENT_REVOKED")
        return consent

    app.state.validate_owner_consent = validate_owner_consent

    @app.post("/api/v1/consent/record")
    async def record(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        consent = await run_in_threadpool(record_consent, account, value)
        return JSONResponse(status_code=201, content=consent)

    @app.get("/api/v1/consent/{consent_id}")
    def read(request: Request, consent_id: str):
        account = authenticate(bearer(request))
        if set(request.query_params) - {"owner_id"}:
            fail("INVALID_INPUT")
        return read_consent(account, consent_id, request.query_params.get("owner_id"))

    return app
