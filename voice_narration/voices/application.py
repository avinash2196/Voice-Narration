"""Durable profile admission, acoustic assessment and explicit worker seam."""
from copy import deepcopy
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from voice_narration._enrollment import Pages, model, owner, principal, query, serializer
from voice_narration._http import bearer, body, closed, install_errors, text, timestamp
from voice_narration._sql import PersistenceError, fail, identity, instant
from voice_narration.voices.quality import assess, decode, duration_bounds, validate_policy


STATES = {"pending", "quality_checking", "awaiting_user_override", "enrolling", "enrolled", "failed", "revoked"}


def create_app(*, repository, authenticate, validate_consent, artifacts, enrollment, capability,
               list_capabilities, pagination, policy_snapshot, calibration, clock):
    pages = Pages(pagination)
    if not all(callable(value) for value in (authenticate, validate_consent, artifacts, capability,
                                            list_capabilities, policy_snapshot, calibration, clock)):
        fail("INVALID_CONFIGURATION")
    serialized = serializer()
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)

    def readiness(selected):
        cap = capability(selected)
        bounds = duration_bounds(cap)
        snapshot = policy_snapshot()
        if (not isinstance(snapshot, dict) or snapshot.get("enrollment_quality") is None or
                type(snapshot.get("revision")) is not int or snapshot["revision"] < 0):
            fail("CONFIGURATION_REQUIRED")
        policy = validate_policy(snapshot["enrollment_quality"])
        calibration(policy, snapshot["revision"])
        return cap, bounds, snapshot["revision"], policy

    def load(account, profile_id, owner_id=None):
        who = principal(account)
        reader = owner(account)
        if owner_id is not None:
            identity(owner_id)
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
            repository.permit(who, owner_id, "profiles:read", instant(clock()))
            reader = who
        record = repository.read(reader, identity(profile_id), now=instant(clock()))
        if record["category"] != "profile":
            fail("NOT_FOUND")
        if owner_id is not None and record["owner_id"] != owner_id:
            fail("FORBIDDEN")
        consent_account = dict(account, user_id=record["owner_id"], role="User")
        validate_consent(consent_account, record["consent_id"])
        return deepcopy(record["payload"])

    def persist(account, data):
        repository.update_payload(owner(account), data["profile"]["profile_id"], data, now=instant(clock()))

    def transition(account, data, state):
        data["profile"]["status"] = state
        data["profile"]["updated_at"] = timestamp(clock())
        if not data["history"] or data["history"][-1] != state:
            data["history"].append(state)
        persist(account, data)

    def current_samples(account, profile, bounds):
        samples = artifacts(account, profile["consent_id"], [s["artifact_id"] for s in profile["samples"]])
        decoded = [decode(item["bytes"], item["artifact"]["format"]) for item in samples]
        if any(not bounds[0] <= item["duration_seconds"] <= bounds[1] for item in decoded):
            fail("INVALID_INPUT")
        return samples, decoded

    @serialized
    def create(account, value):
        who = owner(account)
        closed(value, {"name", "language", "consent_id", "sample_artifact_ids", "model"})
        text(value["name"])
        selected = model(value["model"])
        consent_id = identity(value["consent_id"])
        validate_consent(account, consent_id)
        cap, bounds, revision, policy = readiness(selected)
        if value["language"] not in ("hi", "en") or value["language"] not in cap["languages"]:
            fail("UNSUPPORTED_CAPABILITY")
        samples = artifacts(account, consent_id, value["sample_artifact_ids"])
        for sample in samples:
            decoded = decode(sample["bytes"], sample["artifact"]["format"])
            if not bounds[0] <= decoded["duration_seconds"] <= bounds[1]:
                fail("INVALID_INPUT")
        profile_id, now = str(uuid4()), instant(clock())
        profile = {"profile_id": profile_id, "owner_id": who["user_id"], "name": value["name"],
                   "language": value["language"], "consent_id": consent_id,
                   "samples": [deepcopy(item["artifact"]) for item in samples], "model": selected,
                   "status": "pending", "quality": None, "failure": None,
                   "created_at": timestamp(now), "updated_at": timestamp(now)}
        repository.save({"id": profile_id, "owner_id": who["user_id"], "profile_id": profile_id,
                         "consent_id": consent_id, "category": "profile", "created_at": now,
                         "payload": {"profile": profile, "history": ["pending"], "provenance": {}}})
        return deepcopy(profile)

    def evaluate(account, data, bounds, revision, policy):
        profile = data["profile"]
        transition(account, data, "quality_checking")
        samples, decoded = current_samples(account, profile, bounds)
        findings = assess(decoded, policy=policy, duration_bounds=bounds)
        if any(item["severity"] == "failure" for item in findings):
            fail("INVALID_AUDIO")
        assessment_id = str(uuid4())
        warnings = any(item["severity"] == "warning" for item in findings)
        profile["quality"] = {"assessment_id": assessment_id, "findings": findings,
                              "override_allowed": warnings, "override_acknowledged": False}
        data["provenance"][assessment_id] = {
            "revision": revision, "evaluator": policy["vad"]["artifact_ref"],
            "calibration_ref": policy["calibration_ref"],
            "stream_indices": [item["stream_index"] for item in decoded]}
        data["assessment_policy"] = deepcopy(policy)
        transition(account, data, "awaiting_user_override" if warnings else "enrolling")

    @serialized
    def run_pending(profile_id):
        identity(profile_id)
        with repository.transaction():
            record = repository.inspect_private(profile_id)
            if record is None or record["category"] != "profile":
                fail("NOT_FOUND")
            data = deepcopy(record["payload"])
            profile = data["profile"]
            if profile["status"] in ("enrolled", "failed", "revoked"):
                return
            account = {"user_id": record["owner_id"], "role": "User", "email_verified": True}
            try:
                validate_consent(account, profile["consent_id"])
                repository.assert_usable(record["owner_id"], profile_id, profile["consent_id"], now=instant(clock()))
                cap, bounds, revision, policy = readiness(profile["model"])
                quality = profile["quality"]
                provenance = data["provenance"].get(quality["assessment_id"]) if quality else None
                obsolete = quality is not None and (provenance["revision"] != revision or
                                                     data.get("assessment_policy") != policy)
                if profile["status"] in ("pending", "quality_checking") or obsolete:
                    evaluate(account, data, bounds, revision, policy)
                if profile["status"] == "enrolling":
                    samples, decoded = current_samples(account, profile, bounds)
                    validate_consent(account, profile["consent_id"])
                    enrollment.enroll(account, deepcopy(profile), samples)
                    validate_consent(account, profile["consent_id"])
                    transition(account, data, "enrolled")
            except PersistenceError as exc:
                profile["quality"] = None
                profile["failure"] = {"code": exc.code, "message": exc.code.replace("_", " ").capitalize(),
                                      "action": "Restore consent, resources or readiness and create a new profile."}
                try:
                    transition(account, data, "revoked" if exc.code == "CONSENT_REVOKED" else "failed")
                except PersistenceError as safety:
                    if safety.code != "CONSENT_REVOKED":
                        raise

    @serialized
    def acknowledge(account, profile_id, value):
        closed(value, {"assessment_id", "acknowledged"})
        identity(value["assessment_id"])
        if value["acknowledged"] is not True:
            fail("INVALID_INPUT")
        with repository.transaction():
            data = load(account, profile_id)
            profile = data["profile"]
            quality = profile["quality"]
            if profile["status"] in ("failed", "revoked", "pending", "quality_checking") or quality is None:
                fail("INVALID_STATE")
            if profile["status"] != "enrolled":
                cap, bounds, revision, policy = readiness(profile["model"])
                provenance = data["provenance"][quality["assessment_id"]]
                if provenance["revision"] != revision or data.get("assessment_policy") != policy:
                    evaluate(account, data, bounds, revision, policy)
                    return None
            if value["assessment_id"] != quality["assessment_id"]:
                fail("STALE_ASSESSMENT")
            if not quality["override_allowed"]:
                fail("OVERRIDE_NOT_ALLOWED")
            if quality["override_acknowledged"] and profile["status"] in ("enrolling", "enrolled"):
                return deepcopy(profile)
            if profile["status"] != "awaiting_user_override":
                fail("INVALID_STATE")
            quality["override_acknowledged"] = True
            transition(account, data, "enrolling")
            return deepcopy(profile)

    @app.post("/api/v1/voices")
    async def create_profile(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        profile = await run_in_threadpool(create, account, value)
        return JSONResponse(status_code=202, content=profile)

    @app.patch("/api/v1/voices/{profile_id}/quality-override")
    async def override(request: Request, profile_id: str):
        account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        result = await run_in_threadpool(acknowledge, account, profile_id, value)
        if result is None:
            fail("STALE_ASSESSMENT")
        return result

    @app.get("/api/v1/voices/{profile_id}")
    def read(request: Request, profile_id: str):
        account = authenticate(bearer(request))
        params = query(request, {"owner_id"})
        return serialized(load)(account, profile_id, params.get("owner_id"))["profile"]

    @serialized
    def listing(account, parameters):
        who = principal(account)
        target = parameters.get("owner_id", who["user_id"])
        reader = owner(account)
        if "owner_id" in parameters:
            identity(target)
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
            repository.permit(who, target, "profiles:read", instant(clock()))
            reader = who
        if "language" in parameters and parameters["language"] not in ("hi", "en"):
            fail("INVALID_INPUT")
        if "status" in parameters and parameters["status"] not in STATES:
            fail("INVALID_INPUT")

        def records():
            rows = repository.list(reader, owner_id=target, now=instant(clock()))
            profiles = [row["payload"]["profile"] for row in rows if row["category"] == "profile"]
            profiles = [p for p in profiles if all(p[key] == parameters[key] for key in ("language", "status")
                                                  if key in parameters)]
            return sorted(profiles, key=lambda p: (p["created_at"], p["profile_id"]), reverse=True)
        page = pages.page(account, "voices", parameters, records)
        for profile in page["items"]:
            load(account, profile["profile_id"], parameters.get("owner_id"))
        return page

    @app.get("/api/v1/voices")
    def list_profiles(request: Request):
        account = authenticate(bearer(request))
        return listing(account, query(request, {"cursor", "limit", "language", "status", "owner_id"}))

    @app.get("/api/v1/models")
    def list_models(request: Request):
        account = authenticate(bearer(request))
        return serialized(pages.page)(account, "models", query(request, {"cursor", "limit"}), list_capabilities)

    @serialized
    def diagnostic(profile_id, assessment_id=None):
        record = repository.inspect_private(identity(profile_id))
        if record is None or record["category"] != "profile":
            fail("NOT_FOUND")
        data = record["payload"]
        if assessment_id is None:
            return deepcopy(data["history"])
        identity(assessment_id)
        if assessment_id not in data["provenance"]:
            fail("NOT_FOUND")
        return deepcopy(data["provenance"][assessment_id])

    app.state.run_pending = run_pending
    app.state.transition_history = diagnostic
    app.state.assessment_provenance = diagnostic
    app.state.close = repository.close
    return app
