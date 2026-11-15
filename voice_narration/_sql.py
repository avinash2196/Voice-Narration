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
