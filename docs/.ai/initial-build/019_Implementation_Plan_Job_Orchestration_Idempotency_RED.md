# Job Orchestration & Idempotency RED — Implementation Plan019

## Milestone and current authority

This plan proposes **initial-build milestone17, RED**, exactly as recorded in the approved Plan. Artifact019 was the next unused document number when created; it is not milestone19. Milestone16, Job Accounting Contract Amendment, is complete from human approval recorded2026-10-29T01:53:20Z. Milestone17 remains Pending. This document proposes tests only and does not execute the milestone or authorize GREEN. **F2 planning validation remains blocked after the authorized sequential regression retry failed; F2 has not been executed, and this draft is not ready for RED execution approval.**

The Q13 product decisions are resolved. The private composition signatures below are explicit implementation choices for review, as permitted by Q10/Q12. They add no public endpoint, configuration field, account-deletion feature, calibration approval, model enablement, or new product decision.

## Authoritative references

All paths below are relative to the repository. References were read as sources with the following provenance; external documents do not override the user's request or manufacture human approval.

| Reference | Status and use |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved Q13, recorded2026-10-28T23:42:55Z; FR-022/023/045, R-GEN-001, FR-044, NFR-008 and Q13 acceptance criteria govern. |
| docs/.ai/initial-build/Plan.md | Approved Q13 revision2026-10-29T00:32:31Z; current execution table records1–16 Complete and Job RED17 Pending. Governs scope/type, predecessor and traceability. |
| docs/.ai/initial-build/contract/API-Contract.md | Complete amended contract approved2026-10-29T01:53:20Z. Jobs, Policy, generated Artifact, Configuration, Q13 accounting, internal commands and common rules govern. |
| docs/.ai/initial-build/Job-Period-Accounting-Proposal.md | Approved2026-10-28T02:54:15Z; original admission facts, epoch projections, monthly recognition, unknown holds and minimum lifetime facts. |
| 001_Implementation_Plan_Foundation.md | Approved/executed; pinned Windows Python/FastAPI/HTTPX/pytest/PostgreSQL/Compose harness, real owner isolation, PostgreSQL-backed queue/outbox prerequisites. |
| 002_Implementation_Plan_Model_Feasibility.md | Approved/executed documentation assessment; commercial/model/human-evaluation gates remain. No production model approval inferred. |
| 003_Implementation_Plan_Persistence_RED.md | Approved but stopped; read with004 recovery, not substituted for successful recovery evidence. |
| 004_Implementation_Plan_Persistence_RED_Recovery.md | Approved2026-10-25T02:26:04Z and executed;33 real isolated owner persistence cases. |
| 005_Implementation_Plan_Persistence_GREEN.md | Approved2026-10-25T03:25:08Z; owner-local SQL/retention/grants decisions carried forward with006 verification. |
| 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved2026-10-25T03:32:49Z and executed; repeatable33-case GREEN. |
| 007_Implementation_Plan_Authentication_Consent_RED.md | Approved2026-10-25T15:41:03Z and executed;24 actual Auth/Consent HTTP expectations. |
| 008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved2026-10-25T18:53:07Z and executed; actual account verification/login/live consent. |
| 009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved2026-10-25T21:43:58Z and executed; native evaluator and deterministic synthetic evidence, not human calibration. |
| 010_Implementation_Plan_Voice_Enrollment_RED.md | Approved/executed2026-10-25T22:44:13Z; existing real HTTP fixtures and explicit raw collaborator boundaries. |
| 011_Implementation_Plan_Enrollment_Catalog_Test_Wiring_Correction.md | Approved/executed2026-10-26T16:54:05Z; explicit trusted catalog seam, no implicit model/default. |
| 012_Implementation_Plan_Enrollment_Interface_Completion_RED.md | Approved/executed2026-10-26T17:56:49Z; actual40 enrollment identities, current selected-model contract. |
| 013_Implementation_Plan_Voice_Enrollment_GREEN.md | Historical, not current execution authority; replaced by014 correction and015 reviewed GREEN. |
| 014_Implementation_Plan_Enrollment_Playback_Link_Test_Wiring_Correction.md | Approved/executed2026-10-27T05:28:04Z; origin-relative playback links resolve against actual fixture origin. |
| 015_Implementation_Plan_Voice_Enrollment_GREEN.md | Executed after re-approval2026-10-28T01:10:47Z; two97/97 passes743.72s/623.70s, exact predecessor bytes and successful owned cleanup. |
| Enrollment-Quality-Policy-Proposal.md; Enrollment-Catalog-Seam-Correction-Proposal.md; Enrollment-Interface-Completion-Proposal.md; Enrollment-Playback-Link-Test-Correction-Proposal.md | Approved predecessor clarifications carried through010–015; synthetic tests cannot become human calibration or licensing evidence. |
| 016_Implementation_Plan_Job_Orchestration_RED.md;017_Implementation_Plan_Job_Orchestration_GREEN.md;018_Implementation_Plan_Mock_Inference_Adapter_RED.md | Preserved external/unreviewed prototypes. Their milestone numbering/completion/commit claims are not authority. Do not overwrite, execute, reuse approvals, or mark later work complete. |
| voice_narration/jobs/application.py;tests/test_job_orchestration.py; actual Auth/Consent/Profile/Artifact/Policy persistence code and approved four test modules | Repository facts, inspected against approved authority. Actual tests/source, not old planning copies, determine current interfaces. |

There is no docs/requirements.md in this checkout. Source command create-implementation-plan, planner agent, PDD and implementation-planning/testing/security/distributed/resilience/Python/API rules guide this one reviewed plan; they do not authorize execution.

## Predecessor and current-state findings

The preserved cohort is97 cases:6 deterministic quality,34 enrollment HTTP,33 persistence and24 Auth/Consent. The actual97 predecessor evidence is in015/Plan; unreviewed95-pass or one-catch-all-pass claims in later external documents do not replace it.

Jobs production exists. Its inspected factory accepts repository/authenticate/validate_consent/artifacts/voices/capability/policy_snapshot/quota_provider/cost_provider/clock, then constructs Pages(None). The current code has /jobs/submit, legacy request/Job shapes,60-second process-local key cache, heuristic duration/cost, no-op recovery and memory-only quota overrides. These are preserved unreviewed divergences, not an absent Jobs module. Policy has delivered RetentionRepository, but no policy.application; Artifact's delivered sample application has no generated-output service. Missing approved orchestration/accounting interfaces may establish RED. Missing pytest fixtures, unrelated constructor wiring, dependencies or Docker permission failures cannot.

The existing Job test contains a broad exception-catching test and seven skipped async placeholders referencing nonexistent fixtures. None establishes approved RED. This plan replaces that complete unreviewed file with concrete tests and preserves its original bytes in planning evidence. It does not delete or weaken an approved normative assertion: the same-coverage replacement covers submission/idempotency/quota/recovery/cost/history/admin configuration explicitly, and adds all Q13 refinements.

Git status was inspected throughout planning; no clean-tree assertion is made. External commit aab7717f187e874eae19f3cb9396533cd065c7de changed Plan.md Current State prose to claim Job/Mock completion from one catch-all pass and skipped placeholders. Later external prose claims19 completed through Mock GREEN020. That summary also incorrectly assigns the00:32:31Z Plan approval time to the Q13 contract. The actual approved milestone definitions/execution table still say Job RED17 Pending; the contract's actual approved status is2026-10-29T01:53:20Z. Preserve the external prose without crediting it as human approval, valid RED or completed implementation. Latest Plan raw SHA256 observed2026-10-29 is e3a9ce3504fc9769fd5271c9c9637b493b33220ba16549ae01ebbf195713c32f (earlier inspected7c2fdbaff6100202f73577c5cb6bfebb69676f43c3419247f82eb86004afcdaf). Current unreviewed inference work is also preserved; this plan owns neither it nor its claims. No new FOUNDATION prerequisite is proposed: actual PG, HTTP, accounts, consent, profile and queue/outbox prerequisites exist. No dependency install is needed to support a prototype.

## Files and ordered proposed changes

Files to create during milestone execution: none. Files to delete: none. Files to modify: **tests/test_job_orchestration.py only**, by complete replacement with the exact code below. The milestone's later verified Execution Status update in Plan.md remains the standard PDD exception to file scope; it is not proposed here during planning.

1. Reuse approved postgres/stores/enrollment_system fixtures, dynamic ports, real owner credentials and real loopback HTTP.
2. Define explicit private synthetic model/pricing/provider/dispatch inputs and real Policy HTTP transport. No collaborator returns a final Job/Usage decision. The generated Artifact factory and Jobs owner authorization port are intended production behavior, not test fake outputs.
3. Replace every placeholder with the complete parameterized behavioral test cohort below; do not skip or catch arbitrary exceptions to claim success.
4. Verify frozen collection, intended RED twice, preserved97 before/after, signature/probe soundness and byte/resource preservation. Do not proceed to production implementation.

## Decisions and complete private protocols for review

These signatures are deliberate future production interfaces under the approved owners, not claims that current prototypes implement them. RED writes no production scaffolding.

| Owner/interface | Exact signature and responsibility |
| --- | --- |
| Policy factory | voice_narration.policy.application.create_app(*,repository,authenticate,authenticate_service,initial_configuration,emit,clock). RetentionRepository is own PG/root only; initial_configuration is the full explicit test Configuration and seeds only an absent durable document, never resets on restart. authenticate(token) is actual Auth verification; authenticate_service(credential) returns authenticated service enum. emit(envelope) accepts raw domain fact and may raise PersistenceError. clock()->aware UTC datetime. |
| Policy state | configuration()->deepcopy of durable effective Configuration; record_request(account,request_id,received_at)->None or PersistenceError, records authenticated public receipt once then enforces request protection; dispatch_pending()->None drains durable owner outbox; close()->None closes only supplied owned repository. |
| Public gateway composition | policy.application.protect_public(app,*,authenticate,record_request,clock)->ASGI app. Count every authenticated /api/v1 receipt including replay/polling/errors, with trusted server ID/time, once. Internal /internal/v1 is excluded. Policy factory applies the same protection to its own public routes; Jobs factory relies on its wrapped public boundary to avoid double counting. Other delivered apps are wrapped only in the all-owner counting test. This introduces no external request-record route or tenth domain service. |
| Jobs factory | voice_narration.jobs.application.create_app(*,repository,authenticate,authenticate_service,validate_consent,voices,artifacts,capability,configuration,policy,estimate,dispatch,execution_permit,clock). repository is actual Jobs-owned HistoryRepository with actual grant authority. No owner shares a database with another. |
| Jobs input ports | validate_consent(account,consent_id)->actual Consent; voices(account,profile_id)->actual authorized Profile over real Profile HTTP; capability(Model)->private synthetic trusted Capability; configuration()->full effective Policy Configuration; policy(operation,body,deadline)->actual response over real Policy HTTP, raising PersistenceError for stable errors; estimate(Model,max_audio_seconds)->{estimated_cost_usd:USD}, raw approved-test-price evidence only. artifacts(operation,body,deadline)->actual Artifact metadata/cleanup over real Artifact HTTP. |
| Jobs resource/dispatch ports | execution_permit()->{always_on_gpu:boolean,approved:boolean}; a trusted private operator/provider evidence port, not a public approval flag. Tests deny always-on GPU without approval and never provision one. dispatch(MessageEnvelope)->None or PersistenceError; accepted delivery can lose its reply, so durable unsent work and stable message identity are required. |
| Jobs state | dispatch_pending()->None; recover()->None, recovers durable unfinished interrupted work and expires deadlines; receive(envelope,*,producer)->None on accepted/deduplicated fact or PersistenceError for terminal/transient failure; artifact_job(account,job_id)->actual current owner-authorized Job for Artifact safety, without counting an internal lookup as a public request; close()->None. On process restart, recovery treats recorded running work as interrupted, delays the next execution attempt by configured retry_delay_seconds and never extends the one deadline. max_attempts includes the initial dispatch; each distinct execution attempt has a new durable narration.generate message_id, redelivery of that attempt reuses its ID. |
| Generated Artifact factory | voice_narration.artifacts.jobs.create_app(*,repository,authenticate,authenticate_service,validate_consent,job,capability,configuration,clock). Separate intended owner-local service composition, not a modification of the delivered sample factory. repository uses a separate connection to the same isolated Artifact-owner DB/root. job(account,job_id) delegates to real Jobs.state.artifact_job; it is not a final Job fake. Implement contract internal store/metadata/batch-delete and generated public links/content. Staged bytes stay inaccessible until completed winner/settlement. |
| Raw test collaborators | TestCatalog only supplies explicitly private synthetic model/capability records. estimate supplies synthetic0.200000 pricing evidence. execution_permit supplies test resource facts. dispatch/emit collect raw envelopes and may simulate lost acknowledgement. Test worker drives actual internal work-item/status/store/complete/fail HTTP calls using synthetic WAV and valid Cost wire data; no AI inference or natural speech is claimed. |

Configuration is fully declared by configuration() in the exact code: every transport/storage/auth/limit/quota/budget/retention/quality value is an explicit private fixture input. Full replace/CAS, page limits, max key bytes, service deadline, attempts/delay, script/output/sample bounds, system concurrency and budget are supplied up front; there is no hidden fallback. initial Configuration revision0 is an isolated bootstrap choice. Synthetic bucket/secret references do not resolve a real cloud account. The full selected quota replaces default; there is no invented system quota period or undefined override-deletion endpoint.

Carried forward: Python3.13.17, pytest9.1.1 with -p no:anyio, FastAPI0.162.0/Uvicorn0.54.0, HTTPX0.28.1, PostgreSQL18.6/Psycopg3.3.6, Compose5.6.0/Docker29.3.1, numpy2.5.4/PyAV19.0.2 and delivered native WebRTC evaluator. No version selection/update/install. Use the approved PostgreSQL-backed outbox harness; physical production broker transport remains the later integration concern, not an unapproved added dependency.

## Contract and requirement coverage

Each name below means test_<name> in the exact code. Parameterized cases are real separately collected tests. Every negative begins after a positive boundary is active. Existing approved97 checks are preserved regressions, never new RED evidence.

| Approved rule/concern | Concrete cases |
| --- | --- |
| FR-022/023/045; canonical202 queued Acceptance, immutable Unicode/profile/model/control snapshots, null unmeasured cost/output, restart-safe exact replay and pinned omitted defaults | acceptance_snapshot_and_durable_replay; unicode_scalar_limit_and_pinned_job_snapshot_after_limits_lowered |
| Durable concurrent owner submission, one reservation, stable outbox delivery identity, no TTL expiry or duplicate billing | concurrent_submit_one_admission_outbox_and_restart; lost_policy_ack_recovery_one_admission_and_settlement |
| Closed Generation/header-only bounded key; scalar script limit; capabilities/model/profile/consent/pricing/protection/provider gates | generation_validation_and_rejection_does_not_bind_key[7]; header_limits_owner_scope_and_live_admission_gates; profile_readiness_and_immediate_consent_fence_before_event_delivery |
| Canonical trusted acceptance_created_at, not delayed Policy receipt; selected epoch window, original quantity attribution, reprojection and all-window active concurrency | jobs_carries_canonical_acceptance_time_across_delayed_policy_receipt; quantity_admission_time_reprojection_and_active_across_windows; default_window_change_override_replacement_and_system_concurrency |
| All authenticated public receipts including replay/polling, every owner surface, own Usage, epoch reprojection; internal service callbacks excluded | public_request_count_replay_poll_and_internal_exclusion; request_projection_includes_every_authenticated_public_owner |
| UTC monthly first recognition, carried unknown holds, measured timestamp preserved, empty aggregate honest0, late known release freshID, original null response snapshot, fresh null no downgrade, duplicate/conflict/opposite terminal winner | monthly_unknown_hold_first_recognition_and_command_snapshots; commit_winner_null_required_and_foreign_accounting_denied; commit_release_race_one_quantity_and_money_winner |
| All3 Policy command IDs and reserve admission timestamp required/closed; same/fresh semantic reserve identity, changed bound/cost/time409; foreign/unknown authority | reserve_command_ids_admission_fact_and_closed_inputs; commit_winner_null_required_and_foreign_accounting_denied |
| Config admin whole replace/revision CAS/persisted effective values; full per-user override; stricter config/model/quota bounds; absolute3000 config cap; system concurrency; admission limits do not retroactively cancel | configuration_cas_quota_limits_and_budget_holds; default_window_change_override_replacement_and_system_concurrency; unicode_scalar_limit_and_pinned_job_snapshot_after_limits_lowered |
| FR-044/NFR-008; estimated holds separate from measured cost, global stop/kill switch before admission and further work, forecast exact real-month formula, no estimate-based/duplicate alert | configuration_cas_quota_limits_and_budget_holds; forecast_uses_known_monthly_spend_and_deduplicates_alerts; cost_wire_validation_exact_decimal_totals[4] |
| Required status chain, actual generated WAV staging/ownership/publication after winner; completion/cancel sequential and concurrent one winner, settlement once | lifecycle_completion_cancel_winner_and_one_billing; complete_cancel_race_one_publication_winner; actual_output_overrun_is_rejected_without_publication |
| One Job/deadline across interruption; delay and max_attempts includes first; RETRY_EXHAUSTED before deadline versus JOB_TIMEOUT; unknown terminal costs retain hold and release active quantity | repeated_crash_attempt_budget_includes_initial_and_preserves_deadline; timeout_retry_same_job_deadline_and_bounded_attempts |
| FR-045 history shape/descending stable pagination/cursor owner binding; live scoped Administrator grants; source immutable; retained-only late known cost | history_snapshot_cursor_owner_and_terminal_cost_update; job_history_granted_administrator_read_rechecks_revocation |
| Q13 accounting-only original-authority settlement after revoke/purge with fresh deadline beyond expired execution; ordinary private callback still fenced/purged, idempotency-only Acceptance, no resurrection | revocation_purge_minimal_metadata_and_late_accounting; internal_deadline_identity_and_transition_conflicts |
| Account-lifetime content-free new ledgers/retry receipts, later larger-window projection after private purge, durable fact dedupe, complete protection unavailable fails closed | revocation_purge_minimal_metadata_and_late_accounting; missing_durable_policy_facts_never_become_zero |

Not tested here, with reason: physical broker connection/TLS/credential rotation/rate/inflight/backpressure/quarantine transport integration and deployed secret resolution belong to Security & Nine-Service Integration, while this milestone tests owner outbox and HTTP domain decisions. Actual model inference, provider metering conversions/half-even rounding from raw measurements, acoustics/natural speech, licensed MP3, section regeneration and real chunk/join quality belong to approved Mock/Real-Model/Frontend/evaluation milestones (FR-024–028/040–042); the generated synthetic WAV/mapping here is orchestration evidence only. Whole/section regeneration operation-specific key scope and acoustic joins are not claimed by create_job tests. Whole-contract exhaustive malformed-byte/duplicate-key/part matrices outside these routes remain their owning stages; the concrete Job/Policy closed/required/authority cases listed here are verified. Public Consent/Voice deletion producers/cleanup API are later deletion/integration work; tests activate the delivered real Consent-owned fence directly, then exercise immediate Jobs HTTP safety before event delivery and broker-input purge afterward. They do not fake a Consent verdict or create a new deletion route. No account-deletion behavior is introduced.

Privacy limitation is explicit: delivered jobs_cleanups.profile_id/consent_id are existing cleanup fence keys established by predecessor persistence. The scan preserves those two existing columns, rather than invent retroactive deletion of predecessor fence keys. Every row is still scanned for script/token/filename/model identity, and every other field/new accounting/retry/fact row for profile/consent identity. Existing cleanup JSON is not exempt. This proves the new lifetime ledgers carry no prohibited private content; it is not a new claim that all previous cleanup/audit metadata retention has been redesigned.

## Acceptance / completion criteria for future execution

1. Exactly the reviewed test replacement is applied; approved97 source/test/configuration bytes and external inputs are preserved. No production source, migration, dependency, runtime/build configuration or test-infrastructure file changes.
2. All38 proposed identities collect with no skips/xfails, catch-all success or missing test fixture. New feature cases fail solely because approved production behavior/interfaces are missing, after real prerequisite setup succeeds. ModuleNotFoundError for intended policy.application/artifacts.jobs, unsupported intended Jobs signature, or behavioral HTTP assertions are valid only when attributed to the approved behavior. Docker access/startup, bad fixture/malformed valid request, missing dependency and unrelated setup failure stop execution and are not RED.
3. The approved97 cohort passes before and after replacement on one retained isolated verification copy, without manual cleanup between repeated verification. Test-owned fixtures create/drop their own UUID projects/databases/roles and prove effective settings/targets. No shared resources are reset.
4. Frozen RED repeats have identical proposed test hashes and feature-attributable failures. The scratch-only approved-signature/probe soundness checks are recorded with their precise limits. Future GREEN must pass every body; entry-interface RED is not evidence those later branches already execute or pass.
5. All original protected hashes remain equal except the authorized target at execution and the milestone's standard verified Plan status update. Owned resources are gone; user Docker and other projects remain untouched. Record exact actual commands/results, not predictions, then stop for a separately reviewed GREEN plan.

## Verification commands for future execution

From an isolated disposable copy, with the existing workspace interpreter (do not install dependencies):

```powershell
$pythonPath = 'C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe'
& $pythonPath -m pytest -p no:anyio -q tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py
& $pythonPath -m py_compile tests/test_job_orchestration.py
& $pythonPath -m pytest -p no:anyio --collect-only -q tests/test_job_orchestration.py
& $pythonPath -m pytest -p no:anyio -v --tb=short tests/test_job_orchestration.py
& $pythonPath -m pytest -p no:anyio -v --tb=short tests/test_job_orchestration.py
& $pythonPath -m pytest -p no:anyio -q tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py
```

Check target/protected raw SHA256 before/after each recorded run and inventory/inspect only project labels printed by those fixtures; retained verification copy has no manual state cleanup between commands. Signature-stub/probe validation is planning soundness only and never enters the working tree. Execution does not add a production stub to satisfy RED.

Expected / Predicted — Not Yet Verified as milestone evidence:38 new intended-feature failures and97 preserved passes, repeated with successful isolated teardown. A passing catch-all, skipped placeholder, baseline failure or unrelated setup error cannot satisfy these criteria. Planning results below, even when observed, are not execution evidence or human approval.

## Pre-authorized contingencies

Only observable Docker named-pipe or loopback bind denial permits requesting normal host-context review for the exact isolated command. No file/dependency/test assertion changes are authorized by this contingency. Docker Desktop/engine lifecycle, stopping other containers or global prune are excluded. Test-owned cleanup is limited to the exact fixture UUID project/roles/databases after verifying labels. Any other failure stops execution for diagnosis and reviewed replanning, without weakening criteria or blind retries.

## Recovery, risks and exclusions

Before applying, retain original target bytes/hash; rollback restores only that exact file after checking no concurrent user edits would be lost. Do not use git reset/clean/checkout, delete external work, or touch unrelated files. Scratch copies are removed only after resolved containment checks and owned process/project completion.

Main risk: intentionally absent approved interfaces block downstream feature bodies at RED. Explicit ports, syntax/collection, stub binding and an isolated positive probe reduce fixture risk but do not replace full GREEN validation. Network startup can fail independently; retain every attempt and distinguish it. Race results may choose either legal winner; assertions require one durable outcome rather than an arbitrary ordering. Non-USD Decimal comparisons accept equivalent string representations; USD remains exact six-place. All price/model/provider/material evidence is private synthetic test input, not a tariff, G1 score, licensing clearance, human calibration or training claim.

No source fixes, commits/pushes, next milestone execution, natural-voice dataset, model download/training, GPU provisioning or deployment is included.

## Exact complete replacement: tests/test_job_orchestration.py

Original external target SHA256: `0576e9c15b1e9135c34119e4737b55f18df47c32ad8acb99e38c452c11056436`. Proposed F2 UTF-8 content SHA256: `ef4393e3079028db3f30ebc8f87d5f5991d9edece161f80f1398fc7682f30c3d`. Complete content follows; no omitted fragments. F2 changes only the raw message-loss target and execution-message count described in planning evidence; F2 runtime validation is pending.

```python
"""Approved Job/Q13 contract: real owner stores and HTTP, private synthetic inputs."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import importlib
import json
from urllib.parse import urljoin

import numpy as np
import psycopg
from psycopg import sql
import pytest

from test_persistence import postgres, stores, uid
from test_authentication_consent import AUTH, ADMIN_PASSWORD, PASSWORD, serve, error, headers, verify
from test_voice_enrollment import enrollment_system, warned, override, profile, create_profile
from test_enrollment_quality import MODEL, candidate_policy, wav_bytes


SCRIPT = "SYNTHETIC_JOB_PRIVATE_MARKER नमस्ते!\nHello, world."
UTC = timezone.utc
JOB_FIELDS = set("job_id owner_id profile_id model script_snapshot language style controls parent_job_id regenerated_chunk_ids status created_at updated_at completed_at output_artifact_id joined_preview_artifact_id duration_seconds estimated_cost_usd measured_cost failure mapping_available".split())
USAGE_FIELDS = set("window_start reset_at accepted_jobs reserved_audio_seconds consumed_audio_seconds requests active_jobs policy estimated_usd measured_cost budget_stopped".split())
SERVICES = "auth consent voices jobs artifacts policy ai worker audit".split()


def stamp(value):
    return value.isoformat().replace("+00:00", "Z")


def decimal_is(value, expected):
    return isinstance(value, str) and Decimal(value) == Decimal(expected)


def cost(compute="0.100000", storage="0.020000", at=None):
    return {"compute_usd": compute, "storage_usd": storage,
            "total_usd": format(Decimal(compute) + Decimal(storage), ".6f"),
            "measured_at": stamp(at or datetime(2030, 1, 1, tzinfo=UTC))}


def configuration():
    return {"revision": 0, "public_base_url": "http://127.0.0.1", "mode": "mock",
            "auth": dict(AUTH),
            "service_urls": {s: "http://127.0.0.1" for s in SERVICES if s != "worker"},
            "transport": {"environment": "local", "service_identity_secret_refs": {
                s: "test-only:" + s for s in SERVICES}},
            "storage": {"primary_bucket": "test-only-private", "credential_secret_ref":
                        "test-only:storage", "local_copy_directory": None},
            "limits": {"upload_max_bytes": 500000, "samples_per_profile": 3,
                       "samples_total_max_bytes": 1500000, "script_max_characters": 1000,
                       "output_max_seconds": "12", "job_timeout_seconds": 120,
                       "inference_timeout_seconds": 60, "max_attempts": 2,
                       "retry_delay_seconds": 2, "idempotency_key_max_bytes": 80,
                       "message_max_bytes": 4096, "message_rate_per_second": 10,
                       "inflight_messages": 2, "page_default": 2, "page_max": 4},
            "default_user_quota": {"window_seconds": 60, "generation_count": 10,
                                   "audio_seconds": "120", "request_count": 1000,
                                   "concurrent_jobs": 3}, "system_concurrent_jobs": 4,
            "budget": {"monthly_target_usd": "20.000000", "forecast_alert_usd": "20.000000",
                       "stop_usd": "100.000000", "kill_switch": False},
            "retention": {"generated_audio_days": 30, "profile_days": 30,
                          "sample_days": 30, "consent_days": 30, "audit_days": 30,
                          "cleanup_window_seconds": 60},
            "enrollment_quality": candidate_policy()}


class PolicyHTTP:
    """Transport only; Policy makes every admission and Usage decision."""
    def __init__(self, world):
        self.world = world
        self.lose_reply = None
        self.calls = []
        self.reserve_delay_seconds = 0

    def command(self, operation, value, deadline):
        from voice_narration._sql import fail
        self.calls.append((operation, deepcopy(value), deadline))
        if operation == "reserve" and self.reserve_delay_seconds:
            self.world.now[0] += timedelta(seconds=self.reserve_delay_seconds)
            self.reserve_delay_seconds = 0
        response = self.world.internal("policy", "/quotas/" + operation, value,
                                       deadline=deadline, service="jobs")
        if response.status_code >= 400:
            fail(response.json()["error"]["code"])
        if self.lose_reply == operation:
            self.lose_reply = None
            fail("DEPENDENCY_UNAVAILABLE")
        return response.json()


class World:
    def __init__(self, system, store_bundle):
        self.s = system
        self.open_store, self.paths, self.targets = store_bundle
        self.now = system["now"]
        self.config = configuration()
        self.events, self.sent, self.estimates = [], [], []
        self.command_contexts = {}
        self.complete_bodies = {}
        self.price = "0.200000"
        self.price_ready = True
        self.protection_ready = True
        self.provider_permit = {"always_on_gpu": False, "approved": False}
        self.drop_dispatch_reply = False
        self.stack = ExitStack()
        self.policy_transport = PolicyHTTP(self)
        self.apps, self.clients = {}, {}
        self.refresh()
        self.owner = self.token["account"]["user_id"]
        self.foreign, _ = verify(system, "foreign@example.invalid")
        cap = system["catalog"].cap
        cap.update(max_script_characters=1000, mapping=True,
                   pause_strength={"min": "0", "max": "1", "step": "0.1", "default": "0.5"},
                   speech_pace={"min": "0.5", "max": "2", "step": "0.1", "default": "1"})
        self.model = system["catalog"].capability

    def refresh(self):
        response = self.s["auth"].post("/auth/login", json={"email": "owner@example.invalid",
                                                          "password": PASSWORD})
        assert response.status_code == 200, response.text
        self.token = response.json()
        self.s["token"] = self.token
        response = self.s["auth"].post("/auth/login", json={"email": "admin@example.invalid",
                                                          "password": ADMIN_PASSWORD})
        assert response.status_code == 200, response.text
        self.admin = response.json()

    def service_identity(self, credential):
        from voice_narration._sql import fail
        if credential not in {"test-only:" + s for s in SERVICES}:
            fail("UNAUTHENTICATED")
        return credential.split(":", 1)[1]

    def estimate(self, model, maximum):
        from voice_narration._sql import fail
        self.estimates.append((deepcopy(model), maximum))
        if not self.price_ready:
            fail("DEPENDENCY_UNAVAILABLE")
        return {"estimated_cost_usd": self.price}

    def dispatch(self, envelope):
        from voice_narration._sql import fail
        self.sent.append(deepcopy(envelope))
        if self.drop_dispatch_reply and envelope["type"] == "narration.generate":
            self.drop_dispatch_reply = False
            fail("DEPENDENCY_UNAVAILABLE")

    def config_snapshot(self):
        from voice_narration._sql import fail
        if not self.protection_ready:
            fail("DEPENDENCY_UNAVAILABLE")
        return self.apps["policy"].state.configuration()

    def voice(self, account, profile_id):
        from voice_narration._sql import fail
        response = self.s["profiles"].get("/voices/" + profile_id, headers=headers(self.token))
        if response.status_code >= 400:
            fail(response.json()["error"]["code"])
        value = response.json()
        if value["owner_id"] != account["user_id"]:
            fail("FORBIDDEN")
        return value

    def job(self, account, job_id):
        # Real Jobs-owned authorization port; an internal lookup is not a public request.
        return self.apps["jobs"].state.artifact_job(account, job_id)

    def start(self, enroll=True):
        if enroll:
            value, self.sample = warned(self.s)
            response = override(self.s, value)
            assert response.status_code == 200, response.text
            self.s["voices"].state.run_pending(value["profile_id"])
            self.profile = profile(self.s, value["profile_id"])
            assert self.profile["status"] == "enrolled"
        self.reopen()

    def reopen(self):
        self.stack.close()
        for app in self.apps.values():
            app.state.close()
        self.stack = ExitStack()
        policy_module = importlib.import_module("voice_narration.policy.application")
        self.policy_repository = self.open_store("policy")
        self.apps["policy"] = policy_module.create_app(
            repository=self.policy_repository, authenticate=self.s["auth_app"].state.verify_token,
            authenticate_service=self.service_identity, initial_configuration=deepcopy(self.config),
            emit=lambda event: self.events.append(deepcopy(event)), clock=lambda: self.now[0])
        self.clients["policy"] = self.stack.enter_context(serve(self.apps["policy"]))
        generated = importlib.import_module("voice_narration.artifacts.jobs")
        self.apps["artifacts"] = generated.create_app(
            repository=self.open_store("artifacts", self.s["grants"].authorize),
            authenticate=self.s["auth_app"].state.verify_token,
            authenticate_service=self.service_identity,
            validate_consent=self.s["app"].state.validate_owner_consent,
            job=self.job,
            capability=self.model, configuration=self.config_snapshot, clock=lambda: self.now[0])
        self.clients["artifacts"] = self.stack.enter_context(serve(self.apps["artifacts"]))
        jobs = importlib.import_module("voice_narration.jobs.application")
        self.apps["jobs"] = jobs.create_app(
            repository=self.open_store("jobs", self.s["grants"].authorize),
            authenticate=self.s["auth_app"].state.verify_token,
            authenticate_service=self.service_identity,
            validate_consent=self.s["app"].state.validate_owner_consent,
            voices=self.voice, artifacts=lambda operation, body, deadline:
                self.artifact_command(operation, body, deadline), capability=self.model,
            configuration=self.config_snapshot, policy=self.policy_transport.command,
            estimate=self.estimate, dispatch=self.dispatch,
            execution_permit=lambda: deepcopy(self.provider_permit), clock=lambda: self.now[0])
        protected = policy_module.protect_public(
            self.apps["jobs"], authenticate=self.s["auth_app"].state.verify_token,
            record_request=self.apps["policy"].state.record_request, clock=lambda: self.now[0])
        self.clients["jobs"] = self.stack.enter_context(serve(protected))
        assert self.config_snapshot() == self.config

    def close(self):
        self.stack.close()
        for app in self.apps.values():
            app.state.close()

    def context(self, owner=None):
        return {"owner_id": owner or self.owner, "actor_id": self.owner, "request_id": uid()}

    def internal(self, destination, path, body, *, deadline=None, service_identity=None, **options):
        identity = options.pop("service", service_identity or "worker")
        client = self.clients[destination]
        return client.post(urljoin(str(client.base_url), "/internal/v1" + path), json=body,
                           headers={"Authorization": "Bearer test-only:" + identity,
                                    "X-Deadline": stamp(deadline or (self.now[0] + timedelta(seconds=30)))},
                           **options)

    def artifact_command(self, operation, body, deadline):
        from voice_narration._sql import fail
        response = self.internal("artifacts", "/artifacts/" + operation, body,
                                 deadline=deadline, service_identity="jobs")
        if response.status_code >= 400:
            fail(response.json()["error"]["code"])
        return response.json()

    def body(self, **changes):
        value = {"profile_id": self.profile["profile_id"], "script": SCRIPT,
                 "language": "hi", "style": "neutral"}
        value.update(changes)
        return value

    def submit(self, key=None, body=None, token=None):
        return self.clients["jobs"].post("/jobs", json=body or self.body(),
            headers=dict(headers(token or self.token), **{"Idempotency-Key": key or uid()}))

    def accept(self, key=None, body=None):
        received_at = self.now[0]
        response = self.submit(key, body)
        assert response.status_code == 202, response.text
        value = response.json()
        assert set(value) == {"job_id", "status", "created_at"} and value["status"] == "queued"
        assert value["created_at"] == stamp(received_at)
        return value

    def get(self, job_id, token=None):
        return self.clients["jobs"].get("/jobs/" + job_id, headers=headers(token or self.token))

    def cancel(self, job_id):
        return self.clients["jobs"].post("/jobs/" + job_id + "/cancel", headers=headers(self.token))

    def usage(self):
        response = self.clients["policy"].get("/admin/quotas/user/" + self.owner + "/status",
                                              headers=headers(self.admin))
        assert response.status_code == 200, response.text
        value = response.json()
        assert set(value) == USAGE_FIELDS
        return value

    def put(self, section, changes):
        value = deepcopy(self.config_snapshot())
        value[section].update(changes)
        response = self.clients["policy"].put("/admin/configuration", json=value,
                                               headers=headers(self.admin))
        assert response.status_code == 200, response.text
        value["revision"] += 1
        assert response.json() == value
        self.config = value

    def quota(self, **changes):
        value = dict(self.config["default_user_quota"], **changes)
        response = self.clients["policy"].put("/admin/quotas/user/" + self.owner,
                                              json=value, headers=headers(self.admin))
        assert response.status_code == 200 and response.json() == value
        assert self.usage()["policy"] == value
        return value

    def reserve(self, *, job_id=None, accepted=None, command_id=None, maximum="12", estimate="0.200000"):
        body = {"context": self.context(), "command_id": command_id or uid(),
                "job_id": job_id or uid(), "acceptance_created_at": stamp(accepted or self.now[0]),
                "max_audio_seconds": maximum, "estimated_cost_usd": estimate}
        response = self.internal("policy", "/quotas/reserve", body, service_identity="jobs")
        assert response.status_code == 201, response.text
        value = response.json()
        assert set(value) == {"reservation_id"}
        return dict(body, reservation_id=value["reservation_id"])

    def settle(self, reservation, operation="release-reservation", measured=None, command_id=None,
               context=None, **changes):
        body = {"context": context or reservation["context"], "command_id": command_id or uid(),
                "reservation_id": reservation["reservation_id"], "job_id": reservation["job_id"],
                "cost": measured}
        if operation == "commit-usage":
            body["audio_seconds"] = "5"
        body.update(changes)
        return self.internal("policy", "/quotas/" + operation, body, service_identity="worker")

    def work(self, job_id):
        response = self.internal("jobs", "/jobs/" + job_id + "/work-item",
                                 {"context": self.context(), "command_id": uid()})
        assert response.status_code == 200, response.text
        value = response.json()
        assert set(value) == {"job", "deadline_at", "reservation_id"}
        return value

    def status(self, job_id, before, after):
        return self.internal("jobs", "/jobs/" + job_id + "/status", {
            "context": self.context(), "command_id": uid(), "expected_status": before, "status": after})

    def running(self, job_id):
        work = self.work(job_id)
        for before, after in (("queued", "preparing"), ("preparing", "running")):
            response = self.status(job_id, before, after)
            assert response.status_code == 200 and response.json()["status"] == after
        return work

    def staged(self, job_id, seconds=5, expected=201):
        body = {"context": self.context(), "command_id": uid(), "profile_id": self.profile["profile_id"],
                "job_id": job_id, "kind": "generated"}
        client = self.clients["artifacts"]
        response = client.post(urljoin(str(client.base_url), "/internal/v1/artifacts/store"),
            data={key: json.dumps(value) if isinstance(value, dict) else value for key, value in body.items()},
            files={"file": ("SYNTHETIC_OUTPUT.wav", wav_bytes(np.zeros((1, 16000 * seconds))), "audio/wav")},
            headers={"Authorization": "Bearer test-only:worker",
                     "X-Deadline": stamp(self.now[0] + timedelta(seconds=30))})
        if expected != 201:
            error(response, expected, "OUTPUT_LIMIT_EXCEEDED")
            return None
        assert response.status_code == expected, response.text
        return response.json()["artifact_id"]

    def complete(self, job_id, artifact_id, command_id=None):
        command_id = command_id or uid()
        context = self.command_contexts.setdefault(command_id, self.context())
        body = {
            "context": context, "command_id": command_id,
            "output_artifact_id": artifact_id, "joined_preview_artifact_id": None,
            "duration_seconds": "5", "chunks": [{"chunk_id": uid(), "index": 0,
                "text_start": 0, "text_end": len(SCRIPT),
                "audio_start_seconds": "0", "audio_end_seconds": "5"}], "cost": cost(at=self.now[0])}
        return self.internal("jobs", "/jobs/" + job_id + "/complete",
                             self.complete_bodies.setdefault(command_id, body))

    def event(self, kind, resource_id, payload, producer):
        value = {"message_id": uid(), "type": kind, "schema_version": 1, "owner_id": self.owner,
                 "actor_id": self.owner, "resource_id": resource_id, "occurred_at": stamp(self.now[0]),
                 "sequence": 1, "request_id": uid(), "payload": payload}
        self.apps["jobs"].state.receive(value, producer=producer)
        return value


@pytest.fixture
def world(enrollment_system, stores):
    value = World(enrollment_system, stores)
    try:
        yield value
    finally:
        value.close()


@pytest.mark.integration
def test_acceptance_snapshot_and_durable_replay(world):
    w = world
    w.start()
    key = uid()
    accepted = w.accept(key)
    job = w.get(accepted["job_id"]).json()
    assert set(job) == JOB_FIELDS
    assert job["script_snapshot"] == SCRIPT and job["model"] == MODEL
    assert set(job["controls"]) == {"pause_strength", "speech_pace"}
    assert decimal_is(job["controls"]["pause_strength"], "0.5")
    assert decimal_is(job["controls"]["speech_pace"], "1")
    assert job["status"] == "queued" and job["measured_cost"] is None
    assert job["estimated_cost_usd"] == "0.200000" and job["mapping_available"] is False
    for field in ("output_artifact_id", "joined_preview_artifact_id", "completed_at", "duration_seconds", "failure"):
        assert job[field] is None
    w.now[0] += timedelta(seconds=61)
    w.reopen()
    replay = w.submit(key)
    assert replay.status_code == 202 and replay.json() == accepted
    equivalent = w.body(controls={"speech_pace": "1.0", "pause_strength": "0.50"})
    assert w.submit(key, equivalent).json() == accepted
    error(w.submit(key, w.body(script=SCRIPT + "!")), 409, "IDEMPOTENCY_CONFLICT")
    assert w.usage()["active_jobs"] == 1 and w.usage()["estimated_usd"] == "0.200000"
    assert len(w.estimates) >= 1
    w.s["catalog"].cap["pause_strength"]["default"] = "0.7"
    assert w.submit(key).json() == accepted
    fresh = w.accept()
    assert decimal_is(w.get(fresh["job_id"]).json()["controls"]["pause_strength"], "0.7")


@pytest.mark.integration
def test_concurrent_submit_one_admission_outbox_and_restart(world):
    w = world
    w.start()
    key = uid()
    with ThreadPoolExecutor(max_workers=4) as pool:
        responses = list(pool.map(lambda _: w.submit(key), range(4)))
    assert all(r.status_code == 202 for r in responses)
    assert len({json.dumps(r.json(), sort_keys=True) for r in responses}) == 1
    assert w.usage()["accepted_jobs"] == 1 and decimal_is(w.usage()["reserved_audio_seconds"], "12")
    w.drop_dispatch_reply = True
    w.apps["jobs"].state.dispatch_pending()
    w.reopen()
    w.apps["jobs"].state.dispatch_pending()
    messages = [m for m in w.sent if m["type"] == "narration.generate"]
    assert len(messages) >= 2 and len({m["message_id"] for m in messages}) == 1
    assert len({m["payload"]["job_id"] for m in messages}) == 1
    assert w.usage()["accepted_jobs"] == 1


@pytest.mark.integration
@pytest.mark.parametrize("mutation,status,code", [
    ({"script": ""}, 400, "INVALID_INPUT"),
    ({"script": "🙂" * 1001}, 400, "LIMIT_EXCEEDED"),
    ({"language": "fr"}, 400, "UNSUPPORTED_CAPABILITY"),
    ({"style": "unknown"}, 400, "UNSUPPORTED_CAPABILITY"),
    ({"controls": {"pause_strength": "0.55", "speech_pace": "1"}}, 400, "UNSUPPORTED_CAPABILITY"),
    ({"acceptance_created_at": "2030-01-01T00:00:00Z"}, 400, "INVALID_INPUT"),
    ({"idempotency_key": "body-is-not-header"}, 400, "INVALID_INPUT")])
def test_generation_validation_and_rejection_does_not_bind_key(world, mutation, status, code):
    w = world
    w.start()
    w.accept()
    key = uid()
    error(w.submit(key, w.body(**mutation)), status, code)
    assert w.submit(key).status_code == 202


@pytest.mark.integration
def test_header_limits_owner_scope_and_live_admission_gates(world):
    w = world
    w.start()
    w.accept()
    for key in (None, " ", "x" * 81):
        request_headers = headers(w.token)
        if key is not None:
            request_headers["Idempotency-Key"] = key
        response = w.clients["jobs"].post("/jobs", json=w.body(), headers=request_headers)
        error(response, 400, "IDEMPOTENCY_KEY_REQUIRED")
    error(w.submit(token=w.foreign), 403, "FORBIDDEN")
    w.s["catalog"].model_ready = False
    error(w.submit(), 503, "MODEL_NOT_READY")
    w.s["catalog"].model_ready = True
    w.price_ready = False
    error(w.submit(), 503, "DEPENDENCY_UNAVAILABLE")
    w.price_ready = True
    w.protection_ready = False
    error(w.submit(), 503, "DEPENDENCY_UNAVAILABLE")
    w.protection_ready = True
    w.provider_permit = {"always_on_gpu": True, "approved": False}
    error(w.submit(), 503, "CONFIGURATION_REQUIRED")


@pytest.mark.integration
def test_quantity_admission_time_reprojection_and_active_across_windows(world):
    w = world
    w.start(enroll=False)
    w.quota(window_seconds=60, concurrent_jobs=1)
    accepted = w.now[0]
    reservation = w.reserve()
    assert w.usage()["accepted_jobs"] == 1
    w.now[0] += timedelta(seconds=61)
    assert w.usage()["accepted_jobs"] == 0 and w.usage()["active_jobs"] == 1
    rejected = dict(reservation, context=w.context(), command_id=uid(), job_id=uid())
    rejected.pop("reservation_id")
    error(w.internal("policy", "/quotas/reserve", rejected, service_identity="jobs"),
          429, "CONCURRENCY_EXHAUSTED")
    w.quota(window_seconds=3600, concurrent_jobs=2)
    assert w.usage()["accepted_jobs"] == 1 and decimal_is(w.usage()["reserved_audio_seconds"], "12")
    assert datetime.fromisoformat(w.usage()["window_start"].replace("Z", "+00:00")).timestamp() % 3600 == 0
    w.now[0] += timedelta(seconds=60)
    response = w.settle(reservation, "commit-usage", cost(at=accepted))
    assert response.status_code == 200, response.text
    assert decimal_is(w.usage()["consumed_audio_seconds"], "5") and decimal_is(w.usage()["reserved_audio_seconds"], "0")
    assert w.usage()["active_jobs"] == 0


@pytest.mark.integration
def test_monthly_unknown_hold_first_recognition_and_command_snapshots(world):
    w = world
    w.now[0] = datetime(2030, 1, 31, 23, 59, 50, tzinfo=UTC)
    w.refresh()
    w.start(enroll=False)
    reservation = w.reserve()
    null_command = uid()
    released = w.settle(reservation, command_id=null_command)
    assert released.status_code == 200, released.text
    original = released.json()
    assert original["active_jobs"] == 0 and original["estimated_usd"] == "0.200000"
    assert original["measured_cost"]["total_usd"] == "0.000000"
    w.now[0] = datetime(2030, 2, 1, 0, 0, 1, tzinfo=UTC)
    w.refresh()
    assert w.usage()["estimated_usd"] == "0.200000"
    measured = cost(at=datetime(2030, 1, 31, 23, 59, 55, tzinfo=UTC))
    error(w.settle(reservation, measured=measured, command_id=null_command), 409, "RESULT_CONFLICT")
    known_command = uid()
    known = w.settle(reservation, measured=measured, command_id=known_command)
    assert known.status_code == 200 and known.json()["estimated_usd"] == "0.000000"
    assert w.usage()["measured_cost"]["total_usd"] == "0.120000"
    w.apps["policy"].state.dispatch_pending()
    facts = [m for m in w.events if m["type"] == "usage.recorded"]
    assert len(facts) == 1 and facts[0]["payload"]["cost"] == measured
    error(w.settle(reservation, command_id=known_command), 409, "RESULT_CONFLICT")
    assert w.settle(reservation, command_id=null_command).json() == original
    assert w.settle(reservation).status_code == 200
    assert w.usage()["estimated_usd"] == "0.000000"
    w.apps["policy"].state.dispatch_pending()
    assert len([m for m in w.events if m["type"] == "usage.recorded"]) == 1
    error(w.settle(reservation, measured=cost("0.110000")), 409, "RESULT_CONFLICT")
    error(w.settle(reservation, "commit-usage", measured), 409, "INVALID_STATE")
    w.now[0] = datetime(2030, 3, 1, tzinfo=UTC)
    w.refresh()
    assert w.settle(reservation, measured=measured, command_id=known_command).json() == known.json()
    assert w.settle(reservation, measured=measured).status_code == 200
    assert w.usage()["measured_cost"]["total_usd"] == "0.000000"
    assert w.usage()["estimated_usd"] == "0.000000"
    w.apps["policy"].state.dispatch_pending()
    assert len([m for m in w.events if m["type"] == "usage.recorded"]) == 1


@pytest.mark.integration
def test_reserve_command_ids_admission_fact_and_closed_inputs(world):
    w = world
    w.start(enroll=False)
    reservation = w.reserve()
    original = {k: v for k, v in reservation.items() if k != "reservation_id"}
    repeated = w.internal("policy", "/quotas/reserve", original, service_identity="jobs")
    assert repeated.status_code == 201 and repeated.json() == {"reservation_id": reservation["reservation_id"]}
    assert w.internal("policy", "/quotas/reserve", dict(original, command_id=uid()),
                      service_identity="jobs").json() == repeated.json()
    for field in ("command_id", "acceptance_created_at"):
        for value in (None, "", "bad"):
            changed = dict(original, **{field: value})
            error(w.internal("policy", "/quotas/reserve", changed, service_identity="jobs"),
                  400, "INVALID_INPUT")
        changed = dict(original)
        del changed[field]
        error(w.internal("policy", "/quotas/reserve", changed, service_identity="jobs"),
              400, "INVALID_INPUT")
    for changes in ({"max_audio_seconds": "11"}, {"estimated_cost_usd": "0.300000"},
                    {"acceptance_created_at": stamp(w.now[0] - timedelta(seconds=1))}):
        error(w.internal("policy", "/quotas/reserve", dict(original, command_id=uid(), **changes),
                         service_identity="jobs"), 409, "RESULT_CONFLICT")
    error(w.internal("policy", "/quotas/reserve", dict(original, job_id=uid()),
                     service_identity="worker"), 403, "FORBIDDEN")


@pytest.mark.integration
def test_commit_winner_null_required_and_foreign_accounting_denied(world):
    w = world
    w.start(enroll=False)
    reservation = w.reserve()
    measured = cost(at=w.now[0])
    committed = w.settle(reservation, "commit-usage", measured)
    assert committed.status_code == 200, committed.text
    assert w.settle(reservation, "commit-usage", measured).status_code == 200
    error(w.settle(reservation), 409, "INVALID_STATE")
    error(w.settle(reservation, "commit-usage", cost("0.110000")), 409, "RESULT_CONFLICT")
    foreign = dict(reservation["context"], owner_id=w.foreign["account"]["user_id"])
    error(w.settle(reservation, "commit-usage", measured, context=foreign), 403, "FORBIDDEN")
    error(w.settle(reservation, "commit-usage", measured, audio_seconds="6"), 409, "RESULT_CONFLICT")
    body = {"context": reservation["context"], "command_id": uid(), "job_id": reservation["job_id"],
            "reservation_id": reservation["reservation_id"]}
    error(w.internal("policy", "/quotas/release-reservation", body), 400, "INVALID_INPUT")
    error(w.internal("policy", "/quotas/commit-usage", dict(body, audio_seconds="5", cost=None)),
          400, "INVALID_INPUT")
    for operation in ("commit-usage", "release-reservation"):
        valid = dict(body, cost=measured)
        if operation == "commit-usage":
            valid["audio_seconds"] = "5"
        for invalid in (None, "", "bad"):
            error(w.internal("policy", "/quotas/" + operation, dict(valid, command_id=invalid)),
                  400, "INVALID_INPUT")
        del valid["command_id"]
        error(w.internal("policy", "/quotas/" + operation, valid), 400, "INVALID_INPUT")
    unknown = dict(reservation, reservation_id=uid(), job_id=uid())
    error(w.settle(unknown, measured=measured), 404, "NOT_FOUND")


@pytest.mark.integration
def test_configuration_cas_quota_limits_and_budget_holds(world):
    w = world
    w.start()
    initial = deepcopy(w.config)
    w.put("limits", {"output_max_seconds": "8"})
    error(w.clients["policy"].put("/admin/configuration", json=initial, headers=headers(w.admin)),
          409, "CONFIGURATION_CONFLICT")
    error(w.clients["policy"].put("/admin/configuration", json=w.config, headers=headers(w.token)),
          403, "FORBIDDEN")
    bad = deepcopy(w.config)
    bad["limits"]["output_max_seconds"] = "3000.000001"
    error(w.clients["policy"].put("/admin/configuration", json=bad, headers=headers(w.admin)),
          400, "INVALID_CONFIGURATION")
    w.quota(audio_seconds="6", generation_count=1)
    accepted = w.accept()
    assert decimal_is(w.estimates[-1][1], "6") and decimal_is(w.usage()["reserved_audio_seconds"], "6")
    error(w.submit(), 429, "QUOTA_EXHAUSTED")
    assert w.get(accepted["job_id"]).json()["status"] == "queued"
    assert w.cancel(accepted["job_id"]).status_code == 200
    w.quota(generation_count=10)
    w.put("budget", {"stop_usd": "0.300000"})
    error(w.submit(), 503, "BUDGET_STOPPED")
    w.put("budget", {"stop_usd": "100.000000"})
    unfinished = w.accept()["job_id"]
    w.put("budget", {"kill_switch": True})
    error(w.submit(), 503, "BUDGET_STOPPED")
    error(w.internal("jobs", "/jobs/" + unfinished + "/work-item",
                     {"context": w.context(), "command_id": uid()}), 503, "BUDGET_STOPPED")
    w.reopen()
    assert w.config_snapshot()["budget"]["kill_switch"] is True


@pytest.mark.integration
def test_forecast_uses_known_monthly_spend_and_deduplicates_alerts(world):
    w = world
    w.now[0] = datetime(2030, 1, 2, tzinfo=UTC)
    w.refresh()
    w.start(enroll=False)
    w.put("budget", {"forecast_alert_usd": "2.000000"})
    reservation = w.reserve(estimate="3.000000")
    w.apps["policy"].state.dispatch_pending()
    assert not [m for m in w.events if m["type"] == "budget.forecast_alert"]
    measured = cost(at=w.now[0])
    assert w.settle(reservation, "commit-usage", measured).status_code == 200
    w.apps["policy"].state.dispatch_pending()
    alerts = [m for m in w.events if m["type"] == "budget.forecast_alert"]
    assert len(alerts) == 1 and alerts[0]["payload"] == {
        "forecast_usd": "3.720000", "target_usd": "20.000000"}
    assert w.settle(reservation, "commit-usage", measured).status_code == 200
    w.reopen()
    w.apps["policy"].state.dispatch_pending()
    assert len([m for m in w.events if m["type"] == "budget.forecast_alert"]) == 1


@pytest.mark.integration
def test_lifecycle_completion_cancel_winner_and_one_billing(world):
    w = world
    w.start()
    accepted = w.accept()
    job_id = accepted["job_id"]
    w.running(job_id)
    artifact = w.staged(job_id)
    error(w.clients["artifacts"].get("/artifacts/" + artifact + "/preview-url", headers=headers(w.token)),
          409, "ARTIFACT_UNAVAILABLE")
    response = w.status(job_id, "running", "post_processing")
    assert response.status_code == 200
    command = uid()
    completed = w.complete(job_id, artifact, command)
    assert completed.status_code == 200, completed.text
    value = completed.json()
    assert value["status"] == "completed" and value["output_artifact_id"] == artifact
    assert decimal_is(value["duration_seconds"], "5") and value["measured_cost"] == cost(at=w.now[0])
    assert value["script_snapshot"] == SCRIPT and value["estimated_cost_usd"] == "0.200000"
    assert value["mapping_available"] is True
    chunks = w.clients["jobs"].get("/jobs/" + job_id + "/chunks", headers=headers(w.token))
    assert chunks.status_code == 200 and len(chunks.json()["items"]) == 1
    link = w.clients["artifacts"].get("/artifacts/" + artifact + "/preview-url", headers=headers(w.token))
    assert link.status_code == 200, link.text
    response = w.clients["artifacts"].get(urljoin(str(w.clients["artifacts"].base_url),
                                                  link.json()["url"]), headers=headers(w.token))
    assert response.status_code == 200 and response.content == wav_bytes(np.zeros((1, 80000)))
    error(w.cancel(job_id), 409, "INVALID_STATE")
    assert w.complete(job_id, artifact, command).json() == value
    assert w.usage()["active_jobs"] == 0 and w.usage()["measured_cost"]["total_usd"] == "0.120000"
    cancelled = w.accept()["job_id"]
    w.running(cancelled)
    output = w.staged(cancelled)
    assert w.status(cancelled, "running", "post_processing").status_code == 200
    assert w.cancel(cancelled).json()["status"] == "cancelled"
    assert w.cancel(cancelled).json()["status"] == "cancelled"
    error(w.complete(cancelled, output), 409, "INVALID_STATE")
    assert w.get(cancelled).json()["output_artifact_id"] is None
    assert w.usage()["measured_cost"]["total_usd"] == "0.120000"


@pytest.mark.integration
def test_timeout_retry_same_job_deadline_and_bounded_attempts(world):
    w = world
    w.start()
    accepted = w.accept()
    work = w.running(accepted["job_id"])
    w.apps["jobs"].state.recover()
    w.now[0] += timedelta(seconds=2)
    w.apps["jobs"].state.dispatch_pending()
    w.reopen()
    current = w.work(accepted["job_id"])
    assert current["deadline_at"] == work["deadline_at"]
    assert current["job"]["job_id"] == accepted["job_id"]
    w.now[0] = datetime.fromisoformat(work["deadline_at"].replace("Z", "+00:00"))
    w.refresh()
    w.apps["jobs"].state.recover()
    timed_out = w.get(accepted["job_id"]).json()
    assert timed_out["status"] == "failed" and timed_out["failure"]["code"] == "JOB_TIMEOUT"
    assert timed_out["measured_cost"] is None
    w.apps["jobs"].state.dispatch_pending()
    messages = [m for m in w.sent if m["type"] == "narration.generate"]
    assert 1 <= len({m["message_id"] for m in messages}) <= 2
    assert all(m["payload"]["deadline_at"] == work["deadline_at"] for m in messages)
    assert w.usage()["active_jobs"] == 0 and w.usage()["estimated_usd"] == "0.200000"


@pytest.mark.integration
def test_history_snapshot_cursor_owner_and_terminal_cost_update(world):
    w = world
    w.start()
    ids = [w.accept()["job_id"] for _ in range(3)]
    response = w.clients["jobs"].get("/jobs?limit=2", headers=headers(w.token))
    assert response.status_code == 200, response.text
    first = response.json()
    assert len(first["items"]) == 2 and first["next_cursor"]
    assert [j["job_id"] for j in first["items"]] == sorted(ids, reverse=True)[:2]
    second = w.clients["jobs"].get("/jobs", params={"limit": 2, "cursor": first["next_cursor"]},
                                    headers=headers(w.token)).json()
    assert {j["job_id"] for j in first["items"] + second["items"]} == set(ids)
    error(w.get(ids[0], token=w.foreign), 403, "FORBIDDEN")
    error(w.clients["jobs"].get("/jobs", params={"cursor": first["next_cursor"] + "x"},
                                headers=headers(w.token)), 400, "INVALID_CURSOR")
    work = w.work(ids[0])
    assert w.cancel(ids[0]).status_code == 200
    measured = cost(at=w.now[0])
    assert w.settle({"context": w.context(), "job_id": ids[0],
                     "reservation_id": work["reservation_id"]}, measured=measured).status_code == 200
    work_reference = {"job_id": ids[0], "cost": measured}
    event = w.event("usage.recorded", ids[0], work_reference, "policy")
    w.apps["jobs"].state.receive(event, producer="policy")
    job = w.get(ids[0]).json()
    assert job["status"] == "cancelled" and job["measured_cost"] == measured
    assert job["script_snapshot"] == SCRIPT and job["output_artifact_id"] is None


@pytest.mark.integration
def test_public_request_count_replay_poll_and_internal_exclusion(world):
    w = world
    w.start()
    key = uid()
    before = w.usage()["requests"]
    accepted = w.accept(key)
    assert w.submit(key).status_code == 202
    assert w.get(accepted["job_id"]).status_code == 200
    assert w.usage()["requests"] == before + 3
    w.work(accepted["job_id"])
    assert w.usage()["requests"] == before + 3
    w.quota(request_count=before + 4)
    assert w.get(accepted["job_id"]).status_code == 200
    error(w.get(accepted["job_id"]), 429, "RATE_LIMITED")


@pytest.mark.integration
def test_request_projection_includes_every_authenticated_public_owner(world):
    w = world
    w.start()
    gateway = importlib.import_module("voice_narration.policy.application").protect_public
    before = w.usage()["requests"]
    surfaces = [(w.s["auth_app"], "/auth/me"),
                (w.s["app"], "/consent/" + w.s["consent_record"]["consent_id"]),
                (w.s["voices"], "/voices/" + w.profile["profile_id"]),
                (w.s["artifacts"], "/artifacts/" + w.sample["artifact_id"] + "/preview-url")]
    with ExitStack() as stack:
        for app, path in surfaces:
            client = stack.enter_context(serve(gateway(app,
                authenticate=w.s["auth_app"].state.verify_token,
                record_request=w.apps["policy"].state.record_request, clock=lambda: w.now[0])))
            assert client.get(path, headers=headers(w.token)).status_code == 200
            assert client.get(path).status_code == 401
    assert w.clients["policy"].get("/quotas/me", headers=headers(w.token)).status_code == 200
    assert w.usage()["requests"] == before + 5
    w.now[0] += timedelta(seconds=61)
    assert w.usage()["requests"] == 0
    w.quota(window_seconds=3600)
    assert w.usage()["requests"] == before + 5


@pytest.mark.integration
def test_revocation_purge_minimal_metadata_and_late_accounting(world):
    w = world
    w.start()
    key = uid()
    accepted = w.accept(key)
    job_id = accepted["job_id"]
    work = w.work(job_id)
    failed_body = {"context": w.context(), "command_id": uid(),
                   "failure": {"code": "DEPENDENCY_UNAVAILABLE", "message": "Synthetic failure",
                               "action": "Retry later"}, "cost": None}
    failed = w.internal("jobs", "/jobs/" + job_id + "/fail", failed_body)
    assert failed.status_code == 200 and failed.json()["measured_cost"] is None
    consent = w.s["consent_record"]["consent_id"]
    # Exercise the delivered Consent owner fence. Its public DELETE is owned later.
    revoked = w.s["consent_repo"].fence({"user_id": w.owner, "role": "User"},
        profile_id=w.profile["profile_id"], consent_id=consent, reason="consent_revoked",
        now=w.now[0], cleanup_window_seconds=60)
    w.event("consent.revoked", consent, {"consent_id": consent, "cleanup_id": revoked["cleanup_id"]}, "consent")
    error(w.internal("jobs", "/jobs/" + job_id + "/fail", failed_body), 409, "CONSENT_REVOKED")
    w.now[0] += timedelta(seconds=121)
    w.refresh()
    w.apps["jobs"].state.recover()
    error(w.get(job_id), 404, "NOT_FOUND")
    error(w.internal("jobs", "/jobs/" + job_id + "/fail", failed_body), 404, "NOT_FOUND")
    assert w.submit(key).status_code == 202 and w.submit(key).json() == accepted
    measured = cost(at=w.now[0] - timedelta(seconds=50))
    reservation = {"job_id": job_id, "reservation_id": work["reservation_id"], "context": failed_body["context"]}
    assert w.settle(reservation, measured=measured).status_code == 200
    event = w.event("usage.recorded", job_id, {"job_id": job_id, "cost": measured}, "policy")
    w.reopen()
    w.apps["jobs"].state.receive(event, producer="policy")
    error(w.get(job_id), 404, "NOT_FOUND")
    w.quota(window_seconds=3600)
    assert w.usage()["accepted_jobs"] == 1 and w.usage()["active_jobs"] == 0
    assert w.usage()["measured_cost"]["total_usd"] == "0.120000"
    forbidden = [SCRIPT, w.token["access_token"], "SYNTHETIC_OUTPUT.wav", MODEL["model_id"]]
    for owner in ("policy", "jobs"):
        with psycopg.connect(**w.targets[owner]) as db:
            tables = db.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'").fetchall()
            for (table,) in tables:
                rows = db.execute(sql.SQL("SELECT row_to_json(t)::text FROM {} t").format(sql.Identifier(table))).fetchall()
                content = "\n".join(row[0] for row in rows)
                assert all(value not in content for value in forbidden), (owner, table)
                for (serialized,) in rows:
                    value = json.loads(serialized)
                    if table == "jobs_cleanups":
                        # Delivered cleanup fences already contain these identity columns;
                        # they are not the new account-lifetime accounting/retry ledger.
                        value.pop("profile_id", None)
                        value.pop("consent_id", None)
                    retained = json.dumps(value)
                    assert w.profile["profile_id"] not in retained and consent not in retained, (owner, table)


@pytest.mark.integration
def test_internal_deadline_identity_and_transition_conflicts(world):
    w = world
    w.start()
    job_id = w.accept()["job_id"]
    w.running(job_id)
    error(w.status(job_id, "running", "preparing"), 409, "INVALID_STATE")
    body = {"context": w.context(), "command_id": uid()}
    error(w.internal("jobs", "/jobs/" + job_id + "/work-item", body,
                     deadline=w.now[0] - timedelta(seconds=1)), 503, "DEADLINE_EXCEEDED")
    foreign = dict(body, context=w.context(w.foreign["account"]["user_id"]))
    error(w.internal("jobs", "/jobs/" + job_id + "/work-item", foreign), 403, "FORBIDDEN")
    error(w.internal("jobs", "/jobs/" + job_id + "/work-item", body,
                     service_identity="audit"), 403, "FORBIDDEN")


@pytest.mark.integration
def test_lost_policy_ack_recovery_one_admission_and_settlement(world):
    w = world
    w.start()
    key = uid()
    w.policy_transport.lose_reply = "reserve"
    error(w.submit(key), 503, "DEPENDENCY_UNAVAILABLE")
    w.reopen()
    accepted = w.accept(key)
    assert w.usage()["accepted_jobs"] == 1 and w.usage()["estimated_usd"] == "0.200000"
    job_id = accepted["job_id"]
    w.running(job_id)
    artifact = w.staged(job_id)
    assert w.status(job_id, "running", "post_processing").status_code == 200
    command = uid()
    w.policy_transport.lose_reply = "commit-usage"
    error(w.complete(job_id, artifact, command), 503, "DEPENDENCY_UNAVAILABLE")
    w.reopen()
    assert w.complete(job_id, artifact, command).status_code == 200
    assert w.usage()["measured_cost"]["total_usd"] == "0.120000"
    assert w.usage()["active_jobs"] == 0 and w.usage()["estimated_usd"] == "0.000000"


@pytest.mark.integration
def test_commit_release_race_one_quantity_and_money_winner(world):
    w = world
    w.start(enroll=False)
    reservation = w.reserve()
    measured = cost(at=w.now[0])
    with ThreadPoolExecutor(max_workers=2) as pool:
        commit = pool.submit(w.settle, reservation, "commit-usage", measured)
        release = pool.submit(w.settle, reservation, "release-reservation", measured)
        responses = [commit.result(), release.result()]
    assert sorted(r.status_code for r in responses) == [200, 409]
    loser = next(r for r in responses if r.status_code == 409)
    error(loser, 409, "INVALID_STATE")
    usage = w.usage()
    assert usage["active_jobs"] == 0 and decimal_is(usage["reserved_audio_seconds"], "0")
    assert decimal_is(usage["consumed_audio_seconds"], "5" if responses[0].status_code == 200 else "0")
    assert usage["measured_cost"]["total_usd"] == "0.120000"


@pytest.mark.integration
def test_complete_cancel_race_one_publication_winner(world):
    w = world
    w.start()
    job_id = w.accept()["job_id"]
    w.running(job_id)
    artifact = w.staged(job_id)
    assert w.status(job_id, "running", "post_processing").status_code == 200
    with ThreadPoolExecutor(max_workers=2) as pool:
        complete = pool.submit(w.complete, job_id, artifact)
        cancel = pool.submit(w.cancel, job_id)
        responses = [complete.result(), cancel.result()]
    assert sorted(r.status_code for r in responses) == [200, 409]
    job = w.get(job_id).json()
    assert job["status"] == ("completed" if responses[0].status_code == 200 else "cancelled")
    assert job["output_artifact_id"] == (artifact if job["status"] == "completed" else None)
    assert w.usage()["active_jobs"] == 0
    link = w.clients["artifacts"].get("/artifacts/" + artifact + "/preview-url", headers=headers(w.token))
    if job["status"] == "completed":
        assert link.status_code == 200
        assert w.usage()["measured_cost"]["total_usd"] == "0.120000"
    else:
        assert link.status_code in (404, 409)
        assert w.usage()["measured_cost"]["total_usd"] == "0.000000"


@pytest.mark.integration
def test_missing_durable_policy_facts_never_become_zero(world):
    w = world
    w.start()
    w.accept()
    assert w.usage()["active_jobs"] == 1
    w.policy_repository.close()
    response = w.clients["policy"].get("/admin/quotas/user/" + w.owner + "/status", headers=headers(w.admin))
    error(response, 503, "DEPENDENCY_UNAVAILABLE")
    error(w.submit(), 503, "DEPENDENCY_UNAVAILABLE")
    w.reopen()
    assert w.usage()["active_jobs"] == 1 and w.usage()["estimated_usd"] == "0.200000"


@pytest.mark.integration
def test_default_window_change_override_replacement_and_system_concurrency(world):
    w = world
    w.start(enroll=False)
    reservation = w.reserve()
    w.now[0] += timedelta(seconds=61)
    assert w.usage()["accepted_jobs"] == 0
    w.put("default_user_quota", {"window_seconds": 3600})
    assert w.usage()["accepted_jobs"] == 1
    w.quota(window_seconds=60)
    assert w.usage()["accepted_jobs"] == 0
    w.quota(window_seconds=3600, concurrent_jobs=1)
    assert w.usage()["accepted_jobs"] == 1 and w.usage()["active_jobs"] == 1
    value = deepcopy(w.config)
    value["system_concurrent_jobs"] = 1
    response = w.clients["policy"].put("/admin/configuration", json=value, headers=headers(w.admin))
    assert response.status_code == 200
    value["revision"] += 1
    w.config = value
    foreign = w.foreign["account"]["user_id"]
    body = {"context": {"owner_id": foreign, "actor_id": foreign, "request_id": uid()},
            "command_id": uid(), "job_id": uid(), "acceptance_created_at": stamp(w.now[0]),
            "max_audio_seconds": "12", "estimated_cost_usd": "0.200000"}
    error(w.internal("policy", "/quotas/reserve", body, service_identity="jobs"),
          429, "CONCURRENCY_EXHAUSTED")
    assert w.settle(reservation).status_code == 200
    assert w.internal("policy", "/quotas/reserve", body, service_identity="jobs").status_code == 201


@pytest.mark.integration
@pytest.mark.parametrize("invalid", [
    {"compute_usd": 0.1}, {"compute_usd": "-0.100000"},
    {"total_usd": "0.999999"}, {"storage_usd": "0.0200001"}])
def test_cost_wire_validation_exact_decimal_totals(world, invalid):
    w = world
    w.start(enroll=False)
    good = w.reserve()
    assert w.settle(good, "commit-usage", cost(at=w.now[0])).status_code == 200
    other = w.reserve()
    error(w.settle(other, "commit-usage", dict(cost(at=w.now[0]), **invalid)), 400, "INVALID_INPUT")
    assert w.usage()["measured_cost"]["total_usd"] == "0.120000"


@pytest.mark.integration
def test_repeated_crash_attempt_budget_includes_initial_and_preserves_deadline(world):
    w = world
    w.start()
    job_id = w.accept()["job_id"]
    w.apps["jobs"].state.dispatch_pending()
    original = w.running(job_id)
    w.reopen()
    w.apps["jobs"].state.recover()
    before = sum(m["type"] == "narration.generate" for m in w.sent)
    w.apps["jobs"].state.dispatch_pending()
    assert sum(m["type"] == "narration.generate" for m in w.sent) == before
    w.now[0] += timedelta(seconds=2)
    w.apps["jobs"].state.dispatch_pending()
    retry = w.work(job_id)
    assert retry["deadline_at"] == original["deadline_at"]
    assert retry["job"]["job_id"] == job_id
    messages = [m for m in w.sent if m["type"] == "narration.generate"]
    assert len({m["message_id"] for m in messages}) == 2
    w.reopen()
    w.apps["jobs"].state.recover()
    w.now[0] += timedelta(seconds=2)
    w.apps["jobs"].state.dispatch_pending()
    failed = w.get(job_id).json()
    assert failed["status"] == "failed" and failed["failure"] is not None
    assert failed["failure"]["code"] == "RETRY_EXHAUSTED"
    assert w.now[0] < datetime.fromisoformat(original["deadline_at"].replace("Z", "+00:00"))
    assert len({m["message_id"] for m in w.sent if m["type"] == "narration.generate"}) == 2
    assert w.usage()["active_jobs"] == 0 and w.usage()["estimated_usd"] == "0.200000"


@pytest.mark.integration
def test_actual_output_overrun_is_rejected_without_publication(world):
    w = world
    w.start()
    job_id = w.accept()["job_id"]
    w.running(job_id)
    assert w.staged(job_id)
    w.staged(job_id, seconds=13, expected=400)
    assert w.get(job_id).json()["output_artifact_id"] is None
    assert decimal_is(w.usage()["reserved_audio_seconds"], "12")


@pytest.mark.integration
def test_profile_readiness_and_immediate_consent_fence_before_event_delivery(world):
    w = world
    w.start()
    job_id = w.accept()["job_id"]
    pending = create_profile(w.s, [w.sample])
    assert pending.status_code == 202
    error(w.submit(body=w.body(profile_id=pending.json()["profile_id"])), 409, "PROFILE_NOT_READY")
    w.s["catalog"].model_ready = False
    error(w.internal("jobs", "/jobs/" + job_id + "/work-item",
                     {"context": w.context(), "command_id": uid()}), 503, "MODEL_NOT_READY")
    w.s["catalog"].model_ready = True
    w.s["consent_repo"].fence({"user_id": w.owner, "role": "User"},
        profile_id=w.profile["profile_id"], consent_id=w.s["consent_record"]["consent_id"],
        reason="consent_revoked", now=w.now[0], cleanup_window_seconds=60)
    error(w.submit(), 409, "CONSENT_REVOKED")
    error(w.internal("jobs", "/jobs/" + job_id + "/work-item",
                     {"context": w.context(), "command_id": uid()}), 409, "CONSENT_REVOKED")


@pytest.mark.integration
def test_unicode_scalar_limit_and_pinned_job_snapshot_after_limits_lowered(world):
    w = world
    w.start()
    text = "🙂" * 1000
    accepted = w.accept(body=w.body(script=text))
    assert w.get(accepted["job_id"]).json()["script_snapshot"] == text
    w.put("limits", {"script_max_characters": 10, "output_max_seconds": "4"})
    error(w.submit(body=w.body(script=text)), 400, "LIMIT_EXCEEDED")
    assert w.get(accepted["job_id"]).json()["status"] == "queued"
    assert decimal_is(w.usage()["reserved_audio_seconds"], "12")


@pytest.mark.integration
def test_jobs_carries_canonical_acceptance_time_across_delayed_policy_receipt(world):
    w = world
    w.start()
    w.now[0] += timedelta(seconds=59)
    w.policy_transport.reserve_delay_seconds = 2
    accepted = w.accept()
    call = next(body for operation, body, deadline in w.policy_transport.calls if operation == "reserve")
    assert call["acceptance_created_at"] == accepted["created_at"]
    assert call["acceptance_created_at"] != stamp(w.now[0])
    assert w.usage()["accepted_jobs"] == 0 and w.usage()["active_jobs"] == 1
    w.quota(window_seconds=3600)
    assert w.usage()["accepted_jobs"] == 1


@pytest.mark.integration
def test_job_history_granted_administrator_read_rechecks_revocation(world):
    w = world
    w.start()
    job_id = w.accept()["job_id"]
    client = w.clients["jobs"]
    path = "/jobs/" + job_id
    error(client.get(path, params={"owner_id": w.owner}, headers=headers(w.admin)), 403, "FORBIDDEN")
    grant = {"grant_id": uid(), "owner_id": w.owner,
             "administrator_id": w.admin["account"]["user_id"], "scopes": ["jobs:read"],
             "created_at": w.now[0], "expires_at": w.now[0] + timedelta(seconds=60), "revoked_at": None}
    actor = {"user_id": w.owner, "role": "User"}
    w.s["grants"].save_grant(actor, grant, now=w.now[0])
    response = client.get(path, params={"owner_id": w.owner}, headers=headers(w.admin))
    assert response.status_code == 200 and response.json()["script_snapshot"] == SCRIPT
    w.s["grants"].revoke_grant(actor, grant["grant_id"], now=w.now[0])
    error(client.get(path, params={"owner_id": w.owner}, headers=headers(w.admin)), 403, "FORBIDDEN")
```

## Planning-time dry-run evidence — blocked, not milestone execution

No approved milestone was executed. All checks ran in disposable copies outside the working tree with the existing .venv. F1 is superseded by the exact proposed F2 above. F2 has not been imported, compiled, collected or executed; no F2 helper/probe/runtime result is claimed.

### Actual attempt history

| Attempt | Real result / interpretation |
| --- | --- |

| Initial sandbox command: python -m pytest -p no:anyio -q -x tests/test_job_orchestration.py | Docker named-pipe permission denied on up and cleanup;1 setup error7.49s. Not RED. No Docker lifecycle workaround. Normal host-context review allowed isolated commands. |

| Exploratory host -q -x |1 missing-Policy failure104.64s after actual owner prerequisites. Draft changed during this exploratory run, so mismatched linecache output is not frozen exact-code evidence. |

| F1 py_compile / collection | Success;38 actual identities collected6.60s, no skips/xfails. These observations apply to F1 only. |

| F1 frozen RED1 |38 missing policy.application failures741.40s, exit1, identical target hash before/after, successful fixture teardown. Valid intended-interface diagnostic for F1; not approved milestone evidence. |

| F1 frozen RED2 |38 failures1553.70s, exit1:37 missing policy.application,1 httpx.ReadTimeout in test_profile_readiness_and_immediate_consent_fence_before_event_delivery during unchanged warned→create_profile POST/voices. Equal F1 hashes and successful teardown. This is NOT a valid complete repeated RED run. |

| Signature-only F1 scratch copy | compileall exit0. Exact acceptance test reaches404 !=202,1failed167.13s, proving factories bind and signatures alone do not deliver behavior. |

| Minimal real-SQL F1 admission probe, independent copy | Exact same test passes61.67s and68.19s without manual cleanup between runs. Actual Auth/Consent/Profile/enrollment and owner PG; admission/immutability/61-second restart/Decimal equivalence/conflict/pinned-default/new-default path only. No broader GREEN claim. |

| Independent preserved97 baseline |97passed978.22s, exit0; original target uncollected. |

| Independent preserved97 after F1-only replacement |95passed2failed1573.64s, exit1. Same97 IDs and unchanged42 post-copy hashes. Job module was not collected. Failures are httpx.ReadTimeout on unchanged POST/api/v1/voices in test_profile_limits_filters_and_stable_snapshot (line694) and test_nondefault_pagination_controls_both_handlers (line750). No assertion mismatch; cause unestablished. No retry or source/timeout change. |

The source hash helper in the independent regression preparation initially normalized LF, then was corrected to raw bytes before any copy/run; an unresolved relative-source helper path was corrected before target replacement. These mechanical preparation corrections changed no source or criteria. Automatic approval review also hit a usage-limit error before the soundness helper was created; that action did not execute. The user's explicit retry resumed saved work rather than rerunning the active process.

F1RED2 and the separate post97 were concurrent with isolated UUID projects. Resource contention is only a hypothesis, not an established cause. A scoped read-only liveness query (CIM first denied by sandbox, then host context) showed the exact pytest process's CPU/IO counters advancing; no process was signalled or rerun.

### Exact commands and trimmed real output

Interpreter: C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe. Feature cwd was the018-job-red-planning-59635758562d40f19e559dd8112290d4 disposable root under the stable visualization directory; signature/probe cwd were its soundness/admission-probe children.


evidence/attempt1-host.txt:

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe -u -m pytest -p no:anyio -q -x tests/test_job_orchestration.py
1 failed in 104.64s (0:01:44)
EXIT: 1
```


evidence/frozen-red-1.txt:

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe -u -m pytest -p no:anyio -q --tb=short tests/test_job_orchestration.py
TARGET_BEFORE: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
38 failed in 741.40s (0:12:21)
TARGET_AFTER: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
EXIT: 1
```


evidence/frozen-red-2.txt:

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe -u -m pytest -p no:anyio -q --tb=short tests/test_job_orchestration.py
TARGET_BEFORE: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
38 failed in 1553.70s (0:25:53)
TARGET_AFTER: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
EXIT: 1
```


soundness/evidence/signature-stub-feature.txt:

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe -u -m pytest -p no:anyio -q --tb=short tests/test_job_orchestration.py::test_acceptance_snapshot_and_durable_replay
TARGET_BEFORE: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
1 failed in 167.13s (0:02:47)
TARGET_AFTER: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
EXIT: 1
```


admission-probe/evidence/admission-probe.txt:

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe -u -m pytest -p no:anyio -q --tb=short tests/test_job_orchestration.py::test_acceptance_snapshot_and_durable_replay
TARGET_BEFORE: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
1 passed in 61.67s (0:01:01)
TARGET_AFTER: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
EXIT: 0
```


admission-probe/evidence/admission-probe-repeat.txt:

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.venv\Scripts\python.exe -u -m pytest -p no:anyio -q -rA --tb=short tests/test_job_orchestration.py::test_acceptance_snapshot_and_durable_replay
TARGET_BEFORE: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
1 passed in 68.19s (0:01:08)
TARGET_AFTER: c775af7493abd10009515f08b739cdec8d629814dee558b43b8c980d989dee97
EXIT: 0
```


Other actual preparation commands were python evidence/prepare_soundness.py; python -m compileall -q voice_narration tests/test_job_orchestration.py in soundness; python evidence/prepare_probe.py; and the same compileall command in admission-probe. Both compileall commands exited0 with empty output. They operated only on scratch source/stubs/probes, not working production. The independent97 command, from its retained separate copy, was:

```text
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py -q -rA
97 passed in 978.22s (0:16:18)
2 failed, 95 passed in 1573.64s (0:26:13)
```


### F2 planning correction and remaining verification

The two precise corrections avoid imposing an Audit-before/after-execution order: lose one reply only for narration.generate, and compare only narration.generate counts while checking retry delay. This changes three lines, no import, fixture infrastructure, test identity, product rule or completion criterion. Full exact F2 is above. Mechanical text diff only; no F2 runtime validation occurred.

```diff
--- F1
+++ F2
@@ -143,7 +143,7 @@
     def dispatch(self, envelope):
         from voice_narration._sql import fail
         self.sent.append(deepcopy(envelope))
-        if self.drop_dispatch_reply:
+        if self.drop_dispatch_reply and envelope["type"] == "narration.generate":
             self.drop_dispatch_reply = False
             fail("DEPENDENCY_UNAVAILABLE")
 
@@ -991,9 +991,9 @@
     original = w.running(job_id)
     w.reopen()
     w.apps["jobs"].state.recover()
-    before = len(w.sent)
+    before = sum(m["type"] == "narration.generate" for m in w.sent)
     w.apps["jobs"].state.dispatch_pending()
-    assert len(w.sent) == before
+    assert sum(m["type"] == "narration.generate" for m in w.sent) == before
     w.now[0] += timedelta(seconds=2)
     w.apps["jobs"].state.dispatch_pending()
     retry = w.work(job_id)
```


On 2026-10-29 (client date; recorded 2026-10-30T01:53:22Z), the user explicitly selected “Investigate and retry sequentially” for the named timeout findings. This authorizes read-only investigation and sequential validation with unchanged runtime code. It does not approve this Implementation Plan for milestone execution, waive either failed result, alter timeouts or acceptance criteria, or authorize concurrent validation runs. The unchanged 97-case regression runs first; remaining F2 planning checks follow only after its successful completion. A new unresolved verification failure stops the retry.

The authorized sequential retry finished with **95 passed, 2 failed in1558.65s (exit1)**. Both failures are real HTTPX ReadTimeouts under the unchanged10-second client timeout: test_guidance_formats_playback_admission_and_originals on POST /api/v1/artifacts/upload (test line252/helper171), and test_profile_limits_filters_and_stable_snapshot on POST /api/v1/voices (test line694/helper206). The earlier failed test_nondefault_pagination_controls_both_handlers passed in this retry. No assertion mismatch or root cause is established; the changed failure pair is recorded without a causal claim. All42 frozen inputs and the same97 node identities were preserved. The original Job test remained uncollected. No timeout was relaxed, production source changed, failure waived, or further retry launched.

The sequential worker has fully finished. All9 exact owned-project container/network/volume queries returned empty. Its durable [sequential recovery evidence](C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/019-job-regression-sequential-4a03ba7bf9fb42d682c640c575aeff8c-evidence) contains the investigation, approval, full output, unchanged-input proof and cleanup. sequential97.txt raw SHA256 is `cf22725fdf9e21d23a9365833ac7f77176c94ede3d79ce2b2e481127c3afd28a`. A complete [frozen42 snapshot](C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/019-job-regression-sequential-4a03ba7bf9fb42d682c640c575aeff8c-frozen42) and manifest are retained for reproducible future work; no current external source is silently substituted.

Pending after this failed recovery: explicit human disposition of the unresolved verification failures; F2 py_compile/collection; raw helper Audit-first/fault-once/retry-ACK check; exact F2 RED twice with successful prerequisites; F2 signature/selected admission soundness; final unchanged-input proof for any carried97 evidence. F2 SHA256 remains `ef4393e3079028db3f30ebc8f87d5f5991d9edece161f80f1398fc7682f30c3d`. No F2 runtime, compile, collection, helper or probe was launched, and no F2 disposable copy was recreated while the sequential worker held the runtime baton. Earlier failed results remain preserved. The user authorized validation recovery only; this failed retry does not authorize milestone execution or another retry.

For a later explicitly authorized F2 RED run, the agreed output-only diagnostic command is `python -m pytest -p no:anyio -v --tb=short tests/test_job_orchestration.py`, preserving the same38 nodes, fixtures, timeouts and criteria while flushing individual test progress. Earlier -q command outputs above remain historical, not relabelled as -v results. This command has not run on F2.

The implementation-planning skill's Pre-existing Failures rule requires: ‘report it, and ask the user before approval how the Acceptance / Completion Criteria treat it.’ [Exact skill](C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0/skills/implementation-planning/SKILL.md). No acceptable-failure exception or new FOUNDATION is silently invented.


### Preservation, exports and cleanup

All78 protected non-Plan files remain raw-byte equal to the79-file planning manifest, including working tests/source/configuration; Plan.md alone changed concurrently through external summary claims, preserved and not edited by this planner. The actual working Job test is still the original0576e9c15b1e9135c34119e4737b55f18df47c32ad8acb99e38c452c11056436. This planner wrote only019 in the workspace and performed no commit/push. External commits/files are not approval.


Feature/stub/probe evidence export: [evidence folder](C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/019-job-planning-evidence-59635758562d40f19e559dd8112290d4). Independent baseline/post97 evidence: [regression evidence](C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/019-job-regression-5e61bbb1d9ef49768c101869d83a4120-evidence). Full logs, exact hashes, manifests, F1/F2 bytes/diff and reusable scratch-only probe/helper inputs are retained outside the repository for the pending disposition. These are planning diagnostics, not installed production or milestone success.


All15 exact-label read-only container/network/volume checks were empty for these completed projects:

```text
vnred2e89673fb2a0456ab3ca15d1e3c8f02b
vnred39dfdf86176648019b7965fefea45540
vnred80478dc3c2bc43788214e30600409493
vnreda37059c225c9433d81d6d50c7db89c41
vnredcb58922ed89d464f99bbf728e6ef54cc
```
The first positive probe used normal pytest capture, so its project ID was not printed; its fixture teardown completed without errors. The repeat printed its ID and explicit empty label checks are recorded. No user Docker/engine/other project lifecycle was touched. After the durable evidence export, the disposable source/test/stub/probe root was resolved and verified as the exact direct child018-job-red-planning-59635758562d40f19e559dd8112290d4 of the named stable visualization root, then removed using native PowerShell Remove-Item -LiteralPath. The matching owned marker was removed. Actual result: `Disposable copy exists after cleanup: False`. Evidence exports remain outside the repository; only019 was written by this planner in the workspace.


| Exported actual log | Raw SHA256 |
| --- | --- |

| evidence/attempt1-host.txt | d84c4108b2e1e6de8c0fb196b234152701fa72575550248c2d1d7436fd0cd8ac |

| evidence/frozen-red-1.txt | 61c19666141f7a1246809c53a0ab73ec26ddd1500814a4920a30625d7881236b |

| evidence/frozen-red-2.txt | 361b5bb8ecd8754f45b8e31eef6140f38b74ccc4e925b09e65c92fab11ddcc66 |

| soundness/evidence/signature-stub-feature.txt | 05ab3c5b6618d8a4467cc0df006d1311971cd8a2769a6d3fa2a0754ac05e5a35 |

| admission-probe/evidence/admission-probe.txt | 8ec375a0b9320cdee1799264f1a44df3ed40143cd8c1a307f7a893212795d4d6 |

| admission-probe/evidence/admission-probe-repeat.txt | 466285f873db70b96edfc4c5b30394110c8368819d626b06feb64396693b53f7 |


Final per-file review: tests/test_job_orchestration.py has complete final replacement content, with no placeholders/skips/catch-all success, matching the one-file Proposed Changes scope. Its exact F2 bytes match the exported proposal. No source/configuration/dependency changes are proposed. Syntax/behavior for F2 remains pending under the explicit blocker, rather than claimed from F1.

### Targeted diagnostic authorization — 2026-10-30

At the user's explicit approval (recorded 2026-10-30T13:00:04Z), run only `tests/test_voice_enrollment.py::test_guidance_formats_playback_admission_and_originals` and `tests/test_voice_enrollment.py::test_profile_limits_filters_and_stable_snapshot` once in a fresh isolated copy of the retained, hash-verified 42-file baseline. A scratch-only stdlib thread-stack sampler may capture stack locations and timing without locals. Runtime source, tests, assertions, and the 10-second client timeout remain unchanged. Preserve prior failures, commands, actual results, and cleanup evidence. No automatic retry, full-suite run, F2 validation, or milestone execution is authorized by this diagnostic approval. This is investigation of the unresolved timeouts, not a waiver or a proposed production change.

### Targeted diagnostic result — 2026-10-30

The authorized two-test run completed with **2 failed in 182.36 seconds**, both unchanged 10-second HTTP receive-header timeouts. All 42 input hashes remained unchanged. No retry, timeout change, source fix, or F2 validation followed. [Diagnostic evidence and precise observations](C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/019-enrollment-stack-diagnostic-6f13b9e399324e4796dfcac82236ba9c-evidence/diagnostic-summary.json).

The 89 timestamped all-thread stack samples repeatedly locate active server work in `voices/quality.py:106`, `converter.resample(frame)`, during both the upload and profile-create requests while the client awaited headers. Server progress also appears after the client timeout; this is not evidence of a permanent deadlock. Other samples include database waits. Sampling overhead was not measured separately, so neither the complete request delay nor a native-library root cause is established by these stacks.

Frozen-source inspection shows a new format-conversion resampler is constructed inside the decoded-frame loop, while profile creation decodes the sample through artifact retrieval and then again in the profile handler. These are investigation targets, not verified causes. A possible next experiment, **not yet authorized or run**, is standalone staged timing on the exact synthetic WAV: decoding, converter construction/resampling, and analysis; compare per-frame construction against per-stream reuse and verify identical decoded arrays. This changes no proposed acceptance criterion and authorizes no production optimization. The Job RED planning validation remains blocked.

## Human Review

Status: Awaiting human approval.

Only approval of this exact completed document authorizes its test-only milestone execution. No approval is inferred from external prototypes or earlier generic approvals.
