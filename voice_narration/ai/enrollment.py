"""Model-selected minimal conditioning behind live owner and sample gates."""
from copy import deepcopy
from uuid import uuid4

from voice_narration._enrollment import model, owner, serializer
from voice_narration._sql import PersistenceError, fail, identity, instant
from voice_narration.voices.quality import decode, duration_bounds


class EnrollmentAdapter:
    def __init__(self, *, repository, validate_consent, artifacts, capability, condition, clock):
        if not all(callable(value) for value in (validate_consent, artifacts, capability, condition, clock)):
            fail("INVALID_CONFIGURATION")
        self.repository = repository
        self.validate_consent = validate_consent
        self.artifacts = artifacts
        self.capability = capability
        self.condition = condition
        self.clock = clock
        self.serialized = serializer()
        self.enroll = self.serialized(self.enroll)
        self.material_kinds = self.serialized(self.material_kinds)

    def material_kinds(self, account, profile_id):
        who = owner(account)
        identity(profile_id)
        rows = self.repository.list(who, owner_id=who["user_id"], now=instant(self.clock()))
        matches = [r for r in rows if r["profile_id"] == profile_id and
                   r["category"] == "conditioning" and r["payload"].get("complete") is True]
        if not matches:
            return []
        record = matches[0]
        self.validate_consent(account, record["consent_id"])
        chunks = self.repository.read_bytes(who, record["id"], now=instant(self.clock()))
        if len(chunks) != len(record["payload"]["materials"]):
            fail("DEPENDENCY_UNAVAILABLE")
        return list(record["payload"]["materials"])

    def enroll(self, account, profile, samples):
        who = owner(account)
        if profile["owner_id"] != who["user_id"]:
            fail("FORBIDDEN")
        self.validate_consent(account, profile["consent_id"])
        selected = model(profile["model"])
        cap = self.capability(selected)
        required = cap.get("enrollment_materials")
        if (not isinstance(required, list) or not required or
                any(k not in ("reference_audio", "embeddings", "weights") for k in required) or
                len(set(required)) != len(required)):
            fail("MODEL_NOT_READY")
        current = self.artifacts(account, profile["consent_id"],
                                 [item["artifact_id"] for item in samples])
        bounds = duration_bounds(cap)
        for item in current:
            decoded = decode(item["bytes"], item["artifact"]["format"])
            if not bounds[0] <= decoded["duration_seconds"] <= bounds[1]:
                fail("INVALID_INPUT")
        existing = self.material_kinds(account, profile["profile_id"])
        if existing:
            return existing
        try:
            materials = self.condition(deepcopy(selected), deepcopy(current), list(required))
        except Exception:
            raise PersistenceError("DEPENDENCY_UNAVAILABLE") from None
        if (not isinstance(materials, dict) or set(materials) != set(required) or
                any(not isinstance(value, bytes) or not value for value in materials.values())):
            fail("DEPENDENCY_UNAVAILABLE")
        self.validate_consent(account, profile["consent_id"])
        if self.capability(selected)["enrollment_materials"] != required:
            fail("MODEL_NOT_READY")
        self.artifacts(account, profile["consent_id"], [item["artifact_id"] for item in current])
        record_id = str(uuid4())
        with self.repository.transaction():
            self.repository.save({"id": record_id, "owner_id": who["user_id"],
                                  "profile_id": profile["profile_id"], "consent_id": profile["consent_id"],
                                  "category": "conditioning",
                                  "created_at": instant(self.clock()),
                                  "payload": {"materials": required, "complete": True}})
            for kind, data in materials.items():
                self.repository.store_bytes(record_id, kind, data)
        return required


def create_adapter(**kwargs):
    return EnrollmentAdapter(**kwargs)
