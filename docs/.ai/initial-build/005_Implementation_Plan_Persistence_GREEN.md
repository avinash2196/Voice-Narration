# Implementation Plan — Persistence & Storage GREEN

## Milestone

Persistence & Storage GREEN, milestone 5 of initial-build.

## Milestone Type

GREEN. Exact proposed production content only; this planning task does not apply it.

## Authoritative References

Paths are repository-relative. Plugin root: C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0.

| Reference inspected | Approval / authority |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved avinash2196 2026-10-19; retained P0 and Q5–Q10 clarifications recorded 2026-10-24. |
| docs/.ai/initial-build/Plan.md | Revised Plan approved avinash2196 2026-10-24. Current Execution Status: CONTRACT, FOUNDATION, assessment and recovery RED Complete; this GREEN Pending. Historical initial-state prose is not today's execution state. |
| docs/.ai/initial-build/contract/API-Contract.md | Contract Review Status approved avinash2196 2026-10-24; authoritative consumer constraints. |
| docs/.ai/initial-build/001_Implementation_Plan_Foundation.md | Approved, executed and verified; runtime, tooling, isolation and filesystem prerequisites carried forward. |
| docs/.ai/initial-build/002_Implementation_Plan_Model_Feasibility.md | Approved/executed assessment; model/protocol decisions do not grant production commercial enablement. |
| docs/.ai/initial-build/003_Implementation_Plan_Persistence_RED.md | Approved/stopped execution; exact internal interfaces and rule coverage carried forward; its environment failure is not valid RED. |
| docs/.ai/initial-build/004_Implementation_Plan_Persistence_RED_Recovery.md | Approved avinash2196 2026-10-24, executed/verified RED. Diagnostic helper only; every assertion and 33 cases preserved. |
| docs/.ai/initial-build/004-red-run2.txt | Actual linked second-run RED evidence; no approval authority. |
| voice_narration_PDD_requirements.md | Retained non-conflicting P0 context; proposed architecture is not implementation authority. |
| tests/test_persistence.py; requirements-dev.txt; pytest.ini; compose.harness.yaml | Inspected delivered tests and prerequisites; exact 004 test block verified. |
| Plugin commands/create-implementation-plan.md; agents/planner.md | Planning command and role instructions. |
| Plugin skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/prompt-driven-development/templates/Implementation-Plan.md; skills/security/SKILL.md; skills/testing/SKILL.md; skills/python-fastapi/SKILL.md | Applied process/domain guidance; no product approval. |

No docs/requirements.md or workspace AGENTS.md was found. No other work item's artifacts supply authority.

## Carried-Forward Decisions

001 fixes CPython3.13.17, pytest9.1.1, Psycopg binary3.3.6, real PostgreSQL18.6, the existing isolated Compose Linux harness and local temporary filesystem adapter. Use stdlib plus existing Psycopg only. No dependency/version/tool/configuration change is proposed, so no new version selection is made. Preserve the nine delivered prerequisite files. 002 keeps model licensing/enablement separate; synthetic nonvoice persistence does not require a model.

003/004 fix the eight owner repositories, complete call signatures, strict canonical lowercase UUID/exact role comparisons, UTC datetimes, safe PersistenceError.code, and 33 positive-before-negative cases. Preserve every test and assertion. Nine service owners remain Auth, Consent, Voices, Jobs, Artifact, Policy, AI, Worker, Audit; Worker has no independent durable private library here. No repository receives another owner's credentials. The authorize callable invokes actual owner-local Auth behavior at the approved test boundary; production must use authenticated service transport later, never Auth SQL sharing. Explicit `-p no:anyio` remains command-only; installed transitive anyio is untouched.

## Preconditions / Predecessor Evidence

Plan.md recovery004 evidence records two exact host-context `.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short` invocations: 33 cases each failed only at intended absent voice_narration imports, after real PostgreSQL18.6, loopback random port/project labels, distinct owner databases/credentials/roots, nonsuperuser roles and empty schemas were verified. Both teardowns succeeded. Durations29.54s and30.81s; full second output is 004-red-run2.txt. This is valid verified RED, not passing product behavior. 003's unknown Compose cause remains preserved history.

FOUNDATION evidence records two Windows readiness passes and actual Linux CI40132442843 at commit0fe8c317ffba011ec1e880d7d6d5af93b6b40d5a. Assessment has actual human investigation/protocol decisions. Current Plan row5 is Pending, with no approved unexecuted GREEN Implementation Plan.

## Current Repository State

Foundation files, .venv and tests/test_persistence.py exist; voice_narration package is absent. Branch codex/foundation-harness. Existing modified001/Plan and untracked002/003/004, evidence, model-eval and tests are preserved. Docker was stopped after predecessor cleanup; its readiness is observed only during approved execution. No baseline runtime test was run during this planning task.

## Files in Scope

### Files to Create

- voice_narration/__init__.py
- voice_narration/auth/__init__.py
- voice_narration/policy/__init__.py
- voice_narration/consent/__init__.py
- voice_narration/voices/__init__.py
- voice_narration/jobs/__init__.py
- voice_narration/artifacts/__init__.py
- voice_narration/ai/__init__.py
- voice_narration/audit/__init__.py
- voice_narration/_sql.py
- voice_narration/consent/persistence.py
- voice_narration/voices/persistence.py
- voice_narration/jobs/persistence.py
- voice_narration/artifacts/persistence.py
- voice_narration/ai/persistence.py
- voice_narration/auth/persistence.py
- voice_narration/policy/persistence.py
- voice_narration/audit/persistence.py

### Files to Modify

None in production/tests/dependencies/configuration. Standard post-verification PDD Execution Status bookkeeping in Plan.md and this Human Review is excluded from file-scope limits.

### Files to Delete

None.

## Proposed Changes

1. Create voice_narration/__init__.py and all eight owner __init__.py files as exact package initializers, without startup/routes/processes.
2. Create voice_narration/_sql.py: safe errors, canonical ID/role/UTC validation, explicit positive retention fields/defaults, single-owner SQL connection/transaction/migration primitives and effective actual target. The helper owns no private-record API, owner enumeration, multi-credential map or privileged SQL. A database-local advisory transaction lock serializes owner operations across instances. schema_version holds owner/version1 and rejects mismatched owner/version without recreation.
3. Create consent/persistence.py, voices/persistence.py, jobs/persistence.py, artifacts/persistence.py and ai/persistence.py with the exact separate owner classes below. Each owns only prefixed tables in its supplied database and supplied root. Deliver immutable trusted records; owner-scoped private reads/listing; live scoped grants; durable local fences; stable cleanup identity/deadline/status; physical owner-only purge; minimal safe deletion metadata. Local retention snapshots are applied explicitly without reading Policy SQL. New saves use the persisted category-specific policy to calculate expires_at atomically with insertion; no post-configuration record silently escapes retention. Read/list/byte retrieval authorizes first, performs expiration, then rechecks live authorization before returning. Observed profile/consent/sample expiration commits a durable fence before access errors, so later policy extension cannot restore access. Only Artifact/AI have binary indices and store/read APIs. Private filesystem paths never become public keys. Purge removes files before SQL records and leaves visible failed status plus permanent fence for recoverable partial deletion.
4. Create auth/persistence.py with owner-issued immutable grants, live scope/owner/admin/role/time/revocation checks and first-timestamp-preserving repeat revocation. This is trusted persistence: target account existence and Administrator eligibility are resolved by the later Auth lifecycle boundary before save_grant, without this milestone implementing account registration.
5. Create policy/persistence.py: Administrator-only retention subsection replacement; required admin values; generated30d/cleanup86400s defaults; durable effective current settings; atomic before/after metadata change events. It is not whole public Configuration revision logic.
6. Create audit/persistence.py: metadata-only exact fields, immutable append, Administrator query, independent configured occurrence-time expiry at the exact boundary. No public deletion/update method.

Explicit implementation choices for review: internal byte kind path component matches lowercase letters/underscore1–64; this is not a new public Artifact.kind/size limit. Migration version1 and advisory lock87352005 are internal constants, not new configuration or a cross-database coordinator. Root is the supplied resolved service-controlled directory. Positive values use contract Pos≤9007199254740991 and reject datetime/timedelta overflow rather than silently creating infinite retention. No hidden profile/sample/consent/audit default exists. Existing stdlib/Psycopg dependencies and all local settings/constants trace to these choices or003/004.

### Requirement / contract traceability

| Approved concern | Proposed surface | Unchanged test cases |
| --- | --- | --- |
| R-ACCT-002/003;FR-004 private libraries/history | Owner SQL records and permit/read/list | test_owner_isolation_survives_reopen (5) |
| Q10 scoped live administrator reads | Auth grants and private repository callback, AI has no grant scope | test_live_scoped_admin_grants (5) |
| R-RET-001/002 separate configurable auditable retention/defaults | Policy configure/current/events; owner apply_retention/expiry; Audit.expire | test_retention_defaults_required_values_and_audit (1); test_retention_expiry_and_shortening (5); test_audit_metadata_has_independent_bounded_retention (1) |
| R-REV-001;R-DEL-001;FR-003 immediate fence and private-data purge | Per-owner cleanup tombstone/assert_usable/read/bytes/purge | test_immediate_durable_fence_and_purge (15) |
| Fixed cleanup deadline and visible dependency failure | Failed state committed with original fence/deadline, retry same cleanup | test_cleanup_failure_never_restores_access_or_moves_deadline (1) |

Total33 cases. Internal synthetic records are not public DTOs. Trusted save/inspect/purge/expiry/deletion_metadata methods stay owner-local and cannot be routed as authorization bypasses. Scheduling/backoff/exhaustion, outbox/deduplication, cross-service immediate propagation, actual model-store adapters, signed links and deployed security remain later Plan-owned integration evidence, exactly as003/004 record. No central transaction is claimed to satisfy those boundaries.

## Proposed Code / Tests

Every following block is the complete final content of its named new file. No executable file is applied during planning.

### voice_narration/__init__.py

```python
"""Voice Narration services."""
```

### voice_narration/auth/__init__.py

```python
"""auth owner."""
```

### voice_narration/policy/__init__.py

```python
"""policy owner."""
```

### voice_narration/consent/__init__.py

```python
"""consent owner."""
```

### voice_narration/voices/__init__.py

```python
"""voices owner."""
```

### voice_narration/jobs/__init__.py

```python
"""jobs owner."""
```

### voice_narration/artifacts/__init__.py

```python
"""artifacts owner."""
```

### voice_narration/ai/__init__.py

```python
"""ai owner."""
```

### voice_narration/audit/__init__.py

```python
"""audit owner."""
```

### voice_narration/_sql.py

```python
"""Single-owner, unprivileged SQL and canonical primitives."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID
import psycopg


class PersistenceError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def fail(code):
    raise PersistenceError(code)


def identity(value):
    try:
        valid = isinstance(value, str) and str(UUID(value)) == value
    except (ValueError, TypeError, AttributeError):
        valid = False
    if not valid:
        fail("INVALID_INPUT")
    return value


def actor(value):
    if not isinstance(value, dict) or set(value) != {"user_id", "role"}:
        fail("INVALID_INPUT")
    identity(value["user_id"])
    if value["role"] not in ("User", "Administrator"):
        fail("FORBIDDEN")
    return value["user_id"], value["role"]


def instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        fail("INVALID_INPUT")
    return value.astimezone(timezone.utc)


def duration(value, multiplier=1):
    if type(value) is not int or not 1 <= value <= 9007199254740991:
        fail("INVALID_CONFIGURATION")
    try:
        return timedelta(seconds=value * multiplier)
    except OverflowError:
        fail("INVALID_CONFIGURATION")


def after(value, interval):
    try:
        return instant(value) + interval
    except OverflowError:
        fail("INVALID_CONFIGURATION")


def retention(values):
    required = {"profile_days", "sample_days", "consent_days", "audit_days"}
    if not isinstance(values, dict) or set(values) - required - {"generated_audio_days", "cleanup_window_seconds"}:
        fail("INVALID_CONFIGURATION")
    if not required <= set(values):
        fail("CONFIGURATION_REQUIRED")
    result = {"generated_audio_days": 30, "cleanup_window_seconds": 86400}
    result.update(values)
    for field, value in result.items():
        duration(value, 1 if field == "cleanup_window_seconds" else 86400)
    return result


class OwnerDatabase:
    def __init__(self, *, database, root, authorize=None):
        self._database = dict(database)
        self._root = Path(root).resolve(strict=True)
        if not self._root.is_dir():
            fail("INVALID_CONFIGURATION")
        self._authorize = authorize
        self._db = None

    @contextmanager
    def transaction(self):
        if self._db is None or self._db.closed:
            fail("DEPENDENCY_UNAVAILABLE")
        try:
            with self._db.transaction():
                self._db.execute("SELECT pg_advisory_xact_lock(87352005)")
                yield self._db
        except psycopg.Error:
            raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None

    def migrate(self, owner, statements):
        try:
            self._db = psycopg.connect(**self._database, autocommit=True)
            with self.transaction() as db:
                db.execute("CREATE TABLE IF NOT EXISTS schema_version (owner text PRIMARY KEY,version integer NOT NULL)")
                rows = db.execute("SELECT owner,version FROM schema_version").fetchall()
                if rows and rows != [(owner, 1)]:
                    fail("INVALID_CONFIGURATION")
                if not rows:
                    for statement in statements:
                        db.execute(statement)
                    db.execute("INSERT INTO schema_version VALUES (%s,1)", (owner,))
        except psycopg.Error:
            self.close()
            raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
        except Exception:
            self.close()
            raise

    def effective_target(self):
        with self.transaction() as db:
            database, user = db.execute("SELECT current_database(),current_user").fetchone()
            return {"database": database, "user": user, "host": db.info.host,
                    "port": db.info.port, "root": str(self._root)}

    def close(self):
        if self._db is not None:
            self._db.close()

    def permit(self, who, owner_id, scope, now):
        user, role = actor(who)
        identity(owner_id)
        instant(now)
        if user == owner_id:
            return
        if role == "Administrator" and scope is not None and self._authorize is not None:
            try:
                allowed = self._authorize(who, owner_id, scope, now=now)
            except Exception:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
            if allowed is True:
                return
        fail("FORBIDDEN")
```

### voice_narration/consent/persistence.py

```python
"""consent-owned private SQL records, fences and cleanup."""
from datetime import datetime, timezone
from uuid import uuid4
from psycopg.types.json import Jsonb
from voice_narration._sql import (OwnerDatabase, PersistenceError, actor as checked_actor, after, duration,
                                  fail, identity, instant, retention)


class ConsentRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("consent", (
            "CREATE TABLE consent_records (id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,category text NOT NULL,created_at timestamptz NOT NULL,payload jsonb NOT NULL,expires_at timestamptz)",
            "CREATE INDEX ON consent_records(owner_id,profile_id,consent_id)",
            "CREATE TABLE consent_cleanups (cleanup_id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,actor_id uuid NOT NULL,reason text NOT NULL,requested_at timestamptz NOT NULL,deadline_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('pending','running','completed','failed')),completed_at timestamptz,failure jsonb,UNIQUE(owner_id,profile_id,consent_id))",
            "CREATE TABLE consent_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",

        ))

    @staticmethod
    def _record(row):
        return {"id": str(row[0]), "owner_id": str(row[1]), "profile_id": str(row[2]), "consent_id": str(row[3]),
                "category": row[4], "created_at": row[5], "payload": row[6]}

    @staticmethod
    def _cleanup(row):
        return {"cleanup_id": str(row[0]), "status": row[1], "requested_at": row[2],
                "deadline_at": row[3], "completed_at": row[4], "failure": row[5]}

    def _row(self, db, resource_id):
        identity(resource_id)
        row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM consent_records WHERE id=%s", (resource_id,)).fetchone()
        if row is None:
            fail("NOT_FOUND")
        return row

    def _fenced(self, db, owner_id, profile_id, consent_id):
        return db.execute("SELECT 1 FROM consent_cleanups WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", (owner_id, profile_id, consent_id)).fetchone() is not None

    def _active(self, db, row, now):
        if self._fenced(db, row[1], row[2], row[3]):
            fail("CONSENT_REVOKED")
        if row[7] is not None and instant(now) >= row[7]:
            fail("ARTIFACT_UNAVAILABLE" if row[4] in ("generated", "joined_preview") else "CONSENT_REVOKED")

    @staticmethod
    def _scope(category):
        return "consents:read"

    def save(self, record):
        fields = {"id", "owner_id", "profile_id", "consent_id", "category", "created_at", "payload"}
        if not isinstance(record, dict) or set(record) != fields:
            fail("INVALID_INPUT")
        for field in ("id", "owner_id", "profile_id", "consent_id"):
            identity(record[field])
        created = instant(record["created_at"])
        if not isinstance(record["category"], str) or not record["category"].strip() or not isinstance(record["payload"], dict):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if self._fenced(db, record["owner_id"], record["profile_id"], record["consent_id"]):
                fail("CONSENT_REVOKED")
            if db.execute("SELECT 1 FROM consent_records WHERE id=%s", (record["id"],)).fetchone():
                fail("INVALID_STATE")
            setting = db.execute("SELECT settings FROM consent_retention WHERE singleton=true").fetchone()
            field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(record["category"])
            expiry = after(created, duration(setting[0][field], 86400)) if setting is not None and field is not None else None
            db.execute("INSERT INTO consent_records(id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (record["id"], record["owner_id"], record["profile_id"], record["consent_id"], record["category"], created, Jsonb(record["payload"]), expiry))

    def read(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            return self._record(row)

    def list(self, actor, *, owner_id, now):
        checked_actor(actor)
        identity(owner_id)
        with self.transaction() as db:
            categories = db.execute("SELECT DISTINCT category FROM consent_records WHERE owner_id=%s", (owner_id,)).fetchall()
            for (category,) in categories or [(None,)]:
                self.permit(actor, owner_id, self._scope(category), now)
        self._expire(now)
        with self.transaction() as db:
            rows = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM consent_records WHERE owner_id=%s ORDER BY created_at,id", (owner_id,)).fetchall()
            if not rows:
                self.permit(actor, owner_id, self._scope(None), now)
            result = []
            for row in rows:
                self.permit(actor, owner_id, self._scope(row[4]), now)
                if not self._fenced(db, row[1], row[2], row[3]) and (row[7] is None or instant(now) < row[7]):
                    result.append(self._record(row))
            return result

    def assert_usable(self, owner_id, profile_id, consent_id, *, now):
        for value in (owner_id, profile_id, consent_id):
            identity(value)
        self._expire(now)
        with self.transaction() as db:
            if self._fenced(db, owner_id, profile_id, consent_id):
                fail("CONSENT_REVOKED")

    def _fence(self, db, owner_id, actor_id, profile_id, consent_id, reason, now, window):
        row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM consent_cleanups WHERE owner_id=%s AND profile_id=%s AND consent_id=%s", (owner_id, profile_id, consent_id)).fetchone()
        if row:
            return self._cleanup(row)
        cleanup_id, deadline = str(uuid4()), after(now, duration(window))
        db.execute("INSERT INTO consent_cleanups(cleanup_id,owner_id,profile_id,consent_id,actor_id,reason,requested_at,deadline_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                   (cleanup_id, owner_id, profile_id, consent_id, actor_id, reason, now, deadline))
        return {"cleanup_id": cleanup_id, "status": "pending", "requested_at": now, "deadline_at": deadline, "completed_at": None, "failure": None}

    def fence(self, actor, *, profile_id, consent_id, reason, now, cleanup_window_seconds):
        user, _ = checked_actor(actor)
        identity(profile_id)
        identity(consent_id)
        now = instant(now)
        duration(cleanup_window_seconds)
        if reason not in ("profile_deleted", "consent_revoked", "sample_expired", "profile_expired", "consent_expired"):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            return self._fence(db, user, user, profile_id, consent_id, reason, now, cleanup_window_seconds)

    def cleanup(self, actor, cleanup_id):
        user, _ = checked_actor(actor)
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id FROM consent_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[6]) != user:
                fail("FORBIDDEN")
            return self._cleanup(row)

    def purge(self, cleanup_id, *, now):
        identity(cleanup_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id,profile_id,consent_id FROM consent_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if row[1] == "completed":
                return self._cleanup(row)
            records = db.execute("SELECT id FROM consent_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9]).fetchall()
            try:
                for (resource_id,) in records:
                    self._erase(str(resource_id))
            except OSError:
                db.execute("UPDATE consent_cleanups SET status='failed',failure=%s WHERE cleanup_id=%s", (Jsonb({"code": "DEPENDENCY_UNAVAILABLE", "message": "Storage unavailable"}), cleanup_id))
            else:
                db.execute("DELETE FROM consent_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9])
                db.execute("UPDATE consent_cleanups SET status='completed',completed_at=%s,failure=NULL WHERE cleanup_id=%s", (now, cleanup_id))
            return self._cleanup(db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM consent_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone())

    def inspect_private(self, resource_id):
        identity(resource_id)
        with self.transaction() as db:
            row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload FROM consent_records WHERE id=%s", (resource_id,)).fetchone()
            return self._record(row) if row else None

    def deletion_metadata(self, cleanup_id):
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT owner_id,actor_id,requested_at,profile_id,reason FROM consent_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            return {"owner_id": str(row[0]), "actor_id": str(row[1]), "occurred_at": row[2], "resource_id": str(row[3]), "type": row[4]}

    def _expire(self, now):
        now = instant(now)
        with self.transaction() as db:
            setting = db.execute("SELECT settings FROM consent_retention WHERE singleton=true").fetchone()
            if setting is None:
                return
            for item in db.execute("SELECT id,owner_id,profile_id,consent_id,category FROM consent_records WHERE expires_at<=%s", (now,)).fetchall():
                if item[4] not in ("generated", "joined_preview"):
                    reason = {"profile": "profile_expired", "consent": "consent_expired", "sample": "sample_expired"}.get(item[4])
                    if reason is not None:
                        self._fence(db, str(item[1]), str(item[1]), str(item[2]), str(item[3]), reason, now, setting[0]["cleanup_window_seconds"])
                else:
                    self._erase_expired(db, str(item[0]))

    def apply_retention(self, policy, *, now):
        policy = retention(policy)
        now = instant(now)
        self._expire(now)
        with self.transaction() as db:
            db.execute("INSERT INTO consent_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(policy),))
            for resource_id, category, created_at in db.execute("SELECT id,category,created_at FROM consent_records").fetchall():
                field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(category)
                if field is not None:
                    expiry = after(created_at, duration(policy[field], 86400))
                    db.execute("UPDATE consent_records SET expires_at=%s WHERE id=%s", (expiry, resource_id))
        self._expire(now)

    def expiry(self, resource_id):
        with self.transaction() as db:
            return self._row(db, resource_id)[7]

    def _directory(self, resource_id):
        identity(resource_id)
        target = self._root / resource_id
        if target.is_symlink() or target.resolve().parent != self._root:
            fail("INVALID_INPUT")
        return target

    def _erase(self, resource_id):
        target = self._directory(resource_id)
        if target.exists():
            for entry in target.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    raise OSError("Unexpected storage directory")
                entry.unlink(missing_ok=True)
            target.rmdir()

    def _erase_expired(self, db, resource_id):
        self._erase(resource_id)
```

### voice_narration/voices/persistence.py

```python
"""voices-owned private SQL records, fences and cleanup."""
from datetime import datetime, timezone
from uuid import uuid4
from psycopg.types.json import Jsonb
from voice_narration._sql import (OwnerDatabase, PersistenceError, actor as checked_actor, after, duration,
                                  fail, identity, instant, retention)


class ProfileRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("voices", (
            "CREATE TABLE voices_records (id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,category text NOT NULL,created_at timestamptz NOT NULL,payload jsonb NOT NULL,expires_at timestamptz)",
            "CREATE INDEX ON voices_records(owner_id,profile_id,consent_id)",
            "CREATE TABLE voices_cleanups (cleanup_id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,actor_id uuid NOT NULL,reason text NOT NULL,requested_at timestamptz NOT NULL,deadline_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('pending','running','completed','failed')),completed_at timestamptz,failure jsonb,UNIQUE(owner_id,profile_id,consent_id))",
            "CREATE TABLE voices_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",

        ))

    @staticmethod
    def _record(row):
        return {"id": str(row[0]), "owner_id": str(row[1]), "profile_id": str(row[2]), "consent_id": str(row[3]),
                "category": row[4], "created_at": row[5], "payload": row[6]}

    @staticmethod
    def _cleanup(row):
        return {"cleanup_id": str(row[0]), "status": row[1], "requested_at": row[2],
                "deadline_at": row[3], "completed_at": row[4], "failure": row[5]}

    def _row(self, db, resource_id):
        identity(resource_id)
        row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM voices_records WHERE id=%s", (resource_id,)).fetchone()
        if row is None:
            fail("NOT_FOUND")
        return row

    def _fenced(self, db, owner_id, profile_id, consent_id):
        return db.execute("SELECT 1 FROM voices_cleanups WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", (owner_id, profile_id, consent_id)).fetchone() is not None

    def _active(self, db, row, now):
        if self._fenced(db, row[1], row[2], row[3]):
            fail("CONSENT_REVOKED")
        if row[7] is not None and instant(now) >= row[7]:
            fail("ARTIFACT_UNAVAILABLE" if row[4] in ("generated", "joined_preview") else "CONSENT_REVOKED")

    @staticmethod
    def _scope(category):
        return "profiles:read"

    def save(self, record):
        fields = {"id", "owner_id", "profile_id", "consent_id", "category", "created_at", "payload"}
        if not isinstance(record, dict) or set(record) != fields:
            fail("INVALID_INPUT")
        for field in ("id", "owner_id", "profile_id", "consent_id"):
            identity(record[field])
        created = instant(record["created_at"])
        if not isinstance(record["category"], str) or not record["category"].strip() or not isinstance(record["payload"], dict):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if self._fenced(db, record["owner_id"], record["profile_id"], record["consent_id"]):
                fail("CONSENT_REVOKED")
            if db.execute("SELECT 1 FROM voices_records WHERE id=%s", (record["id"],)).fetchone():
                fail("INVALID_STATE")
            setting = db.execute("SELECT settings FROM voices_retention WHERE singleton=true").fetchone()
            field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(record["category"])
            expiry = after(created, duration(setting[0][field], 86400)) if setting is not None and field is not None else None
            db.execute("INSERT INTO voices_records(id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (record["id"], record["owner_id"], record["profile_id"], record["consent_id"], record["category"], created, Jsonb(record["payload"]), expiry))

    def read(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            return self._record(row)

    def list(self, actor, *, owner_id, now):
        checked_actor(actor)
        identity(owner_id)
        with self.transaction() as db:
            categories = db.execute("SELECT DISTINCT category FROM voices_records WHERE owner_id=%s", (owner_id,)).fetchall()
            for (category,) in categories or [(None,)]:
                self.permit(actor, owner_id, self._scope(category), now)
        self._expire(now)
        with self.transaction() as db:
            rows = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM voices_records WHERE owner_id=%s ORDER BY created_at,id", (owner_id,)).fetchall()
            if not rows:
                self.permit(actor, owner_id, self._scope(None), now)
            result = []
            for row in rows:
                self.permit(actor, owner_id, self._scope(row[4]), now)
                if not self._fenced(db, row[1], row[2], row[3]) and (row[7] is None or instant(now) < row[7]):
                    result.append(self._record(row))
            return result

    def assert_usable(self, owner_id, profile_id, consent_id, *, now):
        for value in (owner_id, profile_id, consent_id):
            identity(value)
        self._expire(now)
        with self.transaction() as db:
            if self._fenced(db, owner_id, profile_id, consent_id):
                fail("CONSENT_REVOKED")

    def _fence(self, db, owner_id, actor_id, profile_id, consent_id, reason, now, window):
        row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM voices_cleanups WHERE owner_id=%s AND profile_id=%s AND consent_id=%s", (owner_id, profile_id, consent_id)).fetchone()
        if row:
            return self._cleanup(row)
        cleanup_id, deadline = str(uuid4()), after(now, duration(window))
        db.execute("INSERT INTO voices_cleanups(cleanup_id,owner_id,profile_id,consent_id,actor_id,reason,requested_at,deadline_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                   (cleanup_id, owner_id, profile_id, consent_id, actor_id, reason, now, deadline))
        return {"cleanup_id": cleanup_id, "status": "pending", "requested_at": now, "deadline_at": deadline, "completed_at": None, "failure": None}

    def fence(self, actor, *, profile_id, consent_id, reason, now, cleanup_window_seconds):
        user, _ = checked_actor(actor)
        identity(profile_id)
        identity(consent_id)
        now = instant(now)
        duration(cleanup_window_seconds)
        if reason not in ("profile_deleted", "consent_revoked", "sample_expired", "profile_expired", "consent_expired"):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            return self._fence(db, user, user, profile_id, consent_id, reason, now, cleanup_window_seconds)

    def cleanup(self, actor, cleanup_id):
        user, _ = checked_actor(actor)
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id FROM voices_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[6]) != user:
                fail("FORBIDDEN")
            return self._cleanup(row)

    def purge(self, cleanup_id, *, now):
        identity(cleanup_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id,profile_id,consent_id FROM voices_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if row[1] == "completed":
                return self._cleanup(row)
            records = db.execute("SELECT id FROM voices_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9]).fetchall()
            try:
                for (resource_id,) in records:
                    self._erase(str(resource_id))
            except OSError:
                db.execute("UPDATE voices_cleanups SET status='failed',failure=%s WHERE cleanup_id=%s", (Jsonb({"code": "DEPENDENCY_UNAVAILABLE", "message": "Storage unavailable"}), cleanup_id))
            else:
                db.execute("DELETE FROM voices_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9])
                db.execute("UPDATE voices_cleanups SET status='completed',completed_at=%s,failure=NULL WHERE cleanup_id=%s", (now, cleanup_id))
            return self._cleanup(db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM voices_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone())

    def inspect_private(self, resource_id):
        identity(resource_id)
        with self.transaction() as db:
            row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload FROM voices_records WHERE id=%s", (resource_id,)).fetchone()
            return self._record(row) if row else None

    def deletion_metadata(self, cleanup_id):
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT owner_id,actor_id,requested_at,profile_id,reason FROM voices_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            return {"owner_id": str(row[0]), "actor_id": str(row[1]), "occurred_at": row[2], "resource_id": str(row[3]), "type": row[4]}

    def _expire(self, now):
        now = instant(now)
        with self.transaction() as db:
            setting = db.execute("SELECT settings FROM voices_retention WHERE singleton=true").fetchone()
            if setting is None:
                return
            for item in db.execute("SELECT id,owner_id,profile_id,consent_id,category FROM voices_records WHERE expires_at<=%s", (now,)).fetchall():
                if item[4] not in ("generated", "joined_preview"):
                    reason = {"profile": "profile_expired", "consent": "consent_expired", "sample": "sample_expired"}.get(item[4])
                    if reason is not None:
                        self._fence(db, str(item[1]), str(item[1]), str(item[2]), str(item[3]), reason, now, setting[0]["cleanup_window_seconds"])
                else:
                    self._erase_expired(db, str(item[0]))

    def apply_retention(self, policy, *, now):
        policy = retention(policy)
        now = instant(now)
        self._expire(now)
        with self.transaction() as db:
            db.execute("INSERT INTO voices_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(policy),))
            for resource_id, category, created_at in db.execute("SELECT id,category,created_at FROM voices_records").fetchall():
                field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(category)
                if field is not None:
                    expiry = after(created_at, duration(policy[field], 86400))
                    db.execute("UPDATE voices_records SET expires_at=%s WHERE id=%s", (expiry, resource_id))
        self._expire(now)

    def expiry(self, resource_id):
        with self.transaction() as db:
            return self._row(db, resource_id)[7]

    def _directory(self, resource_id):
        identity(resource_id)
        target = self._root / resource_id
        if target.is_symlink() or target.resolve().parent != self._root:
            fail("INVALID_INPUT")
        return target

    def _erase(self, resource_id):
        target = self._directory(resource_id)
        if target.exists():
            for entry in target.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    raise OSError("Unexpected storage directory")
                entry.unlink(missing_ok=True)
            target.rmdir()

    def _erase_expired(self, db, resource_id):
        self._erase(resource_id)
```

### voice_narration/jobs/persistence.py

```python
"""jobs-owned private SQL records, fences and cleanup."""
from datetime import datetime, timezone
from uuid import uuid4
from psycopg.types.json import Jsonb
from voice_narration._sql import (OwnerDatabase, PersistenceError, actor as checked_actor, after, duration,
                                  fail, identity, instant, retention)


class HistoryRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("jobs", (
            "CREATE TABLE jobs_records (id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,category text NOT NULL,created_at timestamptz NOT NULL,payload jsonb NOT NULL,expires_at timestamptz)",
            "CREATE INDEX ON jobs_records(owner_id,profile_id,consent_id)",
            "CREATE TABLE jobs_cleanups (cleanup_id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,actor_id uuid NOT NULL,reason text NOT NULL,requested_at timestamptz NOT NULL,deadline_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('pending','running','completed','failed')),completed_at timestamptz,failure jsonb,UNIQUE(owner_id,profile_id,consent_id))",
            "CREATE TABLE jobs_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",

        ))

    @staticmethod
    def _record(row):
        return {"id": str(row[0]), "owner_id": str(row[1]), "profile_id": str(row[2]), "consent_id": str(row[3]),
                "category": row[4], "created_at": row[5], "payload": row[6]}

    @staticmethod
    def _cleanup(row):
        return {"cleanup_id": str(row[0]), "status": row[1], "requested_at": row[2],
                "deadline_at": row[3], "completed_at": row[4], "failure": row[5]}

    def _row(self, db, resource_id):
        identity(resource_id)
        row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM jobs_records WHERE id=%s", (resource_id,)).fetchone()
        if row is None:
            fail("NOT_FOUND")
        return row

    def _fenced(self, db, owner_id, profile_id, consent_id):
        return db.execute("SELECT 1 FROM jobs_cleanups WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", (owner_id, profile_id, consent_id)).fetchone() is not None

    def _active(self, db, row, now):
        if self._fenced(db, row[1], row[2], row[3]):
            fail("CONSENT_REVOKED")
        if row[7] is not None and instant(now) >= row[7]:
            fail("ARTIFACT_UNAVAILABLE" if row[4] in ("generated", "joined_preview") else "CONSENT_REVOKED")

    @staticmethod
    def _scope(category):
        return "jobs:read"

    def save(self, record):
        fields = {"id", "owner_id", "profile_id", "consent_id", "category", "created_at", "payload"}
        if not isinstance(record, dict) or set(record) != fields:
            fail("INVALID_INPUT")
        for field in ("id", "owner_id", "profile_id", "consent_id"):
            identity(record[field])
        created = instant(record["created_at"])
        if not isinstance(record["category"], str) or not record["category"].strip() or not isinstance(record["payload"], dict):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if self._fenced(db, record["owner_id"], record["profile_id"], record["consent_id"]):
                fail("CONSENT_REVOKED")
            if db.execute("SELECT 1 FROM jobs_records WHERE id=%s", (record["id"],)).fetchone():
                fail("INVALID_STATE")
            setting = db.execute("SELECT settings FROM jobs_retention WHERE singleton=true").fetchone()
            field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(record["category"])
            expiry = after(created, duration(setting[0][field], 86400)) if setting is not None and field is not None else None
            db.execute("INSERT INTO jobs_records(id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (record["id"], record["owner_id"], record["profile_id"], record["consent_id"], record["category"], created, Jsonb(record["payload"]), expiry))

    def read(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            return self._record(row)

    def list(self, actor, *, owner_id, now):
        checked_actor(actor)
        identity(owner_id)
        with self.transaction() as db:
            categories = db.execute("SELECT DISTINCT category FROM jobs_records WHERE owner_id=%s", (owner_id,)).fetchall()
            for (category,) in categories or [(None,)]:
                self.permit(actor, owner_id, self._scope(category), now)
        self._expire(now)
        with self.transaction() as db:
            rows = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM jobs_records WHERE owner_id=%s ORDER BY created_at,id", (owner_id,)).fetchall()
            if not rows:
                self.permit(actor, owner_id, self._scope(None), now)
            result = []
            for row in rows:
                self.permit(actor, owner_id, self._scope(row[4]), now)
                if not self._fenced(db, row[1], row[2], row[3]) and (row[7] is None or instant(now) < row[7]):
                    result.append(self._record(row))
            return result

    def assert_usable(self, owner_id, profile_id, consent_id, *, now):
        for value in (owner_id, profile_id, consent_id):
            identity(value)
        self._expire(now)
        with self.transaction() as db:
            if self._fenced(db, owner_id, profile_id, consent_id):
                fail("CONSENT_REVOKED")

    def _fence(self, db, owner_id, actor_id, profile_id, consent_id, reason, now, window):
        row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM jobs_cleanups WHERE owner_id=%s AND profile_id=%s AND consent_id=%s", (owner_id, profile_id, consent_id)).fetchone()
        if row:
            return self._cleanup(row)
        cleanup_id, deadline = str(uuid4()), after(now, duration(window))
        db.execute("INSERT INTO jobs_cleanups(cleanup_id,owner_id,profile_id,consent_id,actor_id,reason,requested_at,deadline_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                   (cleanup_id, owner_id, profile_id, consent_id, actor_id, reason, now, deadline))
        return {"cleanup_id": cleanup_id, "status": "pending", "requested_at": now, "deadline_at": deadline, "completed_at": None, "failure": None}

    def fence(self, actor, *, profile_id, consent_id, reason, now, cleanup_window_seconds):
        user, _ = checked_actor(actor)
        identity(profile_id)
        identity(consent_id)
        now = instant(now)
        duration(cleanup_window_seconds)
        if reason not in ("profile_deleted", "consent_revoked", "sample_expired", "profile_expired", "consent_expired"):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            return self._fence(db, user, user, profile_id, consent_id, reason, now, cleanup_window_seconds)

    def cleanup(self, actor, cleanup_id):
        user, _ = checked_actor(actor)
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id FROM jobs_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[6]) != user:
                fail("FORBIDDEN")
            return self._cleanup(row)

    def purge(self, cleanup_id, *, now):
        identity(cleanup_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id,profile_id,consent_id FROM jobs_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if row[1] == "completed":
                return self._cleanup(row)
            records = db.execute("SELECT id FROM jobs_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9]).fetchall()
            try:
                for (resource_id,) in records:
                    self._erase(str(resource_id))
            except OSError:
                db.execute("UPDATE jobs_cleanups SET status='failed',failure=%s WHERE cleanup_id=%s", (Jsonb({"code": "DEPENDENCY_UNAVAILABLE", "message": "Storage unavailable"}), cleanup_id))
            else:
                db.execute("DELETE FROM jobs_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9])
                db.execute("UPDATE jobs_cleanups SET status='completed',completed_at=%s,failure=NULL WHERE cleanup_id=%s", (now, cleanup_id))
            return self._cleanup(db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM jobs_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone())

    def inspect_private(self, resource_id):
        identity(resource_id)
        with self.transaction() as db:
            row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload FROM jobs_records WHERE id=%s", (resource_id,)).fetchone()
            return self._record(row) if row else None

    def deletion_metadata(self, cleanup_id):
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT owner_id,actor_id,requested_at,profile_id,reason FROM jobs_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            return {"owner_id": str(row[0]), "actor_id": str(row[1]), "occurred_at": row[2], "resource_id": str(row[3]), "type": row[4]}

    def _expire(self, now):
        now = instant(now)
        with self.transaction() as db:
            setting = db.execute("SELECT settings FROM jobs_retention WHERE singleton=true").fetchone()
            if setting is None:
                return
            for item in db.execute("SELECT id,owner_id,profile_id,consent_id,category FROM jobs_records WHERE expires_at<=%s", (now,)).fetchall():
                if item[4] not in ("generated", "joined_preview"):
                    reason = {"profile": "profile_expired", "consent": "consent_expired", "sample": "sample_expired"}.get(item[4])
                    if reason is not None:
                        self._fence(db, str(item[1]), str(item[1]), str(item[2]), str(item[3]), reason, now, setting[0]["cleanup_window_seconds"])
                else:
                    self._erase_expired(db, str(item[0]))

    def apply_retention(self, policy, *, now):
        policy = retention(policy)
        now = instant(now)
        self._expire(now)
        with self.transaction() as db:
            db.execute("INSERT INTO jobs_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(policy),))
            for resource_id, category, created_at in db.execute("SELECT id,category,created_at FROM jobs_records").fetchall():
                field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(category)
                if field is not None:
                    expiry = after(created_at, duration(policy[field], 86400))
                    db.execute("UPDATE jobs_records SET expires_at=%s WHERE id=%s", (expiry, resource_id))
        self._expire(now)

    def expiry(self, resource_id):
        with self.transaction() as db:
            return self._row(db, resource_id)[7]

    def _directory(self, resource_id):
        identity(resource_id)
        target = self._root / resource_id
        if target.is_symlink() or target.resolve().parent != self._root:
            fail("INVALID_INPUT")
        return target

    def _erase(self, resource_id):
        target = self._directory(resource_id)
        if target.exists():
            for entry in target.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    raise OSError("Unexpected storage directory")
                entry.unlink(missing_ok=True)
            target.rmdir()

    def _erase_expired(self, db, resource_id):
        self._erase(resource_id)
```

### voice_narration/artifacts/persistence.py

```python
"""artifacts-owned private SQL records, fences and cleanup."""
from datetime import datetime, timezone
from uuid import uuid4
import os
import re
from psycopg.types.json import Jsonb
from voice_narration._sql import (OwnerDatabase, PersistenceError, actor as checked_actor, after, duration,
                                  fail, identity, instant, retention)


class ArtifactRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("artifacts", (
            "CREATE TABLE artifacts_records (id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,category text NOT NULL,created_at timestamptz NOT NULL,payload jsonb NOT NULL,expires_at timestamptz)",
            "CREATE INDEX ON artifacts_records(owner_id,profile_id,consent_id)",
            "CREATE TABLE artifacts_cleanups (cleanup_id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,actor_id uuid NOT NULL,reason text NOT NULL,requested_at timestamptz NOT NULL,deadline_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('pending','running','completed','failed')),completed_at timestamptz,failure jsonb,UNIQUE(owner_id,profile_id,consent_id))",
            "CREATE TABLE artifacts_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",
            "CREATE TABLE artifacts_bytes (resource_id uuid NOT NULL REFERENCES artifacts_records(id) ON DELETE CASCADE,kind text NOT NULL,position bigint GENERATED ALWAYS AS IDENTITY,PRIMARY KEY(resource_id,kind))",
        ))

    @staticmethod
    def _record(row):
        return {"id": str(row[0]), "owner_id": str(row[1]), "profile_id": str(row[2]), "consent_id": str(row[3]),
                "category": row[4], "created_at": row[5], "payload": row[6]}

    @staticmethod
    def _cleanup(row):
        return {"cleanup_id": str(row[0]), "status": row[1], "requested_at": row[2],
                "deadline_at": row[3], "completed_at": row[4], "failure": row[5]}

    def _row(self, db, resource_id):
        identity(resource_id)
        row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM artifacts_records WHERE id=%s", (resource_id,)).fetchone()
        if row is None:
            fail("NOT_FOUND")
        return row

    def _fenced(self, db, owner_id, profile_id, consent_id):
        return db.execute("SELECT 1 FROM artifacts_cleanups WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", (owner_id, profile_id, consent_id)).fetchone() is not None

    def _active(self, db, row, now):
        if self._fenced(db, row[1], row[2], row[3]):
            fail("CONSENT_REVOKED")
        if row[7] is not None and instant(now) >= row[7]:
            fail("ARTIFACT_UNAVAILABLE" if row[4] in ("generated", "joined_preview") else "CONSENT_REVOKED")

    @staticmethod
    def _scope(category):
        return {"sample": "samples:read", "generated": "audio:read", "joined_preview": "audio:read"}.get(category)

    def save(self, record):
        fields = {"id", "owner_id", "profile_id", "consent_id", "category", "created_at", "payload"}
        if not isinstance(record, dict) or set(record) != fields:
            fail("INVALID_INPUT")
        for field in ("id", "owner_id", "profile_id", "consent_id"):
            identity(record[field])
        created = instant(record["created_at"])
        if not isinstance(record["category"], str) or not record["category"].strip() or not isinstance(record["payload"], dict):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if self._fenced(db, record["owner_id"], record["profile_id"], record["consent_id"]):
                fail("CONSENT_REVOKED")
            if db.execute("SELECT 1 FROM artifacts_records WHERE id=%s", (record["id"],)).fetchone():
                fail("INVALID_STATE")
            setting = db.execute("SELECT settings FROM artifacts_retention WHERE singleton=true").fetchone()
            field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(record["category"])
            expiry = after(created, duration(setting[0][field], 86400)) if setting is not None and field is not None else None
            db.execute("INSERT INTO artifacts_records(id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (record["id"], record["owner_id"], record["profile_id"], record["consent_id"], record["category"], created, Jsonb(record["payload"]), expiry))

    def read(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            return self._record(row)

    def list(self, actor, *, owner_id, now):
        checked_actor(actor)
        identity(owner_id)
        with self.transaction() as db:
            categories = db.execute("SELECT DISTINCT category FROM artifacts_records WHERE owner_id=%s", (owner_id,)).fetchall()
            for (category,) in categories or [(None,)]:
                self.permit(actor, owner_id, self._scope(category), now)
        self._expire(now)
        with self.transaction() as db:
            rows = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM artifacts_records WHERE owner_id=%s ORDER BY created_at,id", (owner_id,)).fetchall()
            if not rows:
                self.permit(actor, owner_id, self._scope(None), now)
            result = []
            for row in rows:
                self.permit(actor, owner_id, self._scope(row[4]), now)
                if not self._fenced(db, row[1], row[2], row[3]) and (row[7] is None or instant(now) < row[7]):
                    result.append(self._record(row))
            return result

    def assert_usable(self, owner_id, profile_id, consent_id, *, now):
        for value in (owner_id, profile_id, consent_id):
            identity(value)
        self._expire(now)
        with self.transaction() as db:
            if self._fenced(db, owner_id, profile_id, consent_id):
                fail("CONSENT_REVOKED")

    def _fence(self, db, owner_id, actor_id, profile_id, consent_id, reason, now, window):
        row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM artifacts_cleanups WHERE owner_id=%s AND profile_id=%s AND consent_id=%s", (owner_id, profile_id, consent_id)).fetchone()
        if row:
            return self._cleanup(row)
        cleanup_id, deadline = str(uuid4()), after(now, duration(window))
        db.execute("INSERT INTO artifacts_cleanups(cleanup_id,owner_id,profile_id,consent_id,actor_id,reason,requested_at,deadline_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                   (cleanup_id, owner_id, profile_id, consent_id, actor_id, reason, now, deadline))
        return {"cleanup_id": cleanup_id, "status": "pending", "requested_at": now, "deadline_at": deadline, "completed_at": None, "failure": None}

    def fence(self, actor, *, profile_id, consent_id, reason, now, cleanup_window_seconds):
        user, _ = checked_actor(actor)
        identity(profile_id)
        identity(consent_id)
        now = instant(now)
        duration(cleanup_window_seconds)
        if reason not in ("profile_deleted", "consent_revoked", "sample_expired", "profile_expired", "consent_expired"):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            return self._fence(db, user, user, profile_id, consent_id, reason, now, cleanup_window_seconds)

    def cleanup(self, actor, cleanup_id):
        user, _ = checked_actor(actor)
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[6]) != user:
                fail("FORBIDDEN")
            return self._cleanup(row)

    def purge(self, cleanup_id, *, now):
        identity(cleanup_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id,profile_id,consent_id FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if row[1] == "completed":
                return self._cleanup(row)
            records = db.execute("SELECT id FROM artifacts_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9]).fetchall()
            try:
                for (resource_id,) in records:
                    self._erase(str(resource_id))
            except OSError:
                db.execute("UPDATE artifacts_cleanups SET status='failed',failure=%s WHERE cleanup_id=%s", (Jsonb({"code": "DEPENDENCY_UNAVAILABLE", "message": "Storage unavailable"}), cleanup_id))
            else:
                db.execute("DELETE FROM artifacts_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9])
                db.execute("UPDATE artifacts_cleanups SET status='completed',completed_at=%s,failure=NULL WHERE cleanup_id=%s", (now, cleanup_id))
            return self._cleanup(db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone())

    def inspect_private(self, resource_id):
        identity(resource_id)
        with self.transaction() as db:
            row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload FROM artifacts_records WHERE id=%s", (resource_id,)).fetchone()
            return self._record(row) if row else None

    def deletion_metadata(self, cleanup_id):
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT owner_id,actor_id,requested_at,profile_id,reason FROM artifacts_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            return {"owner_id": str(row[0]), "actor_id": str(row[1]), "occurred_at": row[2], "resource_id": str(row[3]), "type": row[4]}

    def _expire(self, now):
        now = instant(now)
        with self.transaction() as db:
            setting = db.execute("SELECT settings FROM artifacts_retention WHERE singleton=true").fetchone()
            if setting is None:
                return
            for item in db.execute("SELECT id,owner_id,profile_id,consent_id,category FROM artifacts_records WHERE expires_at<=%s", (now,)).fetchall():
                if item[4] not in ("generated", "joined_preview"):
                    reason = {"profile": "profile_expired", "consent": "consent_expired", "sample": "sample_expired"}.get(item[4])
                    if reason is not None:
                        self._fence(db, str(item[1]), str(item[1]), str(item[2]), str(item[3]), reason, now, setting[0]["cleanup_window_seconds"])
                else:
                    self._erase_expired(db, str(item[0]))

    def apply_retention(self, policy, *, now):
        policy = retention(policy)
        now = instant(now)
        self._expire(now)
        with self.transaction() as db:
            db.execute("INSERT INTO artifacts_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(policy),))
            for resource_id, category, created_at in db.execute("SELECT id,category,created_at FROM artifacts_records").fetchall():
                field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(category)
                if field is not None:
                    expiry = after(created_at, duration(policy[field], 86400))
                    db.execute("UPDATE artifacts_records SET expires_at=%s WHERE id=%s", (expiry, resource_id))
        self._expire(now)

    def expiry(self, resource_id):
        with self.transaction() as db:
            return self._row(db, resource_id)[7]

    def _directory(self, resource_id):
        identity(resource_id)
        target = self._root / resource_id
        if target.is_symlink() or target.resolve().parent != self._root:
            fail("INVALID_INPUT")
        return target

    def _erase(self, resource_id):
        target = self._directory(resource_id)
        if target.exists():
            for entry in target.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    raise OSError("Unexpected storage directory")
                entry.unlink(missing_ok=True)
            target.rmdir()

    def _erase_expired(self, db, resource_id):
        try:
            self._erase(resource_id)
        except OSError:
            return
        db.execute("DELETE FROM artifacts_bytes WHERE resource_id=%s", (resource_id,))

    def store_bytes(self, resource_id, kind, data):
        self._expire(datetime.now(timezone.utc))
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self._active(db, row, datetime.now(timezone.utc))
            if not isinstance(kind, str) or not re.fullmatch(r"[a-z_]{1,64}", kind) or not isinstance(data, bytes):
                fail("INVALID_INPUT")
            directory = self._directory(resource_id)
            temporary = None
            try:
                directory.mkdir(exist_ok=True, mode=0o700)
                temporary = directory / ("tmp_" + uuid4().hex)
                with temporary.open("xb") as output:
                    output.write(data)
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temporary, directory / kind)
                db.execute("INSERT INTO artifacts_bytes(resource_id,kind) VALUES (%s,%s) ON CONFLICT(resource_id,kind) DO NOTHING", (resource_id, kind))
            except OSError:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
            finally:
                if temporary is not None and temporary.exists():
                    try:
                        temporary.unlink()
                    except OSError:
                        pass

    def read_bytes(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            kinds = db.execute("SELECT kind FROM artifacts_bytes WHERE resource_id=%s ORDER BY position", (resource_id,)).fetchall()
            directory = self._directory(resource_id)
            try:
                result = []
                for (kind,) in kinds:
                    path = directory / kind
                    if path.is_symlink():
                        fail("DEPENDENCY_UNAVAILABLE")
                    result.append(path.read_bytes())
                return result
            except OSError:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
```

### voice_narration/ai/persistence.py

```python
"""ai-owned private SQL records, fences and cleanup."""
from datetime import datetime, timezone
from uuid import uuid4
import os
import re
from psycopg.types.json import Jsonb
from voice_narration._sql import (OwnerDatabase, PersistenceError, actor as checked_actor, after, duration,
                                  fail, identity, instant, retention)


class ConditioningRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("ai", (
            "CREATE TABLE ai_records (id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,category text NOT NULL,created_at timestamptz NOT NULL,payload jsonb NOT NULL,expires_at timestamptz)",
            "CREATE INDEX ON ai_records(owner_id,profile_id,consent_id)",
            "CREATE TABLE ai_cleanups (cleanup_id uuid PRIMARY KEY,owner_id uuid NOT NULL,profile_id uuid NOT NULL,consent_id uuid NOT NULL,actor_id uuid NOT NULL,reason text NOT NULL,requested_at timestamptz NOT NULL,deadline_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('pending','running','completed','failed')),completed_at timestamptz,failure jsonb,UNIQUE(owner_id,profile_id,consent_id))",
            "CREATE TABLE ai_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",
            "CREATE TABLE ai_bytes (resource_id uuid NOT NULL REFERENCES ai_records(id) ON DELETE CASCADE,kind text NOT NULL,position bigint GENERATED ALWAYS AS IDENTITY,PRIMARY KEY(resource_id,kind))",
        ))

    @staticmethod
    def _record(row):
        return {"id": str(row[0]), "owner_id": str(row[1]), "profile_id": str(row[2]), "consent_id": str(row[3]),
                "category": row[4], "created_at": row[5], "payload": row[6]}

    @staticmethod
    def _cleanup(row):
        return {"cleanup_id": str(row[0]), "status": row[1], "requested_at": row[2],
                "deadline_at": row[3], "completed_at": row[4], "failure": row[5]}

    def _row(self, db, resource_id):
        identity(resource_id)
        row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM ai_records WHERE id=%s", (resource_id,)).fetchone()
        if row is None:
            fail("NOT_FOUND")
        return row

    def _fenced(self, db, owner_id, profile_id, consent_id):
        return db.execute("SELECT 1 FROM ai_cleanups WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", (owner_id, profile_id, consent_id)).fetchone() is not None

    def _active(self, db, row, now):
        if self._fenced(db, row[1], row[2], row[3]):
            fail("CONSENT_REVOKED")
        if row[7] is not None and instant(now) >= row[7]:
            fail("ARTIFACT_UNAVAILABLE" if row[4] in ("generated", "joined_preview") else "CONSENT_REVOKED")

    @staticmethod
    def _scope(category):
        return None

    def save(self, record):
        fields = {"id", "owner_id", "profile_id", "consent_id", "category", "created_at", "payload"}
        if not isinstance(record, dict) or set(record) != fields:
            fail("INVALID_INPUT")
        for field in ("id", "owner_id", "profile_id", "consent_id"):
            identity(record[field])
        created = instant(record["created_at"])
        if not isinstance(record["category"], str) or not record["category"].strip() or not isinstance(record["payload"], dict):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if self._fenced(db, record["owner_id"], record["profile_id"], record["consent_id"]):
                fail("CONSENT_REVOKED")
            if db.execute("SELECT 1 FROM ai_records WHERE id=%s", (record["id"],)).fetchone():
                fail("INVALID_STATE")
            setting = db.execute("SELECT settings FROM ai_retention WHERE singleton=true").fetchone()
            field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(record["category"])
            expiry = after(created, duration(setting[0][field], 86400)) if setting is not None and field is not None else None
            db.execute("INSERT INTO ai_records(id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (record["id"], record["owner_id"], record["profile_id"], record["consent_id"], record["category"], created, Jsonb(record["payload"]), expiry))

    def read(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            return self._record(row)

    def list(self, actor, *, owner_id, now):
        checked_actor(actor)
        identity(owner_id)
        with self.transaction() as db:
            categories = db.execute("SELECT DISTINCT category FROM ai_records WHERE owner_id=%s", (owner_id,)).fetchall()
            for (category,) in categories or [(None,)]:
                self.permit(actor, owner_id, self._scope(category), now)
        self._expire(now)
        with self.transaction() as db:
            rows = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload,expires_at FROM ai_records WHERE owner_id=%s ORDER BY created_at,id", (owner_id,)).fetchall()
            if not rows:
                self.permit(actor, owner_id, self._scope(None), now)
            result = []
            for row in rows:
                self.permit(actor, owner_id, self._scope(row[4]), now)
                if not self._fenced(db, row[1], row[2], row[3]) and (row[7] is None or instant(now) < row[7]):
                    result.append(self._record(row))
            return result

    def assert_usable(self, owner_id, profile_id, consent_id, *, now):
        for value in (owner_id, profile_id, consent_id):
            identity(value)
        self._expire(now)
        with self.transaction() as db:
            if self._fenced(db, owner_id, profile_id, consent_id):
                fail("CONSENT_REVOKED")

    def _fence(self, db, owner_id, actor_id, profile_id, consent_id, reason, now, window):
        row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM ai_cleanups WHERE owner_id=%s AND profile_id=%s AND consent_id=%s", (owner_id, profile_id, consent_id)).fetchone()
        if row:
            return self._cleanup(row)
        cleanup_id, deadline = str(uuid4()), after(now, duration(window))
        db.execute("INSERT INTO ai_cleanups(cleanup_id,owner_id,profile_id,consent_id,actor_id,reason,requested_at,deadline_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                   (cleanup_id, owner_id, profile_id, consent_id, actor_id, reason, now, deadline))
        return {"cleanup_id": cleanup_id, "status": "pending", "requested_at": now, "deadline_at": deadline, "completed_at": None, "failure": None}

    def fence(self, actor, *, profile_id, consent_id, reason, now, cleanup_window_seconds):
        user, _ = checked_actor(actor)
        identity(profile_id)
        identity(consent_id)
        now = instant(now)
        duration(cleanup_window_seconds)
        if reason not in ("profile_deleted", "consent_revoked", "sample_expired", "profile_expired", "consent_expired"):
            fail("INVALID_INPUT")
        with self.transaction() as db:
            return self._fence(db, user, user, profile_id, consent_id, reason, now, cleanup_window_seconds)

    def cleanup(self, actor, cleanup_id):
        user, _ = checked_actor(actor)
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id FROM ai_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[6]) != user:
                fail("FORBIDDEN")
            return self._cleanup(row)

    def purge(self, cleanup_id, *, now):
        identity(cleanup_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure,owner_id,profile_id,consent_id FROM ai_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if row[1] == "completed":
                return self._cleanup(row)
            records = db.execute("SELECT id FROM ai_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9]).fetchall()
            try:
                for (resource_id,) in records:
                    self._erase(str(resource_id))
            except OSError:
                db.execute("UPDATE ai_cleanups SET status='failed',failure=%s WHERE cleanup_id=%s", (Jsonb({"code": "DEPENDENCY_UNAVAILABLE", "message": "Storage unavailable"}), cleanup_id))
            else:
                db.execute("DELETE FROM ai_records WHERE owner_id=%s AND (profile_id=%s OR consent_id=%s)", row[6:9])
                db.execute("UPDATE ai_cleanups SET status='completed',completed_at=%s,failure=NULL WHERE cleanup_id=%s", (now, cleanup_id))
            return self._cleanup(db.execute("SELECT cleanup_id,status,requested_at,deadline_at,completed_at,failure FROM ai_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone())

    def inspect_private(self, resource_id):
        identity(resource_id)
        with self.transaction() as db:
            row = db.execute("SELECT id,owner_id,profile_id,consent_id,category,created_at,payload FROM ai_records WHERE id=%s", (resource_id,)).fetchone()
            return self._record(row) if row else None

    def deletion_metadata(self, cleanup_id):
        identity(cleanup_id)
        with self.transaction() as db:
            row = db.execute("SELECT owner_id,actor_id,requested_at,profile_id,reason FROM ai_cleanups WHERE cleanup_id=%s", (cleanup_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            return {"owner_id": str(row[0]), "actor_id": str(row[1]), "occurred_at": row[2], "resource_id": str(row[3]), "type": row[4]}

    def _expire(self, now):
        now = instant(now)
        with self.transaction() as db:
            setting = db.execute("SELECT settings FROM ai_retention WHERE singleton=true").fetchone()
            if setting is None:
                return
            for item in db.execute("SELECT id,owner_id,profile_id,consent_id,category FROM ai_records WHERE expires_at<=%s", (now,)).fetchall():
                if item[4] not in ("generated", "joined_preview"):
                    reason = {"profile": "profile_expired", "consent": "consent_expired", "sample": "sample_expired"}.get(item[4])
                    if reason is not None:
                        self._fence(db, str(item[1]), str(item[1]), str(item[2]), str(item[3]), reason, now, setting[0]["cleanup_window_seconds"])
                else:
                    self._erase_expired(db, str(item[0]))

    def apply_retention(self, policy, *, now):
        policy = retention(policy)
        now = instant(now)
        self._expire(now)
        with self.transaction() as db:
            db.execute("INSERT INTO ai_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(policy),))
            for resource_id, category, created_at in db.execute("SELECT id,category,created_at FROM ai_records").fetchall():
                field = {"profile": "profile_days", "sample": "sample_days", "consent": "consent_days", "generated": "generated_audio_days", "joined_preview": "generated_audio_days"}.get(category)
                if field is not None:
                    expiry = after(created_at, duration(policy[field], 86400))
                    db.execute("UPDATE ai_records SET expires_at=%s WHERE id=%s", (expiry, resource_id))
        self._expire(now)

    def expiry(self, resource_id):
        with self.transaction() as db:
            return self._row(db, resource_id)[7]

    def _directory(self, resource_id):
        identity(resource_id)
        target = self._root / resource_id
        if target.is_symlink() or target.resolve().parent != self._root:
            fail("INVALID_INPUT")
        return target

    def _erase(self, resource_id):
        target = self._directory(resource_id)
        if target.exists():
            for entry in target.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    raise OSError("Unexpected storage directory")
                entry.unlink(missing_ok=True)
            target.rmdir()

    def _erase_expired(self, db, resource_id):
        try:
            self._erase(resource_id)
        except OSError:
            return
        db.execute("DELETE FROM ai_bytes WHERE resource_id=%s", (resource_id,))

    def store_bytes(self, resource_id, kind, data):
        self._expire(datetime.now(timezone.utc))
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self._active(db, row, datetime.now(timezone.utc))
            if not isinstance(kind, str) or not re.fullmatch(r"[a-z_]{1,64}", kind) or not isinstance(data, bytes):
                fail("INVALID_INPUT")
            directory = self._directory(resource_id)
            temporary = None
            try:
                directory.mkdir(exist_ok=True, mode=0o700)
                temporary = directory / ("tmp_" + uuid4().hex)
                with temporary.open("xb") as output:
                    output.write(data)
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temporary, directory / kind)
                db.execute("INSERT INTO ai_bytes(resource_id,kind) VALUES (%s,%s) ON CONFLICT(resource_id,kind) DO NOTHING", (resource_id, kind))
            except OSError:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
            finally:
                if temporary is not None and temporary.exists():
                    try:
                        temporary.unlink()
                    except OSError:
                        pass

    def read_bytes(self, actor, resource_id, *, now):
        checked_actor(actor)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
        self._expire(now)
        with self.transaction() as db:
            row = self._row(db, resource_id)
            self.permit(actor, str(row[1]), self._scope(row[4]), now)
            self._active(db, row, now)
            kinds = db.execute("SELECT kind FROM ai_bytes WHERE resource_id=%s ORDER BY position", (resource_id,)).fetchall()
            directory = self._directory(resource_id)
            try:
                result = []
                for (kind,) in kinds:
                    path = directory / kind
                    if path.is_symlink():
                        fail("DEPENDENCY_UNAVAILABLE")
                    result.append(path.read_bytes())
                return result
            except OSError:
                raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
```

### voice_narration/auth/persistence.py

```python
"""Auth-owned live scoped private-read grants."""
from psycopg.types.json import Jsonb
from voice_narration._sql import OwnerDatabase, actor as checked_actor, fail, identity, instant


SCOPES = {"profiles:read", "samples:read", "jobs:read", "audio:read", "consents:read"}


class GrantRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("auth", (
            "CREATE TABLE auth_grants (grant_id uuid PRIMARY KEY,owner_id uuid NOT NULL,administrator_id uuid NOT NULL,scopes jsonb NOT NULL,created_at timestamptz NOT NULL,expires_at timestamptz NOT NULL,revoked_at timestamptz)",
            "CREATE INDEX ON auth_grants(owner_id,administrator_id)",
        ))

    @staticmethod
    def _grant(row):
        return {"grant_id": str(row[0]), "owner_id": str(row[1]), "administrator_id": str(row[2]), "scopes": row[3], "created_at": row[4], "expires_at": row[5], "revoked_at": row[6]}

    def save_grant(self, actor, grant, *, now):
        user, _ = checked_actor(actor)
        now = instant(now)
        fields = {"grant_id", "owner_id", "administrator_id", "scopes", "created_at", "expires_at", "revoked_at"}
        if not isinstance(grant, dict) or set(grant) != fields:
            fail("INVALID_INPUT")
        for field in ("grant_id", "owner_id", "administrator_id"):
            identity(grant[field])
        if user != grant["owner_id"]:
            fail("FORBIDDEN")
        scopes = grant["scopes"]
        if not isinstance(scopes, list) or not scopes or any(type(s) is not str or s not in SCOPES for s in scopes):
            fail("INVALID_INPUT")
        if len(set(scopes)) != len(scopes) or grant["revoked_at"] is not None:
            fail("INVALID_INPUT")
        created, expires = instant(grant["created_at"]), instant(grant["expires_at"])
        if expires <= now or expires <= created:
            fail("INVALID_INPUT")
        with self.transaction() as db:
            if db.execute("SELECT 1 FROM auth_grants WHERE grant_id=%s", (grant["grant_id"],)).fetchone():
                fail("INVALID_STATE")
            db.execute("INSERT INTO auth_grants VALUES (%s,%s,%s,%s,%s,%s,NULL)", (grant["grant_id"], user, grant["administrator_id"], Jsonb(scopes), created, expires))

    def revoke_grant(self, actor, grant_id, *, now):
        user, _ = checked_actor(actor)
        identity(grant_id)
        now = instant(now)
        with self.transaction() as db:
            row = db.execute("SELECT grant_id,owner_id,administrator_id,scopes,created_at,expires_at,revoked_at FROM auth_grants WHERE grant_id=%s", (grant_id,)).fetchone()
            if row is None:
                fail("NOT_FOUND")
            if str(row[1]) != user:
                fail("FORBIDDEN")
            db.execute("UPDATE auth_grants SET revoked_at=COALESCE(revoked_at,%s) WHERE grant_id=%s", (now, grant_id))
            return self._grant(db.execute("SELECT grant_id,owner_id,administrator_id,scopes,created_at,expires_at,revoked_at FROM auth_grants WHERE grant_id=%s", (grant_id,)).fetchone())

    def authorize(self, actor, owner_id, scope, *, now):
        user, role = checked_actor(actor)
        identity(owner_id)
        now = instant(now)
        if role != "Administrator" or scope not in SCOPES:
            return False
        with self.transaction() as db:
            return db.execute("SELECT 1 FROM auth_grants WHERE owner_id=%s AND administrator_id=%s AND scopes @> %s AND created_at<=%s AND expires_at>%s AND revoked_at IS NULL LIMIT 1", (owner_id, user, Jsonb([scope]), now, now)).fetchone() is not None
```

### voice_narration/policy/persistence.py

```python
"""Policy-owned retention subsection and atomic change history."""
from psycopg.types.json import Jsonb
from voice_narration._sql import OwnerDatabase, actor as checked_actor, fail, instant, retention


class RetentionRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("policy", (
            "CREATE TABLE policy_retention (singleton boolean PRIMARY KEY CHECK(singleton),settings jsonb NOT NULL)",
            "CREATE TABLE policy_retention_events (sequence bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,actor_id uuid NOT NULL,occurred_at timestamptz NOT NULL,before_value jsonb,after_value jsonb NOT NULL)",
        ))

    def configure(self, actor, values, *, now):
        user, role = checked_actor(actor)
        if role != "Administrator":
            fail("FORBIDDEN")
        now, values = instant(now), retention(values)
        with self.transaction() as db:
            row = db.execute("SELECT settings FROM policy_retention WHERE singleton=true").fetchone()
            before = row[0] if row else None
            if before != values:
                db.execute("INSERT INTO policy_retention VALUES (true,%s) ON CONFLICT(singleton) DO UPDATE SET settings=EXCLUDED.settings", (Jsonb(values),))
                db.execute("INSERT INTO policy_retention_events(actor_id,occurred_at,before_value,after_value) VALUES (%s,%s,%s,%s)", (user, now, Jsonb(before), Jsonb(values)))
            return values

    def current(self):
        with self.transaction() as db:
            row = db.execute("SELECT settings FROM policy_retention WHERE singleton=true").fetchone()
            if row is None:
                fail("CONFIGURATION_REQUIRED")
            return row[0]

    def policy_events(self):
        with self.transaction() as db:
            return [{"actor_id": str(r[0]), "occurred_at": r[1], "before": r[2], "after": r[3]}
                    for r in db.execute("SELECT actor_id,occurred_at,before_value,after_value FROM policy_retention_events ORDER BY sequence").fetchall()]
```

### voice_narration/audit/persistence.py

```python
"""Audit metadata with independent explicit retention."""
from voice_narration._sql import OwnerDatabase, actor as checked_actor, after, duration, fail, identity, instant


class AuditRepository(OwnerDatabase):
    def initialize(self):
        self.migrate("audit", (
            "CREATE TABLE audit_events (event_id uuid PRIMARY KEY,owner_id uuid NOT NULL,actor_id uuid NOT NULL,occurred_at timestamptz NOT NULL,resource_id uuid NOT NULL,type text NOT NULL,outcome text NOT NULL)",
            "CREATE INDEX ON audit_events(occurred_at,event_id)",
        ))

    def append(self, event):
        fields = {"event_id", "owner_id", "actor_id", "occurred_at", "resource_id", "type", "outcome"}
        if not isinstance(event, dict) or set(event) != fields:
            fail("INVALID_INPUT")
        for field in ("event_id", "owner_id", "actor_id", "resource_id"):
            identity(event[field])
        instant(event["occurred_at"])
        for field in ("type", "outcome"):
            if not isinstance(event[field], str) or not event[field].strip():
                fail("INVALID_INPUT")
        with self.transaction() as db:
            if db.execute("SELECT 1 FROM audit_events WHERE event_id=%s", (event["event_id"],)).fetchone():
                fail("INVALID_STATE")
            db.execute("INSERT INTO audit_events VALUES (%s,%s,%s,%s,%s,%s,%s)", tuple(event[k] for k in ("event_id", "owner_id", "actor_id", "occurred_at", "resource_id", "type", "outcome")))

    def events(self, actor, *, now):
        _, role = checked_actor(actor)
        instant(now)
        if role != "Administrator":
            fail("FORBIDDEN")
        with self.transaction() as db:
            return [{"event_id": str(r[0]), "owner_id": str(r[1]), "actor_id": str(r[2]), "occurred_at": r[3], "resource_id": str(r[4]), "type": r[5], "outcome": r[6]}
                    for r in db.execute("SELECT event_id,owner_id,actor_id,occurred_at,resource_id,type,outcome FROM audit_events ORDER BY occurred_at,event_id").fetchall()]

    def expire(self, *, audit_days, now):
        now, window = instant(now), duration(audit_days, 86400)
        with self.transaction() as db:
            for event_id, occurred in db.execute("SELECT event_id,occurred_at FROM audit_events").fetchall():
                if after(occurred, window) <= now:
                    db.execute("DELETE FROM audit_events WHERE event_id=%s", (event_id,))
```

## Execution Steps

After this exact artifact records human approval: confirm predecessor status, unchanged test block, branch/worktree and foundation preservation. Stop for incompatible drift. Create only the18 exact files above. Initialize owners independently through their own database credentials; run verification below. Any failing check stops for review; do not edit tests, add files or retry until passing. Second suite runs only after first fully passes. Record actual output/exit codes and cleanup in Plan.md, then update this Human Review execution disposition. No later milestone begins automatically.

## Acceptance / Completion Criteria

All18 created files match exact blocks; existing test matches004; all nine foundation files remain unchanged. Both exact suite runs collect and pass all33 cases with no failure/error/skip/xfail and effective real PostgreSQL/database/role/root isolation checks passing, without manual cleanup between runs. Required behavior includes durable SQL across reopen, owner/scoped live reads, required effective retention values and atomic policy audit, exact expiry/shortening, immediate durable local fences, physical owned bytes/metadata purge, stable cleanup identity/deadline/idempotency, visible deletion failure and independent bounded safe audit expiry. No unrelated baseline failure is waived. No previously passing application suite exists beyond this capability. Standard own PDD status bookkeeping is outside file-scope limits. All fixture resources/processes and any Desktop runtime started here must be stopped before reporting.

## Verification

### Commands

Run each separately from repository root; retain real output and exit codes:

```powershell
git branch --show-current
git status --short
git diff --check
git diff --exit-code HEAD -- requirements-dev.txt pytest.ini compose.harness.yaml containers/harness.Dockerfile .dockerignore .gitignore tools/readiness.py docs/developer-setup.md .github/workflows/harness.yml
.\.venv\Scripts\python.exe -c "import sys, importlib.metadata as m; print(sys.executable); print([(p.name,p.value,p.dist.name,p.dist.version) for p in m.entry_points(group='pytest11')])"
docker context show
docker version
docker compose version
docker info --format '{{.ServerVersion}}'
```

Interpreter must be project.venv CPython3.13.17; sole known pytest11 entrypoint anyio/anyio.pytest_plugin4.15.1. New entrypoints stop for review. Carried prerequisites Docker29.3.1 client/server, desktop-linux context and Compose5.6.0. Stopped/missing Desktop pipe is recoverable prerequisite readiness, not an artificial startup gate. Start the existing approved installed runtime with the exact hidden command below. Its sandbox launch may not persist; the same host launch is permitted under the dedicated contingency. Poll the same Docker diagnostics at intervals≤15seconds for up to120seconds, preserving output; missing pipe/not-ready during startup is not a failed test. Do not install/change settings. After the bounded window an unresolved readiness failure stops with evidence.

```powershell
Start-Process -FilePath 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -WindowStyle Hidden
```

When ready, run separately without manual cleaning between invocations:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
```

Both headers must show no loaded anyio plugin. No PYTEST_DISABLE_PLUGIN_AUTOLOAD, pytest.ini/environment rewrite or package change. Linux equivalent .venv/bin/python with identical arguments. Fixtures themselves establish actual PostgreSQL18.6 identity/version, loopback random published port/project, distinct nonsuperuser databases/roles and effective owner roots, so no extra readiness/browser/audio/model process is needed. Second run is authorized only after first passes all cases and teardown. Unexpected environment errors stop, never count as GREEN. Repeat first four git checks after both. Compare18 actual files to exact UTF-8 blocks and existing test to004; record per-file SHA256/counts as actual execution evidence.

Fixtures remove only their own databases/roles/random Compose project. Retain printed project IDs; after interruption inspect exact com.docker.compose.project label and use only that project's existing `compose down --volumes --remove-orphans` with its original fixture environment. No global prune. Stop only Desktop started by this execution using `docker desktop stop`; verify `docker desktop status` and absence of runtime processes started here. Failed cleanup remains incomplete evidence.

### Expected Evidence

Expected / Predicted — Not Yet Verified: two33/33-pass runs with all effective isolation, SQL reopen, live grants, retention/fencing/purge/failure/audit assertions passing; successful fixture teardown, foundation preservation and no unexpected changed file. No prediction is verified milestone evidence. A single pass or static analysis cannot complete GREEN.

### Planning-Time Dry Run

No disposable runtime dry run: active task explicitly prohibits runtime startups and permits static/scratch checks only. Full verification needs Docker/PostgreSQL, stopped after predecessor cleanup. No pytest, Docker launch, DB connection, dependency install or proposed-module import ran during planning. SQL execution, transaction/filesystem behavior and the33-case outcome remain unverified pending approved execution. No unrelated baseline application failure was observed or waived.

Temporary generator vn005_tmp.py outside the repository assembled exact blocks and AST-extracted pure value functions only. It created no proposed executable repository file. Temporary files were removed after checks. An earlier separate temporary handoff failed FileNotFoundError before any repository mutation; an oversized Windows generator command failed launcher error206 before execution. These are planning-tool failures, not baseline failures or runtime evidence. Final assembly used bounded filesystem patches. Actual short command and trimmed output:

```text
.\.venv\Scripts\python.exe C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\vn005_tmp.py
PASS: 18 complete Python blocks; AST; zero Ellipsis/generator markers; exact 004 test preservation; pure retention defaults/explicit values/five invalid values/four required omissions; canonical identity checks
```

This is planning-time static/pure scratch evidence only. Per-file complete-code review is below. Final scope checks record actual results without claiming runtime soundness.

## Migration, Compatibility and Recovery

Each owner's complete inline initialize migration creates only its local schema; no migration tool/dependency is added. Existing approved fixtures use empty databases. DDL/version insertion share one transaction/advisory lock; crash rolls back partial schema. Reopen retains data at owner/version1; mismatch fails closed for reviewed migration planning. Initialize each owner before its API, independently of other owners. Production code uses no superuser/create-role/create-database commands; test provisioning alone uses the approved harness admin.

Purge deletes local files before SQL private rows, catches OSError to commit visible failed status, preserves original fence/deadline and retries missing files idempotently. Crash after some unlinks but before SQL commit leaves a durable fence and retryable rows. Crash after byte rename but before index commit can leave an unindexed private file; purge enumerates the whole validated resource directory including temporary files. No byte write can race a same-owner fence under the shared owner-local SQL advisory lock. This is not a service-spanning transaction.

Rollback removes only these newly created18 files after preserving evidence; fixture cleanup owns only temporary test databases/roots. Never drop a live owner database/root, downgrade persistent production data, reset/clean unrelated work or erase evidence. A required production downgrade/data migration returns to planning.

## Risks

Canonical comparisons: actor.user_id versus resource/list owner; grant owner versus grant actor; grant administrator versus read actor; exact role versus Administrator; exact category scope versus grant scopes; owner/profile/consent versus fence/purge; cleanup owner versus status actor; Policy/Audit actor role versus Administrator. Canonical lowercase UUIDs are rejected if malformed/whitespace/uppercase rather than normalized differently from Auth. Roles are exact enums. UTC comparisons deny at exact grant expiry; revoke preserves first timestamp. Read grants never authorize mutation/purge. Auth account/target eligibility and validated trusted Context belong to later lifecycle/boundary work; raw public owner assertions cannot call these trusted methods.

The shared SQL primitive stores one supplied nonprivileged credential/root, no aggregate repository/owner map/private API. Five private implementations own separate prefixed schema/migrations and deliberately duplicate owner logic. No shared privileged facade is introduced. Later async routes must offload synchronous SQL/filesystem work; no route is added here.

The local root must be service-controlled; UUID directories reject symlinks/escape, reads reject symlink files, purge unlinks symlinks without following them. Deployed encryption/IAM/managed secrets and actual cloud/model adapters are unproved until later integration. Generated/preview expiry removes audio only, never profile revocation. Generated expiry unlink failure leaves data inaccessible by expiry and retries on subsequent expiration sweeps; requested purge has explicit failed Cleanup. Scheduling/deadline retry exhaustion and distributed propagation remain later integration scope explicitly excluded by003/004. No throughput/latency claim follows from a coarse owner-local lock.

Audit has separate configured expire(audit_days,now), immutable append and no public delete. Deletion export/tombstones carry identifiers/times/type/status only, no scripts/audio/embeddings; Audit transport ingestion remains later. Policy's unconfigured section returns CONFIGURATION_REQUIRED rather than inventing admin duration defaults. Representability errors stop configuration rather than silently disabling expiry.

## Pre-authorized Contingencies

Existing Docker startup/readiness and host execution only. Exact observable triggers: stopped/missing Desktop engine pipe; identical sandbox launch does not persist; or explicit permission/access denial to dockerDesktopLinuxEngine. Files changed: none. Exact change: same hidden Start-Process and same context/version/compose/info diagnostics in approved host execution facility, unchanged cwd/environment, bounded polling above. If Docker permission denial affects pytest, after host diagnostics establish readiness run the identical two pytest commands in that same host context, second only after first fully passes. Record each trigger/application. Automatic approval review may reject execution; report stated reason and stop rather than bypassing it. No extra dependencies/configuration, file changes, skips, assertion changes or automatic repeated failed suites are authorized.

## Explicitly Out of Scope

Tests/helper/assertions; dependencies/build/runtime/infrastructure configuration; HTTP/service bootstraps; account/token/consent enrollment lifecycle; job/idempotency/quotas; cloud provisioning/model download/inference/commercial clearance; broker/outbox/worker scheduling; cross-service transport/auth; deployed encryption/IAM/signed links; real model-store adapter purge; frontend; new agents; commits/push/publication; approving/executing this plan or beginning later milestones.

## Exact-Code and Authority Review

| File | Review |
| --- | --- |
| voice_narration/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/auth/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/policy/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/consent/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/voices/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/jobs/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/artifacts/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/ai/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/audit/__init__.py | Complete final content, 1 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 1. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/_sql.py | Complete final content, 135 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 2. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/consent/persistence.py | Complete final content, 222 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 3. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/voices/persistence.py | Complete final content, 222 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 3. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/jobs/persistence.py | Complete final content, 222 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 3. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/artifacts/persistence.py | Complete final content, 278 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 3. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/ai/persistence.py | Complete final content, 278 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 3. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/auth/persistence.py | Complete final content, 63 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 4. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/policy/persistence.py | Complete final content, 36 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 5. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |
| voice_narration/audit/persistence.py | Complete final content, 41 lines; AST parsed; no Ellipsis/generator marker/pseudocode. Matches Proposed Changes 6. Imports are stdlib/existing Psycopg; defaults/settings/migration/locking decisions traced above. |

Final actual static/scope checks:18 complete Python blocks parsed; every public actor parameter retains the approved keyword name; all five private saves compute expiry from persisted settings; authorization precedes read-triggered sweeps; zero Ellipsis/TODO/TBD/FIXME/generator markers; balanced fences; one review status; exact004 test block unchanged; no production package exists. `git diff --check` exit0 with existing001/Plan LF-to-CRLF notices only. The exact nine-file foundation preservation diff exited0 without output. `git status --short` adds only005 to the prior repository changes. These observations are not runtime or milestone evidence.

No new normative R-/FR-/AC-/Q identifier is defined; cited labels reference approved sources. Schema/class/method/lock labels identify implementation only and do not redefine artifact authority. No template comments remain.005 is the next implementation-plan number. No production/test/dependency/configuration file changed during planning.

## Human Review

Status: Approved by avinash2196 on 2026-10-24 (recorded 2026-10-25T03:25:08Z), in response to review of this exact GREEN implementation plan.

Execution status: Execution stopped at a blocker — see Plan.md. Re-approval required before execution. Exact 18 production files applied and verified against this plan; bounded Docker readiness did not establish a successful engine diagnostic. No pytest invocation ran; GREEN is not verified. Owned Docker runtime and diagnostics stopped. No code/test/dependency/configuration fix or later milestone was attempted.
