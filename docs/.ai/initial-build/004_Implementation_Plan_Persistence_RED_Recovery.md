# Implementation Plan — Persistence & Storage RED recovery revision

## Milestone

Persistence & Storage RED, milestone 4 of initial-build.

## Milestone Type

RED. Proposed tests only; this document does not implement or execute them.

## Authoritative References

Paths are repository-relative unless prefixed with the installed plugin root.

| Read document | Authority / disposition |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved by avinash2196 2026-10-19; retained P0 and Q5–Q10 clarifications approved 2026-10-24. |
| docs/.ai/initial-build/Plan.md | Revised Plan approved 2026-10-24. CONTRACT, FOUNDATION and assessment Complete; Persistence RED Blocked after 003 execution; not Complete. Owns unchanged milestone scope and traceability. This recovery requires approval and a Plan disposition permitting retry before execution. |
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

001 fixes CPython 3.13.17, pytest 9.1.1 with no test-plugin use, HTTPX 0.28.1, Psycopg binary 3.3.6 and real PostgreSQL 18.6. Preserve all pinned prerequisites, existing Compose and pytest configuration. The exact retry commands below add `-p no:anyio`; this is a command-only revision requiring this review, not a dependency change. Use stdlib plus existing pytest/Psycopg only; no dependency, runtime, build or infrastructure change. Function-local capability fixtures belong to the proposed test file, not global conftest. Each case gets fresh service databases/credentials and tmp_path roots; verify effective targets. No SQLite substitute, shared development database, paid resource, model loader or audio download.

Nine owners remain Auth, Consent, Voices, Jobs, Artifact, Policy, AI, Worker, Audit. Separate owner databases and credentials are mandatory. Test orchestration is not a new production service or central privileged persistence facade. Worker has no independent durable private library here; its future temporary outputs remain covered by Artifact/AI storage boundaries and later integration tests.

## Preconditions / Predecessor Evidence

Plan.md Execution Status and its FOUNDATION evidence record exact nine delivered prerequisite files, successful Windows two-pass readiness, cleanup and real Linux CI run 40132442843 at commit 0fe8c317ffba011ec1e880d7d6d5af93b6b40d5a. Assessment evidence records four reviewed documents and actual investigation/protocol decisions. No production model approval is needed for nonvoice bytes and synthetic metadata.

003 was approved and executed only through its first verification invocation, then stopped. Plan.md records 33 collected setup errors in Compose up/down before identity/isolation assertions or intended imports; no valid RED and no second run. Its helper captures stderr but the displayed exception omits it. The Compose cause is unknown. Permission denial is an observed separate Docker probe result and only a hypothesis for the pytest failure. Cleanup found no exact-project resources and stopped Docker Desktop. Preserve 003 and its stopped history.

## Current Repository State

The existing tests/test_persistence.py exactly matches 003's 355-line block (recorded SHA256 516c394b74651c9ba7095a6bc4c9638eea04a10b5b7ddc7fe30a307574b3691e); it is the baseline, not a new file to overwrite. Production modules remain absent. Branch codex/foundation-harness and unrelated documentation edits are preserved. No approved unexecuted replacement exists. This document is retry planning for milestone 4, not an additional milestone.

Read-only metadata inspection found the sole pytest11 entrypoint `anyio -> anyio.pytest_plugin` from anyio4.15.1 in the project .venv. HTTPX0.28.1 installed metadata declares `anyio`; the approved FOUNDATION resolved inventory already includes anyio4.15.1 (Plan.md). Thus the package is an approved transitive prerequisite, while plugin auto-loading conflicts with 001/003 no-plugin use wording. Proposed explicit `-p no:anyio` disables that entrypoint for these synchronous tests without uninstalling/changing any dependency. No evidence connects it to Compose failure. An additional entrypoint discovered at execution stops for review; do not silently disable it.

## Files in Scope / Proposed Changes

Create no executable files. Modify only tests/test_persistence.py, with its complete final content below. The sole source change is the run helper: preserve subprocess arguments/check/timeout and CalledProcessError, print captured stdout/stderr before re-raising, redact the exact HARNESS_DB_PASSWORD from printed text. Every test, assertion, fixture setup/teardown and repository signature remains byte-for-byte equivalent outside that helper. Both setup and teardown diagnostics remain visible even when finally replaces the primary exception. No connection/env dump is authorized. Plan.md execution bookkeeping and this document's execution status are separate permitted PDD records.

All 003 behavior decisions, rule coverage, signatures and exclusions carried below remain approved inputs. Only diagnostic handling and exact execution commands are revised. No production, dependency, framework, plugin version, configuration, schema, migration or milestone is introduced.

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
    try:
        return subprocess.run(
            args, cwd=ROOT, env=env, check=True, capture_output=True,
            text=True, timeout=180,
        ).stdout.strip()
    except subprocess.CalledProcessError as error:
        password = (env or {}).get("HARNESS_DB_PASSWORD", "")
        for label, output in (("stdout", error.stdout), ("stderr", error.stderr)):
            diagnostic = output or "<empty>"
            if password:
                diagnostic = diagnostic.replace(password, "<redacted>")
            print(f"subprocess {label}: {diagnostic}", flush=True)
        raise


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

These interfaces carry forward the approved 003 technical proposals for this layer unchanged; they are not new public APIs. Production modules are deliberately absent. The complete calls above determine exact parameter names. Constructors on the eight separate classes are `Class(*, database: dict, root: Path, authorize: callable | None)`. Each owns only its database/root; no constructor receives another owner's credentials. `initialize() -> None` creates/migrates only that owner's schema in GREEN; `effective_target() -> dict` reports actual opened connection/path, not a copy of requested settings; `close() -> None` is idempotent. A later GREEN plan must give exact schema/migration/recovery code before execution.

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

## Execution Steps and Verification

After human approval of this exact recovery and Plan.md disposition authorizing retry only: verify branch/status and baseline test block against 003, preserve unrelated edits, apply the sole helper change from the complete block, and inspect that assertions are unchanged. Preserve the nine foundation files with the exact command below. No install or rebuild is authorized.

Run these read-only diagnostics from the repository root in the same host execution context that will run pytest; record actual output and exit codes:

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

Required pins remain Python3.13.17, pytest9.1.1, Docker29.3.1, Compose5.6.0 and PostgreSQL18.6 from 001. Docker engine stopped is not test failure: start only the already-installed approved Desktop with the following exact hidden launch, then repeat the Docker diagnostics once after readiness. Do not install or alter settings.

```powershell
Start-Process -FilePath 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -WindowStyle Hidden
```

If any diagnostic fails for another cause, stop with output. If and only if Docker diagnostics explicitly say permission/access denied to dockerDesktopLinuxEngine, request/use the approved host execution facility for the same diagnostic commands and both exact pytest commands, with repository cwd unchanged; no environment or code alteration. This is a reviewed host execution contingency, not evidence that permissions caused 003. Automatic review can still reject execution; report that rejection and stop. If host diagnostics succeed but fixture Compose fails, stop after the first suite with now-visible diagnostics; do not rerun until it happens to pass.

Run separately, with no manual cleanup between invocations:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
```

The second run is authorized only when first-run failures are attributable to missing intended behavior and fixture teardown succeeds. An environment/configuration/dependency failure stops execution for review. Record both runs' actual failures and exit codes; Linux equivalent uses `.venv/bin/python` with identical arguments. No environment variable is added/removed for pytest; HARNESS_DB_PASSWORD remains fixture-local as before. Do not use PYTEST_DISABLE_PLUGIN_AUTOLOAD or change pytest.ini. Inspect header to verify anyio plugin absent; synchronous suite requires no plugin. Final status/scope checks use the first four git commands above. Stop only the Desktop runtime started by this execution using `docker desktop stop`; verify `docker desktop status`. Inspect any failed cleanup by its printed random project; cleanup only that exact project using its existing fixture command with its original environment, never global prune.

## Acceptance / Completion Criteria

Only the existing test file's helper changes, apart from PDD bookkeeping; all 33 cases and every original assertion remain. Foundation preservation diff exits0. Effective PostgreSQL version/identity/loopback/dynamic ports/service isolation assertions and teardown succeed on both runs before accepting missing approved owner modules/classes as RED. Both runs show behavior-attributable RED, with no unrelated errors/skips/xfails or suppressed assertions. Anyio entrypoint is disabled explicitly only in these commands; approved packages remain untouched. Unknown Compose causes and failed prerequisites do not count as RED. No valid RED exists until executed evidence supports these criteria; GREEN remains unauthorized.

### Expected / Predicted — Not Yet Verified

33 cases collect; fixture succeeds and intended voice_narration imports/classes fail because approved persistence behavior is absent. Repeated isolated evidence and cleanup are required. This is a prediction; diagnostics may instead expose another prerequisite blocker and require replanning. No assertion is relaxed if it fails.

### Planning-Time Dry Run and Actual Read-Only Findings

No pytest/Compose rerun, Docker launch, install, runtime/configuration/test mutation or disposable runtime probe was performed during recovery planning, as explicitly prohibited by this task. Consequently soundness with a scratch implementation and runtime recovery are not verified. Static parsing/exact assertion preservation results are recorded below and are not milestone evidence. The existing stopped first run is an in-scope prerequisite blocker, not a waived passing baseline or accepted RED. No unrelated pre-existing test failure has been established.

Actual read-only metadata command: `.\.venv\Scripts\python.exe -c "import importlib.metadata as m; print('pytest11:', [(p.name,p.value,p.dist.name,p.dist.version) for p in m.entry_points(group='pytest11')]); print('httpx requirements:', m.requires('httpx')); print('anyio requirements:', m.requires('anyio'))"`. Output establishes sole entrypoint anyio/anyio.pytest_plugin/anyio4.15.1 and HTTPX requirement anyio. No causal inference about Docker follows.

## Risks

Identity comparisons: owner in saved record versus authenticated actor.user_id; list requested owner versus actor; grant.owner_id versus requested owner; grant.administrator_id versus actor; actor.role versus exact Administrator; scope versus exact requested read scope; resource/profile/consent links versus cleanup owner; cleanup owner versus status reader; policy/audit actor.role versus Administrator. All use canonical lowercase UUID strings/exact enum strings produced by Auth, never email, display name, case-folded role, trimmed UUID or user-supplied ownership assertion. The boundary rejects a noncanonical identity rather than normalizing one differently from authentication. Grant expiration/revocation compare aware UTC time on each read; exact expiry denies. No admin mutation/purge grant is inferred from read grants. Trusted setup save/inspect methods must stay owner-local and never become public authorization bypasses.

The test authorization callable crosses an explicit test boundary and invokes real owner-local Auth logic; it is not production permission to read Auth SQL. Immediate cross-service revocation under delay/races and uncertain authorization remain unproved until integration. This suite drives each owner's local durable gate; later adapters must consult current owner state synchronously before inference/publication/retrieval. Generic-shaped synthetic records are test inputs to distinct owner repositories, not a central schema/shared privileged library. Owner-specific schemas and migrations require a later GREEN plan. Internal local-root bytes cannot prove cloud/object/model adapter purge or deployed security. Filesystem failure injection pins the selected local adapter to Path.unlink; another adapter requires review, not silently weakened evidence. The full suite is bounded but creates eight temporary databases per case; no production load/latency target follows from that choice.

## Pre-authorized Contingencies

Only the exact permission-denial host execution contingency described above: observable Docker API access-denied diagnostic; no file change; same diagnostic/pytest commands and cwd on approved host facility. Existing stopped Desktop may be started by the exact hidden command above. No dependency installation, environment rewrite, assertions/configuration change, alternative database or automatic extra retry is authorized. Record triggers and application explicitly. Other blockers stop for review.

## Rollback / Recovery

Restore only the helper to its exact 003 block if this retry is abandoned, preserving the existing tests and stopped history. Do not remove the baseline test file. Inspect/clean only fixture-owned random Compose projects and temporary per-case resources; no broad reset/clean/prune. Preserve evidence and unrelated documentation edits.

## Explicitly Out of Scope

Any production module/class/stub/schema/migration; build/runtime/test infrastructure/config/dependency changes; global conftest or additional test plugins; HTTP routes/service bootstraps; authentication/token/enrollment implementations; distributed broker/admission/worker scheduling; model acquisition/inference/commercial sign-off; deployed acceptance; changes to approved scope/ownership; additional agents; commit/push/publish; approving this plan or starting GREEN.

## Exact-Code and Authority Review

| File | Review |
| --- | --- |
| tests/test_persistence.py | Complete final Python content above; no pseudocode/placeholders/Ellipsis; only helper diagnostics change. All original assertion ASTs/test nodes preserved. Uses existing stdlib subprocess and pytest/Psycopg only. No new dependency/configuration setting; `-p no:anyio` is the exact reviewed command-only suppression of an already-installed transitive entrypoint. |

No requirement, milestone or normative identifier is introduced/reused. This is 004, the next document number, replacing 003 for retry execution only while preserving 003 history. Authoritative additional input: 003 approved/stopped plan, existing tests/test_persistence.py, Plan.md stopped evidence and read-only installed dependency metadata. All other previously read references and their dispositions remain as listed above.

Actual recovery planning checks: proposed Python parsed with ast.parse; seven test functions, zero Ellipsis nodes, every original assertion AST identical. git diff --check exited0 with existing 001/Plan LF-to-CRLF notices only; exact nine-file foundation preservation diff exited0 with no output. Status inspection showed this new004 plus existing documentation/tests changes. No executable file was changed and no test/runtime probe ran.

## Human Review

Status: Approved by avinash2196 on 2026-10-24 (recorded 2026-10-25T02:26:04Z), in response to review of this exact recovery plan and retry disposition. RED retry only; GREEN remains unauthorized.

Execution status: Executed and verified RED on 2026-10-24. Exact helper applied; all original assertions preserved. Both exact pytest invocations produced 33 intended missing-production-module failures with successful real PostgreSQL fixtures and teardown; no unrelated failures, passing cases, skips or xfails. See Plan.md recovery 004 execution evidence and 004-red-run2.txt. This records execution, not a new approval; GREEN remains unauthorized.
