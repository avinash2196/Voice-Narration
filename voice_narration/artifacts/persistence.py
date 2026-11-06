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

    def publish_sample(self, record, data, *, validate):
        if record.get("category") != "sample" or not isinstance(data, bytes) or not data or not callable(validate):
            fail("INVALID_INPUT")
        created = False
        try:
            with self.transaction():
                validate()
                self.save(record)
                created = True
                self.store_bytes(record["id"], "original", data)
                validate()
        except BaseException:
            if created:
                self._erase(record["id"])
            raise

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
