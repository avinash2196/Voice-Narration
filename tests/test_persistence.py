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
