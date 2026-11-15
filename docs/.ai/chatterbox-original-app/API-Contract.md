# API Contract — chatterbox-original-app

## Contract Scope

This contract defines the externally observable behavior of:

- the running voice service (`voice_narration.simple_voices`, `start-voice-service.bat:25`): its existing operations, carried over, and the changes this work item makes to sample storage, durability, retention and deletion, plus one added operation that returns a voice's stored sample;
- the inference service (`voice_narration.inference`): its existing operations, carried over, and the changes this work item makes to the generation operation (provider and language per generation, Chatterbox cloning, failure answers, waiting) and to the provider list;
- the request the inference service sends to the deployed Chatterbox;
- the settings operators set for the inference service.

It delivers milestone OAM-1 of `docs/.ai/chatterbox-original-app/Plan.md` (Status: Approved by Avinash Srivastava on 2026-11-13) under `docs/.ai/chatterbox-original-app/requirements.md` (Status: Approved by Avinash Srivastava on 2026-11-13). It resolves Plan decisions OAC-1–OAC-11.

The deployed Chatterbox's interface is a fixed constraint (CON-3, CON-5) and is not redefined here: this contract references the Chatterbox Synthesize and Chatterbox Caller Identity interfaces of the reference contract on `feature/voice-cloning` at `abbe387`, `docs/.ai/chatterbox-cloud-run/API-Contract.md` (Contract Review Status: Approved 2026-11-09), as the Plan directs (Requirements and Constraints). That contract's other sections and its labels are not adopted.

The TTS page's on-screen behavior (provider, voice and language choice, the text box, the counter, the labels, the disabled Generate button) is governed by the requirements (COA-1, COA-3, COA-5, COA-13, COA-17). This contract governs only what the page sends to and receives from the services.

Labels this contract introduces use the prefix `OAF-` (Chatterbox failure causes). No referenced approved artifact defines it. `OAC-` labels are the Plan's decision labels, cited, not redefined.

This contract governs externally observable behavior only. The approved Plan remains the single source of truth for scope, milestones, and requirement ownership.

## Baseline

No approved contract artifact describes the running voice service or the inference service's operations (Plan Current State, Contracts). The `initial-build` contract (`docs/.ai/initial-build/contract/API-Contract.md`) defines a different voices API that the launchers do not run; it is not the baseline and is not used. As Plan External Contract Requirements directs, the baseline is the current repository behavior.

- Baseline source: the repository at HEAD `8a5eaa6` on branch `claude/chatterbox-original-app-client-a3ef0e`: `voice_narration/simple_voices/application.py`, `voice_narration/simple_voices/__main__.py`, `voice_narration/inference/application.py`, `voice_narration/inference/__main__.py`, `voice_narration/inference/registry.py`, `voice_narration/inference/db.py`. `git diff --stat 664cee4 8a5eaa6` shows only `docs/.ai/chatterbox-original-app/Plan.md` and `requirements.md` changed, so the code is the code the Plan's Current State inspected at `664cee4`.
- Verified against: the repository on 2026-11-13. Checked:
  - Voice service routes: `GET /health` (`:70-73`), `POST /voice/upload` (`:75-127`), `GET /voices` (`:129-138`), `GET /voices/approved` (`:140-149`), `GET /voices/{voice_id}` (`:151-159`), `PATCH /voices/{voice_id}` (`:161-184`), `DELETE /voices/{voice_id}` (`:186-195`), `OPTIONS /{path}` and the CORS headers (`:197-217`); the five preloaded voices (`:13-63`); the in-memory store (`:10`); the upload's hand-parsed `name` and `file` parts (`:83-103`), its response fields (`:106-115`), and its discarding of the audio (`:111`).
  - Inference service routes: `POST /inference/jobs/{job_id}/infer` (`:438-479`), `GET /inference/jobs/{job_id}/output` (`:481-506`), `GET /inference/jobs/{job_id}/download` (`:508-527`), `GET /inference/generations` (`:529-554`), `GET /inference/generations/{job_id}` (`:556-569`), `DELETE /inference/generations/{job_id}` (`:571-582`), `GET /inference/backends` (`:584-609`); history entry fields (`:138-147`); listing order, filters and paging (`:199-218`); the database expiry (`:174`); the startup provider choice (`voice_narration/inference/__main__.py:33-58`); registered providers sorted by name (`voice_narration/inference/registry.py:60`, `:68-77`); `.env` loading (`voice_narration/inference/db.py:14-16`).
  - Clients in the repository: the TTS page sends only `script` and `voice_id` (`frontend/src/services/ttsApi.ts:42-52`) and reads `error` from failure bodies (`:54-57`); the recorder and the upload form send the parts `file` and `name` (`frontend/src/components/VoiceRecorder.tsx:159-161`, `frontend/src/components/VoiceUpload.tsx:264-265`); preserved tests call the generation operation with no provider and expect `200` (`tests/test_inference.py:50-60`, `:126-140`) and expect at least three listed providers including mock, Google and Azure (`:152-176`).
  - No published contract (OpenAPI or other) for these services is committed. No divergence between the repository and the Plan's description of it was found.

## Changes in This Work Item

| Change | Added / Changed / Removed | Requirement / Plan Reference |
| --- | --- | --- |
| `POST /voice/upload` keeps the uploaded `file` part as the voice's sample. A WebM recording is stored as WAV; any other content is stored byte-identical to the part as received | Changed | COA-2, COA-6, OAD-1; OAC-10 |
| `POST /voice/upload` answers `400` when a WebM recording cannot be converted to WAV, and creates no voice | Added | OAD-1; OAC-10 |
| `GET /voices/{voice_id}/sample` returns a voice's stored sample | Added | COA-2, COA-4; OAC-4 |
| Uploaded voices, their samples and their renames or status changes survive a restart of the voice service | Changed | COA-11; OAC-10 |
| Each uploaded voice and its sample are deleted, unrecoverably, 5 days after upload; from then on every voice operation treats the voice as unknown | Added | COA-11; OAC-10 |
| `DELETE /voices/{voice_id}` also deletes the voice's sample, unrecoverably | Changed | COA-11; OAC-10 |
| `POST /inference/jobs/{job_id}/infer` accepts optional `provider` (`google` or `chatterbox`) and `language` (`en` or `hi`, required for `chatterbox`) | Added | COA-1, COA-5; OAC-1, OAC-2 |
| `POST /inference/jobs/{job_id}/infer` answers `400` for an unsupported `provider` value, and for a missing or unsupported `language` in a Chatterbox generation | Added | COA-1, COA-5; OAC-1, OAC-2 |
| A Chatterbox generation is produced by the deployed Chatterbox with the text, the language and the voice's stored sample, and is saved like any other generation | Added | COA-1, COA-4, COA-10, CON-5; OAC-1, OAC-4, OAC-11 |
| A Chatterbox generation that fails answers `503` with one message per cause, OAF-1–OAF-9; nothing is generated by another provider and nothing is saved | Added | COA-7, COA-8; OAC-5 |
| The inference service runs one generation at a time; a generation request that arrives during another waits | Changed | COA-13; OAC-8 |
| A generation whose client stops waiting still completes, and a successful one is saved | Added | COA-9, COA-13; OAC-9 |
| `GET /inference/backends` also lists `chatterbox` | Added | COA-1; OAC-3 |
| Settings `CHATTERBOX_URL`, `CHATTERBOX_TIMEOUT_SECONDS` and `VOICE_SERVICE_URL`; the existing `GOOGLE_APPLICATION_CREDENTIALS` also names the key used for the Chatterbox identity token | Added | COA-7, COA-9, CON-5, CON-6; OAC-4, OAC-6, OAC-7 |

Everything else in this contract is carried over unchanged from the baseline.

## Out of Scope

- The deployed Chatterbox's own interface and deployment (CON-3, Explicit Exclusions): this contract references it and does not change it.
- Copying the Chatterbox service source into this branch (Explicit Exclusions, Q34).
- Per-user voice separation, and any authentication of callers of either local service. Neither service checks the `Authorization` header the page sends (baseline); this stays so (COA-15, Explicit Exclusions).
- A consent step or manual approval before cloning (COA-12, Explicit Exclusions).
- Falling back to Google, or to any other provider, when Chatterbox fails (COA-8, Explicit Exclusions).
- Duplicate prevention or duplicate detection of generation requests (COA-13).
- Any text length limit, and splitting text (COA-17). No operation in this contract limits text length.
- A sample size limit or a sample format check, other than the WebM conversion of OAD-1.
- A machine-readable failure-cause field. Clients tell causes apart by the `error` text only.
- A setting for where voices and samples are stored. The location is not contracted; samples are never stored where version control tracks them (CON-6, Plan OAM-3 exclusions).
- Deleting generations when their recorded expiry passes. The baseline records the expiry and deletes nothing; this work item does not change that.
- Logging, metrics and alerts (requirements Operational Characteristics: observability not required).
- The TTS page's on-screen behavior, governed by the requirements (see Contract Scope).

## Requirement Traceability

| Capability | Requirement / Plan Reference |
| --- | --- |
| Upload keeps the sample; WebM stored as WAV; other content stored as received | COA-2, COA-6, OAD-1, AC-2; OAC-10 |
| Upload answer when a WebM recording cannot be converted | OAD-1; OAC-10 |
| Automatic approval on upload, shared voice list (carried over) | COA-12, COA-15; OAC-10 |
| Voices and samples survive a restart | COA-11, AC-10; OAC-10 |
| 5-day retention of voices and samples | COA-11, AC-10; OAC-10 |
| Delete removes the sample | COA-11; OAC-10 |
| Sample operation used by the inference service | COA-2, COA-4; OAC-4 |
| Generation names its provider and, for Chatterbox, its language | COA-1, COA-5, AC-1, AC-5; OAC-1 |
| Generation with no provider or another provider | COA-1, COA-14; OAC-2 |
| Text of any length carried whole | COA-17, AC-13; OAC-1 |
| Chatterbox call with text, language, sample and identity token | COA-4, CON-5, AC-4; OAC-4, OAC-7 |
| One failure answer per cause, no fallback | COA-7, COA-8, AC-6, AC-7; OAC-5 |
| Configurable time limit, default 1200 s | COA-9, AC-8; OAC-6 |
| Settings for reaching Chatterbox and the voice service | COA-7, CON-5, CON-6; OAC-4, OAC-7 |
| One generation at a time; others wait | COA-13, AC-12; OAC-8 |
| Result delivered on the generation request | COA-4, COA-9, COA-13; OAC-9 |
| `chatterbox` in the provider list; mock, Google, Azure still listed | COA-1, COA-14, AC-11; OAC-3 |
| Cloned generations in history, download, delete, 30-day expiry recorded | COA-10, AC-9; OAC-11 |
| Google narration with Google voices unchanged | COA-14, AC-11 (carried over) |

## Interfaces

### Voice Service Health (HTTP)

Carried over unchanged.

- Purpose: report that the voice service is running.
- Related requirement: baseline.
- Endpoint: `/health`
- HTTP method: `GET`
- Required inputs: none.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON `{"status": "ok", "service": "voice-management"}`.
- Failure status codes: none defined.
- Failure response body: not applicable.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Voice Upload (HTTP)

- Purpose: create a voice from a recorded or uploaded sample, keeping the sample.
- Related requirement: COA-2, COA-6, COA-11, COA-12, COA-15, OAD-1; OAC-10.
- Endpoint: `/voice/upload`
- HTTP method: `POST`
- Required inputs: a `Content-Type` header containing `multipart/form-data` with a `boundary` parameter (carried over).
- Optional inputs (carried over):
  - `name` — a form field, the voice name. Absent, empty or only whitespace: `Unnamed Voice`. Otherwise the value with surrounding whitespace removed.
  - `file` — a file part holding the voice sample. Its file name and content type are not significant (OAD-1).
- Sample storage (changed, OAD-1):
  - When the `file` part's content is WebM audio, as Chrome's recorder produces, the voice's sample is a PCM WAV file holding that recording's audio. The content is recognized from the bytes, never from the file name (`recording.wav`) or the content type (`audio/wav`) the recorder sends. Sample rate and channel count are not contracted.
  - Any other non-empty `file` content (WAV, MP3, OGG or anything else) is stored as the sample byte-identical to the part's content as received. Only WAV and WebM samples are required to clone (COA-6).
  - When there is no `file` part, or it holds zero bytes, the voice is created with no sample (carried over: the baseline creates the voice). Its sample lookup answers `404` (Voice Sample).
- Success status code: `201` (carried over; the baseline sends no `Location` header and none is added).
- Success response body (carried over): JSON `{"id": <string>, "name": <string>, "format": "WAV", "duration": 45, "fileSize": <integer>, "uploadedAt": <string>, "status": "approved", "approvalScore": 95}`.
  - `id` is `voice-` followed by 8 lowercase hexadecimal characters, assigned by the service.
  - `format` is always `"WAV"` and `duration` always `45`, whatever the sample (carried over; informative only).
  - `fileSize` is the number of bytes in the `file` part as received, before any conversion; with no `file` part or an empty one, the number of bytes in the whole request body (carried over).
  - `uploadedAt` is the upload time on the voice service's clock, an ISO 8601 date-time without a time-zone offset (carried over). The 5-day retention is counted from it.
  - `status` `"approved"` and `approvalScore` `95`: every new voice is approved automatically and can be cloned straight away (COA-12, carried over).
- Failure status codes, in the order they are checked:
  1. `400`, `{"error": "Invalid content type"}` — the `Content-Type` header does not contain `multipart/form-data` (carried over).
  2. `400`, `{"error": "Upload failed: the recording could not be converted to WAV."}` — the `file` part is WebM but cannot be converted to WAV (added, OAD-1). No voice is created and nothing is stored.
  3. `500`, `{"error": "Upload failed: <text>"}` — any other error while handling the upload, for example a `multipart/form-data` content type with no `boundary` parameter (carried over).
- Failure response body: JSON `{"error": <string>}`. For failures 1 and 2 the whole string is normative. For failure 3 the prefix `Upload failed: ` is normative and the text after it is informative.
- Validation rules: as listed above. Form parts other than `name` and `file` are ignored, including parts named like server-assigned fields (`id`, `status`, `approvalScore`, `uploadedAt`) (carried over).
- Durability (changed, COA-11): the voice and its sample survive a restart of the voice service until deleted or expired.
- Retention (added, COA-11): see Voice Retention.
- Identity / existence behavior: not applicable. The operation takes no identifier.
- Mutation semantics: each successful call creates a new voice with a new `id`. Nothing existing is changed (carried over).

### Voice List (HTTP)

- Purpose: list every voice for every caller.
- Related requirement: COA-3, COA-11, COA-15; OAC-10.
- Endpoint: `/voices`
- HTTP method: `GET`
- Required inputs: none.
- Optional inputs: none. Query parameters are ignored (carried over).
- Success status code: `200`.
- Success response body (carried over): JSON `{"data": [<voice>, ...]}`. Each `<voice>` is the voice's stored representation with `status` set to `"approved"` and `approvalScore` set to its stored value or `95` when it has none.
  - The five preloaded voices carry `"provider": "google"`, `language`, `gender`, `approvalScore: 100` (carried over, `voice_narration/simple_voices/application.py:13-58`). Recorded and uploaded voices have the upload response's fields and no `provider` field. A client tells recorded and uploaded voices from the preloaded voices by the absence of `provider` (carried over; COA-3).
- Collection ordering: the preloaded voices first, in their fixed order, then the recorded and uploaded voices in upload order, oldest first. The same order holds after a restart (changed only in that it survives a restart; the baseline lists in insertion order).
- Collection contents: every caller receives every voice that is neither deleted nor expired; there is no per-user filter (COA-15, carried over). Expired voices are never listed (Voice Retention).
- Empty result: `{"data": []}`.
- Limits: none; no paging (carried over).
- Failure status codes: none defined.
- Failure response body: not applicable.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Approved Voice List (HTTP)

- Purpose: list the voices the TTS page offers (`frontend/src/services/ttsApi.ts:203-216`).
- Related requirement: COA-3, COA-15; OAC-10.
- Endpoint: `/voices/approved`
- HTTP method: `GET`
- Required inputs: none.
- Optional inputs: none. Query parameters are ignored (carried over).
- Success status code: `200`.
- Success response body (carried over): JSON `{"data": [<voice>, ...]}` — the voices whose stored `status` is `"approved"` or absent or empty, each with `status` set to `"approved"`. Ordering, contents, expiry, empty result and limits as for Voice List.
- Failure status codes: none defined.
- Failure response body: not applicable.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Voice Lookup (HTTP)

- Purpose: return one voice.
- Related requirement: COA-11; OAC-10.
- Endpoint: `/voices/{voice_id}`
- HTTP method: `GET`
- Required inputs: `voice_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON, the voice's stored representation, unmodified (carried over).
- Failure status codes: `404`, `{"error": "Voice not found"}` — no voice has that identifier, or it was deleted, or it has expired (Voice Retention).
- Failure response body: JSON `{"error": <string>}`; the whole string is normative.
- Validation rules: none.
- Identity / existence behavior: the identifier is matched exactly and case-sensitively. Its format is not checked, so a malformed identifier is answered as an unknown one, `404` (carried over).
- Mutation semantics: not applicable.

### Voice Update (HTTP)

- Purpose: rename a voice or change its stored status or score.
- Related requirement: COA-11; OAC-10.
- Endpoint: `/voices/{voice_id}`
- HTTP method: `PATCH`
- Required inputs: `voice_id` path segment; a JSON object body (carried over).
- Optional inputs (carried over): `name`, `status`, `approvalScore`. Each one present in the body replaces the stored value as given, whatever its value or type, including `null`. An absent field leaves the stored value unchanged.
- Success status code: `200`.
- Success response body: JSON, the voice's stored representation after the change (carried over).
- Failure status codes, in the order they are checked:
  1. `404`, `{"error": "Voice not found"}` — unknown, deleted or expired voice.
  2. `400`, `{"error": "Update failed: <text>"}` — the body is not valid JSON (carried over). A valid JSON body that is not an object is not contracted: the baseline answers `400` for some such values and `200` with no change for others (carried over, `voice_narration/simple_voices/application.py:170-184`).
- Failure response body: JSON `{"error": <string>}`. For `404` the whole string is normative; for `400` the prefix `Update failed: ` is normative.
- Validation rules: none beyond the above. Fields other than `name`, `status` and `approvalScore` are ignored (carried over).
- Identity / existence behavior: as for Voice Lookup.
- Mutation semantics: partial update of `name`, `status` and `approvalScore` (carried over). `id`, `uploadedAt`, `fileSize`, `format`, `duration` and the sample cannot be changed. An update to an uploaded voice survives a restart (changed, COA-11). An update does not change `uploadedAt`, so it does not extend retention. Updates to a preloaded voice last until the voice service restarts (see Voice Deletion).

### Voice Deletion (HTTP)

- Purpose: delete a voice and its sample.
- Related requirement: COA-11; OAC-10.
- Endpoint: `/voices/{voice_id}`
- HTTP method: `DELETE`
- Required inputs: `voice_id` path segment.
- Optional inputs: none.
- Success status code: `200` (carried over).
- Success response body: JSON `{"success": true}` (carried over).
- Failure status codes: `404`, `{"error": "Voice not found"}` — unknown, already deleted or expired voice (carried over for unknown).
- Failure response body: JSON `{"error": <string>}`; the whole string is normative.
- Validation rules: none.
- Identity / existence behavior: as for Voice Lookup. A second deletion of the same voice answers `404` (carried over).
- Mutation semantics: deleting an uploaded voice removes the voice and its sample permanently; neither can be recovered, including after a restart (changed, COA-11). The five preloaded voices are present again at every voice-service start, whether or not they were deleted or updated before it (carried over).

### Voice Sample (HTTP)

Added.

- Purpose: return a voice's stored sample, so the inference service can send it to Chatterbox.
- Related requirement: COA-2, COA-4, COA-12; OAC-4.
- Endpoint: `/voices/{voice_id}/sample`
- HTTP method: `GET`
- Required inputs: `voice_id` path segment.
- Optional inputs: none. Query parameters are ignored.
- Success status code: `200`.
- Success response body: the stored sample's bytes, exactly as stored (Voice Upload, Sample storage), with `Content-Type: application/octet-stream`. The body is never empty.
- Availability: a voice's sample can be fetched as soon as its upload has answered `201` (COA-12).
- Failure status codes, in the order they are checked:
  1. `404`, `{"error": "Voice not found"}` — unknown, deleted or expired voice.
  2. `404`, `{"error": "Voice sample not found"}` — the voice exists but has no sample: one of the five preloaded voices, or a voice uploaded with no `file` part or an empty one.
- Failure response body: JSON `{"error": <string>}`; the whole string is normative.
- Validation rules: none.
- Identity / existence behavior: as for Voice Lookup.
- Mutation semantics: not applicable. The operation changes nothing; it does not extend retention.

### Voice Retention (rule for every voice-service operation)

Added (COA-11, OAC-10).

- An uploaded voice expires 5 days (120 hours) after its `uploadedAt`, on the voice service's clock.
- From that moment every voice-service operation treats the voice as unknown: it is not listed, and Voice Lookup, Voice Update, Voice Deletion and Voice Sample answer `404 {"error": "Voice not found"}`.
- The voice and its sample are removed permanently no later than the first voice-service request, or the first voice-service start, after that moment. They cannot be recovered.
- The five preloaded voices do not expire.
- Expiry also applies to any voice uploaded before a restart; time while the service is stopped counts.

### Voice Service Cross-Origin Requests (HTTP)

Carried over unchanged: every voice-service response carries `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS` and `Access-Control-Allow-Headers: Content-Type, Authorization`, and `OPTIONS` on any path answers `200` with body `{}`. The Voice Sample operation is covered by the same rule.

### Inference Generation (HTTP)

- Purpose: generate speech for a text with the provider the request names, save it, and answer when it is ready or has failed.
- Related requirement: COA-1, COA-4, COA-5, COA-7, COA-8, COA-9, COA-10, COA-13, COA-14, COA-17, CON-5; OAC-1, OAC-2, OAC-4, OAC-5, OAC-8, OAC-9, OAC-11.
- Endpoint: `/inference/jobs/{job_id}/infer`
- HTTP method: `POST`
- Required inputs: `job_id` path segment, chosen by the client (carried over); a JSON object body with:
  - `script` — the text to speak (carried over). There is no length limit; the text is used whole and unsplit, exactly as received, for every provider (COA-17).
  - `voice_id` — the voice identifier (carried over). For Google, a Google voice name such as `en-US-Neural2-A`. For Chatterbox, the `id` of a recorded or uploaded voice in the voice service.
- Optional inputs:
  - `provider` (added, COA-1) — which provider generates this request:
    - absent, `null`, or the empty string `""`: the provider the inference service was started with (`INFERENCE_PROVIDER`, carried over; see Inference Service Settings). Existing clients that send no `provider` behave exactly as before;
    - `"google"`: the same as absent. The generation is produced by the startup provider, which is Google when the service was started with `INFERENCE_PROVIDER=google` and the Google provider initialized. When the service fell back to the mock at startup, a `"google"` generation is produced by the mock, as every generation is today (carried over, COA-14);
    - `"chatterbox"`: the deployed Chatterbox (see Inference Service Chatterbox Call);
    - any other value, including `"mock"`, `"azure"`, whitespace, a different letter case, or a value that is not a string: rejected with `400` (failure 3 below).
  - `language` (added, COA-5) — required when `provider` is `"chatterbox"`: exactly `"en"` (English) or `"hi"` (Hindi). For any other provider, `language` is ignored, whatever its value or type; Google derives the language from the voice name (carried over, `voice_narration/inference/providers/google_tts.py:106-107`).
- Success status code: `200` (carried over).
- Success response body (carried over): JSON `{"job_id": <string>, "status": "complete", "duration_seconds": <number>}`. The audio is then available from Inference Generation Download, Inference Generation Output and the history (Inference Generation History).
- Failure status codes, in the order they are checked (the first that applies is answered):
  1. `500`, `{"error": "Inference failed: <text>"}` — the body is not valid JSON, or is valid JSON but not an object (carried over).
  2. `400`, `{"error": "Missing required fields: script, voice_id"}` — `script` or `voice_id` is absent, `null`, an empty string, or another value that is false in JSON terms (`0`, `false`, `[]`, `{}`) (carried over). A `script` of only whitespace is not rejected here.
  3. `400`, `{"error": "Unsupported provider. Choose google or chatterbox."}` — `provider` is present and is not `null`, `""`, `"google"` or `"chatterbox"` (added, OAC-2).
  4. `400`, `{"error": "language must be en or hi for a chatterbox generation."}` — `provider` is `"chatterbox"` and `language` is absent, `null`, or anything other than exactly `"en"` or `"hi"` (added, COA-5).
  5. Waiting (added, OAC-8): from here on the request waits until no other generation is running (see Generation Waiting).
  6. Chatterbox generations only: `503` with the message of the first applicable cause OAF-1–OAF-9 (see Chatterbox Failure Causes) (added, COA-7).
  7. Startup-provider generations only: `400`, `{"error": "<text>"}` — the provider rejected its input with a value error (carried over); `500`, `{"error": "Inference failed: <text>"}` — any other provider error, including Google rejecting long text (carried over; COA-17: "the error the app shows for a failed Google generation").
- Failure response body: JSON `{"error": <string>}`. For failures 2, 3 and 4 and for every OAF message the whole string is normative, with `<N>` and `<status>` filled in. For failure 1 and failure 7 `500`, the prefix `Inference failed: ` is normative and the text after it is informative. For failure 7 `400`, only the status code is normative.
- Validation rules: as listed above. A non-string `script` or `voice_id` that passes check 2 is not otherwise validated; the result is not contracted (carried over). Fields other than `script`, `voice_id`, `provider` and `language` are ignored, including `job_id`, `status` or `duration_seconds` supplied in the body (carried over).
- Result delivery (OAC-9, carried over): the result or failure is the answer to this same request. The request stays open while it waits and while the generation runs, with no limit set by the inference service other than the Chatterbox time limit on the Chatterbox call itself. A client that stops waiting does not cancel the generation: it still completes, and a successful generation is saved and appears in history (COA-10). Limits that a browser or other client places on how long a request may stay open are outside this contract.
- No fallback (COA-8): a Chatterbox generation is never produced by Google or any other provider. When it fails, nothing is generated by another provider, no audio file is written, and no history entry is created or changed; an existing history entry with the same `job_id` stays as it was.
- Saving a success (OAC-11, carried over for every provider): the audio is saved under the inference service's audio storage and recorded as a history entry with `job_id`, `text` (the `script`), `voice_id`, `duration_seconds`, `file_path`, `format` `"wav"`, `status` `"complete"` and `created_at`. It is also written to the database with an expiry of `created_at` plus `AUDIO_RETENTION_DAYS` days (default 30), as every generation is; a database failure does not fail the generation (carried over, `voice_narration/inference/application.py:150-179`).
- Identity / existence behavior: `job_id` is not looked up; any non-empty path segment is accepted (carried over). An empty segment (`/inference/jobs//infer`) does not match the route and is answered by the framework with `404` or `405` (carried over, `tests/test_inference.py:210-222`). For a Chatterbox generation, a `voice_id` that is unknown, deleted, expired, or has no sample is answered OAF-3; there is no separate malformed-identifier answer, because the identifier's format is not checked. For startup-provider generations, `voice_id` handling is carried over (the provider decides).
- Mutation semantics (carried over): a successful call saves the generation under `job_id`. A later successful call with the same `job_id` replaces that history entry. A failed call changes nothing.

### Generation Waiting (rule for Inference Generation)

Added (COA-13, OAC-8).

- The inference service runs one generation at a time, for every provider.
- A generation request that passes checks 1–4 while another generation is running waits until no generation is running, then runs. It is never rejected for being busy. There is no limit on how long it waits or how many requests wait. The order in which waiting requests run is not specified; the requirements state none.
- Requests answered by checks 1–4 are answered without waiting.
- Waiting does not count toward the Chatterbox time limit (Inference Service Chatterbox Call).
- This contract makes no statement about whether other operations are answered while a generation runs.

### Inference Service Chatterbox Call (outbound HTTP from the inference service to Chatterbox)

Added. The request the inference service sends for a Chatterbox generation, to the deployed Chatterbox's Synthesize operation as the reference contract's Chatterbox Synthesize and Chatterbox Caller Identity define it (CON-3, CON-5).

- Purpose: obtain speech in the selected voice from the deployed Chatterbox.
- Related requirement: COA-4, COA-5, COA-9, COA-17, CON-5; OAC-4, OAC-6, OAC-7.
- Steps, in order, each answered by its OAF cause when it fails:
  1. The Chatterbox URL in effect must be non-empty (OAF-1), and the time limit setting valid (OAF-2) (Inference Service Settings).
  2. The inference service fetches the voice's sample from the voice service: `GET <voice service URL in effect>/voices/<voice_id>/sample`. Only a `200` answer with a non-empty body provides the sample. Any other answer, or no answer, is OAF-3. This fetch is not bounded by the Chatterbox time limit.
  3. It obtains a Google-signed OpenID Connect identity token for the service account of the key file named by `GOOGLE_APPLICATION_CREDENTIALS`, with its audience equal to the Chatterbox URL in effect (CON-5). Failure is OAF-4. This step is not bounded by the Chatterbox time limit. The inference service does not check which account the key belongs to; a key for any account other than `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` is rejected by Cloud Run, which is OAF-7.
  4. It sends `POST <Chatterbox URL in effect>/v1/synthesize` with `multipart/form-data`:
     - `text` — the `script`, whole, unsplit and unchanged, of any length (COA-17);
     - `language` — the request's `language`, `en` or `hi` (COA-5);
     - `sample_audio` — a file part holding the fetched sample bytes, unchanged; its file name and content type are not significant to Chatterbox;
     - header `Authorization: Bearer <token>`.
     Redirects are not followed.
- Time limit (COA-9): the call in step 4 is bounded by the time limit in effect, measured from when the inference service starts sending the request until it has received the complete response. Time Chatterbox or Cloud Run spends before answering, including a cold start or a wait at Chatterbox, counts. When the limit is reached the inference service stops waiting: OAF-5.
- Success: a `200` answer whose `Content-Type` media type is `audio/wav` (compared case-insensitively, parameters ignored) and whose body is a readable WAV file. The body becomes the generation's audio, unchanged, and is saved as Inference Generation describes. `duration_seconds` is the WAV's number of sample frames divided by its sample rate, as a JSON number, not rounded.
- Anything else is a failure, answered as OAF-6–OAF-9.

### Chatterbox Failure Causes (rule for Inference Generation)

Added (COA-7, OAC-5). Every cause answers `503` with JSON `{"error": "<message>"}`. Causes are checked in the order listed; the first that applies is answered. Each message ends with "Please retry, or choose another provider." (COA-7).

| Cause | Condition | `error` |
| --- | --- | --- |
| OAF-1 Not configured | The Chatterbox URL in effect is empty: `CHATTERBOX_URL` absent, empty or only whitespace. | `Chatterbox voice cloning is not configured. Please retry, or choose another provider.` |
| OAF-2 Invalid time-limit setting | `CHATTERBOX_TIMEOUT_SECONDS` is set to a value that is not empty, not only whitespace, and not a positive whole number of seconds. | `The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; it must be a positive whole number of seconds. Please retry, or choose another provider.` |
| OAF-3 Voice sample unreadable | The voice service did not provide the sample: the voice is unknown, deleted or expired, has no sample, the voice service answered anything other than `200` with a non-empty body, or could not be reached. | `The voice sample for the selected voice could not be read. Please retry, or choose another provider.` |
| OAF-4 Identity token unavailable | No identity token could be obtained: `GOOGLE_APPLICATION_CREDENTIALS` absent or blank, the key file missing or unreadable or not a service-account key, or the token request to Google failed. | `Could not obtain an identity token for Chatterbox. Please retry, or choose another provider.` |
| OAF-5 Timed out | The Chatterbox call did not complete within the time limit in effect. | `Chatterbox did not respond within <N> seconds. Please retry, or choose another provider.` where `<N>` is the time limit in effect as a whole number |
| OAF-6 Cannot connect | Any transport failure other than OAF-5: for example a URL that cannot be used, name resolution failure, connection refused, TLS failure, or the connection lost before the complete response. | `Could not connect to Chatterbox. Please retry, or choose another provider.` |
| OAF-7 Access denied | Chatterbox, or Cloud Run in front of it, answered `401` or `403`. | `Access to Chatterbox was denied (HTTP <status>). Please retry, or choose another provider.` where `<status>` is the status code received |
| OAF-8 Service error | Any other status than `200`, `401` or `403`, including Chatterbox's `400`, `422`, `500` and `503`, any status Cloud Run answers on its own (for example `429` or `504`, OAR-7), and any redirect status. | `Chatterbox returned an error (HTTP <status>). Please retry, or choose another provider.` where `<status>` is the status code received |
| OAF-9 Not audio | `200` with an empty body, a `Content-Type` whose media type is not `audio/wav`, or a body that is not a readable WAV file. | `Chatterbox returned a response that is not audio. Please retry, or choose another provider.` |

### Inference Generation Output (HTTP)

Carried over unchanged; applies to Chatterbox generations as to every other.

- Purpose: return the audio of a generation made since the inference service started.
- Related requirement: COA-4 (carried over).
- Endpoint: `/inference/jobs/{job_id}/output`
- HTTP method: `GET`
- Required inputs: `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON `{"audio_bytes": <base64 string>, "format": <string>, "duration_seconds": <number>}`.
- Failure status codes: `404`, `{"error": "Job <job_id> not found or no output available"}` — no generation with that `job_id` was made since the service started; `500`, `{"error": "Output retrieval failed: <text>"}` — any other error.
- Failure response body: JSON `{"error": <string>}`; for `404` the whole string with `<job_id>` filled in is normative; for `500` the prefix is normative.
- Validation rules: none.
- Identity / existence behavior: exact match on `job_id`; no format check, so a malformed identifier is answered `404`.
- Mutation semantics: not applicable.

### Inference Generation Download (HTTP)

Carried over unchanged; applies to cloned generations (COA-10, OAC-11).

- Purpose: download a generation's audio.
- Related requirement: COA-10.
- Endpoint: `/inference/jobs/{job_id}/download`
- HTTP method: `GET`
- Required inputs: `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: the audio bytes, `Content-Type: audio/wav`, `Content-Disposition: attachment; filename="<voice_id>_<job_id>.wav"` (`generation_<job_id>.wav` when no history entry exists).
- Failure status codes: `404`, `{"error": "Job <job_id> not found or no output available"}` — no saved file and no generation since start; `500`, `{"error": <text>}` — any other error.
- Failure response body: JSON `{"error": <string>}`; for `404` the whole string is normative; for `500` only the status code.
- Validation rules: none.
- Identity / existence behavior: as for Inference Generation Output.
- Mutation semantics: not applicable.

### Inference Generation History (HTTP)

Carried over unchanged; cloned generations appear in it like any other (COA-10, OAC-11).

- Purpose: list saved generations.
- Related requirement: COA-10.
- Endpoint: `/inference/generations`
- HTTP method: `GET`
- Required inputs: none.
- Optional inputs (query): `skip` (integer, default `0`, values below `0` become `0`), `limit` (integer, default `20`, clamped to `1`–`100`), `voice_id`, `created_at_from`, `created_at_to`, `search`. An absent or empty filter is not applied.
- Success status code: `200`.
- Success response body: JSON `{"items": [<entry>, ...], "total": <integer>, "skip": <integer>, "limit": <integer>}`, where each `<entry>` has the fields listed under Inference Generation, Saving a success, and `total` counts the entries after filtering and before paging.
- Collection ordering: newest `created_at` first. Empty result: `items` `[]`, `total` `0`.
- Matching and filtering: `voice_id` exact, case-sensitive; `created_at_from` and `created_at_to` compared as text against `created_at`, inclusive; `search` a case-insensitive substring of `text`.
- Failure status codes: `400`, `{"error": <text>}` — `skip` or `limit` is not an integer; `500`, `{"error": "History listing failed: <text>"}`.
- Failure response body: JSON `{"error": <string>}`; only the status code and, for `500`, the prefix are normative.
- Validation rules: as above. Other query parameters are ignored.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Inference Generation Detail (HTTP)

Carried over unchanged.

- Purpose: return one saved generation's history entry.
- Related requirement: COA-10.
- Endpoint: `/inference/generations/{job_id}`
- HTTP method: `GET`
- Required inputs: `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON, the history entry.
- Failure status codes: `404`, `{"error": "Generation <job_id> not found"}`; `500`, `{"error": "Generation lookup failed: <text>"}`.
- Failure response body: JSON `{"error": <string>}`; for `404` the whole string is normative; for `500` the prefix.
- Validation rules: none.
- Identity / existence behavior: exact match; a malformed identifier is answered `404`.
- Mutation semantics: not applicable.

### Inference Generation Deletion (HTTP)

Carried over unchanged; applies to cloned generations (COA-10, OAC-11).

- Purpose: delete a saved generation and its audio.
- Related requirement: COA-10.
- Endpoint: `/inference/generations/{job_id}`
- HTTP method: `DELETE`
- Required inputs: `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`, also for a `job_id` that has no generation (carried over).
- Success response body: JSON `{"job_id": <string>, "deleted": true}`.
- Failure status codes: `500`, `{"error": "Generation deletion failed: <text>"}`.
- Failure response body: JSON `{"error": <string>}`; the prefix is normative.
- Validation rules: none.
- Identity / existence behavior: unknown and malformed identifiers are both answered `200` (carried over).
- Mutation semantics: removes the history entry, its audio file, the in-memory output and the database record. A repeat is answered the same way.

### Inference Provider List (HTTP)

- Purpose: list the providers the TTS page offers (`frontend/src/services/ttsApi.ts:182-201`).
- Related requirement: COA-1, COA-14; OAC-3.
- Endpoint: `/inference/backends`
- HTTP method: `GET`
- Required inputs: none.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON `{"backends": [{"name": <string>, "provider_class": <string>, "description": <string>}, ...]}`.
  - `azure`, `google` and `mock` are listed with their baseline `description` (carried over).
  - `chatterbox` is listed with `description` `"Chatterbox voice cloning (deployed Cloud Run service)"` (added). It is listed whether or not the Chatterbox settings are set; a generation with missing settings answers OAF-1 or OAF-4.
  - `provider_class` is a non-empty string; its value is informative.
  - The text of `description` before the first ` (` is the display name the page derives (carried over, `frontend/src/services/ttsApi.ts:197`); for Chatterbox it is `Chatterbox voice cloning`.
- Collection ordering: ascending by `name` (carried over): `azure`, `chatterbox`, `google`, `mock`.
- Empty result: not applicable; the list always holds these four.
- Failure status codes: `500`, `{"error": "Backend listing failed: <text>"}` (carried over).
- Failure response body: JSON `{"error": <string>}`; the prefix is normative.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.
- Listing a provider does not make it selectable per generation: Inference Generation accepts only `google` and `chatterbox` as `provider` (OAC-2).

### Inference Service Cross-Origin Requests (HTTP)

Carried over unchanged: the inference service allows every origin, method and header, with credentials allowed.

### Inference Service Settings (operator-set configuration)

Environment variables the inference service reads. Values set in the process environment take precedence; the inference service also loads `.env`, `.env.local` and `.env.production` from the repository root without overriding values already set (carried over, `voice_narration/inference/db.py:14-16`). These files and the key file are gitignored and never committed (CON-6). Unless stated otherwise, a setting is read when the inference application is created at service start; a change takes effect after a restart.

| Setting | Form | Absent / blank | Status |
| --- | --- | --- | --- |
| `CHATTERBOX_URL` | Absolute URL of the deployed Chatterbox, for example `https://chatterbox-model-api-177206684903.asia-southeast1.run.app` (CON-5). Surrounding whitespace and trailing `/` characters are removed; the result is the Chatterbox URL in effect, used both to build the call URL and as the identity token's audience, which CON-5 requires to be exactly the service URL. The value's form is not otherwise checked; a URL that cannot be used is OAF-6. | Absent, empty or only whitespace: the Chatterbox URL in effect is empty, and every Chatterbox generation answers OAF-1. Other providers are unaffected. | Added (OAC-7) |
| `CHATTERBOX_TIMEOUT_SECONDS` | A positive whole number of seconds: after removing surrounding whitespace, decimal digits only, value at least `1`. No upper bound. | Absent, empty or only whitespace: `1200` (COA-9). Any other value that is not a positive whole number (for example `0`, `-5`, `10.5`, `ten`) makes every Chatterbox generation answer OAF-2; the service still starts, and other providers are unaffected. | Added (OAC-6) |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a service-account key file, absolute or relative to the inference service's working directory. For Chatterbox it must be the key of `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` (CON-5). The key file is read when an identity token is needed. | Absent or blank: no identity token can be obtained, and every Chatterbox generation answers OAF-4. | Existing setting, read by the Google provider (carried over); newly also used for the Chatterbox identity token (OAC-7) |
| `VOICE_SERVICE_URL` | Base URL of the voice service. Surrounding whitespace and trailing `/` characters are removed. | Absent, empty or only whitespace: `http://localhost:8002`, the voice service's default address (`voice_narration/simple_voices/__main__.py:18`, `.env.example:10`). | Added (OAC-4); the name already appears in `.env.example:10`, which no code reads at baseline |
| `INFERENCE_PROVIDER` | `google`, `azure`, `mock` or any other value. | Carried over: `google` starts with the Google provider, or with the mock when Google cannot be initialized; any other value, absent or blank starts with the mock. This is the startup provider used for generations with no `provider` or `provider` `"google"`. | Carried over unchanged |
| `AUDIO_RETENTION_DAYS` | Whole number of days. Read at each save. | Absent: `30` (COA-10). | Carried over unchanged |
| `AUDIO_STORAGE_PATH`, `DATABASE_URL`, `INFERENCE_HOST`, `INFERENCE_PORT` | As in the baseline. | As in the baseline. | Carried over unchanged |

No setting disables the identity token; it is attached to every Chatterbox call. The voice service gains no setting (`VOICE_SERVICE_PORT` is carried over unchanged).

## Contract-Wide Rules

- Input parsing and type errors:
  - Voice Upload: a request whose `Content-Type` is not `multipart/form-data` answers `400 Invalid content type`; one that cannot otherwise be parsed answers `500 Upload failed: <text>` (carried over).
  - Voice Update: a body that is not valid JSON answers `400 Update failed: <text>`; a valid JSON body that is not an object is not contracted (carried over).
  - Inference Generation: a body that is not a JSON object answers `500 Inference failed: <text>` (carried over). `provider` and `language` of a type other than string, when they are checked, are rejected with their `400` (failures 3 and 4). Non-string `script` and `voice_id` are not contracted beyond check 2 (carried over).
  - Inference Generation History: a non-integer `skip` or `limit` answers `400` (carried over).
  - Path segments are strings and have no format; no path parameter has a type error.
- Absent / null / empty / blank values: stated per field. In summary: upload `name` absent or blank becomes `Unnamed Voice`; an absent or empty `file` gives a voice with no sample; `script` and `voice_id` absent, `null` or empty answer `400`, and whitespace-only `script` is accepted; `provider` absent, `null` or `""` means the startup provider; `language` absent, `null` or empty answers `400` for Chatterbox and is ignored otherwise; settings as in the settings table; a history filter that is absent or empty is not applied.
- Read-only and unknown request fields: server-assigned fields supplied by the client (`id`, `status`, `approvalScore`, `uploadedAt` on upload; `job_id`, `status`, `duration_seconds` in a generation body) are ignored. Undefined fields, form parts and query parameters are ignored by every operation. `status` and `approvalScore` are writable through Voice Update (carried over).
- Numeric semantics: `fileSize` is an integer byte count of the uploaded part before conversion. `duration` `45` and `approvalScore` `95` are fixed values (carried over). `duration_seconds` of a Chatterbox generation is sample frames divided by sample rate, a JSON number, not rounded; for other providers it is carried over from the provider. `CHATTERBOX_TIMEOUT_SECONDS` is a whole number of seconds and is not rounded; a fractional value is invalid (OAF-2). `<N>` in OAF-5 is written as a whole number. Voice retention is exactly 120 hours from `uploadedAt`; generation expiry is `created_at` plus `AUDIO_RETENTION_DAYS` whole days. There are no monetary values.
- Collection ordering, empty results, limits: Voice List and Approved Voice List — preloaded voices in fixed order, then uploaded voices oldest first, empty `{"data": []}`, no limit. Inference Generation History — newest first, empty `items: []`, `limit` clamped to `1`–`100`. Inference Provider List — ascending by `name`, always four entries. No other operation returns a collection.
- Matching and filtering semantics: voice identifiers and `job_id` are matched exactly and case-sensitively. `provider` matches exactly `"google"` or `"chatterbox"`, and `language` exactly `"en"` or `"hi"`, case-sensitive with no trimming. WebM content is recognized from the bytes. The Chatterbox success `Content-Type` check is case-insensitive on the media type with parameters ignored. History filters as stated in Inference Generation History.
- Error response shape and which parts are normative: every application-generated error of both services is JSON `{"error": <string>}` (carried over; the TTS page reads `error`, `frontend/src/services/ttsApi.ts:54-57`). Normative parts are stated per operation: the whole string for every error this work item adds and for the fixed carried-over strings; only the prefix where carried-over errors embed exception text. Answers the web framework generates itself (an unmatched route or method) carry its own body; only their status code is normative.
- Versioning and compatibility of message or RPC schemas: not applicable. There are no message or RPC interfaces, and the HTTP operations are not versioned (carried over). HTTP compatibility is described under Compatibility Notes.

## Decisions Resolved

| Decision | Resolution | Source |
| --- | --- | --- |
| OAC-1 How a generation request names its provider and language, and carries text of any length | Optional JSON fields `provider` (`"google"` or `"chatterbox"`) and `language` (exactly `"en"` or `"hi"`, required for `"chatterbox"`, ignored otherwise) on the existing `POST /inference/jobs/{job_id}/infer`. `script` has no length limit and is used whole, unsplit and unchanged for every provider. `"google"` is produced by the startup provider, which is Google when the service started with Google; when the service fell back to the mock at startup, the mock produces it, as today. | Proposed — deferred by Plan OAC-1 (COA-1, COA-5, COA-17; Google behavior kept as now, COA-14) |
| OAC-2 No provider, or a provider other than Google or Chatterbox | Absent, `null` or `""`: the startup provider, exactly as before, so existing clients and the preserved tests are unaffected. Any other value, including `"mock"` and `"azure"`: `400 Unsupported provider. Choose google or chatterbox.` The mock and Azure providers themselves are unchanged. | Proposed — deferred by Plan OAC-2 (COA-1, COA-14) |
| OAC-3 Chatterbox in the provider list | `GET /inference/backends` adds `{"name": "chatterbox", "description": "Chatterbox voice cloning (deployed Cloud Run service)", "provider_class": <string>}`, always listed. `azure`, `google`, `mock` stay as they are; order stays ascending by name. | Proposed — deferred by Plan OAC-3 (COA-1, COA-14, `tests/test_inference.py:152-176`) |
| OAC-4 How the inference service obtains a voice's sample; unknown, expired, sample-less voices | Added voice-service operation `GET /voices/{voice_id}/sample` returning the stored bytes (`application/octet-stream`), `404 Voice not found` for unknown, deleted or expired voices and `404 Voice sample not found` for voices with no sample. The inference service reaches it at `VOICE_SERVICE_URL` (default `http://localhost:8002`). Any failure to get a non-empty `200` sample, including the voice service being unreachable, is OAF-3. | Proposed — deferred by Plan OAC-4 (COA-2, COA-4, COA-7); setting name from `.env.example:10` |
| OAC-5 The nine failure causes: answer, wording, order | OAF-1–OAF-9, each `503` with `{"error": <message>}`, worded as in Chatterbox Failure Causes, each ending "Please retry, or choose another provider.", checked in the listed order: settings (OAF-1, OAF-2), sample (OAF-3), token (OAF-4), then the call's outcome (OAF-5–OAF-9). No other provider is tried. | Nine causes and closing sentence: COA-7, AC-6; no fallback: COA-8. Status, wording and order: Proposed — deferred by Plan OAC-5 |
| OAC-6 The time-limit setting | `CHATTERBOX_TIMEOUT_SECONDS`, a positive whole number of seconds, read at service start. Absent or blank: `1200`. Any other non-positive-whole-number value: every Chatterbox generation answers OAF-2. It bounds the Chatterbox call from the start of sending until the complete response, including cold start and any wait at Chatterbox; not the wait in the inference service, the sample fetch, or obtaining the token. On expiry: OAF-5. | Default 1200 s and configurable: COA-9, AC-8. Name, form, invalid values, when read, span: Proposed — deferred by Plan OAC-6 |
| OAC-7 Settings to reach the deployed Chatterbox | `CHATTERBOX_URL` (trimmed, trailing `/` removed; used as the call base and the token audience). Absent or blank: OAF-1. The identity token is obtained from the key named by the existing `GOOGLE_APPLICATION_CREDENTIALS`; absent or blank, or any failure to obtain a token: OAF-4. No setting disables the token. | Account and audience: CON-5. Key files never committed: CON-6. Names, forms, reuse of `GOOGLE_APPLICATION_CREDENTIALS`, absent/blank handling: Proposed — deferred by Plan OAC-7 |
| OAC-8 How a request arriving during a generation waits | One generation at a time, for every provider. A request that passes input validation waits, unbounded and never rejected for being busy, then runs. Waiting order unspecified. Validation failures are answered without waiting. Waiting does not count toward the time limit. | A request that arrives during a generation waits: COA-13, AC-12. Providers covered, unbounded wait, validation before waiting, not counted: Proposed — deferred by Plan OAC-8 |
| OAC-9 How the TTS page receives a long generation's result | On the same generation request, as today: the request stays open while waiting and generating, with no inference-service limit other than the Chatterbox time limit. A client that stops waiting does not cancel the generation; a successful one is still saved and appears in history. Browser limits on how long a request may stay open are outside this contract (see Compatibility Notes). | Proposed — deferred by Plan OAC-9 (COA-4, COA-9, COA-13; Plan OAR-3) |
| OAC-10 Voice-service changes | Upload keeps the `file` part as the sample: WebM recognized from the bytes and stored as PCM WAV; any other content stored byte-identical; a WebM that cannot be converted answers `400 Upload failed: the recording could not be converted to WAV.` and creates no voice. Response shape, `201`, automatic approval and the shared list carried over. Uploaded voices, samples and updates survive restarts. Voices expire 120 hours after `uploadedAt`: treated as unknown (`404 Voice not found`) from then on, removed permanently no later than the next request or start. Delete removes the sample permanently. Preloaded voices never expire and return at every start. List order: preloaded, then uploads oldest first. | Sample kept: COA-2. WebM as WAV, others as received: OAD-1, COA-6. 5 days, unrecoverable, survive restart: COA-11. Automatic approval: COA-12. Shared list: COA-15. Conversion-failure answer, expiry semantics, removal timing, list order, preloaded voices: Proposed — deferred by Plan OAC-10 |
| OAC-11 Cloned generations in history, download, delete, 30-day retention | A successful Chatterbox generation is saved and recorded exactly as any other generation: same history entry fields, same download and deletion operations, same database expiry of `created_at` plus `AUDIO_RETENTION_DAYS` (default 30) days. No field is added to the history entry. A failed one saves nothing. | History, download, delete: COA-10, AC-9. 30-day retention: COA-10 (existing `AUDIO_RETENTION_DAYS`). Same record, no added field, nothing saved on failure: Proposed — deferred by Plan OAC-11 (COA-8) |

## Compatibility Notes

- Existing callers of Inference Generation that send no `provider` (the current TTS page, `frontend/src/services/ttsApi.ts:42-52`, and the preserved tests) get the same behavior as before, except that a generation request now waits while another generation runs (COA-13). A caller that sends a `provider` value other than `google` or `chatterbox` previously had it ignored and now receives `400`; no client in the repository sends `provider` (COA-1).
- The provider list gains one entry; clients that require at least three entries including `mock`, `google` and `azure` (`tests/test_inference.py:152-176`) are unaffected.
- The voice upload's response shape and status are unchanged. Upload now fails with `400` for a WebM recording that cannot be converted, where the baseline always created the voice.
- Uploaded voices now survive restarts and now disappear 5 days after upload (COA-11); clients that relied on a restart clearing voices see them persist.
- Deleting a voice now also removes its sample permanently.
- Google narration with Google voices is unchanged (COA-14), including the error answer when Google rejects long text (COA-17).
- A generation may hold its request open for the wait plus up to the Chatterbox time limit (default 1200 s) plus the sample fetch and token time. Whether a browser keeps a request open that long is outside the services' control (Plan OAR-3); when a client gives up, a successful generation still appears in history. OAM-8 exercises real cold starts.

## Contract Review Status

- Status: Approved by Avinash Srivastava on 2026-11-13, as written, accepting every resolution marked `Proposed — deferred by Plan OAC-n`.
- Human review required before implementation planning that depends on this contract. On approval the user replaces the status with `Approved by <name> on <date>`, and the CONTRACT milestone's row in `Plan.md` Execution Status is marked complete, pointing to this contract. Approval accepts every resolution marked `Proposed — deferred by Plan OAC-n` in Decisions Resolved.
