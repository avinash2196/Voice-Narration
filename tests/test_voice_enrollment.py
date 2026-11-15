"""Real owner boundaries and measurements; test-only evidence, no model-quality claim."""
from copy import deepcopy
from decimal import Decimal
from datetime import timedelta
import hashlib
import importlib
import json
from urllib.parse import urljoin, urlsplit

import numpy as np
import pytest

from test_persistence import NOW, principal, postgres, stores, uid
from test_authentication_consent import (AUTH, ADMIN_PASSWORD, serve, error, verify,
                                         headers, record)
from test_enrollment_quality import (MODEL, CHECKS, candidate_policy, evaluator_identity,
                                    wav_bytes, independent_decode, expected_findings,
                                    check_assessment, codec_bytes)


SETTINGS = {"max_upload_bytes": 500000, "max_samples_per_profile": 3,
            "sample_min_seconds": "1", "sample_max_seconds": "12",
            "signed_link_seconds": 60, "sample_days": 1,
            "default_page_size": 10, "max_page_size": 20}


class TestCatalog:
    __test__ = False

    def __init__(self):
        self.model_ready = True
        self.evaluator_ready = True
        self.policy = candidate_policy()
        self.revision = 1
        self.accepted = None
        self.extra_caps = []
        self.blocked_models = set()
        self.ordered_caps = None
        self.cap = {"model": dict(MODEL), "languages": ["hi", "en"], "mixed_language": True,
                    "styles": ["neutral"], "pause_strength": None, "speech_pace": None,
                    "section_regeneration": False, "mapping": False,
                    "max_script_characters": 100, "max_output_seconds": "12",
                    "sample_min_seconds": "1", "sample_max_seconds": "12",
                    "formats": ["wav"], "enrollment_materials": ["reference_audio"],
                    "recording_guidance": ["Test fixture: record naturally in Hindi or English.",
                                           "Use the displayed duration and a quiet room."]}
        self.accept()

    def accept(self):
        # This is a private test collaborator, never human calibration approval.
        self.accepted = {"test_only": True, "policy": deepcopy(self.policy),
                         "revision": self.revision, "evaluator": evaluator_identity(),
                         "ref": self.policy["calibration_ref"] if self.policy else None}

    def capability(self, model):
        from voice_narration._sql import fail
        if not self.model_ready or (model["model_id"], model["version"]) in self.blocked_models:
            fail("MODEL_NOT_READY")
        for cap in [self.cap] + self.extra_caps:
            if cap["model"] == model:
                return deepcopy(cap)
        fail("MODEL_NOT_READY")

    def list_capabilities(self):
        # Synthetic enabled/approved catalog records for this isolated test only.
        # This does not grant production model or calibration approval.
        if not self.model_ready:
            return []
        # Private synthetic provider order; never expose Approval metadata.
        source = self.ordered_caps if self.ordered_caps is not None else [self.cap]
        return deepcopy(source)

    def snapshot(self):
        return {"revision": self.revision, "enrollment_quality": deepcopy(self.policy)}

    def calibration(self, policy, revision):
        from voice_narration._sql import fail
        if not self.evaluator_ready:
            fail("DEPENDENCY_UNAVAILABLE")
        if (self.accepted is None or self.accepted["policy"] != policy or
                self.accepted["revision"] != revision or
                self.accepted["evaluator"] != evaluator_identity()):
            fail("CONFIGURATION_REQUIRED")
        return deepcopy(self.accepted)


@pytest.fixture
def enrollment_system(stores):
    open_store, paths, targets = stores
    grants = open_store("auth")
    consent_repo = open_store("consent", grants.authorize)
    voices_repo = open_store("voices", grants.authorize)
    artifact_repo = open_store("artifacts", grants.authorize)
    ai_repo = open_store("ai", grants.authorize)
    now = [NOW]
    deliveries = []
    calls = []
    catalog = TestCatalog()
    auth_factory = importlib.import_module("voice_narration.auth.application").create_app
    consent_factory = importlib.import_module("voice_narration.consent.application").create_app
    # Resolve intended missing behavior only after delivered isolated stores initialize.
    artifact_factory = importlib.import_module("voice_narration.artifacts.application").create_app
    voices_factory = importlib.import_module("voice_narration.voices.application").create_app
    adapter_factory = importlib.import_module("voice_narration.ai.enrollment").create_adapter
    auth = auth_factory(database=targets["auth"], root=paths["auth"], auth_settings=dict(AUTH),
                        clock=lambda: now[0],
                        send_verification=lambda email, token: deliveries.append((email, token)),
                        administrator={"email": "admin@example.invalid", "password": ADMIN_PASSWORD,
                                       "name": "Synthetic administrator"})
    consents = consent_factory(repository=consent_repo, authenticate=auth.state.verify_token,
                               clock=lambda: now[0])
    artifacts = artifact_factory(repository=artifact_repo, authenticate=auth.state.verify_token,
                                 validate_consent=consents.state.validate_owner_consent,
                                 capability=catalog.capability, settings=dict(SETTINGS),
                                 clock=lambda: now[0])

    def condition(model, samples, required_materials):
        calls.append({"model": deepcopy(model), "samples": deepcopy(samples),
                      "required_materials": list(required_materials)})
        return {kind: ("test-only-material:" + kind).encode() for kind in required_materials}

    adapter = adapter_factory(repository=ai_repo,
                              validate_consent=consents.state.validate_owner_consent,
                              artifacts=artifacts.state.enrollment_samples,
                              capability=catalog.capability, condition=condition,
                              clock=lambda: now[0])
    def make_voices(repository, pagination=None):
        if pagination is None:
            pagination = {key: SETTINGS[key] for key in
                          ("default_page_size", "max_page_size")}
        return voices_factory(repository=repository, authenticate=auth.state.verify_token,
                              validate_consent=consents.state.validate_owner_consent,
                              artifacts=artifacts.state.enrollment_samples, enrollment=adapter,
                              capability=catalog.capability,
                              list_capabilities=catalog.list_capabilities, pagination=pagination,
                              policy_snapshot=catalog.snapshot,
                              calibration=catalog.calibration, clock=lambda: now[0])

    voices = make_voices(voices_repo)
    assert artifacts.state.effective_settings() == SETTINGS
    assert voices_repo.effective_target()["database"] == targets["voices"]["dbname"]
    assert artifact_repo.effective_target()["root"] == str(paths["artifacts"])
    assert ai_repo.effective_target()["user"] == targets["ai"]["user"]
    assert len({targets[s]["dbname"] for s in targets}) == 8
    try:
        with serve(auth) as accounts, serve(consents) as legal, serve(artifacts) as media, serve(voices) as profiles:
            system = {"auth": accounts, "consent": legal, "now": now,
                      "deliveries": deliveries, "auth_app": auth, "app": consents,
                      "media": media, "profiles": profiles, "voices": voices,
                      "artifacts": artifacts, "adapter": adapter, "catalog": catalog,
                      "calls": calls, "grants": grants, "consent_repo": consent_repo,
                      "voices_repo": voices_repo, "artifact_repo": artifact_repo,
                      "ai_repo": ai_repo, "paths": paths,
                      "make_voices": lambda pagination: make_voices(voices_repo, pagination),
                      "reopen_voices": lambda: make_voices(open_store("voices", grants.authorize))}
            token, _ = verify(system)
            system["token"] = token
            system["consent_record"] = record(system, token)
            yield system
    finally:
        voices.state.close()
        artifacts.state.close()
        auth.state.close()


def upload(system, data=None, fmt="wav", token=None, consent_id=None, expected=201, code=None,
           model=None):
    data = wav_bytes(np.zeros((1, 80000))) if data is None else data
    model = dict(MODEL) if model is None else model
    mime = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
    response = system["media"].post("/artifacts/upload", headers=headers(token or system["token"]),
                                     data={"consent_id": consent_id or system["consent_record"]["consent_id"],
                                           "model_id": model["model_id"], "model_version": model["version"]},
                                     files={"file": ("SYNTHETIC_PRIVATE_FILENAME." + fmt, data, mime)})
    if expected != 201:
        error(response, expected, code)
        return response
    assert response.status_code == 201, response.text
    result = response.json()
    assert set(result) == {"artifact_id", "owner_id", "kind", "consent_id", "profile_id", "job_id",
                           "format", "size_bytes", "duration_seconds", "sample_rate_hz",
                           "created_at", "expires_at", "availability"}
    reference = independent_decode(data)
    assert result["owner_id"] == (token or system["token"])["account"]["user_id"]
    assert result["kind"] == "sample" and result["format"] == fmt
    assert result["size_bytes"] == len(data)
    assert abs(Decimal(result["duration_seconds"]) - reference["duration_seconds"]) <= Decimal("0.000001")
    assert result["sample_rate_hz"] == reference["sample_rate_hz"]
    assert result["availability"] == "available"
    return result


def returned_link_url(system, value):
    base = str(system["media"].base_url)
    resolved = urljoin(base, value)
    expected, actual = urlsplit(base), urlsplit(resolved)
    assert (actual.scheme, actual.netloc) == (expected.scheme, expected.netloc), "Playback stays on the fixture origin"
    return resolved


def create_profile(system, samples, **changes):
    body = {"name": "मेरा निजी स्वर", "language": "hi",
            "consent_id": system["consent_record"]["consent_id"],
            "sample_artifact_ids": [s["artifact_id"] for s in samples], "model": dict(MODEL)}
    body.update(changes)
    return system["profiles"].post("/voices", headers=headers(system["token"]), json=body)


def profile(system, profile_id):
    response = system["profiles"].get("/voices/" + profile_id, headers=headers(system["token"]))
    assert response.status_code == 200, response.text
    return response.json()


def warned(system):
    sample = upload(system)
    response = create_profile(system, [sample])
    assert response.status_code == 202, response.text
    pending = response.json()
    assert pending["status"] == "pending" and pending["quality"] is None and pending["failure"] is None
    system["voices"].state.run_pending(pending["profile_id"])
    value = profile(system, pending["profile_id"])
    assert value["status"] == "awaiting_user_override"
    check_assessment(value["quality"]["findings"], expected_findings(
        [independent_decode(wav_bytes(np.zeros((1, 80000))))],
        system["catalog"].policy, ("1", "12")))
    assert value["quality"]["override_allowed"] is True
    assert value["quality"]["override_acknowledged"] is False
    return value, sample


def override(system, value, assessment_id=None):
    return system["profiles"].patch("/voices/" + value["profile_id"] + "/quality-override",
                                      headers=headers(system["token"]),
                                      json={"assessment_id": assessment_id or value["quality"]["assessment_id"],
                                            "acknowledged": True})


@pytest.mark.integration
def test_guidance_formats_playback_admission_and_originals(enrollment_system):
    s = enrollment_system
    # Capability is exposed by the enrollment service's model boundary for this test.
    response = s["profiles"].get("/models", headers=headers(s["token"]))
    assert response.status_code == 200, response.text
    capability = response.json()["items"][0]
    assert capability == s["catalog"].cap
    assert capability["recording_guidance"] and capability["sample_min_seconds"] == "1"
    payloads = [(wav_bytes(np.zeros((1, 80000))), "wav"),
                (codec_bytes("mp3", "mp3", [np.zeros(72000, dtype=np.int16)]), "mp3"),
                (codec_bytes("mp4", "aac", [np.zeros(72000, dtype=np.int16)]), "m4a")]
    for data, fmt in payloads:
        sample = upload(s, data, fmt)
        result = s["media"].get("/artifacts/" + sample["artifact_id"] + "/preview-url",
                                   headers=headers(s["token"]))
        assert result.status_code == 200, result.text
        link = result.json()
        playback_url = returned_link_url(s, link["url"])
        content = s["media"].get(playback_url, headers=headers(s["token"]))
        assert content.status_code == 200 and content.content == data
        assert "inline" in content.headers["content-disposition"]
        assert content.headers["content-type"].split(";")[0] == {
            "wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
        error(s["media"].get(playback_url), 401, "UNAUTHENTICATED")
        error(s["media"].get("/artifacts/" + sample["artifact_id"] + "/download-url?format=wav",
                               headers=headers(s["token"])), 400, "UNSUPPORTED_FORMAT")
    for data, fmt, code in [(b"", "wav", "INVALID_AUDIO"), (b"not audio", "wav", "INVALID_AUDIO"),
                             (payloads[0][0], "mp3", "INVALID_AUDIO"),
                             (wav_bytes(np.zeros((1, 15999))), "wav", "INVALID_AUDIO"),
                             (wav_bytes(np.zeros((1, 192001))), "wav", "INVALID_AUDIO"),
                             (b"x" * 500001, "wav", "LIMIT_EXCEEDED")]:
        upload(s, data, fmt, expected=400, code=code)
    for length in (16000, 192000):
        upload(s, wav_bytes(np.zeros((1, length))))


@pytest.mark.integration
def test_warning_override_profile_reuse_and_minimal_materials(enrollment_system, caplog):
    s = enrollment_system
    value, sample = warned(s)
    assert s["calls"] == []
    assert value["name"] == "मेरा निजी स्वर" and value["language"] == "hi"
    assert value["model"] == MODEL
    assert [x["artifact_id"] for x in value["samples"]] == [sample["artifact_id"]]
    assert value["samples"][0]["duration_seconds"] == sample["duration_seconds"]
    assert value["consent_id"] == s["consent_record"]["consent_id"]
    assert set(value) == {"profile_id", "owner_id", "name", "language", "consent_id", "samples",
                          "model", "status", "quality", "failure", "created_at", "updated_at"}
    aid = value["quality"]["assessment_id"]
    provenance = s["voices"].state.assessment_provenance(value["profile_id"], aid)
    assert provenance == {"revision": 1, "evaluator": evaluator_identity(),
                           "calibration_ref": "test-only-analytic-v1", "stream_indices": [0]}
    accepted = override(s, value)
    assert accepted.status_code == 200 and accepted.json()["status"] == "enrolling"
    assert accepted.json()["quality"]["override_acknowledged"] is True
    s["voices"].state.run_pending(value["profile_id"])
    complete = profile(s, value["profile_id"])
    assert complete["status"] == "enrolled" and complete["failure"] is None
    assert len(s["calls"]) == 1
    captured = s["calls"][0]
    assert captured["model"] == MODEL and captured["required_materials"] == ["reference_audio"]
    assert [x["artifact_id"] for x in captured["samples"]] == [sample["artifact_id"]]
    assert captured["samples"][0]["bytes"] == wav_bytes(np.zeros((1, 80000)))
    assert captured["samples"][0]["stream_index"] == 0
    account = s["token"]["account"]
    assert s["adapter"].material_kinds(account, value["profile_id"]) == ["reference_audio"]
    records = s["ai_repo"].list(principal(account["user_id"]), owner_id=account["user_id"], now=NOW)
    assert len(records) == 1 and records[0]["profile_id"] == value["profile_id"]
    assert s["ai_repo"].read_bytes(principal(account["user_id"]), records[0]["id"], now=NOW) == [
        b"test-only-material:reference_audio"]
    repeated = override(s, value)
    assert repeated.status_code == 200 and repeated.json() == complete
    s["voices"].state.run_pending(value["profile_id"])
    assert len(s["calls"]) == 1
    listed = s["profiles"].get("/voices?language=hi&status=enrolled", headers=headers(s["token"]))
    assert listed.status_code == 200 and listed.json()["items"] == [complete]
    reopened = s["reopen_voices"]()
    try:
        with serve(reopened) as fresh_process_boundary:
            reread = fresh_process_boundary.get("/voices/" + value["profile_id"],
                                                 headers=headers(s["token"]))
            assert reread.status_code == 200 and reread.json() == complete
    finally:
        reopened.state.close()
    assert s["voices"].state.transition_history(value["profile_id"]) == [
        "pending", "quality_checking", "awaiting_user_override", "enrolling", "enrolled"]
    error(override(s, value, uid()), 409, "STALE_ASSESSMENT")
    for marker in ("SYNTHETIC_PRIVATE_FILENAME", "test-only-material:", "मेरा निजी स्वर"):
        assert marker not in caplog.text


@pytest.mark.integration
def test_obsolete_assessment_rerecording_and_strict_override(enrollment_system):
    s = enrollment_system
    old, sample = warned(s)
    old_quality = deepcopy(old["quality"])
    s["catalog"].revision += 1
    s["catalog"].policy["silence"]["max_fraction"] = 0.5
    s["catalog"].policy["calibration_ref"] = "test-only-analytic-v2"
    s["catalog"].accept()
    error(override(s, old), 409, "STALE_ASSESSMENT")
    current = profile(s, old["profile_id"])
    if current["status"] == "quality_checking":
        s["voices"].state.run_pending(old["profile_id"])
        current = profile(s, old["profile_id"])
    assert current["quality"]["assessment_id"] != old_quality["assessment_id"]
    assert old["quality"] == old_quality and current["quality"]["override_acknowledged"] is False
    fresh, replacement = warned(s)
    assert replacement["artifact_id"] != sample["artifact_id"]
    error(override(s, fresh, old_quality["assessment_id"]), 409, "STALE_ASSESSMENT")
    path = "/voices/" + fresh["profile_id"] + "/quality-override"
    for body in ({"acknowledged": True}, {"assessment_id": fresh["quality"]["assessment_id"],
                  "acknowledged": False}, {"assessment_id": fresh["quality"]["assessment_id"],
                  "acknowledged": True, "extra": 1}):
        error(s["profiles"].patch(path, headers=headers(s["token"]), json=body), 400, "INVALID_INPUT")
    assert s["calls"] == []


@pytest.mark.integration
@pytest.mark.parametrize("gate", ["missing_policy", "missing_calibration", "changed_settings",
                                  "changed_evaluator", "unavailable_evaluator", "model"])
def test_readiness_gates_without_false_pass(enrollment_system, gate):
    s = enrollment_system
    value, sample = warned(s)
    assert value["quality"]["findings"]
    catalog = s["catalog"]
    code = "CONFIGURATION_REQUIRED"
    if gate == "missing_policy":
        catalog.policy = None
    elif gate == "missing_calibration":
        catalog.accepted = None
    elif gate == "changed_settings":
        catalog.policy["clipping"]["max_fraction"] = 0.002
    elif gate == "changed_evaluator":
        catalog.accepted["evaluator"] = "test-only-different-hash"
    elif gate == "unavailable_evaluator":
        catalog.evaluator_ready = False
        code = "DEPENDENCY_UNAVAILABLE"
    else:
        catalog.model_ready = False
        code = "MODEL_NOT_READY"
    error(create_profile(s, [sample]), 503, code)
    assert s["calls"] == []
    # Existing delivered operation stays usable while enrollment alone is unavailable.
    assert s["auth"].get("/auth/me", headers=headers(s["token"])).status_code == 200
    assert record(s, s["token"])["status"] == "active"


@pytest.mark.integration
def test_ownership_reference_validation_and_live_consent_fence(enrollment_system):
    s = enrollment_system
    value, sample = warned(s)
    other, _ = verify(s, "other@example.invalid")
    other_consent = record(s, other)
    files_before = {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()}
    owner = principal(s["token"]["account"]["user_id"])
    rows_before = s["artifact_repo"].list(owner, owner_id=owner["user_id"], now=NOW)
    upload(s, token=other, consent_id=s["consent_record"]["consent_id"], expected=403, code="FORBIDDEN")
    assert s["artifact_repo"].list(owner, owner_id=owner["user_id"], now=NOW) == rows_before
    assert {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()} == files_before
    foreign = upload(s, token=other, consent_id=other_consent["consent_id"])
    for changes, status, code in [({"sample_artifact_ids": []}, 400, "INVALID_INPUT"),
                                  ({"sample_artifact_ids": [sample["artifact_id"]] * 2}, 400, "INVALID_INPUT"),
                                  ({"sample_artifact_ids": [uid()]}, 409, "ARTIFACT_UNAVAILABLE"),
                                  ({"sample_artifact_ids": [foreign["artifact_id"]]}, 403, "FORBIDDEN"),
                                  ({"language": "fr"}, 400, "UNSUPPORTED_CAPABILITY"),
                                  ({"extra": 1}, 400, "INVALID_INPUT")]:
        error(create_profile(s, [sample], **changes), status, code)
    error(s["profiles"].get("/voices/" + value["profile_id"], headers=headers(other)), 403, "FORBIDDEN")
    error(s["profiles"].get("/voices?owner_id=" + other["account"]["user_id"],
                              headers=headers(s["token"])), 403, "FORBIDDEN")
    # Actual Consent persistence fence, through its owner: no invented revocation stub.
    owner = principal(s["token"]["account"]["user_id"])
    cid = s["consent_record"]["consent_id"]
    s["consent_repo"].fence(owner, profile_id=cid, consent_id=cid, reason="consent_revoked",
                             now=NOW, cleanup_window_seconds=60)
    error(override(s, value), 409, "CONSENT_REVOKED")
    upload(s, expected=409, code="CONSENT_REVOKED")
    s["voices"].state.run_pending(value["profile_id"])
    assert s["calls"] == []


@pytest.mark.integration
@pytest.mark.parametrize("materials", [["reference_audio"], ["embeddings"], ["weights"]])
def test_all_pass_without_override_and_model_minimal_material_selection(enrollment_system, materials):
    s = enrollment_system
    policy = candidate_policy()
    # Explicit test settings exercise all-pass control flow; not candidate/default calibration.
    policy["clipping"]["max_fraction"] = 1
    policy["silence"]["max_fraction"] = 1
    policy["noise"] = {"min_snr_db": -100, "min_speech_seconds": 0.000001,
                       "min_nonspeech_seconds": 0.000001}
    policy["level"] = {"min_speech_rms_dbfs": -120, "max_speech_rms_dbfs": 0}
    policy["speech_presence"] = {"min_fraction": 0, "min_seconds": 0.000001}
    chosen = None
    for pitch in (110, 170, 230, 310):
        t = np.arange(80000) / 16000
        values = np.random.default_rng(200 + pitch).normal(0, 0.0002, (1, t.size))
        window = (t >= 1) & (t < 4)
        values[0, window] += (0.12 * np.sin(2 * np.pi * pitch * t[window]) +
                               0.04 * np.sin(2 * np.pi * 3 * pitch * t[window]))
        data = wav_bytes(values)
        reference = expected_findings([independent_decode(data)], policy, ("1", "12"))
        if all(finding[1] == "pass" for finding in reference):
            chosen = (data, reference)
            break
    assert chosen is not None, "Synthetic native-label fixture failure is not valid RED"
    s["catalog"].policy = policy
    s["catalog"].cap["enrollment_materials"] = materials
    s["catalog"].accept()
    sample = upload(s, chosen[0])
    response = create_profile(s, [sample], language="en", name="Synthetic English profile")
    assert response.status_code == 202, response.text
    pid = response.json()["profile_id"]
    s["voices"].state.run_pending(pid)
    value = profile(s, pid)
    assert value["status"] == "enrolled"
    check_assessment(value["quality"]["findings"], chosen[1])
    assert value["quality"]["override_allowed"] is False
    assert value["quality"]["override_acknowledged"] is False
    assert s["voices"].state.transition_history(pid) == [
        "pending", "quality_checking", "enrolling", "enrolled"]
    assert len(s["calls"]) == 1 and s["calls"][0]["required_materials"] == materials
    assert s["adapter"].material_kinds(s["token"]["account"], pid) == materials
    who = principal(s["token"]["account"]["user_id"])
    rows = s["ai_repo"].list(who, owner_id=who["user_id"], now=NOW)
    assert len(rows) == 1
    assert s["ai_repo"].read_bytes(who, rows[0]["id"], now=NOW) == [
        ("test-only-material:" + materials[0]).encode()]
    error(override(s, value), 409, "OVERRIDE_NOT_ALLOWED")
    assert len(s["calls"]) == 1


@pytest.mark.integration
def test_evaluator_execution_failure_cannot_be_overridden(enrollment_system, monkeypatch):
    s = enrollment_system
    # First prove the evaluator is active and warnings exist before fault injection.
    original, sample = warned(s)
    import webrtcvad

    def unavailable(self, data, sample_rate, length=None):
        raise RuntimeError("synthetic evaluator execution fault")

    monkeypatch.setattr(webrtcvad.Vad, "is_speech", unavailable)
    response = create_profile(s, [sample], name="Synthetic execution failure")
    assert response.status_code == 202, response.text
    pid = response.json()["profile_id"]
    s["voices"].state.run_pending(pid)
    value = profile(s, pid)
    assert value["status"] == "failed"
    assert value["failure"]["code"] == "DEPENDENCY_UNAVAILABLE"
    assert value["failure"]["message"].strip() and value["failure"]["action"].strip()
    assert value["quality"] is None
    error(override(s, value, original["quality"]["assessment_id"]), 409, "INVALID_STATE")
    assert s["calls"] == []


@pytest.mark.integration
def test_multistream_metadata_playback_and_conditioning(enrollment_system):
    s = enrollment_system
    data = codec_bytes("mp4", "aac", [np.zeros(48000, dtype=np.int16),
                       np.full(72000, 2048, dtype=np.int16)], default_index=1)
    reference = independent_decode(data)
    sample = upload(s, data, "m4a")
    response = create_profile(s, [sample])
    assert response.status_code == 202, response.text
    pid = response.json()["profile_id"]
    s["voices"].state.run_pending(pid)
    value = profile(s, pid)
    check_assessment(value["quality"]["findings"], expected_findings(
        [reference], s["catalog"].policy, ("1", "12")))
    assert value["status"] == "awaiting_user_override"
    assert override(s, value).status_code == 200
    s["voices"].state.run_pending(pid)
    captured = s["calls"][0]["samples"][0]
    assert captured["stream_index"] == reference["stream_index"] and captured["bytes"] == data
    response = s["media"].get("/artifacts/" + sample["artifact_id"] + "/preview-url",
                                 headers=headers(s["token"]))
    assert response.status_code == 200, response.text
    playback_url = returned_link_url(s, response.json()["url"])
    playback = s["media"].get(playback_url, headers=headers(s["token"]))
    assert playback.status_code == 200 and playback.content == data
    assert independent_decode(playback.content)["stream_index"] == captured["stream_index"]


@pytest.mark.integration
@pytest.mark.parametrize("part", ["model_id", "model_version"])
@pytest.mark.parametrize("defect", ["missing", "blank", "duplicate", "malformed"])
def test_upload_model_parts_closed(enrollment_system, part, defect):
    s = enrollment_system
    upload(s)
    who = principal(s["token"]["account"]["user_id"])
    before = s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW)
    files_before = {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()}
    fields = {"consent_id": s["consent_record"]["consent_id"],
              "model_id": MODEL["model_id"], "model_version": MODEL["version"]}
    if defect == "missing":
        del fields[part]
    elif defect == "blank":
        fields[part] = "  "
    elif defect == "malformed":
        if part == "model_id":
            fields[part] = MODEL["model_id"].upper()
        else:
            del fields[part]
    parts = [(key, (None, value)) for key, value in fields.items()]
    if defect == "duplicate":
        parts.append((part, (None, fields[part])))
    if defect == "malformed" and part == "model_version":
        parts.append((part, ("version.bin", b"test-only-v1", "application/octet-stream")))
    parts.append(("file", ("synthetic.wav", wav_bytes(np.zeros((1, 80000))), "audio/wav")))
    error(s["media"].post("/artifacts/upload", headers=headers(s["token"]), files=parts),
          400, "INVALID_INPUT")
    assert s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW) == before
    assert {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()} == files_before


@pytest.mark.integration
def test_unknown_parts_and_unready_models_discard_streams(enrollment_system):
    s = enrollment_system
    upload(s)
    who = principal(s["token"]["account"]["user_id"])
    before = s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW)
    files_before = {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()}
    parts = [("consent_id", (None, s["consent_record"]["consent_id"])),
             ("model_id", (None, MODEL["model_id"])), ("model_version", (None, MODEL["version"])),
             ("extra", (None, "unknown")),
             ("file", ("synthetic.wav", wav_bytes(np.zeros((1, 80000))), "audio/wav"))]
    error(s["media"].post("/artifacts/upload", headers=headers(s["token"]), files=parts),
          400, "INVALID_INPUT")
    upload(s, model={"model_id": uid(), "version": "unknown"}, expected=503, code="MODEL_NOT_READY")
    upload(s, model={"model_id": MODEL["model_id"], "version": "unknown"},
           expected=503, code="MODEL_NOT_READY")
    # Known but unapproved identity is represented by the trusted provider gate.
    s["catalog"].blocked_models.add((MODEL["model_id"], MODEL["version"]))
    upload(s, expected=503, code="MODEL_NOT_READY")
    s["catalog"].blocked_models.clear()
    s["catalog"].model_ready = False
    upload(s, expected=503, code="MODEL_NOT_READY")
    assert s["artifact_repo"].list(who, owner_id=who["user_id"], now=NOW) == before
    assert {p: p.read_bytes() for p in s["paths"]["artifacts"].rglob("*") if p.is_file()} == files_before


@pytest.mark.integration
def test_selected_model_bounds_guidance_and_independent_reuse(enrollment_system):
    s = enrollment_system
    catalog = s["catalog"]
    alternate = deepcopy(catalog.cap)
    alternate["model"] = {"model_id": uid(), "version": "test-only-alternate"}
    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "4", "6"
    alternate["recording_guidance"] = ["Synthetic alternate guidance: four to six seconds."]
    catalog.extra_caps = [alternate]
    catalog.ordered_caps = [alternate, catalog.cap]
    listed = s["profiles"].get("/models", headers=headers(s["token"]))
    assert listed.status_code == 200 and listed.json()["items"][0] == alternate
    selected = listed.json()["items"][0]
    sample = upload(s, model=selected["model"])
    assert s["artifact_repo"].read_bytes(principal(s["token"]["account"]["user_id"]),
                                         sample["artifact_id"], now=NOW) == [wav_bytes(np.zeros((1, 80000)))]
    for frames in (63999, 96001):
        upload(s, wav_bytes(np.zeros((1, frames))), model=selected["model"],
               expected=400, code="INVALID_AUDIO")
    for frames in (64000, 96000):
        upload(s, wav_bytes(np.zeros((1, frames))), model=selected["model"])
    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "0.5", "20"
    for frames in (15999, 192001):
        upload(s, wav_bytes(np.zeros((1, frames))), model=alternate["model"],
               expected=400, code="INVALID_AUDIO")
    for frames in (16000, 192000):
        upload(s, wav_bytes(np.zeros((1, frames))), model=alternate["model"])
    response = create_profile(s, [sample], model=dict(MODEL))
    assert response.status_code == 202, response.text
    pid = response.json()["profile_id"]
    s["voices"].state.run_pending(pid)
    value = profile(s, pid)
    assert value["status"] == "awaiting_user_override"
    assert override(s, value).status_code == 200
    s["voices"].state.run_pending(pid)
    assert profile(s, pid)["status"] == "enrolled"
    assert s["calls"][-1]["model"] == MODEL
    before_calls = len(s["calls"])
    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "6", "7"
    error(create_profile(s, [sample], model=alternate["model"]), 400, "INVALID_INPUT")
    assert len(s["calls"]) == before_calls
    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "4", "6"
    pending = create_profile(s, [sample], model=alternate["model"])
    assert pending.status_code == 202, pending.text
    later = pending.json()["profile_id"]
    s["voices"].state.run_pending(later)
    warned_value = profile(s, later)
    assert warned_value["status"] == "awaiting_user_override"
    assert override(s, warned_value).status_code == 200
    alternate["sample_min_seconds"], alternate["sample_max_seconds"] = "6", "7"
    s["voices"].state.run_pending(later)
    assert profile(s, later)["status"] == "failed"
    assert len(s["calls"]) == before_calls


def catalog_records(catalog, count):
    from uuid import UUID
    private = []
    for index in range(count):
        cap = deepcopy(catalog.cap)
        cap["model"] = {"model_id": str(UUID(int=index + 1)), "version": "test-only-catalog"}
        private.append((NOW + timedelta(seconds=(index * 7) % count), cap))
    # Approval data stays private; consumer gets ordered public Capability only.
    private.sort(key=lambda row: (row[0], row[1]["model"]["model_id"],
                                  row[1]["model"]["version"]), reverse=True)
    catalog.ordered_caps = [cap for approved_at, cap in private]
    return deepcopy(catalog.ordered_caps)


@pytest.mark.integration
def test_catalog_order_limits_and_authenticated_snapshot(enrollment_system):
    s = enrollment_system
    expected = catalog_records(s["catalog"], 23)
    assert expected != sorted(expected, key=lambda cap: cap["model"]["model_id"], reverse=True)
    first = s["profiles"].get("/models", headers=headers(s["token"]))
    assert first.status_code == 200, first.text
    page = first.json()
    assert page["items"] == expected[:SETTINGS["default_page_size"]] and page["next_cursor"]
    maximum = s["profiles"].get("/models?limit=20", headers=headers(s["token"]))
    assert maximum.status_code == 200 and maximum.json()["items"] == expected[:20]
    error(s["profiles"].get("/models?limit=21", headers=headers(s["token"])), 400, "LIMIT_EXCEEDED")
    error(s["profiles"].get("/models"), 401, "UNAUTHENTICATED")
    other, _ = verify(s, "catalog-other@example.invalid")
    query = {"cursor": page["next_cursor"]}
    error(s["profiles"].get("/models", params=query, headers=headers(other)), 400, "INVALID_CURSOR")
    error(s["profiles"].get("/models", params={"cursor": page["next_cursor"] + "x"},
                             headers=headers(s["token"])), 400, "INVALID_CURSOR")
    fresh = deepcopy(expected[0]); fresh["model"]["model_id"] = uid()
    s["catalog"].ordered_caps.insert(0, fresh)
    items = list(page["items"])
    while page["next_cursor"] is not None:
        response = s["profiles"].get("/models", params={"cursor": page["next_cursor"]},
                                      headers=headers(s["token"]))
        assert response.status_code == 200, response.text
        page = response.json()
        assert page["items"]
        items.extend(page["items"])
        assert len(items) <= len(expected)
    assert items == expected
    s["catalog"].model_ready = False
    empty = s["profiles"].get("/models", headers=headers(s["token"]))
    assert empty.status_code == 200 and empty.json() == {"items": [], "next_cursor": None}


@pytest.mark.integration
def test_profile_limits_filters_and_stable_snapshot(enrollment_system):
    s = enrollment_system
    sample = upload(s)
    created = []
    for index in range(21):
        s["now"][0] = NOW + timedelta(seconds=index)
        response = create_profile(s, [sample], name="Synthetic page " + str(index))
        assert response.status_code == 202, response.text
        created.append(response.json())
    expected = list(reversed(created))
    response = s["profiles"].get("/voices?language=hi&status=pending", headers=headers(s["token"]))
    assert response.status_code == 200, response.text
    page = response.json()
    assert page["items"] == expected[:10] and page["next_cursor"]
    maximum = s["profiles"].get("/voices?limit=20", headers=headers(s["token"]))
    assert maximum.status_code == 200 and maximum.json()["items"] == expected[:20]
    error(s["profiles"].get("/voices?limit=21", headers=headers(s["token"])), 400, "LIMIT_EXCEEDED")
    other, _ = verify(s, "page-other@example.invalid")
    query = {"cursor": page["next_cursor"], "language": "hi", "status": "pending"}
    error(s["profiles"].get("/voices", params=query, headers=headers(other)), 400, "INVALID_CURSOR")
    error(s["profiles"].get("/voices", params=dict(query, language="en"),
                             headers=headers(s["token"])), 400, "INVALID_CURSOR")
    s["now"][0] += timedelta(seconds=1)
    assert create_profile(s, [sample], name="Synthetic post-snapshot").status_code == 202
    items = list(page["items"])
    while page["next_cursor"] is not None:
        query["cursor"] = page["next_cursor"]
        response = s["profiles"].get("/voices", params=query, headers=headers(s["token"]))
        assert response.status_code == 200, response.text
        page = response.json()
        assert page["items"]
        items.extend(page["items"])
        assert len(items) <= len(expected)
    assert items == expected
    foreign = s["profiles"].get("/voices", headers=headers(other))
    assert foreign.status_code == 200 and foreign.json() == {"items": [], "next_cursor": None}


@pytest.mark.integration
@pytest.mark.parametrize("pagination", [{}, {"default_page_size": 0, "max_page_size": 20},
    {"default_page_size": 21, "max_page_size": 20},
    {"default_page_size": True, "max_page_size": 20},
    {"default_page_size": 10, "max_page_size": "20"},
    {"default_page_size": 10, "max_page_size": 20, "extra": 1}])
def test_pagination_configuration_fails_closed(enrollment_system, pagination):
    s = enrollment_system
    working = s["profiles"].get("/models", headers=headers(s["token"]))
    assert working.status_code == 200 and working.json()["items"]
    from voice_narration._sql import PersistenceError
    with pytest.raises(PersistenceError) as caught:
        s["make_voices"](pagination)
    assert caught.value.code == "INVALID_CONFIGURATION"


@pytest.mark.integration
def test_nondefault_pagination_controls_both_handlers(enrollment_system):
    s = enrollment_system
    expected = catalog_records(s["catalog"], 5)
    sample = upload(s)
    created = []
    for index in range(5):
        s["now"][0] = NOW + timedelta(seconds=index)
        response = create_profile(s, [sample], name="Synthetic configured " + str(index))
        assert response.status_code == 202, response.text
        created.append(response.json())
    app = s["make_voices"]({"default_page_size": 2, "max_page_size": 3})
    try:
        with serve(app) as client:
            for endpoint, records in (("/models", expected), ("/voices", list(reversed(created)))):
                first = client.get(endpoint, headers=headers(s["token"]))
                assert first.status_code == 200 and first.json()["items"] == records[:2]
                maximum = client.get(endpoint, params={"limit": 3}, headers=headers(s["token"]))
                assert maximum.status_code == 200 and maximum.json()["items"] == records[:3]
                error(client.get(endpoint, params={"limit": 4}, headers=headers(s["token"])),
                      400, "LIMIT_EXCEEDED")
    finally:
        app.state.close()
