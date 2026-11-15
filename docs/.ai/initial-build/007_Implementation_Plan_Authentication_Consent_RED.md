# Implementation Plan — Authentication & Consent RED

## Milestone and authority

Milestone 6 of initial-build, RED. This artifact proposes tests only and does not authorize execution or the following GREEN.

Draft completed 2026-10-25, America/Chicago.

## Authoritative References

Paths are repository relative. Requirements and contract are approved by avinash2196 (requirements 2026-10-19, retained P0/Q5–Q10 2026-10-24; contract 2026-10-24). Plan.md is approved 2026-10-24 and records milestone 6 Pending, CONTRACT and milestones 2–5 Complete. Its current execution evidence supersedes historical Current State prose.

Read: requirements.md; Plan.md; contract/API-Contract.md; approved Implementation Plans 001_Implementation_Plan_Foundation.md, 002_Implementation_Plan_Model_Feasibility.md, 003_Implementation_Plan_Persistence_RED.md, 004_Implementation_Plan_Persistence_RED_Recovery.md, 005_Implementation_Plan_Persistence_GREEN.md, 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md; tests/test_persistence.py; voice_narration/_sql.py; voice_narration/auth/persistence.py; voice_narration/consent/persistence.py; requirements-dev.txt. The previous plans are approved inputs, including stopped 003/005 history and the successful 004/006 recovery dispositions. No product-level docs/requirements.md exists.

Process references read under C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0: commands/create-implementation-plan.md, agents/planner.md, skills/implementation-planning/SKILL.md, skills/prompt-driven-development/SKILL.md, skills/testing/SKILL.md, skills/security/SKILL.md, skills/python-fastapi/SKILL.md. They are process guidance, not product authority.

## Current state, predecessors and carried-forward decisions

006 Human Review and Plan execution evidence record two actual 33/33 passes (36.31s, 29.52s), exact eighteen 005 production files, exact 004 tests and nine foundation files preserved. Fixture-owned resources were absent and owned Docker processes stopped. This is predecessor evidence, not a new run.

Auth currently has GrantRepository only. Its save_grant trusts already-resolved Administrator eligibility (005 Proposed Changes item 4). ConsentRepository accepts trusted generic records; it is not an authenticated consent-recording API, email verification system or identity issuer. No auth/application.py or consent/application.py exists. Missing those intended production symbols is valid RED; no scaffolding is needed. Existing 33 tests remain passing regressions, never new RED evidence.

Carry 001's Python3.13.17, FastAPI0.162.0, Uvicorn0.54.0, pytest9.1.1, HTTPX0.28.1, PostgreSQL18.6, Psycopg3.3.6 and unique loopback/temp-root isolation; 004's command-only -p no:anyio and diagnostic helper; 005's owner-separated credentials, canonical UUIDs, exact roles and live grants; 006's bounded Docker observation and host-context contingency. No dependency/version/configuration changes. Existing unrelated uncommitted documentation/package/test work is preserved.

## Files and ordered proposed changes

Create only tests/test_authentication_consent.py, complete content below. Modify/delete no executable file. PDD post-verification bookkeeping in Plan.md and this artifact is outside this file limit.

1. Import the delivered postgres/stores fixtures without editing them. Create test-local HTTP fixtures using stdlib sockets/threads, existing Uvicorn/HTTPX, the same isolated owner stores and a controlled UTC clock.
2. Drive missing Auth registration, verification delivery/consumption, normalized lookup, unchanged duplicate account, password preservation, expiry and separately bootstrapped Administrator through real HTTP.
3. Drive missing Consent recording/read boundary using real issued bearer identities and existing live GrantRepository. Assert immutable legal provenance, explicit assisted authority, ownership, canonical identifiers and authorization before validation.
4. Drive the Consent active-owner validation application boundary before any consumer can receive approval to use/persist samples. This is a consent gate, not upload, enrollment or generation implementation. Auth token verification is the authenticated-generation prerequisite; no jobs endpoint or successful synthesis is invented here.

## Interface choices submitted for review

Missing production symbols referenced by tests are voice_narration.auth.application.create_app and voice_narration.consent.application.create_app. Auth factory keyword arguments: database, root, auth_settings, clock, send_verification, administrator. Consent factory: repository, authenticate, clock. Both return ASGI applications. Auth app exposes state.effective_target() reporting actual database/user/host/port/root, state.effective_auth_settings() reporting the effective auth subsection, state.close() closing its own connections, and state.verify_token(token) returning the actual currently authenticated Account or raising an exception with code UNAUTHENTICATED. Consent app exposes state.validate_owner_consent(account, consent_id) returning active Consent or raising an exception with the applicable contract code. These are internal authoring interfaces proposed here, not new public endpoints. No implementation of them is applied by RED.

administrator is a test-local already-resolved bootstrap credential mapping (email/password/name), standing for the contract's Externally settable configuration paragraph: VOICE_NARRATION_ADMIN_EMAIL plus VOICE_NARRATION_ADMIN_CREDENTIAL_SECRET_REF provisions a verified Administrator separately. This adapter seam does not test environment loading or secret resolution and is never accepted by public registration. send_verification(email, token) captures actual generated credentials at the delivery adapter, not a mock returning the expected identity. authenticate calls the real Auth verification boundary. Only tests supply controlled clock/auth subsection values. They are explicit constructor inputs, not product defaults or alternative environment configuration names. Consent repository and grant callback are actual predecessor implementations. Neither app receives another owner's SQL credentials. New Auth tables must coexist with existing Auth grants without deleting them; future GREEN chooses the smallest compatible migration.

## Proposed exact code

### tests/test_authentication_consent.py

```python
"""Authentication and consent boundaries, synthetic identities, real HTTP and SQL."""
from contextlib import contextmanager
from datetime import timedelta
import importlib
import socket
import threading
import time

import httpx
import pytest
import uvicorn

from test_persistence import NOW, principal, postgres, stores, uid


AUTH = {"access_token_seconds": 120, "verification_token_seconds": 300,
        "signed_link_seconds": 60, "password_min_characters": 8,
        "password_max_characters": 80}
PASSWORD = "  Synthetic password  "
ADMIN_PASSWORD = "Synthetic administrator password"


def timestamp(value):
    return value.isoformat().replace("+00:00", "Z")


def error(response, status, code):
    assert response.status_code == status, response.text
    body = response.json()
    assert set(body) == {"error"}
    assert set(body["error"]) == {"code", "message", "details", "request_id", "timestamp"}
    assert body["error"]["code"] == code
    assert isinstance(body["error"]["message"], str) and body["error"]["message"].strip()
    assert isinstance(body["error"]["details"], list)
    from voice_narration._sql import identity
    identity(body["error"]["request_id"])
    assert body["error"]["timestamp"].endswith("Z")


@contextmanager
def serve(app):
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen(128)
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", lifespan="off"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started, "ASGI server did not start"
        with httpx.Client(base_url=f"http://127.0.0.1:{sock.getsockname()[1]}/api/v1",
                          timeout=10, trust_env=False) as client:
            yield client
    finally:
        server.should_exit = True
        thread.join(10)
        sock.close()
        assert not thread.is_alive(), "HTTP server teardown incomplete"


@pytest.fixture
def system(stores):
    open_store, paths, targets = stores
    grants = open_store("auth")
    consent = open_store("consent", grants.authorize)
    auth_factory = importlib.import_module("voice_narration.auth.application").create_app
    consent_factory = importlib.import_module("voice_narration.consent.application").create_app
    now = [NOW]
    deliveries = []
    administrator = {"email": "admin@example.invalid", "password": ADMIN_PASSWORD,
                     "name": "Synthetic administrator"}
    auth = auth_factory(database=targets["auth"], root=paths["auth"],
                        auth_settings=dict(AUTH), clock=lambda: now[0],
                        send_verification=lambda email, token: deliveries.append((email, token)),
                        administrator=administrator)
    assert auth.state.effective_target() == grants.effective_target()
    assert auth.state.effective_auth_settings() == AUTH
    app = consent_factory(repository=consent, authenticate=auth.state.verify_token,
                          clock=lambda: now[0])
    try:
        with serve(auth) as accounts, serve(app) as consents:
            yield {"auth": accounts, "consent": consents, "now": now,
                   "deliveries": deliveries, "grants": grants, "app": app,
                   "auth_app": auth}
    finally:
        auth.state.close()


def register(system, email="owner@example.invalid", name="Synthetic owner"):
    response = system["auth"].post("/auth/register", json={
        "email": email, "password": PASSWORD, "name": name})
    assert response.status_code == 202, response.text
    assert response.json() == {"verification_required": True}
    canonical = email.strip().lower()
    tokens = [token for address, token in system["deliveries"] if address == canonical]
    assert tokens and isinstance(tokens[-1], str) and tokens[-1].strip()
    return tokens[-1]


def verify(system, email="owner@example.invalid"):
    credential = register(system, email)
    response = system["auth"].post("/auth/verify-email", json={"token": credential})
    assert response.status_code == 200, response.text
    token = response.json()
    assert set(token) == {"access_token", "token_type", "expires_at", "account"}
    assert token["token_type"] == "Bearer"
    assert token["expires_at"] == timestamp(system["now"][0] + timedelta(seconds=120))
    account = token["account"]
    assert set(account) == {"user_id", "email", "name", "role", "email_verified", "created_at"}
    from voice_narration._sql import identity
    identity(account["user_id"])
    assert account["email"] == email.strip().lower()
    assert account["role"] == "User" and account["email_verified"] is True
    assert account["created_at"] == timestamp(system["now"][0])
    return token, credential


def headers(token):
    return {"Authorization": "Bearer " + token["access_token"]}


def consent_body(**changes):
    body = {"consenting_identity": "Synthetic voice owner", "text": "I authorize this voice.\nमैं सहमत हूँ।",
            "version": "synthetic-legal-v1", "assisted": False}
    body.update(changes)
    return body


def record(system, token, **changes):
    response = system["consent"].post("/consent/record", headers=headers(token),
                                      json=consent_body(**changes))
    assert response.status_code == 201, response.text
    result = response.json()
    assert set(result) == {"consent_id", "owner_id", "consenting_identity", "text", "version",
                           "assisted", "authorization", "status", "created_at", "revoked_at"}
    assert result["owner_id"] == token["account"]["user_id"]
    assert result["status"] == "active" and result["revoked_at"] is None
    assert result["created_at"] == timestamp(system["now"][0])
    for field, value in consent_body(**changes).items():
        assert result[field] == value
    assert result["authorization"] == changes.get("authorization")
    return result


def test_registration_verification_login_and_duplicate_identity(system):
    credential = register(system, "  OWNER@Example.invalid  ")
    error(system["auth"].post("/auth/login", json={"email": "owner@example.invalid",
          "password": PASSWORD}), 403, "EMAIL_UNVERIFIED")
    verified = system["auth"].post("/auth/verify-email", json={"token": credential})
    assert verified.status_code == 200
    token = verified.json()
    assert token["account"]["email"] == "owner@example.invalid"
    assert token["account"]["role"] == "User"
    assert system["auth"].get("/auth/me", headers=headers(token)).json() == token["account"]
    duplicate = system["auth"].post("/auth/register", json={"email": "OWNER@example.invalid",
                "password": "different password", "name": "Replacement"})
    assert duplicate.status_code == 202 and duplicate.json() == {"verification_required": True}
    login = system["auth"].post("/auth/login", json={"email": " OWNER@EXAMPLE.INVALID ", "password": PASSWORD})
    assert login.status_code == 200 and login.json()["account"] == token["account"]
    error(system["auth"].post("/auth/login", json={"email": "owner@example.invalid",
          "password": PASSWORD.strip()}), 401, "INVALID_CREDENTIALS")
    error(system["auth"].post("/auth/verify-email", json={"token": credential}), 409, "TOKEN_CONSUMED")


def test_configured_token_boundaries_and_authenticated_principal(system):
    token, credential = verify(system)
    assert system["auth_app"].state.verify_token(token["access_token"]) == token["account"]
    assert system["auth"].get("/auth/me", headers=headers(token)).status_code == 200
    system["now"][0] = NOW + timedelta(seconds=119)
    assert system["auth"].get("/auth/me", headers=headers(token)).status_code == 200
    system["now"][0] = NOW + timedelta(seconds=120)
    error(system["auth"].get("/auth/me", headers=headers(token)), 401, "UNAUTHENTICATED")
    with pytest.raises(Exception) as caught:
        system["auth_app"].state.verify_token(token["access_token"])
    assert caught.value.code == "UNAUTHENTICATED"
    error(system["auth"].get("/auth/me"), 401, "UNAUTHENTICATED")
    error(system["auth"].get("/auth/me", headers={"Authorization": "Bearer unknown"}), 401, "UNAUTHENTICATED")
    system["now"][0] = NOW + timedelta(seconds=300)
    error(system["auth"].post("/auth/verify-email", json={"token": credential}), 400, "INVALID_TOKEN")
    pending = register(system, "pending@example.invalid")
    system["now"][0] += timedelta(seconds=300)
    error(system["auth"].post("/auth/verify-email", json={"token": pending}), 400, "INVALID_TOKEN")
    error(system["auth"].post("/auth/verify-email", json={"token": "unknown"}), 400, "INVALID_TOKEN")


@pytest.mark.parametrize("change", [
    {"role": "Administrator"}, {"email": "two@@example.invalid"}, {"email": "a b@example.invalid"},
    {"email": "@example.invalid"}, {"email": "a@"}, {"name": " "}, {"password": "short"},
    {"password": "x" * 81}, {"email": None}, {"name": 7}, {"unknown": True},
])
def test_registration_closed_validation_after_working_positive(system, change):
    token, unused = verify(system)
    assert token["account"]["role"] == "User"
    body = {"email": "new@example.invalid", "password": PASSWORD, "name": "New synthetic user"}
    body.update(change)
    error(system["auth"].post("/auth/register", json=body), 400, "INVALID_INPUT")


def test_separate_administrator_and_user_roles(system):
    user, unused = verify(system)
    login = system["auth"].post("/auth/login", json={"email": "admin@example.invalid", "password": ADMIN_PASSWORD})
    assert login.status_code == 200, login.text
    admin = login.json()
    assert admin["account"]["role"] == "Administrator" and admin["account"]["email_verified"] is True
    assert system["auth_app"].state.verify_token(admin["access_token"]) == admin["account"]
    assert user["account"]["user_id"] != admin["account"]["user_id"]
    legal = record(system, user)
    error(system["consent"].get("/consent/" + legal["consent_id"], headers=headers(admin),
          params={"owner_id": user["account"]["user_id"]}), 403, "FORBIDDEN")


def test_consent_immutable_legal_provenance_and_owner_gate(system):
    owner, unused = verify(system)
    other, unused = verify(system, "other@example.invalid")
    first = record(system, owner)
    second = record(system, owner, version="synthetic-legal-v2", text="New distinct consent")
    assert second["consent_id"] != first["consent_id"]
    path = "/consent/" + first["consent_id"]
    assert system["consent"].get(path, headers=headers(owner)).json() == first
    active = system["app"].state.validate_owner_consent(owner["account"], first["consent_id"])
    assert active == first
    error(system["consent"].get(path, headers=headers(other)), 403, "FORBIDDEN")
    error(system["consent"].get(path), 401, "UNAUTHENTICATED")
    error(system["consent"].post("/consent/record", json=consent_body()), 401, "UNAUTHENTICATED")
    for consent_id, account, code in [(first["consent_id"], other["account"], "FORBIDDEN"),
                                      (uid(), owner["account"], "NOT_FOUND")]:
        with pytest.raises(Exception) as caught:
            system["app"].state.validate_owner_consent(account, consent_id)
        assert caught.value.code == code
    assert system["consent"].get(path, headers=headers(owner)).json() == first


@pytest.mark.parametrize("change", [
    {"assisted": True}, {"assisted": False, "authorization": "Not applicable"},
    {"assisted": True, "authorization": " "}, {"text": None}, {"version": " "},
    {"consenting_identity": " "}, {"assisted": "false"}, {"owner_id": "forged"},
])
def test_explicit_assisted_authority_and_closed_consent_validation(system, change):
    owner, unused = verify(system)
    positive = record(system, owner, assisted=True, authorization="Owner explicitly authorized assisted recording.")
    assert positive["authorization"] == "Owner explicitly authorized assisted recording."
    error(system["consent"].post("/consent/record", headers=headers(owner),
          json=consent_body(**change)), 400, "INVALID_INPUT")


def test_live_scoped_grant_on_new_consent_boundary(system):
    owner, unused = verify(system)
    response = system["auth"].post("/auth/login", json={"email": "admin@example.invalid", "password": ADMIN_PASSWORD})
    assert response.status_code == 200
    admin = response.json()
    legal = record(system, owner)
    user_id = owner["account"]["user_id"]
    grant_id = uid()
    system["grants"].save_grant(principal(user_id), {"grant_id": grant_id, "owner_id": user_id,
        "administrator_id": admin["account"]["user_id"], "scopes": ["consents:read"],
        "created_at": NOW, "expires_at": NOW + timedelta(seconds=60), "revoked_at": None}, now=NOW)
    path = "/consent/" + legal["consent_id"]
    query = {"owner_id": user_id}
    assert system["consent"].get(path, headers=headers(admin), params=query).json() == legal
    system["grants"].revoke_grant(principal(user_id), grant_id, now=NOW)
    error(system["consent"].get(path, headers=headers(admin), params=query), 403, "FORBIDDEN")
    assert system["consent"].get(path, headers=headers(owner)).json() == legal
    system["grants"].save_grant(principal(user_id), {"grant_id": uid(), "owner_id": user_id,
        "administrator_id": admin["account"]["user_id"], "scopes": ["profiles:read"],
        "created_at": NOW, "expires_at": NOW + timedelta(seconds=60), "revoked_at": None}, now=NOW)
    error(system["consent"].get(path, headers=headers(admin), params=query), 403, "FORBIDDEN")
    system["grants"].save_grant(principal(user_id), {"grant_id": uid(), "owner_id": user_id,
        "administrator_id": admin["account"]["user_id"], "scopes": ["consents:read"],
        "created_at": NOW, "expires_at": NOW + timedelta(seconds=60), "revoked_at": None}, now=NOW)
    assert system["consent"].get(path, headers=headers(admin), params=query).json() == legal
    system["now"][0] = NOW + timedelta(seconds=60)
    error(system["consent"].get(path, headers=headers(admin), params=query), 403, "FORBIDDEN")
```

## Requirement and contract coverage

| Owned requirement / normative rule | New evidence |
| --- | --- |
| R-ACCT-001; FR-001 registration and verified identities | test_registration_verification_login_and_duplicate_identity: open registration, captured delivered credential, unverified login denial, consume-once verification, normalized lookup, duplicate response and unchanged original identity/password; test_configured_token_boundaries_and_authenticated_principal: actual Token/Account shape and configured access/verification expiry boundaries. |
| User/Administrator roles and authenticated-generation prerequisite | test_separate_administrator_and_user_roles: separate verified Administrator bootstrap, User public creation and distinct canonical principal; registration validation rejects public role field. Token boundary checks actual verify_token positive then expired failure. Generation submission itself belongs to the later Jobs milestone; this milestone supplies identity verification, without asserting a fake successful job. |
| Closed account inputs, configured password bounds | test_registration_closed_validation_after_working_positive: eleven cases, each after successful verification. Required text/type/email/unknown fields, preserved password spaces and role elevation covered. |
| R-CONS-001; FR-002; AC-CONS-001 immutable identity/account/time/text/version | test_consent_immutable_legal_provenance_and_owner_gate: actual Consent field set, exact multilingual/legal text and explicit version, issuing canonical account, controlled creation time, new version creates a distinct event and original remains unchanged. Owner read and gate succeed before foreign/unknown/anonymous denials. |
| R-CONS-002 assisted recording explicit authority | test_explicit_assisted_authority_and_closed_consent_validation: eight cases, each first recording explicit assisted authorization successfully, then rejecting absent/blank/inapplicable authority or invalid immutable inputs. |
| Authorized administrative consent queries using live owner grants | test_live_scoped_grant_on_new_consent_boundary: positive private Consent read, then live revoked/wrong-scope/expired grant denial. It verifies the missing consent HTTP authorization adapter, not a duplicate RED claim for already-delivered GrantRepository. |

Contract rules not tested here, with ownership reason: grant create/list/revoke public routes, grant target lookup and collection cursors are not asserted by these tests; scoped persistence already belongs to milestone 5, and public cross-service grant/consumer coverage remains Security & Nine-Service Integration. Consent DELETE/cleanup, revocation and retention mechanics remain existing 33 regression tests and later cross-service propagation. Profile.consent_id association, active-consent-before-upload bytes and unauthorized stream disposal require Artifact/Voices boundaries owned by Voice Enrollment; this milestone tests the actual owner-consent authorization gate those consumers will call. Jobs idempotency, scheduling, output, limits and authenticated submission remain later Jobs evidence. Internal HTTP service identity/deadline/context, events/outbox/Audit propagation, deployed transport/secrets, paging and whole Configuration loading belong to later integration/production prerequisites. No claim of full API contract coverage is made. Common real-transport error envelope/status checks are exercised on the auth and consent routes in this file; exhaustive malformed wire parsing is not independently claimed.

All new tests exercise missing Auth/Consent behavior. No newly added test is predicted to pass on the current repository. Negative checks follow an actual successful identity or consent operation in the same test. Existing regression cases remain expected to pass and are never counted as missing milestone 6 behavior.

## Acceptance / Completion Criteria

After separate human approval, apply only the one complete test file. Preserve the exact existing 33 cases, eighteen production files, dependencies and nine foundation files. Collect exactly 24 new cases (five ordinary cases, eleven registration validation cases, eight consent validation cases). Two new-suite invocations without manual state cleanup must fail exclusively at the intentionally absent Auth/Consent application module/symbol boundary after the delivered real PostgreSQL isolation checks succeed. A missing fixture import, syntax error, dependency failure, Docker error, startup/thread failure or failed teardown is not RED and stops execution. Unexpected passing new tests stop for traceability review. Run the unchanged 33-case persistence suite twice, all pass with no errors/skips/xfails. Both repeated suites must clean their own random resources. Record real commands, outputs, exit codes, timing, project IDs, contingency use and cleanup before marking milestone 6 complete. Do not fix production or continue into GREEN.

## Verification commands and expected evidence

Run from the repository root only after approval. First perform 006's exact eighteen-file/004-test comparison and foundation preservation checks; repeat them after verification. Use the unchanged project interpreter and prerequisite version/plugin metadata checks from 005/006; no additional pytest plugin is permitted. Apply the exact block to tests/test_authentication_consent.py and compare its complete content to this artifact before running.

```powershell
git status --short
git diff --check
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_authentication_consent.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_authentication_consent.py -ra --tb=short
```

Execute each command separately and inspect its output. Second regression run requires first regression run passing. Second RED invocation requires the first showing exactly the intended missing production boundary and successful teardown; there is no retry-until-pass loop or manual cleanup between paired runs. Expected / Predicted — Not Yet Verified: both regression runs 33/33 pass, both new runs 24 setup failures at intended missing auth.application, successful isolation/teardown, zero executable drift outside the new test. Later missing consent.application after Auth is implemented is the second intended capability boundary, not evidence observed during this RED. The missing-module condition alone does not prove eventual tests pass after GREEN; that requires actual future execution.

Docker readiness during approved execution carries 006 verbatim in substance: separately run docker context show, docker version, docker compose version and docker info --format '{{.ServerVersion}}'; require desktop-linux, client/server29.3.1 and Compose5.6.0. If stopped/missing pipe, launch the installed runtime once with the following command, then poll the same diagnostics at intervals no longer than15 seconds, each diagnostic bounded15 seconds, within one total300-second observation window including any host handoff. Terminate/reap exact timed-out diagnostic processes; waits no longer than60 seconds and user updates at least each60 seconds. Startup not-ready observations are prerequisite readiness, not RED failures or an artificial first-probe gate. Do not install/change settings or loop restarts.

```powershell
Start-Process -FilePath 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -WindowStyle Hidden
```

No runtime or Docker command is executed during this planning task.

## Pre-authorized Contingencies

Exact trigger: sandbox Desktop launch fails to persist, or diagnostics explicitly deny access to dockerDesktopLinuxEngine. Files: none. Exact change: run the identical hidden launch only if the first did not persist, identical diagnostics and the exact four pytest commands above in the existing approved host execution facility with the same cwd/environment and original total300-second readiness deadline. Record trigger and use/nonuse. This changes execution context only, never tests/configuration/settings or automatic approval review. Rejection or unresolved readiness stops execution with actual reason.

## Cleanup, recovery and risks

The imported fixtures retain exact random-project Compose down --volumes --remove-orphans and owner database/role cleanup. The new serve fixture exits/join-checks both local Uvicorn threads and closes sockets; Auth closes its own connections before existing stores teardown. Record every actual project ID; verify no exact-project containers/networks/volumes remain. Stop only Desktop started by this execution with docker desktop stop; bound/reap diagnostics, record docker desktop status and Get-Process -Name 'Docker Desktop','com.docker.backend','com.docker.build' -ErrorAction SilentlyContinue | Select-Object ProcessName,Id. No global prune, reset or unrelated cleanup. Recovery reverses only the new test file after confirming no intervening edits; retain historical evidence and unrelated work.

Identity comparisons: email lookup trim/lowercase only; issued user_id, consent owner_id and grant owner/administrator IDs use identical canonical lowercase UUIDs from Auth; exact User/Administrator enum role, exact consents:read scope, exact consent ID and exact owner membership. No authorization compares email/name or applies case folding to UUIDs/roles. Legal identity/text/version are preserved UTF-8 values, not authorization identifiers. Bearer verification precedes private lookup; the tests assert anonymous access cannot inspect/record consent. Controlled clocks and effective auth subsection checks prevent host clock/defaults from silently determining expiry. Synthetic .invalid emails and nonproduction credentials are fixture data; never dump delivery credentials/SQL passwords in evidence. The local callback seam proves domain identity/authorization, not deployed inter-service authentication. Every generic PersistenceError.code asserted is approved contract behavior, not HTTP leakage of arbitrary exceptions.

## Planning-time dry run and exact-code review

No runtime dry run or scratch behavioral probe is performed: this planning task explicitly prohibits Docker/test/runtime startup. Static syntax/fixture/parameterization checks are allowed and recorded below; they do not establish behavioral soundness or future GREEN success. No new baseline runtime failure has been established and none is waived. Missing intended production modules are established by file inspection. A scratch implementation sufficient to pass these HTTP/SQL tests would implement the new capability; none is installed or represented as verified.

Per-file review: tests/test_authentication_consent.py has complete final content, no pseudocode/placeholder/omitted section, matches all four Proposed Changes, uses only approved stdlib/pytest/HTTPX/Uvicorn plus delivered fixtures and repositories. The sole new constructor inputs, state methods, auth subsection values, socket/thread bounds and no-proxy client choice trace to Interface choices and test-local isolation above. No dependency/plugin/build/runtime setting is introduced. No new normative requirement, decision, criterion or contingency identifier reuses an approved identifier. No template comments remain.

Actual static check, 2026-10-25, planning only (no created scratch files):

```powershell
@'
import ast
from pathlib import Path
s=Path('docs/.ai/initial-build/007_Implementation_Plan_Authentication_Consent_RED.md').read_text(encoding='utf-8')
code=s.split('```python\n',1)[1].split('```',1)[0]
t=ast.parse(code, filename='tests/test_authentication_consent.py')
count=0
for n in t.body:
    if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'):
        cases=1
        for d in n.decorator_list:
            if isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and d.func.attr=='parametrize':
                assert isinstance(d.args[1], ast.List)
                cases=len(d.args[1].elts)
        count += cases
        print(n.name, cases)
assert count==24, count
assert not any(isinstance(n,ast.Constant) and n.value is Ellipsis for n in ast.walk(t))
assert (chr(60) + '!' + '--') not in s
for name in ['auth','consent']:
    assert not Path('voice_narration',name,'application.py').exists()
assert not Path('tests/test_authentication_consent.py').exists()
print('PASS: syntax, 24 proposed cases, no ellipsis/template comment, intended modules absent, test file unapplied')
'@ | .\.venv\Scripts\python.exe -B -
```

Exit0; actual trimmed output:

```text
test_registration_verification_login_and_duplicate_identity 1
test_configured_token_boundaries_and_authenticated_principal 1
test_registration_closed_validation_after_working_positive 11
test_separate_administrator_and_user_roles 1
test_consent_immutable_legal_provenance_and_owner_gate 1
test_explicit_assisted_authority_and_closed_consent_validation 8
test_live_scoped_grant_on_new_consent_boundary 1
PASS: syntax, 24 proposed cases, no ellipsis/template comment, intended modules absent, test file unapplied
```

The first version of this inspection helper attempted literal_eval on the parameter array's intentional `"x" * 81` expression and failed with ValueError. The helper was corrected to count AST list elements; the proposed tests did not need a change. This was an inspection-helper failure, not a baseline/runtime test failure. `git diff --check` exited0 with existing001/Plan LF-to-CRLF notices only. This static check proves syntax/count/absence, not fixture execution or behavioral success.

## Explicit exclusions

Production code/scaffolding/migrations, executable application files, dependency/configuration/infrastructure changes, email provider selection, paid provisioning, model acquisition, audio/enrollment/jobs implementation, revocation/purge rescheduling, distributed deployment/security conclusions, extra failed-suite retries, commits/push/PRs and any approval by the planner.

## Human Review

Status: Approved by avinash2196 on 2026-10-25 (recorded 2026-10-25T15:41:03Z), in response to review of this exact Authentication & Consent RED plan.

Execution status: Complete — executed and verified unchanged007 on 2026-10-25 from the recorded resume approval (2026-10-25T17:54:43Z). Two unchanged persistence suites passed33/33 (56.75s,56.19s); two new suites collected24 and failed only at intended missing auth.application after real PostgreSQL isolation (38.62s,31.45s), with successful teardown. Exact18 production/004/007 test and nine foundation files preserved. See Plan.md, Authentication & Consent RED007 resume execution evidence, for commands, outputs, project IDs, named-pipe host contingency and cleanup. User-started Docker remains running. No executable edits in this resume, GREEN, commit or push; prior stopped evidence retained.
