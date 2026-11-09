# Requirements — chatterbox-cloud-run

Every item ends with one source label:

- `[User: brief]` or `[User: Qn]` — stated by the user, in the brief or in the answer to clarification question n (see Clarification Log).
- `[Repo: <path>:<line>]` — established by inspecting the current repository during this capture.
- `[Artifact: <work-item>/<file> <ID>]` — an approved requirement of another work item that this work item explicitly depends on; quote it, do not extend it.
- `[Derived from <sources> — confirmed Qn]` — a consequence derived from other items; recorded only after the user confirmed it.
- `[Left to <phase> — non-blocking]` — valid only in Non-Blocking Decisions.

## Goal

"Deploy the chatterbox on gcp cloud and then run everything else on local for testing"; login and other capabilities come later. Only voice cloning runs on GCP for now. [User: brief, Q6]

## Status

Approved by avinash2196 on 2026-11-09. Approval recorded by the main conversation at the user's explicit approval ("Approve requirements"). This artifact does not authorize a Plan, contract, Implementation Plan, test, or code change.

## Relationship to Product-Level Requirements

There is no product-level `docs/requirements.md`, so this work item changes no product-level statement. [Repo: docs/requirements.md — file absent]

This work item depends on an approved requirement of the `ai-gateway-multimodel` work item: "AGW-011 (Separate model service deployment): Chatterbox must run as a separate self-hosted Cloud Run service exposing an API consumed by the AI Gateway, so model runtime can evolve independently from gateway policy logic." [Artifact: ai-gateway-multimodel/requirements.md AGW-011]

## Repository-Confirmed Facts

- RF-1: The Chatterbox API's synthesize request has an optional `sample_path` field holding a file path. [Repo: voice_narration/chatterbox_api/application.py:24]
- RF-2: When `sample_path` is given, Chatterbox opens it on its own filesystem and answers 404 if the file does not exist. [Repo: voice_narration/chatterbox_api/application.py:65-69]
- RF-3: Chatterbox accepts only the languages `hi` and `en`. [Repo: voice_narration/chatterbox_api/application.py:60]
- RF-4: Chatterbox answers 503 when model generation raises an error. [Repo: voice_narration/chatterbox_api/application.py:72-74]
- RF-5: Chatterbox's device comes from the `CHATTERBOX_DEVICE` environment variable, defaulting to `cpu`. [Repo: voice_narration/chatterbox_api/application.py:15]
- RF-6: The Chatterbox container image is built from `python:3.11-slim` and sets `CHATTERBOX_DEVICE=cpu`. [Repo: cloudrun/chatterbox-service/Dockerfile:1, cloudrun/chatterbox-service/Dockerfile:14]
- RF-7: The existing Chatterbox deployment instructions deploy with `--allow-unauthenticated`. [Repo: cloudrun/chatterbox-service/README.md:11]
- RF-8: Uploaded voice samples are stored on the local filesystem by the voices service, and their local path is recorded as the profile's `sample_path`. [Repo: voice_narration/simple_voices/application.py:115-116, voice_narration/simple_voices/application.py:134]
- RF-9: The local inference service reads the Chatterbox base URL from `VOICE_CLONING_API_BASE_URL`, falling back to `CHATTERBOX_API_BASE_URL`. [Repo: voice_narration/inference/application.py:23-24]
- RF-10: The local inference service sends the profile's local `sample_path` to Chatterbox and calls it with a 120-second timeout. [Repo: voice_narration/inference/application.py:107, voice_narration/inference/application.py:110]
- RF-11: In `voice_cloning` mode, when Chatterbox does not produce audio, the local inference service answers 503 with the single message "Voice cloning service is unavailable. Please retry, or use Google voice narration mode." [Repo: voice_narration/inference/application.py:179-183]
- RF-12: Outside `voice_cloning` mode, the local inference service generates audio with the Google TTS provider. [Repo: voice_narration/inference/application.py:184-186]
- RF-13: Generated audio is written by the local inference service to the local filesystem. [Repo: voice_narration/inference/application.py:177]
- RF-14: Existing test `test_voice_cloning_returns_guidance_when_clone_backend_unavailable` asserts the 503 answer when no clone backend is configured. [Repo: tests/test_clone_flow.py:55-83]
- RF-15: Existing test `test_gateway_execution_returns_non_placeholder_telemetry` replaces the inference service's HTTP call to Chatterbox with a fake response. [Repo: tests/test_ai_gateway_telemetry_red.py:41-47]

## Requirements

- CCR-1 (Cloud scope): Chatterbox voice cloning runs on Google Cloud Run in GCP project `project-84eb579f-1f7b-4f87-838`. Only voice cloning is on GCP for now. [User: brief, Q1, Q6]
- CCR-2 (Local scope): The voices service, inference service and frontend run locally. Narration mode keeps using Google TTS as it does today. [User: Q6]
- CCR-3 (Region): Chatterbox is deployed in region `asia-southeast1`. [Derived from User: Q10 — confirmed Q16]
- CCR-4 (GPU): Chatterbox runs on an NVIDIA L4 GPU. [User: Q2]
- CCR-5 (Voice sample transfer): The voice sample audio is sent to Chatterbox with each synthesis request. [User: Q3]
- CCR-6 (Remove sample path): The `sample_path` field is removed from Chatterbox's synthesize request and is not kept alongside the sample audio. [User: Q8]
- CCR-7 (Private access): Chatterbox is private and callable only by the service account of the existing service-account key (`test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`), with the local inference service attaching that account's Google identity token. [User: Q4, Q5]
- CCR-8 (Failure reporting): When Chatterbox is unreachable or fails, the local inference service answers 503 and the message says why it failed (for example cannot connect, access denied, Chatterbox error, or bad response), replacing today's single generic message. The user accepted this "if its not too much of changes". [Derived from User: Q7 — confirmed Q17]
- CCR-9 (Request time limit): A voice cloning request has a configurable time limit of 10 minutes. [User: Q18]
- CCR-10 (No cloud data retention): Chatterbox does not hold the voice sample or the generated audio after the response; data is saved in the local app. [User: Q14]
- CCR-11 (Deployment documentation): This work item delivers a document describing how to deploy Chatterbox to GCP; performing the deployment is not part of this work item. [User: Q9]

## Operational Characteristics

| Characteristic | Answer | Source |
|----------------|--------|--------|
| Scale | Not required for this work item. | [User: Q13] |
| Deployment | Chatterbox may scale to zero when idle, with at most 1 instance running. | [User: Q11, Q19] |
| Availability and latency | A voice cloning request has a configurable time limit of 10 minutes (CCR-9). No uptime expectation was stated. | [User: Q12, Q18] |
| Consistency and concurrency | Chatterbox handles one cloning request at a time; other requests wait their turn within the time limit. A retried request produces a new clip; no duplicate detection is required. | [User: Q21] |
| Dependency failure | The local inference service answers 503 with the reason for failure (CCR-8). | [Derived from User: Q7 — confirmed Q17] |
| Observability | Not required for this work item beyond Cloud Run's default request logs; no custom logging, metrics or alerts. | [User: Q15, Q20] |

## Decisions Deferred to Later Milestones

- The exact failure reasons and message wording of the 503 answer (CCR-8) are decided by the CONTRACT milestone. [User: Q17]
- The request shape for sending the voice sample audio to Chatterbox (CCR-5, CCR-6) is decided by the CONTRACT milestone. [User: Q3, Q8 — shape not specified by the user]
- The name and form of the setting that configures the 10-minute time limit (CCR-9) is decided by the CONTRACT milestone. [User: Q18 — setting not specified by the user]

## Explicit Exclusions

- Login and authentication of application users are not part of this work item ("we will do login and other later"). [User: brief]
- Performing the GCP deployment is not part of this work item. [User: Q9]
- Moving the voices service, inference service, frontend or narration mode to GCP. [User: Q6]

## Non-Blocking Decisions

- How the deployment document is organized and where it lives in the repository. [Left to Plan — non-blocking]

## Acceptance Criteria

- AC-CCR-1: Voice cloning requests from the local inference service are served by Chatterbox on Cloud Run in project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, on an NVIDIA L4 GPU, when deployed as documented. [Verifies CCR-1, CCR-3, CCR-4]
- AC-CCR-2: Narration mode keeps generating audio with Google TTS locally, and the voices service, inference service and frontend run locally. [Verifies CCR-2]
- AC-CCR-3: A voice cloning request sends the voice sample audio itself to Chatterbox; Chatterbox's synthesize request no longer accepts `sample_path`. [Verifies CCR-5, CCR-6]
- AC-CCR-4: Chatterbox rejects calls that do not carry a valid identity token for the `test-850@…` service account, and the local inference service attaches that account's token. [Verifies CCR-7]
- AC-CCR-5: When Chatterbox is unreachable, denies access, fails, or returns a bad response, the local inference service answers 503 with a message stating which of these happened. [Verifies CCR-8]
- AC-CCR-6: A voice cloning request is limited to a configurable time limit of 10 minutes. [Verifies CCR-9]
- AC-CCR-7: Chatterbox keeps no voice sample or generated audio after responding, and the generated audio is saved by the local app. [Verifies CCR-10]
- AC-CCR-8: A deployment document describes how to deploy Chatterbox to GCP to satisfy CCR-1, CCR-3, CCR-4, CCR-7 and the Deployment characteristic (scale to zero, at most 1 instance, one request at a time). [Verifies CCR-11]

## Clarification Log

| Q | Question | Answer |
|---|----------|--------|
| Q1 | Which GCP project should Chatterbox be deployed into? | `project-84eb579f-1f7b-4f87-838`, the project of the existing service-account key ("Yes, use that project"). |
| Q2 | Should Chatterbox run on a GPU or a CPU on Cloud Run? | NVIDIA L4 GPU. |
| Q3 | How should the voice sample get to Chatterbox? | Send the audio with each request. |
| Q4 | Who should be able to call the Chatterbox URL? | "If we use google token, we can use our service key for that or would we need to configure more .." |
| Q5 | Should Chatterbox be private, callable only by the service account in the existing key, with the local inference service attaching that account's token? | "yes it should be called from that only" |
| Q6 | Do the voices service, inference service and frontend run locally, with only voice_cloning calling the cloud and narration staying on Google TTS? | "yes only cloning needs to be on gcp for now" |
| Q7 | When Chatterbox is unreachable or fails, keep the 503 with the retry/narration message? | "return 503 to show that why it failed" |
| Q8 | Confirm `sample_path` is removed from `/v1/synthesize`, not kept alongside? | Yes. |
| Q9 | Does this work item include actually deploying to GCP, or only code and deployment files? | "create doc on how to" |
| Q10 | Which GCP region? | "souteast1" |
| Q11 | Can the service scale to zero when idle, and what is the most instances at once? | "yes we can do 0" |
| Q12 | How long may one clip take, including a cold start? | "no limit" (superseded by Q18) |
| Q13 | Scale: how many people and clips per day during testing? | Not required. |
| Q14 | Must Chatterbox never store the voice sample or generated audio in the cloud? | "dont hold in chatterbox, we need to save data in local app" |
| Q15 | Is anything needed beyond Cloud Run's default logs? | "not required other than at chatterbox" (clarified by Q20) |
| Q16 | Is "souteast1" `asia-southeast1`? | Yes. |
| Q17 | Should the 503 message also say why it failed, replacing the single generic message, with wording decided in the contract? | "yes if its not too much of changes" |
| Q18 | Is "no limit" the app setting no limit while accepting Cloud Run's 60-minute maximum? | "60 mins would be too big ...lets put configurable limit of 10 mins" |
| Q19 | What is the most instances that may run at once? | 1. |
| Q20 | What must be visible at Chatterbox? ("keep it clean" — default logs only, or one short log line per request?) | Default logs only. |
| Q21 | May concurrent cloning requests run in parallel, and may a retry produce a new clip without duplicate detection? ("use recommended" — one request at a time, retries make a new clip, no duplicate detection) | Yes, record that. |

## Provenance Check

- Every item above carries a source label: checked Goal, Relationship, RF-1–RF-15, CCR-1–CCR-11, the six Operational Characteristics rows, three deferred decisions, three exclusions, one non-blocking decision, and AC-CCR-1–AC-CCR-8.
- `Derived` items, each with its confirming `Qn`: CCR-3 (region `asia-southeast1`, confirmed Q16); CCR-8 and the Dependency failure row (503 with failure reason, confirmed Q17).
- `Left to` items: organization and location of the deployment document (Left to Plan).
- `Repo` citations verified against the current repository during this capture: voice_narration/chatterbox_api/application.py:15, :24, :60, :65-69, :72-74; cloudrun/chatterbox-service/Dockerfile:1, :14; cloudrun/chatterbox-service/README.md:11; voice_narration/simple_voices/application.py:115-116, :134; voice_narration/inference/application.py:23-24, :107, :110, :177, :179-183, :184-186; tests/test_clone_flow.py:55-83; tests/test_ai_gateway_telemetry_red.py:41-47; docs/requirements.md absent.
- `Artifact` citation verified: ai-gateway-multimodel/requirements.md AGW-011 at line 37, artifact status Approved at line 15.
- Requirements without an acceptance criterion: none (CCR-1→AC-1, CCR-2→AC-2, CCR-3→AC-1, CCR-4→AC-1, CCR-5→AC-3, CCR-6→AC-3, CCR-7→AC-4, CCR-8→AC-5, CCR-9→AC-6, CCR-10→AC-7, CCR-11→AC-8).
- Existing behavior affected: RF-14's asserted 503 is kept (status code) and its message changes per CCR-8 (Q7, Q17); RF-15's fake HTTP call is affected by CCR-5/CCR-7 request changes — whether that test is updated is decided by the Plan from CCR-5 and CCR-7, not changed here.
- No statement about this artifact as a whole is made beyond the checks listed above.
