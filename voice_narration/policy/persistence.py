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
