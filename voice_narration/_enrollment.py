"""Private enrollment boundary primitives; no model or policy defaults."""
from copy import deepcopy
from functools import wraps
from secrets import token_urlsafe
from threading import RLock

from voice_narration._http import closed, text
from voice_narration._sql import actor, fail, identity


def principal(account):
    if not isinstance(account, dict) or account.get("email_verified") is not True:
        fail("UNAUTHENTICATED")
    who = {"user_id": account.get("user_id"), "role": account.get("role")}
    actor(who)
    return who


def owner(account):
    who = principal(account)
    return {"user_id": who["user_id"], "role": "User"}


def model(value):
    closed(value, {"model_id", "version"})
    identity(value["model_id"])
    text(value["version"])
    return deepcopy(value)


def serializer():
    lock = RLock()

    def serialized(operation):
        @wraps(operation)
        def invoke(*args, **kwargs):
            with lock:
                return operation(*args, **kwargs)
        return invoke
    return serialized


def query(request, permitted):
    params = request.query_params
    if set(params) - set(permitted) or any(len(params.getlist(key)) != 1 for key in params):
        fail("INVALID_INPUT")
    if any(not value.strip() for value in params.values()):
        fail("INVALID_INPUT")
    return dict(params)


class Pages:
    """Unpredictable process-local cursors bound to principal, filter and frozen records."""
    def __init__(self, settings):
        if (not isinstance(settings, dict) or set(settings) != {"default_page_size", "max_page_size"} or
                any(type(v) is not int or not 1 <= v <= 9007199254740991 for v in settings.values()) or
                settings["default_page_size"] > settings["max_page_size"]):
            fail("INVALID_CONFIGURATION")
        self.settings = dict(settings)
        self.cursors = {}

    def page(self, account, endpoint, parameters, records):
        who = principal(account)
        filters = {k: v for k, v in parameters.items() if k not in ("cursor", "limit")}
        size = self.settings["default_page_size"]
        if "limit" in parameters:
            raw = parameters["limit"]
            if not raw.isascii() or not raw.isdecimal() or int(raw) < 1:
                fail("INVALID_INPUT")
            size = int(raw)
        if size > self.settings["max_page_size"]:
            fail("LIMIT_EXCEEDED")
        binding = (who["user_id"], who["role"], endpoint, filters)
        if "cursor" in parameters:
            saved = self.cursors.get(parameters["cursor"])
            if saved is None or saved[0] != binding:
                fail("INVALID_CURSOR")
            items, start = deepcopy(saved[1]), saved[2]
        else:
            items, start = deepcopy(records()), 0
        end = start + size
        cursor = None
        if end < len(items):
            cursor = token_urlsafe(32)
            self.cursors[cursor] = (deepcopy(binding), items, end)
        return {"items": deepcopy(items[start:end]), "next_cursor": cursor}
