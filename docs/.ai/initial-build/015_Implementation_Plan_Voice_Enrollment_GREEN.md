# Implementation Plan — Voice Enrollment GREEN

## Milestone and authority

initial-build milestone 15, **GREEN**. This is the revised GREEN proposal following completed milestone 14 OTHER 014. It supersedes the unapproved, blocked 013 proposal for future execution only; 013 remains unchanged history. No approved, unexecuted GREEN Implementation Plan exists. This document does not approve itself, implement the working files, change the Plan status or enable a real model.

## Human Review

Status: **Executed - Voice Enrollment GREEN complete after recorded re-approval 2026-10-28T01:10:47Z. Two fresh working-tree runs passed 97/97 (743.72s and 623.70s); exact source/tests and owned cleanup verified. See Plan.md re-approved verification resume evidence; prior stopped execution remains history.**

## Authoritative References

Work-item references are under docs/.ai/initial-build unless indicated.

| Read reference | Authority / status |
| --- | --- |
| requirements.md | Q12 approved 2026-10-26T17:12:20Z; FR-010–013, AC-ENR-001, active consent/privacy and Q11/Q12 constrain this milestone. |
| Plan.md | Playback-correction revision approved 2026-10-27T04:35:33Z; milestone 14 Complete, milestone 15 GREEN Pending; all 40 feature cases plus 57 regressions must pass. |
| contract/API-Contract.md | Q12 approved 2026-10-26T17:39:41Z; existing public prefix, closed enrollment DTOs/errors, model/consent gates, ordered findings and Artifact Link/access rules. Unchanged by this proposal. |
| Enrollment-Quality-Policy-Proposal.md | Q11 approved 2026-10-25T21:03:55Z; exact measurement, aggregation, warnings, readiness and future human calibration obligations. |
| Enrollment-Catalog-Seam-Correction-Proposal.md; Enrollment-Interface-Completion-Proposal.md | Approved catalog/Q12 decisions; explicit keyed and listing capability collaborators, pagination and model-aware uploads. |
| Enrollment-Playback-Link-Test-Correction-Proposal.md | Approved 2026-10-27T04:26:57Z; corrected standard URL resolution is now delivered by 014. |
| 001_Implementation_Plan_Foundation.md | Approved/executed tooling, dependency pins, dynamic loopback, Compose/PostgreSQL/owner-root isolation. |
| 002_Implementation_Plan_Model_Feasibility.md; model-eval/approved.md | Approved investigation/protocol only; no production model, commercial clearance or natural-voice acceptance. |
| 003_Implementation_Plan_Persistence_RED.md; 004_Implementation_Plan_Persistence_RED_Recovery.md | Historical approved RED/stopped and verified recovery; exact persistent contracts and command-only -p no:anyio retained. |
| 005_Implementation_Plan_Persistence_GREEN.md; 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved owner-local persistence and verified recovery, eight separate credentials/roots, canonical IDs, live grants/fences and atomic byte replacement. |
| 007_Implementation_Plan_Authentication_Consent_RED.md; 008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved/completed actual Auth/Consent transport and owner validation; 57 delivered regressions. |
| 009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved/completed native decoder/resampler/VAD prerequisites, exact evaluator manifest and notice limits. |
| 010_Implementation_Plan_Voice_Enrollment_RED.md; 011_Implementation_Plan_Enrollment_Catalog_Test_Wiring_Correction.md | Approved/completed original feature tests and catalog collaborator; history retained. |
| 012_Implementation_Plan_Enrollment_Interface_Completion_RED.md | Approved/completed Q12 RED; 40 actual intended missing-production errors twice after real prerequisites; full original assertions and 57 regressions preserved. |
| 013_Implementation_Plan_Voice_Enrollment_GREEN.md | Unapproved, blocked draft and planning-only 95-pass/two-playback-failure evidence; no execution authority. Proposed Artifact mechanics reviewed as input, not blindly reapplied. |
| 014_Implementation_Plan_Enrollment_Playback_Link_Test_Wiring_Correction.md | Approved 2026-10-27T05:28:04Z and executed: baseline 57/57 in 162.79s, post 57/57 in 197.26s; all 97 IDs/order, 127 original assertions plus one origin assertion and owned cleanup verified. |
| voice_narration_PDD_requirements.md; Contract-Review.md | Subordinate original product context and historical review; no supersession of approved Q11/Q12. No product-level docs/requirements.md or workspace AGENTS.md exists. |
| voice_narration/**/*.py; four tests; prerequisites/configuration listed in the manifest below | Current repository evidence. Existing source retained by the user; not proof of a completed GREEN. |
| Installed plugin 0.15.0 commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning, prompt-driven-development, requirements-analysis, security, testing and python-fastapi SKILL.md | Applied process and domain guidance; mandatory disposable dry run, exact code and separate human approval. |

## Current state, RED evidence and completed predecessor

Current HEAD is 546df09; its title is not milestone evidence. Plan execution status still correctly records Voice Enrollment GREEN Pending. The current branch is codex/foundation-harness; Plan.md and 014 contain pre-existing execution bookkeeping edits. Preserve all existing work. The user explicitly chose to review and retain the current production changes, which are inputs to this proposal.

012 supplies valid predecessor RED: two 40-case runs fail only at intentionally absent approved enrollment modules after real decoder/native/SQL/Auth/Consent prerequisites; 57 regressions pass before and after. Historical 010/011 and 013 failures do not replace that evidence. Completed 014 corrects only the test transport, preserving every original assertion and adding the same-origin assertion. The current inventory remains six acoustic cases, 34 HTTP enrollment cases and 57 regressions: **97**. The test file's current raw SHA256 is recorded below, including the CRLF representation captured after 014.

The retained source already contains real acoustic screening, owner-model admission, durable profiles/history/provenance, ordered configured pagination, minimal conditioning and live consent gates. At initial capture, Artifact routes used /api/v1 but its generated link used /artifacts and pointed outside the actual route under standard URL semantics. A later external working URL-only edit is recorded with the final observed hash below; it does not change the proposed full replacement. request.form() uses the installed parser's default spooled file storage before active owner consent is checked. Admission currently saves metadata and bytes in separate transactions. Its shared sample lookup converts every NOT_FOUND to ARTIFACT_UNAVAILABLE, including public preview lookup. The exact two-file correction below completes these existing contract obligations; no test/contract/default/route alias is changed.

## Carried-forward decisions and complete retained-source review

Keep 001's CPython 3.13.17, FastAPI 0.162.0, Uvicorn 0.54.0, python-multipart 0.0.32, pytest 9.1.1, HTTPX 0.28.1, Psycopg 3.3.6/PostgreSQL 18.6, NumPy 2.5.4/PyAV 19.0.2, existing Compose/CI/isolation and local filesystem boundary. Keep 004's command-only -p no:anyio, 005/006's separate owner databases/credentials/roots and existing transactions, 007/008's canonical account/Consent boundary, 009's actual webrtcvad-wheels 2.0.14.post1 identity and current committed platform hash correction, and 010–014's exact tests/interfaces. No dependency, version, setting or package acquisition occurs.

| Retained component | Review / milestone scope |
| --- | --- |
| voices/quality.py | Actual selected-stream decode, planar original PCM, per-channel 16kHz resampling and real 20ms native VAD; duration/clip/silence/noise/level/speech aggregation, unknowns, six-place rounding and policy validation retained. Six independent analytic tests exercise these outcomes; no supplied final findings. |
| _enrollment.py | Canonical verified principals/model references, exact roles/closed query fields, explicit pagination mapping, principal/filter-bound frozen pages and unpredictable tokens retained. No fixture model or page default. |
| voices/application.py and voices/persistence.py | Required collaborators, durable private state/history/provenance, obsolete unfinished reassessment and current/repeat override behavior, live owner/Consent gates and configured model/profile listing retained. Actual /api/v1 routes already correct: no redundant route delta. Existing owner-local update_payload remains. |
| ai/enrollment.py | Owner/Consent checks, independent selected-model bounds, model-required material list, actual condition callback arguments and own transaction/byte store retained. No production model or final quality result mocked in source. |
| _http.py; Auth/Consent and all other owner persistence | Existing approved status mapping, canonical token identity, consent validation, scoped live grants/fences and credential separation retained byte-exact. |
| artifacts/application.py; artifacts/persistence.py | Correct only the four concrete admission/publication/lookup/link defects identified above with the exact files below. |

## Scope and ordered proposed changes

Create/delete no production, test or configuration files. Modify exactly:

1. voice_narration/artifacts/application.py — replace the file with the complete final content below. MemoryUploadParser substitutes io.BytesIO for file parts, closes parser buffers on every error through the pinned parser lifecycle, keeps the framework scalar-part bound, enforces the configured file-byte bound during parsing, and preserves arbitrary part order and the four closed required parts. Verified authentication precedes parsing; active consent/model checks precede decode/domain use and publication. Public unknown Artifact lookup preserves NOT_FOUND; only internal unavailable enrollment references map to ARTIFACT_UNAVAILABLE. Call owned publish_sample and return the correct /api/v1 content URL. Existing routes, schemas, formats, original bytes and errors remain otherwise unchanged.
2. voice_narration/artifacts/persistence.py — replace the file with the complete final content below. Add only publish_sample(record,data,*,validate), wrapping existing save/store_bytes in the owner transaction with live validation before publication and before commit. On failure remove only the directory for a resource this call successfully created; a duplicate save cannot delete an existing resource. Existing schema/save/read/byte interfaces remain intact.
3. Preserve every other source, all corrected tests, dependency/configuration/build files and prior artifacts byte-exact. After separately approved execution and successful verification, only this artifact's status/evidence and the corresponding Plan execution row/evidence are PDD bookkeeping exceptions.

These are GREEN corrections of existing approved FR-010–013/Q11/Q12 and common Artifact/consent obligations, not a new product decision or a Final Review change. No full service composition, scheduler, frontend, provider selection or future generation behavior is introduced.

## Technical choices and limitations for review

The installed Starlette parser source uses SpooledTemporaryFile by default and parse() closes registered buffers on BaseException. The subclass uses actual io.BytesIO registered in that lifecycle; it does not create or monkeypatch a spool. It preserves the existing scalar max_part_size rather than introducing an operator setting or unlimited scalar input. Successful parsing closes FormData in finally. BytesIO operations may run through the installed UploadFile threadpool path; no event-loop synchronous disk work is added.

publish_sample uses nested Psycopg transactions under the existing owner-local advisory transaction lock, retaining the existing fsync/os.replace file write. SQL metadata and byte index have one commit outcome; ordinary failures compensate only this call's new directory. This is not a power-failure atomic SQL/filesystem transaction: a process crash can leave unreferenced private bytes, never published through an active metadata/index record. Cleanup failure propagates and cannot produce a successful upload. No exactly-once external conditioning guarantee is added; existing AI material transactions have the same filesystem crash limitation. Later orchestration/security/recovery work remains separately owned.

Process-local cursor/link credentials remain restart-invalidated; clients obtain a new link/page. Persisted profiles/history/provenance survive reopen. The 97-case gate is meaningful deterministic/local boundary evidence, not exhaustive failure-interleaving, deployed security, human Hindi/English calibration, commercial clearance or real model inference evidence. No claim of such enablement follows.

## Initial planning snapshot and final observed working baseline

The initial planning manifest below covers 40 source/test/prerequisite files. The final observed external baseline delta is recorded in the dry-run section. The two proposed Artifact files are the only permitted executable changes; 38 others must remain byte-identical. Capture fresh bytes at actual execution; if source has changed materially from this review baseline, stop and report rather than overwrite it.

| File | SHA256 |
| --- | --- |
| .dockerignore | 37549f9cb3356952d07214273ed5e2fd98fe43faec132dd2b23039af640adf28 |
| .github/workflows/harness.yml | 532648b73020192444e61eb414f10affa16b7472abf0f365171185ab2bba79f0 |
| compose.harness.yaml | fac0c98fc3ef7e955cf3e52caf0f6ff62b3df561851f32fde410d61629172699 |
| containers/harness.Dockerfile | 06724a16480bd9f4ae2b9ad54d8bb95029843fb92439d31d81dd06f71687a38a |
| pytest.ini | 8ddeb7c45d2ab502c036d3c69ebfd45e82e79b796ac75b7c94af713956345bd7 |
| requirements-dev.txt | 47749870bd64d5c8399c02460eac6c0b81195ff8b16083054b24441a6da0a4aa |
| requirements-evaluator.txt | 612d628b604d266160cb19cf3de077123df5210dc46ed0593aab00409512ef56 |
| tests/test_authentication_consent.py | 2753e2dcedc5e585bb243fc467b56fd11fd7909b7f76b51c5d822468ca8c94ba |
| tests/test_enrollment_quality.py | 2ef07c8eb2f5a4af22c4ed95192a1a63244f3089688a9d561b8acff2825010b1 |
| tests/test_persistence.py | 47acbe6332947a21b693d77145eae0a6e69fb5fc26775fe62a80f1dbfb5d0a20 |
| tests/test_voice_enrollment.py | 3fd25eebb6d90cbfe43e17a5d749af060543b7fd9243f19b245cc1b511001db7 |
| tools/evaluator_readiness.py | 08304bb62000defb653a6194d29fbff93b1cb986e9e4931ff03873afb93803c7 |
| tools/readiness.py | 249c3fbbb769578c63e70124d873a746527749da67fb1e487059bac95e85dedf |
| voice_narration/__init__.py | 228ccac3cc279f36bab313c47fa528b60f654ad8c338373e304862537fbad402 |
| voice_narration/_enrollment.py | aef31c9b0b3cece39fa703be3fa79ca036dde837d935de0811d6e1baf4541885 |
| voice_narration/_http.py | bf50672f5d2a7625882e013f22c98513d369e90732a0d53b4446d0e7332bd252 |
| voice_narration/_sql.py | a1c0436967508a56cb0ee8e68b4e0618e4beb4f6d0a33b192e82a795c2f6f7ac |
| voice_narration/ai/__init__.py | a5405078859bb3c31c35af431055de99392d3c6e18d8b572a349aa5a2ae2f94b |
| voice_narration/ai/enrollment.py | b3790e2e8515ddf6392614d8d3961db5d187462347cc6c0632ca3fb3c646dc90 |
| voice_narration/ai/persistence.py | d35617c38c237a793eeeb2efb509b37ee00157cd094304e7c85d4cf52aab9f7d |
| voice_narration/artifacts/__init__.py | e08de26e4e2d1c822ce358c2e36db380a90581e328e8c7d1656bf7cd718661b2 |
| voice_narration/artifacts/application.py | 490390b2b8967ea8b0d73f85110a838f212826b3207284cea80e26f891e15032 |
| voice_narration/artifacts/persistence.py | 42cffa83fca36acfa9883267d581ae6ecb0c5f7d81c18cc74b66d126fbd303b2 |
| voice_narration/audit/__init__.py | ddd47817b3bc7efb57b4769a5b5218f304a2444519e44d4b7adb25ab7fc1560b |
| voice_narration/audit/persistence.py | b8f2149fcbd5fef4d2a6fb58c86946d9bd74f07287ade872dbb2e843035a38c7 |
| voice_narration/auth/__init__.py | 05e38574f2fff4330aacd072c2367dbba611ab5a407b7dc2e559b19301024cce |
| voice_narration/auth/accounts.py | 5dbd8fec4104a7bf71c8375085b9c3059d70aeae8292dad48d8ecb9dfb86a3a5 |
| voice_narration/auth/application.py | 44438e6db640073f0ae9b07a009a0db7c68d3a443b6196f15a1997d9b08f09d4 |
| voice_narration/auth/persistence.py | 6fccb75784400bd3142e46999bd326d88a125584d1fc7743bf5e014574b02789 |
| voice_narration/consent/__init__.py | 33028d1c8feb70537e86aa20a4987d69e1f849eb7610373fe140b4297d46e95f |
| voice_narration/consent/application.py | 754e3b6008c3e28faeff64c30d7fd52b8118b146511f8b51b3aa0db5fd22f000 |
| voice_narration/consent/persistence.py | ba29e912a91d8759cf798db2ead56075fac564768dff71f5376004f407e81034 |
| voice_narration/jobs/__init__.py | 5364300b0c8943f7d3f0d38aabba69fc17126ffbf033d3f2d55df25dd975f7cd |
| voice_narration/jobs/persistence.py | 47e7097c63ab31b0a16b3ed424df1cdb1f4af2f1c41d925924ff46d02d9c6ae6 |
| voice_narration/policy/__init__.py | cd2ef341b82381e068f541528ccd78a51fa9025db9c387ba326576aa0ee2f778 |
| voice_narration/policy/persistence.py | e28f5f9ebcfdea76414df62b8ebd76694d1cc51948b00ca6ecd25491aaf8d8af |
| voice_narration/voices/__init__.py | d3c434dc3016c501bdfd549db6c756a5e8a3a048bcbf1a882b222ef1f0b39521 |
| voice_narration/voices/application.py | db628224427e18c95fc167ff63b183d7389c876d8e41cbd71acba2beac323678 |
| voice_narration/voices/persistence.py | b69f0512890ebb03f8829ad0318de086f62ae5d6838a58acb8a135aed55935ad |
| voice_narration/voices/quality.py | 208c4014a27095e306f699c2d261efd827851a9b2324133162ebf45fe5b29a81 |

## Exact proposed final content

Write only the two complete files below after human approval. Full content avoids newline-sensitive patch contexts; no gaps or pseudocode are used.

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

## Acceptance / Completion Criteria

- Only the two exact reviewed Artifact files change, plus this milestone's PDD execution bookkeeping. All four test files, 97 case identities and all other captured source/configuration bytes remain unchanged.
- All 40 feature cases and all 57 preserved cases pass together twice, without manual cleanup between invocations: no errors/failures/skips/xfails. Actual decoder/resampler/native VAD, real loopback HTTP, isolated owner SQL/credentials/roots and effective settings assertions remain in force.
- Existing approved behavior is demonstrated: all six findings; original bytes and selected stream; closed model-aware upload admission and configured/model bounds; owner/Consent fences; readiness/evaluator failure denial; current/repeat/stale overrides and reassessment; durable profile metadata/history/provenance; configured ordered stable pagination; independent selected-model minimal materials. No final-finding mock or private callback introspection substitutes for behavior.
- Exact code review establishes no pre-consent filesystem spool, one owner-local publication transaction with guarded compensation, context-specific public404/internal409, and a real /api/v1 playback endpoint. The unchanged tests exercise admission/publication success and internal unavailable references; they do not exhaustively inject crashes or every storage-failure interleaving. Do not claim those untested guarantees.
- Both test invocations complete owned fixture teardown; all resources/processes started by verification are stopped, and exact observed project container/network/volume checks are empty. User Docker engine/Desktop and pre-existing projects remain untouched and running.
- No production model, calibration acceptance or license/enablement result is claimed. GREEN completion evidence can only be recorded after human-approved working-tree execution, not this disposable planning run.

## Exact temporary verification helper

After approval, create a new task-specific directory under the existing writable visualization root and place the following complete helper there as verify.py. It is temporary execution evidence tooling, not a permanent project file or new product test. Capture mode saves all current file hashes and original two files; check mode verifies all unaffected raw bytes and both complete reviewed files, allowing only platform newline representation.

```python
from pathlib import Path
import hashlib
import json
import sys

root = Path.cwd()
evidence = Path(sys.argv[1])
changed = {'voice_narration/artifacts/application.py': '1533804ef7b801e09c1a092391e63c143efaadfba9cd987c0fda554b210c7f28', 'voice_narration/artifacts/persistence.py': 'b3eaa9c67b25da87520cebe67b97ac5d1488e6620c7241a8b784a15410404f59'}
fixed = ('compose.harness.yaml', 'pytest.ini', 'requirements-dev.txt', 'requirements-evaluator.txt',
         '.dockerignore', '.github/workflows/harness.yml')
if len(sys.argv) > 2 and sys.argv[2] == '--capture':
    evidence.mkdir(parents=True, exist_ok=False)
    paths = [p for folder in ('voice_narration', 'tests', 'containers', 'tools')
             for p in root.joinpath(folder).rglob('*')
             if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    paths += [root / name for name in fixed]
    manifest = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    evidence.joinpath('manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    for name in changed:
        evidence.joinpath(name.replace('/', '_') + '.before').write_bytes(root.joinpath(name).read_bytes())
    print(f'Captured {len(manifest)} source/test/configuration files and two original Artifact files')
else:
    manifest = json.loads(evidence.joinpath('manifest.json').read_text(encoding='utf-8'))
    for name, digest in manifest.items():
        if name not in changed:
            assert hashlib.sha256(root.joinpath(name).read_bytes()).hexdigest() == digest, name
    for name, digest in changed.items():
        text = root.joinpath(name).read_text(encoding='utf-8')
        assert hashlib.sha256(text.encode()).hexdigest() == digest, name
        print(name, 'raw SHA256', hashlib.sha256(root.joinpath(name).read_bytes()).hexdigest())
    print(f'PASS: exact two proposed files (LF-normalized full content); {len(manifest)-2} other files byte-identical')
```

## Exact execution and verification commands

Run from the actual workspace only after approval. Establish git status/HEAD and authority/predecessor status first. Create one temporary directory, write the helper block above there, and define these variables:

```powershell
$taskRoot = 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46'
$taskRun = Join-Path $taskRoot ('015-execution-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $taskRun | Out-Null
$verificationFile = Join-Path $taskRun 'verify.py'
$evidenceDirectory = Join-Path $taskRun 'evidence'
```

Check every command's exit status before the next dependent action. No baseline full-feature run is needed: current unfinished enrollment behavior is this GREEN's subject, not a waived pre-existing failure. Preserve 014's actual baseline/post regression evidence. Capture before applying the two exact source blocks:

```powershell
git status --short
git rev-parse HEAD
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory --capture
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath (Join-Path $taskRun 'collection-before.txt')
```

Apply only the two exact complete source blocks, then run:

```powershell
.\.venv\Scripts\python.exe -m compileall -q voice_narration
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath (Join-Path $taskRun 'collection-after.txt')
$beforeIds = @(Get-Content (Join-Path $taskRun 'collection-before.txt') | Where-Object { $_ -like 'tests/*::*' })
$afterIds = @(Get-Content (Join-Path $taskRun 'collection-after.txt') | Where-Object { $_ -like 'tests/*::*' })
if ($beforeIds.Count -ne 97 -or $afterIds.Count -ne 97 -or @(Compare-Object $beforeIds $afterIds).Count) { throw 'Test inventory changed' }
git diff --check
git status --short
```

Record real output/exit codes, 97 individual outcomes, both elapsed times, exact file hashes, observed fixture-owned project IDs and cleanup. For each exact project recorded from pytest output, use bounded read-only docker ps -a, docker network ls and docker volume ls filtered by its com.docker.compose.project label; no results may remain. Do not infer ownership from a shared vnred prefix. Verify no started HTTP/pytest process remains. Remove only the resolved contained task directory after trimmed actual evidence is recorded in this artifact/Plan. No global cleanup/reset/prune.

## Expected / Predicted — Not Yet Verified milestone evidence

Expected: compile/helper success, 97 case identities unchanged, **97 passed on each full run**, no errors/skips/xfails, two exact source files and 38 other raw hashes preserved, complete owned teardown and empty exact-project checks. These are predictions for approved execution. Planning results below never substitute for milestone evidence.

## Pre-authorized Contingencies

Observable Docker named-pipe permission denial from the actual command or a read-only docker info --format '{{.ServerVersion}}' diagnostic, or loopback bind permission denial, permits only the identical intended verification invocation in normal host context under normal approval review. File/dependency/criteria changes: none. Existing fixtures may create/remove only their own fresh random project resources; never start/stop/restart Docker engine/Desktop, alter contexts/settings or touch other sessions' projects. Record actual trigger and application. Any other runtime failure stops approved execution and returns to planning; no blind retry or assertion relaxation.

## Rollback and recovery

Capture the two original files before application. If rollback is directed, restore only those captured bytes when their current hashes still match this milestone's recorded resulting hashes; preserve intervening external edits instead of overwriting them. No repository-wide reset/checkout/clean, migration, user-data deletion or dependency rollback is authorized. A failed upload is not a published available sample. Do not delete user data to recover verification. Preserve failure evidence and report inaccessible leftovers rather than claiming cleanup.

## Canonical identity / ownership comparisons and risk limits

Auth user_id, consent_id, model_id, artifact/profile IDs, record.owner_id and explicit administrator owner filters use the same canonical lowercase UUID checks as delivered authentication; versions remain exact nonblank strings, roles exact User/Administrator enums. Live granted Administrator read access requires canonical owner match and exact samples:read/profiles:read scope before the trusted service constructs owner-context consent validation. Public input never chooses an arbitrary authenticated actor. Conditioning/profile mutations remain owner-only; worker owner context comes from the trusted persisted record. Signature binding uses canonical principal/role and exact artifact/format/disposition/expiry; every retrieval rechecks current auth/Consent/expiry. SQL values remain parameterized; repositories receive only their owner credentials. Generated UUID filesystem paths retain existing containment/symlink checks. No private sample bytes, filenames, transcripts or conditioning materials are logged.

The frozen97-case local gate is not deployed multi-service authorization or a load/SLO claim. Local serialization and own SQL transactions do not claim distributed exactly-once external effects. Human calibration/corpus/reviewer acceptance and real model software/weights/output-use clearance remain separate later gates. No new public/default configuration, retention or compliance regime is introduced.

## Explicit exclusions and per-file exactness

Exclude tests/assertion edits, package/dependency/runtime/build/configuration changes, model/audio acquisition, private voices/listener outreach, human calibration, training, production enablement/commercial approval, future Jobs/Worker/frontend/full-service transport, private catalog introspection, fixture-specific IDs/bounds, commits/push/publication and self-approval.

- artifacts/application.py: complete final content, no pseudocode/placeholders/gaps; every change appears in Proposed Changes and existing consent/admission/Link/common error rules. Imports are existing pinned libraries plus io stdlib. Existing explicit settings are preserved; none introduced.
- artifacts/persistence.py: complete final content, no pseudocode/placeholders/gaps; only owned publication method is added, no schema/dependency/default. Existing owner transaction/save/byte paths and safety rules are retained.
- Temporary verify.py: complete self-contained capture/check code, stdlib only; not a permanent scope addition. It verifies exact full content and unaffected files rather than importing/faking product behavior.

015 is the next unused artifact number, not a reused requirement identifier. This is a revised GREEN proposal after completed014, not a new Plan requirement or rewrite of 013 history.

## Planning-time dry run — not milestone evidence

The disposable copy was `C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-enrollment-planning-90d0911585374924b6af228f659276a0`. It contained selected source/tests/containers/tools/configuration, initial source snapshots/hash manifest, helper/preparation scripts, collection/output evidence, bytecode and pytest cache. No .git/.venv/secrets/model/private voice was copied; the existing interpreter was reused with scratch CWD. Only the proposed two Artifact files were written inside the disposable copy, never the working source/tests. The proposed source stayed frozen throughout both full runs.

### Actual commands and trimmed real output

From scratch CWD, preparation/compile and the read-only environment trigger were:

```powershell
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' prepare.py
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' -m compileall -q voice_narration
docker info --format '{{.ServerVersion}}'
```

Preparation captured40 source/test/configuration files and original two Artifact bytes before applying the proposed full contents; compile exited0. Restricted Docker diagnostic exited1 with `permission denied while trying to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`. Normal host-context execution was reviewed/approved; no engine/Desktop lifecycle, context/settings change or environment workaround was used.

The following exact command ran twice in normal host context from the same scratch CWD, with no manual cleanup, source edit or criterion change between runs:

```powershell
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA
```

Actual first run: exit0, **97 passed in528.77s** (session14649). Actual repeat: exit0, **97 passed in559.11s** (session68044). Each output contains97 individual PASSED entries matching the captured97 node IDs in identical order: six acoustic cases,34 enrollment HTTP cases,33 persistence cases and24 Auth/Consent cases. No failure/error/skip/xfail or teardown exception occurred. Actual decoder/native VAD and HTTP/SQL fixtures ran; no final-finding stub or production-model claim.

Collection and helper commands were:

```powershell
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath collection.txt
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' verify.py evidence
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' verify.py evidence-capture-check --capture
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' -m compileall -q voice_narration
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' verify.py evidence
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' verify.py evidence
& 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe' -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath collection-after.txt
```

Initial copied-source preparation supplied the original-byte manifest/evidence. The helper capture mode was separately exercised against the frozen proposed copy; that capture-mode functional check is not misrepresented as the original pre-application snapshot. Compile/helper commands exited0. The helper verified the complete two proposed files (LF-normalized content) and all38 unaffected raw hashes before the repeat and after it; one intermediate freeze check was also recorded after the first passing run. Actual proposed raw source hashes: application.py `1533804ef7b801e09c1a092391e63c143efaadfba9cd987c0fda554b210c7f28`; persistence.py `b3eaa9c67b25da87520cebe67b97ac5d1488e6620c7241a8b784a15410404f59`. Collection captured97 IDs in4.73s; final collection reports97 in5.28s, and the two complete node-ID lists compare equal. The four test files, including014's128 assertions, remained byte-exact in scratch. Collection was captured during the first frozen run before the repeat; unchanged initial test bytes and individual outcomes establish identity preservation rather than a fabricated pre-application feature run.

Read-only previous-artifact export encountered a cp1252 UnicodeEncodeError, corrected by explicitly using UTF-8 stdout; this was an inspection helper correction, not a product/test failure or runtime retry. No dependency, input, test, production proposal or criterion was changed after the first run started. No expected failure is accepted as a pass.

### Observed fixture resources and cleanup

| Run | Exact fixture-owned project | Container observed in real pytest output |
| --- | --- | --- |
| 1 | vnred8e4bfd9777cf4977944b91314d005619 | da13ae8f5a4c892ec0df62843c24a38b04002c111ff53def16ca26dfa4163074 |
| 1 | vnred8c6eea4e515541d4ad0685683a8ddca2 | 63472804e353d2c5ebe6c0c170b983d33a25007e0d5bb58d0d14a3ee02af4ae4 |
| 1 | vnred53e13ac24d3341c68a8c4cf9b5444eef | 6d9d319c879da8aa604c606578361e7939d29fc94e0d1ed44d93df15b7231bb6 |
| 2 | vnred9521ecf6d1af475e82bd7c56c8cdcd6e | 5bd44fa5202c3592e84804ada7b602c914cff7318f3acee80236d6667c5b842c |
| 2 | vnred2b856752170e4676b9abe4d437499ab2 | 37ddb854a4c4cb4a3fc72c37019cfc09f9077dabdb62e31bdde78c0688a0b942 |
| 2 | vnred2e54e5b1b36d4d818b3e7170c9f8e0b8 | 70ebcf09902535b99fe267cc5c41e7aae8bf8ff64e0fe7c5cb93949a83670f47 |

For each exact captured project, bounded subprocess.run(timeout=15,capture_output=True,text=True) invoked only these read-only argument vectors (project substituted literally):

```python
['docker', 'ps', '-a', '-q', '--filter', 'label=com.docker.compose.project=' + project]
['docker', 'network', 'ls', '-q', '--filter', 'label=com.docker.compose.project=' + project]
['docker', 'volume', 'ls', '-q', '--filter', 'label=com.docker.compose.project=' + project]
```

Actual host commands were `python check_resources.py run1-final-output.txt resource-checks-run1.json` and the identical run2/output variant, using the same explicit project interpreter above and scratch CWD. All18 exact-project container/network/volume queries exited0 with empty stdout. Existing fixtures alone performed their own teardown; no manual cleanup occurred between runs and no other session's project was touched. Both pytest processes and all collection/compile/helper processes exited; no started server remains after their fixtures' verified teardown.

### Final working baseline observation

During the repeat, the working Artifact application was edited externally at the single returned-URL line. Final observed raw SHA256: `70ab73aa6a87666bfa0f31dbe40cd5f2aad4e554e3782705e719e43ac8988a59`. The exact observed delta against the initial snapshot is:

```diff
-        return {"url": "/artifacts/" + artifact_id + "/content?" + urlencode(parameters),
+        return {"url": "artifacts/" + artifact_id + "/content?" + urlencode(parameters),
```

All other 39 captured working files remain byte-identical. This task preserved that external edit. It lies within the same already-proposed Link correction; the frozen reviewed replacement still returns the valid origin-relative `/api/v1/artifacts/...` URL. No frozen copy, test, requirement or criterion changed and no extra 97-case run was needed for this baseline-only observation. The initial table is a historical planning snapshot; this observed hash/delta identifies the final working input reviewed for that full-file replacement.

### Final document/source preservation and disposable-copy removal

Final `git diff --check` exited0 with only pre-existing LF/CRLF notices for014/Plan. Status shows the pre-existing014/Plan bookkeeping, the observed external Artifact URL-only edit and this new015 artifact. This planning task created only015 in the repository; no source, tests, dependency/configuration, Plan, contract or prior artifact was edited by it.

The absolute disposable path was resolved and checked to remain strictly beneath the explicitly named visualization root, with the exact task-directory basename and matching task marker checked before removal. One PowerShell session used native Remove-Item -LiteralPath on only that exact directory with -Recurse -Force, then its matching015-current-scratch.txt marker. Both paths were verified absent. All copied source, original-byte snapshots, evidence/helper/preparation scripts, raw output/resource JSON, collection captures, bytecode and pytest cache were removed; trimmed real evidence remains in this document. No working file or other session's resource was removed. Docker was left running; no lifecycle/settings operation was performed.

These are planning-time results only. Milestone15 stays Pending and no commercial/model/human-calibration/production-enablement claim follows. Only execution after approval can complete GREEN.



## Actual stopped execution evidence

### Voice Enrollment GREEN 015 stopped execution evidence — 2026-10-27

Recorded 2026-10-28T00:56:29.586559Z. This is actual approved working-tree execution, distinct from the earlier disposable planning passes. The two exact approved Artifact files remain applied; GREEN is not complete.

Approval was recorded by the main conversation at 2026-10-27T06:19:09Z. Approved requirements/Q12 contract/Plan, valid 012 RED and completed 014 were checked before mutation. HEAD was 546df0902dd9c23da600274cfaa7391b0e9ddcce. The prior user-retained working URL edit was captured before applying the reviewed complete replacement.

Commands actually executed (temporary task path C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275; project interpreter from the workspace):

```powershell
git status --short
git rev-parse HEAD
.\.venv\Scripts\python.exe C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/extract.py
.\.venv\Scripts\python.exe C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/verify.py C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/evidence --capture
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/collection-before.txt
docker info --format '{{.ServerVersion}}'
.\.venv\Scripts\python.exe C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/extract.py --apply
.\.venv\Scripts\python.exe -m compileall -q voice_narration
.\.venv\Scripts\python.exe C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/verify.py C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/evidence
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA | Tee-Object -FilePath C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-execution-874ab42ba681440fb9edbe07eae53275/run1.txt
```

Preflight/collection/application/compile/helper exit0: captured 40 files plus two originals; 97 tests collected in 6.16s. Line-anchored fenced-block extraction applied exactly the two approved full contents. Helper proved both expected raw/LF-normalized hashes and 38 other files byte-identical. No tests, dependencies or configuration changed.

Docker contingency: the restricted read-only docker info invocation exited1 with permission denied at dockerDesktopLinuxEngine. Normal approval review permitted the identical intended pytest arguments in host context, using only the existing random-project fixture lifecycle. No engine/Desktop/context/settings operation or unrelated-project cleanup occurred. PowerShell Tee-Object captured real output; its line buffering delayed partial progress, without changing pytest arguments or criteria.

Actual first full verification: exit1/session81500, 63 passed, 34 errors in 66572.51s (18:29:32). Six acoustic cases and all 57 preserved regressions passed. All 34 enrollment cases ended as setup errors before their HTTP bodies ran, rather than feature assertions failing. Every error has the same two fixture timeout causes:

```text
34 occurrences: subprocess.TimeoutExpired: Command '['docker', 'compose', '-f', 'compose.harness.yaml', '-p', 'vnred2683bc0251114b99bd110f5c118ddbe8', 'up', '--detach', '--wait', '--wait-timeout', '120']' timed out after 180 seconds
34 occurrences: subprocess.TimeoutExpired: Command '['docker', 'compose', '-f', 'compose.harness.yaml', '-p', 'vnred2683bc0251114b99bd110f5c118ddbe8', 'down', '--volumes', '--remove-orphans']' timed out after 180 seconds
```

The PostgreSQL module fixture failed at tests/test_persistence.py:67 while running Compose up --detach --wait --wait-timeout 120, under its existing 180-second subprocess limit. Its finally block at line83 also reported a 180-second timeout for that exact project's down --volumes --remove-orphans. This is unrelated environment/setup evidence, not valid RED, not a waived pre-existing failure and not a passing GREEN. The reported 18:29:32 elapsed and observed clock discontinuity are recorded observations; they do not establish why the subprocess operations timed out. No sleep/hibernation root cause is claimed.

Execution stopped after the failed first run. The repeat 97-case verification and normal successful-path postcollection/completion steps were not run. No retry, timeout increase, dependency/source fix, criterion change or assertion weakening was performed.

Read-only stopped-path diagnostics/preservation: sandbox CIM process inspection was unavailable; a normal-reviewed host read of task log size/tail and process ID/name/start/CPU showed original children alive until final output. After the run exited, all five captured original process IDs (308760,65216,193036,417516,417872) were absent. No process was killed. A repeated preservation helper exited0 after failure: both approved source hashes still exact and 38 unaffected raw files unchanged. The stopped_probe.py helper verified 63 PASSED plus 34 ERROR identities account for the original 97-case collection, both repeated timeout causes, and all six authority snapshots unchanged before this bookkeeping.

Exact final raw source SHA256:

```text
voice_narration/artifacts/application.py 1533804ef7b801e09c1a092391e63c143efaadfba9cd987c0fda554b210c7f28
voice_narration/artifacts/persistence.py b3eaa9c67b25da87520cebe67b97ac5d1488e6620c7241a8b784a15410404f59
```

Scoped resource checks used only these exact observed project IDs, including the failed fixture project:

```text
vnred20590459bd0b4ac4b6c16199c289e637
vnred2683bc0251114b99bd110f5c118ddbe8
vnredda20254c8150487aaab49047f2b500c1
```

For each ID, stopped_probe.py ran the following bounded read-only argument vectors with timeout15s per diagnostic:

```python
['docker','ps','-a','--filter','label=com.docker.compose.project='+project,'--format','{{.ID}}']
['docker','network','ls','--filter','label=com.docker.compose.project='+project,'--format','{{.ID}}']
['docker','volume','ls','--filter','label=com.docker.compose.project='+project,'--format','{{.Name}}']
['docker','info','--format','{{.ServerVersion}}']
```

All nine exact-project checks exited0 with empty stdout/stderr; the server read exited0 and returned29.3.1. No manual resource cleanup was needed. The failed finally timeout is retained as a failure; subsequent empty checks are not relabeled successful original teardown. Other sessions' resources and user Docker remained untouched.

Durable stopped-evidence snapshot: C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-stopped-evidence-874ab42b.zip; SHA256 7c17795b4ca3be1e32802c935a88b299d20eb6073494e9bf8976cbe761afc8ee; 256330 bytes. It contains only the 40 captured source/test/configuration files, original two-file snapshots, helper/authority snapshots, before collection and actual output/diagnostics. No .git/.venv, secrets, model or audio assets are included. Actual output SHA256: 5ffc34a385571fbe87f849ce69fa7cf863441656d76b13f6972303151e032333. The archive keeps the exact evidence even after the temporary execution tree is removed.

Minimal recovery: no source, scope, criteria or timeout change is indicated by this setup failure. After human re-approval of existing 015, restart its unchanged approved verification sequence and require two fresh complete 97-case passes. Preserve this failed attempt as history; current Docker health alone does not prove the original timeout cause or successful enrollment behavior. No recovery approval, new Implementation Plan, retry or next-milestone work is performed here.

Calibration, model/runtime licensing and production enablement remain later gates. The user's calibration question did not change this execution or the milestone sequence.

Final stopped-path housekeeping: the resolved absolute temporary execution directory was verified strictly within the explicit visualization root, checked as a non-linked owned task directory, and removed with native PowerShell LiteralPath cleanup; absence confirmed. The evidence ZIP was retained and its SHA256 rechecked. Final git diff --check exited0 after removing one blank EOF introduced by this bookkeeping append (the first documentation-only check reported that whitespace); no runtime verification was retried. Final git status listed only Plan.md and015 bookkeeping. HEAD externally advanced from546df09 to6c971490ffe57ee6f76e4dee0654447eb58fbd49, titled Fix artifact link URL format for urljoin compatibility; both approved source hashes remain exact. This executor performed no commit or push. Prior approved artifact bodies/history remain intact except the current015 Human Review and Plan15 execution row plus appended stopped evidence.


### Voice Enrollment GREEN 015 re-approved verification resume

Recorded 2026-10-28T01:39:32Z; user re-approval was recorded by the main conversation at 2026-10-28T01:10:47Z (2026-10-27 America/Chicago). This is actual working-tree verification, distinct from disposable planning and the earlier stopped 63-pass/34-setup-error attempt. That stopped history remains unchanged. No earlier failure is relabeled a pass.

The approved two Artifact files were already applied and exactly matched both reviewed full contents before this resume. The idempotent application check therefore wrote no production file. Initial and final HEAD were ec96b15b9e2014ec3229cd5778f55d747262c0b4. All 40 source/test/configuration hashes matched the fresh capture before bookkeeping; in particular the 38 unaffected files and all four tests remained byte-identical. No executable source, test, dependency, configuration, timeout, scope or acceptance criterion changed during resumption. The untracked MILESTONE_012_REVIEW.md, step1_before.txt and step2_red1.txt are external work and were left untouched. This executor made no commit or push.

#### Actual commands and real outcomes

Workspace CWD was C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration. The temporary directory was C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344. Approved source/helper blocks were extracted with line-anchored fences; six authority snapshots and two original Artifact files were captured before verification. Commands below show the actual executable arguments; PowerShell checked LASTEXITCODE before dependent actions and returned that exit code to the tool. The before-collection and restricted Docker diagnostic were independent preflight calls. The three-project run1 resource check was read-only while run2 ran; no manual cleanup occurred between runs.

```powershell
git status --short
git log -2 --oneline
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/extract.py'
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/verify.py' 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/evidence' --capture
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/collection-before.txt'
docker info --format '{{.ServerVersion}}'
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/extract.py' --apply
.\.venv\Scripts\python.exe -m compileall -q voice_narration
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/verify.py' 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/evidence'
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA | Tee-Object -FilePath 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/run1.txt'
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/postprobe.py' run1.txt
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA | Tee-Object -FilePath 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/run2.txt'
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/postprobe.py' run1.txt --resources
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/verify.py' 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/evidence'
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object -FilePath 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/collection-after.txt'
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/postprobe.py' run2.txt --resources
docker info --format '{{.ServerVersion}}'
git diff --check
git status --short
git rev-parse HEAD
.\.venv\Scripts\python.exe 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/015-resume-d78835bdb7424e9cbde41d3afc925344/prepare_record.py'
```

Preflight extraction/capture/compile/helper exited0: captured40 files, both exact files already applied,38 review-baseline hashes match. Before collection exited0 with97 tests in6.38s. The restricted Docker diagnostic exited1 with permission denied at npipe:////./pipe/dockerDesktopLinuxEngine. This exact observed trigger activated the approved host-context contingency through normal approval review. Both intended pytest invocations retained identical arguments. No Docker Desktop/engine/context/settings operation, environment workaround or unrelated-resource action occurred.

Actual first fresh run: exit0, **97 passed in 743.72s (0:12:23)**, tool session47495. Actual second fresh run: exit0, **97 passed in 623.70s (0:10:23)**, tool session33620. Each run has97 individual PASSED entries matching the original97 collection identities in identical order: six acoustic,34 enrollment HTTP,33 persistence and24 Auth/Consent. No failure/error/skip/xfail or teardown exception. No source edit or manual cleanup between invocations. Actual decoder/resampler/native VAD, real loopback HTTP and isolated SQL/owner fixtures executed; no final-finding stub or production-model claim.

The final approved helper exited0 with both exact full-file normalized hashes and38 unaffected raw hashes preserved. Postcollection exited0 with97 tests in1.42s. The approved PowerShell Get-Content/filter/Compare-Object check and an ordered joined-list comparison both passed: same97 IDs and order. The raw original test bytes remain unchanged; no assertions were removed or weakened. git diff --check exited0, with only an informational LF/CRLF notice for015; status showed015 bookkeeping plus the three external untracked files. git log -2 --oneline established the initial HEAD; final git rev-parse HEAD confirmed the same full object.

Exact final source SHA256:

```text
voice_narration/artifacts/application.py 1533804ef7b801e09c1a092391e63c143efaadfba9cd987c0fda554b210c7f28
voice_narration/artifacts/persistence.py b3eaa9c67b25da87520cebe67b97ac5d1488e6620c7241a8b784a15410404f59
```

#### Scoped runtime cleanup and evidence integrity

| Fresh run | Exact observed fixture project | Container |
| --- | --- | --- |
| 1 | vnred6415350bc53e4cb7a752fc02b7522c19 | 68d62047af4521822dde04aa639679c81e61b7221014da4deb7f935a9c9a49ea |
| 1 | vnredea3e11f0d4284f41a492a427e5afb357 | f189f64e3b99e85d49c2e28bb90f1d666e545a7b5c65f69742a28a999cf8b1e6 |
| 1 | vnred8cfb9596aaf64a59a2fbd007c78ab470 | 879e96bab1eea6df70eeb4baf8ff5f8611624dfcd16328f04fb51eb63bc12270 |
| 2 | vnred2e5c085e9d674340ac9d7e6c362a8a9e | 64688c468578cb315ed05ae66ff9fb11942197dde738d98d5264a8cde488c1dd |
| 2 | vnrede180f0052cb64f12b30895eeb8d50172 | ea0cfc9946bcaabb8b28627290fa15409001b6cfae2c149c46aee8d69651699f |
| 2 | vnredde873c8db1cd47cc86cd526d8589b426 | 3c5fe182a5fac9735cf8c3110ef30ae85b2acb7f393443d9b1243d976e4b8713 |

For each literal project above, postprobe.py used subprocess.run(capture_output=True,text=True,timeout=15) with only these read-only argument vectors:

```python
['docker','ps','-a','--filter','label=com.docker.compose.project='+project,'--format','{{.ID}}']
['docker','network','ls','--filter','label=com.docker.compose.project='+project,'--format','{{.ID}}']
['docker','volume','ls','--filter','label=com.docker.compose.project='+project,'--format','{{.Name}}']
```

All18 exact-project queries exited0 with empty stdout; no container/network/volume remained for these six projects. The existing fixtures alone performed teardown, including their connections/HTTP servers/owned databases/roles/roots. Both pytest/tool wrapper invocations exited0, as did collection/compile/helper/resource commands; no executor-started background service remains. Other sessions' Python processes/projects were not stopped. Final read-only Docker server query exited0 and printed29.3.1; the user's engine remained running.

Read-only diagnostic/helper corrections: quiet PowerShell Tee output was line-buffered, so no invocation or timeout was changed. A log-size Get-Item probe reported not-found before the first captured line/file existed. An initial timestamp-filtered Get-Process query omitted current workers; a corrected read-only python* ID/name/start/CPU listing showed active workers (~423s/~386s CPU). No command lines/secrets were read and no process was killed. Temporary postprobe.py initially matched zero PASSED lines because its regular expression did not consume captured CRLF endings; inspection proved the97 lines existed, then only that read-only parser normalized line endings and passed. These are diagnostic/export corrections, not test failures, retries or source/criterion changes. The two actual resumed test invocations both passed on their first attempt.

Before authorized bookkeeping, all six captured authority documents were byte-identical. Only the single015 Human Review status and Plan15 execution row are replaced, plus this appended actual evidence; previous bodies and the earlier stopped history are preserved byte-for-byte. Requirements, contract,012 and014 remain unchanged. Model/human-calibration/commercial-clearance and user-enablement gates are not completed here; no model training or voice collection occurred. No next milestone is started.

Durable resume evidence: C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\015-resume-evidence-d78835bd.zip; SHA256 e62d60fd832393a349d4126db71eddb9f6ca39851c953796ff004765a1b34fc1; 258330 bytes. The archive contains captured40 source/test/configuration bytes, two originals, six authority snapshots, exact helper/extractor and read-only output/resource consolidation scripts, both full outputs/collections and their JSON receipts. No .git/.venv, secrets, model or audio assets were included. Raw run1 output SHA256 e65d9e317c29032f48397e2eedfafdac001bff6972a90194927632010131ff32; raw run2 output SHA256 89f748eb2432893abd9f4b34ff7d012d05632d11b88e9c5ee37eed9c33841c8a. The previous stopped-evidence ZIP remains untouched. Temporary-tree deletion follows this record and is confirmed by the final housekeeping receipt.

Final resume housekeeping: the exact owned temporary directory was resolved, verified strictly inside the explicit visualization root with its basename/non-link/owner-marker checks, removed using native PowerShell LiteralPath cleanup, and confirmed absent. The durable resume ZIP remains and its SHA256 was rechecked. The post-bookkeeping git diff check exited0 (informational LF/CRLF notices only); status showed only Plan/015 bookkeeping and the three retained external untracked files. Both verification processes and all owned runtime resources had already exited/cleared. No other session's resource or user file was removed.
