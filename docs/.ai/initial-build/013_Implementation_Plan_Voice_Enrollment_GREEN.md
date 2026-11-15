# Implementation Plan — Voice Enrollment GREEN

## Milestone and disposition

initial-build milestone14, Voice Enrollment GREEN; type GREEN. Predecessor13 is Complete and14 remains Pending. **Blocked draft — not ready for approval or execution.** The user explicitly selected “Review and retain current changes” after the working baseline changed. This revision reviews those retained changes and proposes only the exact corrections below. No working production/test/configuration/dependency change is applied during this planning task, and no Plan.md completion is recorded.


## Authoritative References

Work-item paths are under docs/.ai/initial-build.

| Read reference | Approval / role |
| --- | --- |
| requirements.md | Q12 approved 2026-10-26T17:12:20Z; FR-010/011/012/013, AC-ENR-001, Q11/Q12 govern. |
| Plan.md | 29-stage Q12 revision approved 2026-10-26T17:19:00Z; 13 Complete, 14 Pending. |
| contract/API-Contract.md | Q12 amendment approved 2026-10-26T17:39:41Z; current closed public/internal schemas, pagination, upload and safety rules. |
| Enrollment-Quality-Policy-Proposal.md | Approved Q11, 2026-10-25T21:03:55Z; complete deterministic measurement and future calibration gate. |
| Enrollment-Catalog-Seam-Correction-Proposal.md; Enrollment-Interface-Completion-Proposal.md | Approved catalog correction and Q12 A/B/C inputs; no private callback introspection. |
| 001_Implementation_Plan_Foundation.md | Approved/executed tooling, actual isolated PostgreSQL and loopback HTTP. |
| 002_Implementation_Plan_Model_Feasibility.md; model-eval/approved.md | Approved/executed investigation only; no production model or commercial clearance. |
| 003_Implementation_Plan_Persistence_RED.md; 004_Implementation_Plan_Persistence_RED_Recovery.md | Approved historical RED and verified recovery. |
| 005_Implementation_Plan_Persistence_GREEN.md; 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved/executed owner stores, canonical identities, scoped live grants/fences, atomic byte replacement. |
| 007_Implementation_Plan_Authentication_Consent_RED.md; 008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved/executed verified Auth and owner-only Consent seams. |
| 009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved/executed actual pinned decoder/resampler/native VAD, no calibration claim. |
| 010_Implementation_Plan_Voice_Enrollment_RED.md; 011_Implementation_Plan_Enrollment_Catalog_Test_Wiring_Correction.md | Approved/executed original feature tests and required catalog callable; history retained. |
| 012_Implementation_Plan_Enrollment_Interface_Completion_RED.md | Approved 2026-10-26T17:56:49Z and Complete; exact final interface, actual 40 RED cases and 57 preserved cases. |
| Contract-Review.md; voice_narration_PDD_requirements.md | Historical review and read-only subordinate product context. |
| tests/test_enrollment_quality.py; tests/test_voice_enrollment.py; tests/test_persistence.py; tests/test_authentication_consent.py; voice_narration/**/*.py; pytest.ini; requirements-dev.txt; requirements-evaluator.txt; tools/evaluator_readiness.py; compose.harness.yaml | Current repository evidence; not new product authority. |
| Installed commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/testing/SKILL.md; skills/security/SKILL.md; skills/python-fastapi/SKILL.md; skills/requirements-analysis/SKILL.md | Process guidance in production-engineering-standards 0.15.0. The implementation-planning skill requires disposable dry-run execution before review. |

No workspace AGENTS.md or product-level docs/requirements.md was found. Milestone14 remains Pending;013 is an unapproved draft, now revised after the user explicitly chose to review and retain the current changes. Current source is the retained baseline, not proof of approved milestone execution.


## Current retained baseline, provenance and predecessor evidence

Current HEAD is df9f0d8 (wheel-hash correction), following8e04f10 (prior artifacts/source including the original013 draft). At resume, git status reports two modified existing files (_http.py and voices/persistence.py) and five untracked new GREEN files (_enrollment.py, voices/quality.py, artifacts/application.py, ai/enrollment.py, voices/application.py). Their earlier provenance is not inferred from timestamps or commits. The user expressly resolved the baseline discrepancy by retaining them for review. They are now inputs, not newly applied proposed changes or verified milestone evidence. This replaces013's old claim that four modules are absent and its old create-five/modify-two execution scope. Retained byte hashes are below; the exact final contents replace only the three named current-baseline files after approval.

Predecessor012 records valid40-case missing-production RED twice (41.15s,35.84s), baseline57/57 in106.25s and postchange57/57 in98.60s, all84 original assertions retained. The current target SHA256 remains73164c87ce95cfb90d7c081b355d88644fefdf27c393ab4f9635e9278aad119e. Feature inventory40 plus regression inventory57 gives97. Those historical results do not prove later bodies passed. All four unchanged test files are preserved byte-exact during planning.

The first interrupted planning session's recovered output is6 acoustic passes in33.27s; its combined attempt was6 passed/91 errors in56.42s, exclusively Docker named-pipe permission denial, including fixture teardown denial. That was an environment failure, not GREEN evidence or a production defect. The current resumed sandbox attempt likewise reports6 passed/91 errors in81.68s from the actual Docker pipe denial. Host-context verification below uses only fixture-owned fresh resources; no engine/Desktop lifecycle action.

## Carried-forward decisions

001 retains pinned Python/tooling/PostgreSQL and actual loopback HTTP with dynamic ports/projects/private credentials.002 remains model investigation only.003–006 retain owner-separated SQL, canonical UUID/exact roles, live grants/fences and safe atomic byte replacement.007/008 retain real verified Auth and owner Consent.009 retains existing installed PyAV/NumPy/native WebRTC distribution, with current committed wheel-hash correction retained.010 retains actual six-finding/native-feature tests and explicit worker/history/provenance seams;011/012 retain required ordered list_capabilities, keyed capability(model), explicit pagination and multipart model input, independent profile-model revalidation and no fixture inference. No dependency/version/install/configuration change is proposed.

## Review of all seven retained changes

| Retained file | Review result and traceability |
| --- | --- |
| _enrollment.py | Verified canonical account/owner/model inputs, required explicit pagination mapping, closed duplicate query checks, unpredictable principal/filter/snapshot-bound cursors and serializer. Retained unchanged; Q10/Q12/012. |
| voices/quality.py | Actual selected-stream decoded PCM, per-channel16kHz resampling/native20ms VAD, real partial-frame weighting, six ordered findings, unrounded comparisons and six-place half-even values. Closed Q11 policy/readiness with no acoustic defaults. Retained unchanged; original six quality checks remain independent evidence. |
| artifacts/application.py | Retain model/consent/byte/duration/original-playback behavior; correct pre-consent spool, atomic publication, unknown-resource context and route prefix below. FR-010, Q10–Q12, contract Enrollment/Artifacts/common parsing. |
| ai/enrollment.py | Retain owner/live Consent, independent selected-model bounds and required-material selection, actual condition callback arguments, own transactional metadata/material records and repeat lookup. No final-result/mock/model shortcut introduced. FR-013/Q12. |
| voices/application.py | Retain durable profiles/history/provenance/reassessment/current-warning override/repeats, worker and listing semantics. Correct all five route prefixes to existing configured /api/v1 as required by current contract and delivered Auth/Consent/client. FR-011/012, Q11/Q12. |
| _http.py | Existing approved enrollment errors receive400/401/409 and unrelated mappings remain; retain unchanged. Q7 and contract errors. |
| voices/persistence.py | Existing update_payload uses canonical owner comparison, parameterized SQL, existing advisory transaction lock and live fence. No schema change. Retain unchanged for durable transitions/reopen; FR-012/Q11. |

All retained code uses required collaborators; no private catalog callback introspection, hardcoded synthetic model or operator duration/page default. Review does not claim full transport/configuration/catalog production wiring, human calibration or model commercial/runtime clearance. Existing explicit run_pending seam is the approved worker boundary for this milestone.

## Files in scope and ordered proposed changes

Create/delete no production file. Modify only these three files relative to the user-retained baseline:

1. voice_narration/artifacts/application.py: add MemoryUploadParser using the pinned parser callbacks but io.BytesIO for file parts, validate the four closed parts/count/types and configured file-byte limit while parsing, preserve the existing framework scalar field bound and close buffers on every outcome. Authentication precedes parsing; arbitrary part order is supported; no unconsented file bytes enter filesystem storage. Active owner consent and selected-model readiness still precede decode/domain use/persistence. Add a published sample transaction call. Public unknown artifact keeps404 NOT_FOUND; only internal enrollment references translate to409 ARTIFACT_UNAVAILABLE. Restore /api/v1 on upload/link/content routes and generated content URL.
2. voice_narration/artifacts/persistence.py: add publish_sample(record,data,*,validate) using existing own-store transaction/save/store_bytes, live consent validation before and immediately before commit, metadata-plus-byte-index atomic commit, and compensation of only its newly created UUID byte directory on failure. Existing save/read/store_bytes behavior and schema remain unchanged. This minimal extension is required to prevent a committed sample record without its original bytes; an application-level two-call sequence cannot establish that invariant.
3. voice_narration/voices/application.py: restore /api/v1 on the five existing public routes. The contract defines this configured prefix; delivered Auth/Consent and unchanged HTTP client's base URL already use it. No new endpoint.

Preserve all seven retained files except the exact two application replacements above; ArtifactRepository is the one additional necessary owned extension. All tests, other production, dependencies/configuration/build, prior authorities/history, user data and user Docker are unchanged. Plan.md execution evidence is an execution-only PDD exception after human approval and verification, not an edit authorized now.

## Technical choices for review

Use the existing pinned Starlette MultiPartParser lifecycle. Inspection of installed formparsers.py shows default file parts use SpooledTemporaryFile with a1MiB rollover; hence parsing request.form() before consent can persist unconsented bytes. The proposed subclass substitutes BytesIO at header completion without ever creating a spool, enforces configured max_upload_bytes on file callback data, and limits counts to the contract's one file/three scalars. It preserves Starlette's existing scalar max_part_size default rather than adding a new operator setting or disabling protection. Installed parse() catches BaseException and closes every registered buffer (including PersistenceError paths); upload finally closes the successful form. No filename content is retained or logged. These are internal mechanics of the existing closed multipart contract, not a public field/order/limit delta.

The owned publish_sample extension nests existing transactions, so its metadata/byte-index commit has one database outcome; the original file uses the existing fsync/os.replace path. Live consent callback failure rolls back publication and removes only the newly created directory. A process/power failure can still leave unreferenced private filesystem bytes between replacement and SQL commit; no cross-resource transaction guarantee is invented. They are never exposed without an active metadata/index record. Failed compensation is reported, not treated as success; later authorized cleanup/recovery remains necessary. Existing AI transactional material writes have the same filesystem limitation; no future distributed retry/cleanup feature is pulled into GREEN.

Existing process-local unpredictable cursors/link tokens remain retained. Frozen private profile pages recheck current ownership/Consent; application restart invalidates tokens and clients obtain a new page/link. Persisted profiles/history/provenance survive reopen. Required trusted capability/policy/calibration collaborators enforce real approval/evaluator identity before dependent work; no synthetic acceptance flag is read in production. Full scheduler/transport/configuration/capability providers, human calibration and selected-model clearance remain later gates.

## Retained baseline hashes

```text

voice_narration/_enrollment.py aef31c9b0b3cece39fa703be3fa79ca036dde837d935de0811d6e1baf4541885

voice_narration/voices/quality.py 208c4014a27095e306f699c2d261efd827851a9b2324133162ebf45fe5b29a81

voice_narration/artifacts/application.py 546932c5446aeeed1462303e6add15c8768ac0bc33612bf4fd9e8984d2ca3cdc

voice_narration/ai/enrollment.py b3790e2e8515ddf6392614d8d3961db5d187462347cc6c0632ca3fb3c646dc90

voice_narration/voices/application.py c86a41f89917e7ec0956f60d8084d7b0f94697e77c5667d9c45314d1acf47e5b

voice_narration/_http.py bf50672f5d2a7625882e013f22c98513d369e90732a0d53b4446d0e7332bd252

voice_narration/voices/persistence.py b69f0512890ebb03f8829ad0318de086f62ae5d6838a58acb8a135aed55935ad

```

## Exact proposed final content

These three complete files replace only their current retained counterparts after approval. All other retained source stays byte-exact. This representation avoids newline-sensitive patch context while preserving every proposed line for review.


### voice_narration/artifacts/application.py

```python
"""Owner-consented sample admission and authenticated original playback."""
from copy import deepcopy
from datetime import timedelta, datetime
import io
from secrets import token_urlsafe
from urllib.parse import urlencode
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile
from starlette.datastructures import Headers
from starlette.formparsers import MultiPartParser, MultiPartException
from python_multipart.multipart import parse_options_header

from voice_narration._enrollment import model, owner, principal, query, serializer
from voice_narration._http import bearer, install_errors, timestamp
from voice_narration._sql import PersistenceError, duration, fail, identity, instant
from voice_narration.voices.quality import decode, duration_bounds, rounded


MIME = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}


class MemoryUploadParser(MultiPartParser):
    """Parse arbitrary part order without writing unconsented file bytes to disk."""
    def __init__(self, headers, stream, maximum):
        super().__init__(headers, stream, max_files=1, max_fields=3)
        self.maximum = maximum
        self.file_bytes = 0

    def on_headers_finished(self):
        disposition, options = parse_options_header(self._current_part.content_disposition)
        if disposition != b"form-data" or b"name" not in options:
            fail("INVALID_INPUT")
        try:
            name = options[b"name"].decode("utf-8", errors="strict")
        except UnicodeError:
            raise PersistenceError("INVALID_INPUT") from None
        if name not in {"consent_id", "model_id", "model_version", "file"}:
            fail("INVALID_INPUT")
        self._current_part.field_name = name
        if b"filename" in options:
            self._current_files += 1
            if self._current_files > 1 or name != "file":
                fail("INVALID_INPUT")
            memory = io.BytesIO()
            self._files_to_close_on_error.append(memory)
            self._current_part.file = UploadFile(file=memory, size=0, filename="sample",
                                                headers=Headers(raw=self._current_part.item_headers))
        else:
            self._current_fields += 1
            if self._current_fields > 3 or name == "file":
                fail("INVALID_INPUT")
            self._current_part.file = None

    def on_part_data(self, data, start, end):
        if self._current_part.file is not None:
            self.file_bytes += end - start
            if self.file_bytes > self.maximum:
                fail("LIMIT_EXCEEDED")
        super().on_part_data(data, start, end)


def create_app(*, repository, authenticate, validate_consent, capability, settings, clock):
    required = {"max_upload_bytes", "max_samples_per_profile", "sample_min_seconds", "sample_max_seconds",
                "signed_link_seconds", "sample_days", "default_page_size", "max_page_size"}
    if not isinstance(settings, dict) or set(settings) != required:
        fail("INVALID_CONFIGURATION")
    for key in required - {"sample_min_seconds", "sample_max_seconds"}:
        duration(settings[key])
    duration_bounds({"sample_min_seconds": settings["sample_min_seconds"],
                     "sample_max_seconds": settings["sample_max_seconds"]})
    if not all(callable(value) for value in (authenticate, validate_consent, capability, clock)):
        fail("INVALID_CONFIGURATION")
    settings = deepcopy(settings)
    serialized = serializer()
    links = {}
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)

    def instant_from_text(value):
        return instant(datetime.fromisoformat(value.replace("Z", "+00:00")))

    @serialized
    def sample(account, artifact_id, owner_id=None):
        who = principal(account)
        reader = owner(account)
        if owner_id is not None:
            identity(owner_id)
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
            repository.permit(who, owner_id, "samples:read", instant(clock()))
            reader = who
        record = repository.read(reader, identity(artifact_id), now=instant(clock()))
        if owner_id is not None and record["owner_id"] != owner_id:
            fail("FORBIDDEN")
        payload = record["payload"]
        if record["category"] != "sample" or "artifact" not in payload:
            fail("ARTIFACT_UNAVAILABLE")
        artifact = deepcopy(payload["artifact"])
        if instant(clock()) >= instant_from_text(artifact["expires_at"]):
            fail("ARTIFACT_UNAVAILABLE")
        consent_account = dict(account, user_id=record["owner_id"], role="User")
        validate_consent(consent_account, record["consent_id"])
        return record, artifact, reader

    @serialized
    def enrollment_samples(account, consent_id, ids):
        owner(account)
        validate_consent(account, identity(consent_id))
        if (not isinstance(ids, list) or not ids or len(ids) > settings["max_samples_per_profile"] or
                any(not isinstance(value, str) for value in ids) or len(set(ids)) != len(ids)):
            fail("INVALID_INPUT")
        result = []
        for artifact_id in ids:
            try:
                record, artifact, reader = sample(account, artifact_id)
            except PersistenceError as exc:
                if exc.code == "NOT_FOUND":
                    fail("ARTIFACT_UNAVAILABLE")
                raise
            if record["consent_id"] != consent_id:
                fail("INVALID_INPUT")
            chunks = repository.read_bytes(reader, artifact_id, now=instant(clock()))
            if len(chunks) != 1:
                fail("ARTIFACT_UNAVAILABLE")
            decoded = decode(chunks[0], artifact["format"])
            result.append({"artifact_id": artifact_id, "bytes": chunks[0],
                           "stream_index": decoded["stream_index"], "artifact": artifact})
        return result

    @serialized
    def admit(account, consent_id, selected, data, fmt):
        who = owner(account)
        validate_consent(account, consent_id)
        cap = capability(selected)
        bounds = duration_bounds(cap, settings)
        decoded = decode(data, fmt)
        if not bounds[0] <= decoded["duration_seconds"] <= bounds[1]:
            fail("INVALID_AUDIO")
        now, artifact_id = instant(clock()), str(uuid4())
        expires = now + timedelta(days=settings["sample_days"])
        artifact = {"artifact_id": artifact_id, "owner_id": who["user_id"], "kind": "sample",
                    "consent_id": consent_id, "profile_id": None, "job_id": None,
                    "format": fmt, "size_bytes": len(data),
                    "duration_seconds": rounded(decoded["duration_seconds"]),
                    "sample_rate_hz": decoded["sample_rate_hz"], "created_at": timestamp(now),
                    "expires_at": timestamp(expires), "availability": "available"}
        validate_consent(account, consent_id)
        repository.publish_sample(
            {"id": artifact_id, "owner_id": who["user_id"], "profile_id": artifact_id,
             "consent_id": consent_id, "category": "sample", "created_at": now,
             "payload": {"artifact": artifact, "stream_index": decoded["stream_index"]}},
            data, validate=lambda: validate_consent(account, consent_id))
        return artifact

    @app.post("/api/v1/artifacts/upload")
    async def upload(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        content_type, _ = parse_options_header(request.headers.get("content-type", ""))
        if content_type != b"multipart/form-data":
            fail("INVALID_INPUT")
        try:
            form = await MemoryUploadParser(request.headers, request.stream(), settings["max_upload_bytes"]).parse()
        except (MultiPartException, UnicodeError, ValueError):
            raise PersistenceError("INVALID_INPUT") from None
        try:
            expected = {"consent_id", "model_id", "model_version", "file"}
            if set(form) != expected or any(len(form.getlist(k)) != 1 for k in form):
                fail("INVALID_INPUT")
            if any(not isinstance(form[k], str) for k in expected - {"file"}):
                fail("INVALID_INPUT")
            consent_id = identity(form["consent_id"])
            selected = model({"model_id": form["model_id"], "version": form["model_version"]})
            item = form["file"]
            if not isinstance(item, UploadFile):
                fail("INVALID_INPUT")
            fmt = next((key for key, value in MIME.items() if item.content_type == value), None)
            if fmt is None:
                fail("INVALID_AUDIO")
            await run_in_threadpool(validate_consent, account, consent_id)
            await run_in_threadpool(capability, selected)
            data = await item.read(settings["max_upload_bytes"] + 1)
            if len(data) > settings["max_upload_bytes"]:
                fail("LIMIT_EXCEEDED")
            artifact = await run_in_threadpool(admit, account, consent_id, selected, data, fmt)
            return JSONResponse(status_code=201, content=artifact)
        finally:
            await form.close()

    @serialized
    def link(account, artifact_id, params, disposition):
        if "format" in params:
            fail("UNSUPPORTED_FORMAT")
        record, artifact, _ = sample(account, artifact_id, params.get("owner_id"))
        expires = timestamp(instant(clock()) + timedelta(seconds=settings["signed_link_seconds"]))
        signature = token_urlsafe(32)
        parameters = {"signature": signature, "expires_at": expires,
                      "disposition": disposition, "format": artifact["format"]}
        links[signature] = (principal(account), artifact_id, deepcopy(parameters), params.get("owner_id"))
        return {"url": "/api/v1/artifacts/" + artifact_id + "/content?" + urlencode(parameters),
                "expires_at": expires, "artifact": artifact}

    @app.get("/api/v1/artifacts/{artifact_id}/preview-url")
    def preview(request: Request, artifact_id: str):
        return link(authenticate(bearer(request)), artifact_id, query(request, {"owner_id"}), "inline")

    @app.get("/api/v1/artifacts/{artifact_id}/download-url")
    def download(request: Request, artifact_id: str):
        return link(authenticate(bearer(request)), artifact_id, query(request, {"owner_id", "format"}), "attachment")

    @app.get("/api/v1/artifacts/{artifact_id}/content")
    def content(request: Request, artifact_id: str):
        account = authenticate(bearer(request))
        params = query(request, {"signature", "expires_at", "disposition", "format"})
        saved = links.get(params.get("signature"))
        if saved is None or saved[1] != artifact_id or saved[2] != params:
            fail("INVALID_LINK")
        if saved[0] != principal(account):
            fail("FORBIDDEN")
        if instant(clock()) >= instant_from_text(params["expires_at"]):
            fail("INVALID_LINK")
        if "range" in request.headers:
            fail("INVALID_INPUT")
        record, artifact, reader = sample(account, artifact_id, saved[3])
        chunks = repository.read_bytes(reader, artifact_id, now=instant(clock()))
        if len(chunks) != 1:
            fail("ARTIFACT_UNAVAILABLE")
        return Response(chunks[0], media_type=MIME[artifact["format"]],
                        headers={"Content-Disposition": params["disposition"]})

    app.state.enrollment_samples = enrollment_samples
    app.state.effective_settings = lambda: deepcopy(settings)
    app.state.close = repository.close
    return app
```


### voice_narration/artifacts/persistence.py

```python
"""artifacts-owned private SQL records, fences and cleanup."""
from datetime import datetime, timezone
from uuid import uuid4
import os
import re
from psycopg.types.json import Jsonb
from voice_narration._sql import (OwnerDatabase, PersistenceError, actor as checked_actor, after, duration,
                                  fail, identity, instant, retention)


class ArtifactRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("artifacts", (
            "CREATE TABLE artifacts_records (id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,category text NOT NULL,created_at timestamptz NOT NULL,payload jsonb NOT NULL,expires_at timestamptz)",
            "CREATE INDEX ON artifacts_records(owner_id,profile_id,consent_id)",
            "CREATE TABLE artifacts_cleanups (cleanup_id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,actor_id uuid NOT NULL,reason text NOT NULL,requested_at timestamptz NOT NULL,deadline_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('pending','running','completed','failed')),completed_at timestamptz,failure jsonb,UNIQUE(owner_id,profile_id,consent_id))",
            "CREATE TABLE artifacts_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",
            "CREATE TABLE artifacts_bytes (resource_id uuid NOT NULL REFERENCES artifacts_records(id) ON DELETE CASCADE,kind text NOT NULL,position bigint GENERATED ALWAYS AS IDENTITY,PRIMARY KEY(resource_id,kind))",
        ))

    @staticmethod
    def _record(row):
        return {"id": str(row[0]), "owner_id": str(row[1]), "profile_id": str(row[2]), "consent_id": str(row[3]),
                "category": row[4], "created_at": row[5], "payload": row[6]}

    @staticmethod
    def _cleanup(row):
        return {"cleanup_id": str(row[0]), "status": row[1], "requested_at": row[2],
                "deadline_at": row[3], "completed_at": row[4], "failure": row[5]}

    def _row(self, db, resource_id):
        identity(resource_id)
        row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM artifacts_records WHERE id=%s", (resource_id,)).fetchone()
        if row is None:
            fail("NOT_FOUND")
        return row

    def _fenced(self, db, owner_id, profile_id, consent_id):
        return db.execute("SELECT 1 FROM artifacts_cleanups WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", (owner_id, profile_id, consent_id)).fetchone() is not None

    def _active(self, db, row, now):
        if self._fenced(db, row[1], row[2], row[3]):
            fail("CONSENT_REVOKED")
        if row[7] is not None and instant(now) >= row[7]:
            fail("ARTIFACT_UNAVAILABLE" if row[4] in ("generated", "joined_preview") else "CONSENT_REVOKED")

    @staticmethod
    def _scope(category):
        return {"sample": "samples:read", "generated": "audio:read", "joined_preview": "audio:read"}.get(category)

    def save(self, record):
        fields = {"id", "owner_id", "profile_id", "consent_id", "category", "created_at", "payload"}
        if not isinstance(record, dict) or set(record) != fields:
            fail("INVALID_INPUT")
        for field in ("id", "owner_id", "profile_id", "consent_id"):
            identity(record[field])
        created = instant(record["created_at"])
        if not isinstance(record["category"], str) or not record["category"].strip() or not isinstance(record["payload"], dict):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if self._fenced(db, record["owner_id"], record["profile_id"], record["consent_id"]):
                fail("CONSENT_REVOKED")
            if db.execute("SELECT 1 FROM artifacts_records WHERE id=%s", (record["id"],)).fetchone():
                fail("INVALID_STATE")
            setting = db.execute("SELECT settings FROM artifacts_retention WHERE singleton=true").fetchone()
            field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(record["category"])
            expiry = after(created, duration(setting[0][field], 86400)) if setting is not None and field is not None else None
            db.execute("INSERT INTO artifacts_records(id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (record["id"], record["owner_id"], record["profile_id"], record["consent_id"], record["category"], created, Jsonb(record["payload"]), expiry))

    def publish_sample(self, record, data, *, validate):
        if record.get("category") != "sample" or not isinstance(data, bytes) or not data or not callable(validate):
            fail("INVALID_INPUT")
        created = False
        try:
            with self.transaction():
                validate()
                self.save(record)
                created = True
                self.store_bytes(record["id"], "original", data)
                validate()
        except BaseException:
            if created:
                self._erase(record["id"])
            raise

    def read(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            return self._record(row)

    def list(self, actor, *, owner_id, now):
        checked_actor(actor)
        identity(owner_id)
        with self.transaction() as db:
            categories = db.execute("SELECT DISTINCT category FROM artifacts_records WHERE owner_id=%s", (owner_id,)).fetchall()
            for (category,) in categories or [(None,)]:
                self.permit(actor, owner_id, self._scope(category), now)
        self._expire(now)
        with self.transaction() as db:
            rows = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM artifacts_records WHERE owner_id=%s ORDER BY created_at,id", (owner_id,)).fetchall()
            if not rows:
                self.permit(actor, owner_id, self._scope(None), now)
            result = []
            for row in rows:
                self.permit(actor, owner_id, self._scope(row[4]), now)
                if not self._fenced(db, row[1], row[2], row[3]) and (row[7] is None or instant(now) < row[7]):
                    result.append(self._record(row))
            return result

    def assert_usable(self, owner_id, profile_id, consent_id, *, now):
        for value in (owner_id, profile_id, consent_id):
            identity(value)
        self._expire(now)
        with self.transaction() as db:
            if self._fenced(db, owner_id, profile_id, consent_id):
                fail("CONSENT_REVOKED")

    def _fence(self, db, owner_id, actor_id, profile_id, consent_id, reason, now, window):
        row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM artifacts_cleanups WHERE owner_id=%s AND profile_id=%s AND consent_id=%s", (owner_id, profile_id, consent_id)).fetchone()
        if row:
            return self._cleanup(row)
        cleanup_id, deadline = str(uuid4()), after(now, duration(window))
        db.execute("INSERT INTO artifacts_cleanups(cleanup_id,owner_id,profile_id,consent_id,actor_id,reason,requested_at,deadline_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                   (cleanup_id, owner_id, profile_id, consent_id, actor_id, reason, now, deadline))
        return {"cleanup_id": cleanup_id, "status": "pending", "requested_at": now, "deadline_at": deadline, "completed_at": None, "failure": None}

    def fence(self, actor, *, profile_id, consent_id, reason, now, cleanup_window_seconds):
        user, _ = checked_actor(actor)
        identity(profile_id)
        identity(consent_id)
        now = instant(now)
        duration(cleanup_window_seconds)
        if reason not in ("profile_deleted", "consent_revoked", "sample_expired", "profile_expired", "consent_expired"):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            return self._fence(db, user, user, profile_id, consent_id, reason, now, cleanup_window_seconds)

    def cleanup(self, actor, cleanup_id):
        user, _ = checked_actor(actor)
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[6]) != user:
                fail("FORBIDDEN")
            return self._cleanup(row)

    def purge(self, cleanup_id, *, now):
        identity(cleanup_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id,profile_id,consent_id FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if row[1] == "completed":
                return self._cleanup(row)
            records = db.execute("SELECT id FROM artifacts_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9]).fetchall()
            try:
                for (resource_id,) in records:
                    self._erase(str(resource_id))
            except OSError:
                db.execute("UPDATE artifacts_cleanups SET status='failed',failure=%s WHERE cleanup_id=%s", (Jsonb({"code": "DEPENDENCY_UNAVAILABLE", "message": "Storage unavailable"}), cleanup_id))
            else:
                db.execute("DELETE FROM artifacts_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9])
                db.execute("UPDATE artifacts_cleanups SET status='completed',completed_at=%s,failure=NULL WHERE cleanup_id=%s", (now, cleanup_id))
            return self._cleanup(db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone())

    def inspect_private(self, resource_id):
        identity(resource_id)
        with self.transaction() as db:
            row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload FROM artifacts_records WHERE id=%s", (resource_id,)).fetchone()
            return self._record(row) if row else None

    def deletion_metadata(self, cleanup_id):
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT owner_id,actor_id,requested_at,profile_id,reason FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            return {"owner_id": str(row[0]), "actor_id": str(row[1]), "occurred_at": row[2], "resource_id": str(row[3]), "type": row[4]}

    def _expire(self, now):
        now = instant(now)
        with self.transaction() as db:
            setting = db.execute("SELECT settings FROM artifacts_retention WHERE singleton=true").fetchone()
            if setting is None:
                return
            for item in db.execute("SELECT id,owner_id,profile_id,consent_id,category FROM artifacts_records WHERE expires_at<=%s", (now,)).fetchall():
                if item[4] not in ("generated", "joined_preview"):
                    reason = {"profile": "profile_expired", "consent": "consent_expired", "sample": "sample_expired"}.get(item[4])
                    if reason is not None:
                        self._fence(db, str(item[1]), str(item[1]), str(item[2]), str(item[3]), reason, now, setting[0]["cleanup_window_seconds"])
                else:
                    self._erase_expired(db, str(item[0]))

    def apply_retention(self, policy, *, now):
        policy = retention(policy)
        now = instant(now)
        self._expire(now)
        with self.transaction() as db:
            db.execute("INSERT INTO artifacts_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(policy),))
            for resource_id, category, created_at in db.execute("SELECT id,category,created_at FROM artifacts_records").fetchall():
                field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(category)
                if field is not None:
                    expiry = after(created_at, duration(policy[field], 86400))
                    db.execute("UPDATE artifacts_records SET expires_at=%s WHERE id=%s", (expiry, resource_id))
        self._expire(now)

    def expiry(self, resource_id):
        with self.transaction() as db:
            return self._row(db, resource_id)[7]

    def _directory(self, resource_id):
        identity(resource_id)
        target = self._root / resource_id
        if target.is_symlink() or target.resolve().parent != self._root:
            fail("INVALID_INPUT")
        return target

    def _erase(self, resource_id):
        target = self._directory(resource_id)
        if target.exists():
            for entry in target.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    raise OSError("Unexpected storage directory")
                entry.unlink(missing_ok=True)
            target.rmdir()

    def _erase_expired(self, db, resource_id):
        try:
            self._erase(resource_id)
        except OSError:
            return
        db.execute("DELETE FROM artifacts_bytes WHERE resource_id=%s", (resource_id,))

    def store_bytes(self, resource_id, kind, data):
        self._expire(datetime.now(timezone.utc))
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self._active(db, row, datetime.now(timezone.utc))
            if not isinstance(kind, str) or not re.fullmatch(r"[a-z_]{1,64}", kind) or not isinstance(data, bytes):
                fail("INVALID_INPUT")
            directory = self._directory(resource_id)
            temporary = None
            try:
                directory.mkdir(exist_ok=True, mode=0o700)
                temporary = directory / ("tmp_" + uuid4().hex)
                with temporary.open("xb") as output:
                    output.write(data)
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temporary, directory / kind)
                db.execute("INSERT INTO artifacts_bytes(resource_id,kind) VALUES (%s,%s) ON CONFLICT(resource_id,kind) DO NOTHING", (resource_id, kind))
            except OSError:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
            finally:
                if temporary is not None and temporary.exists():
                    try:
                        temporary.unlink()
                    except OSError:
                        pass

    def read_bytes(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            kinds = db.execute("SELECT kind FROM artifacts_bytes WHERE resource_id=%s ORDER BY position", (resource_id,)).fetchall()
            directory = self._directory(resource_id)
            try:
                result = []
                for (kind,) in kinds:
                    path = directory / kind
                    if path.is_symlink():
                        fail("DEPENDENCY_UNAVAILABLE")
                    result.append(path.read_bytes())
                return result
            except OSError:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
```


### voice_narration/voices/application.py

```python
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
```

## Acceptance / Completion Criteria

1. After human approval apply only these exact three complete files to the retained baseline; no production/test/dependency/configuration/authority mutation beyond that scope.
2. All40 approved feature cases pass with actual decoder/native VAD, real HTTP and isolated owned SQL. Verify six measured findings; original bytes/selected stream; owner/model/format/count/byte/duration admission; readiness denial; warning/current acknowledgement/repeats/reassessment; durable profile metadata/transitions/provenance; configured ordered stable pagination; minimal independently selected-model materials. No skip/xfail/error or mocked final quality.
3. All57 preserved persistence/Auth/Consent cases pass. Combined97 passes twice without manual cleanup between invocations; unchanged fixtures assert effective override settings and isolated database/credentials/roots.
4. Existing contract safety remains: no pre-consent filesystem spooling; no committed sample without its original byte index; public unknown Artifact404 versus internal unavailable sample409. The proposed mechanisms were inspected and compiled, but dedicated runtime failure probes were not performed before the playback-seam blocker was found. This limitation remains explicit.
5. All tests, retained source outside the three exact replacements and all other dependencies/configuration remain byte-exact. No claim of natural Hindi/English calibration, human acceptance, production model/catalog/license readiness or user enablement.
6. Fixture-owned servers/databases/roles/unique Compose resources are torn down; pre-existing Docker engine/Desktop/resources remain untouched.

## Verification commands; Expected / Predicted — Not Yet Verified milestone evidence

Run from the actual repository only after approval/execution:

```powershell
.\.venv\Scripts\python.exe -m compileall -q voice_narration
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q --tb=short
git diff --check
git status --short
```

Expected / Predicted — Not Yet Verified: compile succeeds,97 passed per run with no failure/skip/xfail/error, preserved files' exact hashes, complete teardown with no leftover owned processes/resources. Only approved repository execution can supply milestone evidence; the disposable output below is planning evidence. Record actual commands/results and any contingency at execution; do not turn a failed check into a passing claim.

## Pre-authorized Contingencies

Observable Docker named-pipe or loopback bind permission denial permits only the identical verification invocation in normal host context, under normal review. Fixtures create/down only their own fresh vnred UUID projects on the already-running engine. Never start/stop/restart Docker engine/Desktop or pre-existing containers. No source/approach/test/criterion/dependency change is authorized; behavior failure stops execution for planning, not rerun-until-pass.

## Rollback and recovery

Retain the actual baseline bytes of the three modified files before approved execution; restore only those exact three baseline files. Preserve the user's seven retained changes and all other work. No repository-wide reset/clean/checkout, no database schema migration or user-record deletion. Private unpublished partial bytes are unavailable; failures stay failures and require owned diagnosis/cleanup. A crash during external conditioning may require explicit diagnosis before a retry; no Jobs exactly-once protocol or training promise is made.

## Risks, coverage limits and canonical comparisons

Authenticated user_id, persisted owner_id and all consent/artifact/profile/assessment IDs use the same lowercase UUID identity()/actor() form. Roles compare exact User/Administrator enums. Model IDs use canonical UUID and exact nonblank unnormalized version. Private reads compare authenticated owner or require the existing live scoped Administrator grant and explicit owner_id match; conditioning always owner-only. Worker identity derives only from its trusted owned profile record. Link signatures bind canonical principal/role, artifact,format,disposition,expiry, and every access rechecks live authorization/Consent. Cursors bind canonical principal, exact filters and frozen records with live private checks. SQL uses parameters and separate owner credentials; safe UUID paths and atomic byte replacement remain in owned repositories. No sample bytes/filenames/materials/transcripts/private names are logged.

The97-case unchanged inventory is the approved GREEN gate, not exhaustive coverage of every common API parsing or future failure interleaving. The identified parser/publication corrections were inspected/compiled but have not received dedicated injected-failure runtime verification; no waived criterion or success is inferred. Natural voices/identity/language suitability and commercial/runtime/model calibration remain untested here and gated later. Current native VAD screening cannot guarantee speech/identity quality. Process-local tokens require new first pages/links after restart. SQL and filesystem do not provide a power-failure atomic distributed transaction; no inaccessible residual private bytes are labeled published.

## Explicit exclusions

No working source/test edit during planning, new test/dependency/configuration default, package/model/audio acquisition, private voice/calibration/reviewer outreach, training, model/license clearance, hidden fixture identity/operator bound, catalog callback introspection, full transport/Jobs/frontend/scheduler, future features, authority amendment/self-approval/Plan completion, commit/push/publication or Docker engine/Desktop lifecycle change.

## Planning-time dry run — not milestone evidence

Disposable current-baseline copy: C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\013-enrollment-retained-scratch-94da87310fc548ee9a3601531db26086. It contains selected source/tests/containers/Compose/pytest/manifests, baseline source snapshots and temporary helpers/logs; no.git/.venv/credentials/model/private voice. It uses the actual existing interpreter with scratch CWD. The earlier scratch607bf698… is historical disposable planning code, never the working baseline. Actual results and cleanup follow; the confirmed test-seam contradiction blocks completion.


### Actual commands and trimmed real output

All runtime commands used the existing interpreter below with CWD equal to the disposable retained-scratch path above. No working source was applied. First invocation used sandbox context; the identical second invocation used normal host context after actual named-pipe denial and successful normal approval review.

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe' -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q --tb=short
```

Sandbox result, exit1:

```text
subprocess stderr: permission denied while trying to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
6 passed, 91 errors in 81.68s (0:01:21)
```

Host result, exit1 (planning-time dry run, not milestone evidence):

```text
FAILED tests/test_voice_enrollment.py::test_guidance_formats_playback_admission_and_originals
test_voice_enrollment.py:251: assert content.status_code == 200 and content.content == data
E assert (404 == 200)
FAILED tests/test_voice_enrollment.py::test_multistream_metadata_playback_and_conditioning
test_voice_enrollment.py:513: assert playback.status_code == 200 and playback.content == data
E assert (404 == 200)
2 failed, 95 passed in 422.15s (0:07:02)
isolated persistence project: vnred43f9001117744c95b3a2a4f65c51ebbd
container: 92a20176ffcb77fc0a806c501ca7fa1547a83961e812aca477a1c3baf339e5dc
```

Exactly38 feature cases and57 preserved cases passed; both playback cases failed. No setup/teardown error, skip or xfail in the host result. The first playback case stopped before later assertions in that body; no success is claimed for unreached statements. There was no second97-case run, since repeating a known contradiction would not establish repeatable GREEN.

Actual URL-merging diagnostic, run from the working repository without importing production or changing files:

```powershell
& '.\.venv\Scripts\python.exe' -c "import httpx; c=httpx.Client(base_url='http://127.0.0.1:1234/api/v1'); print(c.build_request('GET','/api/v1/artifacts/example/content').url); print(c.build_request('GET','/artifacts/example/content').url)"
```

```text
http://127.0.0.1:1234/api/v1/api/v1/artifacts/example/content
http://127.0.0.1:1234/api/v1/artifacts/example/content
```

The confirmed contradiction is described with a complete unapplied test diff in [Enrollment-Playback-Link-Test-Correction-Proposal.md](Enrollment-Playback-Link-Test-Correction-Proposal.md). The valid API-prefixed returned URL is retained in this proposed production code. No invalid URL, production alias or silent test edit is used to obtain a pass. The user must review the narrow proposal and normal Plan/OTHER chain before tests change; then013 can be finalized and its disposable97 cases run twice.

Actual static checks, scratch CWD unless noted:

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe' -m compileall -q voice_narration
git apply --check ..\proposed.diff
git apply --ignore-space-change --check ..\proposed.diff
```

Compile exited0 with no output. Initial diff checks used CWD scratch/baseline, containing byte-preserved baseline source. Plain apply check failed on ArtifactRepository CRLF context; newline-aware --ignore-space-change check exited0 with no output. A later blank-context whitespace-normalization probe failed with corrupt patch at line18; that representation was discarded. No production code was changed after the host run. Final exact code is represented as complete file contents, avoiding newline-sensitive patch context altogether. A temporary helper compared the root's11-entry retained baseline manifest: all11 current source/test hashes match; all four scratch test files byte-match working tests. No template comment; exactly three complete final-content sections. A helper initially used the wrong relative path for proposed.diff and received FileNotFoundError before reading a file; the corrected path produced the diagnostic above. These are documentary/static-helper corrections, not hidden runtime reruns.

Temporary artifacts: original607bf698… disposable copy; retained94da8731… copy with selected prerequisites, baseline snapshots, bytecode/cache, revise_plan.py, finish_blocked.py, check_proposal.py and proposed.diff; fixture-owned temporary databases/roles/roots/HTTP resources. Cleanup status is recorded below after final containment checks.


## Per-file exactness review

artifacts/application.py: complete final content covers every proposed line, no placeholder; changes match Proposed Changes and existing Q10/Q11/Q12/contract boundaries. artifacts/persistence.py: complete final content including the necessary owned publication method, no schema/default/dependency; live consent and private-original safety trace to existing contract. voices/application.py: complete final content with the five-route prefix correction, no new public endpoint/input. All other retained seven-file components reviewed and byte-preserved. Each final code block exactly matches the compiled/dry-run disposable source; no code changed after the host run. No ellipsis/pseudocode/template comments or newly reused authority identifier;013 remains a revision of the existing draft, not a new approved artifact.

## Cleanup and final preservation

Read-only host checks for the exact observed project used docker ps -a, docker network ls and docker volume ls with label com.docker.compose.project=vnred43f9001117744c95b3a2a4f65c51ebbd; all exited0 with empty output. All97-case invocation teardown completed without errors. No executor-started server/process remains. The existing fixtures closed their own connections/servers and removed their own projects; no Docker engine/Desktop/pre-existing resource lifecycle operation occurred.

Both explicitly named disposable copies were removed in one PowerShell session after resolving/checking absolute containment under the explicit visualization root. Temporary copies, baseline snapshots, bytecode/cache and all helper/diff artifacts were removed. The planning documents retain trimmed actual evidence; no runtime evidence is promoted to a milestone pass. Final manifest comparison: all11 retained working source/test hashes match. Only013 and the new unapproved playback test-correction proposal are this planning task's lasting changes.
