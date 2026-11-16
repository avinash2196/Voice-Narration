# Requirements — auth-consent

Every item ends with one source label:

- `[User: brief]` or `[User: Qn]` — stated by the user, in the brief or in the answer to clarification question n (see Clarification Log).
- `[Repo: <path>:<line>]` — established by inspecting the current repository during this capture.
- `[Derived from recommended option — confirmed Qn]` — an option the user accepted with "use recommended" and then confirmed.
- `[Left to <phase> — non-blocking]` — valid only in Non-Blocking Decisions.

## Goal

Give the app real sign-up and login, check the login token on every voice-service (8002) and inference-service (8003) request, keep each user's voices and generations private to that user, and record explicit consent before a voice sample is recorded or uploaded for cloning. [User: brief]

## Status

Approved by Avinash Srivastava on 2026-11-16 (revision 2: adds AR-19 from Q26). Revision 1 was approved by Avinash Srivastava on 2026-11-15.

## Relationship to Product-Level Requirements

There is no product-level `docs/requirements.md`. [Repo: docs/ — no requirements.md]

`voice_narration_PDD_requirements.md` (repository root, status "Proposed") is context only for this work item; this work item's answers decide. [User: Q21 — Derived from recommended option, confirmed Q21]

## Business Context

- **Problem:** No one without an account may use the app or get a voice sample, and every cloned voice must have a consent record. Today login has no backend and every endpoint is open. [Derived from recommended option — confirmed Q1]
- **Outcome, and how it is seen:** requests without a valid token are refused, and every new voice has a consent record. [Derived from recommended option — confirmed Q1]
- **Actors:** ordinary users only; there is no administrator role. [Derived from recommended option — confirmed Q2]
- **What a user may do:** sign up, log in, log out, and list, read, play, download, use, change and delete only their own voices and generations. Built-in Google voices stay available to every user. [Derived from recommended option — confirmed Q3]
- **Rule — identity:** an account is identified by its email address, compared without regard to case; one account per email address. [Derived from recommended option — confirmed Q6]
- **Rule — password:** at least 8 characters, with at least 1 uppercase letter and 1 digit, enforced by the server as well as the UI. [Derived from recommended option — confirmed Q6]
- **Rule — consent:** consent is given for each voice, before its sample is recorded or uploaded. [User: brief; Derived from recommended option — confirmed Q11]

## Repository-Confirmed Facts

- The frontend sends sign-up and login to `AUTH_SERVICE`, default `http://localhost:9000`. [Repo: frontend/src/utils/api-config.ts:8]
- The frontend auth client calls `/auth/signup`, `/auth/login`, `/auth/refresh`, `/auth/validate` and `/auth/logout`. [Repo: frontend/src/services/api/authClient.ts:23, :28, :33, :39, :47]
- The Signup page checks the password for at least 8 characters, an uppercase letter and a digit, and sends `agreedToTerms`. [Repo: frontend/src/pages/Auth/Signup.tsx:40, :88]
- On load, `AuthContext` restores any stored token as a hard-coded user named "Test User" without asking a backend. [Repo: frontend/src/context/AuthContext.tsx:121, :126]
- The frontend already sends `Authorization: Bearer <token>` to the inference service. [Repo: frontend/src/services/ttsApi.ts:50]
- `start-all.bat` starts only the voice service, the inference service and the frontend; nothing listens on port 9000. [Repo: start-all.bat:39-41]
- `voice_narration/auth/` and `voice_narration/consent/` hold an auth app (`/api/v1/auth/register`, `/verify-email`, `/login`, `/me`) and a consent app (`/api/v1/consent/record`, `/api/v1/consent/{consent_id}`) that nothing starts; the auth app stores accounts in PostgreSQL tables. [Repo: voice_narration/auth/application.py:28, :34, :39, :44; voice_narration/consent/application.py:98, :105; voice_narration/auth/accounts.py:57]
- The voice service accepts uploads at `/voice/upload` and marks every upload `approved` at once; it serves samples at `/voices/{voice_id}/sample`; it checks no token. [Repo: voice_narration/simple_voices/application.py:94, :133, :184]
- Voice samples are kept for 120 hours. [Repo: voice_narration/simple_voices/store.py:13]
- The inference service accepts an `owner_id` that nothing uses, and records generations in `generation_index.json`. [Repo: voice_narration/inference/application.py:285, :110]
- The inference service fetches a voice sample from the voice service itself when cloning. [Repo: voice_narration/inference/chatterbox.py:146]
- Recording and upload are offered on the Voice Management page. [Repo: frontend/src/pages/VoiceManagement.tsx:128, :140]
- Existing auth tests: `frontend/tests/auth.spec.tsx`, `frontend/tests/auth-api.spec.tsx`, `tests/test_authentication_consent.py`. [Repo: those paths]

## Requirements

### Sign-up and login

- **AR-1** A user signs up with email and password on the existing Signup page; the account can log in at once, with no email verification. [User: brief; Derived from recommended option — confirmed Q5]
- **AR-2** The server refuses a password that is shorter than 8 characters, or has no uppercase letter, or has no digit. [Derived from recommended option — confirmed Q6]
- **AR-3** Email addresses compare without regard to case. Signing up with an email that already has an account is refused, and the user sees "account already exists". Two sign-ups with the same email at the same moment produce exactly one account. [Derived from recommended option — confirmed Q6, Q18]
- **AR-4** A user logs in with email and password on the existing Login page and receives a token; a wrong email or password is refused. No limit on failed login attempts is required. [User: brief; Derived from recommended option — confirmed Q8]
- **AR-5** A login lasts 24 hours from when it is issued; after that its token is refused and the user must log in again. There is no refresh token. [Derived from recommended option — confirmed Q7]
- **AR-6** Logout ends the login on the server: its token is refused afterwards. [Derived from recommended option — confirmed Q7]
- **AR-7** The token the frontend stores is real and is checked: a restored session is used only if the backend accepts its token, and a refused token logs the user out and sends protected pages to the Login page. [User: brief]

### Token checks and ownership

- **AR-8** Every voice-service (8002) and inference-service (8003) endpoint refuses a request without a valid token, except `/health` and `/inference/backends`. [User: brief; Derived from recommended option — confirmed Q15]
- **AR-9** Each voice and each generation belongs to the user who created it. A user can list, read, play, download, use, change and delete only their own; built-in Google voices stay available to every user. [Derived from recommended option — confirmed Q3]
- **AR-10** Voices and generations that existed before this work item and have no owner are shown to and usable by no one. [Derived from recommended option — confirmed Q4]
- **AR-11** The inference service can fetch a voice sample only on behalf of that voice's owner. [Derived from recommended option — confirmed Q16]
- **AR-12** If the account store cannot be read, the voice and inference services refuse the request. [Derived from recommended option — confirmed Q17]

### Consent

- **AR-13** Before a user records or uploads a voice sample for cloning, the user must explicitly tick the statement "I own this voice or have the speaker's informed permission to clone it" (consent version 1); recording and upload cannot start until it is ticked. [User: brief; Derived from recommended option — confirmed Q10, Q11]
- **AR-14** Each consent is recorded with who gave it (the account), when, which voice, and the consent version. [User: brief; Derived from recommended option — confirmed Q10, Q11]
- **AR-15** The voice service rejects an upload that comes without consent. [Derived from recommended option — confirmed Q12]
- **AR-16** Cloning refuses a voice that has no consent record. [Derived from recommended option — confirmed Q12]
- **AR-17** Consent is withdrawn by deleting the voice, which deletes its sample; there is no separate withdraw action. [Derived from recommended option — confirmed Q13]

### Storage

- **AR-18** Accounts, logins and consent records are stored in PostgreSQL when it is available, and in files otherwise. Losing them on a restart is acceptable. [User: Q9, Q23]

### Stored secrets

- **AR-19** Passwords and login tokens are never stored in readable form. [Derived from recommended option — confirmed Q26]

## Scenarios

- **AS-1** A new user signs up with `Ann@Example.com` and a valid password and lands on `/voices`, logged in. → AAC-1
- **AS-2** Signing up again with `ann@example.com` shows "account already exists". → AAC-3
- **AS-3** Signing up with password `password1` (no uppercase) is refused by the server. → AAC-2
- **AS-4** Logging in with a wrong password is refused; with the right password it succeeds. → AAC-4
- **AS-5** 24 hours after login, the next request is refused and the user is sent to Login. → AAC-5, AAC-7
- **AS-6** After logout, a request with the old token is refused. → AAC-6
- **AS-7** A request to 8002 or 8003 without a token is refused, except `/health` and `/inference/backends`. → AAC-8
- **AS-8** User B asks for user A's voice sample or generation, or tries to clone with user A's voice: refused, and A's voice does not appear in B's list. → AAC-9, AAC-11
- **AS-9** A voice uploaded before this work item appears in no user's list. → AAC-10
- **AS-10** A user tries to record or upload without ticking consent: the UI does not allow it, and a direct upload without consent is rejected by the voice service. → AAC-13, AAC-15
- **AS-11** Cloning with a voice that has no consent record is refused. → AAC-16
- **AS-12** A user deletes a voice; its sample is gone. → AAC-17
- **AS-13** The services restart while PostgreSQL is not available; previous accounts and logins no longer work and users sign up again. → AAC-18
- **AS-14** The account store cannot be read; a voice or inference request is refused. → AAC-12

## Operational Characteristics

| Characteristic | Answer | Source |
|----------------|--------|--------|
| Scale | Not required for this work item | [Derived from recommended option — confirmed Q20] |
| Deployment | One instance of each service, run locally as `start-all.bat` does today | [Derived from recommended option — confirmed Q24] |
| Availability and latency | Not required for this work item | [Derived from recommended option — confirmed Q20] |
| Consistency and concurrency | Two sign-ups with the same email at the same moment produce exactly one account | [Derived from recommended option — confirmed Q18] |
| Dependency failure | PostgreSQL absent: use files (AR-18). Account store unreadable: refuse the request (AR-12) | [User: Q9; Derived from recommended option — confirmed Q17] |
| Observability | Not required for this work item | [Derived from recommended option — confirmed Q20] |
| Data durability and retention | Accounts, logins and consent records are kept until a restart; losing them on a restart is acceptable | [User: Q14, Q23] |

## Decisions Deferred to Later Milestones

None.

## Explicit Exclusions

- **AX-1** Background generation jobs, object storage, scaling, observability, mobile recording formats, CORS hardening beyond what auth needs, and deploying. [User: brief]
- **AX-2** Deploying to Cloud Run. [User: Q22]
- **AX-3** An administrator role. [Derived from recommended option — confirmed Q2]
- **AX-4** Email verification. [Derived from recommended option — confirmed Q5]
- **AX-5** Refresh tokens. [Derived from recommended option — confirmed Q7]

## Non-Blocking Decisions

- How "PostgreSQL is available" is detected, and where the files are kept. [Left to Plan — non-blocking]

## Acceptance Criteria

- **AAC-1** (AR-1) Sign-up with a new email and a valid password creates an account that can log in immediately.
- **AAC-2** (AR-2) The server refuses each of: fewer than 8 characters, no uppercase letter, no digit.
- **AAC-3** (AR-3) A second sign-up with the same email in any letter case is refused with "account already exists"; two simultaneous sign-ups with the same email leave exactly one account.
- **AAC-4** (AR-4) Login with the right email and password returns a token; a wrong email or password is refused.
- **AAC-5** (AR-5) A token is accepted before 24 hours from issue and refused after.
- **AAC-6** (AR-6) After logout, the token is refused.
- **AAC-7** (AR-7) On page load the frontend restores a session only when the backend accepts its token; a refused token logs the user out and protected pages redirect to Login.
- **AAC-8** (AR-8) Every 8002 and 8003 endpoint except `/health` and `/inference/backends` refuses a request without a token, with an invalid token, and with an expired token.
- **AAC-9** (AR-9) A user's voice and generation lists contain only their own items (plus built-in Google voices); reading, playing, downloading, using, changing or deleting another user's item is refused.
- **AAC-10** (AR-10) Voices and generations with no owner appear in no list and are refused to every user.
- **AAC-11** (AR-11) A cloning request for a voice the requester does not own cannot fetch that voice's sample.
- **AAC-12** (AR-12) When the account store cannot be read, voice and inference requests are refused.
- **AAC-13** (AR-13) Recording and upload controls stay unusable until the consent statement, version 1, is ticked.
- **AAC-14** (AR-14) After a consented upload, a consent record exists with the account, the time, the voice and version 1.
- **AAC-15** (AR-15) An upload without consent is rejected by the voice service and stores no voice.
- **AAC-16** (AR-16) Cloning with a voice that has no consent record is refused.
- **AAC-17** (AR-17) Deleting a voice removes its sample.
- **AAC-18** (AR-18) With PostgreSQL available, accounts and consent records are stored there; without it, sign-up, login and consent work using files.
- **AAC-19** (AR-19) After sign-up and login, neither the password nor the login token appears in readable form in the stored accounts, logins or files.

## Clarification Log

| Q | Question | Answer |
|---|----------|--------|
| Q1 | Problem and outcome? | Recommended option, confirmed: no access without an account; every cloned voice has a consent record; seen as refused unauthenticated requests and a consent record per new voice. |
| Q2 | Roles? | Recommended option, confirmed: users only, no admin. |
| Q3 | Ownership of voices and generations? | Recommended option, confirmed: each user only their own; Google voices shared. |
| Q4 | Existing ownerless data? | Recommended option, confirmed: shown to no one. |
| Q5 | Email verification? | Recommended option, confirmed: none; account works at once. |
| Q6 | Password rule, email case, duplicate email? | Recommended option, confirmed: server enforces UI rule; case-insensitive; "account already exists". |
| Q7 | Login lifetime, refresh, logout? | Recommended option, confirmed: 24 hours; no refresh token; logout ends the login on the server. |
| Q8 | Limit failed logins? | Recommended option, confirmed: no lockout for now. User asked whether lockout needs an admin; answered that only a permanent lock does. |
| Q9 | Login only with local PostgreSQL? | User: "we should use file based storage if postgres is not available, it fine to loose the data if it restarts". |
| Q10 | Consent wording? | Recommended option, confirmed: "I own this voice or have the speaker's informed permission to clone it", version 1. |
| Q11 | Consent per voice or per account? | Recommended option, confirmed: per voice. |
| Q12 | Server enforcement of consent? | Recommended option, confirmed: reject uploads without consent; cloning refuses voices without a consent record. |
| Q13 | Withdrawing consent? | Recommended option, confirmed: by deleting the voice; no separate action. |
| Q14 | Retention of accounts and consent records? | User (Q9 answer): kept until a restart. |
| Q15 | Endpoints open without a token? | Recommended option, confirmed: `/health` and `/inference/backends`. |
| Q16 | Sample fetch only for the owner? | Recommended option, confirmed: yes. |
| Q17 | Account store unavailable? | Recommended option, confirmed: refuse the request. |
| Q18 | Concurrency of sign-up? | Recommended option, confirmed: exactly one account for simultaneous same-email sign-ups. |
| Q19 | May existing auth tests change? | Recommended option, confirmed: yes. |
| Q20 | Scale, latency, observability? | Recommended option, confirmed: not required. |
| Q21 | Status of `voice_narration_PDD_requirements.md`? | Recommended option, confirmed: context only. |
| Q22 | Is deploying to Cloud Run in scope? | User: "dont worry about these ..lets keep it focused on login and consent only" — out of scope. |
| Q23 | What data loss on restart is acceptable? | User (Q9 answer), then confirmed: accounts, logins and consent records may be lost on restart. |
| Q24 | Number of instances? | Recommended option, confirmed: one instance of each service, locally. |
| Q25 | When to use PostgreSQL vs files? | Confirmed: PostgreSQL when available, files otherwise; detection left to Plan. |
| Q26 | (Raised as AUM2-Q3 while planning AUM-2.) Must passwords and login tokens never be stored in readable form? | Recommended option, confirmed 2026-11-16: yes. |

## Provenance Check

- Every item above carries a source label: checked Goal, Relationship, Business Context (7), Repository-Confirmed Facts (13), AR-1–AR-19, AS-1–AS-14, Operational Characteristics (7 rows), AX-1–AX-5, Non-Blocking (1), AAC-1–AAC-19 (each traces to its AR).
- `Derived` items, each with its confirming `Qn`: Business Context Problem/Outcome (Q1), Actors (Q2), What a user may do (Q3), Identity and Password rules (Q6), Consent rule (Q11); AR-1 (Q5), AR-2 (Q6), AR-3 (Q6, Q18), AR-4 (Q8), AR-5 and AR-6 (Q7), AR-8 (Q15), AR-9 (Q3), AR-10 (Q4), AR-11 (Q16), AR-12 (Q17), AR-13 and AR-14 (Q10, Q11), AR-15 and AR-16 (Q12), AR-17 (Q13); Deployment row (Q24), Consistency row (Q18), Dependency row (Q17); Scale, Availability and Observability rows (Q20); AX-3 (Q2), AX-4 (Q5), AX-5 (Q7); AR-19 (Q26); Relationship (Q21).
- `Left to` items: detection of PostgreSQL availability and file location (Plan).
- `Repo` citations verified against the current repository (commit f3372ce) during this capture: api-config.ts:8; authClient.ts:23, :28, :33, :39, :47; Signup.tsx:40, :88; AuthContext.tsx:121, :126; ttsApi.ts:50; start-all.bat:39-41; auth/application.py:28, :34, :39, :44; consent/application.py:98, :105; auth/accounts.py:57; simple_voices/application.py:94, :133, :184; simple_voices/store.py:13; inference/application.py:110, :285; inference/chatterbox.py:146; VoiceManagement.tsx:128, :140; the three auth test paths; absence of docs/requirements.md.
- Requirements without an acceptance criterion: none (AR-n maps to AAC-n for n = 1–19).
- Scenarios without an acceptance criterion: none (AS-1–AS-14 each list theirs).
- Statements that contradict each other: none found. AR-17 (deleting a voice deletes its sample) and the retention row (consent records kept until restart) are consistent: the consent record outlives the voice until a restart. The approved chatterbox-original-app CON-1 ("only Chatterbox runs on GCP") is not relied on here and is not contradicted, since deploying is excluded (AX-1, AX-2).
- Answers taken from a recommended option, each with its confirming `Qn`: Q1–Q8, Q10–Q13, Q15–Q21, Q24, confirmed by the user's "yes" to the consolidated list; Q26, confirmed by the user's "yes" on 2026-11-16.
- No statement about this artifact as a whole is made beyond the checks listed here.
