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
