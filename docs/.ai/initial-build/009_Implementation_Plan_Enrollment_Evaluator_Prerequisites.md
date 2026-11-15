# Implementation Plan — Enrollment Evaluator Prerequisites

## Milestone

initial-build milestone 9, Enrollment Evaluator Prerequisites. Milestone type: FOUNDATION. The approved Plan records it Pending; no earlier approved/unexecuted plan exists for it. This proposal establishes executable prerequisites for Voice Enrollment RED and its dependent regression/integration/browser checks. It does not implement enrollment.

## Authoritative References

Repository-relative references below were inspected. Their current approval records govern over historical descriptions of repository state.

| Reference | Authority / disposition |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Revised Q11 requirements approved by avinash2196, recorded 2026-10-25T21:07:15Z. |
| docs/.ai/initial-build/Plan.md | Revised Plan approved 2026-10-25T21:13:12Z; milestone 8 Complete, 9 Pending. Scope, sequence, exclusions and execution evidence. |
| docs/.ai/initial-build/contract/API-Contract.md | Complete resulting contract; Q11 amendment approved by avinash2196, recorded 2026-10-25T21:30:20Z. Authoritative predecessor. |
| docs/.ai/initial-build/Enrollment-Quality-Policy-Proposal.md | Approved by avinash2196, recorded 2026-10-25T21:03:55Z. WebRTC GMM mechanism, dependency boundary and later calibration gates. |
| docs/.ai/initial-build/001_Implementation_Plan_Foundation.md | Approved/executed general prerequisites, including exact runtime/tool versions and nine harness files. |
| docs/.ai/initial-build/002_Implementation_Plan_Model_Feasibility.md; model-eval/approved.md | Approved/executed assessment and investigation-only model/protocol decision; no model acquisition or commercial/production clearance. |
| docs/.ai/initial-build/003_Implementation_Plan_Persistence_RED.md | Approved/stopped history, superseded operationally by 004 recovery. |
| docs/.ai/initial-build/004_Implementation_Plan_Persistence_RED_Recovery.md; 004-red-run2.txt | Approved/executed recovery, 33-case RED evidence and unchanged test/helper. |
| docs/.ai/initial-build/005_Implementation_Plan_Persistence_GREEN.md | Approved exact eighteen production files; completed through 006 verification recovery. |
| docs/.ai/initial-build/006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved/executed recovery; bounded diagnostics, isolation and preservation conventions. |
| docs/.ai/initial-build/007_Implementation_Plan_Authentication_Consent_RED.md | Approved/executed 24-case authentication/consent tests and real HTTP fixtures. |
| docs/.ai/initial-build/008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved/executed exact four production files; combined 57-case regression evidence. |
| voice_narration_PDD_requirements.md | Retained nonconflicting product context; work-item Q11 governs its refinement. No docs/requirements.md exists. |
| requirements-dev.txt; tools/readiness.py; containers/harness.Dockerfile; compose.harness.yaml; .dockerignore; .github/workflows/harness.yml; docs/developer-setup.md; tests/test_persistence.py; tests/test_authentication_consent.py; voice_narration/ | Delivered repository facts, not new authority. |
| Installed plugin commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md and templates/Implementation-Plan.md; skills/security/SKILL.md; skills/testing/SKILL.md; skills/python-fastapi/SKILL.md | Process guidance under C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0; no product approval. |

## Predecessor Evidence and Current Repository State

Plan execution evidence records the general FOUNDATION Windows two-pass checks and successful Linux CI run 40132442843. Authentication/Consent GREEN records two combined **57/57 passes**, 94.11s and 93.39s, exact four new files, preserved eighteen persistence files, 004/007 tests and foundation files, fixture cleanup, and running user Docker. Those are historical verified predecessor results, not new runs for 009. The contract amendment's recorded approval completes milestone 8 without claiming runtime evidence.

The checkout contains requirements-dev.txt with nine direct pins and no VAD distribution. tools/readiness.py imports the pinned PyAV/NumPy stack and checks WAV decode and codec availability; it neither imports a detector nor executes a resampler. The image copies only the general requirements; its ignore whitelist admits only that manifest and Dockerfile. CI verifies general prerequisites on ubuntu-24.04. These inspected files establish the genuine missing dependency/invocation prerequisite; missing enrollment classes are not a FOUNDATION trigger.

The checkout has pre-existing modified/untracked authority, model-evaluation, tests and implementation work. Preserve it. No clean-tree assertion is made. No tests, application, Docker command, package installation or package/model asset download was executed while planning. Only read-only source/metadata research and document/static checks are permitted here.

## Carried-Forward Decisions

Keep 001's CPython 3.13.17 x64, official python:3.13.17-slim-trixie image, PostgreSQL 18.6, Compose 5.6.0, Docker 29.3.1 Windows expectation, all nine requirements-dev.txt pins, pytest9.1.1, HTTPX0.28.1, PyAV19.0.2, NumPy2.5.4, Playwright1.64.1, existing Linux runner/actions and unique loopback/tmpfs/temp-root isolation. Keep 004's command-only `-p no:anyio`, exact tests/helper; 005/006 owner-separated databases/credentials, canonical identities and live grants; 007/008 exact HTTP fixtures and four implementation files. No automatic upgrades or new test framework/client/isolation mechanism. User's pre-existing running Docker is left running; no shutdown/restart/lifecycle command is authorized for it.

Only three previously approved harness files change, through the exact reviewed diffs below: Dockerfile, its ignore whitelist and CI workflow. requirements-dev.txt, tools/readiness.py, compose.harness.yaml, pytest.ini, .gitignore and docs/developer-setup.md remain byte-for-byte preserved. The separate evaluator manifest avoids accidentally applying pip's global hash mode to the existing un-hashed dependency graph.

## Binding Decisions for Human Review

| Choice | Selected technical decision and evidence | Alternatives considered |
| --- | --- | --- |
| Detector distribution | webrtcvad-wheels==2.0.14.post1, importing webrtcvad/_webrtcvad. Latest maintainer packaging refresh 2026-10-02 explicitly supports CPython3.10–3.14; real native call delegates to WebRtcVad_Process, whose vad_core.c uses Gaussian mixture models with compiled constant tables. No downloaded weights. | Original webrtcvad2.0.10 lacks the selected maintained wheel/support evidence and would add source-build uncertainty. Silero/ONNX or energy heuristics change the approved detector/mechanism and are not substitutes. Earlier wheels2.0.14 is superseded by the maintained packaging refresh, not selected for cache convenience. |
| Platforms/build | Exactly cp313 win_amd64 and cp313 manylinux2014_x86_64/manylinux_2_17_x86_64 wheels, hash allowlisted below. Existing Windows x64 and Linux x86_64 harness/CI can use binaries without installing compilers. Binary-only installation fails closed on other architectures. | Building sdist would add compiler/build isolation dependencies and new evidence; not authorized. No ARM/macOS support claim. |
| Scope/isolation | A separate stdlib/PyAV prerequisite script checks identity, installed-file RECORD hashes, real decoder/resampler and real VAD calls. It accepts no audio path, user settings, policy or private content. Synthetic all-zero PCM is an executable smoke input only. | Adding detector adapters, classifiers or domain fixtures would preempt Enrollment RED/GREEN and is excluded. |
| Hash/provenance | Separate hash-only manifest installed with --no-deps --only-binary=:all: --require-hashes; ordinary general manifest unchanged. Record source commit and both per-platform artifacts, plus runtime binary/wrapper hashes. | Hashing/upgrading the entire approved general dependency graph is unrelated scope. No mutable branch is used as the artifact identity. |
| Offline verification | Python audit hook denies socket connection/name resolution before importing decoder/detector; invoke twice in process and twice as separate commands. Linux image additionally runs with --network none. | Installing network-control software or changing Windows firewall is unnecessary new host scope. Audit-hook coverage is limited to Python events; native-source inspection and Linux network isolation supply complementary evidence. |

Primary sources inspected 2026-10-25: [PyPI release/support](https://pypi.org/project/webrtcvad-wheels/2.0.14.post1/), [exact release JSON](https://pypi.org/pypi/webrtcvad-wheels/2.0.14.post1/json), [immutable setup.py](https://github.com/daanzu/py-webrtcvad-wheels/blob/726a8c72ce8b33b2df7ecd292372690fea2bad0c/setup.py), [wrapper](https://github.com/daanzu/py-webrtcvad-wheels/blob/726a8c72ce8b33b2df7ecd292372690fea2bad0c/webrtcvad.py), [native bridge](https://github.com/daanzu/py-webrtcvad-wheels/blob/726a8c72ce8b33b2df7ecd292372690fea2bad0c/cbits/pywebrtcvad.c), [GMM source](https://github.com/daanzu/py-webrtcvad-wheels/blob/726a8c72ce8b33b2df7ecd292372690fea2bad0c/cbits/webrtc/common_audio/vad/vad_core.c), [license](https://github.com/daanzu/py-webrtcvad-wheels/blob/726a8c72ce8b33b2df7ecd292372690fea2bad0c/LICENSE), [manifest](https://github.com/daanzu/py-webrtcvad-wheels/blob/726a8c72ce8b33b2df7ecd292372690fea2bad0c/MANIFEST.in). This is current maintainer publication/compatibility evidence, not a long-term-support guarantee or proof of successful installation.

PyPI provenance for [Windows](https://pypi.org/integrity/webrtcvad-wheels/2.0.14.post1/webrtcvad_wheels-2.0.14.post1-cp313-cp313-win_amd64.whl/provenance) and [Linux](https://pypi.org/integrity/webrtcvad-wheels/2.0.14.post1/webrtcvad_wheels-2.0.14.post1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl/provenance) identifies daanzu/py-webrtcvad-wheels, build.yml. Inspected publication statements bind the same SHA256 subjects below; publisher certificate records source726a8c72ce8b33b2df7ecd292372690fea2bad0c and tag2.0.14.post1. Reading these records is not an independent cryptographic attestation verification claim.

| Artifact | Bytes | SHA256 |
| --- | --- | --- |
| webrtcvad_wheels-2.0.14.post1-cp313-cp313-win_amd64.whl | 20675 | ffbe00c93e2b03ee511c7fad29c4d92ec17cd33bc181c55636334079252b633f |
| webrtcvad_wheels-2.0.14.post1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl | 83227 | 70176f1a20edb64d55616161361b0f71105a16041b1e205685c8af3f7c8dc727 |
| webrtcvad_wheels-2.0.14.post1.tar.gz, metadata inventory only; NOT authorized for installation | 187822 | c740e93d24b5d0d7ecdd5548c43e37e2c88564826e869c861d5e3fa7f1cee7ff |

## License and Asset Inventory

The exact source tree's LICENSE combines MIT (Python wrapper/C extension packaging, John Wiseman) and WebRTC BSD3 (vendored native code, WebRTC project authors). Both permit use/modification/redistribution subject to retained notices; native BSD3 also forbids implied endorsement. Preserve the installed complete LICENSE, copyright/conditions/disclaimer with redistributed binaries/images; do not replace it with PyPI's short MIT label. No source license is inferred from the absence of runtime dependencies.

Native header references PATENTS and AUTHORS, but recursive exact release-tree inventory contains neither file. MANIFEST.in includes LICENSE and cbits headers, not those absent files. This absence is explicitly recorded, not represented as bundled notices. Official upstream [PATENTS](https://webrtc.googlesource.com/src/+/refs/heads/main/PATENTS) provides an additional limited Google patent grant with litigation termination; [AUTHORS](https://webrtc.googlesource.com/src/+/refs/heads/main/AUTHORS) records contributors. These current upstream references are contextual, not a claim of reconstructing the vendored historical author's snapshot or proving complete patent clearance. The binding's explicit combined MIT/BSD3 license supplies the permissive copyright license; this plan does not claim unrestricted patent coverage. Execution must confirm the wheel carries its complete LICENSE; missing/different notice, undeclared native payload/dependency or incompatible provenance stops for review. No new legal/commercial model approval is inferred.

PyPI requires_dist contains only unittest2 and psutil conditioned on extra==dev; ordinary installation declares zero runtime Python dependencies. Do not install extras. Native VAD and compiled GMM constants are part of the selected wheel; no separately acquired model/data asset, account, network service, telemetry SDK or external executable is required by inspected wrapper/setup/native bridge. Windows system CRT and Linux loader/libc remain platform prerequisites, not Python dependencies; import success on each actual platform is required. Existing PyAV wheel/native FFmpeg libraries retain the predecessor's separate license boundary, not relicensed by the new binding.

## Files in Scope and Ordered Proposed Changes

Create:

1. requirements-evaluator.txt — exactly one pinned binary-only evaluator allowlisted by the two wheel hashes.
2. tools/evaluator_readiness.py — independent prerequisite identity/integrity/offline decoder/resampler/native invocation smoke, no domain code or tests.
3. docs/evaluator-prerequisites.md — operator commands and retained license/provenance boundary linked to this reviewed inventory.

Modify:

4. .dockerignore — admit only the additional evaluator manifest into the existing private build context.
5. containers/harness.Dockerfile — copy/install that manifest with hash verification/no dependencies/binary-only; include evaluator import in the existing dependency image command.
6. .github/workflows/harness.yml — install the same hash-pinned binding and execute the prerequisite script locally twice and in network-isolated Linux image twice, retaining the existing general prerequisites and steps.

Delete none. No production, domain schema or test file changes. PDD execution-status/evidence update to Plan.md after verified execution is excluded from this six-file implementation scope. New source/notice findings that require another file return for approval; no hidden license-vendoring contingency.

## Proposed Exact Code

### requirements-evaluator.txt

```text
webrtcvad-wheels==2.0.14.post1 \
    --hash=sha256:ffbe00c93e2b03ee511c7fad29c4d92ec17cd33bc181c55636334079252b633f \
    --hash=sha256:70176f1a20edb64d55616161361b0f71105a16041b1e205685c8af3f7c8dc727
```

### tools/evaluator_readiness.py

```python
"""Offline executable prerequisites only; no enrollment or quality decisions."""
import base64
import hashlib
import importlib.metadata
import io
import json
import platform
import sys
import wave


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def offline(event, args):
    if event in {"socket.connect", "socket.connect_ex", "socket.getaddrinfo",
                 "socket.gethostbyname", "socket.gethostbyaddr", "socket.sendto"}:
        raise RuntimeError("network denied by prerequisite probe")


sys.addaudithook(offline)

import av
import numpy as np
import webrtcvad
import _webrtcvad


def identity():
    require(sys.implementation.name == "cpython", "CPython required")
    require(sys.version_info[:3] == (3, 13, 17), "CPython 3.13.17 required")
    require(platform.machine().lower() in {"amd64", "x86_64"}, "x64 required")
    require(sys.platform in {"win32", "linux"}, "Windows/Linux required")
    for name, version in {"av": "19.0.2", "numpy": "2.5.4",
                          "webrtcvad-wheels": "2.0.14.post1"}.items():
        require(importlib.metadata.version(name) == version, name + " pin")
    try:
        importlib.metadata.distribution("webrtcvad")
    except importlib.metadata.PackageNotFoundError:
        pass
    else:
        raise RuntimeError("conflicting webrtcvad distribution installed")
    distribution = importlib.metadata.distribution("webrtcvad-wheels")
    requirements = distribution.requires or []
    require(all("extra" in entry and "dev" in entry for entry in requirements),
            "unexpected runtime dependency metadata")
    files = distribution.files
    require(files is not None, "installed RECORD missing")
    hashes = {}
    notices = []
    for item in files:
        path = distribution.locate_file(item)
        if item.hash is not None:
            require(item.hash.mode == "sha256", "unexpected RECORD hash")
            raw = path.read_bytes()
            actual = base64.urlsafe_b64encode(hashlib.sha256(raw).digest())
            require(actual.decode().rstrip("=") == item.hash.value,
                    "installed file integrity mismatch: " + str(item))
        if str(item).lower().endswith("license"):
            notice = path.read_text(encoding="utf-8")
            require("John Wiseman" in notice and "WebRTC project authors" in notice,
                    "wrapper/native copyright notice missing")
            require("Neither the name of Google" in notice,
                    "native BSD conditions missing")
            notices.append(str(item))
        if str(item).endswith("webrtcvad.py") or "_webrtcvad." in str(item):
            hashes[str(item)] = hashlib.sha256(path.read_bytes()).hexdigest()
    require(notices and len(hashes) == 2, "wrapper/native/license inventory")
    require(webrtcvad.__version__ == "2.0.14.post1", "wrapper version")
    require(_webrtcvad.__file__ is not None, "native module unavailable")
    print(json.dumps({"runtime": sys.version, "platform": platform.platform(),
                      "binding": distribution.version, "files_sha256": hashes,
                      "notices": notices, "requires_dist": requirements,
                      "pyav": av.__version__, "ffmpeg": av.library_versions},
                     sort_keys=True))


def decode_resample(payload):
    with av.open(io.BytesIO(payload), mode="r") as source:
        streams = list(source.streams.audio)
        require(len(streams) == 1, "probe has exactly one audio stream")
        resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
        output = []
        for frame in source.decode(streams[0]):
            output.extend(resampler.resample(frame))
        output.extend(resampler.resample(None))
    require(output, "decoder/resampler emitted no samples")
    require(all(frame.sample_rate == 16000 and frame.format.name == "s16"
                and frame.layout.name == "mono" for frame in output),
            "effective resampler format")
    samples = np.concatenate([frame.to_ndarray().reshape(-1) for frame in output])
    require(samples.size >= 320, "complete 20ms frame unavailable")
    return samples.astype("<i2", copy=False).tobytes()


def encoded(format_name, codec):
    payload = io.BytesIO()
    with av.open(payload, mode="w", format=format_name) as target:
        stream = target.add_stream(codec, rate=24000)
        stream.layout = "mono"
        frame = av.AudioFrame.from_ndarray(np.zeros((1, 2400), dtype=np.int16),
                                           format="s16", layout="mono")
        frame.sample_rate = 24000
        for packet in stream.encode(frame):
            target.mux(packet)
        for packet in stream.encode(None):
            target.mux(packet)
    return payload.getvalue()


def smoke():
    wav = io.BytesIO()
    with wave.open(wav, "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(24000)
        target.writeframes(b"\x00\x00" * 2400)
    payloads = {"wav": wav.getvalue(), "mp3": encoded("mp3", "mp3"),
                "m4a": encoded("mp4", "aac")}
    results = {}
    for name, payload in payloads.items():
        pcm = decode_resample(payload)
        require(webrtcvad.valid_rate_and_frame_length(16000, 320),
                "16000Hz/20ms native support")
        vad = webrtcvad.Vad(1)
        decision = vad.is_speech(pcm[:640], 16000)
        require(decision is False, "synthetic silence native invocation")
        results[name] = {"samples": len(pcm) // 2,
                         "sha256": hashlib.sha256(pcm).hexdigest(),
                         "native_boolean": decision}
    return results


def main():
    identity()
    first = smoke()
    require(smoke() == first, "repeatable decoder/resampler/native smoke")
    print(json.dumps(first, sort_keys=True))
    print("evaluator prerequisites ready: offline deterministic smoke only")


if __name__ == "__main__":
    main()
```

### docs/evaluator-prerequisites.md

```markdown
# Enrollment evaluator prerequisites

Use CPython 3.13.17 x64 and the existing developer harness. General setup remains
in developer-setup.md. The additional manifest installs only the reviewed
webrtcvad-wheels 2.0.14.post1 binary; it does not install dev extras or weights.
Supported prerequisite targets are Windows x64 and Linux glibc x86_64.
Do not fall back to a source build, another detector or another wheel hash.

After approval of initial-build Implementation Plan 009, from the repository root:

    .\.venv\Scripts\python.exe -m pip install --no-deps --only-binary=:all: --require-hashes -r requirements-evaluator.txt
    .\.venv\Scripts\python.exe -m pip check
    .\.venv\Scripts\python.exe tools/evaluator_readiness.py
    .\.venv\Scripts\python.exe tools/evaluator_readiness.py

For an already prepared Linux general harness, use its selected Python interpreter:

    python -m pip install --no-deps --only-binary=:all: --require-hashes -r requirements-evaluator.txt
    python -m pip check
    python tools/evaluator_readiness.py
    python tools/evaluator_readiness.py

The existing dependency Dockerfile also installs this manifest. Run the probe
with the existing image and network disabled, mounting only the probe read-only;
exact Windows/Linux command forms and evidence gates are in Implementation Plan009.
No application, database schema, enrollment setting or calibration is created.

Retain the complete installed distribution LICENSE when redistributing the wheel
or a derived image. It contains MIT wrapper and native WebRTC BSD3 notices,
including copyright, conditions, disclaimer and non-endorsement restriction.
PyPI's short MIT label does not replace the native notice.

The source release tree does not include PATENTS/AUTHORS, although native headers
refer to them. The exact reviewed source identity, official upstream notice
references, package/wheel hashes and limits of the evidence are recorded in
docs/.ai/initial-build/009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md.
They are provenance records, not model commercial clearance or patent guarantees.
Keep the packaged LICENSE; report missing or changed notices rather than silently
substituting another distribution. No extra runtime Python dependencies are
declared without the dev extra. Native/system libraries still require actual
successful import and invocation on each supported target.

The probe reports versions, installed-file hashes, FFmpeg library identities and
deterministic synthetic nonvoice results. It denies Python socket operations and
accepts no private recording input. Linux container execution adds network
isolation. No result measures speech quality, language performance, acoustic
threshold correctness, calibration or production readiness. Enrollment remains
subject to its separate reviewed RED/GREEN and calibration milestones.
```

### .dockerignore

```diff
--- a/.dockerignore
+++ b/.dockerignore
@@ -1,4 +1,5 @@
 *
 !requirements-dev.txt
+!requirements-evaluator.txt
 !containers/
 !containers/harness.Dockerfile
```

### containers/harness.Dockerfile

```diff
--- a/containers/harness.Dockerfile
+++ b/containers/harness.Dockerfile
@@ -1,5 +1,7 @@
 FROM python:3.13.17-slim-trixie
 WORKDIR /workspace
 COPY requirements-dev.txt /tmp/requirements-dev.txt
+COPY requirements-evaluator.txt /tmp/requirements-evaluator.txt
 RUN python -m pip install --no-cache-dir -r /tmp/requirements-dev.txt
-CMD ["python", "-c", "import fastapi,uvicorn,pytest,httpx,psycopg,numpy,av,playwright; print('dependency image ready')"]
+RUN python -m pip install --no-cache-dir --no-deps --only-binary=:all: --require-hashes -r /tmp/requirements-evaluator.txt
+CMD ["python", "-c", "import fastapi,uvicorn,pytest,httpx,psycopg,numpy,av,playwright,webrtcvad,_webrtcvad; print('dependency image ready')"]
```

### .github/workflows/harness.yml

```diff
--- a/.github/workflows/harness.yml
+++ b/.github/workflows/harness.yml
@@ -15,8 +15,13 @@
       - name: Install Python prerequisites
         run: |
           python -m pip install -r requirements-dev.txt
+          python -m pip install --no-deps --only-binary=:all: --require-hashes -r requirements-evaluator.txt
           python -m pip check
           python -m playwright install --with-deps chromium
+      - name: Verify evaluator prerequisites twice
+        run: |
+          python tools/evaluator_readiness.py
+          python tools/evaluator_readiness.py
       - name: Install selected Compose version in isolated CLI configuration
         run: |
           mkdir -p "$RUNNER_TEMP/vn-docker/cli-plugins"
@@ -37,6 +42,10 @@
         run: |
           docker build -f containers/harness.Dockerfile -t vn-harness:foundation .
           docker run --rm vn-harness:foundation
+      - name: Verify evaluator in network-isolated Linux image twice
+        run: |
+          docker run --rm --network none --mount "type=bind,source=$PWD/tools/evaluator_readiness.py,target=/tmp/evaluator_readiness.py,readonly" vn-harness:foundation python /tmp/evaluator_readiness.py
+          docker run --rm --network none --mount "type=bind,source=$PWD/tools/evaluator_readiness.py,target=/tmp/evaluator_readiness.py,readonly" vn-harness:foundation python /tmp/evaluator_readiness.py
       - name: Verify isolated prerequisites twice
         run: python tools/readiness.py
       - name: Record resolved dependency versions
```

## Execution Steps and Verification

All following executable results are **Expected / Predicted — Not Yet Verified**. Execute only after this exact artifact receives human approval. Do not commit, push, open a PR, publish CI changes or dispatch a remote workflow merely to obtain evidence. The existing local Linux dependency container supplies Linux evidence without publication. If unavailable, record Waiting for the specifically named user-supplied approved Linux execution context; neither approve a platform claim nor add compilers/paid resources.

1. Before applying changes, use `.venv/Scripts/python.exe` explicitly. Record `git status --short`, `git diff --check`, current file hashes and actual interpreter identity. Compare all eighteen 005 production blocks, four 008 production blocks, 004 test and 007 test with their exact saved authorities, normalizing CRLF/LF only. Compare the nine original foundation files against their approved 001 blocks. Stop on unexplained drift; record it rather than silently changing it. Save the resulting byte hashes in a temporary evidence manifest outside the checkout. This gives a before/after preservation gate; the three exact harness changes above are its sole foundation exceptions after application.
2. Record bounded read-only diagnostics `docker context show`, `docker version`, `docker compose version`, `docker info --format '{{.ServerVersion}}'`. Require expected desktop-linux, client/server29.3.1, Compose5.6.0 for this Windows context. Bound each process to15seconds; terminate only its diagnostic PID on timeout. Do not start, stop or restart pre-existing user Docker. Missing pipe/access discrepancy uses only the contingency below; actual server output is necessary. A running process or host log is insufficient evidence.
3. Before dependency installation, run the existing general readiness and both full regression commands below on the unmodified baseline. The readiness script already runs twice and removes only its own unique resources. Each pytest run must pass all57cases. A baseline failure is surfaced to the human for disposition before approval/execution proceeds; it is not silently waived or assigned a cause. Baseline checks were not run during this planning task because the task forbids test execution/package acquisition.

```powershell
.\.venv\Scripts\python.exe -c "import sys; assert sys.version_info[:3] == (3,13,17); print(sys.executable, sys.version)"
.\.venv\Scripts\python.exe tools/readiness.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
```

4. Apply exactly the six reviewed files/diffs. Install only the separate evaluator in the existing approved environment, inspect verbose installation output to record the selected wheel filename/hash URL, require no source build or extra dependency, and run these commands separately, preserving real output/exit codes. Do not use `--upgrade`, source-build flags, alternate indexes or dev extras. Stop if wheel identity/hash, architecture, dependency metadata, notice or installed-file verification differs.

```powershell
.\.venv\Scripts\python.exe -m pip install --verbose --no-deps --only-binary=:all: --require-hashes -r requirements-evaluator.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe tools/evaluator_readiness.py
.\.venv\Scripts\python.exe tools/evaluator_readiness.py
.\.venv\Scripts\python.exe -m pip freeze
docker build -f containers/harness.Dockerfile -t vn-harness:foundation .
docker image inspect vn-harness:foundation --format '{{.Id}} {{.Architecture}} {{.Os}}'
docker run --rm --network none vn-harness:foundation
docker run --rm --network none --mount "type=bind,source=$PWD/tools/evaluator_readiness.py,target=/tmp/evaluator_readiness.py,readonly" vn-harness:foundation python /tmp/evaluator_readiness.py
docker run --rm --network none --mount "type=bind,source=$PWD/tools/evaluator_readiness.py,target=/tmp/evaluator_readiness.py,readonly" vn-harness:foundation python /tmp/evaluator_readiness.py
.\.venv\Scripts\python.exe tools/readiness.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
git diff --check
git status --short
```

Docker runs use the existing local Linux engine, disposable `--rm` containers and no persistent volumes. The script mount is read-only and contains no private audio. Save each emitted runtime/wrapper/native/decoder identity and decoded PCM hash as actual evidence. Within each platform the two separate script invocations must yield identical binding/decoder identities and per-format samples/hashes/decisions; platform/version descriptive strings need not equal Windows versus Linux. Synthetic zero frames are never positive speech ground truth. No full regression suite inside the dependency-only Linux container is proposed.

5. Repeat exact-content/hash preservation checks from step1 after verification. All22production files and both test files must remain unchanged; all original foundation files except the three reviewed diffs remain unchanged. The new manifest/script/doc must match the three complete blocks above. Inspect installed distribution files and its complete LICENSE from the actual environment, report contents inventory, wrapper/native hashes, conditional metadata and platform native-library loading results. Do not assert absent supplemental files were installed. The offline smoke and Linux `--network none` runs must pass with no downloaded assets or external service. All commands must pass; baseline failures never become acceptable by omission.
6. Record actual commands, trimmed output, wheel hashes, image identity, per-platform runtime evidence, preservation results and cleanup in Plan.md execution evidence, then update only milestone9 Execution Status if every criterion passes. Stop before Enrollment RED. Temporary evidence files are removed after their content is recorded; all script bytes/buffers are in memory. No user Docker lifecycle change and no remaining executor-created process/container.

## Acceptance / Completion Criteria

- Installed reviewed cp313 Windows x64 wheel and Linux x86_64 image wheel are hash-verified exact2.0.14.post1 binaries; no compiler, source build, extra runtime dependency or external asset acquired.
- Actual complete installed license/native/system dependency inventory matches the reviewed boundaries; wrapper/native integrity and provenance identity are recorded. No impermissible/incompatible or unexplained artifact is accepted.
- On CPython3.13.17 Windows and Linux, the real pinned PyAV decoder/resampler processes WAV/MP3/M4A to16000Hz mono s16 and invokes the real native GMM detector on640byte20ms nonvoice frames, deterministically in repeated runs. Linux network-isolated execution and Python network-denial probe pass.
- Existing general readiness passes; both unmodified-baseline and post-change regression runs pass57/57 twice without cleaning between runs. Exact22production/2test preservation and unaffected six foundation files are proven; three harness diffs/new files match this plan.
- Only these six files plus PDD bookkeeping change. No policy/classification implementation, production symbol/schema/test, private recording, calibration or model download is introduced. Evidence demonstrates the missing executable prerequisite is available for Enrollment RED; it does not claim any Enrollment finding/threshold, quality acceptance or enablement.

## Planning-Time Dry Run

Not performed: the active planning instruction explicitly prohibits package/model acquisition, asset downloads, tests and runtime/Docker changes. A disposable-copy full verification would require acquiring/installing this currently absent binding and running the decoder/VAD/tests. Therefore no runtime/readiness claim is made. Static extraction, syntax/diff checks may be run in a temporary location only; they do not satisfy milestone criteria. Actual baseline and post-change execution remain mandatory after approval; an observed baseline failure requires human disposition, not a criteria waiver. No package archive/wheel was downloaded to manufacture planning evidence.

Read-only research commands actually executed: official PyPI JSON selected version/requires_python/requires_dist and exact two-wheel/sdist filename,size,SHA256 fields; official GitHub recursive release-tree metadata selected LICENSE/PATENTS/AUTHORS/setup.py/webrtcvad.py/native-source identities; immutable raw setup/wrapper/native/license/manifest files were read; official PyPI provenance subject/publisher fields were decoded; official upstream WebRTC PATENTS/AUTHORS references were read. Trimmed results: version2.0.14.post1; Python>=3.10; only dev-extra requirements(unittest2,psutil); source726a8c72ce8b33b2df7ecd292372690fea2bad0c; LICENSE present, PATENTS/AUTHORS absent in binding tree; two subjects match the table. Initial restricted network metadata calls failed DNS; subsequent read-only approved network context succeeded. No runtime failure or cause was inferred from those transport failures.

Static planning check actually executed, not milestone evidence: extract the six named proposed file blocks; `ast.parse(body)` for the Python script; copy only each of the three existing diff targets to a disposable `vn009-static-` temporary directory, normalize CRLF to LF there and run `git apply --check` for each extracted exact diff. No package or runtime probe executed. Output:

```text
AST OK tools/evaluator_readiness.py
.dockerignore 0
containers/harness.Dockerfile 0
.github/workflows/harness.yml 0
temporary static-check directory removed
```

The first restricted-context attempt encountered temporary-directory access denial; a host-context repeat successfully cleaned its own disposable copy. A subsequent initial patch check against CRLF byte copies failed because the displayed patch uses LF; normalized disposable copies passed all three. Execution must apply the reviewed text while preserving the repository's normal line-ending policy. These are tooling/static findings, not baseline test failures or evidence of package readiness.

## Risks

Wheel compatibility is currently a metadata inference until actual imports/native calls pass on both target platforms. Wheel content/license inventory is not yet inspected; unexpected payload or missing notices stops execution. The binding's absent PATENTS/AUTHORS references are explicitly disclosed; current upstream supplemental references do not reconstruct historical provenance or provide a legal opinion. RECORD hashes detect local alteration relative to installed RECORD, while pip's pinned wheel SHA256 establishes download identity; neither alone proves absence of malicious code. Source inspection supports the no external asset design, complemented by actual offline invocation.

Audio codec/encoder support may differ despite the existing pins; a failing encode/decode/resample probe stops for review, with no codec fallback or new package. These synthetic smoke outputs establish executable availability only, never threshold logic/calibration/language quality. Auth/ownership comparisons are unchanged; no new identity/role/ownership check is introduced. Logs contain only public tooling identity and synthetic hashes, never private audio or policy settings. Unrelated pre-existing working-tree changes must survive every check.

## Pre-authorized Contingencies

Only diagnostic-context contingency: observable trigger is a missing/denied `dockerDesktopLinuxEngine` named pipe in the restricted context while the same pre-existing user engine is available to its ordinary host context. Exact files changed: none. Exact action: rerun the same four read-only diagnostics and same approved verification commands in that successful host context; bound each diagnostic to15seconds and the entire observation/handoff interval to120seconds. Preserve partial output and record the context deviation. Do not start/stop/restart Docker, change contexts/settings, install tools or touch any other container. If actual readiness is not established within the bound, stop and record Waiting for user-provided working engine/context. No alternate wheel, compiler, dependency, codec, test or criterion contingency.

## Rollback / Recovery

If execution fails, preserve the real failure evidence and do not mark Complete. Reverse only the three exact diff hunks, remove only the three new files if their creation belongs to this approved execution, and uninstall only the newly installed webrtcvad-wheels from this environment if it was absent before execution. Preserve all unrelated changes and pre-existing Docker/resources. Do not reset/clean the checkout or remove shared images; a rebuilt existing image tag is recorded as an execution side effect, not evidence of application deployment. Any repair beyond exact approved changes returns to planning.

## Exact-Code and Authority Review

| File | Complete content/diff; no placeholder | Change/settings trace |
| --- | --- | --- |
| requirements-evaluator.txt | Complete three-line manifest | Item1; selected release/platform/hash decision and PyPI table |
| tools/evaluator_readiness.py | Complete executable script | Item2; offline/identity/RECORD/decoder/native prerequisite decision; no domain settings |
| docs/evaluator-prerequisites.md | Complete operator document | Item3; approved runtime, separate install and notice/inventory/evidence boundary |
| .dockerignore | Complete one-line-addition diff | Item4; existing build-context privacy plus exact new manifest |
| containers/harness.Dockerfile | Complete two-additions/one-replacement diff | Item5; unchanged image/general pins; exact hash-only binary installation/import |
| .github/workflows/harness.yml | Complete all-changed-lines diff | Item6; existing runner/actions retained; exact install plus repeated local/network-isolated smoke |

No new normative identifier family or reused requirement/contract labels is introduced. The selected distribution is a technical prerequisite under the approved WebRTC GMM policy, not a new product-policy decision. Every new dependency/flag/configuration setting is traced to the explicit binding decisions above. No HTML template comments or partial executable replacement appear.

## Explicitly Out of Scope

Enrollment/acoustic algorithms, downmix/aggregation policy, threshold/configuration/validation implementation, finding classification, warning override/reassessment state, domain fixtures/tests, DBschema, production stubs/adapters, changes to delivered ownership/auth/consent, model/corpus/private recording acquisition, calibration, positive speech ground truth, patent/model commercial clearance, production enablement, new compilers, paid resources, CI publication, commits/pushes/PRs and next milestone execution.

## Human Review

Status: Approved by avinash2196 on 2026-10-25 (recorded 2026-10-25T21:43:58Z), in response to review of this exact Enrollment Evaluator Prerequisites FOUNDATION plan.

Execution status: Complete — executed the exact six reviewed files on 2026-10-25. Windows and Linux CPython3.13.17 binary-only/hash-required installs and repeated offline decoder/resampler/native smoke passed; actual installed LICENSE/RECORD/native inventory inspected. Baseline combined57/57 passes127.02s/125.87s; post-change57/57 passes149.73s/103.79s; both general-readiness invocations passed their two internal checks. Exact22production/2tests/6unaffectedfoundation and six009blocks/diffs verified,24production/test byte hashes recovered against actual predecessor evidence. The newly captured temporary hash manifest disappeared between isolated execution contexts; no unavailable direct byte-before/after comparison is claimed. Named-pipe denial used approved host contingency; incidental helper encoding/hunk-offset issues were corrected without changing reviewed content or retrying a failed runtime check. Plan.md records commands, actual outputs/hashes, license/provenance limits, evidence recovery and complete owned-resource cleanup. User Docker remains running. No Enrollment RED, next milestone, commit, push or CI publication.
