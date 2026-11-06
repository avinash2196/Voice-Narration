# Implementation Plan — Authentication & Consent GREEN

## Milestone and authorization

initial-build milestone 7, GREEN. Proposed exact production content for human review only. No execution, approval, commit, deployment or following milestone is authorized by this artifact.

## Authoritative References

Paths are repository relative unless stated otherwise. Read and carried forward:

| Reference | Authority / disposition |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved avinash2196 2026-10-19; retained P0 and Q5–Q10 clarifications 2026-10-24. |
| docs/.ai/initial-build/Plan.md | Approved avinash2196 2026-10-24. Current execution evidence records milestone 6 Complete and milestone 7 Pending. Historical original-state prose is not current implementation evidence. |
| docs/.ai/initial-build/contract/API-Contract.md | Human approved 2026-10-24; CONTRACT Complete. Account, Consent, normalization, common errors and live grant rules are authoritative. |
| 001_Implementation_Plan_Foundation.md | Approved/executed; pinned tooling, nine foundation files and real isolated PostgreSQL harness. |
| 002_Implementation_Plan_Model_Feasibility.md | Approved/executed assessment; no production model or commercial enablement inferred. |
| 003_Implementation_Plan_Persistence_RED.md | Approved stopped history; interfaces carried forward, environment failure is not RED evidence. |
| 004_Implementation_Plan_Persistence_RED_Recovery.md; 004-red-run2.txt | Approved/executed recovery, exact 33-case tests and command-only anyio exclusion. |
| 005_Implementation_Plan_Persistence_GREEN.md | Approved exact eighteen production files, preserved without modification. |
| 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved/executed verification recovery; owner isolation and bounded diagnostic protocol carried forward. |
| 007_Implementation_Plan_Authentication_Consent_RED.md | Approved/executed RED; constructor seams, configured test inputs and exact 24 cases are binding inputs. |
| voice_narration_PDD_requirements.md | Retained non-conflicting P0 context. |
| tests/test_authentication_consent.py; tests/test_persistence.py; voice_narration/_sql.py; voice_narration/auth/persistence.py; voice_narration/consent/persistence.py; requirements-dev.txt; pytest.ini; compose.harness.yaml | Inspected delivered repository facts, not additional product authority. |
| Installed plugin commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/security/SKILL.md; skills/python-fastapi/SKILL.md; skills/testing/SKILL.md | Applied process/domain guidance under C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0. |

No product-level docs/requirements.md or workspace AGENTS.md exists. This artifact introduces no new normative requirement identifiers or labels that redefine approved ones.

## Current state and predecessor evidence

Plan.md Authentication & Consent RED 007 resume evidence records two 33/33 regression passes (56.75s, 56.19s), then two 24-case runs with only the intentionally absent voice_narration.auth.application import (38.62s, 31.45s). Real isolated PostgreSQL setup and teardown succeeded; no unexpected errors, skips or xfails. Consent application absence is established by static file inspection, not a claimed observed second import failure. The exact 007 test, 004 test, eighteen 005 production files and foundation files were preserved by recorded comparisons. These are actual predecessor observations, not tests rerun during planning.

Auth currently owns only GrantRepository. ConsentRepository already persists generic immutable records, owner gates, live grants and fences; its records are not yet the public consent boundary. The two application modules do not exist. Existing work in the shared checkout must be preserved.

## Carried-forward decisions

Keep CPython3.13.17, FastAPI0.162.0, Uvicorn0.54.0, pytest9.1.1, HTTPX0.28.1, Psycopg3.3.6 and PostgreSQL18.6, existing dependency/configuration files, real HTTP fixtures, randomly allocated loopback/project resources, separate owner credentials/roots, canonical lowercase UUIDs and exact roles. No dependency/version/configuration change is proposed. All new imports are approved libraries or Python standard library; password derivation uses stdlib scrypt, opaque tokens use secrets, stored token digests use SHA256. These mechanisms are submitted here for review, not implied product defaults.

007 fixes create_app keyword interfaces and state seams. Auth alone receives Auth database credentials. Consent receives its existing repository plus the real Auth verification callable; no cross-owner SQL, shared privileged facade or arbitrary public actor mapping is added. Administrator credentials are already-resolved explicit bootstrap inputs; environment/secret resolution and service transport belong to later integration. No default administrator or hidden lifetime is introduced.

## Files in scope and ordered proposed changes

Create exactly four production files, with complete final content below:

1. voice_narration/_http.py: shared stateless HTTP parsing/error helpers only; no credentials, data access or service ownership.
2. voice_narration/auth/accounts.py: Auth-local account, verification and access-token storage; additive tables preserve existing grants/schema-version. Serialize shared connection transactions and consume verification/create access credentials atomically.
3. voice_narration/auth/application.py: the approved registration, verification, login, me and trusted token-verification seams; delivery failure returns dependency unavailable.
4. voice_narration/consent/application.py: authenticated public consent creation/read and owner-only active-consent validation using existing persistence gates.

Modify/delete no existing executable file. Execution-only Plan.md status/evidence and this artifact's review disposition are PDD bookkeeping outside that production-file limit. Tests, schema-version primitives and the eighteen existing production files remain exact.

The additive Auth tables are initialized after GrantRepository.initialize on the same Auth-only connection. The existing v1 migration remains unchanged. CREATE TABLE IF NOT EXISTS in one serialized transaction is the narrowly scoped compatible extension, not a reset or replacement. Existing accounts and grants survive reopening; token digests and password salt/derivation are persisted. Consent maps its consent UUID to the generic record id/profile_id/consent_id before any profile exists; this internal grouping key creates no Voice profile and is not a claim of completed profile association. Future enrollment links its real Profile.consent_id to this consent_id. Existing consent-wide fence/purge queries match consent_id in addition to profile_id, so the legal event remains in that consent's cleanup group. No public profile_id is added to Consent and no existing generic record is rewritten. Actual profile association remains owned by the approved later enrollment work.

## Proposed exact code

### voice_narration/_http.py

```python
"""Stateless public HTTP validation and safe contract errors."""
from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from voice_narration._sql import PersistenceError, fail, instant


STATUS = {"INVALID_INPUT": 400, "INVALID_TOKEN": 400,
          "UNAUTHENTICATED": 401, "INVALID_CREDENTIALS": 401,
          "FORBIDDEN": 403, "EMAIL_UNVERIFIED": 403, "NOT_FOUND": 404,
          "TOKEN_CONSUMED": 409, "CONSENT_REVOKED": 409,
          "INVALID_STATE": 409}


def timestamp(value):
    return instant(value).isoformat().replace("+00:00", "Z")


def closed(body, required, optional=()):
    if not isinstance(body, dict) or not set(required) <= set(body):
        fail("INVALID_INPUT")
    if set(body) - set(required) - set(optional):
        fail("INVALID_INPUT")
    return body


def text(value):
    if not isinstance(value, str) or not value.strip():
        fail("INVALID_INPUT")
    return value


async def body(request: Request):
    try:
        return await request.json()
    except (ValueError, UnicodeError):
        raise PersistenceError("INVALID_INPUT") from None


def bearer(request):
    value = request.headers.get("authorization", "")
    parts = value.split()
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        fail("UNAUTHENTICATED")
    return parts[1]


def install_errors(app, clock):
    def response(code):
        return JSONResponse(status_code=STATUS.get(code, 503), content={"error": {
            "code": code, "message": code.replace("_", " ").capitalize(),
            "details": [], "request_id": str(uuid4()), "timestamp": timestamp(clock())}})

    @app.exception_handler(PersistenceError)
    async def persistence_error(request, exc):
        return response(exc.code)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return response("INVALID_INPUT")

    @app.exception_handler(HTTPException)
    async def http_error(request, exc):
        return response("NOT_FOUND" if exc.status_code == 404 else "INVALID_INPUT")

    @app.exception_handler(Exception)
    async def unexpected_error(request, exc):
        return response("INTERNAL_UNAVAILABLE")
```

### voice_narration/auth/accounts.py

```python
"""Auth-owned persistent accounts and opaque credentials, separate from grants."""
from contextlib import contextmanager
from hashlib import scrypt, sha256
import hmac
import secrets
from threading import RLock
from uuid import uuid4

from voice_narration._http import closed, text, timestamp
from voice_narration._sql import PersistenceError, after, duration, fail, instant
from voice_narration.auth.persistence import GrantRepository


def email(value):
    value = text(value).strip().lower()
    if value.count("@") != 1 or any(char.isspace() for char in value):
        fail("INVALID_INPUT")
    local, domain = value.split("@")
    if not local or not domain:
        fail("INVALID_INPUT")
    return value


def digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


def password_hash(password, salt):
    return scrypt(password.encode("utf-8"), salt=salt, n=32768, r=8, p=3,
                  maxmem=67108864, dklen=32)


class Accounts(GrantRepository):
    def __init__(self, *, database, root, settings, clock):
        super().__init__(database=database, root=root)
        self._lock = RLock()
        self.clock = clock
        fields = {"access_token_seconds", "verification_token_seconds", "signed_link_seconds",
                  "password_min_characters", "password_max_characters"}
        if not isinstance(settings, dict) or set(settings) != fields:
            fail("INVALID_CONFIGURATION")
        self.settings = dict(settings)
        for value in self.settings.values():
            duration(value)
        if settings["password_max_characters"] < settings["password_min_characters"]:
            fail("INVALID_CONFIGURATION")

    @contextmanager
    def transaction(self):
        with self._lock:
            with super().transaction() as db:
                yield db

    def initialize(self):
        super().initialize()
        with self.transaction() as db:
            db.execute("CREATE TABLE IF NOT EXISTS auth_accounts (user_id uuid PRIMARY KEY,email text UNIQUE NOT NULL,name text NOT NULL,role text NOT NULL CHECK(role IN ('User','Administrator')),email_verified boolean NOT NULL,created_at timestamptz NOT NULL,password_salt bytea NOT NULL,password_hash bytea NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS auth_verifications (digest text PRIMARY KEY,user_id uuid NOT NULL REFERENCES auth_accounts(user_id),expires_at timestamptz NOT NULL,consumed_at timestamptz)")
            db.execute("CREATE TABLE IF NOT EXISTS auth_tokens (digest text PRIMARY KEY,user_id uuid NOT NULL REFERENCES auth_accounts(user_id),expires_at timestamptz NOT NULL)")

    @staticmethod
    def account(row):
        return {"user_id": str(row[0]), "email": row[1], "name": row[2], "role": row[3],
                "email_verified": row[4], "created_at": timestamp(row[5])}

    def credentials(self, value):
        closed(value, {"email", "password", "name"})
        address, name, password = email(value["email"]), text(value["name"]), text(value["password"])
        if not self.settings["password_min_characters"] <= len(password) <= self.settings["password_max_characters"]:
            fail("INVALID_INPUT")
        return address, name, password

    def bootstrap(self, value):
        address, name, password = self.credentials(value)
        salt = secrets.token_bytes(16)
        derived = password_hash(password, salt)
        with self.transaction() as db:
            existing = db.execute("SELECT role,email_verified FROM auth_accounts WHERE email=%s", (address,)).fetchone()
            if existing is not None:
                if existing != ("Administrator", True):
                    fail("INVALID_CONFIGURATION")
                return
            db.execute("INSERT INTO auth_accounts VALUES (%s,%s,%s,'Administrator',true,%s,%s,%s)",
                       (str(uuid4()), address, name, instant(self.clock()), salt, derived))

    def register(self, value, deliver):
        address, name, password = self.credentials(value)
        salt = secrets.token_bytes(16)
        derived = password_hash(password, salt)
        token = secrets.token_urlsafe(32)
        now = instant(self.clock())
        with self.transaction() as db:
            if db.execute("SELECT 1 FROM auth_accounts WHERE email=%s", (address,)).fetchone():
                return None
            user_id = str(uuid4())
            db.execute("INSERT INTO auth_accounts VALUES (%s,%s,%s,'User',false,%s,%s,%s)",
                       (user_id, address, name, now, salt, derived))
            db.execute("INSERT INTO auth_verifications VALUES (%s,%s,%s,NULL)",
                       (digest(token), user_id, after(now, duration(self.settings["verification_token_seconds"]))))
            try:
                deliver(address, token)
            except Exception:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None

    def issue(self, db, row, now):
        token = secrets.token_urlsafe(32)
        expires = after(now, duration(self.settings["access_token_seconds"]))
        db.execute("INSERT INTO auth_tokens VALUES (%s,%s,%s)", (digest(token), str(row[0]), expires))
        return {"access_token": token, "token_type": "Bearer", "expires_at": timestamp(expires),
                "account": self.account(row)}

    def verify_email(self, value):
        closed(value, {"token"})
        token = text(value["token"])
        now = instant(self.clock())
        with self.transaction() as db:
            credential = db.execute("SELECT user_id,expires_at,consumed_at FROM auth_verifications WHERE digest=%s", (digest(token),)).fetchone()
            if credential is None or credential[1] <= now:
                fail("INVALID_TOKEN")
            if credential[2] is not None:
                fail("TOKEN_CONSUMED")
            db.execute("UPDATE auth_verifications SET consumed_at=%s WHERE digest=%s", (now, digest(token)))
            row = db.execute("UPDATE auth_accounts SET email_verified=true WHERE user_id=%s RETURNING user_id,email,name,role,email_verified,created_at", (credential[0],)).fetchone()
            return self.issue(db, row, now)

    def login(self, value):
        closed(value, {"email", "password"})
        address, password = email(value["email"]), text(value["password"])
        now = instant(self.clock())
        with self.transaction() as db:
            row = db.execute("SELECT user_id,email,name,role,email_verified,created_at,password_salt,password_hash FROM auth_accounts WHERE email=%s", (address,)).fetchone()
            salt = bytes(row[6]) if row is not None else bytes(16)
            derived = password_hash(password, salt)
            expected = bytes(row[7]) if row is not None else bytes(32)
            if not hmac.compare_digest(derived, expected) or row is None:
                fail("INVALID_CREDENTIALS")
            if row[4] is not True:
                fail("EMAIL_UNVERIFIED")
            return self.issue(db, row, now)

    def verify_token(self, token):
        if not isinstance(token, str) or not token.strip():
            fail("UNAUTHENTICATED")
        with self.transaction() as db:
            row = db.execute("SELECT a.user_id,a.email,a.name,a.role,a.email_verified,a.created_at FROM auth_tokens t JOIN auth_accounts a ON a.user_id=t.user_id WHERE t.digest=%s AND t.expires_at>%s AND a.email_verified=true", (digest(token), instant(self.clock()))).fetchone()
            if row is None:
                fail("UNAUTHENTICATED")
            return self.account(row)
```

### voice_narration/auth/application.py

```python
"""Public Auth boundary with explicit owner-local dependencies."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from voice_narration._http import bearer, body, install_errors
from voice_narration._sql import fail
from voice_narration.auth.accounts import Accounts


def create_app(*, database, root, auth_settings, clock, send_verification, administrator):
    if not callable(clock) or not callable(send_verification):
        fail("INVALID_CONFIGURATION")
    accounts = Accounts(database=database, root=root, settings=auth_settings, clock=clock)
    try:
        accounts.initialize()
        accounts.bootstrap(administrator)
    except Exception:
        accounts.close()
        raise
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)
    app.state.effective_target = accounts.effective_target
    app.state.effective_auth_settings = lambda: dict(accounts.settings)
    app.state.verify_token = accounts.verify_token
    app.state.close = accounts.close

    @app.post("/api/v1/auth/register")
    async def register(request: Request):
        value = await body(request)
        await run_in_threadpool(accounts.register, value, send_verification)
        return JSONResponse(status_code=202, content={"verification_required": True})

    @app.post("/api/v1/auth/verify-email")
    async def verify_email(request: Request):
        value = await body(request)
        return await run_in_threadpool(accounts.verify_email, value)

    @app.post("/api/v1/auth/login")
    async def login(request: Request):
        value = await body(request)
        return await run_in_threadpool(accounts.login, value)

    @app.get("/api/v1/auth/me")
    def me(request: Request):
        return accounts.verify_token(bearer(request))

    return app
```

### voice_narration/consent/application.py

```python
"""Consent public boundary; persistence remains owned by ConsentRepository."""
from functools import wraps
from threading import RLock
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from voice_narration._http import bearer, body, closed, install_errors, text, timestamp
from voice_narration._sql import actor, fail, identity, instant


def create_app(*, repository, authenticate, clock):
    if not callable(authenticate) or not callable(clock):
        fail("INVALID_CONFIGURATION")
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)

    lock = RLock()

    def serialized(operation):
        @wraps(operation)
        def invoke(*args, **kwargs):
            with lock:
                return operation(*args, **kwargs)
        return invoke

    def principal(account):
        if not isinstance(account, dict) or account.get("email_verified") is not True:
            fail("UNAUTHENTICATED")
        who = {"user_id": account.get("user_id"), "role": account.get("role")}
        actor(who)
        return who

    def result(record):
        if record["category"] != "consent":
            fail("NOT_FOUND")
        return dict(record["payload"])

    @serialized
    def record_consent(account, value):
        who = principal(account)
        closed(value, {"consenting_identity", "text", "version", "assisted"}, {"authorization"})
        for field in ("consenting_identity", "text", "version"):
            text(value[field])
        if type(value["assisted"]) is not bool:
            fail("INVALID_INPUT")
        if value["assisted"]:
            text(value.get("authorization"))
        elif "authorization" in value:
            fail("INVALID_INPUT")
        consent_id, now = str(uuid4()), instant(clock())
        consent = {"consent_id": consent_id, "owner_id": who["user_id"],
                   "consenting_identity": value["consenting_identity"], "text": value["text"],
                   "version": value["version"], "assisted": value["assisted"],
                   "authorization": value.get("authorization"), "status": "active",
                   "created_at": timestamp(now), "revoked_at": None}
        repository.save({"id": consent_id, "owner_id": who["user_id"],
                         "profile_id": consent_id, "consent_id": consent_id,
                         "category": "consent", "created_at": now, "payload": consent})
        return consent

    @serialized
    def read_consent(account, consent_id, owner_id):
        who = principal(account)
        identity(consent_id)
        now = instant(clock())
        if owner_id is None:
            reader = {"user_id": who["user_id"], "role": "User"}
        else:
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
            identity(owner_id)
            repository.permit(who, owner_id, "consents:read", now)
            reader = who
        record = repository.read(reader, consent_id, now=now)
        if owner_id is not None and record["owner_id"] != owner_id:
            fail("FORBIDDEN")
        return result(record)

    @serialized
    def validate_owner_consent(account, consent_id):
        who = principal(account)
        identity(consent_id)
        # Validation never consumes an administrator's read grant as owner consent.
        reader = {"user_id": who["user_id"], "role": "User"}
        record = repository.read(reader, consent_id, now=instant(clock()))
        consent = result(record)
        if consent["owner_id"] != who["user_id"]:
            fail("FORBIDDEN")
        if consent["status"] != "active":
            fail("CONSENT_REVOKED")
        return consent

    app.state.validate_owner_consent = validate_owner_consent

    @app.post("/api/v1/consent/record")
    async def record(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        consent = await run_in_threadpool(record_consent, account, value)
        return JSONResponse(status_code=201, content=consent)

    @app.get("/api/v1/consent/{consent_id}")
    def read(request: Request, consent_id: str):
        account = authenticate(bearer(request))
        if set(request.query_params) - {"owner_id"}:
            fail("INVALID_INPUT")
        return read_consent(account, consent_id, request.query_params.get("owner_id"))

    return app
```

## Coverage and completion criteria

Expected / Predicted — Not Yet Verified:

- All 24 exact 007 cases pass: registration/delivery/verification/login and duplicate canonical email; eleven closed registration validation variants; explicit separate verified Administrator; configured token validity at119s and rejection at120s, verification rejection at300s and consumption before expiry; immutable multilingual legal provenance, owner validation and forbidden foreign access; eight assisted/closed consent input variants; real live scoped grant creation/revocation/scope/expiry reads.
- All 33 exact 004 persistence regressions pass. The eight owner databases remain separate, nonsuperuser, temporary and effective-target checked; no Auth connection is supplied to Consent.
- All four proposed production files match these complete blocks. All eighteen 005 files, both approved test files and nine foundation files remain exact. No dependency, test, configuration or existing persistence change.
- Persisted passwords are independently salted scrypt values; access/verification tables contain only token digests. Public Account excludes password, salt and token records. Public registration cannot assign a role. Duplicate registration does not mutate the existing account or credentials.
- Consent accepts no client owner/ID/status/timestamp fields; preserves legal strings byte-for-byte after validating nonblank; creates distinct immutable events. Public retrieval and trusted owner validation use repository fences and authorization. A read grant does not authorize owner validation or consent creation as another account.
- Both full verification runs pass in order without manual state cleaning; no skips/xfails/unexpected errors or outside-scope failure waiver. Fixture resources and started HTTP threads are gone; pre-existing user Docker Desktop remains running.

Only actual successful approved execution plus these checks permits milestone 7 completion. A static planning check is not GREEN evidence.

## Verification after human approval

Use the existing cwd and .venv. Before applying, read current Plan status and approval; stop on drift or any approved file already existing with unrelated contents. Use the exact-content comparisons in006/007 for eighteen production files and both tests, plus001's nine-file foundation preservation check. Repeat those preservation checks after verification. Do not run readiness.py: its Docker lifecycle is outside this task's authorization. User Docker is already running and must not be started, stopped or restarted. If unavailable, report the prerequisite; do not launch it.

Apply only the four complete proposed blocks. No dependency installation, migration command or configuration editing is needed; initialization performs the additive Auth-only DDL when the existing fixture creates Auth. First run:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -ra --tb=short
```

Inspect complete output. Only if every57 case passes, immediately run the identical command a second time, without any manual cleanup:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -ra --tb=short
```

Expected / Predicted — Not Yet Verified: each run collects57 and reports57 passed, exit0. Tests already assert actual effective Auth settings, target database/user/root, HTTP server teardown, token configuration and the real PostgreSQL isolation. One pass is insufficient. Do not retry a failing suite until it happens to pass; preserve failure output and stop for review. Record exact commands, duration, collected/pass/error counts and any deviation in Plan.md only after execution.

Use006/007's bounded diagnostic wrapper: each Docker observation has15s timeout, captures actual child PID/output/exit and kills/reaps only that exact diagnostic child on timeout. Observe only fixture-emitted exact project labels for each run with docker ps -a, docker network ls and docker volume ls. Header-only/empty exact-project results prove fixture resource absence. All fixture Compose projects/databases/temp roots are test owned; only their existing teardown/explicit exact-project recovery can remove them. Never global prune, shared volume deletion, Desktop stop or unrelated cleanup. Do not infer absence of persistent resources merely from pytest exit0. Record Desktop status once afterward as preservation evidence; all executor-started wrapper/pytest processes and HTTP threads must have exited. The already-running user Desktop processes are deliberately preserved.

## Migration, recovery and lifecycle

Deploy/apply ordering for this milestone is Auth initializer first, then its application, then Consent composition. Existing grants are neither deleted nor recreated. All new tables and tokens are Auth owned. Additive table creation is transactional and repeatable; the existing schema_version auth1 remains compatible with GrantRepository reopening. No cross-owner migration or production data conversion occurs here. The test database is discarded by its owning fixture only.

An Auth application construction failure closes its connection. Successful composition owns one Accounts connection and exposes the approved state.close lifecycle hook; the composing caller must close it after stopping request handling, as007 does. Consent does not close its injected repository or authentication dependency because the caller owns them. Its connection is the already-delivered ConsentRepository; no new Consent connection is created. Auth uses RLock around complete owner transactions to prevent interleaving one shared psycopg connection across concurrent HTTP threadpool requests, while inherited PostgreSQL transaction advisory locking serializes account/credential/grant decisions across Auth connections. Consent serializes each entire record/read/validate operation through one application RLock over its injected repository, including each operation's multi-transaction authorization/fence checks. The composition must provide that repository exclusively to this boundary while it serves requests; injecting the same instance into unrelated concurrent callers is unsupported. No existing repository code changes.

Rollback removes only these four newly created files after stopping/closing their owned callers. Preserve existing code/tests and unrelated work; never reset/clean the checkout. On a durable nonfixture deployment do not automatically drop account/token tables or delete registrations to roll back code. This milestone does not authorize deployment or destructive schema rollback. Any unexpected schema drift, verification failure or outside-scope fix returns to planning, with actual evidence and milestone left incomplete.

## Risks and exclusions

Identity comparisons: registration/login/bootstrap use identical trim/lowercase email normalization. Password bytes preserve whitespace and are compared through constant-time derived-hash comparison. Auth emits UUID strings canonicalized from PostgreSQL UUIDs and exact User/Administrator roles. Consent principal extraction validates those same UUID/role values through actor; owner IDs, resource IDs and requested admin owner IDs use identity before comparison. Consent owner comparisons use the authenticated canonical user_id. Administrator read authorization uses the existing live GrantRepository canonical administrator_id/owner_id and exact consents:read scope; no lowercasing or alternate role spelling can elevate privileges. The synthetic role projection User suppresses administrator grants for owner-only paths while preserving the real authenticated UUID; it never changes or issues an account role.

The trusted validate_owner_consent(account, id) seam accepts only accounts from the authenticated composition; it is not a public HTTP endpoint accepting arbitrary JSON principals. Its non-forgeability depends on the approved authenticate injection being the real Auth verifier, as007 supplies. Later internal service identity/transport is explicitly excluded, not simulated by trusting a user-supplied context. Auth transport email delivery is injected; any exception rolls back its account/verification transaction and yields safe503, without exception text or credentials in HTTP errors. Delivery can occur before a later database commit failure; such a credential will be unusable and registration can be retried. No external transactional mail guarantee is claimed.

The generic Consent repository is retained: category=consent and payload contain the complete public legal event; no generic005 payload format, retention policy or immutable record is edited. Existing retention expiry/fences remain authoritative. This milestone supplies no Consent DELETE, profile mutation, grant-management HTTP, signed links, sample upload, voice enrollment, jobs/generation, rate policy, broker, audit publisher, environment/bootstrap secret resolver or deployment entry point. Those are later approved Plan responsibilities. No model loading or paid resource is needed.

## Pre-authorized contingencies

None that changes files, interfaces, assertions, dependencies or acceptance criteria. The prior006/007 diagnostic execution-context contingency may be used only on the same observed named-pipe permission denial, preserving the exact command/arguments and normal approval path. It does not authorize Docker lifecycle commands. A new environmental or functional blocker stops execution for review.

## Planning-time checks

No runtime test, database, Docker command, dependency operation, server or application import was run during planning. The active planning task prohibits runtime/test/database startup while planning and requires preserving the user's running Docker. Therefore the full disposable-copy runtime dry run required by normal guidance was not run; it remains unverified and cannot be represented as passing. Static parsing of the complete proposed blocks and review for signature/SQL/contract alignment are planning checks only. Exact observed static-check results are recorded below after checking the finished artifact.

Planning-time static command actually run from the repository cwd (no disposable copy or other file created):

```powershell
@'
import ast
import pathlib
import re
p = pathlib.Path('docs/.ai/initial-build/008_Implementation_Plan_Authentication_Consent_GREEN.md')
s = p.read_text(encoding='utf-8')
blocks = re.findall(r'^### (voice_narration/[^\n]+)\n\n```python\n(.*?)```', s, re.M | re.S)
assert len(blocks) == 4
for name, code in blocks:
    tree = ast.parse(code, filename=name)
    assert not pathlib.Path(name).exists()
    assert not any(isinstance(n, ast.Constant) and n.value is Ellipsis for n in ast.walk(tree))
    assert not re.search(r'\b(TODO|FIXME|NotImplementedError)\b', code)
    print(f'PASS {name}: complete AST, no placeholder, target absent; {len(code.splitlines())} lines')
assert (chr(60) + '!--') not in s
print('PASS four proposed files match scope; no template comments; no application imports or runtime startup')
'@ | .\.venv\Scripts\python.exe -
```

Actual trimmed output, exit0:

```text
PASS voice_narration/_http.py: complete AST, no placeholder, target absent; 72 lines
PASS voice_narration/auth/accounts.py: complete AST, no placeholder, target absent; 148 lines
PASS voice_narration/auth/application.py: complete AST, no placeholder, target absent; 48 lines
PASS voice_narration/consent/application.py: complete AST, no placeholder, target absent; 112 lines
PASS four proposed files match scope; no template comments; no application imports or runtime startup
```

Per-file exact-code review: all four headings match the four Proposed Changes paths; each provides complete final content, parses without ellipsis or placeholder and creates no executable file during planning. _http uses stdlib uuid and existing FastAPI/Starlette; accounts uses stdlib contextlib/hashlib/hmac/secrets/threading/uuid and the approved Auth/Psycopg persistence; Auth application uses existing FastAPI/Starlette and the proposed Accounts; Consent application uses stdlib functools/threading/uuid, existing FastAPI/Starlette and the injected approved repository. No new library, plugin, version or configuration name is introduced. Constructor auth_settings keys and administrator/delivery/clock seams are exactly007's reviewed inputs. SQL is parameterized; no request value becomes a SQL identifier. Static checks establish syntax and scope only; password performance, SQL integration, transport and full repeatability remain unverified until approved execution.

## Human Review

Status: Approved by avinash2196 on 2026-10-25 (recorded 2026-10-25T18:53:07Z), in response to review of this exact Authentication & Consent GREEN plan.

Execution status: Complete — executed exact four proposed production files under recorded approval on 2026-10-25. Both unchanged combined suites passed57/57 (94.11s,93.39s), no errors/skips/xfails; four new files byte-exact with recorded SHA256;18 existing005 files/004 and007 tests/nine foundation files preserved. All four fixture projects absent afterward, owned processes/HTTP threads closed, user Docker Desktop remains running. Named-pipe denial activated approved host-context contingency; no lifecycle operation. See Plan.md Authentication & Consent GREEN008 execution evidence for actual commands/outputs/hashes/inspection deviations/cleanup. No next milestone, commit or push.
