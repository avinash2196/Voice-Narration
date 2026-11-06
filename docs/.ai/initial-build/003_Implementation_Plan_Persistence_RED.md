# Implementation Plan — Persistence & Storage RED

## Milestone

Persistence & Storage RED, milestone 4 of initial-build.

## Milestone Type

RED. Proposed tests only; this document does not implement or execute them.

## Authoritative References

Paths are repository-relative unless prefixed with the installed plugin root.

| Read document | Authority / disposition |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved by avinash2196 2026-10-19; retained P0 and Q5–Q10 clarifications approved 2026-10-24. |
| docs/.ai/initial-build/Plan.md | Revised Plan approved 2026-10-24. CONTRACT, FOUNDATION and assessment Complete; Persistence RED Pending. Owns milestone scope and traceability. |
| docs/.ai/initial-build/contract/API-Contract.md | Contract Review Status approved by avinash2196 2026-10-24; authoritative consumer behavior. |
| docs/.ai/initial-build/001_Implementation_Plan_Foundation.md | Approved and executed; Windows two-pass and Linux CI evidence recorded in Plan.md. Binding prerequisites carried forward below. |
| docs/.ai/initial-build/002_Implementation_Plan_Model_Feasibility.md | Approved and executed; documentation and actual human decisions recorded in Plan.md. |
| docs/.ai/initial-build/model-eval/approved.md | Actual avinash2196 investigation selection and protocol v1 approval recorded 2026-10-25T02:05:44Z, local 2026-10-24. Initial undecided text is issuance history. Commercial clearance/enablement withheld; irrelevant to synthetic nonmodel persistence tests. |
| docs/.ai/initial-build/Contract-Review.md | Historical review; does not supersede approved contract. |
| docs/.ai/initial-build/architecture/System-Architecture.md | Only nine-service deployment-shape decision approved. Remaining examples are not implementation authority. |
| voice_narration_PDD_requirements.md | Retained non-conflicting baseline P0 context under approved work-item scope. |
| README.md; docs/developer-setup.md; tools/readiness.py; requirements-dev.txt; pytest.ini; compose.harness.yaml | Inspected repository facts / delivered FOUNDATION prerequisites, not new product requirements. |
| Installed plugin commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/prompt-driven-development/templates/Implementation-Plan.md; skills/testing/SKILL.md; skills/security/SKILL.md; skills/python-fastapi/SKILL.md | Process/domain guidance applied. Plugin root C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0. |

No docs/requirements.md or workspace AGENTS.md was found. Process documents introduce no product approval.

## Carried-Forward Decisions

001 fixes CPython 3.13.17, pytest 9.1.1 without plugins, HTTPX 0.28.1, Psycopg binary 3.3.6 and real PostgreSQL 18.6. Preserve all other pinned prerequisites, existing Compose, pytest configuration and Windows/Linux commands. Use stdlib plus existing pytest/Psycopg only; no dependency, runtime, build or infrastructure change. Function-local capability fixtures belong to the proposed test file, not global conftest. Each case gets fresh service databases/credentials and tmp_path roots; verify effective targets. No SQLite substitute, shared development database, paid resource, model loader or audio download.

Nine owners remain Auth, Consent, Voices, Jobs, Artifact, Policy, AI, Worker, Audit. Separate owner databases and credentials are mandatory. Test orchestration is not a new production service or central privileged persistence facade. Worker has no independent durable private library here; its future temporary outputs remain covered by Artifact/AI storage boundaries and later integration tests.

## Preconditions / Predecessor Evidence

Plan.md Execution Status and its FOUNDATION evidence record exact nine delivered prerequisite files, successful Windows two-pass readiness, cleanup and real Linux CI run 40132442843 at commit 0fe8c317ffba011ec1e880d7d6d5af93b6b40d5a. Assessment evidence records four reviewed documents and actual investigation/protocol decisions. No production model approval is needed for nonvoice bytes and synthetic metadata.

No approved unexecuted persistence plan exists. Current task creates only this 003 document. During eventual RED execution, Docker Linux engine must be available through the approved existing local setup; failure is a prerequisite failure, never RED evidence. Docker was stopped after FOUNDATION; planning does not restart it or repeat readiness merely to regenerate prior evidence.

## Current Repository State

Read-only inspection found delivered prerequisite files, documentation, and no tests or production modules. Branch is codex/foundation-harness. Existing modified 001 and Plan.md and untracked 002/model-eval documents are preserved. No pyproject.toml exists; none is required or proposed. Intended persistence symbols are absent, which is legitimate predicted RED under the Plan, not a reason to add stubs.

## Files in Scope

### Files to Create

tests/test_persistence.py only, complete content below.

### Files to Modify

None. Verified-execution PDD bookkeeping is limited to Plan.md and this document's Human Review field after actual execution; it is not authorization to change scope.

### Files to Delete

None.

## Proposed Changes

1. Create one capability test file containing its own ephemeral PostgreSQL fixture and service-local repository tests. It orchestrates the existing Compose project with a random project name/password/loopback port, provisions fresh per-service roles/databases per case and asserts PostgreSQL version/effective identity/path. It cleans only resources it created.
2. Propose exact internal persistence calls as reviewable GREEN targets below. These are Python repository boundaries, not additions to the approved HTTP/message contract. RED creates no module, class, implementation, schema or migration. Reconnection tests prove persistence outside one object lifetime. All data is synthetic.
3. Verify owner-only direct/list reads and scoped live administrator grants, no existence enumeration, independent policies/defaults, expiry and policy shortening, immediate durable fences, bounded auditable physical purge, retry and partial failure. API parsing/status serialization/authentication and cross-service transport remain later milestones; tests assert typed repository error codes only.

## Proposed Code / Tests

The following is the complete final content of tests/test_persistence.py. No other executable file is proposed.

```python
"""Service-local persistence contracts; synthetic data, real PostgreSQL."""
from datetime import datetime, timedelta, timezone
import importlib
import json
from pathlib import Path
import secrets
import subprocess
import uuid

import psycopg
from psycopg import sql
import pytest


ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2030, 1, 1, tzinfo=timezone.utc)
OWNER = "11111111-1111-4111-8111-111111111111"
OTHER = "22222222-2222-4222-8222-222222222222"
ADMIN = "33333333-3333-4333-8333-333333333333"
PROFILE = "44444444-4444-4444-8444-444444444444"
CONSENT = "55555555-5555-4555-8555-555555555555"
SERVICES = {
    "auth": "GrantRepository",
    "policy": "RetentionRepository",
    "consent": "ConsentRepository",
    "voices": "ProfileRepository",
    "jobs": "HistoryRepository",
    "artifacts": "ArtifactRepository",
    "ai": "ConditioningRepository",
    "audit": "AuditRepository",
}
PRIVATE = ("consent", "voices", "jobs", "artifacts", "ai")


def uid():
    return str(uuid.uuid4())


def principal(identity=OWNER, role="User"):
    return {"user_id": identity, "role": role}


def run(args, env=None):
    return subprocess.run(
        args, cwd=ROOT, env=env, check=True, capture_output=True,
        text=True, timeout=180,
    ).stdout.strip()


@pytest.fixture(scope="module")
def postgres():
    import os
    env = dict(os.environ, HARNESS_DB_PASSWORD=secrets.token_hex(24))
    project = "vnred" + uuid.uuid4().hex
    command = ["docker", "compose", "-f", "compose.harness.yaml", "-p", project]
    try:
        run(command + ["config", "--quiet"], env)
        run(command + ["up", "--detach", "--wait", "--wait-timeout", "120"], env)
        port = int(run(command + ["port", "postgres", "5432"], env).rsplit(":", 1)[1])
        container = run(command + ["ps", "--quiet", "postgres"], env)
        info = json.loads(run(["docker", "inspect", container]))[0]
        assert info["Config"]["Labels"]["com.docker.compose.project"] == project
        assert info["HostConfig"]["PortBindings"]["5432/tcp"][0]["HostIp"] == "127.0.0.1"
        target = dict(host="127.0.0.1", port=port, dbname="harness",
                      user="harness", password=env["HARNESS_DB_PASSWORD"], connect_timeout=10)
        with psycopg.connect(**target) as db:
            assert db.execute("SELECT current_database(), current_user, "
                              "current_setting('server_version_num')::int").fetchone() == (
                                  "harness", "harness", 180006)
            assert db.info.port == port
        print("isolated persistence project:", project, "container:", container)
        yield target
    finally:
        run(command + ["down", "--volumes", "--remove-orphans"], env)


@pytest.fixture
def stores(postgres, tmp_path):
    targets = {}
    paths = {}
    instances = []
    with psycopg.connect(**postgres, autocommit=True) as admin:
        try:
            for service in SERVICES:
                name = "vn_" + uuid.uuid4().hex
                password = secrets.token_hex(24)
                admin.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {} NOSUPERUSER "
                                      "NOCREATEDB NOCREATEROLE NOINHERIT").format(
                                          sql.Identifier(name), sql.Literal(password)))
                targets[service] = dict(postgres, dbname=name, user=name, password=password)
                admin.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(name), sql.Identifier(name)))
                paths[service] = (tmp_path / service).resolve()
                paths[service].mkdir()
                with psycopg.connect(**targets[service]) as db:
                    assert db.execute("SELECT current_database(), current_user").fetchone() == (
                        name, name)
                    assert db.info.host == "127.0.0.1" and db.info.port == postgres["port"]
                    assert db.execute("SELECT rolsuper, rolcreatedb, rolcreaterole "
                                      "FROM pg_roles WHERE rolname=current_user").fetchone() == (
                                          False, False, False)
                    assert db.execute("SELECT tablename FROM pg_tables "
                                      "WHERE schemaname='public'").fetchall() == []
                    db.execute(sql.SQL("REVOKE CONNECT ON DATABASE {} FROM PUBLIC").format(
                        sql.Identifier(name)))
            assert len({t["dbname"] for t in targets.values()}) == len(SERVICES)
            assert len(set(paths.values())) == len(SERVICES)

            def open_store(service, authority=None):
                module = importlib.import_module(f"voice_narration.{service}.persistence")
                cls = getattr(module, SERVICES[service])
                store = cls(database=targets[service], root=paths[service], authorize=authority)
                instances.append(store)
                store.initialize()
                effective = store.effective_target()
                assert effective == {"database": targets[service]["dbname"],
                                     "user": targets[service]["user"],
                                     "host": "127.0.0.1", "port": postgres["port"],
                                     "root": str(paths[service])}
                return store

            yield open_store, paths, targets
        finally:
            for store in reversed(instances):
                store.close()
            for target in reversed(list(targets.values())):
                admin.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                    sql.Identifier(target["dbname"])))
                admin.execute(sql.SQL("DROP ROLE IF EXISTS {}").format(sql.Identifier(target["user"])))


def resource(identity=None, owner=OWNER, created=NOW, category="profile"):
    return {"id": identity or uid(), "owner_id": owner, "profile_id": PROFILE,
            "consent_id": CONSENT, "category": category, "created_at": created,
            "payload": {"marker": "SYNTHETIC_PRIVATE_MARKER", "text": "नमस्ते\nHello."}}


def denied(call, code):
    with pytest.raises(Exception) as caught:
        call()
    assert type(caught.value).__name__ == "PersistenceError"
    assert caught.value.code == code
    assert "SYNTHETIC_PRIVATE_MARKER" not in str(caught.value)


@pytest.mark.integration
@pytest.mark.parametrize("service", PRIVATE)
def test_owner_isolation_survives_reopen(stores, service):
    open_store, _, _ = stores
    repo = open_store(service)
    mine, foreign = resource(), resource(owner=OTHER)
    repo.save(mine)
    repo.save(foreign)
    assert repo.read(principal(), mine["id"], now=NOW) == mine
    assert repo.list(principal(), owner_id=OWNER, now=NOW) == [mine]
    denied(lambda: repo.read(principal(" " + OWNER), mine["id"], now=NOW), "INVALID_INPUT")
    denied(lambda: repo.read(principal(ADMIN, "administrator"), mine["id"], now=NOW), "FORBIDDEN")
    denied(lambda: repo.read(principal(), foreign["id"], now=NOW), "FORBIDDEN")
    denied(lambda: repo.read(principal(), uid(), now=NOW), "NOT_FOUND")
    denied(lambda: repo.list(principal(), owner_id=OTHER, now=NOW), "FORBIDDEN")
    denied(lambda: repo.read(principal(ADMIN, "Administrator"), mine["id"], now=NOW), "FORBIDDEN")
    repo.close()
    reopened = open_store(service)
    assert reopened.read(principal(), mine["id"], now=NOW) == mine
    denied(lambda: reopened.read(principal(OTHER), mine["id"], now=NOW), "FORBIDDEN")


@pytest.mark.integration
@pytest.mark.parametrize("service,scope,category", (
    ("consent", "consents:read", "consent"), ("voices", "profiles:read", "profile"),
    ("jobs", "jobs:read", "job"), ("artifacts", "samples:read", "sample"),
    ("artifacts", "audio:read", "generated"),
))
def test_live_scoped_admin_grants(stores, service, scope, category):
    open_store, _, _ = stores
    auth = open_store("auth")
    repo = open_store(service, auth.authorize)
    item = resource(category=category)
    repo.save(item)
    actor = principal(ADMIN, "Administrator")
    assert repo.read(principal(), item["id"], now=NOW) == item
    denied(lambda: repo.read(actor, item["id"], now=NOW), "FORBIDDEN")
    grant = {"grant_id": uid(), "owner_id": OWNER, "administrator_id": ADMIN,
             "scopes": [scope], "created_at": NOW,
             "expires_at": NOW + timedelta(hours=1), "revoked_at": None}
    auth.save_grant(principal(), grant, now=NOW)
    assert repo.read(actor, item["id"], now=NOW) == item
    assert repo.list(actor, owner_id=OWNER, now=NOW) == [item]
    denied(lambda: repo.read(principal(OTHER, "Administrator"), item["id"], now=NOW), "FORBIDDEN")
    denied(lambda: repo.read(principal(ADMIN, "User"), item["id"], now=NOW), "FORBIDDEN")
    denied(lambda: auth.save_grant(principal(OTHER), dict(grant, grant_id=uid()), now=NOW), "FORBIDDEN")
    denied(lambda: repo.read(actor, item["id"], now=grant["expires_at"]), "FORBIDDEN")
    auth.revoke_grant(principal(), grant["grant_id"], now=NOW + timedelta(minutes=1))
    denied(lambda: repo.read(actor, item["id"], now=NOW + timedelta(minutes=1)), "FORBIDDEN")
    again = auth.revoke_grant(principal(), grant["grant_id"], now=NOW + timedelta(minutes=2))
    assert again["revoked_at"] == NOW + timedelta(minutes=1)
    wrong_scope = "jobs:read" if scope != "jobs:read" else "profiles:read"
    wrong = dict(grant, grant_id=uid(), scopes=[wrong_scope])
    auth.save_grant(principal(), wrong, now=NOW)
    denied(lambda: repo.read(actor, item["id"], now=NOW), "FORBIDDEN")
    auth.save_grant(principal(), dict(grant, grant_id=uid()), now=NOW)
    assert repo.read(actor, item["id"], now=NOW) == item
    repo.fence(principal(), profile_id=PROFILE, consent_id=CONSENT,
               reason="consent_revoked", now=NOW, cleanup_window_seconds=86400)
    denied(lambda: repo.read(actor, item["id"], now=NOW), "CONSENT_REVOKED")


@pytest.mark.integration
def test_retention_defaults_required_values_and_audit(stores):
    open_store, _, _ = stores
    policy = open_store("policy")
    configured = {"profile_days": 8, "sample_days": 3, "consent_days": 9, "audit_days": 12}
    result = policy.configure(principal(ADMIN, "Administrator"), configured, now=NOW)
    assert result == dict(configured, generated_audio_days=30, cleanup_window_seconds=86400)
    assert open_store("policy").current() == result
    denied(lambda: policy.configure(principal(), configured, now=NOW), "FORBIDDEN")
    for field in configured:
        bad = dict(configured)
        del bad[field]
        denied(lambda: policy.configure(principal(ADMIN, "Administrator"), bad, now=NOW),
               "CONFIGURATION_REQUIRED")
    for value in (0, -1, True, None, "2"):
        denied(lambda: policy.configure(principal(ADMIN, "Administrator"),
               dict(configured, sample_days=value), now=NOW), "INVALID_CONFIGURATION")
    changed = dict(result, generated_audio_days=2, cleanup_window_seconds=3600)
    assert policy.configure(principal(ADMIN, "Administrator"), changed, now=NOW) == changed
    events = policy.policy_events()
    assert len(events) == 2
    assert events[-1] == {"actor_id": ADMIN, "occurred_at": NOW, "before": result, "after": changed}


@pytest.mark.integration
@pytest.mark.parametrize("service,category,days", (
    ("voices", "profile", 8), ("consent", "consent", 9),
    ("artifacts", "sample", 3), ("artifacts", "generated", 30),
    ("artifacts", "joined_preview", 30),
))
def test_retention_expiry_and_shortening(stores, service, category, days):
    open_store, _, _ = stores
    repo = open_store(service)
    item = resource(category=category)
    policy = {"profile_days": 8, "sample_days": 3, "consent_days": 9, "audit_days": 12,
              "generated_audio_days": 30, "cleanup_window_seconds": 86400}
    repo.save(item)
    repo.apply_retention(policy, now=NOW)
    expiry = NOW + timedelta(days=days)
    assert repo.expiry(item["id"]) == expiry
    assert repo.read(principal(), item["id"], now=expiry - timedelta(microseconds=1)) == item
    denied(lambda: repo.read(principal(), item["id"], now=expiry), "CONSENT_REVOKED"
           if category in ("profile", "consent", "sample") else "ARTIFACT_UNAVAILABLE")
    if category in ("generated", "joined_preview"):
        assert repo.assert_usable(OWNER, PROFILE, CONSENT, now=expiry) is None
    else:
        denied(lambda: repo.assert_usable(OWNER, PROFILE, CONSENT, now=expiry), "CONSENT_REVOKED")
    shorter = dict(policy)
    field = {"profile": "profile_days", "consent": "consent_days", "sample": "sample_days"}.get(
        category, "generated_audio_days")
    shorter[field] = 1
    repo.apply_retention(shorter, now=NOW + timedelta(days=2))
    assert repo.expiry(item["id"]) == NOW + timedelta(days=1)
    denied(lambda: repo.read(principal(), item["id"], now=NOW + timedelta(days=2)),
           "CONSENT_REVOKED" if category in ("profile", "consent", "sample") else "ARTIFACT_UNAVAILABLE")


@pytest.mark.integration
@pytest.mark.parametrize("service", PRIVATE)
@pytest.mark.parametrize("reason", ("profile_deleted", "consent_revoked", "sample_expired"))
def test_immediate_durable_fence_and_purge(stores, service, reason):
    open_store, paths, _ = stores
    repo = open_store(service)
    item, survivor = resource(), resource(owner=OTHER)
    repo.save(item)
    repo.save(survivor)
    binary = b"SYNTHETIC_NONVOICE_BYTES"
    if service in ("artifacts", "ai"):
        for kind in (("sample", "generated", "joined_preview") if service == "artifacts"
                     else ("embedding", "model_material", "reconstructive_cache")):
            repo.store_bytes(item["id"], kind, binary)
        assert any(p.is_file() for p in paths[service].rglob("*"))
        assert repo.read_bytes(principal(), item["id"], now=NOW) == [binary] * 3
    assert repo.read(principal(), item["id"], now=NOW) == item
    assert repo.assert_usable(OWNER, PROFILE, CONSENT, now=NOW) is None
    cleanup = repo.fence(principal(), profile_id=PROFILE, consent_id=CONSENT,
                         reason=reason, now=NOW, cleanup_window_seconds=86400)
    assert cleanup["status"] == "pending"
    assert cleanup["deadline_at"] == NOW + timedelta(seconds=86400)
    denied(lambda: repo.read(principal(), item["id"], now=NOW), "CONSENT_REVOKED")
    denied(lambda: repo.assert_usable(OWNER, PROFILE, CONSENT, now=NOW), "CONSENT_REVOKED")
    if service in ("artifacts", "ai"):
        denied(lambda: repo.read_bytes(principal(), item["id"], now=NOW), "CONSENT_REVOKED")
        denied(lambda: repo.store_bytes(item["id"], "late_result", binary), "CONSENT_REVOKED")
    assert repo.read(principal(OTHER), survivor["id"], now=NOW) == survivor
    repo.close()
    reopened = open_store(service)
    denied(lambda: reopened.assert_usable(OWNER, PROFILE, CONSENT, now=NOW), "CONSENT_REVOKED")
    assert reopened.fence(principal(), profile_id=PROFILE, consent_id=CONSENT,
                          reason=reason, now=NOW + timedelta(hours=1),
                          cleanup_window_seconds=86400) == cleanup
    result = reopened.purge(cleanup["cleanup_id"], now=cleanup["deadline_at"])
    assert result["status"] == "completed" and result["completed_at"] == cleanup["deadline_at"]
    assert reopened.purge(cleanup["cleanup_id"], now=cleanup["deadline_at"]) == result
    assert reopened.inspect_private(item["id"]) is None
    denied(lambda: reopened.read(principal(), item["id"], now=cleanup["deadline_at"]), "NOT_FOUND")
    assert reopened.read(principal(OTHER), survivor["id"], now=cleanup["deadline_at"]) == survivor
    if service in ("artifacts", "ai"):
        assert not any(p.is_file() for p in paths[service].rglob("*"))
    assert reopened.cleanup(principal(), cleanup["cleanup_id"]) == result
    denied(lambda: reopened.cleanup(principal(OTHER), cleanup["cleanup_id"]), "FORBIDDEN")
    metadata = reopened.deletion_metadata(cleanup["cleanup_id"])
    assert metadata == {"owner_id": OWNER, "actor_id": OWNER, "occurred_at": NOW,
                        "resource_id": PROFILE, "type": reason}


@pytest.mark.integration
def test_cleanup_failure_never_restores_access_or_moves_deadline(stores, monkeypatch):
    open_store, _, _ = stores
    repo = open_store("artifacts")
    item = resource()
    repo.save(item)
    repo.store_bytes(item["id"], "sample", b"synthetic")
    assert repo.read_bytes(principal(), item["id"], now=NOW) == [b"synthetic"]
    cleanup = repo.fence(principal(), profile_id=PROFILE, consent_id=CONSENT,
                         reason="profile_deleted", now=NOW, cleanup_window_seconds=3600)
    assert cleanup["deadline_at"] == NOW + timedelta(seconds=3600)
    unlink = Path.unlink

    def unavailable(path, *args, **kwargs):
        raise OSError("synthetic storage unavailable")

    with monkeypatch.context() as patch:
        patch.setattr(Path, "unlink", unavailable)
        failed = repo.purge(cleanup["cleanup_id"], now=NOW)
    assert failed["status"] == "failed" and failed["failure"]["code"] == "DEPENDENCY_UNAVAILABLE"
    assert failed["deadline_at"] == cleanup["deadline_at"]
    denied(lambda: repo.read_bytes(principal(), item["id"], now=NOW), "CONSENT_REVOKED")
    assert Path.unlink is unlink
    completed = repo.purge(cleanup["cleanup_id"], now=cleanup["deadline_at"])
    assert completed["status"] == "completed"
    assert completed["deadline_at"] == cleanup["deadline_at"]


@pytest.mark.integration
def test_audit_metadata_has_independent_bounded_retention(stores):
    open_store, _, _ = stores
    audit = open_store("audit")
    event = {"event_id": uid(), "owner_id": OWNER, "actor_id": OWNER,
             "occurred_at": NOW, "resource_id": PROFILE, "type": "profile_deleted", "outcome": "accepted"}
    audit.append(event)
    assert audit.events(principal(ADMIN, "Administrator"), now=NOW) == [event]
    denied(lambda: audit.events(principal(), now=NOW), "FORBIDDEN")
    denied(lambda: audit.append(dict(event, event_id=uid(), script="private")), "INVALID_INPUT")
    audit.expire(audit_days=12, now=NOW + timedelta(days=12) - timedelta(microseconds=1))
    assert audit.events(principal(ADMIN, "Administrator"), now=NOW) == [event]
    audit.expire(audit_days=12, now=NOW + timedelta(days=12))
    assert audit.events(principal(ADMIN, "Administrator"), now=NOW + timedelta(days=12)) == []
```

## Internal Interface Proposal for Review

These interfaces are new technical proposals for this layer; they are not previously approved architecture or new public APIs. Production modules are deliberately absent. The complete calls above determine exact parameter names. Constructors on the eight separate classes are `Class(*, database: dict, root: Path, authorize: callable | None)`. Each owns only its database/root; no constructor receives another owner's credentials. `initialize() -> None` creates/migrates only that owner's schema in GREEN; `effective_target() -> dict` reports actual opened connection/path, not a copy of requested settings; `close() -> None` is idempotent. A later GREEN plan must give exact schema/migration/recovery code before execution.

| Owner classes / signatures | Meaning and result |
| --- | --- |
| ConsentRepository, ProfileRepository, HistoryRepository, ArtifactRepository, ConditioningRepository: `save(record: dict) -> None`; `read(actor: dict, resource_id: str, *, now: datetime) -> dict`; `list(actor: dict, *, owner_id: str, now: datetime) -> list[dict]` | Trusted owner-local persistence operations; save is not a public consent/enrollment/admission bypass. Input test records are internal synthetic records with exact fields shown in resource(), not HTTP DTOs. Durable owner-scoped retrieval returns saved content; errors expose no payload. |
| Same five: `assert_usable(owner_id: str, profile_id: str, consent_id: str, *, now: datetime) -> None`; `fence(actor: dict, *, profile_id: str, consent_id: str, reason: str, now: datetime, cleanup_window_seconds: int) -> dict` | Per-owner durable revocation gate. All matching records of this actor/owner are inaccessible synchronously before fence returns. Usable checks gate storage/inference/publication adapters later; they do not perform synthesis. Fence returns Cleanup with cleanup_id/status/requested_at/deadline_at/completed_at/failure per approved schema. First request fixes identity/time/deadline; repeated request returns same record. Local test reasons profile_deleted/consent_revoked/sample_expired label the approved triggers, not new contract enum values. |
| Same five: `cleanup(actor: dict, cleanup_id: str) -> dict`; `purge(cleanup_id: str, *, now: datetime) -> dict`; `inspect_private(resource_id: str) -> dict | None`; `deletion_metadata(cleanup_id: str) -> dict` | Owner-only status; trusted cleanup worker operation physically removes owned private records/bytes. inspect_private is owner-local diagnostic retrieval, never externally routed, used to distinguish physical deletion from read filtering. Only exact five metadata fields asserted remain in deletion_metadata; no script, consent text, voice bytes, embedding or private payload. Audit owns retention of exported metadata. |
| ConsentRepository, ProfileRepository, ArtifactRepository: `apply_retention(policy: dict, *, now: datetime) -> None`; `expiry(resource_id: str) -> datetime` | Apply current owner policy, recompute from creation, evaluate at explicit UTC time; no wall-clock sleeps. Profile/consent/sample expiration fences; generated/preview expiration affects audio only. |
| ArtifactRepository, ConditioningRepository: `store_bytes(resource_id: str, kind: str, data: bytes) -> None`; `read_bytes(actor: dict, resource_id: str, *, now: datetime) -> list[bytes]` | Trusted owner-local bytes, physically under the effective isolated root, writes denied after fence. Synthetic kinds enumerate required purge classes, not new Artifact.kind schema values. No filesystem/storage key returned through external API. |
| GrantRepository: `save_grant(actor: dict, grant: dict, *, now: datetime) -> None`; `revoke_grant(actor: dict, grant_id: str, *, now: datetime) -> dict`; `authorize(actor: dict, owner_id: str, scope: str, *, now: datetime) -> bool` | Owner alone grants/revokes; exact live owner/admin/role/scope/expiry/revocation comparison. Revocation preserves first timestamp. Private repositories call authorize for nonowner reads on every operation. AI materials have no public grant scope and remain unavailable to administrators. |
| RetentionRepository: `configure(actor: dict, values: dict, *, now: datetime) -> dict`; `current() -> dict`; `policy_events() -> list[dict]` | Retention subsection only, not whole Configuration replacement/revision semantics. Administrator-only atomic update with required nondefault durations, defaults 30/86400, exact before/after audit once per successful change; rejected update leaves no event. |
| AuditRepository: `append(event: dict) -> None`; `events(actor: dict, *, now: datetime) -> list[dict]`; `expire(*, audit_days: int, now: datetime) -> None` | Metadata-only append and authorized administration; no private content fields. Expiry from occurred_at exactly at boundary. No public deletion/update method; configured expiration is the allowed removal path. |

All repository errors have type name PersistenceError and `.code: str`; their safe string representation contains no private payload. Error classes may be owner-local. Python datetime values are aware UTC; IDs are exact canonical lowercase UUID strings, roles exact User/Administrator. Validated trusted actor comes from Auth in production. The local test authorization callback is an explicit substitute for the service boundary, not a mocked authorization answer: real Auth repository evaluates its own live database. Production must use authenticated Auth HTTP/consumer boundaries and cannot share these databases. No reusable central repository class, privileged shared connection or cross-owner SQL is proposed. Additional internal implementation details require the GREEN review.

## Contract Rule Coverage and Ownership

Names below refer to exact test functions; parametrization is part of coverage. This map covers every normative rule of the approved contract relevant to this milestone's owned persistence concerns. Deferred rules are explicit, never claimed passing.

| Normative rule / approved requirement | This RED evidence / boundary |
| --- | --- |
| Strict owner isolation of private consent/profile/sample/history/materials; role alone no access; owner lists; foreign generic403, unknown404; no private echo; R-ACCT-002/003, FR-004 | test_owner_isolation_survives_reopen across five owners, positive read/list before negative cases, saved foreign fixture, reopened connection. Repository codes FORBIDDEN/NOT_FOUND; HTTP status/body/auth-before-lookup transport verified later Security & Nine-Service Integration. Accounts authentication/credential isolation owned Authentication & Consent, not implemented here. |
| Explicit live scoped expiring administrator grant; owner alone grant/revoke; exact role/admin/owner/scope matching; repeat revoke timestamp | test_live_scoped_admin_grants across all public private-read owners; positive granted read/list followed by wrong principal/role/owner/scope, exact-expiry and revoked denials. Full grant HTTP schema, target-account existence, future-expiry validation, immutable request fields and registration/token rules belong Authentication & Consent RED. AI private materials have no administrator scope. |
| Canonical IDs/exact role matching/no coercive identity comparison | test_owner_isolation_survives_reopen rejects leading-space identity and wrong-case Administrator. Canonical authentication IDs themselves and malformed public UUID parsing/400 mapping belong Authentication & Consent and Security integration. No email-based ownership comparison. |
| Separate configurable profiles/samples/generated/consent/audit policies; administrator config; default generated30 and cleanup86400, other durations required; positive integer durations; R-RET-001/002 | test_retention_defaults_required_values_and_audit verifies exact defaults, required nondefaults, invalid durations, nonadmin denial, persisted reopen, custom audio/cleanup bounds and only successful before/after events. Full Configuration revision/concurrency/other sections are Job Orchestration & Idempotency and Security integration; no configuration DTO added here. |
| Day86400; expiry from creation/event; joined preview generated policy; shortened policies recompute/fence immediately; profile/consent/sample expiry revokes while generated expiry audio only | test_retention_expiry_and_shortening for five service/category pairs with exact before/at boundary and post-shortening checks; test_audit_metadata_has_independent_bounded_retention for occurrence-based audit expiry. Cross-owner propagation/current remote authorization belongs later integration; per-owner fences are exercised below. |
| Deletion/revocation immediately fences synthesis/retrieval, event delay cannot restore access; R-REV-001, FR-003 | test_immediate_durable_fence_and_purge for five owners and three triggers; positive reads/usability/bytes first, same-instant negative checks, durable reopen, late result rejection. Auth grant cannot override revocation; production fence transport/admission checks belong Security integration and Job orchestration. No generation engine is claimed tested. |
| Asynchronous cleanup with default/custom deadline, status visibility, owner-only cleanup read, repeat tombstone same Cleanup; failure never restores access/extends deadline | test_immediate_durable_fence_and_purge and test_cleanup_failure_never_restores_access_or_moves_deadline. No tombstone-expiration policy is specified by contract: retained repeat is tested; removal-after-tombstone404 is deferred until a GREEN design proposes lifecycle without inventing retention. HTTP202 and real transport are later integration checks. |
| Physical purge profile metadata, original samples, generated and joined audio, model/embedding material, reconstructive caches; associated private history; only permitted metadata retained; R-DEL-001 | test_immediate_durable_fence_and_purge checks storage-owner record absence, actual files absent, owner-scoped survivor unchanged and exact safe deletion metadata. Purge is idempotent across reopen. Test uses synthetic nonvoice bytes; model-specific stores covered later Real-Model Inference Integration with selected-model prerequisites. Local downloaded copies outside server purge per Q1 are not server-owned and are excluded. |
| Cleanup bounded retries/visible dependency failure | test_cleanup_failure_never_restores_access_or_moves_deadline injects filesystem unlink failure, visible failed result and recovery within original deadline. Scheduling/backoff/exhaustion, events/outbox/deduplication and cross-service partial failure transport remain Security integration; no scheduler or broker implemented here. |
| Audit separate policy; metadata only, no private payload; administrator query; consent/audit not indefinite | test_audit_metadata_has_independent_bounded_retention permits an exact deletion Audit event, rejects extra script, proves positive authorized query then nonadmin denial and before/at expiry. Consent creation/immutability/events owned Authentication & Consent. Audit list paging/filter/timeline transport and event ingestion belong Security integration. |
| Artifact access live fence; private paths not exposed; generated expiry does not revive profile, no late publication | Owner reads/bytes and gate tests above exercise persistent decisions. Signed link cryptography/principal binding/format/disposition/range/content types/HTTP errors, deployed encryption/managed secrets/IAM and real-service authorization uncertainty503 belong Security & Nine-Service Integration. No local test establishes deployed acceptance. |
| Contract list stable ordering/cursor snapshot/authenticated filters; JSON/type/null/unknown parsing; transport schemas/numbers/versions; jobs/idempotency/quota/state/chunks; enrollment/audio/model gates | Not asserted here: list is owner-local minimum persistence retrieval, not Page or public schema. These transport and distinct lifecycle concerns remain their Plan-owned Authentication, Enrollment, Job, Inference, Security and Frontend REDs. Minimal synthetic records do not define public DTOs or claim workflow validation. |

## Execution Steps

After human approval only: inspect predecessors/branch/status; preserve existing edits; create exactly tests/test_persistence.py from the complete block. Do not create intended modules or migrations. Use already approved prerequisites and Docker engine; unavailable dependencies/configuration stop execution. Run the exact capability suite twice, without manual state cleanup between runs; record full failing node IDs, exception classes and causal traces. Missing intended modules/classes/methods are valid RED only after fixture prerequisites succeed. Never skip, xfail, loosen assertions or add production stubs to turn environment failures into RED. Stop after reviewed evidence and permitted PDD bookkeeping. No GREEN, publishing, commit or push authorized here.

## Acceptance / Completion Criteria

Only the one proposed test file changes apart from PDD execution bookkeeping. Complete code matches the approved block, all expected parameter cases collect, fixtures verify effective isolation, and both invocations yield behavior-attributable RED (not no-tests, syntax/import-dependency, Docker, credentials, permissions or configuration failure). Intended missing voice_narration owner module/class is behavior-attributable; missing pytest/Psycopg is not. No test is required to pass while its intended production boundary is absent; there are no preserved application tests assigned to this milestone. Every owned requirement has the mapped positive-before-negative failing surface above. Container/roles/databases/files are isolated and torn down by fixtures, no model/private sample/paid resource acquired, original branch and unrelated edits preserved. The exact future GREEN target remains reviewed, with no production code applied by RED.

## Verification

### Commands

Run from repository root with already-approved installed prerequisites and available Docker engine:

```powershell
git branch --show-current
git status --short
git diff --check
git diff --exit-code HEAD -- requirements-dev.txt pytest.ini compose.harness.yaml containers/harness.Dockerfile .dockerignore .gitignore tools/readiness.py docs/developer-setup.md .github/workflows/harness.yml
.\.venv\Scripts\python.exe -m pytest tests/test_persistence.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest tests/test_persistence.py -ra --tb=short
git status --short
```

The two pytest commands are separate commands even when the first fails; retain both exit codes/output. Linux uses `.venv/bin/python` for these same invocations. Fixtures allocate fresh per-case targets on each invocation, no manual cleaning. The existing Compose definition and pins are reused unchanged. Expected repository branch codex/foundation-harness; foundation preservation diff exit0. This persistence suite itself checks real PostgreSQL/isolation before lazy intended production imports, so no redundant browser/audio/readiness process is needed for this capability. If Docker is unavailable, use approved developer setup only to restore the existing prerequisite; changing/reinstalling infrastructure requires review, not a contingency here.

### Expected Evidence

Expected / Predicted — Not Yet Verified: collected parametrized tests fail because intended owner persistence modules/classes are absent. A representative predicted error is ModuleNotFoundError for voice_narration (or its owner persistence module); the accepted failure class is missing approved behavior, not a mandated exact trace. All fixture prerequisite assertions must have passed first, and teardown must complete. After GREEN the same tests must pass; any unexpectedly passing owned behavior needs traceability review, not automatic RED credit. Preserved-behavior tests expected to pass at RED: none. No empty-suite success, skipped case or environment failure counts.

### Planning-Time Dry Run

No disposable runtime dry run was performed. The exact suite requires a running Docker Linux engine/isolated PostgreSQL; Docker was stopped after the completed FOUNDATION and this documentation-only task authorizes no processes/containers. A disposable copy would still require those processes and cannot manufacture completed GREEN modules. No model/runtime installation, readiness rerun or test execution occurred. Static AST/document checks can verify syntax and exact-code completeness without importing proposed modules, connecting a database or writing tests. Their actual result is recorded in the per-file review below; static checks are not RED or runtime evidence. No application baseline suite exists, so no pre-existing test failure was observed or waived.

## Risks

Identity comparisons: owner in saved record versus authenticated actor.user_id; list requested owner versus actor; grant.owner_id versus requested owner; grant.administrator_id versus actor; actor.role versus exact Administrator; scope versus exact requested read scope; resource/profile/consent links versus cleanup owner; cleanup owner versus status reader; policy/audit actor.role versus Administrator. All use canonical lowercase UUID strings/exact enum strings produced by Auth, never email, display name, case-folded role, trimmed UUID or user-supplied ownership assertion. The boundary rejects a noncanonical identity rather than normalizing one differently from authentication. Grant expiration/revocation compare aware UTC time on each read; exact expiry denies. No admin mutation/purge grant is inferred from read grants. Trusted setup save/inspect methods must stay owner-local and never become public authorization bypasses.

The test authorization callable crosses an explicit test boundary and invokes real owner-local Auth logic; it is not production permission to read Auth SQL. Immediate cross-service revocation under delay/races and uncertain authorization remain unproved until integration. This suite drives each owner's local durable gate; later adapters must consult current owner state synchronously before inference/publication/retrieval. Generic-shaped synthetic records are test inputs to distinct owner repositories, not a central schema/shared privileged library. Owner-specific schemas and migrations require a later GREEN plan. Internal local-root bytes cannot prove cloud/object/model adapter purge or deployed security. Filesystem failure injection pins the selected local adapter to Path.unlink; another adapter requires review, not silently weakened evidence. The full suite is bounded but creates eight temporary databases per case; no production load/latency target follows from that choice.

## Pre-authorized Contingencies

None. Unexpected environment/configuration failures, required new infrastructure, changed module/signature/schema decisions or unrelated failing baseline checks return to planning/review. No fallback SQLite, skips, test weakening, new packages or production scaffolding.

## Rollback / Recovery

Before execution tests/test_persistence.py must be absent; if it exists, stop and inspect instead of overwriting. Rollback removes only that created file after preserving any execution evidence. Fixture finally blocks close connections and remove only case-owned databases/roles and the random Compose project. On interruption inspect the printed project/container label and use the existing developer-setup recovery guidance for that exact project; never broad docker cleanup, repository reset/clean or shared-database deletion. pytest tmp_path owns test files; no private content is placed there.

## Explicitly Out of Scope

Any production module/class/stub/schema/migration; build/runtime/test infrastructure/config/dependency changes; global conftest or test plugins; HTTP routes/service bootstraps; authentication/token/enrollment implementations; distributed broker/admission/worker scheduling; model acquisition/inference/commercial sign-off; deployed acceptance; changes to approved scope/ownership; additional agents; commit/push/publish; approving this plan or starting GREEN.

## Exact-Code and Authority Review

| File | Review |
| --- | --- |
| tests/test_persistence.py | Complete final content in one Python block; no placeholder, pseudocode or partial diff. Matches all three Proposed Changes. Imports are stdlib plus existing pytest/Psycopg from 001; Compose paths/project credentials/ports follow approved harness isolation. Module/class/signature and synthetic schema choices are explicit review proposals above, not new dependencies/settings. No executable file is written during planning. |

No new requirement, milestone or normative contract identifier is introduced. Python function names, service-local module names and synthetic kind/reason labels identify tests/internal proposals and do not redefine existing R-/FR-/AC- authority labels. Human review is the only status field in this artifact.

Actual planning checks on 2026-10-24: the existing .venv Python parsed the sole proposed Python block with ast.parse without importing or executing it: PASS, seven test functions, 355 proposed source lines, zero Ellipsis nodes. Document checks found four balanced fence lines (Python plus PowerShell), zero template comments, zero trailing-whitespace lines and one Status field. git diff --check returned exit0 with only pre-existing 001/Plan LF-to-CRLF notices. The exact nine-file foundation preservation diff returned no output/exit0. git status --short showed only the pre-existing modified 001/Plan, untracked 002/model-eval and this new 003. No test/source/configuration file, tempfile, installed package, background process or container was created by planning. These are static/scope observations, not completed RED evidence or approval.

## Human Review

Status: Approved by avinash2196 on 2026-10-24 (recorded 2026-10-25T02:17:55Z), in response to review of this specific plan. Execution stopped at a blocker — see Plan.md. Re-approval required before execution.

