"""Deterministic decoded audio screening; calibration approval is external."""
from copy import deepcopy
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
import io
import math

import av
import numpy as np
import webrtcvad

from voice_narration._sql import PersistenceError, fail


CHECKS = ("duration", "clipping", "silence", "noise", "level", "speech_presence")


def rounded(value):
    if value is None:
        return None
    return format(Decimal(str(value)).quantize(Decimal("0.000001"),
                                             rounding=ROUND_HALF_EVEN), "f")


def validate_policy(policy):
    shapes = {"vad": {"implementation", "artifact_ref", "sample_rate_hz", "frame_ms", "mode"},
              "clipping": {"peak_abs", "max_fraction"},
              "silence": {"frame_rms_dbfs", "max_fraction"},
              "noise": {"min_snr_db", "min_speech_seconds", "min_nonspeech_seconds"},
              "level": {"min_speech_rms_dbfs", "max_speech_rms_dbfs"},
              "speech_presence": {"min_fraction", "min_seconds"}}
    if not isinstance(policy, dict) or set(policy) != set(shapes) | {"policy_id", "calibration_ref"}:
        fail("INVALID_CONFIGURATION")
    if policy["policy_id"] != "enrollment-acoustics-v1":
        fail("INVALID_CONFIGURATION")
    if not isinstance(policy["calibration_ref"], str) or not policy["calibration_ref"].strip():
        fail("INVALID_CONFIGURATION")
    for section, keys in shapes.items():
        if not isinstance(policy[section], dict) or set(policy[section]) != keys:
            fail("INVALID_CONFIGURATION")
    vad = policy["vad"]
    if (vad["implementation"] != "webrtc-gmm" or
            not isinstance(vad["artifact_ref"], str) or not vad["artifact_ref"].strip() or
            type(vad["sample_rate_hz"]) is not int or vad["sample_rate_hz"] != 16000 or
            type(vad["frame_ms"]) is not int or vad["frame_ms"] != 20 or
            type(vad["mode"]) is not int or not 0 <= vad["mode"] <= 3):
        fail("INVALID_CONFIGURATION")
    for section in set(shapes) - {"vad"}:
        for value in policy[section].values():
            if type(value) not in (int, float):
                fail("INVALID_CONFIGURATION")
            number = Decimal(str(value))
            if not number.is_finite() or number.as_tuple().exponent < -6:
                fail("INVALID_CONFIGURATION")
    clip, silence, noise = policy["clipping"], policy["silence"], policy["noise"]
    level, speech = policy["level"], policy["speech_presence"]
    if not (0 < clip["peak_abs"] <= 1 and 0 <= clip["max_fraction"] <= 1 and
            silence["frame_rms_dbfs"] < 0 and 0 <= silence["max_fraction"] <= 1 and
            noise["min_speech_seconds"] > 0 and noise["min_nonspeech_seconds"] > 0 and
            level["min_speech_rms_dbfs"] < level["max_speech_rms_dbfs"] <= 0 and
            0 <= speech["min_fraction"] <= 1 and speech["min_seconds"] > 0):
        fail("INVALID_CONFIGURATION")
    return deepcopy(policy)


def duration_bounds(capability, settings=None):
    try:
        low = Decimal(capability["sample_min_seconds"])
        high = Decimal(capability["sample_max_seconds"])
        if settings is not None:
            low = max(low, Decimal(settings["sample_min_seconds"]))
            high = min(high, Decimal(settings["sample_max_seconds"]))
        if not low.is_finite() or not high.is_finite() or low <= 0 or low > high:
            fail("INVALID_CONFIGURATION")
        return low, high
    except (KeyError, TypeError, InvalidOperation, ValueError):
        raise PersistenceError("INVALID_CONFIGURATION") from None


def decode(data, format):
    if not isinstance(data, bytes) or not data or format not in ("wav", "mp3", "m4a"):
        fail("INVALID_AUDIO")
    try:
        with av.open(io.BytesIO(data)) as source:
            names = set(source.format.name.split(","))
            permitted = {"wav": {"wav"}, "mp3": {"mp3"}, "m4a": {"mov", "mp4", "m4a"}}
            if not names & permitted[format]:
                fail("INVALID_AUDIO")
            streams = [(stream.index, bool(int(stream.disposition) & 1))
                       for stream in source.streams.audio]
        defaults = [index for index, default in streams if default]
        order = defaults if len(defaults) == 1 else [index for index, _ in streams]
        for index in sorted(order):
            try:
                with av.open(io.BytesIO(data)) as source:
                    frames = list(source.decode(source.streams[index]))
                    if not frames:
                        continue
                    rate = frames[0].sample_rate
                    channels = len(frames[0].layout.channels)
                    originals = []
                    analysis = [[] for _ in range(channels)]
                    samplers = [av.AudioResampler(format="dblp", layout="mono", rate=16000)
                                for _ in range(channels)]
                    for frame in frames:
                        converter = av.AudioResampler(format="dblp", layout=frame.layout, rate=rate)
                        for planar in converter.resample(frame):
                            values = planar.to_ndarray().astype(np.float64)
                            if values.shape[0] != channels or not np.isfinite(values).all():
                                fail("INVALID_AUDIO")
                            originals.append(values)
                            for channel in range(channels):
                                mono = av.AudioFrame.from_ndarray(values[channel:channel + 1],
                                                                 format="dblp", layout="mono")
                                mono.sample_rate = rate
                                analysis[channel].extend(samplers[channel].resample(mono))
                    for channel in range(channels):
                        analysis[channel].extend(samplers[channel].resample(None))
                    original = np.concatenate(originals, axis=1)
                    resampled = np.stack([np.concatenate([f.to_ndarray().reshape(-1) for f in rows])
                                          for rows in analysis])
                    if not original.shape[1] or not resampled.shape[1] or not np.isfinite(resampled).all():
                        fail("INVALID_AUDIO")
                    return {"channels": original, "analysis_channels": resampled,
                            "sample_rate_hz": rate, "stream_index": index,
                            "duration_seconds": Decimal(original.shape[1]) / Decimal(rate)}
            except av.error.FFmpegError:
                continue
    except (av.error.FFmpegError, ValueError, TypeError, IndexError):
        raise PersistenceError("INVALID_AUDIO") from None
    fail("INVALID_AUDIO")


def features(sample, policy):
    original, analysis = sample["channels"], sample["analysis_channels"]
    lengths, powers = [], []
    for start in range(0, analysis.shape[1], 320):
        block = analysis[:, start:start + 320]
        lengths.append(block.shape[1])
        powers.append(np.mean(block * block, axis=1))
    lengths = np.asarray(lengths)
    powers = np.asarray(powers).T
    masks = []
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
    snrs, levels = [], []
    for channel in range(analysis.shape[0]):
        speech = masks[channel]
        sc, nc = int(lengths[speech].sum()), int(lengths[~speech].sum())
        s = float(np.dot(powers[channel, speech], lengths[speech]) / sc) if sc else 0
        n = float(np.dot(powers[channel, ~speech], lengths[~speech]) / nc) if nc else 0
        if sc:
            levels.append(10 * math.log10(s) if s > 0 else None)
            valid = (sc / 16000 >= policy["noise"]["min_speech_seconds"] and
                     nc / 16000 >= policy["noise"]["min_nonspeech_seconds"] and n > 0 and s > n)
            snrs.append(10 * math.log10((s - n) / n) if valid else None)
    return {"duration": sample["duration_seconds"],
            "clipping": max(float(np.mean(np.abs(c) >= policy["clipping"]["peak_abs"])) for c in original),
            "silence": float(lengths[quiet].sum() / lengths.sum()),
            "speech_presence": speech_count / int(lengths.sum()), "speech_seconds": speech_count / 16000,
            "snrs": snrs, "levels": levels}


def assess(samples, *, policy, duration_bounds):
    policy = validate_policy(policy)
    if not samples:
        fail("INVALID_INPUT")
    try:
        rows = [features(sample, policy) for sample in samples]
    except Exception:
        raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
    snrs = [v for row in rows for v in row["snrs"] if v is not None]
    levels = [v for row in rows for v in row["levels"] if v is not None]
    measured = [min(r["duration"] for r in rows), max(r["clipping"] for r in rows),
                max(r["silence"] for r in rows), min(snrs) if snrs else None,
                min(levels) if levels else None, min(r["speech_presence"] for r in rows)]
    noise_unknown = any(not r["snrs"] or any(v is None for v in r["snrs"]) for r in rows)
    level_unknown = any(not r["levels"] or any(v is None for v in r["levels"]) for r in rows)
    low, high = map(Decimal, duration_bounds)
    flags = [any(not low <= r["duration"] <= high for r in rows),
             measured[1] > policy["clipping"]["max_fraction"],
             measured[2] > policy["silence"]["max_fraction"],
             noise_unknown or measured[3] is None or measured[3] < policy["noise"]["min_snr_db"],
             level_unknown or any(v < policy["level"]["min_speech_rms_dbfs"] or
                                  v > policy["level"]["max_speech_rms_dbfs"] for v in levels),
             any(r["speech_presence"] < policy["speech_presence"]["min_fraction"] or
                 r["speech_seconds"] < policy["speech_presence"]["min_seconds"] for r in rows)]
    if noise_unknown:
        measured[3] = None
    if level_unknown:
        measured[4] = None
    actions = ("Record within the displayed duration bounds.", "Lower gain and re-record.",
               "Reduce long quiet sections or move closer.",
               "Use a quieter room and include a natural pause; acknowledge uncertainty if needed.",
               "Adjust microphone distance and gain; both low and high channels may need correction.",
               "Speak naturally in Hindi or English; short detected speech may need re-recording.")
    units = ("seconds", "ratio", "ratio", "dB", "dBFS", "ratio")
    result = []
    for index, check in enumerate(CHECKS):
        severity = "failure" if index == 0 and flags[index] else "warning" if flags[index] else "pass"
        message = ("Measurement inconclusive." if measured[index] is None else
                   "Screening bounds exceeded." if flags[index] else "Screening bounds met.")
        result.append({"check": check, "severity": severity, "measured": rounded(measured[index]),
                       "unit": units[index], "message": message, "action": actions[index]})
    return result
