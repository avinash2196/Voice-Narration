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
