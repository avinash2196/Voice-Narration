# Plan — auth-consent

## Status

Approved by Avinash Srivastava on 2026-11-16 (8-milestone revision).

Revision history:

- This revision (8 milestones) revises the Plan approved by Avinash Srivastava on 2026-11-16 (7-milestone revision). It folds in requirements revision 2 (AR-19, AAC-19, Q26) and the user's answers AUM2-Q1 and AUM2-Q2 of 2026-11-16, raised by the AUM-2 planning dry run of 2026-11-16 (the Implementation Plan dry run for Accounts and storage RED, numbered AUM-2 in the 7-milestone revision and AUM-3 in this one; the name "AUM-2 planning dry run" is kept throughout as the evidence's name). It adds a FOUNDATION milestone and renumbers the later milestones (mapping under Milestones). AUM-1 (CONTRACT) is Complete and is unchanged with its evidence. No other milestone had executed, so every other milestone is Pending.
- The 7-milestone revision reduced 11 milestones to 7 at the user's decision of 2026-11-16, "Merge milestones first" [User: milestone merge, 2026-11-16]. No milestone had executed at that time.

Answers recorded in this revision:

- **AUM2-Q1** [User: AUM2-Q1, 2026-11-16] option (a): add a FOUNDATION milestone immediately before the Accounts and storage RED milestone that makes the frontend test environment deliver the account client's requests, so frontend RED tests can reach the mock server. Its Implementation Plan chooses the mechanism. It serves Accounts and storage RED and Consent RED, which both need frontend tests. Delivered by AUM-2.
- **AUM2-Q2** [User: AUM2-Q2, 2026-11-16]: the pre-existing failures named in Current State are recorded as known and must not get worse; they are not fixed in this work item. Reflected in Current State, Verification Commands, the success criteria of AUM-2, AUM-4, AUM-6 and AUM-8, Risks (AUR-1, AUR-8) and Final Acceptance Criteria.
- **AUM2-Q3** became requirements Q26, answered in requirements revision 2 (AR-19).

## Objective

Deliver real sign-up, login and logout; a token check on every voice-service (8002) and inference-service (8003) operation except the two AR-8 leaves open; per-user privacy of voices and generations; an explicit, recorded consent before a voice sample is recorded or uploaded for cloning; and passwords and login tokens never stored in readable form — as approved in `docs/.ai/auth-consent/requirements.md` (Status: Approved by Avinash Srivastava on 2026-11-16, revision 2).

## Current State

Inspected at HEAD `f3372ce` on branch `claude/auth-consent`. The working tree has only the untracked `docs/.ai/auth-consent/` folder (`git status --short`). There is no product-level `docs/requirements.md`.

Account operations:

- The frontend sends sign-up, login, refresh, validate and logout to `API_CONFIG.AUTH_SERVICE`, default `http://localhost:9000` (`frontend/src/utils/api-config.ts:8`, `frontend/src/services/api/authClient.ts:23-48`). Nothing listens there: `start-all.bat:39-41` starts only the voice service, the inference service and the frontend.
- `frontend/src/context/AuthContext.tsx:109-147` restores a session only when both a token and a refresh token are stored, and then as a hard-coded "Test User" without asking any backend. `frontend/src/App.tsx:263` logs out by clearing local state only; no server call is made.
- The Signup page checks the password for at least 8 characters, an uppercase letter and a digit (`frontend/src/pages/Auth/Signup.tsx:40`) and navigates to the voice page after sign-up (`Signup.tsx:100`). The Login page does the same after login (`frontend/src/pages/Auth/Login.tsx:61`).
- `voice_narration/auth/` (register with email verification, login, me; administrator bootstrap; PostgreSQL tables, `voice_narration/auth/accounts.py:55-60`) and `voice_narration/consent/` (record and read consent) are applications that no launcher starts. Their tests are in `tests/test_authentication_consent.py`, which needs the Docker PostgreSQL harness (`tests/test_persistence.py:59-83`, `compose.harness.yaml`). That unstarted auth application keeps a salted derived value of each password rather than the password (`voice_narration/auth/accounts.py:28-29`, `:57`, `:75-76`) and a digest of each token rather than the token (`accounts.py:59`, `:108`).

Frontend test environment (AUM2-Q1):

- The account client sends every request through the shared HTTP client (`frontend/src/services/api/authClient.ts:1`), which creates an abort controller for its timeout and always passes its `AbortSignal` to `fetch` (`frontend/src/services/api/httpClient.ts:89-100`). `frontend/src/middleware/tokenInterceptor.ts` also uses that client. The voice and inference calls in `frontend/src/services/voiceApi.ts` and `frontend/src/services/ttsApi.ts` call `fetch` directly without a signal (`voiceApi.ts:7`, `ttsApi.ts:46`).
- Frontend tests run under `vitest` in the `jsdom` environment with `tests/mocks/setup.ts` as setup (`frontend/vitest.config.ts`), which starts an `msw` request mock server (`frontend/tests/mocks/setup.ts:1-11`).
- In the AUM-2 planning dry run of 2026-11-16, `fetch` in the frontend test environment rejected that signal with `TypeError: RequestInit: Expected signal ("AbortSignal {}") to be an instance of AbortSignal.`, so requests made through the account client never reach the mock server [User: AUM2-Q1, 2026-11-16].

Voice service (8002, `voice_narration/simple_voices/application.py`):

- Checks no token on any operation. Every upload is marked approved at once (`:94-149`, `:133`). The voice list and approved-voice list return every uploaded voice to every caller, after the five preloaded Google voices (`:151-171`). Any caller may rename or delete any voice, including a preloaded one (`:200-240`). The sample operation returns any voice's sample (`:184-198`). An explicit cross-origin preflight handler answers every path (`:243-254`).
- Uploaded voices and samples are kept on disk under the gitignored `voice_storage/` (`:15`, `.gitignore`) and removed 120 hours after upload (`voice_narration/simple_voices/store.py:13`).

Inference service (8003, `voice_narration/inference/application.py`):

- Checks no token on any operation. `owner_id` parameters exist but are unused (`:285`, `:336`). Generations are recorded in `audio_storage/generation_index.json` (`:110`) and, when the database is reachable, in a database table (`:170-197`, `voice_narration/inference/db.py`, default database from `DATABASE_URL` or a local PostgreSQL URL, `db.py:19-28`). The generation operation takes a client-chosen job identifier (`:470`). History, detail, download, output and deletion return or remove any generation (`:526-627`).
- `audio_storage/` is tracked in git: `git ls-files audio_storage` lists 25 files, including `generation_index.json` and generation audio with no owner.
- Chatterbox cloning fetches the voice's sample from the voice service itself, sending no credential (`voice_narration/inference/chatterbox.py:145-155`).

Contracts: the approved contract `docs/.ai/auth-consent/API-Contract.md` (delivered by AUM-1, approved by Avinash Srivastava on 2026-11-16) defines the account operations and the changed voice and inference services, built on the baseline `docs/.ai/chatterbox-original-app/API-Contract.md` (approved 2026-11-13).

Existing tests affected by this work item:

- `tests/test_voice_sample_persistence_red.py` — voice upload, list, sample, rename, deletion and retention, all without a token. `test_voices_samples_and_renames_survive_a_restart_and_are_listed_for_every_caller` (`:336`) asserts the shared list that AR-9 replaces. `test_deleting_a_voice_removes_its_sample_permanently_including_after_a_restart` (`:410`) covers AR-17.
- `tests/test_inference.py`, `tests/test_inference_provider_choice_red.py`, `tests/test_generation_persistence_red.py`, `tests/test_generation_history_download.py`, `tests/test_generation_delete_search_red.py`, `tests/test_job_orchestration.py` — inference operations without a token.
- `tests/test_authentication_consent.py` — the unstarted auth and consent applications (Q19: may change).
- `frontend/tests/auth.spec.tsx` and `frontend/tests/auth-api.spec.tsx` — auth behavior, including refresh tokens. Many cases in both files assert only `expect(true).toBe(true)` (for example `auth.spec.tsx:62`, `:69`, `:76`; `auth-api.spec.tsx:38`), so no test checks the Signup page's password rule. `frontend/tests/mocks/auth-handlers.ts` mocks the frontend's current auth calls.
- `frontend/tests/voice.spec.tsx` — recording and upload (`:367-384`), with no consent step.

Known pre-existing failures (AUM-2 planning dry run of 2026-11-16, recorded as known at AUM2-Q2 [User: AUM2-Q2, 2026-11-16]; not fixed in this work item and must not get worse):

- The full backend run (AUV-2) aborts with exit code 127 inside `tests/test_voice_enrollment.py`; the cause is unknown.
- `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing` fails.
- The frontend suite (AUV-5) has 90 failures: 27 in `frontend/tests/tts.spec.tsx` and 63 in `frontend/tests/voice.spec.tsx`.

An earlier record agrees for the last two (another work item's evidence, `docs/.ai/chatterbox-original-app/Plan.md`, OAM-7 GREEN, 2026-11-14): backend `1 failed, 100 passed, 17 skipped` with the three Docker-dependent files left out, and frontend `Tests 90 failed | 282 passed (372)`.

Test infrastructure available: `pytest`, `httpx`, `psycopg`, FastAPI's test client and `av` import in the current Python environment; Docker answers (server 29.3.1), so the existing PostgreSQL harness can run; a local PostgreSQL listens on port 5432; `frontend/package.json` has `vitest`, `msw`, Testing Library and `jsdom`. `frontend/node_modules` is not installed in this worktree.

## In Scope

- An external contract for the account operations and for the changes to the voice and inference services (AUM-1, complete).
- A frontend test environment in which requests made through the account client reach the frontend tests' request mock (AUM2-Q1).
- Storage of accounts, logins and consent records, in PostgreSQL when it is available and in files otherwise (AR-18, PLD-1, PLD-2), with passwords and login tokens never stored in readable form (AR-19).
- Sign-up, login, login expiry, logout and the session check (AR-1–AR-6).
- Token checks, per-user ownership, ownerless legacy data, owner-only sample fetch, and refusal when the account store cannot be read, in both services (AR-8–AR-12).
- Consent recording and enforcement in the services (AR-14–AR-16).
- The frontend's real session handling, the consent tick before recording or upload, and its use of the contracted operations (AR-7, AR-13, UIC-1, UIC-2).
- Changing existing tests that encode behavior this work item replaces: open access, shared lists, upload without consent, refresh tokens, and unverified session restore (AR-7, AR-8, AR-9, AR-15, AX-5, Q19).

## Out of Scope

- AX-1 Background generation jobs, object storage, scaling, observability, mobile recording formats, CORS hardening beyond what auth needs, and deploying.
- AX-2 Deploying to Cloud Run.
- AX-3 An administrator role.
- AX-4 Email verification.
- AX-5 Refresh tokens.
- A limit on failed login attempts (AR-4).
- A separate consent-withdraw action (AR-17).
- Fixing the known pre-existing failures named in Current State (AUM2-Q2).

## Requirements and Constraints

- Requirements AR-1–AR-19, scenarios AS-1–AS-14 and acceptance criteria AAC-1–AAC-19 of `docs/.ai/auth-consent/requirements.md` (revision 2) govern. The Business Context rules (identity, password, per-voice consent) are delivered with AR-3, AR-2 and AR-13–AR-14.
- Operational characteristics (requirements): one instance of each service, run locally the way `start-all.bat` runs them; simultaneous same-email sign-ups produce exactly one account; PostgreSQL absent → files, account store unreadable → refuse; accounts, logins and consent records kept until a restart, with loss on restart acceptable; scale, availability/latency and observability not required for this work item.
- `voice_narration_PDD_requirements.md` is context only (Q21).
- The approved contract `docs/.ai/auth-consent/API-Contract.md` (AUM-1) governs all externally observable behavior. Behavior of its baseline that it does not change stays as it is.
- The known pre-existing failures named in Current State must not get worse and are not fixed here (AUM2-Q2).
- Plan decisions (requirements: "How 'PostgreSQL is available' is detected, and where the files are kept. [Left to Plan — non-blocking]"):
  - **PLD-1** Each service decides once, when it starts, which store to use. It uses PostgreSQL when it can connect to the PostgreSQL database the services are already configured to use for generation records (`voice_narration/inference/db.py:19-28`), and files otherwise. It keeps that choice until it is restarted. If the chosen store later cannot be read, AR-12 applies: requests are refused, and there is no switch to the other store while running.
  - **PLD-2** The files are kept in a local folder of the repository working copy that git ignores, like the voice samples' folder (`voice_storage/`, `.gitignore`). The folder's name, and whether operators can set it, are decided by AUM-1 if operators can set it, and otherwise by the AUM-4 Implementation Plan.

## Non-Blocking Open Decisions

None. The one non-blocking decision in the requirements is decided by PLD-1 and PLD-2 for review with this Plan.

## External Contract Requirements

A contract is required: this work item adds account operations the frontend calls, and changes the externally observable behavior of the voice and inference services. It is delivered and approved.

- Artifact: `docs/.ai/auth-consent/API-Contract.md`, delivered by AUM-1 (Complete — contract approved by Avinash Srivastava on 2026-11-16).
- Baseline (`prompt-driven-development` Changed Contracts): `docs/.ai/chatterbox-original-app/API-Contract.md`, approved 2026-11-13. The account operations have no baseline: no approved contract defines them, and the frontend's current calls (`frontend/src/services/api/authClient.ts`) are a client in the repository, not a contract.
- Decisions AUM-1 resolved (none was deferred by the requirements; these are the externally observable behavior needed to define the required operations):
  - **CTD-1** The account operations for sign-up, login, session check and logout (AR-1, AR-4–AR-7): where the frontend reaches them, what each request and answer carries, and the refusals for the password rule (AR-2), an existing email (AR-3, including the fixed text "account already exists"), wrong credentials (AR-4), and an expired or ended login (AR-5, AR-6).
  - **CTD-2** How a token is presented to voice-service and inference-service operations, and the answers for a missing, invalid or expired token (AR-8) and for an account store that cannot be read (AR-12). Also how cross-origin preflight requests are treated, so that the browser frontend can send the token, within AX-1 ("CORS hardening beyond what auth needs" is excluded).
  - **CTD-3** The answers when a user addresses another user's voice or generation, or an ownerless one (AR-9, AR-10). This includes list contents, a generation request that names another user's voice or reuses another user's generation identifier, and a change or deletion aimed at a built-in Google voice (which AR-9 keeps available to every user).
  - **CTD-4** How the inference service obtains a voice's sample on behalf of the requesting user, and the answer when it cannot (AR-11). This changes the baseline's Voice Sample operation and OAC-4.
  - **CTD-5** What an upload must carry to count as consented (consent statement version 1, AR-13), and the answer to an upload without consent (AR-15).
  - **CTD-6** The answer when cloning names a voice with no consent record (AR-16), and where it falls among the baseline's generation failure answers.
  - **CTD-7** Any operator-set configuration the account operations or the store need (AR-18, PLD-1, PLD-2), including how the PostgreSQL database is named and, if operators can set it, the file folder.
- AR-19 (requirements revision 2) concerns only how passwords and login tokens are kept in the store; it adds no externally observable behavior and needs no contract change. The approved contract is a constraint for every later milestone and is not reopened by this revision.

## Milestones

Decomposition:

- Split: contract — the work item adds account operations and changes an existing contract, so AUM-1 comes first.
- Split: frontend test request delivery (AUM-2) — different verification setup: the frontend RED tests of AUM-3 and AUM-7 need requests made through the account client to reach the request mock, and the AUM-2 planning dry run showed they do not (Current State) [User: AUM2-Q1, 2026-11-16].
- Split: accounts and storage (AUM-3, AUM-4) — separate engineering decision (credential and login handling, simultaneous sign-ups, the PostgreSQL-or-files store design, PLD-1, PLD-2, and keeping passwords and login tokens unreadable, AR-19) and different risk (a security change). The store is merged into this pair because it holds only accounts, logins and consent records [User: milestone merge, 2026-11-16]. The frontend's session check and its use of the contracted sign-up, login and logout (AR-7, UIC-1) are merged into this pair because they are the account behavior seen from the frontend [User: milestone merge, 2026-11-16]. AR-19 belongs here because it is a property of how this pair's store keeps accounts and logins (requirements revision 2).
- Split: service access (AUM-5, AUM-6) — separate engineering decision (the ownership model and ownerless legacy data) and ordering (its tests need real tokens from AUM-4).
- Split: consent (AUM-7, AUM-8) — separate business rule (the consent record and its enforcement), ordering (a consent record names the authenticated account, from AUM-6), and size (adding it to AUM-6 would make one Implementation Plan cover every service change). The frontend's consent tick and the consent an upload carries (AR-13, UIC-2) are merged into this pair because they are the consent behavior seen from the frontend [User: milestone merge, 2026-11-16].

No REFACTOR milestone is planned.

FOUNDATION: one FOUNDATION milestone, AUM-2, is needed. This corrects the 7-milestone revision's statement that no FOUNDATION milestone was needed: that statement held that the frontend test tooling declared in the frontend's package manifest was sufficient, but the AUM-2 planning dry run of 2026-11-16 showed that requests made through the account client are rejected in the frontend test environment before they reach the request mock (Current State). AUM-2 serves AUM-3 Accounts and storage RED and AUM-7 Consent RED, which both need frontend tests that reach the mock server [User: AUM2-Q1, 2026-11-16]. AUM-5 Service access RED has no frontend tests and needs nothing from AUM-2. For every other prerequisite, the repository state projected after each RED milestone's predecessors complete already provides what its tests need (see each RED milestone's Prerequisites).

Milestone numbering, old to new (this revision renumbers every milestone after AUM-1; AUM-1 keeps its number, status and evidence):

| This revision | 7-milestone revision (approved 2026-11-16) | 11-milestone version (before the merge) |
| --- | --- | --- |
| AUM-1 Contract (CONTRACT) | AUM-1 | AUM-1 |
| AUM-2 Frontend test request delivery (FOUNDATION) | none — new | none |
| AUM-3 Accounts and storage RED | AUM-2 | AUM-2 Storage RED, AUM-4 Accounts RED, and the AR-7 and UIC-1 parts of AUM-10 Frontend RED |
| AUM-4 Accounts and storage GREEN | AUM-3 | AUM-3 Storage GREEN, AUM-5 Accounts GREEN, and the AR-7 and UIC-1 parts of AUM-11 Frontend GREEN |
| AUM-5 Service access RED | AUM-4 | AUM-6 |
| AUM-6 Service access GREEN | AUM-5 | AUM-7 |
| AUM-7 Consent RED | AUM-6 | AUM-8 Consent RED, and the AR-13 and UIC-2 parts of AUM-10 |
| AUM-8 Consent GREEN | AUM-7 | AUM-9 Consent GREEN, and the AR-13 and UIC-2 parts of AUM-11 |

References in the approved `docs/.ai/auth-consent/API-Contract.md` that this renumbering makes stale (not edited here; the contract stays as approved). Each cites a 7-milestone number; the milestone now meant is in brackets:

- line 67: "Plan AUM-6" [now AUM-7 Consent RED];
- line 104: "Plan AUM-3" [now AUM-4 Accounts and storage GREEN];
- line 681: "the AUM-3 Implementation Plan" [now AUM-4];
- line 714, CTD-7 row, twice: "left to the AUM-3 Implementation Plan" and "AUM-3 names it" [now AUM-4];
- line 718: "Plan AUM-4" [now AUM-5 Service access RED];
- line 721: "Plan AUM-7" [now AUM-8 Consent GREEN] and "Plan AUM-6" [now AUM-7 Consent RED];
- line 725: "Plan AUM-3" [now AUM-4 Accounts and storage GREEN].

Line 13's "AUM-1" is unchanged. Not caused by the renumbering, line 13 also cites this Plan's status as "Approved … (7-milestone revision)" and the requirements' status as approved on 2026-11-15; both have since been superseded (this revision; requirements revision 2).

### AUM-1 Contract (CONTRACT)

- Capability / purpose: define the externally observable behavior of the account operations, and the changes to the voice and inference services.
- Rationale: every later milestone depends on approved externally observable behavior. A changed contract starts from its baseline.
- Milestone type: CONTRACT.
- Predecessor: Plan approval.
- Scope:
  - `docs/.ai/auth-consent/API-Contract.md`, built from the baseline named in External Contract Requirements, verified against the repository, with the account operations added and the changes for AR-1–AR-18 recorded.
  - Resolve CTD-1–CTD-7.
- Owned requirements / concerns: CTD-1–CTD-7.
- Explicit exclusions: no Implementation Plan, test or code change. No decision beyond CTD-1–CTD-7 and the behavior they need. Nothing excluded by AX-1–AX-5.
- Success criteria: the contract records the baseline source and its verification, a Changes in This Work Item section, and a resolution for each CTD. The user records its approval, and this milestone's Execution Status row then points to it.

### AUM-2 Frontend test request delivery (FOUNDATION)

- Capability / purpose: make the frontend test environment deliver the requests the account client makes to the frontend tests' request mock, so that frontend RED tests can reach the mock server.
- Rationale: test-infrastructure prerequisite [User: AUM2-Q1, 2026-11-16]. In the AUM-2 planning dry run of 2026-11-16, every request made through the account client was rejected in the frontend test environment because of the abort signal the shared HTTP client always attaches (Current State). Without this milestone, the frontend tests of AUM-3 and AUM-7 would fail for an environment reason, which is not valid RED evidence. RED milestones cannot add test infrastructure (Plan Content Rule 11).
- Milestone type: FOUNDATION.
- Predecessor: AUM-1.
- Serves: AUM-3 Accounts and storage RED and AUM-7 Consent RED.
- Scope: in the frontend test environment, a request made through the account client, with the abort signal it always carries, reaches the request mock and receives the mock's answer instead of being rejected. Its Implementation Plan chooses the mechanism [User: AUM2-Q1, 2026-11-16].
- Owned requirements / concerns: frontend test request delivery (AUM2-Q1), the prerequisite for the frontend tests of AUM-3 and AUM-7.
- Explicit exclusions: no tests written or changed, and no assertion removed or weakened. No approved behavior: no account, session, token-check, ownership or consent behavior. No change to the frontend's production behavior, including the shared HTTP client's timeout. No fix of the known pre-existing failures (AUM2-Q2). Nothing excluded by AX-1–AX-5.
- Success criteria: the evidence its Implementation Plan names shows a request made through the account client in the frontend test environment reaching the request mock and receiving its answer, with no abort-signal rejection; the frontend type check (AUV-6) passes; the full frontend suite (AUV-5) passes apart from the known pre-existing failures named in Current State, with no failure beyond them (AUM2-Q2).

### AUM-3 Accounts and storage RED

- Capability / purpose: tests that specify storage of accounts, logins and consent records, with passwords and login tokens never stored in readable form; sign-up, login, login expiry, logout and the session check; and the frontend's checked session and its use of the contracted account operations.
- Rationale: one cohesive account behavior with one security-relevant design decision, together with the store that holds it and the frontend's account behavior [User: milestone merge, 2026-11-16].
- Milestone type: RED.
- Predecessor: AUM-2.
- Scope — tests that verify:
  - with PostgreSQL available, accounts, logins and consent records (account, time, voice, consent version) are stored in PostgreSQL (AR-18, AAC-18);
  - without PostgreSQL, the same records are stored in files in a git-ignored local folder, and sign-up and login work using them (AR-18, AAC-18, PLD-2);
  - the store is chosen once, when a service starts, by whether that service can connect to the configured database (PLD-1);
  - stored records stay readable while the service runs (data durability and retention);
  - after sign-up and login, neither the password nor the login token appears in readable form in the stored accounts, logins or files, with PostgreSQL available and without it (AR-19, AAC-19);
  - through the account operations as AUM-1 defines them: sign-up with a new email and a valid password creates an account that can log in at once, with no verification step (AR-1, AAC-1);
  - the server refuses a password shorter than 8 characters, one with no uppercase letter, and one with no digit (AR-2, AAC-2);
  - emails compare without regard to case; a second sign-up in any letter case is refused with "account already exists"; simultaneous same-email sign-ups leave exactly one account (AR-3, AAC-3, consistency and concurrency);
  - login with the right email and password returns a token, and a wrong email or password is refused (AR-4, AAC-4);
  - a token is accepted before 24 hours from issue and refused after (AR-5, AAC-5);
  - after logout, the token is refused (AR-6, AAC-6);
  - the account operations answer when started as one local process the way the repository's local start-up starts the services (deployment);
  - in the frontend, on page load, a stored session is restored only when the session check accepts its token, with no refresh token needed; a token the account operations or either service refuses logs the user out, and protected pages send the user to the Login page (AR-7, AAC-7);
  - the frontend's Signup, Login and logout actions use the account operations as AUM-1 defines them: a new sign-up lands logged in on the voice page (AS-1); "account already exists" is shown for an existing email (AS-2); logout ends the login on the server (UIC-1);
  - existing tests of the unstarted auth and consent applications (Current State) that conflict with these behaviors are changed to match them (Q19);
  - existing frontend tests and test mocks that encode refresh tokens or unverified session restore are changed to the approved behavior (Q19, AX-5).
- Owned requirements / concerns: none delivered. Verifies AR-1–AR-7, AR-18, AR-19, PLD-1, PLD-2, UIC-1, consistency and concurrency, deployment, dependency failure (PostgreSQL absent), and data durability and retention.
- Prerequisites (Plan Content Rule 11): the Python test runner, the HTTP test client, the PostgreSQL client library, the existing PostgreSQL test harness and the way existing tests start a service as its own process are present (Current State). The frontend test runner, request mocking and component-test tooling are declared in the frontend's package manifest (Current State); installing them (AUV-4) changes no tracked file. After AUM-2, requests the account client makes in the frontend test environment reach the request mock. AUM-1 changes no executable artifact.
- Explicit exclusions: no production code. No token checks in the voice or inference services. No consent behavior. No email verification, refresh token, failed-login limit or administrator role. No writes to the developer's own local PostgreSQL database or to tracked repository files. No fix of the known pre-existing failures (AUM2-Q2).
- Success criteria: the new and changed tests compile and fail only because the approved storage, account and frontend session behavior is absent. Every other test keeps its baseline result.

### AUM-4 Accounts and storage GREEN

- Capability / purpose: the store for accounts, logins and consent records, keeping passwords and login tokens unreadable; working sign-up, login, login expiry, logout and session check; and real, checked sessions and contracted account calls in the frontend.
- Rationale: the smallest change that makes the AUM-3 evidence pass.
- Milestone type: GREEN.
- Predecessor: AUM-3.
- Scope:
  - accounts, logins and consent records are stored in PostgreSQL when it is available and in files otherwise, chosen once at service start (PLD-1) and kept in a git-ignored local folder (PLD-2), with any operator setting as AUM-1 defines (CTD-7);
  - passwords and login tokens are kept in that store, in PostgreSQL and in files, only in a form from which they cannot be read (AR-19);
  - the account operations as AUM-1 defines them, using that store, with AR-1–AR-6 behavior;
  - the repository's local start-up starts whatever the account operations need, one instance each (deployment);
  - in the frontend, session restore checks the token with the account operations, needing no refresh token; a refused token logs out and redirects protected pages to Login; Signup, Login and logout use the contracted account operations (AR-7, UIC-1).
- Owned requirements / concerns: AR-1, AR-2, AR-3, AR-4, AR-5, AR-6, AR-7, AR-18, AR-19, PLD-1, PLD-2, UIC-1, consistency and concurrency, deployment, data durability and retention, and dependency failure (PostgreSQL absent).
- Explicit exclusions: no token checks in the voice or inference services. No consent behavior. No change to how generation records are stored. No change to the Signup page's existing password check. Nothing excluded by AX-3–AX-5, and no failed-login limit. No fix of the known pre-existing failures (AUM2-Q2).
- Success criteria: the AUM-3 tests pass, and every verification command for a GREEN milestone passes, including the frontend type check, apart from the known pre-existing failures named in Current State, with no failure beyond them (AUM2-Q2).

### AUM-5 Service access RED

- Capability / purpose: tests that specify token checks and per-user ownership in the voice and inference services.
- Rationale: the ownership model and the treatment of ownerless data are one design decision across both services. The tests need real tokens from AUM-4.
- Milestone type: RED.
- Predecessor: AUM-4.
- Scope — tests that verify:
  - every voice-service and inference-service operation except the two AR-8 leaves open refuses a request with no token, with an invalid token, and with an expired token, answering as AUM-1 defines (AR-8, AAC-8);
  - a user's voice lists and generation lists contain only their own items plus the built-in Google voices; reading, playing, downloading, using, changing or deleting another user's item is refused (AR-9, AAC-9);
  - voices and generations with no owner appear in no list and are refused to every user (AR-10, AAC-10);
  - a cloning request for a voice the requester does not own cannot fetch that voice's sample (AR-11, AAC-11);
  - when the account store cannot be read, voice and inference requests are refused (AR-12, AAC-12, dependency failure — account store unreadable);
  - existing voice-service and inference-service tests that call protected operations without a token, or assert a list shared by every caller, are changed to call as an authenticated owner and to assert the per-user behavior, without removing any other assertion.
- Owned requirements / concerns: none delivered. Verifies AR-8–AR-12, and dependency failure (account store unreadable).
- Prerequisites (Plan Content Rule 11): after AUM-4, tokens can be obtained from the account operations and the store exists. The services' existing test patterns are present (Current State). This milestone has no frontend tests, so it needs nothing from AUM-2.
- Explicit exclusions: no production code. No consent behavior. No frontend change. No administrator access to other users' items.
- Success criteria: the new and changed tests compile and fail only because the approved access behavior is absent. Every other test keeps its baseline result.

### AUM-6 Service access GREEN

- Capability / purpose: token checks and per-user ownership in both services.
- Rationale: the smallest change that makes the AUM-5 evidence pass.
- Milestone type: GREEN.
- Predecessor: AUM-5.
- Scope: both services check the token on every operation except the two AR-8 leaves open. Each voice and generation belongs to its creator. Ownerless legacy items are shown to and usable by no one. The inference service fetches a sample only on behalf of the voice's owner. Requests are refused when the account store cannot be read. All of this as AUM-1 defines it.
- Owned requirements / concerns: AR-8, AR-9, AR-10, AR-11, AR-12, dependency failure (account store unreadable).
- Explicit exclusions: no consent behavior. No frontend change. No change to retention, providers or Chatterbox behavior beyond what AUM-1 changes. Nothing excluded by AX-1. No fix of the known pre-existing failures (AUM2-Q2).
- Success criteria: the AUM-5 tests pass, and every verification command for a GREEN milestone passes, apart from the known pre-existing failures named in Current State, with no failure beyond them (AUM2-Q2).

### AUM-7 Consent RED

- Capability / purpose: tests that specify consent recording and enforcement in the services, and the frontend's consent tick and the consent an upload carries.
- Rationale: a separate business rule, reviewed on its own, together with its frontend behavior [User: milestone merge, 2026-11-16].
- Milestone type: RED.
- Predecessor: AUM-6.
- Scope — tests that verify:
  - after a consented upload, a consent record exists with the account, the time, the voice and version 1 (AR-14, AAC-14);
  - an upload without consent is rejected by the voice service and stores no voice (AR-15, AAC-15);
  - cloning with a voice that has no consent record is refused (AR-16, AAC-16);
  - in the frontend, the recording and upload controls stay unusable until the statement "I own this voice or have the speaker's informed permission to clone it" (version 1) is ticked (AR-13, AAC-13);
  - a recording or upload made after the tick carries consent as AUM-1 defines it (UIC-2);
  - existing backend tests, and existing frontend tests and test mocks, that upload without consent are changed to upload with consent, without removing any other assertion.
- Owned requirements / concerns: none delivered. Verifies AR-13, AR-14, AR-15, AR-16, UIC-2.
- Prerequisites (Plan Content Rule 11): after AUM-6, authenticated, owner-scoped uploads and cloning exist. The store holds consent records (AUM-4). The frontend test tooling is declared in the frontend's package manifest (Current State) and installed by AUV-4. After AUM-4, the frontend's protected pages, where recording and upload are offered, depend on the session check made through the account client; after AUM-2, those requests reach the request mock in the frontend test environment.
- Explicit exclusions: no production code. No separate consent-withdraw action. No refresh token. No fix of the known pre-existing failures (AUM2-Q2).
- Success criteria: the new and changed tests compile and fail only because the approved consent behavior is absent. Every other test keeps its baseline result.

### AUM-8 Consent GREEN

- Capability / purpose: consent recording and enforcement in the services, and the consent tick in the frontend.
- Rationale: the smallest change that makes the AUM-7 evidence pass.
- Milestone type: GREEN.
- Predecessor: AUM-7.
- Scope:
  - a consented upload records who consented, when, for which voice, and version 1. An upload without consent is rejected and stores nothing. Cloning refuses a voice with no consent record. All of this as AUM-1 defines it. Deleting a voice still deletes its sample (AR-17, preserved);
  - in the frontend, recording and upload require the version 1 consent tick and send consent as contracted (AR-13, UIC-2).
- Owned requirements / concerns: AR-13, AR-14, AR-15, AR-16, UIC-2.
- Explicit exclusions: no separate withdraw action. No change to retention. No refresh token. No fix of the known pre-existing failures (AUM2-Q2).
- Success criteria: the AUM-7 tests pass, and every verification command for a GREEN milestone passes, including the frontend type check and the existing voice-deletion test named in Current State, as changed by AUM-5 and AUM-7, apart from the known pre-existing failures named in Current State, with no failure beyond them (AUM2-Q2).

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| AR-1 Sign-up; can log in at once, no verification | AUM-4 | AUM-3 |
| AR-2 Server password rule (with Business Context password rule, server part) | AUM-4 | AUM-3 |
| AR-3 Case-insensitive email, "account already exists", one account for simultaneous sign-ups (with Business Context identity rule) | AUM-4 | AUM-3 |
| AR-4 Login returns a token; wrong email or password refused | AUM-4 | AUM-3 |
| AR-4 "No limit on failed login attempts is required" | none — exclusion | Final Review |
| AR-5 24-hour login, then refused | AUM-4 | AUM-3 |
| AR-6 Logout ends the login on the server | AUM-4 | AUM-3 |
| AR-7 Real, checked frontend session; refused token logs out and redirects | AUM-4 | AUM-3 |
| AR-8 Token check on every 8002/8003 operation except the two left open | AUM-6 | AUM-5 |
| AR-9 Own voices and generations only; Google voices for everyone | AUM-6 | AUM-5 |
| AR-10 Ownerless legacy items shown to and usable by no one | AUM-6 | AUM-5 |
| AR-11 Sample fetched only on behalf of the owner | AUM-6 | AUM-5 |
| AR-12 Account store unreadable → refuse | AUM-6 | AUM-5 |
| AR-13 Consent tick, version 1, before recording or upload (with Business Context per-voice consent rule) | AUM-8 | AUM-7 |
| AR-14 Consent record: account, time, voice, version | AUM-8 | AUM-7 |
| AR-15 Upload without consent rejected | AUM-8 | AUM-7 |
| AR-16 Cloning refuses a voice with no consent record | AUM-8 | AUM-7 |
| AR-17 Deleting a voice deletes its sample | none — preserved | AUM-8 (existing test `tests/test_voice_sample_persistence_red.py:410` in its full-suite run) |
| AR-17 No separate withdraw action | none — exclusion | Final Review |
| AR-18 PostgreSQL when available, files otherwise; loss on restart acceptable | AUM-4 | AUM-3 |
| AR-19 Passwords and login tokens never stored in readable form | AUM-4 | AUM-3 |
| Business Context password rule, UI part (Signup page check, `Signup.tsx:40`) | none — preserved | Final Review (no existing test checks it: `frontend/tests/auth.spec.tsx` cases are placeholders) |
| PLD-1 Store chosen once at service start | AUM-4 | AUM-3 |
| PLD-2 Files in a git-ignored local folder | AUM-4 | AUM-3 |
| UIC-1 Signup, Login and logout use the contracted account operations (AS-1, AS-2, logout on server) | AUM-4 | AUM-3 |
| UIC-2 Recording and upload send consent as contracted | AUM-8 | AUM-7 |
| Frontend test request delivery (AUM2-Q1), prerequisite for AUM-3 and AUM-7 | AUM-2 | AUM-2 (its completion evidence) |
| Known pre-existing failures not made worse (AUM2-Q2) | none — preserved | AUM-2, AUM-4, AUM-6 and AUM-8 (their full-suite runs compared with the known failures in Current State) |
| CTD-1 Account operations | AUM-1 | human review |
| CTD-2 Token presentation, refusals, preflight | AUM-1 | human review |
| CTD-3 Answers for other users' and ownerless items | AUM-1 | human review |
| CTD-4 Owner-only sample fetch | AUM-1 | human review |
| CTD-5 Consented upload | AUM-1 | human review |
| CTD-6 Cloning without a consent record | AUM-1 | human review |
| CTD-7 Operator-set configuration | AUM-1 | human review |
| Operational — scale | none — not required | none |
| Operational — deployment (one instance of each, run locally as today) | AUM-4 | AUM-3 |
| Operational — availability and latency | none — not required | none |
| Operational — consistency and concurrency (one account for simultaneous sign-ups) | AUM-4 | AUM-3 |
| Operational — dependency failure: PostgreSQL absent → files | AUM-4 | AUM-3 |
| Operational — dependency failure: account store unreadable → refuse | AUM-6 | AUM-5 |
| Operational — observability | none — not required | none |
| Operational — data durability and retention (kept until restart) | AUM-4 | AUM-3 |
| AX-1 Background jobs, object storage, scaling, observability, mobile formats, CORS hardening beyond auth, deploying | none — exclusion | Final Review |
| AX-2 Deploying to Cloud Run | none — exclusion | Final Review |
| AX-3 Administrator role | none — exclusion | Final Review |
| AX-4 Email verification | none — exclusion | Final Review |
| AX-5 Refresh tokens | none — exclusion | Final Review |

## Verification Commands

| ID | Command (from the repository root unless stated) | Use | Source |
| --- | --- | --- | --- |
| AUV-1 | `python -m pytest <test files> -q` | Scoped backend runs: RED execution and dry runs (AUM-3, AUM-5, AUM-7) | `pytest.ini` (`testpaths = tests`, `pythonpath = .`); `requirements-dev.txt` (`pytest==9.1.1`) |
| AUV-2 | `python -m pytest -q` | The full backend suite, once per GREEN execution (AUM-4, AUM-6, AUM-8). It includes the Docker-dependent files (`tests/test_persistence.py`, `tests/test_authentication_consent.py`, `tests/test_voice_enrollment.py`). Known: the run aborts with exit code 127 inside `tests/test_voice_enrollment.py`, and `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing` fails (Current State, AUM2-Q2); a result is accepted only when it is no worse than these | `pytest.ini`; Docker available (Current State); AUM-2 planning dry run of 2026-11-16 |
| AUV-3 | `git status --short -- audio_storage` must print nothing | After every backend test run, because generation files are tracked | `git ls-files audio_storage` (25 tracked files) |
| AUV-4 | `npm ci` (in `frontend/`) | Before frontend test runs in a worktree without `node_modules`; changes no tracked file | `frontend/package.json`, `frontend/package-lock.json` |
| AUV-5 | `npx vitest run` (in `frontend/`); scoped: `npx vitest run <test file>` | Frontend tests: scoped in AUM-3 and AUM-7; the full frontend suite once in AUM-2, AUM-4 and AUM-8. Known: 90 failures, 27 in `tts.spec.tsx` and 63 in `voice.spec.tsx` (Current State, AUM2-Q2); a result is accepted only when it is no worse than these | `frontend/package.json` (`"test": "vitest"`), `frontend/vitest.config.ts`; AUM-2 planning dry run of 2026-11-16 |
| AUV-6 | `npm run type-check` (in `frontend/`) | AUM-2, AUM-3, AUM-4, AUM-7 and AUM-8 | `frontend/package.json` (`"type-check": "tsc --noEmit"`) |

AUM-2's own completion evidence (a request through the account client reaching the request mock) is named by its Implementation Plan. Output is written to log files, and only summaries and failing tests are recorded (`prompt-driven-development` Test Scope and Output). AUM-1 runs no command.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| AUM-1 Contract (CONTRACT) | Complete — contract approved by Avinash Srivastava on 2026-11-16 | `docs/.ai/auth-consent/API-Contract.md` |
| AUM-2 Frontend test request delivery (FOUNDATION) | Complete — executed and verified 2026-11-16 (`001_Implementation_Plan_AUM-2.md`) | See "AUM-2 evidence" below |
| AUM-3 Accounts and storage RED | Pending | |
| AUM-4 Accounts and storage GREEN | Pending | |
| AUM-5 Service access RED | Pending | |
| AUM-6 Service access GREEN | Pending | |
| AUM-7 Consent RED | Pending | |
| AUM-8 Consent GREEN | Pending | |

### AUM-2 evidence

Executed 2026-11-16 from `001_Implementation_Plan_AUM-2.md` (FOUNDATION), HEAD `f3372ce`. Logs in `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/aum2-exec-logs/` (outside the repository); only summaries are recorded here.

| Step | Command as run | Result |
| --- | --- | --- |
| 1 | `git status --short` (repository root) | `?? docs/.ai/auth-consent/` |
| 2 | `npm ci` (AUV-4) | exit 0 |
| 3 | `npx vitest run` on the unmodified repository (AUV-5, baseline) | exit 1; `Test Files  2 failed \| 3 passed (5)`; `Tests  90 failed \| 282 passed (372)`; failing tests: 27 in `tests/tts.spec.tsx`, 63 in `tests/voice.spec.tsx` (list saved as `aum2-baseline-fails.txt`) — matches the known failures in Current State |
| 4 | temporary check created; `npx vitest run .vitest/aum2-check` before the change | exit 1; `Tests  2 failed (2)`; both `TypeError: RequestInit: Expected signal ("AbortSignal {}") to be an instance of AbortSignal.` — FTC-3 met |
| 5 | created `frontend/tests/environment/jsdom-node-abort.ts`; `git apply --check -v` then `git apply` of the `vitest.config.ts` diff | `Checking patch frontend/vitest.config.ts...`; both exit 0; line 8 now `environment: './tests/environment/jsdom-node-abort.ts',` |
| 6 | `npx vitest run .vitest/aum2-check` | exit 0; `Tests  2 passed (2)`; `grep -c "Expected signal"` → `0` — FTC-1, FTC-2 met |
| 7 | `npx vitest run .vitest/aum2-check` (second run, no cleaning) | exit 0; `Tests  2 passed (2)`; `grep -c "Expected signal"` → `0` — FTC-2 repeat met |
| 8 | `rm -rf .vitest`; `ls -a` | no `.vitest` entry |
| 9 | `npm run type-check` (AUV-6) | exit 0 (`tsc --noEmit`, no errors) — FTC-4 met |
| 10 | `npx vitest run` (AUV-5) | exit 1; `Test Files  2 failed \| 3 passed (5)`; `Tests  90 failed \| 282 passed (372)`; failing-test list identical to step 3 (new failures: none; baseline failures now passing: none) — FTC-5 met (AUM2-Q2: no worse) |
| 11 | `git status --short`; `git diff --stat -- frontend/src frontend/tests frontend/package.json frontend/package-lock.json` | ` M frontend/vitest.config.ts`, `?? docs/.ai/auth-consent/`, `?? frontend/tests/environment/`; diff stat empty — FTC-6 met |

Deviations: (1) step 1 used a fixed log folder in the session scratchpad instead of `mktemp -d`; it is outside the repository as the plan requires. (2) vitest wrote ANSI color codes to the logs, so the summaries and ` FAIL ` lines were extracted after stripping them with `sed 's/\x1b\[[0-9;]*m//g'`; no command was rerun for this. Pre-authorized contingencies: none listed. Processes started: none left running (every `vitest run` and `tsc` exited).

## Risks

- **AUR-1 Pre-existing failures.** The AUM-2 planning dry run of 2026-11-16 recorded failures outside this work item: the full backend run aborting with exit code 127 inside `tests/test_voice_enrollment.py` (cause unknown), `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing`, and 90 frontend failures (27 `tts.spec.tsx`, 63 `voice.spec.tsx`) (Current State). Mitigation: these are recorded as known and must not get worse; they are not fixed here [User: AUM2-Q2, 2026-11-16]. Each Implementation Plan records its own baseline of these named failures before any change, and its run is accepted only when its failures are no worse than them (`implementation-planning` Pre-existing Failures).
- **AUR-2 Tests touching real data.** Tests could write to the developer's local PostgreSQL (port 5432 is open) or to tracked `audio_storage/` files. Mitigation: AUM-3 excludes writes to them, and AUV-3 checks `audio_storage` after every backend run. Implementation Plans use isolated test storage, as the existing tests do (`tests/test_persistence.py:59-83`, `tests/test_voice_sample_persistence_red.py:1-7`).
- **AUR-3 Services choosing different stores.** Under PLD-1, a service started while PostgreSQL was unavailable uses files, and one started later may use PostgreSQL. Tokens issued in one store are then refused by services using the other. Mitigation: `start-all.bat` starts the services together. The user restarts them together. If that is not acceptable, PLD-1 is revised at Plan review.
- **AUR-4 Browser preflight versus AR-8.** Browsers send cross-origin preflight requests without the token. The voice service answers them through its own handler (`voice_narration/simple_voices/application.py:243-254`). Mitigation: resolved by CTD-2 in the approved contract (AUM-1) within AX-1; AUM-5 and AUM-6 follow it.
- **AUR-5 Implementation Plan size.** AUM-6 changes both services (`voice_narration/simple_voices/application.py`, 271 lines; `voice_narration/inference/application.py`, 668 lines). After the merge, AUM-4 covers the store, the account operations, the local start-up (`start-all.bat`, 53 lines) and the frontend session (`frontend/src/context/AuthContext.tsx`, 153 lines; `frontend/src/services/api/authClient.ts`, 53 lines), and AUM-8 covers consent in the voice and inference services and in the frontend's recorder and upload form (`frontend/src/components/VoiceRecorder.tsx`, 285 lines; `frontend/src/components/VoiceUpload.tsx`, 464 lines). Mitigation: if any of their Implementation Plans is too large to review as exact code, it stops for replanning rather than growing.
- **AUR-6 Ownerless legacy data.** Existing voices in `voice_storage/`, tracked generations in `audio_storage/generation_index.json`, and database generation rows have no owner. Mitigation: AR-10 hides them from everyone. AUM-5 tests that, and no milestone migrates or deletes them.
- **AUR-7 FOUNDATION changing production behavior.** The abort signal that the test environment rejects is attached by production code, the shared HTTP client's timeout (`frontend/src/services/api/httpClient.ts:89-100`). A mechanism that changed that client would change the frontend's production behavior. Mitigation: AUM-2 excludes any change to the frontend's production behavior; its Implementation Plan chooses a mechanism within that exclusion, or stops for replanning if none exists.
- **AUR-8 Results hidden by the backend abort.** Because the full backend run aborts inside `tests/test_voice_enrollment.py` (Current State), tests the run would reach after that point produce no result in AUV-2. Mitigation: within the scope of AUM2-Q2, each RED milestone runs its new and changed test files with AUV-1, and each GREEN Implementation Plan lists its affected tests and runs them with AUV-1 in addition to AUV-2 (`prompt-driven-development` Test Scope and Output); the abort itself is not fixed here.

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| AAC-1 Sign-up creates an account that can log in immediately | requirements | AUM-4 |
| AAC-2 Server refuses each password-rule failure | requirements | AUM-4 |
| AAC-3 "account already exists" in any letter case; one account for simultaneous sign-ups | requirements | AUM-4 |
| AAC-4 Right credentials return a token; wrong ones are refused | requirements | AUM-4 |
| AAC-5 Token accepted before 24 hours, refused after | requirements | AUM-4 |
| AAC-6 Token refused after logout | requirements | AUM-4 |
| AAC-7 Session restored only when the backend accepts the token; refused token logs out and redirects | requirements | AUM-4 |
| AAC-8 Every 8002/8003 operation except the two left open refuses missing, invalid and expired tokens | requirements | AUM-6 |
| AAC-9 Lists hold only own items plus Google voices; others' items refused | requirements | AUM-6 |
| AAC-10 Ownerless items in no list and refused to all | requirements | AUM-6 |
| AAC-11 Cloning cannot fetch a sample of a voice the requester does not own | requirements | AUM-6 |
| AAC-12 Account store unreadable → voice and inference requests refused | requirements | AUM-6 |
| AAC-13 Recording and upload unusable until the version 1 statement is ticked | requirements | AUM-8 |
| AAC-14 Consent record with account, time, voice and version 1 after a consented upload | requirements | AUM-8 |
| AAC-15 Upload without consent rejected; no voice stored | requirements | AUM-8 |
| AAC-16 Cloning with a voice without a consent record refused | requirements | AUM-8 |
| AAC-17 Deleting a voice removes its sample | requirements | AUM-8 (preserved test in its full-suite run) |
| AAC-18 PostgreSQL used when available; files otherwise | requirements | AUM-4 |
| AAC-19 Neither password nor login token readable in stored accounts, logins or files after sign-up and login | requirements (revision 2) | AUM-4 |
| Local start-up starts everything the account operations need, one instance each | requirements (Operational Characteristics, deployment) | AUM-4, and Final Review inspection of the start-up script |
| Known pre-existing failures not made worse | AUM2-Q2 [User: AUM2-Q2, 2026-11-16] | AUM-2, AUM-4, AUM-6 and AUM-8 full-suite runs |
| Exclusions AX-1–AX-5, no failed-login limit, no separate withdraw action | requirements | Final Review inspection |
