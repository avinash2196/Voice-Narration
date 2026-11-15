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
