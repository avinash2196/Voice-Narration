# Chatterbox Commercial Evidence — ai-gateway-multimodel

## Purpose

Record commercial-use eligibility evidence for Chatterbox code, weights, and output-use terms before any production model enablement (AGW-004/AGW-005).

## Status

Completed evidence capture on 2026-11-08; awaiting user confirmation for downstream enablement decisions.

## Evidence Sources

| Evidence Area | Source URL / Artifact | Retrieved | Extracted evidence | Commercial Use Allowed | Notes |
| --- | --- | --- | --- | --- | --- |
| Source code license | https://raw.githubusercontent.com/resemble-ai/chatterbox/master/LICENSE | 2026-11-08 | MIT License text grants rights to “use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies”. | Yes | Standard MIT obligations apply (preserve copyright/license notice). |
| Model distribution metadata | https://huggingface.co/ResembleAI/chatterbox | 2026-11-08 | Model card text explicitly states “Licensed under MIT”. | Yes | Treat as model-card claim; keep immutable snapshot/commit hash when implementing enforcement. |
| Package metadata | https://pypi.org/project/chatterbox-tts/ | 2026-11-08 | PyPI metadata lists `License: MIT License` and includes open-source installation/usage path. | Yes | Supports operational use claims but is secondary to authoritative license files/model cards. |
| Vendor status update | https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages | 2026-11-08 | Update states product line is retired commercially by vendor but remains open source archive. | Yes (license unchanged) | Operational/support risk exists; not a license prohibition by itself. |

## Runtime Policy Check (AGW-005)

| Check | Result | Evidence |
| --- | --- | --- |
| Self-hosted runtime path available | Met | PyPI project documents local installation (`pip install chatterbox-tts`) and local Python inference usage. |
| No mandatory external API dependency for core generation | Met | Hugging Face/PyPI usage examples show direct local model loading (`from_pretrained`) and generation without required external inference API calls. |

## Gate Decision

- Decision: **Met with operational caveat**
- Rationale: Commercial-use and redistribution permissions are MIT-based and explicitly permissive; self-hosted path is documented. Caveat: upstream vendor has retired commercial offering/support, so long-term maintenance/support burden is on repository owners.
- Approved by: Pending (milestone evidence only; no runtime enablement decision recorded here)
- Approved at: Pending
