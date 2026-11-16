# API Contract — auth-consent

## Contract Scope

This contract defines the externally observable behavior of:

- the account service, added by this work item: sign-up, login, session check and logout, which the frontend calls;
- the voice service (port 8002) and the inference service (port 8003): their operations carried over from the baseline, and the changes this work item makes for token checks, per-user ownership, the owner-only sample fetch, refusal when the account store cannot be read, and consent;
- the request the inference service sends to the voice service for a cloning sample;
- where accounts, logins and consent records are stored, as far as it can be observed;
- the settings operators set for these services.

It delivers milestone AUM-1 of `docs/.ai/auth-consent/Plan.md` (Status: Approved by Avinash Srivastava on 2026-11-16 (8-milestone revision)) under `docs/.ai/auth-consent/requirements.md` (Status: Approved by Avinash Srivastava on 2026-11-16, revision 2). It resolves Plan decisions CTD-1–CTD-7.

The frontend's on-screen behavior (session restore, logging out on a refused token, redirecting to Login, the consent tick, the Signup page's own password check) is governed by the requirements (AR-7, AR-13, Business Context password rule). This contract governs only what the frontend sends to and receives from the services.

The deployed Chatterbox's interface is carried over from the baseline unchanged (see Inference Service Chatterbox Call).

Labels this contract introduces use the prefix `AUE-` (refusal answers). No referenced approved artifact defines it. `AR-`, `AS-`, `AAC-`, `AX-` labels are the requirements' labels; `AUM-`, `AUR-`, `AUV-`, `CTD-`, `PLD-`, `UIC-` labels are the Plan's; `OAF-`, `OAC-`, `OAD-`, `COA-`, `CON-` labels are the baseline's and its work item's. All of them are cited, not redefined.

This contract governs externally observable behavior only. The approved Plan remains the single source of truth for scope, milestones, and requirement ownership.

## Baseline

- Baseline source: `docs/.ai/chatterbox-original-app/API-Contract.md`, Contract Review Status "Approved by Avinash Srivastava on 2026-11-13", as Plan External Contract Requirements names it. It has no Amendments. The account operations have no baseline: no approved contract defines them, and the frontend's current calls (`frontend/src/services/api/authClient.ts:22-48`) are a client in the repository, not a contract (Plan External Contract Requirements).
- Verified against: the repository at HEAD `f3372ce` on branch `claude/auth-consent`, on 2026-11-16. Checked:
  - The baseline's milestones that implement the services are executed: `docs/.ai/chatterbox-original-app/Plan.md` Execution Status records OAM-3 and OAM-5 GREEN verified. The last commits touching either service are `0465867` (OAM-3) and `ce598d4` (OAM-5); `git diff --stat 60a9192 f3372ce -- voice_narration/simple_voices voice_narration/inference frontend/src/services` is empty.
  - Voice service (`voice_narration/simple_voices/application.py`): `GET /health` (`:89-92`); `POST /voice/upload` (`:94-149`) with hand-parsed `name` and `file` parts (`:103-122`), WebM conversion (`:124`), response fields (`:126-135`), `400 Invalid content type` (`:139-142`), the conversion failure text (`:16`, `:143-144`) and `500 Upload failed: <text>` (`:145-149`); `GET /voices` (`:151-160`); `GET /voices/approved` (`:162-171`); `GET /voices/{voice_id}` (`:173-182`); `GET /voices/{voice_id}/sample` (`:184-198`); `PATCH /voices/{voice_id}` (`:200-227`); `DELETE /voices/{voice_id}`, including deletion of a preloaded voice until restart (`:229-241`, `:78`); `OPTIONS /{path}` (`:243-254`); retention before every request (`:256-260`) and the CORS headers on every response (`:262-269`); the five preloaded voices (`:19-65`); 120-hour retention (`voice_narration/simple_voices/store.py:13`); `VOICE_SERVICE_PORT` (`voice_narration/simple_voices/__main__.py:18`). The voice service reads no `.env` file and no `DATABASE_URL`.
  - Inference service (`voice_narration/inference/application.py`): CORS middleware allowing every origin, method and header with credentials (`:451-457`); `POST /inference/jobs/{job_id}/infer` with its check order (`:494-524`) and one generation at a time (`:102`, `:510`); `GET /inference/jobs/{job_id}/output` (`:526-551`); `GET /inference/jobs/{job_id}/download` (`:553-572`); `GET /inference/generations` (`:574-599`, ordering and filters `:208-237`); `GET /inference/generations/{job_id}` (`:601-614`); `DELETE /inference/generations/{job_id}` (`:616-627`, `:252-278`); `GET /inference/backends` (`:629-654`, `:370-405`); history entry fields (`:157-166`); database expiry (`:193`). There is no `/health` route. `owner_id` parameters exist and are unused (`:285`, `:336`).
  - Chatterbox call and settings (`voice_narration/inference/chatterbox.py`): messages OAF-1–OAF-9 (`:20-32`); settings (`:66-73`); sample fetch with no credential (`:145-155`); identity token, call and answer handling (`:157-194`). `DATABASE_URL` and `.env` loading (`voice_narration/inference/db.py:13-28`). `INFERENCE_PROVIDER` startup choice (`voice_narration/inference/__main__.py:33-58`).
  - Clients in the repository: every voice-service and inference-service call sends `Authorization: Bearer <token>` (`frontend/src/services/voiceApi.ts:10`, `:26`, `:41`, `:56`, `:70`; `frontend/src/services/ttsApi.ts:50`, `:85`, `:111`, `:126`, `:150`, `:191`, `:213`); the TTS page sends `script`, `voice_id`, `provider` and, for Chatterbox, `language` (`ttsApi.ts:52-57`) and reads `error` from failure bodies (`ttsApi.ts:61-62`); the recorder and upload form send `file` and `name` parts through `VoiceAPI.uploadVoice` (`frontend/src/components/VoiceRecorder.tsx:159-163`, `frontend/src/components/VoiceUpload.tsx:264-272`). The account client sends to `VITE_AUTH_API_BASE_URL`, default `http://localhost:9000` (`frontend/src/utils/api-config.ts:8`, `frontend/.env.development:2`).
  - No published contract (OpenAPI or other) for these services is committed. `start-all.bat:39-41` starts only the voice service, the inference service and the frontend.
  - Result: no divergence between the baseline and the repository was found. The baseline's own verification text cites line numbers of its earlier baseline commit; this contract cites the current lines.

## Changes in This Work Item

| Change | Added / Changed / Removed | Requirement / Plan Reference |
| --- | --- | --- |
| Account service with Account Sign-up `POST /auth/signup`, Account Login `POST /auth/login`, Account Session Check `GET /auth/validate` and Account Logout `POST /auth/logout`, reached at `http://localhost:9000` by default | Added | AR-1, AR-4, AR-6, AR-7, UIC-1; CTD-1 |
| Sign-up refusals: body not a JSON object (AUE-7), email or password missing (AUE-8), password rule (AUE-9), existing email `account already exists` (AUE-10) | Added | AR-2, AR-3; CTD-1 |
| Login refusal for a wrong email or password (AUE-11); no limit on failed attempts | Added | AR-4; CTD-1 |
| A login lasts 24 hours from issue; logout ends it; no refresh token | Added | AR-5, AR-6, AX-5; CTD-1 |
| Every voice-service and inference-service request, except to `/health` and `/inference/backends` and except CORS preflights, needs `Authorization: Bearer <token>` of a current login; otherwise `401` (AUE-1) | Added | AR-8; CTD-2 |
| Requests are refused with `503` (AUE-2) when the account store cannot be read | Added | AR-12; CTD-2 |
| CORS preflights are answered without a token; refusals carry the services' CORS headers | Changed | AR-8, AX-1; CTD-2 |
| Each recorded or uploaded voice and each generation belongs to the account that created it; voice lists, the approved voice list and generation history hold only the requester's own items plus the five built-in Google voices | Changed | AR-9; CTD-3 |
| Another user's, an ownerless, or a lost account's voice or generation is answered as unknown by every operation | Changed | AR-9, AR-10; CTD-3 |
| Deleting another user's or an ownerless generation deletes nothing; the answer is the baseline's answer for an unknown identifier | Changed | AR-9, AR-10; CTD-3 |
| A generation request whose `job_id` is held by another user's or an ownerless generation is refused with `409` (AUE-6) | Added | AR-9, AR-10; CTD-3 |
| Renaming, changing or deleting a built-in Google voice is refused with `403` (AUE-5); the baseline allowed it until a restart | Changed | AR-9; CTD-3 |
| Voice Sample serves a voice's sample only to its owner's token; the inference service fetches it with the requesting user's token | Changed | AR-11; CTD-4 (changes baseline OAC-4) |
| Voice Upload requires the form field `consentVersion` with value `1`; without it, `400` (AUE-3) and no voice is stored; a consented upload records the account, the time, the voice and version 1 | Added | AR-13, AR-14, AR-15; CTD-5 |
| A Chatterbox generation for a voice with no consent record is refused with `403` (AUE-4), checked after OAF-3 and before OAF-4 | Added | AR-16; CTD-6 |
| Accounts, logins and consent records are stored in PostgreSQL when each service can connect to `DATABASE_URL` at its start, otherwise in files | Added | AR-18, PLD-1, PLD-2; CTD-7 |
| `DATABASE_URL` is also read by the voice service and the account service; added setting `AUTH_SERVICE_PORT` | Added | AR-18, PLD-1; CTD-7 |
| Out of Scope no longer excludes authentication of callers, per-user voice separation, or a consent step | Removed | AR-8, AR-9, AR-13 |

Everything else in this contract is carried over unchanged from the baseline.

## Out of Scope

- Email verification (AX-4). An account can log in as soon as it is created.
- Refresh tokens (AX-5). The account service has no `/auth/refresh` operation, and no answer carries a `refreshToken`.
- An administrator role, or any access to another user's items (AX-3).
- A limit on failed login attempts (AR-4). Repeated wrong passwords never lock or slow an account.
- A separate consent-withdraw action (AR-17). Consent is withdrawn by deleting the voice (Voice Deletion, carried over).
- An operation that returns consent records, or that returns the account owning a voice or generation. AAC-14 is verified against the store (Plan AUM-7).
- Migrating, assigning an owner to, or deleting voices and generations that existed before this work item (Plan AUR-6). They stay hidden (AR-10). Voice retention still applies to them.
- The applications in `voice_narration/auth/` (`/api/v1/auth/...`) and `voice_narration/consent/` (`/api/v1/consent/...`). No launcher starts them, and their routes are not part of this contract.
- CORS hardening beyond what auth needs, background generation jobs, object storage, scaling, observability, mobile recording formats and deploying (AX-1), and deploying to Cloud Run (AX-2).
- Logging, metrics and alerts (requirements Operational Characteristics: observability not required).
- The frontend's on-screen behavior (see Contract Scope).
- Carried over from the baseline: the deployed Chatterbox's own interface and deployment; copying the Chatterbox service source; manual approval before cloning (every upload is still approved automatically, COA-12); falling back to another provider when Chatterbox fails; duplicate prevention or detection of generation requests; any text length limit, and splitting text; a sample size limit or format check other than the WebM conversion; a machine-readable failure-cause field (clients tell causes apart by status and `error` text); a setting for where voices and samples are stored; deleting generations when their recorded expiry passes.

## Requirement Traceability

| Capability | Requirement / Plan Reference |
| --- | --- |
| Account Sign-up: account created with email and password, logged in at once, no verification | AR-1, AX-4, AS-1, AAC-1, UIC-1; CTD-1 |
| Server password rule | AR-2, Business Context password rule, AS-3, AAC-2; CTD-1 |
| Case-insensitive email, `account already exists`, one account for simultaneous sign-ups | AR-3, Business Context identity rule, Operational consistency, AS-2, AAC-3; CTD-1 |
| Account Login and its refusal; no failed-login limit | AR-4, AS-4, AAC-4; CTD-1 |
| 24-hour login, no refresh | AR-5, AX-5, AS-5, AAC-5; CTD-1 |
| Account Logout ends the login on the server | AR-6, AS-6, AAC-6, UIC-1; CTD-1 |
| Account Session Check | AR-7, AAC-7; CTD-1 |
| Token check on every voice-service and inference-service request except `/health` and `/inference/backends` | AR-8, AS-7, AAC-8; CTD-2 |
| CORS preflights and CORS headers on refusals | AR-8, AX-1; CTD-2 |
| Refusal when the account store cannot be read | AR-12, AS-14, AAC-12, Operational dependency failure; CTD-2 |
| Per-user lists and access; built-in Google voices for everyone and unchangeable | AR-9, AS-8, AAC-9; CTD-3 |
| Ownerless items hidden and refused | AR-10, AS-9, AAC-10; CTD-3 |
| Owner-only sample fetch, with the requesting user's token | AR-11, AS-8, AAC-11; CTD-4 |
| Consented upload with `consentVersion` `1`; consent record | AR-13, AR-14, Business Context consent rule, AAC-14, UIC-2; CTD-5 |
| Upload without consent refused, no voice stored | AR-15, AS-10, AAC-15; CTD-5 |
| Cloning refuses a voice with no consent record | AR-16, AS-11, AAC-16; CTD-6 |
| Deleting a voice deletes its sample (carried over) | AR-17, AS-12, AAC-17 |
| Store selection, file fallback, loss on restart acceptable | AR-18, PLD-1, PLD-2, AS-13, AAC-18, Operational durability; CTD-7 |
| Settings `DATABASE_URL`, `AUTH_SERVICE_PORT` | AR-18, PLD-1, PLD-2, Operational deployment; CTD-7 |
| Every other capability of the voice and inference services | Baseline, carried over |

## Interfaces

### Account Service (HTTP, the service as a whole)

Added (CTD-1). One local process, one instance, started by the repository's local start-up together with the voice and inference services (Operational deployment; Plan AUM-4). It listens on every network interface, as the voice service does, on port `AUTH_SERVICE_PORT` (default `9000`), so the frontend reaches it at its existing default `http://localhost:9000` (`frontend/src/utils/api-config.ts:8`). Its operations are the four below; any other path or method is answered by the web framework (`404` or `405`; only the status code is normative).

### Account Sign-up (HTTP)

Added.

- Purpose: create an account and log it in.
- Related requirement: AR-1, AR-2, AR-3, AR-5, AS-1, AS-2, AS-3, UIC-1; CTD-1.
- Endpoint: `/auth/signup` on the account service.
- HTTP method: `POST`
- Required inputs: a JSON object body with:
  - `email` — a string. Surrounding whitespace is removed; the result is the account's email.
  - `password` — a string, used exactly as received (not trimmed).
- Optional inputs: none. Every other body field is ignored, including `confirmPassword` and `agreedToTerms`, which the Signup page sends (`frontend/src/pages/Auth/Signup.tsx:84-89`), and fields named like server-assigned values (`id`, `token`). The `Authorization` header is ignored.
- Success status code: `201`. No `Location` header is sent, because no operation addresses an account by its URL.
- Success response body: JSON `{"token": <string>, "user": {"id": <string>, "email": <string>}}`.
  - `token` is a new login, issued at this moment, so the user is logged in straight away (AR-1, AS-1). Login Lifetime applies to it. It is an opaque non-empty string; its format is not contracted.
  - `user.id` is an opaque non-empty string assigned by the account service; its format is not contracted.
  - `user.email` is the email as stored: as sent, with surrounding whitespace removed, in its original letter case.
- Failure status codes, in the order they are checked (the first that applies is answered):
  1. `400` AUE-7 — the body is not valid JSON, or is valid JSON but not an object.
  2. `400` AUE-8 — `email` or `password` is absent, `null`, not a string, or empty; `email` that is only whitespace counts as empty.
  3. `400` AUE-9 — the password breaks the password rule (Validation rules).
  4. `503` AUE-2 — the account store cannot be read or written.
  5. `409` AUE-10 — an account with this email already exists.
- Failure response body: JSON `{"error": <string>}`, the whole string normative (Refusal Answers).
- Validation rules:
  - Password rule (AR-2, the same rule the Signup page checks, `Signup.tsx:40`): at least 8 characters, counted as Unicode code points; at least one uppercase letter `A`–`Z`; at least one digit `0`–`9`. Each failure, alone or together, answers AUE-9. There is no maximum length and no other rule.
  - The email's format is not checked by the server. The requirements state no server email check; the Signup page checks it.
- Identity / existence behavior: emails are compared without regard to case: two emails are the same when they are equal after both are converted to lower case (AR-3). A sign-up with an email that matches an existing account in any letter case answers AUE-10 and changes nothing. When several sign-ups with the same email arrive at the same moment, exactly one answers `201` and every other answers AUE-10; exactly one account exists afterwards (AR-3, Operational consistency).
- Mutation semantics: each `201` creates one new account and one login. No existing account is ever changed by this operation.

### Account Login (HTTP)

Added.

- Purpose: log in to an existing account.
- Related requirement: AR-4, AR-5, AS-4, UIC-1; CTD-1.
- Endpoint: `/auth/login` on the account service.
- HTTP method: `POST`
- Required inputs: a JSON object body with `email` and `password`, both strings, read as for Account Sign-up.
- Optional inputs: none. Other body fields and the `Authorization` header are ignored.
- Success status code: `200`.
- Success response body: JSON `{"token": <string>, "user": {"id": <string>, "email": <string>}}`, with the meanings stated for Account Sign-up. `token` is a new login issued at this moment.
- Failure status codes, in the order they are checked:
  1. `400` AUE-7 — the body is not a JSON object.
  2. `400` AUE-8 — `email` or `password` is absent, `null`, not a string, or empty.
  3. `503` AUE-2 — the account store cannot be read or written.
  4. `401` AUE-11 — no account has this email, or the password is not the account's password. Both cases have the same answer.
- Failure response body: JSON `{"error": <string>}`, the whole string normative.
- Validation rules: the password rule is not applied at login; a password that breaks it is simply wrong (AUE-11). No limit on failed attempts (AR-4).
- Identity / existence behavior: the email is matched without regard to case, as for Account Sign-up; the password is matched exactly.
- Mutation semantics: each `200` issues one new login. The account's other logins are unaffected and stay valid until they expire or are logged out.

### Account Session Check (HTTP)

Added.

- Purpose: tell the frontend whether a stored token is a current login, and whose (AR-7).
- Related requirement: AR-5, AR-6, AR-7, AAC-7; CTD-1.
- Endpoint: `/auth/validate` on the account service.
- HTTP method: `GET`
- Required inputs: header `Authorization: Bearer <token>` (Token Presentation and Check).
- Optional inputs: none. Query parameters and any body are ignored.
- Success status code: `200`.
- Success response body: JSON `{"user": {"id": <string>, "email": <string>}}` — the account the login belongs to.
- Failure status codes, in the order they are checked:
  1. `401` AUE-1 — no usable bearer token.
  2. `503` AUE-2 — the account store cannot be read.
  3. `401` AUE-1 — the token is not a login, has expired, or was logged out.
- Failure response body: JSON `{"error": <string>}`, the whole string normative. `401` means the token is refused. `503` means the check could not be made; it says nothing about the token.
- Validation rules: none beyond the above.
- Identity / existence behavior: see Token Presentation and Check.
- Mutation semantics: none. A session check does not extend the login.

### Account Logout (HTTP)

Added.

- Purpose: end a login on the server (AR-6).
- Related requirement: AR-6, AS-6, UIC-1; CTD-1.
- Endpoint: `/auth/logout` on the account service.
- HTTP method: `POST`
- Required inputs: header `Authorization: Bearer <token>`.
- Optional inputs: none. Any body is ignored, including the `{}` the frontend client sends (`frontend/src/services/api/authClient.ts:47`).
- Success status code: `200`.
- Success response body: JSON `{"success": true}`.
- Failure status codes: as for Account Session Check, in the same order.
- Failure response body: as for Account Session Check.
- Validation rules: none beyond the above.
- Identity / existence behavior: see Token Presentation and Check.
- Mutation semantics: ends the login whose token was presented. From this answer on, that token is refused with AUE-1 by every operation that checks tokens, on all three services. Other logins of the same account are unaffected. A repeat with the same token answers AUE-1.

### Login Lifetime (rule for every token check)

Added (AR-5, CTD-1).

- A login is accepted while less than 24 hours (86,400 seconds) have passed since it was issued, and refused from that moment on. Time is measured on the clock of the service checking the token. All services run on the same machine (Operational deployment).
- Nothing extends a login: no session check, request or refresh token (AX-5).
- A login also ends when it is logged out (Account Logout), and may be lost on a restart (Account Store).

### Token Presentation and Check (rule for every operation of the voice service and the inference service, and for Account Session Check and Account Logout)

Added (AR-8, AR-12, CTD-2).

- The token is presented only in the header `Authorization: Bearer <token>`: the scheme `Bearer`, in any letter case, then one space, then the token. A token in a query parameter, a cookie or the body is not read.
- A usable bearer token is missing when the header is absent, uses another scheme, or has an empty token.
- Exempt requests, answered with no token check and whatever their `Authorization` header holds, including when the account store cannot be read:
  - every request to the paths `/health` and `/inference/backends`, exactly, on the voice service and on the inference service (AR-8). Where a service has no operation at the path (the inference service has no `/health`, the voice service has no `/inference/backends`), the framework answers `404`, as in the baseline;
  - every CORS preflight: an `OPTIONS` request carrying both an `Origin` and an `Access-Control-Request-Method` header (see Cross-Origin Requests);
  - Account Sign-up and Account Login.
- Every other request to the voice service or the inference service, including one to an unknown path or with an unsupported method, and every Account Session Check and Account Logout request, is checked before anything else in the order:
  1. no usable bearer token: `401` AUE-1;
  2. the account store cannot be read: `503` AUE-2;
  3. the token is not a login issued by the account service, has expired (Login Lifetime), or was logged out: `401` AUE-1.
  A request that passes is made by the token's account, the requester. Only then does the operation's own behavior apply, including the framework's `404` or `405` for unknown paths and methods.
- The token is checked once, when the request arrives. A login that expires or is logged out while an accepted request waits or runs does not stop that request (see Inference Generation).
- No request is refused for a valid token because of which client sent it.

### Account Store (rule for the three services)

Added (AR-12, AR-18, PLD-1, PLD-2, CTD-2, CTD-7).

- The account store holds accounts, logins and consent records.
- Choice (PLD-1): each of the three services, when it starts, tries to connect to the database named by `DATABASE_URL` (Settings). If it connects, it uses PostgreSQL for as long as it runs. Otherwise it uses files in a git-ignored local folder of the repository working copy (PLD-2) for as long as it runs. It never switches while running.
- Unreadable store (AR-12): when the chosen store cannot be read (or, for an operation that writes, written), the request is refused with `503` AUE-2. Requests to exempt paths are unaffected.
- Durability (AR-18, Operational durability): accounts, logins and consent records are kept while the services run. Whether they survive a restart is not contracted; losing them is acceptable (AS-13). After such a loss, earlier tokens are refused (AUE-1) and users sign up again.
- Services using different stores: a service started while it could connect uses PostgreSQL, and one started while it could not uses files (Plan AUR-3). They do not share accounts, logins or consent records. A token issued from one store is refused (AUE-1) by a service using the other.

### Ownership (rule for every voice-service and inference-service operation)

Added (AR-9, AR-10, CTD-3).

- A recorded or uploaded voice belongs to the requester whose Voice Upload created it. A generation belongs to the requester whose Inference Generation saved it.
- The five built-in Google voices (`en-US-Neural2-A`, `en-US-Neural2-C`, `en-US-Neural2-E`, `hi-IN-Neural2-A`, `hi-IN-Neural2-B`) belong to no account. They are listed for and readable by every requester. No requester can rename, change or delete them (AUE-5).
- A voice or generation that is not the requester's is answered exactly as an unknown one by every operation, unless an operation below states otherwise. This covers:
  - another account's item;
  - an ownerless item: one that existed before this work item and has no owner (AR-10);
  - an item whose owning account no longer exists in the store, for example after a restart lost it. An item belongs only to the account that created it. A later account never becomes its owner, even one that signs up with the same email.
- Such items are never listed and are not counted in any `total`.
- No operation returns the account that owns an item.

### Voice Service Health (HTTP)

Carried over unchanged. Exempt from the token check (AR-8).

- Purpose: report that the voice service is running.
- Related requirement: baseline; AR-8.
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

- Purpose: create a voice owned by the requester from a recorded or uploaded sample, with the requester's consent, keeping the sample.
- Related requirement: AR-9, AR-13, AR-14, AR-15; baseline COA-2, COA-6, COA-11, COA-12, OAD-1; CTD-3, CTD-5.
- Endpoint: `/voice/upload`
- HTTP method: `POST`
- Required inputs:
  - a usable bearer token of a current login (Token Presentation and Check) (added);
  - a `Content-Type` header containing `multipart/form-data` with a `boundary` parameter (carried over);
  - `consentVersion` — a form field (added, AR-13, AR-15). After surrounding whitespace is removed its value must be exactly `1`, the version of the statement "I own this voice or have the speaker's informed permission to clone it". It is sent for a recording and for an uploaded file alike (UIC-2).
- Optional inputs (carried over):
  - `name` — a form field, the voice name. Absent, empty or only whitespace: `Unnamed Voice`. Otherwise the value with surrounding whitespace removed.
  - `file` — a file part holding the voice sample. Its file name and content type are not significant (OAD-1).
- Sample storage (carried over):
  - When the `file` part's content is WebM audio, as Chrome's recorder produces, the voice's sample is a PCM WAV file holding that recording's audio. The content is recognized from the bytes, never from the file name (`recording.wav`) or the content type (`audio/wav`) the recorder sends. Sample rate and channel count are not contracted.
  - Any other non-empty `file` content (WAV, MP3, OGG or anything else) is stored as the sample byte-identical to the part's content as received. Only WAV and WebM samples are required to clone (COA-6).
  - When there is no `file` part, or it holds zero bytes, the voice is created with no sample. Its sample lookup answers `404` (Voice Sample).
- Consent record (added, AR-14): with every `201`, a consent record is stored in the account store holding the requester's account, the time the upload was accepted on the voice service's clock, the new voice's `id`, and consent version `1`. A voice is created only together with its consent record: when the record cannot be stored, the answer is AUE-2 and no voice and no sample are stored.
- Ownership (added, AR-9): the new voice belongs to the requester (Ownership).
- Success status code: `201` (carried over; no `Location` header).
- Success response body (carried over, unchanged): JSON `{"id": <string>, "name": <string>, "format": "WAV", "duration": 45, "fileSize": <integer>, "uploadedAt": <string>, "status": "approved", "approvalScore": 95}`. No consent or owner field is added.
  - `id` is `voice-` followed by 8 lowercase hexadecimal characters, assigned by the service.
  - `format` is always `"WAV"` and `duration` always `45`, whatever the sample (informative only).
  - `fileSize` is the number of bytes in the `file` part as received, before any conversion; with no `file` part or an empty one, the number of bytes in the whole request body.
  - `uploadedAt` is the upload time on the voice service's clock, an ISO 8601 date-time without a time-zone offset. The 5-day retention is counted from it.
  - `status` `"approved"` and `approvalScore` `95`: every new voice is approved automatically and can be cloned straight away (COA-12).
- Failure status codes, in the order they are checked:
  1. `401` AUE-1 or `503` AUE-2 — Token Presentation and Check (added).
  2. `400`, `{"error": "Invalid content type"}` — the `Content-Type` header does not contain `multipart/form-data` (carried over).
  3. `500`, `{"error": "Upload failed: <text>"}` — the body cannot be parsed, for example a `multipart/form-data` content type with no `boundary` parameter (carried over). This is answered even when `consentVersion` is missing, because the body cannot be read.
  4. `400` AUE-3 — `consentVersion` is absent, or its value after removing surrounding whitespace is not exactly `1` (added, AR-15). No voice, sample or consent record is stored.
  5. `400`, `{"error": "Upload failed: the recording could not be converted to WAV."}` — the `file` part is WebM but cannot be converted to WAV (carried over). No voice is created and nothing is stored.
  6. `503` AUE-2 — the consent record cannot be stored (added). Nothing is stored.
  7. `500`, `{"error": "Upload failed: <text>"}` — any other error while handling the upload (carried over).
- Failure response body: JSON `{"error": <string>}`. For failures 2, 4 and 5, AUE-1 and AUE-2 the whole string is normative. For failures 3 and 7 the prefix `Upload failed: ` is normative and the text after it is informative.
- Validation rules: as listed above. Form parts other than `name`, `file` and `consentVersion` are ignored, including parts named like server-assigned fields (`id`, `status`, `approvalScore`, `uploadedAt`) and any part naming an owner (carried over, extended to `consentVersion`). When `consentVersion` appears more than once, the result is not contracted.
- Durability (carried over): the voice and its sample survive a restart of the voice service until deleted or expired. Its consent record follows Account Store durability.
- Retention (carried over): see Voice Retention.
- Identity / existence behavior: not applicable. The operation takes no identifier.
- Mutation semantics: each successful call creates a new voice with a new `id` owned by the requester, and one consent record. Nothing existing is changed (carried over).

### Voice List (HTTP)

- Purpose: list the built-in Google voices and the requester's own voices.
- Related requirement: AR-9, AR-10; baseline COA-3, COA-11; CTD-3.
- Endpoint: `/voices`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added).
- Optional inputs: none. Query parameters are ignored (carried over).
- Success status code: `200`.
- Success response body (carried over): JSON `{"data": [<voice>, ...]}`. Each `<voice>` is the voice's stored representation with `status` set to `"approved"` and `approvalScore` set to its stored value or `95` when it has none.
  - The five built-in voices carry `"provider": "google"`, `language`, `gender`, `approvalScore: 100` (`voice_narration/simple_voices/application.py:19-65`). Recorded and uploaded voices have the upload response's fields and no `provider` field. A client tells recorded and uploaded voices from the built-in voices by the absence of `provider` (COA-3).
- Collection ordering (carried over): the built-in voices first, in their fixed order, then the requester's recorded and uploaded voices in upload order, oldest first. The same order holds after a restart.
- Collection contents (changed, AR-9, AR-10): the five built-in voices and the requester's own voices that are neither deleted nor expired. Another account's, ownerless and lost accounts' voices are never listed (Ownership). Expired voices are never listed (Voice Retention).
- Empty result: not reachable, because the five built-in voices are always listed; a requester with no voices of their own receives only them.
- Limits: none; no paging (carried over).
- Failure status codes: `401` AUE-1, `503` AUE-2 (added).
- Failure response body: JSON `{"error": <string>}`, the whole string normative.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Approved Voice List (HTTP)

- Purpose: list the voices the TTS page offers (`frontend/src/services/ttsApi.ts:210-223`).
- Related requirement: AR-9, AR-10; baseline COA-3; CTD-3.
- Endpoint: `/voices/approved`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added).
- Optional inputs: none. Query parameters are ignored (carried over).
- Success status code: `200`.
- Success response body (carried over): JSON `{"data": [<voice>, ...]}` — of the voices Voice List would list for the requester, those whose stored `status` is `"approved"` or absent or empty, each with `status` set to `"approved"`. Ordering, expiry and limits as for Voice List. The five built-in voices are always approved and cannot be changed (AUE-5), so the list always holds at least them.
- Failure status codes: `401` AUE-1, `503` AUE-2 (added).
- Failure response body: JSON `{"error": <string>}`, the whole string normative.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Voice Lookup (HTTP)

- Purpose: return one voice.
- Related requirement: AR-9, AR-10; baseline COA-11; CTD-3.
- Endpoint: `/voices/{voice_id}`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added); `voice_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON, the voice's stored representation, unmodified (carried over), with the fields listed for Voice Upload or, for a built-in voice, for Voice List. No owner field is returned.
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `404`, `{"error": "Voice not found"}` — no voice has that identifier, or it was deleted, or it has expired (Voice Retention) (carried over), or it is not the requester's and not a built-in voice (added, Ownership).
- Failure response body: JSON `{"error": <string>}`; the whole string is normative.
- Validation rules: none.
- Identity / existence behavior: the identifier is matched exactly and case-sensitively. Its format is not checked, so a malformed identifier is answered as an unknown one, `404` (carried over). Another account's, an ownerless and a lost account's voice are answered as unknown (added).
- Mutation semantics: not applicable.

### Voice Update (HTTP)

- Purpose: rename one of the requester's voices or change its stored status or score.
- Related requirement: AR-9, AR-10; baseline COA-11; CTD-3.
- Endpoint: `/voices/{voice_id}`
- HTTP method: `PATCH`
- Required inputs: a usable bearer token of a current login (added); `voice_id` path segment; a JSON object body (carried over).
- Optional inputs (carried over): `name`, `status`, `approvalScore`. Each one present in the body replaces the stored value as given, whatever its value or type, including `null`. An absent field leaves the stored value unchanged.
- Success status code: `200`.
- Success response body: JSON, the voice's stored representation after the change (carried over).
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `404`, `{"error": "Voice not found"}` — unknown, deleted, expired, or not the requester's (as Voice Lookup).
  3. `403` AUE-5 — the voice is one of the five built-in voices (changed; the baseline applied the change until a restart). Nothing is changed.
  4. `400`, `{"error": "Update failed: <text>"}` — the body is not valid JSON (carried over). A valid JSON body that is not an object is not contracted: the baseline answers `400` for some such values and `200` with no change for others (carried over, `voice_narration/simple_voices/application.py:210-227`).
- Failure response body: JSON `{"error": <string>}`. For `404`, AUE-1, AUE-2 and AUE-5 the whole string is normative; for `400` the prefix `Update failed: ` is normative.
- Validation rules: none beyond the above. Fields other than `name`, `status` and `approvalScore` are ignored, including any field naming an owner (carried over).
- Identity / existence behavior: as for Voice Lookup.
- Mutation semantics (carried over): partial update of `name`, `status` and `approvalScore`. `id`, `uploadedAt`, `fileSize`, `format`, `duration`, the sample, the owner and the consent record cannot be changed. An update survives a restart. An update does not change `uploadedAt`, so it does not extend retention. Built-in voices cannot be updated (failure 3).

### Voice Deletion (HTTP)

- Purpose: delete one of the requester's voices and its sample; this is also how consent is withdrawn (AR-17).
- Related requirement: AR-9, AR-10, AR-17; baseline COA-11; CTD-3.
- Endpoint: `/voices/{voice_id}`
- HTTP method: `DELETE`
- Required inputs: a usable bearer token of a current login (added); `voice_id` path segment.
- Optional inputs: none.
- Success status code: `200` (carried over).
- Success response body: JSON `{"success": true}` (carried over).
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `403` AUE-5 — the voice is one of the five built-in voices (changed; the baseline removed it until a restart). Nothing is deleted.
  3. `404`, `{"error": "Voice not found"}` — unknown, already deleted, expired, or not the requester's (as Voice Lookup). Nothing is deleted.
- Failure response body: JSON `{"error": <string>}`; the whole string is normative.
- Validation rules: none.
- Identity / existence behavior: as for Voice Lookup. A second deletion of the same voice answers `404` (carried over).
- Mutation semantics: deleting one of the requester's voices removes the voice and its sample permanently; neither can be recovered, including after a restart (carried over, AR-17). Its consent record is not removed by this operation; it follows Account Store durability.

### Voice Sample (HTTP)

- Purpose: return the requester's own voice's stored sample, so the inference service can send it to Chatterbox on the owner's behalf.
- Related requirement: AR-8, AR-9, AR-10, AR-11; baseline COA-2, COA-4, COA-12; CTD-4 (changes baseline OAC-4).
- Endpoint: `/voices/{voice_id}/sample`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added). The voice service serves a sample only to its owner's token (AR-11). The inference service presents the token of the generation request it is serving (Inference Service Chatterbox Call); it has no credential of its own. `voice_id` path segment.
- Optional inputs: none. Query parameters are ignored.
- Success status code: `200`.
- Success response body: the stored sample's bytes, exactly as stored (Voice Upload, Sample storage), with `Content-Type: application/octet-stream`. The body is never empty (carried over).
- Availability: a voice's sample can be fetched by its owner as soon as its upload has answered `201` (COA-12).
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `404`, `{"error": "Voice not found"}` — unknown, deleted, expired, or not the requester's (as Voice Lookup; changed: another account's, an ownerless and a lost account's voice now answer this).
  3. `404`, `{"error": "Voice sample not found"}` — the voice is a built-in voice, or one of the requester's voices uploaded with no `file` part or an empty one (carried over).
- Failure response body: JSON `{"error": <string>}`; the whole string is normative.
- Validation rules: none.
- Identity / existence behavior: as for Voice Lookup.
- Mutation semantics: not applicable. The operation changes nothing; it does not extend retention.

### Voice Retention (rule for every voice-service operation)

Carried over unchanged (COA-11, OAC-10). It applies to every recorded or uploaded voice, whoever owns it, including ownerless voices.

- An uploaded voice expires 5 days (120 hours) after its `uploadedAt`, on the voice service's clock.
- From that moment every voice-service operation treats the voice as unknown: it is not listed, and Voice Lookup, Voice Update, Voice Deletion and Voice Sample answer `404 {"error": "Voice not found"}`.
- The voice and its sample are removed permanently no later than the first voice-service request, or the first voice-service start, after that moment. They cannot be recovered. A request refused by the token check still counts as a request for this rule.
- The five built-in voices do not expire.
- Expiry also applies to any voice uploaded before a restart; time while the service is stopped counts.

### Cross-Origin Requests (HTTP, all three services)

Voice service (carried over, extended): every voice-service response, including AUE-1 and AUE-2 refusals, carries `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS` and `Access-Control-Allow-Headers: Content-Type, Authorization`. A CORS preflight on any path answers `200` with body `{}` and needs no token (changed: a preflight is exempt from the token check). An `OPTIONS` request that is not a CORS preflight is checked like any other request: without a usable token it answers AUE-1; with a current login it answers `200` with body `{}`, as in the baseline.

Inference service (carried over, extended): the service allows every origin, method and header, with credentials allowed. CORS preflights are answered by that rule without a token. Every response, including AUE-1 and AUE-2 refusals, carries the same CORS headers as a successful response, so a browser can read the refusal's status. The preflight answer's body is not normative.

Account service (added): as the inference service: every origin, method and header allowed, with credentials allowed; preflights answered without a token; every response, including refusals, carries the CORS headers.

A CORS preflight performs no operation and returns no voice, generation, account or consent data. Only the request the browser sends after it does, and that request carries the token and is checked (AR-8).

### Inference Generation (HTTP)

- Purpose: generate speech for a text with the provider the request names, save it as the requester's, and answer when it is ready or has failed.
- Related requirement: AR-8, AR-9, AR-10, AR-11, AR-16; baseline COA-1, COA-4, COA-5, COA-7, COA-8, COA-9, COA-10, COA-13, COA-14, COA-17, CON-5; CTD-3, CTD-4, CTD-6.
- Endpoint: `/inference/jobs/{job_id}/infer`
- HTTP method: `POST`
- Required inputs: a usable bearer token of a current login (added); `job_id` path segment, chosen by the client (carried over); a JSON object body with:
  - `script` — the text to speak (carried over). There is no length limit; the text is used whole and unsplit, exactly as received, for every provider (COA-17).
  - `voice_id` — the voice identifier (carried over). For Google, a Google voice name such as `en-US-Neural2-A`. For Chatterbox, the `id` of one of the requester's recorded or uploaded voices in the voice service.
- Optional inputs (carried over):
  - `provider` — which provider generates this request:
    - absent, `null`, or the empty string `""`: the provider the inference service was started with (`INFERENCE_PROVIDER`; see Settings);
    - `"google"`: the same as absent. The generation is produced by the startup provider, which is Google when the service was started with `INFERENCE_PROVIDER=google` and the Google provider initialized. When the service fell back to the mock at startup, a `"google"` generation is produced by the mock (COA-14);
    - `"chatterbox"`: the deployed Chatterbox (see Inference Service Chatterbox Call);
    - any other value, including `"mock"`, `"azure"`, whitespace, a different letter case, or a value that is not a string: rejected with `400` (failure 3 below).
  - `language` — required when `provider` is `"chatterbox"`: exactly `"en"` (English) or `"hi"` (Hindi). For any other provider, `language` is ignored, whatever its value or type; Google derives the language from the voice name.
- Success status code: `200` (carried over).
- Success response body (carried over): JSON `{"job_id": <string>, "status": "complete", "duration_seconds": <number>}`. The audio is then available to the requester from Inference Generation Download, Inference Generation Output and the history.
- Failure status codes, in the order they are checked (the first that applies is answered):
  0. `401` AUE-1 or `503` AUE-2 — Token Presentation and Check (added). Answered without waiting.
  1. `500`, `{"error": "Inference failed: <text>"}` — the body is not valid JSON, or is valid JSON but not an object (carried over).
  2. `400`, `{"error": "Missing required fields: script, voice_id"}` — `script` or `voice_id` is absent, `null`, an empty string, or another value that is false in JSON terms (`0`, `false`, `[]`, `{}`) (carried over). A `script` of only whitespace is not rejected here.
  3. `400`, `{"error": "Unsupported provider. Choose google or chatterbox."}` — `provider` is present and is not `null`, `""`, `"google"` or `"chatterbox"` (carried over).
  4. `400`, `{"error": "language must be en or hi for a chatterbox generation."}` — `provider` is `"chatterbox"` and `language` is absent, `null`, or anything other than exactly `"en"` or `"hi"` (carried over).
  5. Waiting (carried over): from here on the request waits until no other generation is running (see Generation Waiting).
  6. `409` AUE-6 — a generation with this `job_id` exists that is not the requester's: another account's, an ownerless or a lost account's generation (added, AR-9, AR-10). Nothing is generated, saved or changed.
  7. Chatterbox generations only, in this order (changed): OAF-1, OAF-2, OAF-3; then `403` AUE-4 when no consent record exists for the voice (added, AR-16), or `503` AUE-2 when the consent records cannot be read; then OAF-4–OAF-9 (see Chatterbox Failure Causes).
  8. Startup-provider generations only (carried over): `400`, `{"error": "<text>"}` — the provider rejected its input with a value error; `500`, `{"error": "Inference failed: <text>"}` — any other provider error, including Google rejecting long text (COA-17).
- Failure response body: JSON `{"error": <string>}`. For failures 2, 3 and 4, every AUE answer and every OAF message the whole string is normative, with `<job_id>`, `<N>` and `<status>` filled in. For failure 1 and failure 8 `500`, the prefix `Inference failed: ` is normative and the text after it is informative. For failure 8 `400`, only the status code is normative.
- Validation rules (carried over): as listed above. A non-string `script` or `voice_id` that passes check 2 is not otherwise validated; the result is not contracted. Fields other than `script`, `voice_id`, `provider` and `language` are ignored, including `job_id`, `status`, `duration_seconds` or any owner field supplied in the body.
- Voices of other accounts (added, CTD-3): for a Chatterbox generation, a `voice_id` that is not one of the requester's voices is answered OAF-3, as an unknown voice is, because the voice service does not give the sample to the requester's token (CTD-4). For a startup-provider generation, `voice_id` names a provider voice; no recorded or uploaded voice and no sample is used, so no ownership check applies and `voice_id` handling is carried over (the provider decides).
- Consent (added, AR-16): a Chatterbox generation proceeds only when a consent record exists for the voice (Voice Upload, Consent record). Startup-provider generations use no recorded or uploaded voice and need no consent record.
- Result delivery (carried over): the result or failure is the answer to this same request. The request stays open while it waits and while the generation runs, with no limit set by the inference service other than the Chatterbox time limit on the Chatterbox call itself. A client that stops waiting does not cancel the generation: it still completes, and a successful generation is saved and appears in the requester's history (COA-10). The token is checked once, at check 0; a login that expires or is logged out after that does not stop the generation, except that a Chatterbox generation's sample fetch then presents a refused token and answers OAF-3. Limits that a browser or other client places on how long a request may stay open are outside this contract.
- No fallback (carried over, COA-8): a Chatterbox generation is never produced by Google or any other provider. When it fails, nothing is generated by another provider, no audio file is written, and no history entry is created or changed; an existing history entry with the same `job_id` stays as it was.
- Saving a success (carried over, extended): the audio is saved under the inference service's audio storage and recorded as a history entry with `job_id`, `text` (the `script`), `voice_id`, `duration_seconds`, `file_path`, `format` `"wav"`, `status` `"complete"` and `created_at`. The generation belongs to the requester (added); no owner field is added to the history entry. It is also written to the database with an expiry of `created_at` plus `AUDIO_RETENTION_DAYS` days (default 30), as every generation is; a database failure does not fail the generation.
- Identity / existence behavior: `job_id` is not looked up except for check 6; any non-empty path segment is accepted (carried over). An empty segment (`/inference/jobs//infer`) does not match the route: without a usable token it answers AUE-1 (Token Presentation and Check); with a current login the framework answers `404` or `405` (carried over). For a Chatterbox generation, a `voice_id` that is unknown, deleted, expired, not the requester's, or has no sample is answered OAF-3; there is no separate malformed-identifier answer, because the identifier's format is not checked.
- Mutation semantics: a successful call saves the generation under `job_id` as the requester's. A later successful call by the same requester with the same `job_id` replaces that history entry (carried over). A call whose `job_id` is held by a generation that is not the requester's changes nothing (check 6). A failed call changes nothing.

### Generation Waiting (rule for Inference Generation)

Carried over (COA-13, OAC-8), with the token check and the `job_id` check placed.

- The inference service runs one generation at a time, for every provider and every requester.
- A generation request that passes the token check and checks 1–4 while another generation is running waits until no generation is running, then continues with check 6. It is never rejected for being busy. There is no limit on how long it waits or how many requests wait. The order in which waiting requests run is not specified.
- Requests answered by the token check or by checks 1–4 are answered without waiting.
- Waiting does not count toward the Chatterbox time limit (Inference Service Chatterbox Call).
- This contract makes no statement about whether other operations are answered while a generation runs.

### Inference Service Chatterbox Call (outbound HTTP from the inference service)

Carried over, with step 2 changed (AR-11, CTD-4) and the consent check added after it (AR-16, CTD-6). The request to the deployed Chatterbox is as the reference contract's Chatterbox Synthesize and Chatterbox Caller Identity define it (`feature/voice-cloning` at `abbe387`, `docs/.ai/chatterbox-cloud-run/API-Contract.md`; CON-3, CON-5).

- Purpose: obtain speech in the requester's selected voice from the deployed Chatterbox.
- Related requirement: AR-11, AR-16; baseline COA-4, COA-5, COA-9, COA-17, CON-5.
- Steps, in order, each answered by its cause when it fails:
  1. The Chatterbox URL in effect must be non-empty (OAF-1), and the time limit setting valid (OAF-2) (Settings).
  2. The inference service fetches the voice's sample from the voice service on behalf of the requester: `GET <voice service URL in effect>/voices/<voice_id>/sample` with header `Authorization: Bearer <token>`, where `<token>` is the token of the generation request being served, unchanged (changed, AR-11). Only a `200` answer with a non-empty body provides the sample. Any other answer, including `404` for a voice that is not the requester's and AUE-1 or AUE-2 from the voice service, or no answer, is OAF-3. This fetch is not bounded by the Chatterbox time limit.
  3. Consent (added, AR-16): a consent record must exist for `voice_id` in the account store. No record: AUE-4. The consent records cannot be read: AUE-2.
  4. It obtains a Google-signed OpenID Connect identity token for the service account of the key file named by `GOOGLE_APPLICATION_CREDENTIALS`, with its audience equal to the Chatterbox URL in effect (CON-5). Failure is OAF-4. This step is not bounded by the Chatterbox time limit. The inference service does not check which account the key belongs to; a key for any account other than `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` is rejected by Cloud Run, which is OAF-7.
  5. It sends `POST <Chatterbox URL in effect>/v1/synthesize` with `multipart/form-data`:
     - `text` — the `script`, whole, unsplit and unchanged, of any length (COA-17);
     - `language` — the request's `language`, `en` or `hi` (COA-5);
     - `sample_audio` — a file part holding the fetched sample bytes, unchanged; its file name and content type are not significant to Chatterbox;
     - header `Authorization: Bearer <identity token>`. The requester's login token is never sent to Chatterbox.
     Redirects are not followed.
- Time limit (COA-9): the call in step 5 is bounded by the time limit in effect, measured from when the inference service starts sending the request until it has received the complete response. Time Chatterbox or Cloud Run spends before answering, including a cold start or a wait at Chatterbox, counts. When the limit is reached the inference service stops waiting: OAF-5.
- Success: a `200` answer whose `Content-Type` media type is `audio/wav` (compared case-insensitively, parameters ignored) and whose body is a readable WAV file. The body becomes the generation's audio, unchanged, and is saved as Inference Generation describes. `duration_seconds` is the WAV's number of sample frames divided by its sample rate, as a JSON number, not rounded.
- Anything else is a failure, answered as OAF-6–OAF-9.

### Chatterbox Failure Causes (rule for Inference Generation)

Carried over (COA-7, OAC-5), with OAF-3's condition extended. Every cause answers `503` with JSON `{"error": "<message>"}`. Causes are checked in the order listed, with the consent check (step 3 of Inference Service Chatterbox Call: AUE-4 or AUE-2) between OAF-3 and OAF-4; the first that applies is answered. Each message ends with "Please retry, or choose another provider." (COA-7). AUE-4 is not a Chatterbox failure cause and does not use this closing sentence.

| Cause | Condition | `error` |
| --- | --- | --- |
| OAF-1 Not configured | The Chatterbox URL in effect is empty: `CHATTERBOX_URL` absent, empty or only whitespace. | `Chatterbox voice cloning is not configured. Please retry, or choose another provider.` |
| OAF-2 Invalid time-limit setting | `CHATTERBOX_TIMEOUT_SECONDS` is set to a value that is not empty, not only whitespace, and not a positive whole number of seconds. | `The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; it must be a positive whole number of seconds. Please retry, or choose another provider.` |
| OAF-3 Voice sample unreadable | The voice service did not provide the sample: the voice is unknown, deleted or expired, is not the requester's (another account's, ownerless, or a lost account's — added), has no sample, the voice service refused the forwarded token (added), answered anything other than `200` with a non-empty body, or could not be reached. | `The voice sample for the selected voice could not be read. Please retry, or choose another provider.` |
| OAF-4 Identity token unavailable | No identity token could be obtained: `GOOGLE_APPLICATION_CREDENTIALS` absent or blank, the key file missing or unreadable or not a service-account key, or the token request to Google failed. | `Could not obtain an identity token for Chatterbox. Please retry, or choose another provider.` |
| OAF-5 Timed out | The Chatterbox call did not complete within the time limit in effect. | `Chatterbox did not respond within <N> seconds. Please retry, or choose another provider.` where `<N>` is the time limit in effect as a whole number |
| OAF-6 Cannot connect | Any transport failure other than OAF-5: for example a URL that cannot be used, name resolution failure, connection refused, TLS failure, or the connection lost before the complete response. | `Could not connect to Chatterbox. Please retry, or choose another provider.` |
| OAF-7 Access denied | Chatterbox, or Cloud Run in front of it, answered `401` or `403`. | `Access to Chatterbox was denied (HTTP <status>). Please retry, or choose another provider.` where `<status>` is the status code received |
| OAF-8 Service error | Any other status than `200`, `401` or `403`, including Chatterbox's `400`, `422`, `500` and `503`, any status Cloud Run answers on its own (for example `429` or `504`), and any redirect status. | `Chatterbox returned an error (HTTP <status>). Please retry, or choose another provider.` where `<status>` is the status code received |
| OAF-9 Not audio | `200` with an empty body, a `Content-Type` whose media type is not `audio/wav`, or a body that is not a readable WAV file. | `Chatterbox returned a response that is not audio. Please retry, or choose another provider.` |

### Inference Generation Output (HTTP)

- Purpose: return the audio of one of the requester's generations made since the inference service started.
- Related requirement: AR-9, AR-10; baseline COA-4; CTD-3.
- Endpoint: `/inference/jobs/{job_id}/output`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added); `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body (carried over): JSON `{"audio_bytes": <base64 string>, "format": <string>, "duration_seconds": <number>}`.
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `404`, `{"error": "Job <job_id> not found or no output available"}` — no generation with that `job_id` was made since the service started (carried over), or it is not the requester's (added, Ownership).
  3. `500`, `{"error": "Output retrieval failed: <text>"}` — any other error (carried over).
- Failure response body: JSON `{"error": <string>}`; for `404` the whole string with `<job_id>` filled in is normative; for `500` the prefix is normative; AUE answers whole.
- Validation rules: none.
- Identity / existence behavior: exact match on `job_id`; no format check, so a malformed identifier is answered `404` (carried over). A generation that is not the requester's is answered as unknown (added).
- Mutation semantics: not applicable.

### Inference Generation Download (HTTP)

- Purpose: download one of the requester's generations' audio.
- Related requirement: AR-9, AR-10; baseline COA-10; CTD-3.
- Endpoint: `/inference/jobs/{job_id}/download`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added); `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body (carried over): the audio bytes, `Content-Type: audio/wav`, `Content-Disposition: attachment; filename="<voice_id>_<job_id>.wav"` (`generation_<job_id>.wav` when no history entry exists).
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `404`, `{"error": "Job <job_id> not found or no output available"}` — no saved file and no generation since start (carried over), or the generation is not the requester's (added).
  3. `500`, `{"error": <text>}` — any other error (carried over).
- Failure response body: JSON `{"error": <string>}`; for `404` and AUE answers the whole string is normative; for `500` only the status code.
- Validation rules: none.
- Identity / existence behavior: as for Inference Generation Output.
- Mutation semantics: not applicable.

### Inference Generation History (HTTP)

- Purpose: list the requester's saved generations.
- Related requirement: AR-9, AR-10; baseline COA-10; CTD-3.
- Endpoint: `/inference/generations`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added).
- Optional inputs (query, carried over): `skip` (integer, default `0`, values below `0` become `0`), `limit` (integer, default `20`, clamped to `1`–`100`), `voice_id`, `created_at_from`, `created_at_to`, `search`. An absent or empty filter is not applied.
- Success status code: `200`.
- Success response body (carried over): JSON `{"items": [<entry>, ...], "total": <integer>, "skip": <integer>, "limit": <integer>}`, where each `<entry>` has the fields listed under Inference Generation, Saving a success, and `total` counts the entries after filtering and before paging.
- Collection contents (changed, AR-9, AR-10): only the requester's own generations. Another account's, ownerless and lost accounts' generations are never listed or counted (Ownership).
- Collection ordering (carried over): newest `created_at` first. Empty result: `items` `[]`, `total` `0`.
- Matching and filtering (carried over), applied within the requester's generations: `voice_id` exact, case-sensitive; `created_at_from` and `created_at_to` compared as text against `created_at`, inclusive; `search` a case-insensitive substring of `text`.
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `400`, `{"error": <text>}` — `skip` or `limit` is not an integer (carried over).
  3. `500`, `{"error": "History listing failed: <text>"}` (carried over).
- Failure response body: JSON `{"error": <string>}`; for AUE answers the whole string is normative; otherwise only the status code and, for `500`, the prefix.
- Validation rules: as above. Other query parameters are ignored, including any naming an owner (carried over).
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.

### Inference Generation Detail (HTTP)

- Purpose: return one of the requester's saved generations' history entry.
- Related requirement: AR-9, AR-10; baseline COA-10; CTD-3.
- Endpoint: `/inference/generations/{job_id}`
- HTTP method: `GET`
- Required inputs: a usable bearer token of a current login (added); `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON, the history entry, with the fields listed under Inference Generation, Saving a success (carried over). No owner field is returned.
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `404`, `{"error": "Generation <job_id> not found"}` — no saved generation has that `job_id` (carried over), or it is not the requester's (added).
  3. `500`, `{"error": "Generation lookup failed: <text>"}` (carried over).
- Failure response body: JSON `{"error": <string>}`; for `404` and AUE answers the whole string is normative; for `500` the prefix.
- Validation rules: none.
- Identity / existence behavior: exact match; a malformed identifier is answered `404` (carried over). A generation that is not the requester's is answered as unknown (added).
- Mutation semantics: not applicable.

### Inference Generation Deletion (HTTP)

- Purpose: delete one of the requester's saved generations and its audio.
- Related requirement: AR-9, AR-10; baseline COA-10; CTD-3.
- Endpoint: `/inference/generations/{job_id}`
- HTTP method: `DELETE`
- Required inputs: a usable bearer token of a current login (added); `job_id` path segment.
- Optional inputs: none.
- Success status code: `200`, also for a `job_id` that has no generation (carried over), and for a `job_id` whose generation is not the requester's (added).
- Success response body: JSON `{"job_id": <string>, "deleted": true}` (carried over).
- Failure status codes, in the order they are checked:
  1. `401` AUE-1, `503` AUE-2 (added).
  2. `500`, `{"error": "Generation deletion failed: <text>"}` (carried over).
- Failure response body: JSON `{"error": <string>}`; for AUE answers the whole string is normative; for `500` the prefix.
- Validation rules: none.
- Identity / existence behavior: unknown and malformed identifiers are both answered `200` (carried over). A generation that is not the requester's is answered as unknown: `200`, and nothing is deleted (added, AR-9, AR-10).
- Mutation semantics: for one of the requester's generations, removes the history entry, its audio file, the in-memory output and the database record (carried over). For a generation that is not the requester's, nothing is removed or changed: the deletion is refused, with the same answer as for an unknown identifier, so the answer does not reveal whether the generation exists. A repeat is answered the same way.

### Inference Provider List (HTTP)

Carried over unchanged. Exempt from the token check (AR-8): it is answered whatever the `Authorization` header holds, including the token the TTS page sends (`frontend/src/services/ttsApi.ts:188-193`), and when the account store cannot be read.

- Purpose: list the providers the TTS page offers (`frontend/src/services/ttsApi.ts:188-208`).
- Related requirement: baseline COA-1, COA-14; AR-8.
- Endpoint: `/inference/backends`
- HTTP method: `GET`
- Required inputs: none.
- Optional inputs: none.
- Success status code: `200`.
- Success response body: JSON `{"backends": [{"name": <string>, "provider_class": <string>, "description": <string>}, ...]}`.
  - `azure`, `google` and `mock` are listed with their baseline `description`.
  - `chatterbox` is listed with `description` `"Chatterbox voice cloning (deployed Cloud Run service)"`. It is listed whether or not the Chatterbox settings are set; a generation with missing settings answers OAF-1 or OAF-4.
  - `provider_class` is a non-empty string; its value is informative.
  - The text of `description` before the first ` (` is the display name the page derives (`frontend/src/services/ttsApi.ts:205`); for Chatterbox it is `Chatterbox voice cloning`.
- Collection ordering: ascending by `name`: `azure`, `chatterbox`, `google`, `mock`.
- Empty result: not applicable; the list always holds these four.
- Failure status codes: `500`, `{"error": "Backend listing failed: <text>"}`.
- Failure response body: JSON `{"error": <string>}`; the prefix is normative.
- Validation rules: none.
- Identity / existence behavior: not applicable.
- Mutation semantics: not applicable.
- Listing a provider does not make it selectable per generation: Inference Generation accepts only `google` and `chatterbox` as `provider`.

### Refusal Answers (rule)

Added. Every answer is JSON `{"error": <string>}`; the whole string is normative, with `<job_id>` filled in.

| Answer | Status | `error` | Where |
| --- | --- | --- | --- |
| AUE-1 Token refused | `401` | `Authentication required` | Token Presentation and Check: no usable bearer token, or a token that is not a current login (AR-5, AR-6, AR-8) |
| AUE-2 Account store unreadable | `503` | `The account store cannot be read. Please try again later.` | Any operation that needs the account store and cannot read or write it (AR-12) |
| AUE-3 Upload without consent | `400` | `Upload failed: consent version 1 is required.` | Voice Upload (AR-15) |
| AUE-4 No consent record | `403` | `This voice has no consent record, so it cannot be cloned.` | Inference Generation, Chatterbox (AR-16) |
| AUE-5 Built-in voice | `403` | `Built-in voices cannot be changed or deleted.` | Voice Update, Voice Deletion (AR-9) |
| AUE-6 `job_id` in use | `409` | `job_id <job_id> is already in use. Choose another job_id.` | Inference Generation (AR-9, AR-10) |
| AUE-7 Body not a JSON object | `400` | `The request body must be a JSON object.` | Account Sign-up, Account Login |
| AUE-8 Email or password missing | `400` | `email and password are required.` | Account Sign-up, Account Login |
| AUE-9 Password rule | `400` | `Password must be at least 8 characters with 1 uppercase letter and 1 number` | Account Sign-up (AR-2; the Signup page's own message, `frontend/src/pages/Auth/Signup.tsx:58`) |
| AUE-10 Existing email | `409` | `account already exists` | Account Sign-up (AR-3) |
| AUE-11 Wrong credentials | `401` | `Invalid email or password.` | Account Login (AR-4) |

### Settings (operator-set configuration)

Environment variables the services read. Unless stated otherwise, a setting is read when the service starts; a change takes effect after a restart. Values set in the process environment take precedence; the inference service also loads `.env`, `.env.local` and `.env.production` from the repository root without overriding values already set (carried over, `voice_narration/inference/db.py:13-16`). These files and the key file are gitignored and never committed (CON-6).

| Setting | Read by | Form | Absent / blank | Status |
| --- | --- | --- | --- | --- |
| `DATABASE_URL` | Inference service (carried over); voice service and account service (added) | A PostgreSQL URL, as in the baseline; a `postgresql://` URL is accepted (`voice_narration/inference/db.py:19-25`). Each of the three services takes it exactly as the inference service does: from the process environment, else from `.env`, `.env.local` or `.env.production` at the repository root. It names the database for generation records (carried over) and, when the service can connect to it at its start, for accounts, logins and consent records (Account Store, PLD-1). | Absent or empty: the inference service's baseline default, `postgresql://voice_narration:voice123@localhost:5432/voice_narration` (`db.py:27-28`), for all three services. | Changed (CTD-7) |
| `AUTH_SERVICE_PORT` | Account service | A whole number, the port the account service listens on, read from the process environment as `VOICE_SERVICE_PORT` is. | Absent: `9000`, the frontend's default account URL (`frontend/src/utils/api-config.ts:8`). A value that is not a whole number: the account service does not start, as for `VOICE_SERVICE_PORT` (`voice_narration/simple_voices/__main__.py:18`). | Added (CTD-7) |
| `CHATTERBOX_URL` | Inference service | Absolute URL of the deployed Chatterbox (CON-5). Surrounding whitespace and trailing `/` characters are removed; the result is the Chatterbox URL in effect, used both to build the call URL and as the identity token's audience. The value's form is not otherwise checked; a URL that cannot be used is OAF-6. | Absent, empty or only whitespace: every Chatterbox generation answers OAF-1. Other providers are unaffected. | Carried over unchanged |
| `CHATTERBOX_TIMEOUT_SECONDS` | Inference service | A positive whole number of seconds: after removing surrounding whitespace, decimal digits only, value at least `1`. No upper bound. | Absent, empty or only whitespace: `1200` (COA-9). Any other value that is not a positive whole number makes every Chatterbox generation answer OAF-2; the service still starts, and other providers are unaffected. | Carried over unchanged |
| `GOOGLE_APPLICATION_CREDENTIALS` | Inference service | Path to a service-account key file, absolute or relative to the inference service's working directory; read by the Google provider and, when an identity token is needed, for the Chatterbox identity token (CON-5). | Absent or blank: no identity token can be obtained, and every Chatterbox generation answers OAF-4. | Carried over unchanged |
| `VOICE_SERVICE_URL` | Inference service | Base URL of the voice service, used for the sample fetch. Surrounding whitespace and trailing `/` characters are removed. | Absent, empty or only whitespace: `http://localhost:8002`. | Carried over unchanged |
| `INFERENCE_PROVIDER` | Inference service | `google`, `azure`, `mock` or any other value. | `google` starts with the Google provider, or with the mock when Google cannot be initialized; any other value, absent or blank starts with the mock. | Carried over unchanged |
| `AUDIO_RETENTION_DAYS` | Inference service | Whole number of days. Read at each save. | Absent: `30` (COA-10). | Carried over unchanged |
| `AUDIO_STORAGE_PATH`, `INFERENCE_HOST`, `INFERENCE_PORT` | Inference service | As in the baseline. | As in the baseline. | Carried over unchanged |
| `VOICE_SERVICE_PORT` | Voice service | As in the baseline. | As in the baseline. | Carried over unchanged |

- The folder that holds accounts, logins and consent records when a service uses files is not a setting. It is a git-ignored local folder of the repository working copy (PLD-2); its name is decided by the AUM-4 Implementation Plan, as PLD-2 directs when operators cannot set it.
- The login lifetime (24 hours, AR-5) and the consent version (`1`, AR-13) are fixed, not settings.
- The frontend's existing `VITE_AUTH_API_BASE_URL` (`frontend/src/utils/api-config.ts:8`, `frontend/.env.development:2`) already points at `http://localhost:9000`; this contract adds no frontend setting.

## Contract-Wide Rules

- Input parsing and type errors:
  - Token Presentation and Check comes before every other check of a non-exempt request; a malformed `Authorization` header is a missing token (AUE-1).
  - Account Sign-up and Account Login: a body that is not a JSON object answers AUE-7, whatever the `Content-Type`; `email` or `password` that is not a string answers AUE-8.
  - Voice Upload: a request whose `Content-Type` is not `multipart/form-data` answers `400 Invalid content type`; one that cannot otherwise be parsed answers `500 Upload failed: <text>` (carried over). `consentVersion` is read as text; any value other than `1` after removing surrounding whitespace answers AUE-3.
  - Voice Update: a body that is not valid JSON answers `400 Update failed: <text>`; a valid JSON body that is not an object is not contracted (carried over).
  - Inference Generation: a body that is not a JSON object answers `500 Inference failed: <text>` (carried over). `provider` and `language` of a type other than string, when they are checked, are rejected with their `400`. Non-string `script` and `voice_id` are not contracted beyond check 2 (carried over).
  - Inference Generation History: a non-integer `skip` or `limit` answers `400` (carried over).
  - Path segments are strings and have no format; no path parameter has a type error.
- Absent / null / empty / blank values: stated per field. In summary: `Authorization` absent, of another scheme, or with an empty token is a missing token (AUE-1); `email` and `password` absent, `null`, non-string or empty answer AUE-8, and an `email` of only whitespace is empty; `consentVersion` absent or blank answers AUE-3; upload `name` absent or blank becomes `Unnamed Voice`; an absent or empty `file` gives a voice with no sample; `script` and `voice_id` absent, `null` or empty answer `400`, and whitespace-only `script` is accepted; `provider` absent, `null` or `""` means the startup provider; `language` absent, `null` or empty answers `400` for Chatterbox and is ignored otherwise; settings as in the settings table; a history filter that is absent or empty is not applied.
- Read-only and unknown request fields: server-assigned and derived fields supplied by the client are ignored (`id`, `status`, `approvalScore`, `uploadedAt` on upload; `job_id`, `status`, `duration_seconds` in a generation body; `id`, `token` in a sign-up or login body). No request field can set an item's owner or a consent record's account or time; such fields are ignored. Undefined fields, form parts and query parameters are ignored by every operation, including `confirmPassword` and `agreedToTerms` on sign-up. `status` and `approvalScore` are writable through Voice Update for the requester's own voices (carried over).
- Numeric semantics: a login lasts exactly 24 hours (86,400 seconds) from issue, accepted strictly before and refused from then. Password length is counted in Unicode code points. `consentVersion` is the text `1`, not a number. `fileSize` is an integer byte count of the uploaded part before conversion. `duration` `45` and `approvalScore` `95` are fixed values (carried over). `duration_seconds` of a Chatterbox generation is sample frames divided by sample rate, a JSON number, not rounded; for other providers it is carried over from the provider. `CHATTERBOX_TIMEOUT_SECONDS` is a whole number of seconds and is not rounded; a fractional value is invalid (OAF-2). `<N>` in OAF-5 is written as a whole number. `AUTH_SERVICE_PORT` is a whole number. Voice retention is exactly 120 hours from `uploadedAt`; generation expiry is `created_at` plus `AUDIO_RETENTION_DAYS` whole days. There are no monetary values.
- Collection ordering, empty results, limits: Voice List and Approved Voice List — built-in voices in fixed order, then the requester's uploaded voices oldest first, never empty, no limit. Inference Generation History — the requester's generations, newest first, empty `items: []` with `total` `0`, `limit` clamped to `1`–`100`. Inference Provider List — ascending by `name`, always four entries. No other operation returns a collection; the account operations return none.
- Matching and filtering semantics: emails are compared without regard to case (equal after converting both to lower case), with surrounding whitespace removed first. Passwords and tokens are matched exactly and case-sensitively; the `Bearer` scheme is matched in any letter case. Voice identifiers and `job_id` are matched exactly and case-sensitively (carried over), and then the item must be the requester's (Ownership). `provider` matches exactly `"google"` or `"chatterbox"`, and `language` exactly `"en"` or `"hi"`, case-sensitive with no trimming. `consentVersion` matches exactly `1` after removing surrounding whitespace. WebM content is recognized from the bytes. The Chatterbox success `Content-Type` check is case-insensitive on the media type with parameters ignored. History filters as stated in Inference Generation History.
- Error response shape and which parts are normative: every application-generated error of all three services is JSON `{"error": <string>}` (carried over for the voice and inference services; the same shape for the account service, following the repository's convention, AP1). Normative parts are stated per operation: the whole string for every AUE answer, for every OAF message and for the fixed carried-over strings; only the prefix where carried-over errors embed exception text. Status codes are normative throughout: `401` always means the token or the credentials are refused; `503` AUE-2 means the account store could not be read and says nothing about the token. Answers the web framework generates itself (an unmatched route or method) carry its own body; only their status code is normative.
- Versioning and compatibility of message or RPC schemas: not applicable. There are no message or RPC interfaces, and the HTTP operations are not versioned (carried over). HTTP compatibility is described under Compatibility Notes.
- HTTP conventions (`api-design` AP1): the account paths `/auth/signup`, `/auth/login`, `/auth/validate` and `/auth/logout` name actions rather than resources, deviating from AP3. They follow the repository's existing convention for these operations, the frontend's account client (`frontend/src/services/api/authClient.ts:23-47`), as the services' `/voice/upload` and `/inference/jobs/{job_id}/infer` do. Sign-up answers `201` without a `Location` header, deviating from AP5, because no operation addresses an account by URL. Logout answers `200 {"success": true}` rather than `204`, following the voice service's deletion answer and the frontend client's expected body. Refusals use `401`, `403` and `503`, which AP5 does not list. These deviations are recorded here for review.

## Decisions Resolved

| Decision | Resolution | Source |
| --- | --- | --- |
| CTD-1 The account operations: where the frontend reaches them, what each request and answer carries, and the refusals | A separate account service, one local process started with the other services, on port `AUTH_SERVICE_PORT` (default `9000`, the frontend's default). `POST /auth/signup` and `POST /auth/login` take `{"email", "password"}` and answer `201` / `200` with `{"token", "user": {"id", "email"}}`; sign-up logs the new account in. `GET /auth/validate` answers `200 {"user": {...}}`. `POST /auth/logout` answers `200 {"success": true}` and ends that login only. Refusals: AUE-7 body not an object, AUE-8 missing email or password, AUE-9 password rule (`400`); AUE-10 `409 account already exists`; AUE-11 `401` wrong email or password (one answer for both); AUE-1 `401` refused token; AUE-2 `503` store unreadable. Email trimmed, compared case-insensitively, stored as entered; no server email format check. Password rule: at least 8 code points, an `A`–`Z`, a `0`–`9`. Login lifetime exactly 24 hours, never extended. Several valid logins per account. No refresh operation. | No verification: AR-1, AX-4. Password rule: AR-2, Business Context, `Signup.tsx:40`. Case-insensitive email, the text `account already exists`, one account for simultaneous sign-ups: AR-3, Operational consistency. Login, refusal, no failed-login limit: AR-4. 24 hours, no refresh: AR-5, AX-5. Logout on the server: AR-6. Session check: AR-7. One instance, local: Operational deployment. Everything else, including the paths, shapes, status codes, messages, trimming and the AUE-2 answer on the account service: Proposed — deferred by Plan CTD-1 |
| CTD-2 How a token is presented to the voice and inference services; answers for a missing, invalid or expired token and for an unreadable account store; CORS preflights | `Authorization: Bearer <token>` only (the header every frontend call already sends); scheme in any letter case. Every request except to `/health` and `/inference/backends`, and except CORS preflights, is checked first, including unknown paths: no usable token `401` AUE-1; store unreadable `503` AUE-2; unknown, expired or logged-out token `401` AUE-1. Exempt paths ignore the header and work when the store is unreadable. A CORS preflight (`OPTIONS` with `Origin` and `Access-Control-Request-Method`) is answered with the CORS headers and no data, without a token; any other `OPTIONS` is checked. Every refusal carries the service's CORS headers. The token is checked once when the request arrives. This is defined consistently with AR-8: a preflight performs no operation and returns no data, and the request it precedes is checked. | Exempt paths: AR-8. Refuse when the store cannot be read: AR-12. CORS kept to what auth needs: AX-1. Header form: repository, `voiceApi.ts:10`, `ttsApi.ts:50`. Statuses, messages, check order, preflight definition, unknown paths, refusal CORS headers: Proposed — deferred by Plan CTD-2 |
| CTD-3 Answers for another user's or an ownerless voice or generation; list contents; generation naming another user's voice or reusing another user's `job_id`; changes to built-in Google voices | Lists hold the five built-in voices plus the requester's own voices, and only the requester's generations. Every operation answers another account's, an ownerless or a lost account's item exactly as an unknown one: voice operations `404 Voice not found`; generation output, download and detail their `404`; generation deletion `200 {"deleted": true}` with nothing deleted (the baseline answer for an unknown identifier). A Chatterbox generation naming a voice that is not the requester's answers OAF-3, as for an unknown voice; a startup-provider generation uses no recorded voice, so no ownership check applies. A generation whose `job_id` is held by a generation that is not the requester's answers `409` AUE-6, checked after waiting, and changes nothing; the requester's own `job_id` is still replaced. Renaming, changing or deleting a built-in voice answers `403` AUE-5 for everyone. An item belongs only to its creating account; a later account never becomes its owner, even one with the same email after a loss. No operation returns an owner. | Own items only, built-in voices for every user: AR-9, Business Context. Ownerless items usable by no one: AR-10. Answers, `job_id` handling, built-in voice refusal, deletion answer, lost accounts, startup-provider voices: Proposed — deferred by Plan CTD-3 |
| CTD-4 How the inference service obtains a voice's sample on behalf of the requesting user, and the answer when it cannot | The inference service calls Voice Sample with the generation request's own bearer token, unchanged; it has no credential of its own. The voice service serves a sample only to its owner's token, and answers `404 Voice not found` for any other voice, and AUE-1 / AUE-2 as for any request. Any answer other than `200` with a non-empty body, or no answer, is OAF-3 (unchanged cause and message; condition extended). The login token is never sent to Chatterbox. Changes baseline OAC-4 and the Voice Sample operation. | Only on behalf of the owner: AR-11. Voice Sample must check a token: AR-8. Mechanism and answers: Proposed — deferred by Plan CTD-4 |
| CTD-5 What an upload must carry to count as consented, and the answer to an upload without consent | Form field `consentVersion` with value `1` (after removing surrounding whitespace) on `POST /voice/upload`, for recordings and uploaded files alike. Absent or any other value: `400` AUE-3, checked after the content-type and body parsing checks and before the WebM conversion; nothing is stored. With every `201` a consent record holds the requester's account, the time the upload was accepted, the voice `id` and version `1`; if it cannot be stored, AUE-2 and nothing is stored. The upload's response is unchanged. No operation returns consent records. | Statement and version 1: AR-13. Record contents: AR-14. Reject uploads without consent, store no voice: AR-15, AAC-15. Field name, value, status, message, check position, record time: Proposed — deferred by Plan CTD-5 |
| CTD-6 The answer when cloning names a voice with no consent record, and where it falls among the generation failure answers | `403` AUE-4 `This voice has no consent record, so it cannot be cloned.`, checked for Chatterbox generations after OAF-3 (so only the requester's own voices with a sample reach it, and it reveals nothing about other users' voices) and before OAF-4; nothing is generated or saved. AUE-2 when the consent records cannot be read. It is not a Chatterbox failure cause and does not end with the OAF closing sentence. Startup-provider generations need no consent record. | Cloning refuses a voice without a consent record: AR-16. Status, message, position: Proposed — deferred by Plan CTD-6 |
| CTD-7 Operator-set configuration for the account operations and the store, including how the PostgreSQL database is named and whether operators can set the file folder | `DATABASE_URL` names the database for all three services, read exactly as the inference service reads it, with its baseline default; each service uses PostgreSQL if it can connect at its start, otherwise files, and never switches. Added `AUTH_SERVICE_PORT`, default `9000`. The file folder is not operator-settable; its name is left to the AUM-4 Implementation Plan. Login lifetime and consent version are fixed. | PostgreSQL when available, files otherwise: AR-18. Choice once at start against the generation-record database: PLD-1. Git-ignored local folder, and AUM-4 names it when operators cannot set it: PLD-2. Reuse of `DATABASE_URL` for the voice and account services, `AUTH_SERVICE_PORT` and its default, folder not settable: Proposed — deferred by Plan CTD-7 |

## Compatibility Notes

- Every voice-service and inference-service operation except `/health`, `/inference/backends` and CORS preflights now answers `401` without the bearer token of a current login (AR-8). The frontend already sends `Authorization: Bearer <token>` on every such call (Baseline). Existing tests that call these operations without a token change (Plan AUM-5).
- Voice lists, the approved voice list and generation history are now per user (AR-9). Voices and generations that existed before this work item are hidden from everyone (AR-10), including the generations tracked in `audio_storage/generation_index.json` and the voices in `voice_storage/` (Plan AUR-6). The baseline's shared list, and the test that asserts it (Plan Current State), change.
- Built-in Google voices can no longer be renamed, changed or deleted (AUE-5). The baseline allowed it until a restart.
- Voice Upload now needs `consentVersion` `1` (AR-15). The current recorder and upload form do not send it (`VoiceRecorder.tsx:159-161`, `VoiceUpload.tsx:264-265`); the frontend adds it (Plan AUM-8, UIC-2), and existing tests that upload without consent change (Plan AUM-7). The upload's success response is unchanged.
- Voice Sample now serves a sample only to its owner's token. The inference service forwards the requester's token (CTD-4); no other client in the repository calls it.
- A generation request reusing a `job_id` held by another user's or an ownerless generation now answers `409`; the baseline replaced the entry. The TTS page generates unique `job_id`s (`ttsApi.ts:42`). Deleting a generation that is not the requester's now deletes nothing, with the same `200` answer.
- A Chatterbox generation for a voice with no consent record now answers `403` AUE-4.
- The account service listens at `http://localhost:9000`, the frontend's default. Differences from the frontend's current account client, changed by Plan AUM-4 (UIC-1, AX-5): there is no `/auth/refresh` (the framework answers `404`); answers carry no `refreshToken`, while `AuthContext` currently restores a session only when a refresh token is stored (`frontend/src/context/AuthContext.tsx:111-118`); error bodies carry `error`, while the shared HTTP client reads `message` (`frontend/src/services/api/httpClient.ts:150`); `/auth/validate` answers `{"user": ...}` rather than `{"valid": ...}`, which the client does not read (`authClient.ts:37-44`). The `401` answer of Account Login is a credentials refusal, not a refused session.
- The frontend's evaluation calls also default to `http://localhost:9000` (`frontend/src/utils/api-config.ts:11`, `frontend/src/services/voiceApi.ts:82-108`). Nothing answered them before; with the account service running they receive the framework's `404` instead of a connection failure. Both are failures, and the evaluation calls are outside this work item.
- The voice service and the account service now read `DATABASE_URL`, including from the repository's `.env` files. With PostgreSQL reachable at that URL at start, accounts, logins and consent records are written there (AR-18).
- Everything else, including Google narration, the Chatterbox call to the deployed service and its failure answers, retention of voices and generations, and the provider list, is unchanged.

## Contract Review Status

- Status: Approved by Avinash Srivastava on 2026-11-16 (reference-only revision for the 8-milestone Plan)
- Reference-only revision: the Plan's 8-milestone revision (approved by Avinash Srivastava on 2026-11-16) adds FOUNDATION milestone AUM-2 and renumbers the 7-milestone revision's AUM-2–AUM-7 as AUM-3–AUM-8 (Plan Milestones, numbering table). Requirements revision 2 (approved by Avinash Srivastava on 2026-11-16) adds AR-19, which changes no externally observable behavior, so no interface traces to it. This revision updates only the references these changes made stale: the Plan and requirements statuses in Contract Scope; Out of Scope, Plan AUM-6 to AUM-7; Account Service, Plan AUM-3 to AUM-4; Settings, the AUM-3 Implementation Plan to AUM-4; Decisions Resolved CTD-7, AUM-3 to AUM-4 twice; Compatibility Notes, Plan AUM-4 to AUM-5, Plan AUM-7 to AUM-8, Plan AUM-6 to AUM-7, and Plan AUM-3 to AUM-4. AUM-1 is unchanged. No contract decision, interface, field, status code, message, setting or Decisions Resolved resolution changes.
- Human review required before implementation planning that depends on this contract. On approval the user replaces the status with `Approved by <name> on <date>`, and the CONTRACT milestone's row in `Plan.md` Execution Status is marked complete, pointing to this contract. Approval accepts every resolution marked `Proposed — deferred by Plan CTD-n` in Decisions Resolved.
