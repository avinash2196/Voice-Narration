# Plan — chatterbox-original-app

## Status

Approved by Avinash Srivastava on 2026-11-13, as written. The pre-existing frontend failures (90 at planning time, including the two "Max 5000 chars/request" label tests) and the two known backend failures are accepted as named old failures and are not repaired in this work item.

## Objective

Let a logged-in user of the original multi-page app record or upload a voice on `/voices`, then choose Chatterbox on `/tts` and get speech in that voice from the deployed Chatterbox service, in English or Hindi, while Google narration keeps working and text is no longer capped for any provider (requirements Goal, COA-1–COA-17).

Authoritative input: `docs/.ai/chatterbox-original-app/requirements.md`, Status "Approved by Avinash Srivastava on 2026-11-13". No product-level `docs/requirements.md` exists (requirements, Relationship to Product-Level Requirements; re-checked during planning).

Labels this Plan introduces use prefixes no referenced approved artifact defines: `OAM-` (milestones), `OAC-` (contract decisions), `OAD-` (Plan decisions), `OAR-` (risks), `OAS-` (Plan-level success criteria), `OAV-` (verification commands).

## Current State

Inspected at HEAD `664cee4` on branch `claude/chatterbox-original-app-client-a3ef0e`, 2026-11-13. The working tree is clean apart from this work-item folder.

Existing behavior this work item affects:

- **Voice service.** The running voice service (`start-voice-service.bat:25`) keeps voices in an in-memory dictionary (`voice_narration/simple_voices/application.py:10`), preloaded with five Google voices (`:13-63`). Upload parses multipart data by hand (`:83-103`), keeps only the sample's length, not its audio (`:111`), and stores every voice as approved with score 95 (`:113-114`). Listing returns every voice to every caller with no per-user filter (`:129-149`). A voice can be deleted (`:186-195`). Voices are lost when the service restarts.
- **Inference service.** One provider is chosen at startup from `INFERENCE_PROVIDER`: Google, else the mock; Azure falls back to the mock (`voice_narration/inference/__main__.py:33-58`). The generation operation reads only the text and the voice identifier from the request (`voice_narration/inference/application.py:461-463`), calls the startup provider (`:292`), and answers failures with an error message body (`:465-479`). Each generation is saved under the audio storage root, which defaults to the tracked `audio_storage/` folder (`:87-89`, `:130-149`), and is also written to the database with an expiry of `AUDIO_RETENTION_DAYS`, default 30 days, inside a block that silently ignores database failure (`:150-179`). The database defaults to a local PostgreSQL instance (`voice_narration/inference/db.py:19-28`). History listing, download and deletion exist (`:508-582`). The provider listing returns every registered provider (`:343-373`, `:584-609`); the registry registers mock, Google and Azure (`voice_narration/inference/registry.py:68-77`).
- **TTS page.** The provider list comes from the inference service's provider listing, and each provider is labelled with a hard-coded 5000-character maximum (`frontend/src/services/ttsApi.ts:182-201`, `frontend/src/components/ProviderSelector.tsx:89`). The generation request carries only the text and voice identifier, so the chosen provider is not sent (`frontend/src/services/ttsApi.ts:42-52`); for Google, a non-Google voice identifier is replaced (`:7-19`). The voice selector shows only Google-pattern voices whenever any exist (`frontend/src/components/VoiceSelector.tsx:21-39`). The text box truncates at 5000 characters, shows "n / 5000", a 90% warning and a maximum-reached message (`frontend/src/components/TextToSpeechInput.tsx:4-70`). The Generate button is disabled while a generation is being submitted (`frontend/src/components/GenerationSubmitForm.tsx:133`). A failed generation shows the error text from the response (`frontend/src/components/GenerationErrorDisplay.tsx:50`). The audio of a ready generation is loaded into the player (`frontend/src/pages/TextToSpeech.tsx:34-51`). The page waits on one request for the whole generation (`frontend/src/services/ttsApi.ts:42-59`).
- **Recorder.** The recorder uses the browser's default format (WebM in Chrome), labels the recording as WAV and uploads it as `recording.wav` (`frontend/src/components/VoiceRecorder.tsx:52`, `:67`, `:160`). The upload form accepts MP3, WAV and OGG (`frontend/src/components/VoiceUpload.tsx:104-105`).
- **Contracts.** No approved contract artifact describes the running voice service or the inference service's operations: the `initial-build` contract (`docs/.ai/initial-build/contract/API-Contract.md`) defines a different voices API that the launchers do not run. The deployed Chatterbox is described by the reference contract on `feature/voice-cloning` at `abbe387`, `docs/.ai/chatterbox-cloud-run/API-Contract.md` (Contract Review Status: Approved 2026-11-09); its inference-service sections describe code that is not on this branch.
- **Ignored files.** `.env` and `service-account-key.json` are gitignored (`.gitignore:5`, `:8`). `audio_storage/` is tracked (25 files).

Existing tests that cover this behavior:

- Backend: `tests/test_inference.py`, `tests/test_provider_registry.py`, `tests/test_generation_history_download.py`, `tests/test_generation_persistence_red.py`, `tests/test_generation_delete_search_red.py` — 29 passed in a planning run on 2026-11-13. That run modified the tracked `audio_storage/generation_index.json` and created an untracked `audio_storage/generations/2026-11-13/` folder (written by `tests/test_generation_history_download.py`, whose app uses the default storage root, `:18`); both were restored. No test exercises the running voice service.
- Frontend: `frontend/tests/tts.spec.tsx` and `frontend/tests/voice.spec.tsx`. The cap tests and test mock named in requirements COA-17 are: the counter test expecting "0 / 5000" (`tts.spec.tsx:83`), M3.1.6 cap (`:113-120`), M3.1.7 counter (`:130`), M3.1.8 90% warning (`:133-144`), the provider-label assertions in M3.3.2 (`:256`) and M3.3.5 (`:291`), and the test mock's 5000-character rejection (`frontend/tests/mocks/tts-handlers.ts:27`). The M3.1 tests pass; M3.3.2 and M3.3.5 fail at baseline (see below).

Pre-existing failures:

- Named by the user: `tests/test_voice_enrollment.py` times out; `tests/test_real_model_inference.py` has one failure. Not run during planning.
- Observed during planning: the frontend suite (`npx vitest run` after `npm ci`, 2026-11-13, HEAD `664cee4`) reports `Test Files 2 failed | 2 passed (4)`, `Tests 90 failed | 263 passed (353)`.
  - `tts.spec.tsx`, 27 failures: M3.2.1–M3.2.7, M3.3.1–M3.3.6, M3.7.1–M3.7.7, M3.11.1, M3.11.2, M3.11.3, M3.11.5, M3.12.1, M3.12.5, M3.12.7. Example cause: M3.3.5 renders "fetch failed", because the test mock serves endpoints the page does not call (`frontend/tests/mocks/tts-handlers.ts:18-215` against `frontend/src/services/ttsApi.ts:42`, `:183`, `:204`).
  - `voice.spec.tsx`, 63 failures: M2.2.4, M2.3.2, M2.3.5, M2.6.7, M2.8.2–M2.8.8, M2.9.1–M2.9.8, M2.10.1–M2.10.10, M2.11.1–M2.11.9, M2.12.1–M2.12.9, M2.13.1–M2.13.8, M2.14.1–M2.14.8.
  - Each failure was seen in one run; each Implementation Plan confirms its baseline (`implementation-planning` Pre-existing Failures).
- `npm run type-check` passes at baseline.

Environment facts: a fresh worktree has no `frontend/node_modules`; `npm ci` installs it from the committed lockfile, into a gitignored folder. The Python environment on PATH has the packages pinned in `requirements-dev.txt`, plus `pytest-asyncio`, the Google Text-to-Speech client and the Google authentication library, none of which `requirements-dev.txt` declares. The audio library pinned in `requirements-dev.txt` encoded a WebM/Opus clip and converted it to WAV in a scratch check outside the repository during planning.

## In Scope

- An approved API/external contract for the voice-service and inference-service behavior this work item changes, and for the settings it adds (OAM-1).
- The voice service: it keeps each voice's sample, stores Chrome recordings as WAV (OAD-1), keeps voices and samples across restarts, deletes them 5 days after upload, keeps automatic approval and the shared list (OAM-2, OAM-3).
- The inference service: it uses the provider each generation names, clones through the deployed Chatterbox with the chosen language and the voice's sample, gives one message per failure cause, applies the configurable time limit, does not fall back to Google, keeps cloned generations in history, and makes a second request wait (OAM-4, OAM-5).
- The TTS page: Google or Chatterbox chosen per generation, recorded and uploaded voices selectable for Chatterbox, English or Hindi chosen, failure messages shown, cloned audio played, and no text cap for any provider (OAM-6, OAM-7).
- The user's manual check against the deployed Cloud Run service (OAM-8).

## Out of Scope

Exclusions stated by the requirements:

- Copying the Chatterbox service source (`voice_narration/chatterbox_api/`, `cloudrun/chatterbox-service/`, the `setuptools==80.10.2` pin) into this branch; putting the service on `main` is a separate PR outside this work item (Explicit Exclusions, Q34).
- Changing or redeploying the deployed Chatterbox service (Explicit Exclusions, CON-3).
- Per-user voice separation (Explicit Exclusions, COA-15).
- A consent step or manual approval before cloning (Explicit Exclusions, COA-12).
- Falling back to Google when Chatterbox fails (Explicit Exclusions, COA-8).
- Duplicate prevention beyond the disabled Generate button (COA-13).
- Splitting long text (COA-17).
- A local Docker build or container, and any `gcloud` command, during planning or execution (CON-2).
- Running anything other than Chatterbox on GCP (CON-1).
- Committing voice samples, `service-account-key.json` or `.env` (CON-6).

Not required for this work item (requirements Operational Characteristics): scale, availability, and observability.

## Requirements and Constraints

- Requirements COA-1–COA-17, constraints CON-1–CON-6, scenarios S-1–S-8 and acceptance criteria AC-1–AC-13, as approved in `requirements.md`.
- Operational characteristics as approved: each local service runs as one instance and Chatterbox runs on Cloud Run; a Chatterbox call may last up to the configurable limit, default 1200 s, and cold starts take about 80–100 s; a request that arrives during a generation waits; dependency failure shows the error for its cause with no Google fallback, and automated tests use a fake Chatterbox; voices and samples survive a restart and are deleted 5 days after upload; generated clips keep the 30-day retention. Scale, availability and observability are not required.
- Deployed Chatterbox interface (fixed constraint, CON-3, CON-5): the Chatterbox Synthesize and Chatterbox Caller Identity interfaces of the reference contract (`feature/voice-cloning` at `abbe387`, `docs/.ai/chatterbox-cloud-run/API-Contract.md`). Its other sections and its labels are not adopted.
- User constraint for this Plan (create-plan arguments, 2026-11-13): tracked files under `audio_storage/` must not be modified; when a test run touches them, they are restored (OAV-3).
- **OAD-1 Chrome recordings reach Chatterbox as WAV (Plan decision; requirements Decisions Deferred, COA-6).** The voice service stores the sample of a Chrome recording as WAV audio when it stores the sample, whatever file name or type label the upload carries. A WAV upload is stored as received. MP3 and OGG uploads stay accepted and are stored as received; they are not required to clone. The recorder and the upload form stay unchanged. Reason: the deployed Chatterbox is unchanged (CON-3), and WAV is the one format the requirements require to clone (COA-6). Converting when the sample is stored means every consumer of the sample gets WAV. The conversion can be tested in the backend suite with a WebM recording built inside the test, using the audio library already pinned in `requirements-dev.txt` (Current State). Recording WAV in the browser would change the recorder, which the frontend test environment cannot record with.

## Non-Blocking Open Decisions

- Which language is preselected when Chatterbox is chosen. COA-5 requires only that the user can choose English or Hindi. Decided in the OAM-6 Implementation Plan, for review.
- Whether Google voices are also listed when Chatterbox is chosen. COA-3 requires that recorded and uploaded voices are listed and selectable. Decided in the OAM-6 Implementation Plan, for review.
- How each Implementation Plan's Acceptance / Completion Criteria treat the pre-existing failures named in Current State. The user decides this before approving each Implementation Plan whose verification runs them (`implementation-planning` Pre-existing Failures). Repairing those failing tests is not in this work item's requirements.

## External Contract Requirements

A contract is required. This work item changes the operations the TTS page calls on the inference service, the voice-service behavior the inference service depends on, and adds settings operators set. It is delivered by OAM-1, the first milestone after Plan approval.

- **Artifact:** the work item's API/external contract in `docs/.ai/chatterbox-original-app/`.
- **Baseline (`prompt-driven-development` Changed Contracts):** no approved contract artifact describes these operations (Current State), so the baseline is the current repository behavior of the running voice service (`voice_narration/simple_voices/application.py`) and inference service (`voice_narration/inference/application.py`, `voice_narration/inference/__main__.py`). OAM-1 verifies the baseline against the repository and surfaces any divergence for review. Carried-over behavior is not reopened.
- **Fixed constraint, not redefined:** the deployed Chatterbox's Synthesize and Caller Identity interfaces in the reference contract (CON-3, CON-5). The contract references them and does not change them.
- **Decisions OAM-1 must resolve** (the Plan resolves none of them):
  - **OAC-1** How a generation request names the chosen provider (Google or Chatterbox) and, for Chatterbox, the chosen language (English or Hindi), and how it carries text of any length for every provider (COA-1, COA-5, COA-17).
  - **OAC-2** What a generation request does when it names no provider, or a provider other than Google or Chatterbox (COA-1; COA-14 keeps mock and Azure unchanged).
  - **OAC-3** How Chatterbox appears in the provider list the TTS page reads, while mock, Google and Azure stay listed as `tests/test_inference.py:152-176` checks (COA-1, COA-14).
  - **OAC-4** How the inference service obtains a voice's stored sample from the voice service, and the answer for an unknown voice, an expired voice, or a voice without a usable sample (COA-2, COA-4, COA-7 "voice sample unreadable").
  - **OAC-5** The answer for each of the nine failure causes in COA-7, including the full wording of each message (each ending "Please retry, or choose another provider.") and the order in which the causes are checked (COA-7, COA-8).
  - **OAC-6** The time-limit setting: its name, accepted form, default of 1200 seconds, what counts as invalid (the "invalid time-limit setting" cause), when it is read, and the span it bounds (COA-9).
  - **OAC-7** The settings the inference service reads to reach the deployed Chatterbox: its URL, and the credential used to obtain the identity token for the CON-5 service account with the audience CON-5 requires. Also how an absent or blank value is handled ("not configured", "identity token unavailable") (COA-7, CON-5, CON-6).
  - **OAC-8** How a generation request that arrives while another is generating waits, for which providers, and whether the wait counts toward the time limit (COA-13, COA-9).
  - **OAC-9** How and when the TTS page receives the result or failure of a generation that may last up to the time limit (COA-4, COA-9, COA-13).
  - **OAC-10** The voice-service changes: the upload answer once the sample is kept, including the answer when a Chrome recording cannot be stored as WAV (OAD-1); listing, lookup and deletion for voices past the 5-day retention; what deleting a voice does to its sample; persistence across restarts; and automatic approval and the shared list kept (COA-2, COA-6, COA-11, COA-12, COA-15).
  - **OAC-11** How cloned generations appear in the generation history, download and delete operations, and how their 30-day retention is recorded (COA-10).

## Milestones

Decomposition: Split: separate engineering decision, independent capabilities, different verification setup, ordering — boundaries and reasons below.

Milestone boundaries:

- **OAM-1 (CONTRACT) first:** the work item changes operations between the TTS page, the inference service and the voice service, and adds operator settings. Every repository-changing milestone depends on that behavior being approved first.
- **Voice service pair (OAM-2, OAM-3):** a separate engineering decision — how voices and samples are stored durably, retained for 5 days, and converted under OAD-1. The voice service can be verified on its own in the backend suite.
- **Inference service pair (OAM-4, OAM-5):** a separate engineering decision — how the Chatterbox call is made with an identity token and a time limit, how failures map to nine messages, and how per-generation routing and waiting work. Ordering: it is planned against the executed voice service, whose sample it sends. Its tests use a fake Chatterbox (COA-16).
- **TTS page pair (OAM-6, OAM-7):** different verification setup (the frontend suite, not the backend suite), and an independent capability — provider, voice and language selection, the message display, and the cap removal. Ordering: it is planned against the executed inference service whose requests it sends.
- **OAM-8 (OTHER) last:** different verification setup — the user, the deployed Cloud Run service and real credentials (COA-16, CON-2). It changes no production behavior.
- No FOUNDATION milestone: the Plan Content Rule 11 check in each RED milestone finds every prerequisite in place. No REFACTOR milestone: none is requested.

### OAM-1 — Local service contract (CONTRACT)

- **Capability / purpose:** define the externally observable behavior this work item adds or changes in the voice service and the inference service, and the settings operators set.
- **Rationale:** a contract is required (External Contract Requirements); it comes before every other milestone.
- **Milestone type:** CONTRACT.
- **Predecessor:** Plan approval.
- **Scope:**
  - Deliver the work item's API/external contract artifact. Its baseline is the current repository behavior, verified against the repository, with divergences surfaced.
  - Resolve OAC-1–OAC-11, each traced to its requirements.
  - Reference the deployed Chatterbox's Synthesize and Caller Identity interfaces as a fixed constraint, and OAD-1 as the Plan's decision.
- **Owned requirements / concerns:** decisions OAC-1–OAC-11, covering the externally observable error mapping, configuration names and retention behavior.
- **Explicit exclusions:** no Implementation Plan, test, or code; no change to the deployed Chatterbox interface; no restating or re-publishing of the reference contract; no operation, field or setting beyond what OAC-1–OAC-11 need; no documentation format or tooling.
- **Success criteria:** the contract artifact answers OAC-1–OAC-11 with traceability; its baseline check is recorded; the user's approval is recorded in its status, which marks OAM-1 complete in Execution Status.

### OAM-2 — Voice service RED (RED)

- **Capability / purpose:** executable evidence that the voice service lacks the sample, durability and retention behavior.
- **Rationale:** opens the voice service pair (Milestone boundaries).
- **Milestone type:** RED.
- **Predecessor:** OAM-1.
- **Scope** — tests that verify, against the approved contract (OAC-4, OAC-10):
  - A Chrome-style recording — WebM audio uploaded under a WAV file name and type label, as the recorder sends it — is stored with a WAV sample (COA-2, COA-6, OAD-1).
  - A WAV upload's sample is stored exactly as received (COA-2, COA-6).
  - MP3 and OGG uploads are still accepted, and their samples are kept as received (COA-2, COA-6).
  - A new voice is approved automatically and its sample is available to the inference service straight away, as OAC-4 defines (COA-12, COA-2).
  - Voices and their samples are still present after the voice service restarts (COA-11).
  - A voice and its sample are gone 5 days after upload, as OAC-10 defines (COA-11).
  - Every caller sees every voice, with no per-user filtering, including after a restart (COA-15).
  - The upload answer when a Chrome recording cannot be stored as WAV (OAC-10).
- **Prerequisites (Plan Content Rule 11):** the backend test runner, the HTTP test client, the multipart support and the audio library that builds the WebM recording are already pinned and installed (Current State). The tests' fakes and data live in the tests. Nothing is missing, so no FOUNDATION milestone is needed.
- **Owned requirements / concerns:** none delivered. It verifies COA-2, COA-6 (storage), COA-11, COA-12 and COA-15 (Requirement Traceability).
- **Explicit exclusions:** no production, build or configuration change; no inference-service or TTS-page tests; tests use no network and leave tracked `audio_storage/` files unchanged.
- **Success criteria:** each new test fails only because the approved behavior is missing (valid RED evidence, recorded in Execution Status). Existing tests are unchanged, and their results are unchanged apart from the named pre-existing failures.

### OAM-3 — Voice service GREEN (GREEN)

- **Capability / purpose:** the voice service keeps samples durably, stores Chrome recordings as WAV and applies the 5-day retention.
- **Rationale:** closes the voice service pair.
- **Milestone type:** GREEN.
- **Predecessor:** OAM-2.
- **Scope** — the behavior that makes the OAM-2 evidence pass:
  - Each recorded or uploaded voice's sample is kept, and made available to the inference service as OAC-4 defines (COA-2).
  - A Chrome recording's sample is stored as WAV; WAV, MP3 and OGG uploads are stored as received (COA-6, OAD-1).
  - Voices and samples survive a restart (COA-11).
  - Each voice and its sample are deleted, unrecoverably, 5 days after upload (COA-11).
  - Automatic approval is kept (COA-12).
  - The voice list stays shared by every caller (COA-15).
  - Upload, listing, lookup and deletion follow OAC-10.
- **Owned requirements / concerns:** COA-2, COA-6 (sample storage format), COA-11, COA-12, COA-15, OAD-1; the voice service's persistence behavior and retention.
- **Explicit exclusions:** no per-user separation; no consent or manual approval; no change to the recorder, the upload form, the inference service or the TTS page; no voice sample or key file committed (samples are kept only where version control ignores them, CON-6); no change to tracked `audio_storage/` files.
- **Success criteria:** the OAM-2 tests pass; the full backend suite passes apart from the named pre-existing failures; `audio_storage/` is unchanged (OAV-3).

### OAM-4 — Inference service RED (RED)

- **Capability / purpose:** executable evidence that the inference service cannot route a generation to Chatterbox and does not report Chatterbox failures as required.
- **Rationale:** opens the inference service pair (Milestone boundaries).
- **Milestone type:** RED.
- **Predecessor:** OAM-3.
- **Scope** — tests that verify, with a fake Chatterbox and no network (COA-16), against the approved contract:
  - A generation that names Chatterbox sends the deployed Chatterbox (as CON-5 and the reference contract define) the entered text whole, unsplit and longer than 5000 characters, along with the chosen language and the selected voice's stored sample. It carries an identity token for the configured Chatterbox URL, and the audio Chatterbox returns becomes the generation's audio (COA-1, COA-4, COA-5, CON-5; OAC-1, OAC-4, OAC-7).
  - A generation that names Google is generated by Google, not Chatterbox; a generation that names no provider behaves as OAC-2 defines (COA-1).
  - Each of the nine failure causes produces its own message as OAC-5 defines, each ending "Please retry, or choose another provider." (COA-7).
  - When Chatterbox fails, no Google generation is made and no audio is saved (COA-8).
  - The time limit defaults to 1200 seconds and can be configured as OAC-6 defines; a call that exceeds it produces the timed-out message (COA-9).
  - A cloned generation appears in history, can be downloaded and deleted, and has its 30-day retention recorded, as OAC-11 defines (COA-10).
  - A generation request that arrives while another is generating waits and then completes, as OAC-8 defines (COA-13).
- **Prerequisites (Plan Content Rule 11):** the backend test runner with its async support (already used by the existing inference tests, though undeclared — OAR-4), the HTTP test client and the pinned HTTP client library are installed. The fake Chatterbox, the fake identity token and the sample source are test code. After OAM-3, the voice service the tests may use exists. Nothing is missing, so no FOUNDATION milestone is needed.
- **Owned requirements / concerns:** COA-16's automated-test part (these tests use a fake Chatterbox and no network). It verifies COA-1, COA-4, COA-5, COA-7, COA-8, COA-9 and COA-10 (inference parts), COA-13 (waiting) and CON-5.
- **Preserved tests (unchanged):** `tests/test_inference.py`, `tests/test_provider_registry.py`, `tests/test_generation_history_download.py`, `tests/test_generation_persistence_red.py`, `tests/test_generation_delete_search_red.py`.
- **Explicit exclusions:** no production, build or configuration change; no change to the preserved tests; no network; no voice-service or TTS-page tests; tracked `audio_storage/` files left unchanged.
- **Success criteria:** each new test fails only because the approved behavior is missing (valid RED evidence, recorded). The preserved tests still pass.

### OAM-5 — Inference service GREEN (GREEN)

- **Capability / purpose:** the inference service clones through the deployed Chatterbox for generations that name it, and reports each failure cause.
- **Rationale:** closes the inference service pair.
- **Milestone type:** GREEN.
- **Predecessor:** OAM-4.
- **Scope** — the behavior that makes the OAM-4 evidence pass:
  - Each generation uses the provider it names (COA-1, OAC-1, OAC-2), and Chatterbox appears in the provider list as OAC-3 defines.
  - A Chatterbox generation sends the text whole, the chosen language and the voice's stored sample to the deployed Chatterbox, with an identity token for the CON-5 service account obtained from the OAC-7 settings, and returns the speech (COA-4, COA-5, CON-5).
  - Each of the nine failure causes gets its own message (COA-7, OAC-5), with no Google fallback (COA-8).
  - The configurable time limit, default 1200 seconds (COA-9, OAC-6).
  - Cloned generations in history, download and deletion, with the 30-day retention (COA-10, OAC-11).
  - Waiting for a request that arrives during a generation (COA-13, OAC-8), and delivery of the result or failure as OAC-9 defines.
- **Owned requirements / concerns:** COA-1 (inference part), COA-4 (cloned speech produced), COA-5 (inference part), COA-7 (inference part), COA-8, COA-9, COA-10, COA-13 (waiting), CON-5; the error mapping and the Chatterbox settings.
- **Explicit exclusions:** no change to the mock, Google or Azure providers or their tests (COA-14); no Google fallback; no duplicate prevention; no text splitting; no change to the deployed Chatterbox and no copied Chatterbox source; no Docker or `gcloud`; no logging or metrics added for observability; no voice-service or TTS-page change; no change to tracked `audio_storage/` files.
- **Success criteria:** the OAM-4 tests and the preserved tests pass; the full backend suite passes apart from the named pre-existing failures; `audio_storage/` is unchanged (OAV-3).

### OAM-6 — TTS page RED (RED)

- **Capability / purpose:** executable evidence that the TTS page cannot choose Chatterbox, a voice and a language for a generation, and still caps text.
- **Rationale:** opens the TTS page pair (Milestone boundaries).
- **Milestone type:** RED.
- **Predecessor:** OAM-5.
- **Scope** — tests that verify, against the approved contract, with the inference and voice services mocked:
  - The page offers Google and Chatterbox, and the generation request names the chosen provider (COA-1, OAC-1).
  - With Chatterbox chosen, the recorded and uploaded voices are listed and selectable (COA-3).
  - With Chatterbox chosen, English or Hindi can be chosen, and the request carries the choice (COA-5).
  - A Chatterbox failure message from the inference service is shown to the user (COA-7).
  - A finished Chatterbox generation's audio is loaded into the page's player (COA-4).
  - The Generate button is disabled while a Chatterbox generation is running (COA-13).
  - For every provider, text longer than 5000 characters stays whole in the text box and is sent whole, unsplit. The count reads "n characters", and no "/ 5000", 90% warning, maximum-reached message or "Max 5000 chars/request" label is shown. A rejected long-text Google generation shows the app's failed-generation error (COA-17). The label's absence is checked by a test that reaches the provider list (OAR-6).
  - The cap tests and the test mock listed in Current State are changed to match COA-17.
- **Existing tests changed by this milestone:** the cap tests and test mock listed in Current State (requirements COA-17, Repository-Confirmed Facts). M3.3.2 and M3.3.5 already fail at baseline for an unrelated reason, so they are not RED evidence (OAR-6).
- **Prerequisites (Plan Content Rule 11):** the frontend test runner, the component-testing libraries and the request-mocking library are declared in the lockfile and installed by `npm ci` (OAV-4), which changes no tracked file. Nothing is missing, so no FOUNDATION milestone is needed.
- **Owned requirements / concerns:** COA-17's test-change part (the cap tests and test mock change to match). It verifies the page parts of COA-1, COA-3, COA-4, COA-5, COA-7, COA-13 and COA-17.
- **Explicit exclusions:** no production, build or configuration change; no backend tests; no change to existing frontend tests other than the cap tests and test mock named in Current State; no repair of the pre-existing failures.
- **Success criteria:** each new or changed test fails only because the approved behavior is missing (valid RED evidence, recorded). The exceptions are M3.3.2 and M3.3.5, which keep their pre-existing failure, recorded as such. All other tests keep their baseline result.

### OAM-7 — TTS page GREEN (GREEN)

- **Capability / purpose:** the TTS page lets the user choose Google or Chatterbox, a voice and a language for each generation, shows cloning failures, plays cloned speech, and accepts text of any length.
- **Rationale:** closes the TTS page pair.
- **Milestone type:** GREEN.
- **Predecessor:** OAM-6.
- **Scope** — the behavior that makes the OAM-6 evidence pass:
  - The chosen provider is sent with each generation (COA-1).
  - Recorded and uploaded voices are selectable for Chatterbox (COA-3).
  - English or Hindi is chosen for Chatterbox generations (COA-5).
  - Chatterbox failure messages are shown (COA-7).
  - Cloned speech plays on the page (COA-4).
  - The Generate button stays disabled during a generation (COA-13).
  - The cap, the "/ 5000" count, the 90% warning, the maximum-reached message and the "Max 5000 chars/request" label are removed; the count reads "n characters"; text is sent whole for every provider (COA-17).
- **Owned requirements / concerns:** COA-1 (page part), COA-3, COA-4 (playback on the page), COA-5 (page part), COA-7 (page part), COA-13 (disabled button), COA-17 (behavior).
- **Explicit exclusions:** no change to the recorder or upload form (OAD-1); no per-user voice filtering; no Google fallback; no text splitting; no new limit; no other duplicate prevention; no backend change; no repair of the pre-existing failures.
- **Success criteria:** the OAM-6 tests pass, apart from M3.3.2 and M3.3.5 keeping their pre-existing failure. The full frontend suite shows no failure other than the named pre-existing failures, and `npm run type-check` passes. The backend is unchanged.

### OAM-8 — Cloud Run manual validation (OTHER)

- **Capability / purpose:** the user's manual check that a voice recorded in Chrome, and a voice uploaded as WAV, each produce speech in that voice through the deployed Chatterbox, in English and in Hindi, playing on the TTS page (COA-16, AC-4, AC-5).
- **Rationale:** requirements COA-16 and Business Context Outcome make the user's manual check against Cloud Run the final check. It needs the user, the deployed service and real credentials.
- **Milestone type:** OTHER (validation protocol).
- **Predecessor:** OAM-7.
- **Scope:**
  - A validation protocol, set out in its Implementation Plan: the steps to start the local services one instance each with the OAC-7 settings, and the cases to run.
  - Inputs, all supplied by the user and never committed (CON-6): a voice recorded in Chrome on `/voices`, a WAV file, the service-account key and the local settings.
  - For each case, the expected observation and the met or not-met rule.
  - The cases: S-1 in English and in Hindi; S-2 in English and in Hindi.
- **No-behavior-change statement:** it changes no production code, test, build or configuration file; the only repository change is the evidence it records in this Plan.
- **Baseline evidence:** the full-suite results recorded at OAM-7, and the user's confirmation that the deployed service is the unchanged one at the CON-5 URL.
- **Preserved tests:** the full backend and frontend suites recorded at OAM-7. OAM-8 changes no file they cover.
- **Completion evidence:** the user's recorded met or not-met result for each case, with the voice heard and the language chosen.
- **Owned requirements / concerns:** COA-16's manual part; the deployment characteristic (local services one instance each, Chatterbox on Cloud Run).
- **Explicit exclusions:** no Docker or `gcloud` (CON-2); no change to the deployed service (CON-3); no committed sample, key or `.env` (CON-6); no code change. A not-met case is reported for replanning, not fixed here.
- **Success criteria:** every case is recorded as met. Execution Status shows `Waiting — manual check from user` until the user records the results.

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| COA-1 provider chosen per generation — inference service uses the provider the request names | OAM-5 | OAM-4 |
| COA-1 provider chosen per generation — page offers Google and Chatterbox and sends the choice | OAM-7 | OAM-6 |
| COA-2 sample kept by the voice service | OAM-3 | OAM-2 |
| COA-3 recorded and uploaded voices selectable on `/tts` when Chatterbox is chosen | OAM-7 | OAM-6 |
| COA-4 cloned speech produced through the deployed Chatterbox for the voice, text and language | OAM-5 | OAM-4 |
| COA-4 cloned speech plays on the TTS page | OAM-7 | OAM-6 |
| COA-5 English or Hindi — chosen on the page and sent | OAM-7 | OAM-6 |
| COA-5 English or Hindi — forwarded to Chatterbox | OAM-5 | OAM-4 |
| COA-6 Chrome recordings and WAV uploads stored so they clone; MP3/OGG still accepted (with OAD-1) | OAM-3 | OAM-2 |
| COA-7 one message per failure cause — produced by the inference service | OAM-5 | OAM-4 |
| COA-7 one message per failure cause — shown on the page | OAM-7 | OAM-6 |
| COA-8 no fallback to Google | OAM-5 | OAM-4 |
| COA-9 configurable time limit, default 1200 s, timed-out message | OAM-5 | OAM-4 |
| COA-10 cloned generations in history, downloadable, deletable, 30-day retention | OAM-5 | OAM-4 |
| COA-11 voices and samples survive restart; deleted 5 days after upload | OAM-3 | OAM-2 |
| COA-12 automatic approval kept; clonable straight away | OAM-3 | OAM-2 |
| COA-13 a request that arrives during a generation waits | OAM-5 | OAM-4 |
| COA-13 Generate button disabled during a generation | OAM-7 | OAM-6 |
| COA-13 no other duplicate prevention added | none — exclusion | Final Review |
| COA-14 mock, Google and Azure providers and their tests unchanged; Google narration as before apart from the cap | none — preserved | OAM-5 (preserved tests listed in OAM-4) and OAM-7 (full frontend suite) |
| COA-15 shared voice list | OAM-3 | OAM-2 |
| COA-16 automated tests use a fake Chatterbox with no network | OAM-4 | Final Review |
| COA-16 final check is the user's manual test on Cloud Run | OAM-8 | OAM-8 |
| COA-17 no text cap, sent whole, plain count, warnings and label removed | OAM-7 | OAM-6 |
| COA-17 the cap tests and test mock change to match | OAM-6 | Final Review |
| CON-1 only Chatterbox runs on GCP | none — exclusion | Final Review |
| CON-2 no local Docker build or container, no `gcloud` | none — exclusion | Final Review |
| CON-3 deployed Chatterbox used unchanged | none — exclusion | Final Review |
| CON-4 Chatterbox stays a separate service | none — exclusion | Final Review |
| CON-5 call the deployed service with the identity token for the named account and audience, in its request and response form | OAM-5 | OAM-4 |
| CON-6 voice samples, `service-account-key.json` and `.env` never committed | none — exclusion | Final Review |
| Exclusion: copying the Chatterbox service source into this branch | none — exclusion | Final Review |
| Exclusion: changing or redeploying the deployed Chatterbox | none — exclusion | Final Review |
| Exclusion: per-user voice separation | none — exclusion | Final Review |
| Exclusion: consent step or manual approval before cloning | none — exclusion | Final Review |
| Exclusion: falling back to Google when Chatterbox fails | none — exclusion | Final Review |
| OAD-1 Chrome recordings stored as WAV | OAM-3 | OAM-2 |
| Contract decisions OAC-1–OAC-11 | OAM-1 | Human review of the contract |
| Operational: scale | none — not required | none |
| Operational: deployment — local services one instance each, Chatterbox on Cloud Run | OAM-8 | OAM-8 |
| Operational: availability | none — not required | none |
| Operational: latency — up to the time limit; cold starts 80–100 s | covered by the COA-9 row | covered by the COA-9 row |
| Operational: consistency and concurrency | covered by the COA-13 rows | covered by the COA-13 rows |
| Operational: dependency failure | covered by the COA-7, COA-8 and COA-16 rows | covered by the COA-7, COA-8 and COA-16 rows |
| Operational: observability | none — not required | none |
| Operational: data durability and retention | covered by the COA-10 and COA-11 rows | covered by the COA-10 and COA-11 rows |
| User constraint: tracked `audio_storage/` files unchanged | none — exclusion | Final Review (with OAV-3 evidence per milestone) |

The Business Context rules restate COA-5, COA-11, COA-12 and COA-17 and are traced through those rows. Scenarios S-1–S-8 are traced through AC-1–AC-13 (Final Acceptance Criteria).

## Verification Commands

| ID | Command (run from the repository root unless stated) | Use | Source |
| --- | --- | --- | --- |
| OAV-1 | `python -m pytest <test files> -q` | Scoped backend runs (RED and dry runs) | `pytest.ini` (`testpaths = tests`, `pythonpath = .`); `requirements-dev.txt` (`pytest==9.1.1`) |
| OAV-2 | `python -m pytest -q` | Full backend suite, once per backend GREEN execution and at OAM-7. Pre-existing: the `tests/test_voice_enrollment.py` timeout and one `tests/test_real_model_inference.py` failure | `pytest.ini`; pre-existing failures named by the user (create-plan arguments, 2026-11-13) |
| OAV-3 | `git status --short -- audio_storage` must print nothing; if it does, `git checkout -- audio_storage` then `git clean -fd -- audio_storage` | After every backend test run | User constraint (create-plan arguments, 2026-11-13); planning run evidence (Current State) |
| OAV-4 | `npm ci` (in `frontend/`) | Before any frontend test run in a fresh worktree; changes no tracked file | `frontend/package.json`, `frontend/package-lock.json` |
| OAV-5 | `npx vitest run` (in `frontend/`); scoped: `npx vitest run tests/tts.spec.tsx -t "<test name>"` | Frontend tests. Baseline: `Tests 90 failed / 263 passed (353)` (Current State) | `frontend/package.json` (`"test": "vitest"`), `frontend/vitest.config.ts` |
| OAV-6 | `npm run type-check` (in `frontend/`) | OAM-6 and OAM-7; passes at baseline | `frontend/package.json` (`"type-check": "tsc --noEmit"`) |

No verification command uses Docker or `gcloud` (CON-2). OAM-8's steps are recorded in its Implementation Plan. Output is written to log files, and only summaries and failing tests are recorded (`prompt-driven-development` Test Scope and Output).

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| OAM-1 Local service contract (CONTRACT) | Complete | `docs/.ai/chatterbox-original-app/API-Contract.md`, Approved by Avinash Srivastava on 2026-11-13 |
| OAM-2 Voice service RED | Complete — valid RED established 2026-11-13 | `001_Implementation_Plan_OAM-2.md`; see OAM-2 RED evidence below |
| OAM-3 Voice service GREEN | Blocked — V3C-4 not met: 67 full-suite errors outside the accepted list (Docker engine not running) | `002_Implementation_Plan_OAM-3.md`; see OAM-3 stopped execution evidence below |
| OAM-4 Inference service RED | Pending | — |
| OAM-5 Inference service GREEN | Pending | — |
| OAM-6 TTS page RED | Pending | — |
| OAM-7 TTS page GREEN | Pending | — |
| OAM-8 Cloud Run manual validation (OTHER) | Pending | — |

### OAM-2 RED evidence

Executed 2026-11-13 at HEAD `ff9d3ee`, Git Bash, from the repository root. Change: created `tests/test_voice_sample_persistence_red.py`, extracted verbatim from the plan's Proposed Code block (`001_Implementation_Plan_OAM-2.md` lines 152-578). No other repository file changed. Logs are in `$TEMP` (outside the repository).

- Compile: `python -m compileall -q . -x '(node_modules|\.git|\.venv|frontend)'` exited 0.
- Command 1: `python -m pytest tests/test_voice_sample_persistence_red.py -q > "$TEMP/oam2-red-run1.log" 2>&1; tail -1 …; grep -c "unexpected keyword argument 'root'" …` → `11 failed in 11.63s`; `11`. 0 passed, 0 errors. Failing tests (all 11 in the file):
  - `test_chrome_recording_labelled_wav_is_stored_as_pcm_wav_holding_the_recording`
  - `test_wav_upload_sample_is_stored_byte_identical`
  - `test_mp3_and_ogg_uploads_are_accepted_and_kept_as_received[mp3-libmp3lame-voice.mp3-audio/mpeg-ID3]`
  - `test_mp3_and_ogg_uploads_are_accepted_and_kept_as_received[ogg-libopus-voice.ogg-audio/ogg-OggS]`
  - `test_new_voice_is_approved_automatically_and_its_sample_is_available_straight_away`
  - `test_sample_answers_not_found_for_unknown_preloaded_and_sampleless_voices`
  - `test_chrome_recording_that_cannot_be_converted_is_rejected_and_creates_no_voice`
  - `test_voices_samples_and_renames_survive_a_restart_and_are_listed_for_every_caller`
  - `test_voice_expires_120_hours_after_upload_and_is_removed_unrecoverably`
  - `test_voice_uploaded_before_a_restart_expires_while_the_service_is_stopped`
  - `test_deleting_a_voice_removes_its_sample_permanently_including_after_a_restart`
- Failure causes (V2C-2): seven tests raise `TypeError: create_app() got an unexpected keyword argument 'root'` in the test process. Four tests (conversion failure, restart, stopped-service expiry, deletion) fail with `AssertionError: voice service exited during start:`, which quotes the same `TypeError` from the service log. No other cause appeared. The audio builders (`chrome_recording`, `encoded_audio` with `libmp3lame`/`libopus`, `unconvertible_webm`) ran before each failure, so V2R-4 did not occur.
- Command 2 (second run, no cleanup): `11 failed in 12.56s`; grep count `11`; 11 `FAILED` lines, with the same four "exited during start" failures. Identical to run 1 (V2C-3).
- Command 3: `python -m pytest --collect-only -q > "$TEMP/oam2-collect.log" 2>&1; tail -1 …` → `173 tests collected in 3.90s`, with no collection error (V2C-5).
- Command 4: `git status --short -- audio_storage` → no output (V2C-4, OAV-3).
- Command 5: `git status --short` → `?? tests/test_voice_sample_persistence_red.py`, plus the work-item changes under `docs/.ai/chatterbox-original-app/` (V2C-1).
- Why this is valid RED: every failure comes from the absent approved seam `create_app(*, root, clock)` (V2D-1), which is part of the behavior OAM-3 must deliver. No failure comes from compilation, configuration, dependencies or the environment. As V2R-2 records, the behavior-level failures behind the seam were shown only by the planning stub. I re-read each assertion against `API-Contract.md` (Voice Upload sample storage and failure 2, Voice List ordering and contents, Voice Update, Voice Deletion, Voice Sample, Voice Retention). Each one asserts the contracted behavior, not the current state. The tests that check something is absent (`not storage_holds`, `404`s after expiry or deletion) each first exercise the positive case in the same test: the sample is present, or a `400` with the exact body is returned.
- Preserved-behavior tests expected to pass at RED: none planned, and none passed.
- Pre-authorized contingencies: none listed and none applied.
- Deviations: one addition. The plan lists no compile command, so I added the `compileall` step above to satisfy the RED "compile everything" scope (`prompt-driven-development` Test Scope). It writes only gitignored `__pycache__`. The five planned commands ran as written and in order.
- Processes: each voice-service process the tests started exited during start and was collected by the fixture's `kill()`/`wait()`. A process check afterwards found no process from this run still running. The `uvicorn.exe` on port 8000 is from an unrelated project (`v11\Traffic`) and was started before this run.

### OAM-3 stopped execution evidence

Executed 2026-11-13 at HEAD `8907c63`, which differs from the plan's `1d35815` only by the plan itself (`git diff --stat 1d35815 HEAD -- voice_narration .gitignore tests` printed nothing). Git Bash, from the repository root. Logs are in `$TEMP` (`C:\Users\avina\AppData\Local\Temp`), outside the repository.

- Changes applied: `recordings.py` and `store.py` were created from the plan's code blocks (`002_Implementation_Plan_OAM-3.md` lines 150-211 and 217-304), and `cmp` showed them identical to the blocks. The `application.py` and `.gitignore` diffs (lines 310-506 and 517-524) were applied with `git apply` after `git apply --check`. The sorted `+`/`-` lines of `git diff` match the plan's diffs exactly (`cmp` printed nothing). V3C-1 holds.
- Command 1: `compiled`.
- Command 2: `11 passed in 14.11s` (V3C-2 met).
- Command 3, no cleanup: `11 passed in 36.28s` (V3C-3 met).
- Command 4a: `$TEMP/oam3-accepted.txt` written; `wc -l` gives `25`; `sort -c` reports it sorted.
- Command 4b: `1 failed, 64 passed, 17 skipped, 43 warnings, 91 errors in 128.20s (0:02:08)`; interrupt count `0`.
- Command 4c: the `unexpected:` list is not empty. It holds 67 node ids:
  - `tests/test_persistence.py`: 33;
  - `tests/test_authentication_consent.py`: 24;
  - `tests/test_voice_enrollment.py`: 10. They are `test_all_pass_without_override_and_model_minimal_material_selection[materials0]`, `test_guidance_formats_playback_admission_and_originals`, `test_obsolete_assessment_rerecording_and_strict_override`, `test_readiness_gates_without_false_pass[changed_evaluator, changed_settings, missing_calibration, missing_policy, model, unavailable_evaluator]` and `test_warning_override_profile_reuse_and_minimal_materials`.
  - The `accepted, not failing:` list is empty. Results of the accepted tests: `test_production_inference_module_missing` FAILED (`ImportError: cannot import name 'ProductionInferenceProvider'`, as on the baseline). The 24 accepted `test_voice_enrollment.py` ids are ERROR, each now at setup with the Docker cause below, not the baseline's `psycopg` timeouts. `[materials1]` appears once, as ERROR, not also FAILED.
- Cause of every one of the 91 errors: a test fixture's `subprocess.CalledProcessError` from `docker compose -f compose.harness.yaml -p vnred… up --detach --wait --wait-timeout 120` and `… down --volumes --remove-orphans`. There were 91 of each, each `returned non-zero exit status 1`. `docker info` printed `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine … The system cannot find the file specified`, so the Docker engine was not running. None of the three files references `simple_voices` or `voice_storage` (`grep` found no match). The failures do not come from OAM-3's change, but V3C-4 counts any failure outside the accepted list. Under V3C-4 and V3R-9, execution stopped here, with no rerun, skip or repair.
- Command 4d: `173 tests collected in 2.91s`, with no collection error.
- Command 5: ` M audio_storage/generation_index.json`, `?? audio_storage/generations/2026-11-13/`.
- Command 6: `git checkout -- audio_storage`. Then `git clean -fd -- audio_storage` printed `Removing audio_storage/archive/`, `Removing audio_storage/generations/2026-11-13/`, `Removing audio_storage/temp/`. Repeating command 5 printed nothing (V3C-5 met).
- Command 7: `absent`; `.gitignore:11:/voice_storage/	voice_storage/voices.json` (V3C-6 met).
- Command 8: `(*, root=None, clock=None) -> fastapi.applications.FastAPI`, then `<repository root>\voice_storage` (V3C-7 met). The return annotation is in the plan's code; the expected evidence omitted it.
- Command 9: ` M .gitignore`, ` M voice_narration/simple_voices/application.py`, `?? voice_narration/simple_voices/recordings.py`, `?? voice_narration/simple_voices/store.py`, and `git diff --stat` reports `2 files changed, 77 insertions(+), 24 deletions(-)` for the tracked files. The applied OAM-3 changes are left in the working tree, uncommitted, for the user's decision.
- Pre-authorized contingencies: none listed, none applied.
- Deviations: none in the commands. To apply the plan's code, each code block was extracted with `sed` line ranges into the scratchpad, then copied with `cp` and applied with `git apply`, as Execution Step 3 suggests.
- Processes: the full suite ran as a background job, which exited. No container was started, because the engine was unreachable. Afterwards the only `python.exe` processes were PIDs 307936 and 307796, the unrelated `v11\Traffic` uvicorn. This run started no process that is still running.
- Minimum revision to resume: no `Plan.md` scope change is indicated. Either the user starts the Docker engine and re-approves this same Implementation Plan for a fresh command-4 run, or a revised Implementation Plan changes the V3C-4 accepted-failure rule for review.

## Risks

- **OAR-1 Tests write to tracked `audio_storage/`.** `tests/test_generation_history_download.py:18` builds an app over the default storage root (`voice_narration/inference/application.py:87-89`). The planning run modified `audio_storage/generation_index.json` and added a folder. Mitigation: OAV-3 after every backend run; new tests in OAM-2 and OAM-4 keep their own storage out of `audio_storage/`.
- **OAR-2 Cloned-generation retention is recorded only in the database, and failures there are ignored.** The expiry is written inside a block that swallows database errors (`voice_narration/inference/application.py:150-179`), and the database defaults to a local PostgreSQL instance (`voice_narration/inference/db.py:19-28`). Mitigation: the OAM-4 Implementation Plan shows how its test observes the 30-day expiry without a running PostgreSQL instance, as OAC-11 defines it.
- **OAR-3 Long generations held on one request.** The page waits on a single request for the whole generation (`frontend/src/services/ttsApi.ts:42-59`), and the inference service generates inside that request (`voice_narration/inference/application.py:438-479`). A Chatterbox call may last up to 1200 s, plus any wait (COA-9, COA-13). Mitigation: OAC-9 in OAM-1 defines how the page receives a long generation's result; OAM-8 exercises real cold starts.
- **OAR-4 Undeclared libraries.** The Google provider's client library and the Google authentication library, and the async test support used by the existing tests, are installed in the inspected environment but not declared in `requirements-dev.txt` (Current State). Mitigation: the OAM-4 and OAM-5 Implementation Plans name each installed library they rely on, and any declaration change, for review.
- **OAR-5 Hand-written multipart parsing in the voice service.** Upload extracts file bytes by splitting on line breaks (`voice_narration/simple_voices/application.py:83-103`), so a stored sample could differ from the uploaded bytes. Mitigation: OAM-2 verifies that a WAV upload's stored sample is byte-identical to the upload.
- **OAR-6 Pre-existing frontend failures overlap the cap tests.** M3.3.2 and M3.3.5, two of the label tests COA-17 changes, already fail because the test mock does not serve the provider list the page reads (Current State). Changing them cannot by itself give valid RED evidence. Mitigation: OAM-6 also checks the label's absence with a test that reaches the provider list. The named failures are treated as the user decides before each frontend Implementation Plan is approved (Non-Blocking Open Decisions).
- **OAR-7 Platform limits in front of Chatterbox.** The reference contract states that Cloud Run may answer on its own, for example when its request time limit is reached (reference contract, Inference Job Creation, failure reason table). Its configured limit is outside this work item (CON-3). Mitigation: such an answer is reported by the OAC-5 message for its cause; OAM-8 records any case it affects.

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| AC-1 On `/tts` the user can choose Google or Chatterbox, and the generation uses the chosen provider | requirements AC-1 | OAM-7 (page sends the choice) and OAM-5 (service uses it) |
| AC-2 A Chrome recording or WAV upload has its sample stored by the voice service | requirements AC-2 | OAM-3 |
| AC-3 With Chatterbox chosen, recorded and uploaded voices are listed and selectable | requirements AC-3 | OAM-7 |
| AC-4 A Chatterbox generation for a Chrome-recorded or WAV-uploaded voice plays on the TTS page, and the user hears the selected voice in the manual Cloud Run check | requirements AC-4 | OAM-5 and OAM-7 (automated, fake Chatterbox); OAM-8 (manual) |
| AC-5 English or Hindi can be chosen for Chatterbox, and the chosen language is used | requirements AC-5 | OAM-7 and OAM-5 (automated); OAM-8 (heard) |
| AC-6 Each of the nine causes produces its own message ending "Please retry, or choose another provider.", shown by automated tests against a fake Chatterbox | requirements AC-6 | OAM-5 (messages) and OAM-7 (shown on the page) |
| AC-7 When Chatterbox fails, no Google audio is produced | requirements AC-7 | OAM-5 |
| AC-8 The time limit is configurable, default 1200 s; exceeding it produces the timed-out message | requirements AC-8 | OAM-5 |
| AC-9 A cloned generation appears in history, can be downloaded and deleted, and has 30-day retention | requirements AC-9 | OAM-5 |
| AC-10 Voices and samples survive a restart and are deleted 5 days after upload | requirements AC-10 | OAM-3 |
| AC-11 Mock, Google and Azure and their existing tests pass unchanged; Google narration behaves as before apart from the cap | requirements AC-11 | OAM-5 (preserved backend tests) and OAM-7 (full frontend suite); Final Review inspection that those tests are unchanged |
| AC-12 A request made during a generation waits and then completes; the Generate button is disabled during a generation | requirements AC-12 | OAM-5 (waits) and OAM-7 (disabled button) |
| AC-13 For every provider, text over 5000 characters is kept and sent whole, unsplit; the count reads "n characters"; no "/ 5000", 90% warning, maximum-reached message or "Max 5000 chars/request" label | requirements AC-13 | OAM-7 |
| OAS-1 Tracked `audio_storage/` files are unchanged at the end of every milestone | User constraint (create-plan arguments, 2026-11-13) | OAV-3 evidence at OAM-2–OAM-7; Final Review inspection |
| OAS-2 Every full-suite run at OAM-3, OAM-5 and OAM-7 fails only on the pre-existing failures named in Current State | Plan; `implementation-planning` Pre-existing Failures | OAM-3, OAM-5, OAM-7 |
