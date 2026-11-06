# Implementation Plan — Voice Enrollment RED

## Milestone and authorization

initial-build milestone 10; type RED, as recorded in the approved revised 26-milestone Plan. This document proposes exactly two test files; it applies neither file and authorizes no GREEN, dependency/configuration change, model acquisition or enablement.

## Authoritative References

Paths below are repository relative; work-item references are under docs/.ai/initial-build.

| Read reference | Authority / disposition |
| --- | --- |
| requirements.md | Approved Q11 revision by avinash2196, recorded 2026-10-25T21:07:15Z; FR-010–013, AC-ENR-001 and Q5–Q11 apply. |
| Plan.md | Revised Plan approved 2026-10-25T21:13:12Z; milestone 9 Complete, milestone 10 Pending, milestone 11/12 Pending. Execution evidence is current; historical initial-state prose is not current runtime evidence. |
| contract/API-Contract.md | Baseline approved 2026-10-24, Q11 amendment approved 2026-10-25T21:30:20Z; milestone 8 Complete. Entities, Enrollment, Artifacts, Configuration, Internal interfaces and common rules govern these tests. |
| Enrollment-Quality-Policy-Proposal.md | Approved 2026-10-25T21:03:55Z; complete deterministic measurement, unknown, aggregation and warning rules; human calibration remains milestone 12. |
| 001_Implementation_Plan_Foundation.md | Approved/executed; pinned Python/tooling, real isolated PostgreSQL, loopback resources. |
| 002_Implementation_Plan_Model_Feasibility.md; model-eval/approved.md | Approved/executed assessment and investigation/protocol decision only; no selected runtime, duration limits, production model, commercial clearance or measured quality. |
| 003_Implementation_Plan_Persistence_RED.md; 004_Implementation_Plan_Persistence_RED_Recovery.md | Approved original/stopped history and approved successful recovery; existing 33 persistence tests, fixtures, interfaces and diagnostic helper carried forward. |
| 005_Implementation_Plan_Persistence_GREEN.md; 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved exact eighteen files and successful verification resume; owner-separated databases/credentials/roots, canonical identity and live grant/fence rules. |
| 007_Implementation_Plan_Authentication_Consent_RED.md; 008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved/executed; exact 24 tests and four delivered files; Auth verification and Consent owner-validation seams retained. |
| 009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved 2026-10-25T21:43:58Z and executed Complete; exact binding, native/offline Windows/Linux probes, repeatability and preservation evidence. |
| voice_narration_PDD_requirements.md | Read-only nonconflicting baseline P0 context, subordinate to approved work-item revisions. |
| tests/test_persistence.py; tests/test_authentication_consent.py; voice_narration/voices/persistence.py; voice_narration/artifacts/persistence.py; voice_narration/ai/persistence.py; voice_narration/auth/application.py; voice_narration/consent/application.py; voice_narration/_http.py; tools/evaluator_readiness.py; requirements-dev.txt; requirements-evaluator.txt; pytest.ini | Inspected current implementation/tooling facts, not additional product authority. |
| Installed plugin commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/testing/SKILL.md; skills/security/SKILL.md; skills/python-fastapi/SKILL.md; skills/requirements-analysis/SKILL.md | Process/domain guidance read under C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0; no product authority. |

No workspace AGENTS.md or product-level docs/requirements.md was found. Existing uncommitted files shown by git status are preserved. No approved unexecuted milestone-10 plan exists; 010 is the next number.

## Current state, predecessor evidence and carried-forward decisions

009 and Plan execution evidence record installed webrtcvad-wheels 2.0.14.post1, repeated real decoder/resampler/native calls offline on Windows/Linux CPython 3.13.17, baseline 57/57 twice (127.02s,125.87s) and post-change 57/57 twice (149.73s,103.79s), successful general readiness and cleanup. These are recorded actual predecessor results, not runs performed during this planning task. Exact 22 production files, two test files and six unaffected foundation files were preserved; 009 discloses the lost transient pre/post manifest and recovered authority comparisons instead of claiming an unavailable byte comparison.

Current source contains persistence plus Auth/Consent applications. It has no voices/quality.py, voices/application.py, artifacts/application.py or ai/enrollment.py. Absence of these intended behavior symbols is predicted RED, not a prerequisite failure. Existing fixtures already supply eight durable owner stores with distinct credentials and roots; Worker remains orchestration without an independent durable private library. Nine domain owners remain unchanged.

Carry forward all existing pins, command-only `-p no:anyio`, existing real PostgreSQL 18.6 fixtures, random loopback ports/projects, exact UUID/role rules and Auth/Consent signatures. No dependency/version/framework/plugin/configuration/build/schema change is proposed. Use only stdlib and installed av/NumPy/WebRTC VAD/pytest/HTTPX. Synthetic test signals contain no natural speech or private recordings. They test deterministic algorithm correctness and interaction, never natural positive speech, Hindi/English calibration, speaker similarity, model quality or commercial readiness.

## Files in scope and ordered proposed changes

Create only:

1. tests/test_enrollment_quality.py — independently named audio tests with independent decoded PCM/native-VAD oracle, original/channel/partial-frame/stream checks, six exact findings and policy boundary checks.
2. tests/test_voice_enrollment.py — independently named real-HTTP/SQL tests using delivered Auth/Consent and owner repositories, real Artifact/Voices/AI boundaries, real acoustic assessment, admission/readiness/override/provenance/profile/material/ownership checks.

Modify/delete no existing executable file. Execution-only Plan.md status/evidence bookkeeping is outside this file limit; do not edit Plan during planning. Complete final content for each created file follows. Test-local helpers/collaborators are inside those files, not new shared infrastructure or conftest.

## Interface choices submitted for review

These missing internal authoring signatures are proposed here for review; they are not public endpoints or RED scaffolding:

- voices.quality.decode(data:bytes, format:str) returns a mapping with `channels` (float64 planar original-scale PCM), `sample_rate_hz`, `stream_index`, `duration_seconds` (Decimal), and `analysis_channels` (separately resampled float64 planar 16kHz). `assess(samples, *, policy, duration_bounds)` returns the six ordered public Finding dictionaries. `validate_policy(policy)` returns an equal validated policy or raises existing PersistenceError INVALID_CONFIGURATION. Actual assessment performs native VAD itself; no labels/findings argument exists.
- artifacts.application.create_app(repository, authenticate, validate_consent, capability, settings, clock) keyword-only: ASGI app. `state.enrollment_samples(account, consent_id, ids)` returns authorized immutable sample bytes/selected metadata at the Artifact boundary; `state.effective_settings()` reports actual upload/link limits. `state.close()` closes only app-owned resources. The supplied repository is Artifact-only.
- ai.enrollment.create_adapter(repository, validate_consent, artifacts, capability, condition, clock) keyword-only: returns an adapter with `enroll(account, profile, samples)` and `material_kinds(account, profile_id)`. It persists only capability-needed model materials in its own AI repository. `condition(model, samples, required_materials)` is the explicit test collaborator; it returns distinguishable synthetic bytes for each requested kind and records its actual arguments. It never supplies Quality, state or safety decisions.
- voices.application.create_app(repository, authenticate, validate_consent, artifacts, enrollment, capability, policy_snapshot, calibration, clock) keyword-only: ASGI app. `state.run_pending(profile_id)` is a deterministic worker scheduling seam: execute queued assessment/conditioning work, recording the same durable states an asynchronous worker would. `state.transition_history(profile_id)` returns persisted state names; `state.assessment_provenance(profile_id, assessment_id)` returns private revision/evaluator/calibration/stream-index metadata. These are trusted test diagnostics, never public routes. `state.close()` closes only app-owned resources.

Artifact receives no Voices/AI credentials; Voices receives only its own repository plus callable boundaries; AI receives only its own repository. Test orchestration may hold all fixtures, production owners may not. Auth token verification and Consent.validate_owner_consent are actual delivered callables. Test-local catalog exposes `capability(model)` and `calibration(policy, revision)`; its synthetic evidence explicitly says test-only and binds the actual installed evaluator identity/hashes plus exact settings. Missing/mismatched entries must fail. Its fixture model UUID/version, duration1..12 seconds and configured limits are explicit test values, never approved Chatterbox bounds or production defaults. No fabricated public deployment example or real user enablement is created. Production catalog/evidence acquisition and transport wiring remain later work.

No material product decision is left unresolved for these deterministic tests: real model limits/runtime and human calibration outcomes remain unavailable and are replaced only at the explicitly reviewed test boundary. They remain mandatory gates for actual user enrollment. Full Configuration administrator GET/PUT/CAS transport belongs its later owning integration/policy work; these tests cover Q11 subsection validation and enrollment applicability at the callable boundary only.

## Exact proposed code

### tests/test_enrollment_quality.py

```python
"""Synthetic nonvoice PCM; actual decoder and native VAD, never speech ground truth."""
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_EVEN
import hashlib
import importlib
import io
import math
from pathlib import Path
import struct
import wave

import av
import numpy as np
import pytest
import webrtcvad
import _webrtcvad


CHECKS = ("duration", "clipping", "silence", "noise", "level", "speech_presence")
MODEL = {"model_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "version": "test-only-v1"}


def evaluator_identity():
    files = (Path(webrtcvad.__file__), Path(_webrtcvad.__file__))
    return "test-only-installed:" + ":".join(hashlib.sha256(p.read_bytes()).hexdigest()
                                               for p in files)


def candidate_policy():
    return {"policy_id": "enrollment-acoustics-v1", "calibration_ref": "test-only-analytic-v1",
            "vad": {"implementation": "webrtc-gmm", "artifact_ref": evaluator_identity(),
                    "sample_rate_hz": 16000, "frame_ms": 20, "mode": 1},
            "clipping": {"peak_abs": 0.999, "max_fraction": 0.001},
            "silence": {"frame_rms_dbfs": -50, "max_fraction": 0.60},
            "noise": {"min_snr_db": 15, "min_speech_seconds": 0.30,
                      "min_nonspeech_seconds": 0.30},
            "level": {"min_speech_rms_dbfs": -35, "max_speech_rms_dbfs": -10},
            "speech_presence": {"min_fraction": 0.20, "min_seconds": 1.00}}


def wav_bytes(channels, rate=16000):
    values = np.asarray(channels, dtype=np.float64)
    pcm = np.clip(np.rint(values.T * 32768), -32768, 32767).astype("<i2")
    output = io.BytesIO()
    with wave.open(output, "wb") as target:
        target.setnchannels(values.shape[0])
        target.setsampwidth(2)
        target.setframerate(rate)
        target.writeframes(pcm.tobytes())
    return output.getvalue()


def codec_bytes(format_name, codec, channels, rate=24000, default_index=None):
    output = io.BytesIO()
    with av.open(output, "w", format=format_name) as target:
        streams = []
        for index, values in enumerate(channels):
            stream = target.add_stream(codec, rate=rate)
            stream.layout = "mono"
            if default_index is not None:
                stream.disposition = 1 if index == default_index else 0
            streams.append((stream, values))
        for stream, values in streams:
            frame = av.AudioFrame.from_ndarray(np.asarray([values], dtype=np.int16),
                                               format="s16", layout="mono")
            frame.sample_rate = rate
            for packet in stream.encode(frame):
                target.mux(packet)
            for packet in stream.encode(None):
                target.mux(packet)
    return output.getvalue()


def independent_decode(data):
    # Container selection is independent of the implementation under test.
    candidates = []
    with av.open(io.BytesIO(data)) as source:
        for stream in source.streams.audio:
            candidates.append((stream.index, bool(int(stream.disposition) & 1)))
    defaults = [index for index, default in candidates if default]
    order = defaults if len(defaults) == 1 else [index for index, _ in candidates]
    for index in sorted(order):
        try:
            with av.open(io.BytesIO(data)) as source:
                stream = source.streams[index]
                frames = list(source.decode(stream))
                if not frames:
                    continue
                rate = frames[0].sample_rate
                channels = len(frames[0].layout.channels)
                originals = []
                resampled = [[] for _ in range(channels)]
                samplers = [av.AudioResampler(format="dblp", layout="mono", rate=16000)
                            for _ in range(channels)]
                for frame in frames:
                    converted = av.AudioResampler(format="dblp", layout=frame.layout,
                                                  rate=rate).resample(frame)
                    for planar in converted:
                        values = planar.to_ndarray().astype(np.float64)
                        originals.append(values)
                        for channel in range(channels):
                            mono = av.AudioFrame.from_ndarray(values[channel:channel + 1],
                                                             format="dblp", layout="mono")
                            mono.sample_rate = rate
                            resampled[channel].extend(samplers[channel].resample(mono))
                for channel in range(channels):
                    resampled[channel].extend(samplers[channel].resample(None))
                original = np.concatenate(originals, axis=1)
                analysis = np.stack([np.concatenate([f.to_ndarray().reshape(-1) for f in fs])
                                     for fs in resampled])
                return {"channels": original, "analysis_channels": analysis,
                        "sample_rate_hz": rate, "stream_index": index,
                        "duration_seconds": Decimal(original.shape[1]) / Decimal(rate)}
        except av.error.FFmpegError:
            continue
    raise AssertionError("Synthetic fixture must have a decodable selected stream")


def rounded(value):
    if value is None:
        return None
    return format(Decimal(str(value)).quantize(Decimal("0.000001"),
                                             rounding=ROUND_HALF_EVEN), "f")


def native_features(decoded, policy):
    original = decoded["channels"]
    analysis = decoded["analysis_channels"]
    masks = []
    powers = []
    lengths = []
    for start in range(0, analysis.shape[1], 320):
        block = analysis[:, start:start + 320]
        lengths.append(block.shape[1])
        powers.append(np.mean(block * block, axis=1))
    powers = np.asarray(powers).T
    lengths = np.asarray(lengths)
    for channel in analysis:
        detector = webrtcvad.Vad(policy["vad"]["mode"])
        decisions = []
        for start in range(0, channel.size, 320):
            block = channel[start:start + 320]
            pcm = np.clip(np.rint(block * 32768), -32768, 32767).astype("<i2")
            packet = pcm.tobytes() + b"\0\0" * (320 - pcm.size)
            decisions.append(detector.is_speech(packet, 16000))
        masks.append(decisions)
    masks = np.asarray(masks, dtype=bool)
    speech_count = int(lengths[np.any(masks, axis=0)].sum())
    quiet = np.all(powers <= 10 ** (policy["silence"]["frame_rms_dbfs"] / 10), axis=0)
    snrs = []
    levels = []
    for channel in range(analysis.shape[0]):
        speech = masks[channel]
        sc = int(lengths[speech].sum())
        nc = int(lengths[~speech].sum())
        s = float(np.dot(powers[channel, speech], lengths[speech]) / sc) if sc else 0
        n = float(np.dot(powers[channel, ~speech], lengths[~speech]) / nc) if nc else 0
        if sc:
            levels.append(10 * math.log10(s) if s > 0 else None)
            valid = (sc / 16000 >= policy["noise"]["min_speech_seconds"] and
                     nc / 16000 >= policy["noise"]["min_nonspeech_seconds"] and n > 0 and s > n)
            snrs.append(10 * math.log10((s - n) / n) if valid else None)
    return {"duration": float(decoded["duration_seconds"]),
            "clipping": max(float(np.mean(np.abs(c) >= policy["clipping"]["peak_abs"]))
                            for c in original),
            "silence": float(lengths[quiet].sum() / lengths.sum()),
            "speech_presence": speech_count / int(lengths.sum()),
            "speech_seconds": speech_count / 16000,
            "snrs": snrs, "levels": levels}


def expected_findings(decoded_samples, policy, bounds):
    rows = [native_features(d, policy) for d in decoded_samples]
    valid_snrs = [v for row in rows for v in row["snrs"] if v is not None]
    valid_levels = [v for row in rows for v in row["levels"] if v is not None]
    measured = [min(r["duration"] for r in rows), max(r["clipping"] for r in rows),
                max(r["silence"] for r in rows), min(valid_snrs) if valid_snrs else None,
                min(valid_levels) if valid_levels else None,
                min(r["speech_presence"] for r in rows)]
    noise_unknown = any(not r["snrs"] or any(v is None for v in r["snrs"]) for r in rows)
    level_unknown = any(not r["levels"] or any(v is None for v in r["levels"]) for r in rows)
    flags = [any(not float(bounds[0]) <= r["duration"] <= float(bounds[1]) for r in rows),
             measured[1] > policy["clipping"]["max_fraction"],
             measured[2] > policy["silence"]["max_fraction"],
             noise_unknown or measured[3] is None or measured[3] < policy["noise"]["min_snr_db"],
             level_unknown or any(v < policy["level"]["min_speech_rms_dbfs"] or
                                  v > policy["level"]["max_speech_rms_dbfs"] for v in valid_levels),
             any(r["speech_presence"] < policy["speech_presence"]["min_fraction"] or
                 r["speech_seconds"] < policy["speech_presence"]["min_seconds"] for r in rows)]
    if noise_unknown:
        measured[3] = None
    if level_unknown:
        measured[4] = None
    return [(check, "failure" if i == 0 and flags[i] else "warning" if flags[i] else "pass",
             rounded(measured[i]), ("seconds", "ratio", "ratio", "dB", "dBFS", "ratio")[i])
            for i, check in enumerate(CHECKS)]


def check_assessment(actual, expected):
    assert len(actual) == 6
    assert [r["check"] for r in actual] == list(CHECKS)
    for result, reference in zip(actual, expected):
        assert set(result) == {"check", "severity", "measured", "unit", "message", "action"}
        assert (result["check"], result["severity"], result["unit"]) == (
            reference[0], reference[1], reference[3])
        if reference[2] is None:
            assert result["measured"] is None
        else:
            assert isinstance(result["measured"], str)
            assert abs(Decimal(result["measured"]) - Decimal(reference[2])) <= Decimal("0.000001")
            assert "e" not in result["measured"].lower()
            assert Decimal(result["measured"]).as_tuple().exponent >= -6
        assert result["message"].strip() and result["action"].strip()


@pytest.fixture
def quality():
    return importlib.import_module("voice_narration.voices.quality")


@pytest.fixture
def decoded_samples():
    policy = candidate_policy()
    n = 80000
    t = np.arange(n) / 16000
    rng = np.random.default_rng(107)
    signals = [np.zeros((1, n)), np.full((1, n), 0.25),
               np.asarray([0.16 * np.sin(2 * np.pi * 190 * t)]),
               rng.normal(0, 0.005, (1, n)),
               np.asarray([0.15 * np.sin(2 * np.pi * 180 * t),
                           -0.15 * np.sin(2 * np.pi * 180 * t)])]
    clipped = np.zeros((1, n))
    clipped[0, :80] = 32767 / 32768
    signals.extend([clipped, np.full((1, 1601), 0.125)])
    mixture = rng.normal(0, 0.002, (1, n))
    mixture[0, 16000:64000] += (0.10 * np.sin(2 * np.pi * 170 * t[16000:64000]) +
                              0.04 * np.sin(2 * np.pi * 510 * t[16000:64000]))
    signals.append(mixture)
    payloads = [(wav_bytes(signal), "wav") for signal in signals]
    payloads.extend([(codec_bytes("mp3", "mp3", [np.zeros(72000, dtype=np.int16)]), "mp3"),
                     (codec_bytes("mp4", "aac", [np.zeros(72000, dtype=np.int16)]), "m4a")])
    # Two streams: one default, then none/multiple defaults. MP4 may set a default;
    # the reference reads the actual encoded flags rather than assuming muxer flags.
    for default in (1, None):
        payloads.append((codec_bytes("mp4", "aac", [np.zeros(48000, dtype=np.int16),
                         np.full(72000, 2048, dtype=np.int16)], default_index=default), "m4a"))
    references = [independent_decode(data) for data, fmt in payloads]
    expectations = [expected_findings([reference], policy, ("0.01", "12"))
                    for reference in references]
    # Fixture codec/stream/native oracle failures must surface before missing behavior.
    quality = importlib.import_module("voice_narration.voices.quality")
    decoded = []
    for (data, fmt), reference, expected in zip(payloads, references, expectations):
        original_hash = hashlib.sha256(data).hexdigest()
        actual = quality.decode(data, fmt)
        assert actual["sample_rate_hz"] == reference["sample_rate_hz"]
        assert actual["stream_index"] == reference["stream_index"]
        assert actual["duration_seconds"] == reference["duration_seconds"]
        np.testing.assert_allclose(actual["channels"], reference["channels"], rtol=0, atol=1e-12)
        np.testing.assert_allclose(actual["analysis_channels"], reference["analysis_channels"],
                                   rtol=0, atol=1e-12)
        assert hashlib.sha256(data).hexdigest() == original_hash
        check_assessment(quality.assess([actual], policy=policy,
                                       duration_bounds=("0.01", "12")), expected)
        decoded.append(actual)
    return decoded


@pytest.mark.audio
def test_decoded_formats_channels_partial_frames_and_streams(decoded_samples):
    assert len(decoded_samples) == 12


@pytest.mark.audio
def test_every_sample_aggregation(quality, decoded_samples):
    policy = candidate_policy()
    decoded = decoded_samples
    for group in ([decoded[0], decoded[2]], [decoded[4], decoded[6], decoded[-1]]):
        check_assessment(quality.assess(group, policy=policy, duration_bounds=("0.01", "12")),
                         expected_findings(group, policy, ("0.01", "12")))
@pytest.mark.audio
def test_clipping_and_duration_edges(quality, decoded_samples):
    policy = candidate_policy()
    decoded = decoded_samples
    # Exact ratio edges and partial-frame weighting: equality passes, strict excess warns.
    for fraction in (0.001, 0.000999, 0.001001):
        edge = deepcopy(policy)
        edge["clipping"]["max_fraction"] = fraction
        check_assessment(quality.assess([decoded[5]], policy=edge, duration_bounds=("1", "12")),
                         expected_findings([decoded[5]], edge, ("1", "12")))
    for lower, upper in (("5", "5"), ("5.000001", "6"), ("1", "4.999999")):
        check_assessment(quality.assess([decoded[0]], policy=policy, duration_bounds=(lower, upper)),
                         expected_findings([decoded[0]], policy, (lower, upper)))
@pytest.mark.audio
def test_acoustic_thresholds_and_unknowns(quality, decoded_samples):
    policy = candidate_policy()
    decoded = decoded_samples
    for section, key, values in (("silence", "max_fraction", (1, 0.999999)),
                                ("speech_presence", "min_fraction", (0, 1)),
                                ("noise", "min_speech_seconds", (0.3, 8)),
                                ("noise", "min_nonspeech_seconds", (0.3, 8)),
                                ("level", "min_speech_rms_dbfs", (-90, -15)),
                                ("level", "max_speech_rms_dbfs", (-10, -1))):
        for value in values:
            edge = deepcopy(policy)
            edge[section][key] = value
            check_assessment(quality.assess([decoded[7]], policy=edge, duration_bounds=("1", "12")),
                             expected_findings([decoded[7]], edge, ("1", "12")))


@pytest.mark.audio
def test_real_vad_numeric_level_noise_and_speech_edges(quality):
    policy = candidate_policy()
    samples = []
    for pitch in (110, 170, 230, 310):
        t = np.arange(80000) / 16000
        rng = np.random.default_rng(200 + pitch)
        values = rng.normal(0, 0.0002, (1, t.size))
        window = (t >= 1) & (t < 4)
        values[0, window] += (0.12 * np.sin(2 * np.pi * pitch * t[window]) +
                               0.04 * np.sin(2 * np.pi * 3 * pitch * t[window]))
        samples.append(quality.decode(wav_bytes(values), "wav"))
    # Detector labels are an independent native-computation oracle, not human labels.
    policy["noise"]["min_speech_seconds"] = 0.000001
    policy["noise"]["min_nonspeech_seconds"] = 0.000001
    rows = [native_features(sample, policy) for sample in samples]
    usable = [(sample, row) for sample, row in zip(samples, rows)
              if row["snrs"] and all(v is not None for v in row["snrs"]) and row["levels"]]
    assert usable, "Synthetic fixture lacks native-labelled groups: prerequisite/fixture failure, not RED"
    sample, row = usable[0]
    for section, key, value in (("noise", "min_snr_db", min(row["snrs"])),
                                ("level", "min_speech_rms_dbfs", min(row["levels"])),
                                ("level", "max_speech_rms_dbfs", max(row["levels"])),
                                ("speech_presence", "min_fraction", row["speech_presence"]),
                                ("speech_presence", "min_seconds", row["speech_seconds"])):
        for delta in (-0.000002, 0, 0.000002):
            edge = deepcopy(policy)
            edge["level"] = {"min_speech_rms_dbfs": -120, "max_speech_rms_dbfs": 0}
            edge[section][key] = float(Decimal(str(value)).quantize(Decimal("0.000001")) +
                                       Decimal(str(delta)))
            check_assessment(quality.assess([sample], policy=edge, duration_bounds=("1", "12")),
                             expected_findings([sample], edge, ("1", "12")))
@pytest.mark.audio
def test_policy_validation_and_nonfinite_decoded_audio(quality):
    policy = candidate_policy()
    assert quality.validate_policy(deepcopy(policy)) == policy
    for change in ({}, {"extra": 1}, {"policy_id": "other"}, {"vad": None},
                   {"clipping": {"peak_abs": True, "max_fraction": 0}},
                   {"noise": {"min_snr_db": float("nan"), "min_speech_seconds": 1,
                              "min_nonspeech_seconds": 1}}):
        invalid = deepcopy(policy)
        if not change:
            del invalid["calibration_ref"]
        invalid.update(change)
        with pytest.raises(Exception) as caught:
            quality.validate_policy(invalid)
        assert caught.value.code == "INVALID_CONFIGURATION"
    # RIFF float WAV with nonfinite PCM is decodable but invalid admission input.
    raw = struct.pack("<ff", float("nan"), float("inf"))
    header = b"WAVEfmt " + struct.pack("<IHHIIHH", 16, 3, 1, 16000, 64000, 4, 32)
    data = b"RIFF" + struct.pack("<I", 4 + len(header) - 4 + 8 + len(raw)) + header
    data += b"data" + struct.pack("<I", len(raw)) + raw
    with pytest.raises(Exception) as caught:
        quality.decode(data, "wav")
    assert caught.value.code == "INVALID_AUDIO"
```

### tests/test_voice_enrollment.py

```python
"""Real owner boundaries and measurements; test-only evidence, no model-quality claim."""
from copy import deepcopy
from decimal import Decimal
import hashlib
import importlib
import json
from urllib.parse import urlsplit

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
        if not self.model_ready or model != MODEL:
            fail("MODEL_NOT_READY")
        return deepcopy(self.cap)

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
    def make_voices(repository):
        return voices_factory(repository=repository, authenticate=auth.state.verify_token,
                              validate_consent=consents.state.validate_owner_consent,
                              artifacts=artifacts.state.enrollment_samples, enrollment=adapter,
                              capability=catalog.capability, policy_snapshot=catalog.snapshot,
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
                      "reopen_voices": lambda: make_voices(open_store("voices", grants.authorize))}
            token, _ = verify(system)
            system["token"] = token
            system["consent_record"] = record(system, token)
            yield system
    finally:
        voices.state.close()
        artifacts.state.close()
        auth.state.close()


def upload(system, data=None, fmt="wav", token=None, consent_id=None, expected=201, code=None):
    data = wav_bytes(np.zeros((1, 80000))) if data is None else data
    mime = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
    response = system["media"].post("/artifacts/upload", headers=headers(token or system["token"]),
                                     data={"consent_id": consent_id or system["consent_record"]["consent_id"]},
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
        parts = urlsplit(link["url"])
        content = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
        assert content.status_code == 200 and content.content == data
        assert "inline" in content.headers["content-disposition"]
        assert content.headers["content-type"].split(";")[0] == {
            "wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
        error(s["media"].get(parts.path + "?" + parts.query), 401, "UNAUTHENTICATED")
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
    upload(s, token=other, consent_id=s["consent_record"]["consent_id"], expected=403, code="FORBIDDEN")
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
    parts = urlsplit(response.json()["url"])
    playback = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
    assert playback.status_code == 200 and playback.content == data
    assert independent_decode(playback.content)["stream_index"] == captured["stream_index"]
```

## Contract and requirement coverage

| Approved obligation | Proposed verifying test(s) / explicit limit |
| --- | --- |
| FR-010 permitted WAV/MP3/M4A, bytes/MIME match, decoded duration, size and inclusive bounds | decoded_formats_channels_partial_frames_and_streams; guidance_formats_playback_admission_and_originals. Browser microphone media uses the same backend admission; actual recording controls/UI remain the Plan's browser workflow milestone. |
| FR-011 guidance/playback/re-recording/actionable six findings | guidance_formats_playback_admission_and_originals; obsolete_assessment_rerecording_and_strict_override; all audio tests. Message/action checked as nonblank, not newly prescribed copy. Playback content is fetched through real signed authenticated HTTP. |
| Six findings, IEEE arithmetic, clipping original channels, per-channel analysis, anti-phase support, partial frame real weights, ratios, noise/level nulls | decoded formats fixture; every_sample_aggregation; clipping_and_duration_edges; acoustic_thresholds_and_unknowns; real_vad_numeric_level_noise_and_speech_edges. No mocked finding or VAD label supplied to production. |
| Stream selection, originals, same selected stream for metadata/playback/conditioning | independent decoded stream oracle plus multistream_metadata_playback_and_conditioning checks metadata, assessment, unchanged playback and captured conditioning stream index/original bytes. |
| Hard validation versus override warning, pending and durable states | guidance_formats_playback_admission_and_originals; warning_override_profile_reuse_and_minimal_materials; all_pass_without_override_and_model_minimal_material_selection; evaluator_execution_failure_cannot_be_overridden. |
| Current/repeated/stale acknowledgements and obsolete unfinished reassessment | warning_override_profile_reuse_and_minimal_materials; obsolete_assessment_rerecording_and_strict_override. No rewriting of old caller-observed Quality; retained provenance requested by assessment ID. |
| FR-012 owned profile metadata/reuse, friendly Unicode name, language/model/consent/sample order/status | warning_override_profile_reuse_and_minimal_materials; ownership_reference_validation_and_live_consent_fence; all-pass English case. Durable existing repository is real; no in-memory profile collaborator. |
| FR-013 only model-needed reference/embedding/weight material | parameterized all-pass test checks each material independently in actual AI storage; warning override test checks actual persisted bytes. Conditioning collaborator is interaction-only, no training/quality promise. |
| Q11 closed policy validation, boundaries, missing/invalid applicability | policy_validation_and_nonfinite_decoded_audio; readiness_gates_without_false_pass. Configuration HTTP/CAS/admin transport is not delivered by this layer and remains later integration ownership; no new external behavior asserted for undefined fields. |
| Q11 evaluator runtime failure and active consent safety | evaluator_execution_failure_cannot_be_overridden; ownership_reference_validation_and_live_consent_fence; actual Consent owner fence used. Wider distributed revocation/cleanup events and deployed auth-service transport remain later integration. |
| Q11 provenance/privacy, unrelated delivered operations usable | warning override provenance/log checks; readiness gate Auth/Consent positive operations. No production user enablement is claimed. |

These tests do not replace human calibration: milestone 12 retains every required separate-language/source count, held-out split, reviewer adjudication, Wilson interval, warning/SNR denominator and acceptance criterion in Q11/proposal points 1–6. Model runtime/quality/licensing gates likewise remain later work.

## Verification and Expected / Predicted — Not Yet Verified evidence

Execute only after human approval of this exact artifact. All outcomes in this section are predictions until actual execution. First record git status and file hashes and compare the 22 delivered production files and two existing tests to approved 005/008/004/007 blocks (normalize CRLF/LF only), plus the six exact 009 contents/diffs and unaffected foundation files. Stop on unexplained drift. Existing user Docker must remain running; do not start, stop, restart, reset, change context/settings or replace its processes.

Use .venv/Scripts/python.exe, CPython3.13.17. Run bounded read-only Docker diagnostics individually: `docker context show`, `docker version`, `docker compose version`, `docker info --format '{{.ServerVersion}}'`. Each process has a15second deadline; terminate only that diagnostic PID on timeout. Require actual desktop-linux/server29.3.1/Compose5.6.0 responses, not process/log inference. The dedicated contingency below applies to named-pipe permission discrepancies only.

Run these exact commands separately and retain actual stdout/stderr/exit status; no dependency install, build or lifecycle command is added. readiness.py and pytest fixtures may create/delete only their own uniquely named resources after approval.

```powershell
.\.venv\Scripts\python.exe tools/readiness.py
.\.venv\Scripts\python.exe tools/evaluator_readiness.py
.\.venv\Scripts\python.exe tools/evaluator_readiness.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
```

Both existing suites must pass all57 cases twice without cleanup between invocations. A pre-existing failure is a finding requiring human disposition, never valid enrollment RED. Do not rerun until green, waive a failure, skip, xfail or weaken an assertion. The evaluator/readiness prerequisites must actually pass first; absent intended Enrollment symbols are not prerequisites.

Apply only the two complete test blocks after prerequisites pass. Then:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
git diff --check
git status --short
```

Expected failure class: all new cases fail only at intentionally absent Enrollment domain modules/symbols after their applicable existing prerequisites initialize; quality cases at voices.quality, integration cases first at artifacts.application. Further intended symbols become reachable under GREEN; no claim is made of observing later missing imports today. Missing libraries, invalid fixture/codec/stream manipulation, HTTP startup, database, teardown or unexpected exception is unrelated and stops execution. Existing57 cases remain passing twice after application. Record counts from actual collection, every failure cause, skips/xfails (must be zero), resource cleanup and preserved file comparisons. Do not classify failing synthetic oracle adequacy as intended RED.

## Acceptance / Completion Criteria

- Approved predecessors and actual existing prerequisites pass before new RED runs. Existing57 regressions pass twice before and twice after application without cleaning between runs; every new case is collected and fails only for intentionally absent approved behavior symbols.
- Both exact test files match the reviewed blocks, compile, contain no stubs/production changes and use actual decoded PCM and real approved native VAD for expected and actual acoustic behavior. Independent oracle adequately covers numeric and unknown branches; soundness gaps or fixture failures must return for review, never be recorded as successful RED.
- Two repeated RED invocations show only intended missing-symbol failures after isolated setup; every failure is examined, no skip/xfail, no unrelated failures accepted. Exact counts and actual output are recorded after execution, not inferred solely from static parsing.
- Delivered22production/two existing tests/all prerequisite/configuration files remain unchanged. Only the two new test files plus this milestone's PDD execution bookkeeping change. No actual user enablement, human calibration claim, model/runtime download, dependency/configuration/schema change or user Docker lifecycle action occurs.
- Every executor-owned HTTP thread/socket/temp store/unique Compose project is stopped or removed. Pre-existing Docker and unrelated changes survive. Completion updates only milestone10 execution evidence, and stops before GREEN.

## Planning-time dry run and static review

No disposable-copy runtime dry run or scratch behavior/stub execution was run: the active task explicitly prohibits tests, runtime/Docker execution and package operations during planning. This restriction also excludes execution in a disposable copy. Consequently predicted collection, codec/stream APIs, native-positive synthetic fixture adequacy, HTTP states and all assertions remain unverified. No baseline test failure was observed in this planning task; predecessor results are cited with their limits above. Static syntax and exact-block checks are recorded separately below and never substituted for runtime soundness or milestone evidence. A failed eventual fixture/probe is a planning finding requiring correction and re-review.

Actual static-only check: a standard-library script read this artifact, extracted exactly the two named Python blocks, parsed each with ast.parse, counted test functions and literal parameterizations, checked for Ellipsis placeholders and HTML template comments. It imported/executed neither proposed module nor product/runtime code and created no temporary file. Output before the subsequent durable-reopen-only refinement:

```text
tests/test_enrollment_quality.py AST OK 365 lines 6 test functions 6 predicted cases
tests/test_voice_enrollment.py AST OK 472 lines 8 test functions 15 predicted cases
Exactly two complete code blocks; no executable file applied; no runtime/test execution
```

Static AST predicts21 new cases, not verified pytest collection. The checker emitted a Python ast.Ellipsis deprecation warning; that was a checker API warning, not a proposed-test/runtime failure. Final affected blocks are re-parsed after refinement; final results are reported in the planning handoff. No scratch stub/probe is claimed sound. Runtime soundness remains unverified under the explicit no-runtime planning instruction.

Final actual static-only result after durable reopening refinement, using ast.Constant for the placeholder check:

```text
tests/test_enrollment_quality.py AST OK 365 lines
tests/test_voice_enrollment.py AST OK 484 lines
Final static check: two complete blocks; no placeholders/template comments
```

`git diff --check` exited0, with existing LF/CRLF conversion warnings for .dockerignore, .github/workflows/harness.yml, containers/harness.Dockerfile and001. It does not inspect an untracked artifact's contents, so the separate artifact/block checks above are the evidence for010. No existing file was changed by this planning task.

## Risks, canonical comparisons and explicit exclusions

Identity comparisons introduced by the tested behavior: authenticated Account.user_id against consent.owner_id, sample.owner_id, profile.owner_id and requested owner_id; sample.consent_id against active consent_id; model.model_id, artifact/profile/assessment IDs and grant target IDs against stored IDs. All use the same canonical lowercase UUID validation as delivered authentication/_sql.identity; whitespace/case-altered IDs are invalid, never normalized into another owner. Exact roles are User/Administrator; role alone is never owner consent or content access. Existing Auth email trim/lowercase remains exclusively the issuer's rule. Test bearer authentication is real; no public caller-supplied account mapping is accepted.

Decoded native labels are computational ground truth only for this fixed detector, never human speech truth. Candidate generation may fail to supply usable native groups; that is a fixture finding, not permission to mock detector labels or claim calibration. Decoder/encoder flags and frame boundaries need actual approved execution validation. Tolerances are1e-12 normalized PCM on the same pinned path and1e-6 public decimal measurements; severity compares unrounded values. Cross-platform classification equality is not asserted beyond predecessor prerequisite evidence.

Catalog test identities and settings are isolated dependency inputs, not registry approval. No fallback defaults or policy bypass exists outside these tests. Logging checks use synthetic markers only. Existing generic persistence schemas may need minimal additive GREEN changes later; none is authorized here. Full browser microphone/UI, distributed cleanup/retry/publication races, deployed transport, full Policy configuration HTTP, model performance and accepted private calibration remain their named later Plan milestones. No commit, push, PR, publication, remote workflow, paid compute or additional delivery process is prescribed.

## Pre-authorized Contingencies

Only diagnostic-context contingency: trigger is missing/denied dockerDesktopLinuxEngine named pipe in restricted context while the same pre-existing user engine works in ordinary host context. Exact file changes: none. Exact action: rerun the same four read-only diagnostics and approved verification commands in the successful host context, each diagnostic bounded15seconds and observation/handoff bounded120seconds. Record original denial, real host output and deviation. No start/stop/restart/context/settings change and no unrelated container access. If readiness remains unavailable, record Waiting for user-provided working engine/context. No alternate detector/codec/dependency/test/criterion contingency.

## Rollback / recovery and review status

On failure retain actual evidence, mark no completion and return for review. Remove only the two test files if this approved execution created them, preserving unrelated work; do not reset/clean/checkout the repository. Fixture teardown may remove only its own unique resources. Do not stop user Docker. This artifact is Proposed, not approved, and has no execution authorization.

## Exact-code / authority self-check

| File | Complete final content, no placeholder/pseudocode | Proposed-change and setting trace |
| --- | --- | --- |
| tests/test_enrollment_quality.py | Complete Python block; no production stub | File1; Q11/proposal algorithm and candidate settings; explicit reviewed decoder/assessment/policy interfaces and tolerance/oracle choices; installed009 detector. |
| tests/test_voice_enrollment.py | Complete Python block; no production stub | File2; FR-010–013/Q5/Q8–Q11/contract; explicit reviewed factories, test-only capability/evidence/material collaborator, fixture settings and scheduler diagnostics; existing owner/Auth/Consent seams. |

No new requirement-ID family is introduced and no approved label is redefined. Test names and test-only internal interface choices do not supersede normative contract labels. No template comments remain. No dependency, plugin or runtime setting is introduced; every test-local input and seam is submitted explicitly for this review.

## Human Review

Status: Executed — Voice Enrollment RED Complete on 2026-10-25 under avinash2196 approval recorded2026-10-25T22:44:13Z. Exact two reviewed files applied; baseline57/57 twice,21 intended missing-symbol errors twice, post-change57/57 twice, exact preservation and owned-resource cleanup verified. See Plan.md Voice Enrollment RED execution evidence. No GREEN or later milestone authorized.
