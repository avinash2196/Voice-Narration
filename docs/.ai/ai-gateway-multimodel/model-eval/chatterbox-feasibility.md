# Chatterbox Hindi/English Feasibility — ai-gateway-multimodel

## Purpose

Capture feasibility evidence for Hindi and English support plus operational notes required for gateway routing policy (AGW-006 and milestone-2 scope).

## Status

Completed evidence capture on 2026-11-08.

## Evaluation Inputs

| Input | Value |
| --- | --- |
| Language set | Hindi (`hi`) and English (`en`) |
| Work item | ai-gateway-multimodel |
| Model candidate | Chatterbox (Multilingual family) |
| Evidence basis | Official model card/docs statements; no local benchmark execution in this milestone |

## Feasibility Findings

| Dimension | Result | Evidence |
| --- | --- | --- |
| Hindi support claim | Met | Hugging Face model card lists Hindi in supported languages and Hindi single-language pack links. |
| English support claim | Met | Hugging Face model card lists English support across base/multilingual variants. |
| Self-hosted usage feasibility | Met | PyPI/HF docs provide direct local installation and code examples for local generation. |
| Accent-transfer/cross-language caveat | Known limitation | Model docs warn reference clip language mismatch may transfer accent; mitigation guidance includes CFG adjustments. |
| Production support caveat | Risk accepted | Resemble resource update notes commercial retirement/no active support despite open-source availability. |

## Routing Policy Readiness Outcome

- Ready for AGW routing milestones: **Yes, with explicit policy constraints**
- Required policy constraints for next milestones:
  1. Restrict initial route to approved Chatterbox variants with `languages_supported` including `hi` and `en`.
  2. Include deterministic guardrails for unsupported language/model combinations.
  3. Treat support/maintenance caveat as operational risk in fallback and incident policy.
