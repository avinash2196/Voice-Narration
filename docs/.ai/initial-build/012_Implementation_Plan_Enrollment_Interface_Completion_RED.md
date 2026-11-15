# Implementation Plan — Enrollment Interface Completion RED

## Milestone

initial-build milestone 13, Enrollment Interface Completion RED; type RED. The approved 29-stage Plan records it Pending and predecessor 12 Complete. This proposes test changes only. Historical 010/011 remain unchanged.

## Authoritative References

Work-item references are under docs/.ai/initial-build. Approval records are authority, not newly executed evidence.

| Read reference | Authority / disposition |
| --- | --- |
| requirements.md | Q12 approved 2026-10-26T17:12:20Z; FR-010/012/013, AC-ENR-001 and Q12 apply. |
| Plan.md | Q12 revision approved 2026-10-26T17:19:00Z; milestone 12 Complete, 13 Pending. |
| contract/API-Contract.md | Q12 amendment approved 2026-10-26T17:39:41Z; required multipart Model, List, enrollment, ownership and common rules govern. |
| Enrollment-Interface-Completion-Proposal.md | Approved 2026-10-26T17:10:04Z; batched A/B/C decisions. |
| Enrollment-Catalog-Seam-Correction-Proposal.md; Enrollment-Quality-Policy-Proposal.md | Approved historical seam correction and Q11 measurement/calibration policy. |
| 001_Implementation_Plan_Foundation.md | Approved/executed tooling and real isolated PostgreSQL/HTTP. |
| 002_Implementation_Plan_Model_Feasibility.md; model-eval/approved.md | Approved investigation-only model decision; no production clearance. |
| 003_Implementation_Plan_Persistence_RED.md; 004_Implementation_Plan_Persistence_RED_Recovery.md | Approved stopped history and completed RED recovery. |
| 005_Implementation_Plan_Persistence_GREEN.md; 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved implementation and completed verification of eighteen production files. |
| 007_Implementation_Plan_Authentication_Consent_RED.md; 008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved/executed real identity/consent boundaries and 24 tests. |
| 009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved/executed actual evaluator/codec prerequisites, no calibration claim. |
| 010_Implementation_Plan_Voice_Enrollment_RED.md | Approved/executed six acoustic/fifteen HTTP cases; retained interfaces/assertions. |
| 011_Implementation_Plan_Enrollment_Catalog_Test_Wiring_Correction.md | Approved/executed listing seam only; current target hash and 57-case passing evidence. |
| Contract-Review.md; voice_narration_PDD_requirements.md | Historical review and subordinate nonconflicting product context. |
| tests/test_voice_enrollment.py; tests/test_enrollment_quality.py; tests/test_persistence.py; tests/test_authentication_consent.py; voice_narration/**/*.py; tools/evaluator_readiness.py; requirements-dev.txt; requirements-evaluator.txt; pytest.ini | Inspected repository facts, not additional product authority. |
| Installed commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md and templates/Implementation-Plan.md; skills/testing/SKILL.md; skills/security/SKILL.md; skills/python-fastapi/SKILL.md; skills/requirements-analysis/SKILL.md | Process/domain guidance under C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0. |

No workspace AGENTS.md or product-level docs/requirements.md was found. No approved unexecuted milestone-13 plan exists. No new authority identifier is introduced.

## Carried-Forward Decisions and Predecessor Evidence

001 retains pinned project Python/pytest/HTTPX/PostgreSQL and unique ports/projects/credentials/roots. 002 retains investigation-only model status. 003–006 retain owner-store fixtures and exact preservation. 007/008 retain actual authentication, canonical identities and live Consent checks. 009 retains installed decoder/resampler/native VAD. 010 retains every assertion, findings, original-byte/stream rules and worker/provenance diagnostics. 011 retains required zero-argument list_capabilities and keyed capability(model). No dependency/version/configuration/schema change.

Plan.md's completed 011 evidence records 57/57 baseline in 103.16s and postchange in 85.94s, retained collection, collaborator checks twice, exact preservation and cleanup. Current target SHA256 is 054f67b8827b18eb5d8d4202a23f16612d2c177ce66fe41380e1612e2518cd04, observed again during planning. Quality remains 2ef07c8eb2f5a4af22c4ed95192a1a63244f3089688a9d561b8acff2825010b1. Historical 010's 21 missing-symbol errors twice are history, not Q12 evidence or proof of unreached bodies. Completed 009 proved unchanged installed evaluator/codec prerequisites; broader readiness is unnecessary here.

## Current State and Complete Seam Audit

Actual Auth/Consent applications and owner persistence exist; voices.quality, artifacts.application, voices.application and ai.enrollment do not. Those intended missing symbols predict valid RED after real reached fixtures; unrelated environment failures do not. Current upload lacks Model, Voices lacks explicit pagination, and catalog listing has one record. Existing modified/untracked foundation, workflow, requirements/Plan/contract, tests, production/evaluator and prior artifacts must be preserved; no clean-tree claim.

| Flow | Complete reviewed inputs |
| --- | --- |
| Auth/Consent -> Artifact | Actual authenticate and validate_owner_consent; consent/model/file; Artifact repository/settings/clock; explicit keyed capability before admission. |
| Artifact -> Voices -> AI | Existing enrollment_samples returns authorized originals/metadata; selected profile Model rechecked at admission and conditioning; owners keep separate repositories. |
| Configuration -> lists | Existing limits.page_default/page_max mapped to required default_page_size/max_page_size; closed positive integers, default <= max. Policy snapshot remains revision/enrollment_quality. |
| Approval provider -> models | Zero-argument provider owns private persisted Approval order and returns enabled/approved public Capability; consumer preserves order/authenticated snapshot. |
| Quality/calibration/conditioning | Actual installed native quality, policy_snapshot/calibration/revision and condition(model,samples,required_materials); no mocked final findings. The synthetic private acceptance collaborator makes no real human-calibration claim. |
| Clock/storage/diagnostics | Eight existing isolated stores, explicit clock, run_pending/history/provenance/close; no callback introspection or inferred fixture model. |

## Files in Scope and Proposed Changes

Create/delete no executable file. Modify only tests/test_voice_enrollment.py by this complete diff. Leave all six acoustic cases byte-exact, both 57-case regression files, 22 production files, six 009-unaffected foundation files and 001–011 unchanged. Verified Plan.md bookkeeping is the PDD file-scope exception; no Plan edit during planning.

1. Extend synthetic TestCatalog with additional capabilities, blocked model identities and ordered public records; preserve deepcopy and MODEL_NOT_READY. Private approval times remain provider-local.
2. Supply explicit pagination to Voices and expose a test closure for invalid/nondefault mappings. Invalid mapping raises PersistenceError INVALID_CONFIGURATION before constructing an app: precise internal authoring choice for review, not a public HTTP code extension.
3. Add explicit model parts to upload helper, retain exhaustive Artifact assertions, and strengthen unauthorized-stream storage observations.
4. Add focused exact cases for malformed/unknown model parts, readiness/disposal, selected-model bounds/guidance/reuse, ordered stable catalog pagination, stable profile pagination, invalid and nondefault pagination.

## Complete Internal Interface Record

All factories are keyword-only. artifacts.application.create_app(*, repository, authenticate, validate_consent, capability, settings, clock) retains state.enrollment_samples(account,consent_id,ids), effective_settings(), close(). Upload maps model_id/model_version to Model; no public Artifact field/permanent binding.

voices.application.create_app(*, repository, authenticate, validate_consent, artifacts, enrollment, capability, list_capabilities, pagination, policy_snapshot, calibration, clock). Required pagination is the closed validated mapping above, with no default. list_capabilities() returns enabled/approved public capabilities already in persisted descending Approval-time/model_id/version order. Provider owns private Approval data. Retain state.run_pending(profile_id), transition_history(profile_id), assessment_provenance(profile_id,assessment_id), close().

ai.enrollment.create_adapter(*, repository, validate_consent, artifacts, capability, condition, clock), enroll(account,profile,samples), material_kinds(account,profile_id); condition(model,samples,required_materials) remains. quality.decode(data,format), assess(samples,*,policy,duration_bounds), validate_policy(policy) remain as 010. No public signature/field change beyond approved Q12 parts. Existing SETTINGS 10/20 and model 1..12 plus new synthetic alternatives are test inputs, not product defaults/model approvals.

## Exact Proposed Diff

```diff
--- a/tests/test_voice_enrollment.py
+++ b/tests/test_voice_enrollment.py
@@ -1,6 +1,7 @@
 """Real owner boundaries and measurements; test-only evidence, no model-quality claim."""
 from copy import deepcopy
 from decimal import Decimal
+from datetime import timedelta
 import hashlib
 import importlib
 import json
@@ -32,6 +33,9 @@
         self.policy = candidate_policy()
         self.revision = 1
         self.accepted = None
+        self.extra_caps = []
+        self.blocked_models = set()
+        self.ordered_caps = None
         self.cap = {"model": dict(MODEL), "languages": ["hi", "en"], "mixed_language": True,
                     "styles": ["neutral"], "pause_strength": None, "speech_pace": None,
                     "section_regeneration": False, "mapping": False,
@@ -50,14 +54,21 @@
 
     def capability(self, model):
         from voice_narration._sql import fail
-        if not self.model_ready or model != MODEL:
+        if not self.model_ready or (model["model_id"], model["version"]) in self.blocked_models:
             fail("MODEL_NOT_READY")
-        return deepcopy(self.cap)
+        for cap in [self.cap] + self.extra_caps:
+            if cap["model"] == model:
+                return deepcopy(cap)
+        fail("MODEL_NOT_READY")
 
     def list_capabilities(self):
         # Synthetic enabled/approved catalog records for this isolated test only.
         # This does not grant production model or calibration approval.
-        return [deepcopy(self.cap)] if self.model_ready else []
+        if not self.model_ready:
+            return []
+        # Private synthetic provider order; never expose Approval metadata.
+        source = self.ordered_caps if self.ordered_caps is not None else [self.cap]
+        return deepcopy(source)
 
     def snapshot(self):
         return {"revision": self.revision, "enrollment_quality": deepcopy(self.policy)}
@@ -113,12 +124,15 @@
                               artifacts=artifacts.state.enrollment_samples,
                               capability=catalog.capability, condition=condition,
                               clock=lambda: now[0])
-    def make_voices(repository):
+    def make_voices(repository, pagination=None):
+        if pagination is None:
+            pagination = {key: SETTINGS[key] for key in
+                          ("default_page_size", "max_page_size")}
         return voices_factory(repository=repository, authenticate=auth.state.verify_token,
                               validate_consent=consents.state.validate_owner_consent,
                               artifacts=artifacts.state.enrollment_samples, enrollment=adapter,
                               capability=catalog.capability,
-                              list_capabilities=catalog.list_capabilities,
+                              list_capabilities=catalog.list_capabilities, pagination=pagination,
                               policy_snapshot=catalog.snapshot,
                               calibration=catalog.calibration, clock=lambda: now[0])
 
@@ -137,6 +151,7 @@
                       "calls": calls, "grants": grants, "consent_repo": consent_repo,
                       "voices_repo": voices_repo, "artifact_repo": artifact_repo,
                       "ai_repo": ai_repo, "paths": paths,
+                      "make_voices": lambda pagination: make_voices(voices_repo, pagination),
                       "reopen_voices": lambda: make_voices(open_store("voices", grants.authorize))}
             token, _ = verify(system)
             system["token"] = token
@@ -148,11 +163,14 @@
         auth.state.close()
 
 
-def upload(system, data=None, fmt="wav", token=None, consent_id=None, expected=201, code=None):
+def upload(system, data=None, fmt="wav", token=None, consent_id=None, expected=201, code=None,
+           model=None):
     data = wav_bytes(np.zeros((1, 80000))) if data is None else data
+    model = dict(MODEL) if model is None else model
     mime = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
     response = system["media"].post("/artifacts/upload", headers=headers(token or system["token"]),
-                                     data={"consent_id": consent_id or system["consent_record"]["consent_id"]},
+                                     data={"consent_id": consent_id or system["consent_record"]["consent_id"],
+                                           "model_id": model["model_id"], "model_version": model["version"]},
                                      files={"file": ("SYNTHETIC_PRIVATE_FILENAME." + fmt, data, mime)})
     if expected != 201:
         error(response, expected, code)
@@ -365,7 +383,12 @@
     value, sample = warned(s)
     other, _ = verify(s, "other@example.invalid")
     other_consent = record(s, other)
+    files_before = {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()}
+    owner = principal(s["token"]["account"]["user_id"])
+    rows_before = s["artifact_repo"].list(owner, owner_id=owner["user_id"], now=NOW)
     upload(s, token=other, consent_id=s["consent_record"]["consent_id"], expected=403, code="FORBIDDEN")
+    assert s["artifact_repo"].list(owner, owner_id=owner["user_id"], now=NOW) == rows_before
+    assert {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()} == files_before
     foreign = upload(s, token=other, consent_id=other_consent["consent_id"])
     for changes, status, code in [({"sample_artifact_ids": []}, 400, "INVALID_INPUT"),
                                   ({"sample_artifact_ids": [sample["artifact_id"]] * 2}, 400, "INVALID_INPUT"),
@@ -489,3 +512,245 @@
     playback = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
     assert playback.status_code == 200 and playback.content == data
     assert independent_decode(playback.content)["stream_index"] == captured["stream_index"]
+
+
+@pytest.mark.integration
+@pytest.mark.parametrize("part", ["model_id", "model_version"])
+@pytest.mark.parametrize("defect", ["missing", "blank", "duplicate", "malformed"])
+def test_upload_model_parts_closed(enrollment_system, part, defect):
+    s = enrollment_system
+    upload(s)
+    who = principal(s["token"]["account"]["user_id"])
+    before = s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW)
+    files_before = {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()}
+    fields = {"consent_id": s["consent_record"]["consent_id"],
+              "model_id": MODEL["model_id"], "model_version": MODEL["version"]}
+    if defect == "missing":
+        del fields[part]
+    elif defect == "blank":
+        fields[part] = "  "
+    elif defect == "malformed":
+        if part == "model_id":
+            fields[part] = MODEL["model_id"].upper()
+        else:
+            del fields[part]
+    parts = [(key, (None, value)) for key, value in fields.items()]
+    if defect == "duplicate":
+        parts.append((part, (None, fields[part])))
+    if defect == "malformed" and part == "model_version":
+        parts.append((part, ("version.bin", b"test-only-v1", "application/octet-stream")))
+    parts.append(("file", ("synthetic.wav", wav_bytes(np.zeros((1, 80000))), "audio/wav")))
+    error(s["media"].post("/artifacts/upload", headers=headers(s["token"]), files=parts),
+          400, "INVALID_INPUT")
+    assert s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW) == before
+    assert {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()} == files_before
+
+
+@pytest.mark.integration
+def test_unknown_parts_and_unready_models_discard_streams(enrollment_system):
+    s = enrollment_system
+    upload(s)
+    who = principal(s["token"]["account"]["user_id"])
+    before = s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW)
+    files_before = {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()}
+    parts = [("consent_id", (None, s["consent_record"]["consent_id"])),
+             ("model_id", (None, MODEL["model_id"])), ("model_version", (None, MODEL["version"])),
+             ("extra", (None, "unknown")),
+             ("file", ("synthetic.wav", wav_bytes(np.zeros((1, 80000))), "audio/wav"))]
+    error(s["media"].post("/artifacts/upload", headers=headers(s["token"]), files=parts),
+          400, "INVALID_INPUT")
+    upload(s, model={"model_id": uid(), "version": "unknown"}, expected=503, code="MODEL_NOT_READY")
+    upload(s, model={"model_id": MODEL["model_id"], "version": "unknown"},
+           expected=503, code="MODEL_NOT_READY")
+    # Known but unapproved identity is represented by the trusted provider gate.
+    s["catalog"].blocked_models.add((MODEL["model_id"], MODEL["version"]))
+    upload(s, expected=503, code="MODEL_NOT_READY")
+    s["catalog"].blocked_models.clear()
+    s["catalog"].model_ready = False
+    upload(s, expected=503, code="MODEL_NOT_READY")
+    assert s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW) == before
+    assert {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()} == files_before
+
+
+@pytest.mark.integration
+def test_selected_model_bounds_guidance_and_independent_reuse(enrollment_system):
+    s = enrollment_system
+    catalog = s["catalog"]
+    alternate = deepcopy(catalog.cap)
+    alternate["model"] = {"model_id": uid(), "version": "test-only-alternate"}
+    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "4", "6"
+    alternate["recording_guidance"] = ["Synthetic alternate guidance: four to six seconds."]
+    catalog.extra_caps = [alternate]
+    catalog.ordered_caps = [alternate, catalog.cap]
+    listed = s["profiles"].get("/models", headers=headers(s["token"]))
+    assert listed.status_code == 200 and listed.json()["items"][0] == alternate
+    selected = listed.json()["items"][0]
+    sample = upload(s, model=selected["model"])
+    assert s["artifact_repo"].read_bytes(principal(s["token"]["account"]["user_id"]),
+                                         sample["artifact_id"], now=NOW) == [wav_bytes(np.zeros((1, 80000)))]
+    for frames in (63999, 96001):
+        upload(s, wav_bytes(np.zeros((1, frames))), model=selected["model"],
+               expected=400, code="INVALID_AUDIO")
+    for frames in (64000, 96000):
+        upload(s, wav_bytes(np.zeros((1, frames))), model=selected["model"])
+    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "0.5", "20"
+    for frames in (15999, 192001):
+        upload(s, wav_bytes(np.zeros((1, frames))), model=alternate["model"],
+               expected=400, code="INVALID_AUDIO")
+    for frames in (16000, 192000):
+        upload(s, wav_bytes(np.zeros((1, frames))), model=alternate["model"])
+    response = create_profile(s, [sample], model=dict(MODEL))
+    assert response.status_code == 202, response.text
+    pid = response.json()["profile_id"]
+    s["voices"].state.run_pending(pid)
+    value = profile(s, pid)
+    assert value["status"] == "awaiting_user_override"
+    assert override(s, value).status_code == 200
+    s["voices"].state.run_pending(pid)
+    assert profile(s, pid)["status"] == "enrolled"
+    assert s["calls"][-1]["model"] == MODEL
+    before_calls = len(s["calls"])
+    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "6", "7"
+    error(create_profile(s, [sample], model=alternate["model"]), 400, "INVALID_INPUT")
+    assert len(s["calls"]) == before_calls
+    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "4", "6"
+    pending = create_profile(s, [sample], model=alternate["model"])
+    assert pending.status_code == 202, pending.text
+    later = pending.json()["profile_id"]
+    s["voices"].state.run_pending(later)
+    warned_value = profile(s, later)
+    assert warned_value["status"] == "awaiting_user_override"
+    assert override(s, warned_value).status_code == 200
+    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "6", "7"
+    s["voices"].state.run_pending(later)
+    assert profile(s, later)["status"] == "failed"
+    assert len(s["calls"]) == before_calls
+
+
+def catalog_records(catalog, count):
+    from uuid import UUID
+    private = []
+    for index in range(count):
+        cap = deepcopy(catalog.cap)
+        cap["model"] = {"model_id": str(UUID(int=index + 1)), "version": "test-only-catalog"}
+        private.append((NOW + timedelta(seconds=(index * 7) % count), cap))
+    # Approval data stays private; consumer gets ordered public Capability only.
+    private.sort(key=lambda row: (row[0], row[1]["model"]["model_id"],
+                                  row[1]["model"]["version"]), reverse=True)
+    catalog.ordered_caps = [cap for approved_at, cap in private]
+    return deepcopy(catalog.ordered_caps)
+
+
+@pytest.mark.integration
+def test_catalog_order_limits_and_authenticated_snapshot(enrollment_system):
+    s = enrollment_system
+    expected = catalog_records(s["catalog"], 23)
+    assert expected != sorted(expected, key=lambda cap: cap["model"]["model_id"], reverse=True)
+    first = s["profiles"].get("/models", headers=headers(s["token"]))
+    assert first.status_code == 200, first.text
+    page = first.json()
+    assert page["items"] == expected[:SETTINGS["default_page_size"]] and page["next_cursor"]
+    maximum = s["profiles"].get("/models?limit=20", headers=headers(s["token"]))
+    assert maximum.status_code == 200 and maximum.json()["items"] == expected[:20]
+    error(s["profiles"].get("/models?limit=21", headers=headers(s["token"])), 400, "LIMIT_EXCEEDED")
+    error(s["profiles"].get("/models"), 401, "UNAUTHENTICATED")
+    other, _ = verify(s, "catalog-other@example.invalid")
+    query = {"cursor": page["next_cursor"]}
+    error(s["profiles"].get("/models", params=query, headers=headers(other)), 400, "INVALID_CURSOR")
+    error(s["profiles"].get("/models", params={"cursor": page["next_cursor"] + "x"},
+                             headers=headers(s["token"])), 400, "INVALID_CURSOR")
+    fresh = deepcopy(expected[0]); fresh["model"]["model_id"] = uid()
+    s["catalog"].ordered_caps.insert(0, fresh)
+    items = list(page["items"])
+    while page["next_cursor"] is not None:
+        response = s["profiles"].get("/models", params={"cursor": page["next_cursor"]},
+                                      headers=headers(s["token"]))
+        assert response.status_code == 200, response.text
+        page = response.json()
+        assert page["items"]
+        items.extend(page["items"])
+        assert len(items) <= len(expected)
+    assert items == expected
+    s["catalog"].model_ready = False
+    empty = s["profiles"].get("/models", headers=headers(s["token"]))
+    assert empty.status_code == 200 and empty.json() == {"items": [], "next_cursor": None}
+
+
+@pytest.mark.integration
+def test_profile_limits_filters_and_stable_snapshot(enrollment_system):
+    s = enrollment_system
+    sample = upload(s)
+    created = []
+    for index in range(21):
+        s["now"][0] = NOW + timedelta(seconds=index)
+        response = create_profile(s, [sample], name="Synthetic page " + str(index))
+        assert response.status_code == 202, response.text
+        created.append(response.json())
+    expected = list(reversed(created))
+    response = s["profiles"].get("/voices?language=hi&status=pending", headers=headers(s["token"]))
+    assert response.status_code == 200, response.text
+    page = response.json()
+    assert page["items"] == expected[:10] and page["next_cursor"]
+    maximum = s["profiles"].get("/voices?limit=20", headers=headers(s["token"]))
+    assert maximum.status_code == 200 and maximum.json()["items"] == expected[:20]
+    error(s["profiles"].get("/voices?limit=21", headers=headers(s["token"])), 400, "LIMIT_EXCEEDED")
+    other, _ = verify(s, "page-other@example.invalid")
+    query = {"cursor": page["next_cursor"], "language": "hi", "status": "pending"}
+    error(s["profiles"].get("/voices", params=query, headers=headers(other)), 400, "INVALID_CURSOR")
+    error(s["profiles"].get("/voices", params=dict(query, language="en"),
+                             headers=headers(s["token"])), 400, "INVALID_CURSOR")
+    s["now"][0] += timedelta(seconds=1)
+    assert create_profile(s, [sample], name="Synthetic post-snapshot").status_code == 202
+    items = list(page["items"])
+    while page["next_cursor"] is not None:
+        query["cursor"] = page["next_cursor"]
+        response = s["profiles"].get("/voices", params=query, headers=headers(s["token"]))
+        assert response.status_code == 200, response.text
+        page = response.json()
+        assert page["items"]
+        items.extend(page["items"])
+        assert len(items) <= len(expected)
+    assert items == expected
+    foreign = s["profiles"].get("/voices", headers=headers(other))
+    assert foreign.status_code == 200 and foreign.json() == {"items": [], "next_cursor": None}
+
+
+@pytest.mark.integration
+@pytest.mark.parametrize("pagination", [{}, {"default_page_size": 0, "max_page_size": 20},
+    {"default_page_size": 21, "max_page_size": 20},
+    {"default_page_size": True, "max_page_size": 20},
+    {"default_page_size": 10, "max_page_size": "20"},
+    {"default_page_size": 10, "max_page_size": 20, "extra": 1}])
+def test_pagination_configuration_fails_closed(enrollment_system, pagination):
+    s = enrollment_system
+    working = s["profiles"].get("/models", headers=headers(s["token"]))
+    assert working.status_code == 200 and working.json()["items"]
+    from voice_narration._sql import PersistenceError
+    with pytest.raises(PersistenceError) as caught:
+        s["make_voices"](pagination)
+    assert caught.value.code == "INVALID_CONFIGURATION"
+
+
+@pytest.mark.integration
+def test_nondefault_pagination_controls_both_handlers(enrollment_system):
+    s = enrollment_system
+    expected = catalog_records(s["catalog"], 5)
+    sample = upload(s)
+    created = []
+    for index in range(5):
+        s["now"][0] = NOW + timedelta(seconds=index)
+        response = create_profile(s, [sample], name="Synthetic configured " + str(index))
+        assert response.status_code == 202, response.text
+        created.append(response.json())
+    app = s["make_voices"]({"default_page_size": 2, "max_page_size": 3})
+    try:
+        with serve(app) as client:
+            for endpoint, records in (("/models", expected), ("/voices", list(reversed(created)))):
+                first = client.get(endpoint, headers=headers(s["token"]))
+                assert first.status_code == 200 and first.json()["items"] == records[:2]
+                maximum = client.get(endpoint, params={"limit": 3}, headers=headers(s["token"]))
+                assert maximum.status_code == 200 and maximum.json()["items"] == records[:3]
+                error(client.get(endpoint, params={"limit": 4}, headers=headers(s["token"])),
+                      400, "LIMIT_EXCEEDED")
+    finally:
+        app.state.close()
```

## Contract Traceability and Static Inventory

| Approved rule | Proposed evidence |
| --- | --- |
| Exactly-one required canonical Model parts; missing/blank/duplicate/wrong-type/unknown rejection | test_upload_model_parts_closed (8); test_unknown_parts_and_unready_models_discard_streams (1) |
| Unknown/version mismatch/unapproved/unavailable MODEL_NOT_READY; discarded bytes; live owner consent | Same readiness case; retained ownership test strengthened with real owner rows/files |
| Guidance before upload, selected model/config bounds and exact edges, independent reuse/admission/conditioning | test_selected_model_bounds_guidance_and_independent_reuse (1); retained exhaustive Artifact/Profile shape and accepted-format assertions |
| Configured default/max actually control both lists; no hidden values; invalid config fails closed | test_pagination_configuration_fails_closed (6); test_nondefault_pagination_controls_both_handlers (1) |
| Provider order, stable snapshots, cursor integrity/principal/filter binding, empty pages | test_catalog_order_limits_and_authenticated_snapshot (1); test_profile_limits_filters_and_stable_snapshot (1) |
| Q11 quality/readiness/live-consent/original streams/material minimization | Retained eight HTTP functions/fifteen cases and all six acoustic cases; every existing assertion retained |

Profile admission uses common inherited 400 INVALID_INPUT for model-bound constraint failure, not a new POST /voices error. Changed live bounds after accepted work assert failed/no conditioning via the existing asynchronous state contract without inventing an error code/message. Guidance comes from actual HTTP catalog before synthetic bytes/upload; this is service-flow coverage, not a browser/UI claim. Output formats remain wav-only in synthetic Capability while retained WAV/MP3/M4A uploads all succeed.

AST-derived exact proposed inventory (not actual pytest collection):

| Function | Cases |
| --- | ---: |
| test_guidance_formats_playback_admission_and_originals | 1 |
| test_warning_override_profile_reuse_and_minimal_materials | 1 |
| test_obsolete_assessment_rerecording_and_strict_override | 1 |
| test_readiness_gates_without_false_pass | 6 |
| test_ownership_reference_validation_and_live_consent_fence | 1 |
| test_all_pass_without_override_and_model_minimal_material_selection | 3 |
| test_evaluator_execution_failure_cannot_be_overridden | 1 |
| test_multistream_metadata_playback_and_conditioning | 1 |
| test_upload_model_parts_closed | 8 |
| test_unknown_parts_and_unready_models_discard_streams | 1 |
| test_selected_model_bounds_guidance_and_independent_reuse | 1 |
| test_catalog_order_limits_and_authenticated_snapshot | 1 |
| test_profile_limits_filters_and_stable_snapshot | 1 |
| test_pagination_configuration_fails_closed | 6 |
| test_nondefault_pagination_controls_both_handlers | 1 |

34 HTTP plus six unchanged acoustic = 40 predicted feature cases: 21 retained and 19 new. Actual collection must confirm identities/counts. Every new function begins with positive behavior before absence-only assertions. No new case is predicted to pass at RED. Preserved-behavior tests expected to pass within the feature RED inventory: none. The separate 57-case regression constraint must pass before/after. Private Approval-registry correctness, admin Configuration transport, full UI and real calibration/model approval remain later boundaries, not normative rules silently claimed tested here.

## Execution Steps

1. Read this artifact's single Human Review field and predecessor approval/status records; stop unless approval is recorded. Capture git status --short and a stable UTF-8 SHA256 manifest under the allowed visualization directory for all existing checkout files, excluding only exact directory components .git, .venv, .pytest_cache and __pycache__. Include untracked files, target/quality, both regression files, all 22 production files, six 009-unaffected foundation files and 001–011. Require the observed target/quality hashes above. Preserve target bytes separately for recovery. No runtime action during planning.
2. Execute the 57-case regression command once before application. Require 57 passes and successful fixture teardown. Existing fixtures create only uniquely named projects/databases/roles/ports/roots and own their teardown. Do not change user Docker state, install packages or run broader readiness. Any SQL/native/codec/HTTP/environment failure stops; it is not RED.
3. Extract the single diff fence under Exact Proposed Diff with an anchored line scanner: a line exactly ```diff starts it and a line exactly ``` ends it. Never split on arbitrary backticks. Mechanically verify old hunk lines against current source in memory, apply all hunks in memory, ast.parse the result, then write only tests/test_voice_enrollment.py as UTF-8. Compare exact resultant source/hash and preservation manifest. Use stdin or a bounded temporary helper, avoiding Windows command-length limits. Keep manifests/output in the stable visualization directory, not per-launch TEMP. Helper scripts are not repository deliverables.
4. Collect feature IDs once; require all retained IDs plus the new IDs above, 40 cases, no skip/xfail. Execute the feature command twice without manual cleanup. Inspect every first-run cause before invoking the second. An intended absent application/module/signature is valid missing behavior after valid reached prerequisites; unrelated environment/fixture failures stop for review. No fake findings/stub/evaluator substitute, runtime retry or assertion change.
5. Execute the preserved 57-case command once after application. Before/after are the two isolated passing runs without manual cleanup. Record full trimmed actual outputs, exit codes, collected IDs/counts, each RED cause and reached fixture stage, resource/connection teardown and exact preservation. Compare manifest: only target and normal verified milestone bookkeeping may differ. Record git diff --check and status. Stop before GREEN; missing modules do not prove later bodies sound.

## Verification Commands

Run separately, in this exact sequence from the repository root, after approval:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio --collect-only tests/test_enrollment_quality.py tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
git diff --check
git status --short
```

Expected / Predicted — Not Yet Verified: 57 passes before/after, actual collection 40, two missing-feature RED invocations, likely six voices.quality and 34 artifacts.application missing-symbol errors from current absent source. Actual causes/counts must come from execution. Fixture/native/SQL/environment failures, skips/xfails, weakened assertions, unexpected new passing cases or lost preservation do not meet completion. Collection is inventory, not RED evidence.

## Acceptance / Completion Criteria

- Apply exactly the approved test diff only; preserve all original assertions, six acoustic cases, 57 regressions, 22 production files, six foundation files and 001–011. Plan's own verified execution bookkeeping is the PDD exception.
- Actual retained/new IDs and counts match the inventory. Two feature invocations fail only for missing approved behavior after valid reached prerequisites; every new owned rule has valid RED evidence. Unreached bodies remain expressly unverified.
- All 57 regressions pass before and after; durable manifest/output/cleanup evidence supports exact preservation and isolation. User Docker remains untouched.
- No production/dependency/configuration/schema/calibration/model enablement/commit/push. Record only actual verified milestone evidence in Plan.md, never predicted success.

## Planning-Time Dry Run and Exact-Code Review

No runtime dry run or scratch implementation/stub probe ran: the active task explicitly forbids runtime/test/DB/Docker/package operations during planning. No pytest collection, fixture/application import or decoder/native call ran. Static-only reads, hashes, AST parsing and in-memory diff work were used. Proposed source parses; all 84 existing assert nodes remain present. The complete unified diff was regenerated mechanically from current source and the reviewed additions; no test file was written. This is syntax/applicability evidence only, not runtime soundness or milestone evidence.

Per-file result: tests/test_voice_enrollment.py has a complete diff, no pseudocode/placeholders, all changes match Proposed Changes, no dependency/plugin/configuration-file setting introduced. Required pagination traces to Q12 A and existing SETTINGS; synthetic alternate Model/bounds/2-and-3 page sizes are test-only inputs. tests/test_enrollment_quality.py has no proposed edit and retains all six tests. No template comments or new authority labels.

Planning helper deviations: a preliminary per-launch TEMP draft could not be reopened by a later launch; a subsequent oversized single command hit Windows error 206 before execution. Switched to bounded direct artifact patches. An initial static diff anchor typo failed before target write and was corrected against the actual final source line; the final diff was regenerated and AST/assertion-checked. None ran a runtime check or changed executable source. These helper outcomes are not product evidence.

## Risks

Authenticated cursor binding uses actual verified Account.user_id in canonical lowercase UUID form, not email/token text or untrusted owner_id. Artifact owner/authenticated user/Consent owner comparisons use the same delivered canonical IDs. Model identity uses canonical model_id plus exact case-sensitive version; no normalization/inference. Cross-principal tests authenticate a distinct real account. Profile cursor filters are exact; tampering/changed filter uses INVALID_CURSOR. Existing scoped administrator/live-grant behavior remains; no admin shortcut. Foreign owner errors retain generic 403 without private echo.

Catalog private synthetic Approval times intentionally produce order different from model ID sorting. Consumer sees public Capability only. This proves consumer ordering/snapshot behavior, not an unimplemented production registry's approval correctness. Synthetic collaborator acceptance never means real model feasibility, commercial approval or human calibration. Current missing applications will prevent reaching later checks at RED; report that limit and require all cases pass at GREEN.

## Pre-authorized Contingencies

None for file/code changes. Additional files/dependencies, changed assertions/approach or unrelated failure return to planning. Normal tool permissions may permit the identical authorized command in an available host context; this does not authorize altered commands, package installation, Docker lifecycle/settings/context changes or runtime retries.

## Rollback / Recovery

Retain exact target bytes/hash in the stable evidence directory before application. If mechanical application/preservation fails, restore only this target from the verified snapshot and stop. No repository-wide reset/clean/checkout. Existing fixture finally blocks clean only their generated resources; no global Docker cleanup.

## Explicit Exclusions

Production implementation, schema, dependencies, runtime/build/deployment configuration, acoustic policy changes, new public fields/errors, permanent model binding, output-format upload exclusions, full UI/admin Configuration/production catalog transport, calibration/model approval, broader readiness without specific new evidence, completed artifact rewriting, commit/push/publication and user Docker lifecycle changes.

## Human Review

Status: Executed — Enrollment Interface Completion RED Complete on 2026-10-26 under avinash2196 approval recorded 2026-10-26T17:56:49Z. Exact approved one-file diff;40 actual feature identities; two valid missing-production runs (40 errors in41.15s/35.84s); preserved57 regressions pass before106.25s and after98.60s;84 original assertions and full manifest preservation verified. See Plan.md Enrollment Interface Completion RED 012 execution evidence and linked durable actual outputs/hashes/cleanup/permission-contingency history. Later feature bodies remain unverified; no GREEN authorized.
