# Implementation Plan

## Milestone

RED CRM-7 — Chatterbox Model Loading RED + GREEN CRM-8 — Chatterbox Model Loading GREEN (`Plan.md` revision 2, `Decomposition (CRM-7 and CRM-8 only): one pair, one plan`).

## Milestone Type

RED (CRM-7) + GREEN (CRM-8), paired plan. Execution runs in two verified steps: `generate-tests` applies the RED part and records RED evidence; then `implement-approved-plan` applies the GREEN part.

## Review Summary

- Behavior change: RED — tests only. GREEN — Chatterbox loads its model with `from_pretrained(device=DEVICE)`, dropping the `t3_model` argument the pinned `chatterbox-tts==0.1.7` loader does not accept; synthesize and metadata can then answer as contracted.
- Requirements covered: Plan traceability row "Chatterbox model loading through the pinned model runtime's loading interface, with the configured device (defect C6-Q-1; needed for AC-CCR-1)" — owned by CRM-8, verified by CRM-7.
- Files: created none; modified `tests/test_chatterbox_service_red.py` (RED), `voice_narration/chatterbox_api/application.py` (GREEN, one line); deleted none.
- Tests added: C7-T1 (2 cases: model loaded on the default and the configured device, synthesize answers WAV) and C7-T2 (2 cases: metadata answers its contracted body with the default and configured variant). The CRM-2 stand-in loader is aligned to the pinned signature `from_pretrained(cls, device)`, so 8 CRM-2 tests that load the model also become RED evidence, with no assertion changed.
- Verification: `.\.venv\Scripts\python.exe -m pytest tests -ra` — expected RED `12 failed, 63 passed`; GREEN `75 passed`.
- Needs attention: C7-D-1 (aligning the shared CRM-2 stand-in rather than adding a second one); C8-RSK-1 (`CHATTERBOX_MODEL_VARIANT` stays reported but never selected weights in the pinned release).

## Authoritative References

| Document | Status | Used for |
| --- | --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 | AC-CCR-1, RF-5, operational characteristics |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Revision 2 — approved by avinash2196 on 2026-11-10 ("Approve revision 2") | CRM-7 and CRM-8 scope, exclusions, success criteria, traceability, RSK-10, Verification Commands, Execution Status |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09; CRM-1 row Complete in `Plan.md` Execution Status | Constraint (no amendment, per `Plan.md` External Contract Requirements): Chatterbox Synthesize success and failure 7, Chatterbox Health body, Chatterbox Metadata success and failure, CCD-8 |
| `001_Implementation_Plan_Chatterbox_Service_RED.md` | Revision 2 approved by avinash2196 on 2026-11-09; executed | C2-D-1 to C2-D-7, C2-T1 to C2-T13 |
| `002_Implementation_Plan_Chatterbox_Service_GREEN.md` | Approved by avinash2196 on 2026-11-09; executed | C3-D-3, C3-RSK-1 |
| `003_Implementation_Plan_Inference_Client_RED.md` | Approved by avinash2196 on 2026-11-09; executed | Read for Carried-Forward Decisions only; touches no file of this milestone |
| `004_Implementation_Plan_Inference_Client_GREEN.md` | Approved by avinash2196 on 2026-11-10; executed | Read for Carried-Forward Decisions only; touches no file of this milestone |
| `005_Implementation_Plan_Chatterbox_Cloud_Run_Deployment_Document.md` | Awaiting human approval (not authority) | Read only for the C6-Q-1 evidence that `Plan.md` revision 2 cites |
| `docs/developer-setup.md` | Repository documentation | Lines 6, 43-48, 59-65, 79: no CUDA, no model weights, boundary isolation allowed, verification command |
| `docs/requirements.md` | Does not exist | — |
| `chatterbox-tts` 0.1.7 wheel, `https://files.pythonhosted.org/packages/54/37/11a7f06983bfd5ebba71eb2caa6660941b17b31f3c49d4a5fe9e1e804d31/chatterbox_tts-0.1.7-py3-none-any.whl`, SHA-256 `83782500e3ad4e7c919132e9d7eb8755f29f57c5bde5ec48c655ca23a4eb113c` (matches PyPI JSON metadata) | External source, read as a zip, not installed | Loader signature `chatterbox/mtl_tts.py:201-202`, `generate` signature `:249-260`, `self.sr` `:148`, device handling `:167`, `:176`, `:203` |

Skills applied: `implementation-planning`, `prompt-driven-development`, `testing`, `python-fastapi`, `code-quality`. `security` does not apply: neither milestone owns or verifies an authentication or authorization requirement.

## Carried-Forward Decisions

From `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2 (approved 2026-11-09), none reopened:

- C2-D-1 — model boundary `generate(..., audio_prompt_path=<file>)`: unchanged; the stand-in `generate` signature is not touched.
- C2-D-2 — stand-in runtime surface limited to what the application uses: unchanged; the aligned loader narrows the stand-in to the pinned release's own parameter list, which `Plan.md` CRM-7 scope authorizes ("brought into line with the same loading interface").
- C2-D-3, C2-D-4 — retention checks: unchanged. The new `_Recorder.loaded_devices` list is test-owned and is not an application module global.
- C2-D-5, C2-D-6 — concurrency harness and one connection per request over real transport: unchanged.
- C2-D-7 — `raise_server_exceptions=False` / `raise_app_exceptions=False`: unchanged; it is what turns the loader `TypeError` into a `500` status assertion at RED.

From `002_Implementation_Plan_Chatterbox_Service_GREEN.md` (approved 2026-11-09): C3-D-3 — model loading runs under `_generation_lock` inside `_synthesize_wav`: unchanged by the GREEN line.

Conventions carried from CRM-3 to CRM-5 execution (`Plan.md` evidence): files are written with LF endings; content is checked by SHA-256 after writing.

## Preconditions / Predecessor Evidence

- `Plan.md` Execution Status: CRM-1 to CRM-5 Complete; CRM-7 and CRM-8 Pending with no Implementation Plan ("paired Implementation Plan with CRM-8, not yet written"). No earlier plan exists for either milestone.
- CRM-5 is the predecessor of CRM-7. CRM-5 evidence: `71 passed` twice; `voice_narration/inference/application.py` SHA-256 `4a98dafc…1088`. HEAD is `9be9ca8` ("CRM-5 GREEN").
- Inspected on 2026-11-10 at HEAD `9be9ca8`. SHA-256 of the files the recorded evidence names, all matching: `voice_narration/chatterbox_api/application.py` `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a` (CRM-3), `tests/test_chatterbox_service_red.py` `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4` (CRM-2), `tests/_chatterbox_boundary.py` `7ef1a7bd…0608`, `tests/test_inference_client_red.py` `fff78d05…314e`, `tests/test_clone_flow.py` `84416efa…edb8`, `tests/test_ai_gateway_telemetry_red.py` `ab285fd7…2f88`, `voice_narration/inference/application.py` `4a98dafc…1088`.
- `git status --short`: ` M docs/.ai/chatterbox-cloud-run/Plan.md` and `?? docs/.ai/chatterbox-cloud-run/005_Implementation_Plan_Chatterbox_Cloud_Run_Deployment_Document.md`, both under `docs/.ai/<work-item>/` and so expected. No code change is uncommitted.
- Classification (`Plan.md` Current State, "Chatterbox model loading"): production is wrong and no test exposes it, so RED writes or changes tests.
- No FOUNDATION precedes CRM-7 (`Plan.md` Prerequisite coverage): the test runner, `fastapi`, `httpx`, `uvicorn` and `pytest` are declared in `requirements-dev.txt:1-5` and installed in `.venv` (Python 3.13.17).

## Current Repository State

- `voice_narration/chatterbox_api/application.py:20-21` — `DEVICE = os.getenv("CHATTERBOX_DEVICE", "cpu")`, `MODEL_VARIANT = os.getenv("CHATTERBOX_MODEL_VARIANT", "v3")`, read at import.
- `voice_narration/chatterbox_api/application.py:43` — `_model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE, t3_model=MODEL_VARIANT)`.
- `voice_narration/chatterbox_api/application.py:52-53` — `_synthesize_wav` takes `_generation_lock` and then calls `_get_model()`, outside the `try` at `:58-61` that maps generation errors to `_GenerationFailed`; so a load error is an unhandled `500` (contract Synthesize failure 7).
- `voice_narration/chatterbox_api/application.py:77-84` — `health` reports `MODEL_VARIANT` and `DEVICE`; `:138-145` — `metadata` calls `_get_model()` and answers `model_id="chatterbox-multilingual-v3"`, `model_version=MODEL_VARIANT`, `sample_rate_hz=model.sr`.
- `MODEL_VARIANT` stays used after GREEN at `:82` and `:143`.
- `chatterbox/mtl_tts.py:201-202` (pinned 0.1.7 wheel) — `@classmethod def from_pretrained(cls, device: torch.device)`; no `t3_model`, no `**kwargs`. `:211-219` downloads a fixed file list including `t3_mtl23ls_v2.safetensors`. `:203` and `:167` compare `device` with strings, and `:176`, `:183`, `:189` pass it to `.to(device)`, so the application's string device is accepted.
- `tests/test_chatterbox_service_red.py:103-105` — stand-in `from_pretrained(cls, device, **kwargs)` accepts any keyword (why no test caught the defect).
- `tests/test_chatterbox_service_red.py:39-48` — `_Recorder`; `:151-184` — `chatterbox` fixture installs stand-in modules with the function-scoped `monkeypatch` and imports the application fresh, removing it again at teardown.
- `tests/test_chatterbox_service_red.py:204-207` — `_assert_valid_wav_answer` asserts `status_code == 200` first.
- CRM-2 tests that reach `_get_model()` (they call `_synthesize_wav`): C2-T1, C2-T4, C2-T8, C2-T9, C2-T10, C2-T11, C2-T12, C2-T13. Tests that reject before generation and never load: C2-T2, C2-T3, C2-T5, C2-T6, C2-T7.
- No test exercises `/v1/metadata`: `git grep -n "metadata" -- tests` finds only `tests/test_ai_gateway_red.py:19` and `tests/test_ai_gateway_telemetry_red.py:64`, both a gateway request's `"metadata"` field. `git grep -n "chatterbox_api" -- tests` finds only `tests/test_chatterbox_service_red.py:31`.
- `pytest.ini` — `testpaths = tests`, `pythonpath = .`, `--strict-config --strict-markers`; no `conftest.py` exists in `tests/`.
- Git config `core.autocrlf=true`: `git apply` without `-c core.autocrlf=false` writes CRLF (planning dry run, step 3).

## Files in Scope

### Files to Create

None.

### Files to Modify

- RED (CRM-7): `tests/test_chatterbox_service_red.py`.
- GREEN (CRM-8): `voice_narration/chatterbox_api/application.py`.

### Files to Delete

None.

## Proposed Changes

### RED part — `tests/test_chatterbox_service_red.py`

1. Module docstring: name CRM-7 next to CRM-2 and model loading next to synthesize behavior, and state that the stand-in loader accepts exactly the pinned release's loading arguments `from_pretrained(cls, device)`.
2. Constants: add `HEALTH = "/health"`, `METADATA = "/v1/metadata"`, `METADATA_MODEL_ID = "chatterbox-multilingual-v3"` (the contract's Chatterbox Metadata `model_id`).
3. `_Recorder.__init__`: add `self.loaded_devices: list[str] = []`, the device of each `from_pretrained` call.
4. `_FakeMultilingualTTS.from_pretrained`: change the signature from `(cls, device, **kwargs)` to `(cls, device)`, the pinned release's parameter list, so Python itself rejects any other loading argument with `TypeError`; record `device` in `cls.recorder.loaded_devices` under the recorder lock; still return `cls()`. This aligns every CRM-2 test's isolation of the model runtime; no CRM-2 assertion changes.
5. New helper `_reimport_with_settings(chatterbox: _Harness, monkeypatch, settings: dict[str, str | None]) -> _Harness`: sets each setting with `monkeypatch.setenv`, or removes it with `monkeypatch.delenv(..., raising=False)` when its value is `None`; removes the application module from `sys.modules`; imports it again; returns a `_Harness` over the new module with the fixture's recorder and temp root. Needed because `DEVICE` and `MODEL_VARIANT` are read at import (`application.py:20-21`).
6. New test C7-T1 `test_synthesize_loads_model_with_pinned_loader_on_configured_device`, parametrized `default-device` (`CHATTERBOX_DEVICE` removed → `cpu`) and `configured-device` (`cuda` → `cuda`): asserts the setting in force through `GET /health` `device`; then a valid synthesize answers `200` `audio/wav` at the model's sample rate (`_assert_valid_wav_answer`); `loaded_devices == [expected_device]`; the sample reached the model.
7. New test C7-T2 `test_metadata_answers_model_identity_after_pinned_load`, parametrized `default-variant` (`CHATTERBOX_MODEL_VARIANT` removed → `v3`) and `configured-variant` (`v9-test`), with `CHATTERBOX_DEVICE` removed: asserts the setting in force through `GET /health` `model_variant`; then `GET /v1/metadata` answers `200` with exactly `{"model_id": "chatterbox-multilingual-v3", "model_version": <variant>, "sample_rate_hz": 24000}`; `loaded_devices == ["cpu"]`.

Contract rule coverage (`API-Contract.md`, constraint):

| Contract rule | Test |
| --- | --- |
| Chatterbox Synthesize success: `200`, `audio/wav`, at the model's sample rate | C7-T1; C2-T1, C2-T4, C2-T9, C2-T11, C2-T12, C2-T13 (aligned stand-in) |
| Chatterbox Synthesize failure 6 (generation error → `503` prefix) reachable once the model loads | C2-T8, C2-T10 (aligned stand-in) |
| Chatterbox Metadata success body, `model_version` = `CHATTERBOX_MODEL_VARIANT`, `sample_rate_hz` = model rate | C7-T2 |
| Chatterbox Health `device` = `CHATTERBOX_DEVICE` (default `cpu`), `model_variant` = `CHATTERBOX_MODEL_VARIANT` (default `v3`) | C7-T1, C7-T2 — used as the check that the overridden setting is in force; passes at RED and is not RED evidence |
| RF-5 device setting is the device the model loads on | C7-T1 |
| Not tested: Synthesize failure 7 and Metadata failure `500` when the model cannot be loaded | CRM-7 scope lists only the success answers; these failure answers are carried-over baseline behavior and do not change |
| Not tested: "the first call may take as long as a model load" | Informative, not normative |

Test-design decisions for review (they bind CRM-8, which may not change these tests):

- C7-D-1 — Align the shared CRM-2 stand-in loader to `from_pretrained(cls, device)`, rather than adding a second, strict stand-in used only by the new tests. Why: the `**kwargs` stand-in is why the defect went unseen (`Plan.md` Current State), `Plan.md` CRM-7 scope allows the alignment, and with it every Chatterbox test isolates the runtime with the interface the pinned release actually has. Consequence: 8 CRM-2 tests that load the model fail at RED on their own unchanged status assertions, and pass again after GREEN. Alternative: keep `**kwargs` in the CRM-2 stand-in and add a strict stand-in for C7-T1 and C7-T2. Not chosen: 13 tests would keep accepting a loading call the pinned release rejects. Alternative: compare the call with `inspect.signature` of a recorded signature. Not chosen: Python's own argument binding is the exact behavior of the real loader.
- C7-D-2 — New tests go into `tests/test_chatterbox_service_red.py`, not a new module. Why: the stand-in fixture lives in that module and `tests/` has no `conftest.py`; sharing it with a new module would need either importing a fixture from a test module or a new shared test module, and `Plan.md` CRM-7 excludes test-infrastructure changes. Alternative: a new `tests/test_chatterbox_model_loading_red.py` importing the fixture. Not chosen for those reasons.
- C7-D-3 — Settings are overridden by re-importing the application (`_reimport_with_settings`) and proven in force through the contracted `GET /health` fields. Why: the application reads both settings at import (`application.py:20-21`), and `implementation-planning` Repeatable, Isolated Verification requires asserting the effective value. Alternative: `monkeypatch.setattr(application, "DEVICE", ...)`. Not chosen: it would bypass the setting the contract names.
- C7-D-4 — Override values `cuda` and `v9-test`. Any value differing from the defaults would do; `cuda` is the CUDA device name `torch` uses, and the contract leaves `model_variant` a free string. The stand-in does not interpret either.

No dependency, plugin, marker or configuration setting is introduced. Every import already exists in the file.

### GREEN part — `voice_narration/chatterbox_api/application.py`

1. `_get_model()` (line 43): replace `ChatterboxMultilingualTTS.from_pretrained(device=DEVICE, t3_model=MODEL_VARIANT)` with `ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)`. Nothing else changes; `MODEL_VARIANT` is still read at `:21` and reported at `:82` and `:143`.

Implementation decision for review:

- C8-D-1 — Pass only `device=DEVICE`, by keyword. Why: it is the one parameter of the pinned loader (`mtl_tts.py:202`), named as there, and the smallest change that makes the RED evidence pass. Alternative: positional `from_pretrained(DEVICE)` — equivalent; not chosen, to keep the baseline's keyword form. Alternative: pass `t3_model` only when the loader accepts it (`inspect.signature`). Not chosen: speculative support for releases the repository does not pin. Alternative: change the pinned runtime version. Excluded by `Plan.md` CRM-8 ("no change to dependency declarations or the pinned runtime version").

Mapping of RED tests to the change: every one of the 12 RED failures has the same cause, the `t3_model` keyword at `:43` (dry run step 4 shows `TypeError: _FakeMultilingualTTS.from_pretrained() got an unexpected keyword argument 't3_model'`), so the one-line change makes all 12 pass (dry run step 6).

## Proposed Code / Tests

### RED — `tests/test_chatterbox_service_red.py`, complete unified diff against the committed file (SHA-256 before `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`, 490 lines; after `b421a77ca09692a67f9dbc50885ff8eb0d6024d40799e1a5ee8eb7d9a6325225`, 568 lines, LF, ASCII)

```diff
--- a/tests/test_chatterbox_service_red.py
+++ b/tests/test_chatterbox_service_red.py
@@ -1,10 +1,13 @@
-"""CRM-2 RED: Chatterbox model API synthesize behavior (chatterbox-cloud-run API-Contract.md).
+"""CRM-2 and CRM-7 RED: Chatterbox model API synthesize behavior and model loading
+(chatterbox-cloud-run API-Contract.md).
 
 The model runtime (torch, torchaudio, chatterbox) is not installed locally and is never
 loaded here. Each test installs stand-in runtime modules in ``sys.modules`` before it
 imports the Chatterbox application, so no CUDA, model weights or network access is needed.
 The stand-ins only record what the application hands to the model and encode the samples
 the model returns as WAV; every asserted behavior is produced by the application itself.
+The stand-in model loader accepts exactly the loading arguments of the pinned
+chatterbox-tts 0.1.7 release, ``from_pretrained(cls, device)``.
 """
 
 from __future__ import annotations
@@ -30,6 +33,9 @@
 
 APP_MODULE = "voice_narration.chatterbox_api.application"
 SYNTHESIZE = "/v1/synthesize"
+HEALTH = "/health"
+METADATA = "/v1/metadata"
+METADATA_MODEL_ID = "chatterbox-multilingual-v3"
 FAKE_SAMPLE_RATE = 24000
 GENERATED_SAMPLES = [0.0, 0.25, -0.25, 0.5]
 SAMPLE_PATH_DETAIL = "sample_path is not supported; send the voice sample as sample_audio"
@@ -42,6 +48,7 @@
     def __init__(self) -> None:
         self.lock = threading.Lock()
         self.calls: list[dict] = []
+        self.loaded_devices: list[str] = []
         self.active = 0
         self.max_active = 0
         self.delay_seconds = 0.0
@@ -101,7 +108,11 @@
     sr = FAKE_SAMPLE_RATE
 
     @classmethod
-    def from_pretrained(cls, device, **kwargs) -> "_FakeMultilingualTTS":
+    def from_pretrained(cls, device) -> "_FakeMultilingualTTS":
+        """Same parameters as the pinned release's loader: the device is the only one."""
+        recorder = cls.recorder
+        with recorder.lock:
+            recorder.loaded_devices.append(device)
         return cls()
 
     def generate(self, text, language_id, audio_prompt_path=None, **kwargs) -> _FakeTensor:
@@ -184,6 +195,22 @@
         sys.modules.pop(APP_MODULE, None)
 
 
+def _reimport_with_settings(chatterbox: _Harness, monkeypatch, settings: dict[str, str | None]) -> _Harness:
+    """Imports a fresh application under ``settings``; a ``None`` value removes the setting.
+
+    The application reads its settings when it is imported, so the copy the fixture
+    imported is replaced. The stand-in runtime and the recorder stay the fixture's.
+    """
+    for name, value in settings.items():
+        if value is None:
+            monkeypatch.delenv(name, raising=False)
+        else:
+            monkeypatch.setenv(name, value)
+    sys.modules.pop(APP_MODULE, None)
+    application = importlib.import_module(APP_MODULE)
+    return _Harness(application, chatterbox.recorder, chatterbox.temp_root)
+
+
 def _unique_sample() -> bytes:
     return b"RIFF" + os.urandom(48)
 
@@ -488,3 +515,54 @@
             json_body = client.post(SYNTHESIZE, json={"text": "Hello there", "language": "en"})
         _assert_validation_error(json_body)
         assert len(chatterbox.recorder.calls) == 1
+
+
+@pytest.mark.parametrize(
+    ("configured_device", "expected_device"),
+    [(None, "cpu"), ("cuda", "cuda")],
+    ids=["default-device", "configured-device"],
+)
+def test_synthesize_loads_model_with_pinned_loader_on_configured_device(
+    chatterbox, monkeypatch, configured_device, expected_device
+):
+    harness = _reimport_with_settings(chatterbox, monkeypatch, {"CHATTERBOX_DEVICE": configured_device})
+    client = harness.client()
+    health = client.get(HEALTH)
+    assert health.status_code == 200, health.text
+    assert health.json()["device"] == expected_device
+    sample = _unique_sample()
+
+    response = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))
+
+    _assert_valid_wav_answer(response)
+    assert harness.recorder.loaded_devices == [expected_device]
+    assert harness.recorder.calls[0]["prompt_bytes"] == sample
+
+
+@pytest.mark.parametrize(
+    ("configured_variant", "expected_variant"),
+    [(None, "v3"), ("v9-test", "v9-test")],
+    ids=["default-variant", "configured-variant"],
+)
+def test_metadata_answers_model_identity_after_pinned_load(
+    chatterbox, monkeypatch, configured_variant, expected_variant
+):
+    harness = _reimport_with_settings(
+        chatterbox,
+        monkeypatch,
+        {"CHATTERBOX_MODEL_VARIANT": configured_variant, "CHATTERBOX_DEVICE": None},
+    )
+    client = harness.client()
+    health = client.get(HEALTH)
+    assert health.status_code == 200, health.text
+    assert health.json()["model_variant"] == expected_variant
+
+    response = client.get(METADATA)
+
+    assert response.status_code == 200, response.text
+    assert response.json() == {
+        "model_id": METADATA_MODEL_ID,
+        "model_version": expected_variant,
+        "sample_rate_hz": FAKE_SAMPLE_RATE,
+    }
+    assert harness.recorder.loaded_devices == ["cpu"]
```

### GREEN — `voice_narration/chatterbox_api/application.py`, complete unified diff against the committed file (SHA-256 before `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a`; after `a8432b4d4638bee6ed78e98f3eb167492be206086c1615259027ebd3e1ac5281`, 145 lines, LF, ASCII)

```diff
--- a/voice_narration/chatterbox_api/application.py
+++ b/voice_narration/chatterbox_api/application.py
@@ -40,7 +40,7 @@
 def _get_model() -> ChatterboxMultilingualTTS:
     global _model
     if _model is None:
-        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE, t3_model=MODEL_VARIANT)
+        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
     return _model
 
 
```

## Execution Steps

RED step (`generate-tests chatterbox-cloud-run`):

1. Confirm this plan's Human Review status records approval.
2. `git status --short`: only entries under `docs/.ai/chatterbox-cloud-run/`. `git diff --quiet HEAD -- voice_narration/ tests/`: exit `0`.
3. `sha256sum tests/test_chatterbox_service_red.py voice_narration/chatterbox_api/application.py`: `2ce5b014…56d4`, `10cc955b…c54a`.
4. Extract the RED diff block above with LF endings to a scratch file and run `git -c core.autocrlf=false apply <scratch file>`. `sha256sum tests/test_chatterbox_service_red.py`: `b421a77ca09692a67f9dbc50885ff8eb0d6024d40799e1a5ee8eb7d9a6325225`.
5. Run C7-V1, C7-V2, C7-V3 in that order; record evidence in `Plan.md` (CRM-7 row) and set this plan's status to `RED executed — see Plan.md; GREEN approved, not yet executed`.

GREEN step (`implement-approved-plan chatterbox-cloud-run`):

1. Confirm the Human Review status above and the CRM-7 Complete row in `Plan.md`.
2. `git status --short`: ` M tests/test_chatterbox_service_red.py` plus entries under `docs/.ai/chatterbox-cloud-run/` only. `sha256sum tests/test_chatterbox_service_red.py voice_narration/chatterbox_api/application.py`: `b421a77c…5225`, `10cc955b…c54a`.
3. Extract the GREEN diff block above with LF endings to a scratch file and run `git -c core.autocrlf=false apply <scratch file>`. `sha256sum voice_narration/chatterbox_api/application.py`: `a8432b4d4638bee6ed78e98f3eb167492be206086c1615259027ebd3e1ac5281`.
4. Run C8-V1 to C8-V4 in order; record evidence in `Plan.md` (CRM-8 row) and set this plan's status to `Executed — see Plan.md`.

## Acceptance / Completion Criteria

RED (CRM-7):

- C7-AC-1 — `tests/test_chatterbox_service_red.py` has SHA-256 `b421a77c…5225`; no other file changed apart from `Plan.md` Execution Status and this plan's Human Review status.
- C7-AC-2 — 75 tests are collected with no collection, import or fixture error.
- C7-AC-3 — exactly these 12 tests fail, each with an `AssertionError` from its own status assertion (directly or through `_assert_valid_wav_answer`), and no failure is an import, configuration, dependency, transport or environment error: C2-T1, C2-T4, C2-T8, C2-T9, C2-T10, C2-T11, C2-T12, C2-T13, C7-T1 (2 cases), C7-T2 (2 cases).
- C7-AC-4 — the other 63 tests pass, including C2-T2, C2-T3, C2-T5, C2-T6 and C2-T7.
- C7-AC-5 — the repeat run of `tests/test_chatterbox_service_red.py` gives the same 12 failures and 5 passes.

GREEN (CRM-8):

- C8-AC-1 — `voice_narration/chatterbox_api/application.py` has SHA-256 `a8432b4d…5281`; `tests/test_chatterbox_service_red.py` is still `b421a77c…5225`; no other file changed apart from `Plan.md` Execution Status and this plan's Human Review status.
- C8-AC-2 — the full suite passes: 75 collected, 75 passed, no `FAILED` or `ERROR` line.
- C8-AC-3 — the repeat run of `tests/test_chatterbox_service_red.py` passes 17 of 17.
- C8-AC-4 — `t3_model` no longer occurs under `voice_narration/` or `tests/`; the application diff is one line changed in `_get_model` only.

## Verification

### Commands

Write each command's output to a log file and record only its summary and failing tests. Commands are run from the repository root.

- C7-V1 — `.\.venv\Scripts\python.exe -m pytest tests -ra` (full suite once at RED, because `Plan.md` CRM-7 success criteria require "every other test passes").
- C7-V2 — `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -ra --tb=line` (second run, no cleaning; the tests override settings and use temporary directories).
- C7-V3 — `git status --short`.
- C8-V1 — `.\.venv\Scripts\python.exe -m pytest tests -ra`.
- C8-V2 — `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -ra` (second run, no cleaning).
- C8-V3 — `git grep -n "t3_model" -- voice_narration tests` (expected no output, exit `1`).
- C8-V4 — `git status --short` and `git diff --stat -- voice_narration/`.

### Affected Tests

All 13 CRM-2 tests in `tests/test_chatterbox_service_red.py` (C2-T1 to C2-T13), because they use the changed stand-in fixture, plus the four new C7 cases. Found by: the changed file itself; `git grep -n "chatterbox_api" -- tests` lists only `tests/test_chatterbox_service_red.py:31`, so no other test file references the changed application or the stand-in.

### Expected Evidence

Expected / Predicted — Not Yet Verified.

- Preserved-behavior tests (expected to pass at RED): none. C2-T2, C2-T3, C2-T5, C2-T6 and C2-T7 are existing tests in the changed shared file that never load the model; they are expected to pass at RED and are not RED evidence.
- C7-V1: `collected 75 items`, `12 failed, 63 passed, 1 warning` (the existing `StarletteDeprecationWarning`). First failing location per test: `_assert_valid_wav_answer` status line (`tests/test_chatterbox_service_red.py:232`, `assert 500 == 200`) for C2-T1, C2-T4, C2-T9, C2-T11, C2-T12, C2-T13 and both C7-T1 cases; `:427` (`assert 500 == 503`) for C2-T8; `:458` (`assert 500 == 503`) for C2-T10; `:562` (`assert 500 == 200`) for both C7-T2 cases. The captured `uvicorn` log of C2-T13 contains `TypeError: _FakeMultilingualTTS.from_pretrained() got an unexpected keyword argument 't3_model'`. Why this is the missing approved behavior: the `500` is the load failure the pinned loader produces for the `t3_model` keyword (`application.py:43`, `mtl_tts.py:202`), not an absent route or import.
- C7-V2: `12 failed, 5 passed`, same `FAILED` lines.
- C7-V3: ` M tests/test_chatterbox_service_red.py` plus `docs/.ai/chatterbox-cloud-run/` entries.
- C8-V1: `collected 75 items`, `75 passed, 1 warning`.
- C8-V2: `17 passed, 1 warning`.
- C8-V3: no output, exit `1`.
- C8-V4: ` M tests/test_chatterbox_service_red.py`, ` M voice_narration/chatterbox_api/application.py` plus `docs/.ai/chatterbox-cloud-run/` entries; `1 file changed, 1 insertion(+), 1 deletion(-)` with the `LF will be replaced by CRLF` warning.

### Planning-Time Dry Run

Planning-time dry run, not milestone evidence. Run on 2026-11-10 in disposable copies under the session scratchpad `crm78\` (`tar` of `pytest.ini`, `requirements-dev.txt`, `tests`, `voice_narration`, `.env`, `service-account-key.json`, without `__pycache__`), with the repository's `.venv\Scripts\python.exe` (Python 3.13.17) and `-p no:cacheprovider`.

1. Baseline copy, `python -m pytest tests/test_chatterbox_service_red.py -q`: exit `0`, `13 passed, 1 warning in 6.06s`. No pre-existing failure in the affected file. The full suite was not run at planning (proportional rule); its last recorded result is `71 passed` twice at CRM-5, on code whose SHA-256 values match the current files (Preconditions).
2. Wheel check: `chatterbox_tts-0.1.7-py3-none-any.whl` downloaded to the scratchpad, `sha256sum` `83782500…113c` (matches PyPI metadata); `chatterbox/mtl_tts.py:201-202` reads `@classmethod` / `def from_pretrained(cls, device: torch.device) -> 'ChatterboxMultilingualTTS':`; `:249-260` `def generate(self, text, language_id, audio_prompt_path=None, exaggeration=0.5, ...)`.
3. RED diff applied to a fresh baseline copy with `git -c core.autocrlf=false apply red.diff`: applied cleanly; `sha256sum` `b421a77c…5225`, 568 lines, ASCII, LF. (Without `-c core.autocrlf=false`, `git apply` wrote CRLF and a different hash; hence the flag in the Execution Steps.)
4. RED: `python -m compileall -q tests voice_narration`: exit `0`. `python -m pytest tests --collect-only -q`: exit `0`, `75 tests collected`. `python -m pytest tests/test_chatterbox_service_red.py -ra --tb=line`: exit `1`, `12 failed, 5 passed, 1 warning in 1.72s`; failure locations `8 × :232`, `1 × :427`, `1 × :458`, `2 × :562`, all `AssertionError: Internal Server Error`; the log has 1 line `unexpected keyword argument 't3_model'`; count of `ModuleNotFoundError|ImportError|ReadError|ConnectError|RemoteProtocolError|did not start|fixture … not found`: `0`.
5. Extra listing run, `python -m pytest tests/test_chatterbox_service_red.py -rA -q --tb=no`, to name the passing tests: `PASSED` C2-T2, C2-T3, C2-T5, C2-T6, C2-T7.
6. GREEN diff applied on top with `git -c core.autocrlf=false apply green.diff`: applied cleanly; `sha256sum` `a8432b4d…5281`. `python -m pytest tests/test_chatterbox_service_red.py -ra`: exit `0`, `17 passed, 1 warning in 2.90s`; `FAILED`/`ERROR` lines `0`.
7. Created and deleted afterwards: scratchpad folders `crm78\` (copies `base`, `red`, `green`, `apply`, `tools\make_red.py`, `red.diff`, `green.diff`, and logs) and `wheel78\` (wheel, `meta.json`, extracted `mtl_tts.py`). Nothing was written to the repository except this Implementation Plan.

## Risks

- C7-RSK-1 — Real model runtime not exercised (`Plan.md` RSK-10, C3-RSK-1). The stand-in mirrors the pinned loader's parameter list read from the wheel; the real `from_pretrained` downloads weights (`mtl_tts.py:211-219`), which `docs/developer-setup.md:79` says not to acquire here. That the string device is accepted is read from `mtl_tts.py:167`, `:176`, `:203`, not observed at runtime.
- C7-RSK-2 — The aligned stand-in rejects every loading keyword except `device`. If the declared runtime version changes, its loader may differ and these tests must be revisited; dependency declarations are out of scope (`Plan.md` RSK-6, RSK-10).
- C8-RSK-1 — `CHATTERBOX_MODEL_VARIANT` no longer reaches the loader. In the pinned release it never could select weights: the loader always downloads the same file list, including `t3_mtl23ls_v2.safetensors` (`mtl_tts.py:211-219`). Health and metadata keep reporting the setting, and metadata keeps `model_id` `chatterbox-multilingual-v3`, as `API-Contract.md` (Chatterbox Health, Chatterbox Metadata, CCD-8) requires. Whether those reported values describe the loaded weights is a contract matter outside this milestone, noted for the reviewer.
- Security: no identity, role or ownership comparison is introduced or changed.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

- RED: `git restore --source=HEAD -- tests/test_chatterbox_service_red.py`.
- GREEN: `git restore --source=HEAD -- voice_narration/chatterbox_api/application.py`.

## Explicitly Out of Scope

- Any inference-service change, and any change to tests other than `tests/test_chatterbox_service_red.py`.
- Any change to the contract, or to the contracted answers of health, metadata or synthesize, including Synthesize failure 7 and the Metadata load-failure `500`.
- Dependency declarations, the pinned runtime version, build, container, deployment or documentation changes (CRM-6 owns the deployment document).
- Installing the model runtime or acquiring model weights; any test that does so.
- Logging, metrics or alerts.

## Human Review

Status: Executed — see Plan.md
