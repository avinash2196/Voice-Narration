# API Contract — chatterbox-cloud-run

## Contract Scope

This contract defines the externally observable behavior of:

- the Chatterbox model API (`GET /health`, `GET /v1/metadata`, `POST /v1/synthesize`), with the synthesize request changed to carry the voice sample audio instead of a file path;
- the request the local inference service sends to Chatterbox for voice cloning, including the caller identity it attaches;
- the local inference service's job-creation operation (`POST /inference/jobs`), with its voice cloning failure answer changed to state why cloning failed;
- the operator-set settings the local inference service reads to call the private Chatterbox.

It delivers milestone CRM-1 of `docs/.ai/chatterbox-cloud-run/Plan.md` (Status: Approved by avinash2196 on 2026-11-09) under the requirements in `docs/.ai/chatterbox-cloud-run/requirements.md` (Status: Approved by avinash2196 on 2026-11-09).

This contract governs externally observable behavior only. The approved Plan remains the single source of truth for scope, milestones, and requirement ownership.

## Baseline

No approved contract artifact covers the Chatterbox model API or the inference service's job-creation operation. As the approved Plan records (External Contract Requirements), the baseline is the current repository behavior. The `initial-build` contract defines a different API (for example `POST /jobs`, `POST /ai/infer`) that is not this code; the Plan does not name it as the baseline, and this contract does not use it.

- Baseline source: the current repository behavior at commit `360846e`: the Chatterbox model API in `voice_narration/chatterbox_api/application.py` (operations listed in `cloudrun/chatterbox-service/README.md:16-20`), and the inference service's job-creation operation and cloning settings in `voice_narration/inference/application.py:22-24`, `:99-116`, `:157-216`.
- Verified against: the repository at HEAD `360846e` on 2026-11-09 (the commit the Plan records for its Current State). Checked:
  - the README's endpoint list (`GET /health`, `GET /v1/metadata`, `POST /v1/synthesize`) matches the three routes in `voice_narration/chatterbox_api/application.py:43`, `:53`, `:89`;
  - the synthesize fields `text`, `language`, `sample_path` (`:21-24`), its validation (`:55-61`), its sample-path handling (`:65-69`), its generation-failure answer (`:71-74`) and its WAV response (`:83-86`);
  - the inference settings (`voice_narration/inference/application.py:23-24`), its cloning call (`:99-116`), job creation (`:157-216`), and the gateway pass-through (`:363-366`).
  No published contract (OpenAPI or other) exists in the repository; `git ls-files` lists only the work-item contract artifacts. The only in-repository client of `POST /v1/synthesize` is the inference service (`voice_narration/inference/application.py:110`). No divergence was found.

## Changes in This Work Item

| Change | Added / Changed / Removed | Requirement / Plan Reference |
| --- | --- | --- |
| `POST /v1/synthesize` request body changes from a JSON object to `multipart/form-data` with parts `text`, `language` and `sample_audio` (the voice sample audio file); `sample_audio` is required | Changed | CCR-5, CCR-6; Plan External Contract Requirements change 1; CCD-1 |
| `sample_path` removed from `POST /v1/synthesize`; a request carrying a `sample_path` part is answered `400`; the baseline `404 sample_path does not exist` answer is removed | Removed | CCR-6, AC-CCR-3; Plan change 2; CCD-2 |
| `POST /v1/synthesize` answers `400` when `sample_audio` is empty; a non-empty sample the model cannot use is answered as a generation failure (`503`) | Added | CCR-6; Plan change 2; CCD-3 |
| Chatterbox calls require a Google-signed identity token for `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`, enforced by the Cloud Run deployment; the inference service attaches that token | Added | CCR-7, AC-CCR-4; Plan change 3; CCD-4 |
| Chatterbox serves one synthesize request at a time; other requests wait | Added | Requirements Operational Characteristics: Consistency and concurrency; CCD-9 |
| Chatterbox holds neither the voice sample nor the generated audio after responding | Added | CCR-10, AC-CCR-7; CCD-10 |
| The inference service sends the profile's stored voice sample audio itself in each cloning request, and no sample path | Changed | CCR-5, AC-CCR-3; CCD-1 |
| In `voice_cloning` mode the single generic `503` message is replaced by one message per failure reason CFR-1–CFR-9 | Changed | CCR-8, AC-CCR-5; Plan change 4; CCD-5 |
| The 120-second cloning timeout is replaced by the configurable time limit `VOICE_CLONING_TIMEOUT_SECONDS`, default `600` seconds | Changed | CCR-9, AC-CCR-6; Plan change 5; CCD-6 |
| `GOOGLE_APPLICATION_CREDENTIALS` (existing setting) also names the service-account key the inference service uses to obtain the identity token | Changed | CCR-7; Plan change 6; CCD-7 |

Everything else in this contract is carried over unchanged from the baseline.

## Out of Scope

- Login and authentication of application users (requirements Explicit Exclusions). No operation in this contract gains a user-facing authentication requirement.
- Performing the GCP deployment, and the Cloud Run deployment settings themselves (GPU, region, instance counts, per-instance request limit, platform request time limit). These belong to the deployment document of CRM-6, not this contract.
- Moving the voices service, inference service, frontend or narration mode to GCP.
- Any change to the AI Gateway contract (`docs/.ai/ai-gateway-multimodel/contract/API-Contract.md`, approved 2026-11-08), to the voices service API, to narration mode, or to the frontend.
- Any change to `GET /health` or `GET /v1/metadata` behavior in the Chatterbox application.
- Duplicate detection of repeated cloning requests (requirements Consistency and concurrency: "no duplicate detection is required").
- Logging, metrics, or alerts beyond Cloud Run's default request logs (requirements Observability).
- A sample-size limit, a sample-format check beyond non-emptiness, or a machine-readable failure-reason field. None is authorized; this contract defines none.

## Requirement Traceability

| Capability | Requirement / Plan Reference |
| --- | --- |
| `POST /v1/synthesize` carries the voice sample audio as the `sample_audio` part | CCR-5, CCR-6, AC-CCR-3; Plan change 1 |
| `POST /v1/synthesize` rejects `sample_path` and answers a missing, empty or unusable sample | CCR-6, AC-CCR-3; Plan change 2 |
| Carried-over `text` and `language` validation and generation-failure answer | RF-3, RF-4; Plan CRM-2 scope (carried-over behavior) |
| Caller identity required for every Chatterbox call on Cloud Run | CCR-7, AC-CCR-4; Plan change 3 |
| One synthesize request at a time; a retried request produces a new clip | Requirements Consistency and concurrency |
| No voice sample or generated audio held after responding | CCR-10, AC-CCR-7 |
| Inference service sends the sample audio and the identity token | CCR-5, CCR-7; Plan changes 1, 3, 6 |
| Inference service failure answer with reason (CFR-1–CFR-9) | CCR-8, AC-CCR-5, Dependency failure characteristic; Plan change 4 |
| `VOICE_CLONING_TIMEOUT_SECONDS` time limit | CCR-9, AC-CCR-6; Plan change 5 |
| Settings for calling the private Chatterbox | CCR-7, RF-9; Plan change 6 |
| Generated audio saved and served by the local app | CCR-10 local part, RF-13 (carried over) |
| Narration mode unchanged | CCR-2, RF-12 (carried over) |
| `GET /health`, `GET /v1/metadata` unchanged | Baseline; Plan CRM-3 exclusion "no change to the health or metadata operations" |

## Interfaces

### Chatterbox Synthesize (HTTP)

- Purpose: generate speech for the given text in the voice of the given sample.
- Related requirement: CCR-5, CCR-6, CCR-7, CCR-10; Consistency and concurrency; RF-3, RF-4 (carried over).
- Endpoint: `/v1/synthesize`
- HTTP method: `POST`
- Required inputs: a `multipart/form-data` body with:
  - `text` — a form field, the text to speak;
  - `language` — a form field, the language code;
  - `sample_audio` — a file part holding the voice sample audio bytes. The part's filename and content type are not significant and are ignored.
  - On Cloud Run, the `Authorization` header, as described under Chatterbox Caller Identity.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: the generated speech as WAV audio, `Content-Type: audio/wav`, at the model's sample rate (carried over).
- Failure status codes, in the order they are checked (the first that applies is answered):
  1. `422` — the body is not `multipart/form-data` (including a JSON body in the baseline shape), or a `text`, `language` or `sample_audio` part is missing, or `sample_audio` is not a file part. This is the framework's request-validation answer, carried over from the baseline answer for missing or malformed fields.
  2. `400`, detail `sample_path is not supported; send the voice sample as sample_audio` — the body contains a part named `sample_path`, whatever its value (including empty).
  3. `400`, detail `text is required` — `text` is empty or only whitespace (carried over).
  4. `400`, detail `language must be hi or en` — `language`, after trimming surrounding whitespace and lowercasing, is not `hi` or `en` (carried over, RF-3).
  5. `400`, detail `sample_audio is required` — the `sample_audio` part holds zero bytes.
  6. `503`, detail `chatterbox_synthesis_failed: <error text>` — model generation raised an error, including when a non-empty sample cannot be used by the model (carried over, RF-4).
  7. `500` — any other unhandled error, for example a failure while loading the model before generation (carried over: model loading at `voice_narration/chatterbox_api/application.py:63` is outside the generation error handling). The body is not specified.
  On Cloud Run, a call without a valid identity token is rejected by the platform before any of these checks (see Chatterbox Caller Identity).
- Failure response body:
  - `400` and `503`: JSON `{"detail": "<string>"}`. For `400` the whole detail string is normative. For `503` the prefix `chatterbox_synthesis_failed: ` is normative and the error text after it is informative.
  - `422`: JSON `{"detail": [ ... ]}`, the framework's validation-error list. The status code and the presence of a `detail` list are normative; the list entries are informative.
- Validation rules:
  - `text` is trimmed of surrounding whitespace and the trimmed text is spoken (carried over).
  - `language` is trimmed and lowercased, then must be `hi` or `en` (carried over).
  - `sample_audio` must be non-empty. Chatterbox does not otherwise check its format; a sample the model cannot read results in failure 6.
  - Parts other than `text`, `language`, `sample_audio` and `sample_path` are ignored (carried over from the baseline, which ignored unknown JSON fields).
- Concurrency: Chatterbox runs one synthesize generation at a time. A request that arrives while another is generating waits, and is then served; Chatterbox itself does not reject a request for being busy. The order in which waiting requests are served is not specified. Waiting time counts toward the caller's time limit (VOICE_CLONING_TIMEOUT_SECONDS).
- Repeated requests: each request, including an identical repeat or a retry, runs a new generation and produces a new clip. There is no duplicate detection.
- Retention: once the response has been sent, whether success or failure, Chatterbox holds no copy of the voice sample or of the generated audio, in memory or on its filesystem. Chatterbox never reads a voice sample from its own filesystem.
- Identity / existence behavior: not applicable. The operation takes no identifier; the baseline file-path lookup and its `404` are removed.
- Mutation semantics: not applicable. The operation creates and stores nothing.

### Chatterbox Health (HTTP)

Carried over unchanged.

- Purpose: report that the Chatterbox application is running.
- Related requirement: baseline.
- Endpoint: `/health`
- HTTP method: `GET`
- Required inputs: none (on Cloud Run, the `Authorization` header as described under Chatterbox Caller Identity).
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON `{"status": "ok", "service": "chatterbox_api", "model_variant": <string>, "device": <string>}`, where `model_variant` is the value of `CHATTERBOX_MODEL_VARIANT` (default `v3`) and `device` is the value of `CHATTERBOX_DEVICE` (default `cpu`, RF-5).
- Failure status codes: none defined by the application.
- Failure response body: not applicable.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Chatterbox Metadata (HTTP)

Carried over unchanged.

- Purpose: report the model identity and output sample rate.
- Related requirement: baseline.
- Endpoint: `/v1/metadata`
- HTTP method: `GET`
- Required inputs: none (on Cloud Run, the `Authorization` header as described under Chatterbox Caller Identity).
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON `{"model_id": "chatterbox-multilingual-v3", "model_version": <string>, "sample_rate_hz": <integer>}`, where `model_version` is the value of `CHATTERBOX_MODEL_VARIANT` and `sample_rate_hz` is the model's output sample rate. The model is loaded on first use, so the first call may take as long as a model load.
- Failure status codes: `500` when the model cannot be loaded (body not specified).
- Failure response body: not specified.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Chatterbox Caller Identity

Applies to every Chatterbox operation above when Chatterbox runs on Cloud Run as documented by CRM-6.

- A call must carry the header `Authorization: Bearer <token>`, where `<token>` is a Google-signed OpenID Connect identity token for the service account `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`, with its audience set to the Chatterbox service URL (CCR-7).
- Cloud Run checks the token, not the Chatterbox application. A call with no token, an invalid or expired token, a token with the wrong audience, or a token for any other identity is rejected by Cloud Run with `401` or `403` before it reaches Chatterbox. Which of the two is answered is the platform's choice; clients may rely only on "`401` or `403`". The body is the platform's and is not specified (AC-CCR-4).
- The Chatterbox application performs no identity check of its own and ignores the `Authorization` header. When it runs outside Cloud Run, for example locally, it answers without checking identity.

### Inference Service Voice Cloning Call (outbound HTTP from the inference service to Chatterbox)

This is the request the inference service sends to Chatterbox Synthesize when a job is created in `voice_cloning` mode.

- Purpose: obtain cloned speech for a job from the configured Chatterbox.
- Related requirement: CCR-5, CCR-7, CCR-9.
- Endpoint: `<base URL>/v1/synthesize`, where `<base URL>` is the base URL in effect (see Inference Service Settings): the configured value with surrounding whitespace removed and nothing else changed (carried over).
- HTTP method: `POST`
- Request:
  - `text` — the job's text, trimmed (carried over);
  - `language` — the part of the voice profile's `language` before the first `-`, lowercased; `en` when the profile has no language (carried over from `voice_narration/inference/application.py:106`);
  - `sample_audio` — the complete, unmodified bytes of the file at the profile's stored `sample_path` (RF-8);
  - no `sample_path` part;
  - header `Authorization: Bearer <token>` — a Google-signed identity token for the service account of the key file named by `GOOGLE_APPLICATION_CREDENTIALS`, with its audience equal to the base URL in effect.
- The call is bounded by the time limit `VOICE_CLONING_TIMEOUT_SECONDS`, measured from when the inference service starts sending the request to Chatterbox until it has received the complete response. Obtaining the identity token comes before this and is not counted toward the limit. When the limit is reached, the inference service stops waiting and answers with CFR-5.
- A success is a `200` response whose `Content-Type` media type is `audio/wav` (compared case-insensitively, parameters ignored) and whose body is not empty. The body is saved by the local inference service as the job's audio (carried over, RF-13). Anything else is a failure, answered as CFR-6–CFR-9 (CFR-5 when the time limit is reached).

### Inference Job Creation (HTTP)

- Purpose: create a narration or voice cloning job and return where its audio is served.
- Related requirement: CCR-2, CCR-5, CCR-7, CCR-8, CCR-9, CCR-10 local part.
- Endpoint: `/inference/jobs`
- HTTP method: `POST`
- Required inputs (carried over): a JSON object with `text` (non-blank string) and `voice_profile_id` (string).
- Optional inputs (carried over): `voice_name` (default `Custom Clone`), `user_id` (default `guest`), `mode` (default `narration`). An absent, `null` or empty value takes the default. `mode` equal to `voice_cloning` selects voice cloning through Chatterbox; any other value selects narration with Google TTS (RF-12).
- Success status code: `200` (carried over).
- Success response body (carried over): JSON `{"id": <string>, "status": "completed", "audio_url": <string>, "download_url": <string>, "voice_profile_id": <string>, "voice_name": <string>}`. The audio is stored by the local inference service and served at `audio_url` (RF-13, CCR-10 local part).
- Failure status codes, in the order they are checked:
  1. `422` — the body is not valid JSON or not a JSON object (carried over, framework validation).
  2. `400`, detail `Text is required` — `text` absent, `null` or blank (carried over).
  3. `400`, detail `voice_profile_id is required` — `voice_profile_id` absent, `null` or empty (carried over).
  4. `404`, detail `Voice registry not initialized` — no voice registry exists (carried over).
  5. `404`, detail `Voice profile not found` — no profile has that id (carried over).
  6. `403`, detail `Voice profile is not available for generation` — the profile's status is not `approved` or `active` (carried over).
  7. In `voice_cloning` mode only: `503` with the message of the first applicable failure reason in the table below (changed, CCR-8).
- Voice cloning failure reasons, checked in this order. Each message is followed by the same sentence the baseline message used, ` Please retry, or use Google voice narration mode.`:

  | Reason | Condition | `detail` |
  | --- | --- | --- |
  | CFR-1 Not configured | The configured base URL is empty (see Inference Service Settings). | `Voice cloning failed: no voice cloning service is configured. Please retry, or use Google voice narration mode.` |
  | CFR-2 Invalid time limit | `VOICE_CLONING_TIMEOUT_SECONDS` is set to a non-blank value that is not a positive whole number. | `Voice cloning failed: VOICE_CLONING_TIMEOUT_SECONDS must be a positive whole number of seconds. Please retry, or use Google voice narration mode.` |
  | CFR-3 Voice sample unreadable | The profile has no stored `sample_path`, or the file at it cannot be read. | `Voice cloning failed: the voice sample for this profile could not be read. Please retry, or use Google voice narration mode.` |
  | CFR-4 Identity token unavailable | No identity token could be obtained: the key file is missing or unreadable, is not a service-account key, or the token request to Google failed. | `Voice cloning failed: could not obtain an identity token for the voice cloning service. Please retry, or use Google voice narration mode.` |
  | CFR-5 Timed out | The call to Chatterbox did not complete within the time limit. | `Voice cloning failed: the voice cloning service did not respond within <N> seconds. Please retry, or use Google voice narration mode.` where `<N>` is the time limit in effect, written as a whole number |
  | CFR-6 Cannot connect | Any transport failure other than CFR-5 (for example name resolution, connection refused, TLS failure, connection lost before the full response). | `Voice cloning failed: could not connect to the voice cloning service. Please retry, or use Google voice narration mode.` |
  | CFR-7 Access denied | Chatterbox (or Cloud Run in front of it) answered `401` or `403`. | `Voice cloning failed: access to the voice cloning service was denied (HTTP <status>). Please retry, or use Google voice narration mode.` where `<status>` is the status code received |
  | CFR-8 Chatterbox error | Any other non-`200` status. This includes Chatterbox's `400`, `422`, `500` and `503` answers and any status Cloud Run answers on its own, such as `429` or `504`. | `Voice cloning failed: the voice cloning service returned an error (HTTP <status>). Please retry, or use Google voice narration mode.` where `<status>` is the status code received |
  | CFR-9 Bad response | `200` with an empty body, or with a `Content-Type` whose media type is not `audio/wav`. | `Voice cloning failed: the voice cloning service returned a response that is not audio. Please retry, or use Google voice narration mode.` |

  A cloning failure creates no job record and no audio file.
- Failure response body: JSON `{"detail": "<string>"}` (carried over). The `detail` strings above are normative in full, with `<N>` and `<status>` filled in. The `422` body is the framework's validation-error list; there, only the status code is normative.
- Validation rules: as listed under Failure status codes (carried over). This contract does not define behavior for JSON field values of the wrong type (for example a number for `text`). That behavior is unchanged from the baseline and not contracted.
- Identity / existence behavior (carried over): an unknown `voice_profile_id` is answered `404 Voice profile not found`. The operation does not check the identifier's format, so there is no separate malformed-identifier answer.
- Mutation semantics (carried over): each successful call creates a new job and returns its representation. Nothing existing is updated.
- Gateway pass-through (unchanged, constraint): the AI Gateway execution operation (`POST /ai-gateway/v1/executions`) answers a cloning failure with its approved `503 MODEL_UNAVAILABLE` error, `retryable: true`, and `errors[0].message` equal to the `detail` above (`voice_narration/inference/application.py:363-366`). Its error shape stays as approved in `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md`.

### Inference Service Settings (operator-set configuration)

Environment variables the local inference service reads. They are read once, when the service starts, from the process environment (carried over for the base URLs); a change takes effect after a restart. The one exception is `GOOGLE_APPLICATION_CREDENTIALS`, as described in its row.

| Setting | Form | Absent / blank | Status |
| --- | --- | --- | --- |
| `VOICE_CLONING_API_BASE_URL` | Absolute URL of Chatterbox, for example the Cloud Run service URL, with no trailing `/`. Surrounding whitespace is removed; otherwise the value is used unchanged (the base URL in effect), both to build the call URL and as the identity token's audience. | When the variable is not set, `CHATTERBOX_API_BASE_URL` is used. When it is set but empty or only whitespace, the base URL is empty (no fallback). | Carried over (RF-9); additionally used as the token audience (CCD-4) |
| `CHATTERBOX_API_BASE_URL` | Same form as above. Used only when `VOICE_CLONING_API_BASE_URL` is not set. | Empty base URL. An empty base URL makes every voice cloning job fail with CFR-1. | Carried over (RF-9) |
| `VOICE_CLONING_TIMEOUT_SECONDS` | A positive whole number of seconds: decimal digits only, surrounding whitespace removed, value at least `1`. No upper bound is defined by this contract. | Not set, empty or only whitespace: `600` (10 minutes). Any other value that is not a positive whole number (for example `0`, `-5`, `10.5`, `ten`) makes every voice cloning job fail with CFR-2. Narration is unaffected. | Added (CCR-9) |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to the service-account key file for `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`. Located as the existing narration provider locates it: the process environment; when not set there, the repository-root `.env` file; otherwise `service-account-key.json` at the repository root (`voice_narration/inference/providers/google.py:13-35`). | Neither set nor a default key file present: no identity token can be obtained, and voice cloning jobs fail with CFR-4. | Existing setting; newly also used for the Chatterbox identity token (CCR-7) |

An identity token is attached to every voice cloning call, whatever the base URL. No setting disables it.

## Contract-Wide Rules

- Input parsing and type errors: a body that cannot be parsed as the operation's declared body type (`multipart/form-data` for Chatterbox Synthesize, a JSON object for Inference Job Creation) is answered `422` with the framework's validation-error list (carried over). For Chatterbox Synthesize, a missing part or a non-file `sample_audio` is also `422`. Wrong-type JSON values in Inference Job Creation are not contracted (see that interface). The GET operations take no input.
- Absent / null / empty / blank values: Chatterbox Synthesize: a missing part is `422`; blank `text` is `400 text is required`; blank `language` is `400 language must be hi or en`; zero-byte `sample_audio` is `400 sample_audio is required`; a `sample_path` part is `400` even when empty. Inference Job Creation: absent, `null` and empty are treated alike, as listed for each field. Settings: as in the settings table.
- Read-only and unknown request fields: Chatterbox Synthesize ignores parts other than `text`, `language`, `sample_audio` and `sample_path`, and rejects `sample_path`. Inference Job Creation ignores fields it does not define (carried over). Neither operation accepts server-assigned fields; a job `id` or `status` supplied in the request is ignored.
- Numeric semantics: `VOICE_CLONING_TIMEOUT_SECONDS` is a whole number of seconds; no rounding is applied, and a fractional value is invalid (CFR-2). `sample_rate_hz` is an integer reported by the model. No monetary or derived values are defined by this contract. The gateway's `usage` fields are governed by the AI Gateway contract.
- Collection ordering, empty results, limits: not applicable. No operation in this contract returns a collection; `GET /inference/jobs` and the gateway's model list are outside this contract. No request-size or sample-size limit is defined.
- Matching and filtering semantics: `language` is matched exactly against `hi` and `en` after trimming and lowercasing. The `Content-Type` check for a Chatterbox success is case-insensitive on the media type, with parameters ignored. Voice profile lookup is by exact identifier. There is no other filtering.
- Error response shape and which parts are normative: application-generated errors are JSON `{"detail": <string>}`. The normative parts per operation are stated in each interface: full detail strings for Chatterbox `400` and for every inference `400`/`403`/`404`/`503`, only the `chatterbox_synthesis_failed: ` prefix for Chatterbox `503`, and only the status code for `422` and for platform answers (`401`/`403`/`429`/`504`), whose bodies are the platform's.
- Versioning and compatibility of message or RPC schemas: not applicable. There are no message or RPC interfaces. HTTP compatibility is described under Compatibility Notes.

## Decisions Resolved

| Decision | Resolution | Source |
| --- | --- | --- |
| CCD-1 Request shape for sending the voice sample audio | `POST /v1/synthesize` takes `multipart/form-data` with form fields `text`, `language` and the required file part `sample_audio`. The inference service sends the stored sample file's bytes unmodified. Part filename and content type are not significant. | Proposed — deferred by requirements "Decisions Deferred to Later Milestones" (request shape, CCR-5, CCR-6) and Plan External Contract Requirements change 1 |
| CCD-2 Removal of `sample_path` | A `sample_path` part is answered `400 sample_path is not supported; send the voice sample as sample_audio`. A JSON body in the baseline shape is answered `422`. The baseline `404 sample_path does not exist` is removed. | Removal: CCR-6, AC-CCR-3. Answers: Proposed — deferred by Plan change 2 |
| CCD-3 Missing or unusable voice sample | Missing part: `422`. Zero bytes: `400 sample_audio is required`. Non-empty but unusable by the model: generation failure `503 chatterbox_synthesis_failed: <error text>` (RF-4). | Proposed — deferred by Plan change 2 |
| CCD-4 Caller identity | A Google-signed OpenID Connect identity token for `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` in `Authorization: Bearer`. Account and token type come from CCR-7. Proposed: the audience is the base URL in effect; Cloud Run enforces the check with `401` or `403`; the Chatterbox application performs no check of its own. | Account and token: CCR-7, AC-CCR-4. Audience and enforcement point: Proposed — deferred by Plan change 3 (consistent with Plan CRM-3 and CRM-6 scope) |
| CCD-5 Failure reasons and message wording | Nine reasons, CFR-1–CFR-9, checked in the stated order. Each answers `503` with `{"detail": "Voice cloning failed: <reason>. Please retry, or use Google voice narration mode."}` worded exactly as tabled. CFR-1 replaces the baseline no-backend message (RF-14). CFR-2, CFR-3 and CFR-4 cover local causes the requirement's examples do not list. | 503 and "message says why": CCR-8, AC-CCR-5. Reasons and wording: Proposed — deferred by requirements "Decisions Deferred" (CCR-8 wording) and Plan change 4 |
| CCD-6 Time-limit setting name and form | `VOICE_CLONING_TIMEOUT_SECONDS`, a positive whole number of seconds, default `600`, read at service start. Absent or blank uses the default; any other invalid value makes cloning fail with CFR-2. It bounds the call to Chatterbox from the start of sending until the complete response, including any wait at Chatterbox, but not obtaining the identity token. On expiry: CFR-5. Replaces the 120-second timeout (RF-10). | 10-minute configurable limit: CCR-9, AC-CCR-6. Name, form, invalid-value handling and measured span: Proposed — deferred by requirements "Decisions Deferred" (time-limit setting) and Plan change 5 |
| CCD-7 Local settings for the private Chatterbox | Base URL settings carried over unchanged (RF-9) and also used as the token audience. The identity token comes from the key file named by the existing `GOOGLE_APPLICATION_CREDENTIALS`, located as the narration provider locates it. No new URL, audience or credential setting is added, and no setting disables the token. | Base URL: RF-9 (baseline). Key: CCR-7 ("existing service-account key"). Reuse of `GOOGLE_APPLICATION_CREDENTIALS` and no opt-out: Proposed — deferred by Plan change 6 |
| CCD-8 Behavior carried over | `GET /health`, `GET /v1/metadata`, the `text` and `language` rules, the generation-failure `503`, the WAV success answer, the job-creation inputs, validations, success body and pass-through all stay as in the baseline. | Plan External Contract Requirements (carry unchanged behavior over); Plan CRM-3 exclusion |
| CCD-9 One request at a time | Chatterbox runs one generation at a time. Others wait and are then served, never rejected by Chatterbox for being busy. Waiting order is not specified because the requirements state none. Waiting counts toward the caller's time limit. | Requirements Consistency and concurrency |
| CCD-10 No retention | After a response (success or failure), Chatterbox holds no voice sample or generated audio, in memory or on disk, and reads no sample from its own filesystem. Generated audio is saved by the local inference service. | CCR-10, AC-CCR-7 |
| CCD-11 Retries | Every request, including a retry or identical repeat, produces a new generation. There is no duplicate detection. The AI Gateway's idempotency replay is unchanged. | Requirements Consistency and concurrency; Plan RSK-9 (gateway idempotency unchanged) |

## Compatibility Notes

- `POST /v1/synthesize` changes incompatibly: a baseline JSON request is answered `422`, and `sample_path` is no longer accepted (CCR-6, AC-CCR-3). The requirements approve this removal. The only in-repository client, the local inference service, changes to the new shape in CRM-5. Between CRM-3 and CRM-5, the repository's inference service cannot clone against the changed Chatterbox; this follows from the Plan's milestone order.
- The voice cloning `503` message of `POST /inference/jobs` changes (CCR-8). The status code `503` and the `{"detail": <string>}` shape are unchanged. Every message keeps the baseline's closing sentence `Please retry, or use Google voice narration mode.`. Consumers that display the detail (the frontend, `frontend/src/App.jsx:127-129`) or pass it through (the AI Gateway, `voice_narration/inference/application.py:363-366`) receive the new text with no shape change.
- The AI Gateway contract is unchanged.
- `GET /health` and `GET /v1/metadata` are unchanged in the application. On Cloud Run they, like synthesize, require the caller identity (Chatterbox Caller Identity).
- The existing base URL settings keep their names, precedence and blank handling.

## Contract Review Status

- Status: Approved by avinash2196 on 2026-11-09. Approval recorded by the main conversation at the user's explicit approval ("Approve contract"). This approval accepts every proposed decision CCD-1–CCD-7 in Decisions Resolved.
