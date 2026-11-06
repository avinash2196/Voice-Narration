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
