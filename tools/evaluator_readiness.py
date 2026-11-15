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
