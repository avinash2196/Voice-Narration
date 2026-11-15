"""Authentication and consent boundaries, synthetic identities, real HTTP and SQL."""
from contextlib import contextmanager
from datetime import timedelta
import importlib
import socket
import threading
import time

import httpx
import pytest
import uvicorn

from test_persistence import NOW, principal, postgres, stores, uid


AUTH = {"access_token_seconds": 120, "verification_token_seconds": 300,
        "signed_link_seconds": 60, "password_min_characters": 8,
        "password_max_characters": 80}
PASSWORD = "  Synthetic password  "
ADMIN_PASSWORD = "Synthetic administrator password"


def timestamp(value):
    return value.isoformat().replace("+00:00", "Z")


def error(response, status, code):
    assert response.status_code == status, response.text
    body = response.json()
    assert set(body) == {"error"}
    assert set(body["error"]) == {"code", "message", "details", "request_id", "timestamp"}
    assert body["error"]["code"] == code
    assert isinstance(body["error"]["message"], str) and body["error"]["message"].strip()
    assert isinstance(body["error"]["details"], list)
    from voice_narration._sql import identity
    identity(body["error"]["request_id"])
    assert body["error"]["timestamp"].endswith("Z")


@contextmanager
def serve(app):
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen(128)
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", lifespan="off"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started, "ASGI server did not start"
        with httpx.Client(base_url=f"http://127.0.0.1:{sock.getsockname()[1]}/api/v1",
                          timeout=10, trust_env=False) as client:
            yield client
    finally:
        server.should_exit = True
        thread.join(10)
        sock.close()
        assert not thread.is_alive(), "HTTP server teardown incomplete"


@pytest.fixture
def system(stores):
    open_store, paths, targets = stores
    grants = open_store("auth")
    consent = open_store("consent", grants.authorize)
    auth_factory = importlib.import_module("voice_narration.auth.application").create_app
    consent_factory = importlib.import_module("voice_narration.consent.application").create_app
    now = [NOW]
    deliveries = []
    administrator = {"email": "admin@example.invalid", "password": ADMIN_PASSWORD,
                     "name": "Synthetic administrator"}
    auth = auth_factory(database=targets["auth"], root=paths["auth"],
                        auth_settings=dict(AUTH), clock=lambda: now[0],
                        send_verification=lambda email, token: deliveries.append((email, token)),
                        administrator=administrator)
    assert auth.state.effective_target() == grants.effective_target()
    assert auth.state.effective_auth_settings() == AUTH
    app = consent_factory(repository=consent, authenticate=auth.state.verify_token,
                          clock=lambda: now[0])
    try:
        with serve(auth) as accounts, serve(app) as consents:
            yield {"auth": accounts, "consent": consents, "now": now,
                   "deliveries": deliveries, "grants": grants, "app": app,
                   "auth_app": auth}
    finally:
        auth.state.close()


def register(system, email="owner@example.invalid", name="Synthetic owner"):
    response = system["auth"].post("/auth/register", json={
        "email": email, "password": PASSWORD, "name": name})
    assert response.status_code == 202, response.text
    assert response.json() == {"verification_required": True}
    canonical = email.strip().lower()
    tokens = [token for address, token in system["deliveries"] if address == canonical]
    assert tokens and isinstance(tokens[-1], str) and tokens[-1].strip()
    return tokens[-1]


def verify(system, email="owner@example.invalid"):
    credential = register(system, email)
    response = system["auth"].post("/auth/verify-email", json={"token": credential})
    assert response.status_code == 200, response.text
    token = response.json()
    assert set(token) == {"access_token", "token_type", "expires_at", "account"}
    assert token["token_type"] == "Bearer"
    assert token["expires_at"] == timestamp(system["now"][0] + timedelta(seconds=120))
    account = token["account"]
    assert set(account) == {"user_id", "email", "name", "role", "email_verified", "created_at"}
    from voice_narration._sql import identity
    identity(account["user_id"])
    assert account["email"] == email.strip().lower()
    assert account["role"] == "User" and account["email_verified"] is True
    assert account["created_at"] == timestamp(system["now"][0])
    return token, credential


def headers(token):
    return {"Authorization": "Bearer " + token["access_token"]}


def consent_body(**changes):
    body = {"consenting_identity": "Synthetic voice owner", "text": "I authorize this voice.\nमैं सहमत हूँ।",
            "version": "synthetic-legal-v1", "assisted": False}
    body.update(changes)
    return body


def record(system, token, **changes):
    response = system["consent"].post("/consent/record", headers=headers(token),
                                      json=consent_body(**changes))
    assert response.status_code == 201, response.text
    result = response.json()
    assert set(result) == {"consent_id", "owner_id", "consenting_identity", "text", "version",
                           "assisted", "authorization", "status", "created_at", "revoked_at"}
    assert result["owner_id"] == token["account"]["user_id"]
    assert result["status"] == "active" and result["revoked_at"] is None
    assert result["created_at"] == timestamp(system["now"][0])
    for field, value in consent_body(**changes).items():
        assert result[field] == value
    assert result["authorization"] == changes.get("authorization")
    return result


def test_registration_verification_login_and_duplicate_identity(system):
    credential = register(system, "  OWNER@Example.invalid  ")
    error(system["auth"].post("/auth/login", json={"email": "owner@example.invalid",
          "password": PASSWORD}), 403, "EMAIL_UNVERIFIED")
    verified = system["auth"].post("/auth/verify-email", json={"token": credential})
    assert verified.status_code == 200
    token = verified.json()
    assert token["account"]["email"] == "owner@example.invalid"
    assert token["account"]["role"] == "User"
    assert system["auth"].get("/auth/me", headers=headers(token)).json() == token["account"]
    duplicate = system["auth"].post("/auth/register", json={"email": "OWNER@example.invalid",
                "password": "different password", "name": "Replacement"})
    assert duplicate.status_code == 202 and duplicate.json() == {"verification_required": True}
    login = system["auth"].post("/auth/login", json={"email": " OWNER@EXAMPLE.INVALID ", "password": PASSWORD})
    assert login.status_code == 200 and login.json()["account"] == token["account"]
    error(system["auth"].post("/auth/login", json={"email": "owner@example.invalid",
          "password": PASSWORD.strip()}), 401, "INVALID_CREDENTIALS")
    error(system["auth"].post("/auth/verify-email", json={"token": credential}), 409, "TOKEN_CONSUMED")


def test_configured_token_boundaries_and_authenticated_principal(system):
    token, credential = verify(system)
    assert system["auth_app"].state.verify_token(token["access_token"]) == token["account"]
    assert system["auth"].get("/auth/me", headers=headers(token)).status_code == 200
    system["now"][0] = NOW + timedelta(seconds=119)
    assert system["auth"].get("/auth/me", headers=headers(token)).status_code == 200
    system["now"][0] = NOW + timedelta(seconds=120)
    error(system["auth"].get("/auth/me", headers=headers(token)), 401, "UNAUTHENTICATED")
    with pytest.raises(Exception) as caught:
        system["auth_app"].state.verify_token(token["access_token"])
    assert caught.value.code == "UNAUTHENTICATED"
    error(system["auth"].get("/auth/me"), 401, "UNAUTHENTICATED")
    error(system["auth"].get("/auth/me", headers={"Authorization": "Bearer unknown"}), 401, "UNAUTHENTICATED")
    system["now"][0] = NOW + timedelta(seconds=300)
    error(system["auth"].post("/auth/verify-email", json={"token": credential}), 400, "INVALID_TOKEN")
    pending = register(system, "pending@example.invalid")
    system["now"][0] += timedelta(seconds=300)
    error(system["auth"].post("/auth/verify-email", json={"token": pending}), 400, "INVALID_TOKEN")
    error(system["auth"].post("/auth/verify-email", json={"token": "unknown"}), 400, "INVALID_TOKEN")


@pytest.mark.parametrize("change", [
    {"role": "Administrator"}, {"email": "two@@example.invalid"}, {"email": "a b@example.invalid"},
    {"email": "@example.invalid"}, {"email": "a@"}, {"name": " "}, {"password": "short"},
    {"password": "x" * 81}, {"email": None}, {"name": 7}, {"unknown": True},
])
def test_registration_closed_validation_after_working_positive(system, change):
    token, unused = verify(system)
    assert token["account"]["role"] == "User"
    body = {"email": "new@example.invalid", "password": PASSWORD, "name": "New synthetic user"}
    body.update(change)
    error(system["auth"].post("/auth/register", json=body), 400, "INVALID_INPUT")


def test_separate_administrator_and_user_roles(system):
    user, unused = verify(system)
    login = system["auth"].post("/auth/login", json={"email": "admin@example.invalid", "password": ADMIN_PASSWORD})
    assert login.status_code == 200, login.text
    admin = login.json()
    assert admin["account"]["role"] == "Administrator" and admin["account"]["email_verified"] is True
    assert system["auth_app"].state.verify_token(admin["access_token"]) == admin["account"]
    assert user["account"]["user_id"] != admin["account"]["user_id"]
    legal = record(system, user)
    error(system["consent"].get("/consent/" + legal["consent_id"], headers=headers(admin),
          params={"owner_id": user["account"]["user_id"]}), 403, "FORBIDDEN")


def test_consent_immutable_legal_provenance_and_owner_gate(system):
    owner, unused = verify(system)
    other, unused = verify(system, "other@example.invalid")
    first = record(system, owner)
    second = record(system, owner, version="synthetic-legal-v2", text="New distinct consent")
    assert second["consent_id"] != first["consent_id"]
    path = "/consent/" + first["consent_id"]
    assert system["consent"].get(path, headers=headers(owner)).json() == first
    active = system["app"].state.validate_owner_consent(owner["account"], first["consent_id"])
    assert active == first
    error(system["consent"].get(path, headers=headers(other)), 403, "FORBIDDEN")
    error(system["consent"].get(path), 401, "UNAUTHENTICATED")
    error(system["consent"].post("/consent/record", json=consent_body()), 401, "UNAUTHENTICATED")
    for consent_id, account, code in [(first["consent_id"], other["account"], "FORBIDDEN"),
                                      (uid(), owner["account"], "NOT_FOUND")]:
        with pytest.raises(Exception) as caught:
            system["app"].state.validate_owner_consent(account, consent_id)
        assert caught.value.code == code
    assert system["consent"].get(path, headers=headers(owner)).json() == first


@pytest.mark.parametrize("change", [
    {"assisted": True}, {"assisted": False, "authorization": "Not applicable"},
    {"assisted": True, "authorization": " "}, {"text": None}, {"version": " "},
    {"consenting_identity": " "}, {"assisted": "false"}, {"owner_id": "forged"},
])
def test_explicit_assisted_authority_and_closed_consent_validation(system, change):
    owner, unused = verify(system)
    positive = record(system, owner, assisted=True, authorization="Owner explicitly authorized assisted recording.")
    assert positive["authorization"] == "Owner explicitly authorized assisted recording."
    error(system["consent"].post("/consent/record", headers=headers(owner),
          json=consent_body(**change)), 400, "INVALID_INPUT")


def test_live_scoped_grant_on_new_consent_boundary(system):
    owner, unused = verify(system)
    response = system["auth"].post("/auth/login", json={"email": "admin@example.invalid", "password": ADMIN_PASSWORD})
    assert response.status_code == 200
    admin = response.json()
    legal = record(system, owner)
    user_id = owner["account"]["user_id"]
    grant_id = uid()
    system["grants"].save_grant(principal(user_id), {"grant_id": grant_id, "owner_id": user_id,
        "administrator_id": admin["account"]["user_id"], "scopes": ["consents:read"],
        "created_at": NOW, "expires_at": NOW + timedelta(seconds=60), "revoked_at": None}, now=NOW)
    path = "/consent/" + legal["consent_id"]
    query = {"owner_id": user_id}
    assert system["consent"].get(path, headers=headers(admin), params=query).json() == legal
    system["grants"].revoke_grant(principal(user_id), grant_id, now=NOW)
    error(system["consent"].get(path, headers=headers(admin), params=query), 403, "FORBIDDEN")
    assert system["consent"].get(path, headers=headers(owner)).json() == legal
    system["grants"].save_grant(principal(user_id), {"grant_id": uid(), "owner_id": user_id,
        "administrator_id": admin["account"]["user_id"], "scopes": ["profiles:read"],
        "created_at": NOW, "expires_at": NOW + timedelta(seconds=60), "revoked_at": None}, now=NOW)
    error(system["consent"].get(path, headers=headers(admin), params=query), 403, "FORBIDDEN")
    system["grants"].save_grant(principal(user_id), {"grant_id": uid(), "owner_id": user_id,
        "administrator_id": admin["account"]["user_id"], "scopes": ["consents:read"],
        "created_at": NOW, "expires_at": NOW + timedelta(seconds=60), "revoked_at": None}, now=NOW)
    assert system["consent"].get(path, headers=headers(admin), params=query).json() == legal
    system["now"][0] = NOW + timedelta(seconds=60)
    error(system["consent"].get(path, headers=headers(admin), params=query), 403, "FORBIDDEN")
