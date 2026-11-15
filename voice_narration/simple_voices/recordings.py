"""Chrome recordings stored as PCM WAV (Plan OAD-1).

Chrome's recorder produces WebM audio, which the voice service converts to
WAV when it stores the sample. WebM is recognized from the bytes, never from
the file name or content type the upload carries.
"""

import io
import wave

import av

EBML_MAGIC = b"\x1a\x45\xdf\xa3"
WEBM_DOCTYPE = b"\x42\x82\x84webm"


class ConversionError(Exception):
    """A WebM recording could not be converted to WAV."""


def is_webm(data: bytes) -> bool:
    """True when ``data`` starts with an EBML header whose DocType is ``webm``."""
    if len(data) < 5 or not data.startswith(EBML_MAGIC):
        return False
    marker = data[4]
    width = 1
    while width <= 8 and not marker & (0x80 >> (width - 1)):
        width += 1
    if width > 8:
        return False
    size = marker & (0xFF >> width)
    for byte in data[5:4 + width]:
        size = (size << 8) | byte
    header_start = 4 + width
    return WEBM_DOCTYPE in data[header_start:header_start + size]


def webm_to_wav(data: bytes) -> bytes:
    """Decode the recording's first audio stream to 16-bit PCM mono WAV."""
    resampler = av.AudioResampler(format="s16", layout="mono")
    pcm = bytearray()
    rate = 0
    try:
        with av.open(io.BytesIO(data)) as source:
            for frame in source.decode(audio=0):
                for converted in resampler.resample(frame):
                    rate = converted.sample_rate
                    pcm += converted.to_ndarray().tobytes()
        for converted in resampler.resample(None):
            rate = converted.sample_rate
            pcm += converted.to_ndarray().tobytes()
    except (av.FFmpegError, IndexError) as error:
        raise ConversionError(str(error)) from error
    if not pcm:
        raise ConversionError("the recording holds no audio")
    output = io.BytesIO()
    with wave.open(output, "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(rate)
        target.writeframes(bytes(pcm))
    return output.getvalue()
