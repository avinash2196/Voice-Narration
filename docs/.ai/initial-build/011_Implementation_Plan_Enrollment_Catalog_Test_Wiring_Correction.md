# Implementation Plan — Enrollment Catalog Test-Wiring Correction

## Milestone

Milestone 11 of initial-build: Enrollment Catalog Test-Wiring Correction. Predecessor: completed Voice Enrollment RED (milestone 10, artifact 010).

## Milestone Type

OTHER. Approved Plan.md milestone 11 explicitly assigns no product requirement ownership or production behavior change: only test collaborator wiring and its internal interface documentation. This artifact proposes implementation; it does not execute it. If production behavior is needed, stop and return for RED/GREEN planning.

## Authoritative References

References are repository-relative unless prefixed with the installed plugin root. Inspected 2026-10-26. Approval records below are historical authority, not new verification.

| Reference | Approval / authority |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Q11 revision approved by avinash2196, 2026-10-25T21:07:15Z; unchanged product scope. |
| docs/.ai/initial-build/Plan.md | Current 27-milestone revision approved by avinash2196, 2026-10-26T16:09:38Z; milestones 1–10 complete, milestone 11 Pending, GREEN next. Milestone 11 baseline, preservation and passing completion rules govern. |
| docs/.ai/initial-build/contract/API-Contract.md | Baseline approved 2026-10-24; Q11 amendment approved 2026-10-25T21:30:20Z. Models/policy/audit already requires enabled/approved catalog listing; service ownership and public behavior unchanged. CONTRACT rows complete. |
| docs/.ai/initial-build/Enrollment-Catalog-Seam-Correction-Proposal.md | Approved by avinash2196, recorded 2026-10-26T04:12:59Z; exact diff, required enumeration collaborator and correction review sequence. |
| docs/.ai/initial-build/Enrollment-Quality-Policy-Proposal.md | Approved 2026-10-25T21:03:55Z; preserves real acoustic checks and separate human calibration gates. |
| docs/.ai/initial-build/001_Implementation_Plan_Foundation.md | Executed and verified under human approval; general runtime/tooling/isolation decisions carried forward. |
| docs/.ai/initial-build/002_Implementation_Plan_Model_Feasibility.md | Executed assessment under human approval; investigation-only model selection, no production licensing or enablement. |
| docs/.ai/initial-build/003_Implementation_Plan_Persistence_RED.md | Historical executed RED; recovery follows in 004. |
| docs/.ai/initial-build/004_Implementation_Plan_Persistence_RED_Recovery.md | Historical completed recovery RED under approval; actual owner-store fixtures remain authoritative test source. |
| docs/.ai/initial-build/005_Implementation_Plan_Persistence_GREEN.md | Historical approved implementation; verified completion through 006. |
| docs/.ai/initial-build/006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Historical approved verification completion and exact preservation protocol. |
| docs/.ai/initial-build/007_Implementation_Plan_Authentication_Consent_RED.md | Historical approved/executed RED; real transport, canonical identity and consent fixture decisions retained. |
| docs/.ai/initial-build/008_Implementation_Plan_Authentication_Consent_GREEN.md | Historical approved/executed GREEN; delivered identity/consent boundaries and passing regression evidence. |
| docs/.ai/initial-build/009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved/executed FOUNDATION; pinned permitted evaluator, actual native/codec prerequisites, no calibration claim. |
| docs/.ai/initial-build/010_Implementation_Plan_Voice_Enrollment_RED.md | Approved/executed RED, approval recorded 2026-10-25T22:44:13Z. Complete original tests/interface remain immutable history. |
| voice_narration_PDD_requirements.md | Retained non-conflicting product baseline through requirements.md; no amendment here. |
| docs/.ai/initial-build/Contract-Review.md | Historical intermediate review; later approved contract governs. |
| tests/test_voice_enrollment.py; tests/test_enrollment_quality.py; tests/test_persistence.py; tests/test_authentication_consent.py; pytest.ini | Current executable source/configuration inspected as repository facts, not new requirements. |
| Installed commands/create-implementation-plan.md; agents/planner.md | Process instructions. |
| Installed skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/prompt-driven-development/templates/Implementation-Plan.md; skills/testing/SKILL.md; skills/security/SKILL.md; skills/requirements-analysis/SKILL.md | Process/template/domain guidance; active user restriction permits static checks only during planning. |

Installed root: C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0. No workspace AGENTS.md or product-level docs/requirements.md was found. No approved unexecuted Implementation Plan for milestone 11 exists; 011 is the next artifact number. Explicit authorization, observed facts and future predicted evidence are distinguished below; no new material product decision is needed for this proposal-authorized delta.

## Carried-Forward Decisions

001 retains project CPython 3.13.17/.venv, pytest 9.1.1, HTTPX real transport, PostgreSQL 18.6/Psycopg, NumPy/PyAV, Compose and fresh unique store/container/port/path isolation. No dependency selection or version change occurs. 002 retains model investigation-only status and separate commercial/runtime approval. 003/004/005/006 retain owner-store isolation, fixture cleanup and exact preservation; 007/008 retain delivered real authentication/consent and canonical IDs. 009 retains actual pinned evaluator identity, no substitute detector and no production calibration claim. 010 retains all test assertions, test identities, six quality/fifteen enrollment cases, scheduler diagnostics and keyed capability lookup. Its factory signature gains only the proposal-authorized listing keyword documented here. The new signature does not retroactively modify 010 or its execution evidence.

## Preconditions / Predecessor Evidence

Plan.md Voice Enrollment RED execution evidence records baseline 57/57 twice (87.92s, 86.94s), 21 intended missing-module setup errors twice (27.28s, 26.82s), then 57/57 twice (115.66s, 111.42s), exact test contents/preservation and owned-resource cleanup. Six errors were at voice_narration.voices.quality; fifteen at voice_narration.artifacts.application. Later fixture bodies/factory wiring were not reached. These historical errors establish neither soundness of later runtime bodies nor enrollment success. They are not rerun or relabeled as passing OTHER evidence.

Before any execution-time edit, capture the exact current hashes and absent listing seam, compare current enrollment source to historical 010, capture a complete in-scope repository preservation manifest, and pass the preserved 57 cases before editing. That fresh execution baseline is required but has not been run in this planning task.

## Current Repository State

Current TestCatalog.capability(model) rejects nonmatching/unready models and returns a deepcopy; no enumeration method or factory keyword exists. The authenticated /models test runs before supplying a model identity, so keyed lookup alone provides no enumeration source (proposal and test_guidance_formats_playback_admission_and_originals). Missing feature imports occur inside fixtures/tests, so collection and direct TestCatalog construction need no missing feature module or runtime database. TestCatalog construction uses only candidate_policy and evaluator_identity; the latter hashes installed evaluator files, not a quality assessment or database. No hypothesis about unexecuted feature behavior is promoted to evidence.

Observed read-only SHA256: tests/test_voice_enrollment.py = 54e7b44af2f1b7addf12bda786eff7ffbb62f2363d6a126a295c88f0a6d88970; tests/test_enrollment_quality.py = 2ef07c8eb2f5a4af22c4ed95192a1a63244f3089688a9d561b8acff2825010b1. These match recorded 010 execution hashes. The target is UTF-8/LF. git status --short shows pre-existing modified .dockerignore, workflow, Dockerfile, 001, Plan, contract and requirements plus untracked prior artifacts, proposals, model-eval, tests, production and evaluator files. Preserve all of that state. No baseline runtime failure was observed by this planner because runtime checks are expressly forbidden during planning.

## Files in Scope

Files to create during implementation: none in the checkout. Files to modify: tests/test_voice_enrollment.py only, by the complete diff below. Files to delete: none. This planning task creates only this 011 document. The corresponding internal factory-interface documentation is wholly in this document; 010 is not edited. Verified execution bookkeeping in Plan.md and this document's Human Review field are PDD exceptions, performed only after actual verified execution.

## Proposed Changes

1. Add TestCatalog.list_capabilities(self), a zero-argument synthetic catalog collaborator returning [deepcopy(self.cap)] when model_ready, otherwise a fresh empty list, with the two exact scope comments below.
2. Add required list_capabilities=catalog.list_capabilities only to the existing Voices factory call; split its existing capability/policy_snapshot line exactly as reviewed. Do not alter any assertion or other executable source.
3. Record this required internal factory signature delta here, for later GREEN implementation only: voice_narration.voices.application.create_app(*, repository, authenticate, validate_consent, artifacts, enrollment, capability, list_capabilities, policy_snapshot, calibration, clock). It returns the existing planned ASGI app and retains all 010 state diagnostics. list_capabilities is required, with no fallback; it is a zero-argument callable returning enabled/approved Capability records at the authorized catalog boundary. capability(model) remains keyed admission/enrollment lookup. Authentication, pagination and public serialization stay actual Voices behavior under the unchanged contract. No model constants/private-bound-object introspection may substitute for enumeration. This defines no public endpoint, new service owner or calibration/model approval.

## Proposed Code / Tests

Complete unified diff for the sole executable file; original/context line numbers match current UTF-8/LF source and approved proposal:

```diff
--- a/tests/test_voice_enrollment.py
+++ b/tests/test_voice_enrollment.py
@@ -53,6 +53,11 @@
         if not self.model_ready or model != MODEL:
             fail("MODEL_NOT_READY")
         return deepcopy(self.cap)
+
+    def list_capabilities(self):
+        # Synthetic enabled/approved catalog records for this isolated test only.
+        # This does not grant production model or calibration approval.
+        return [deepcopy(self.cap)] if self.model_ready else []
 
     def snapshot(self):
         return {"revision": self.revision, "enrollment_quality": deepcopy(self.policy)}
@@ -112,7 +117,9 @@
         return voices_factory(repository=repository, authenticate=auth.state.verify_token,
                               validate_consent=consents.state.validate_owner_consent,
                               artifacts=artifacts.state.enrollment_samples, enrollment=adapter,
-                              capability=catalog.capability, policy_snapshot=catalog.snapshot,
+                              capability=catalog.capability,
+                              list_capabilities=catalog.list_capabilities,
+                              policy_snapshot=catalog.snapshot,
                               calibration=catalog.calibration, clock=lambda: now[0])
 
     voices = make_voices(voices_repo)
```

## Execution Steps and Verification Commands

Everything in this section is proposed for execution after human approval. Run from C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration. Use existing project Python only. Do not install/build/start the application or run the 21 missing-feature cases. Existing regression fixtures alone may create/remove their own unique isolated resources; pre-existing user Docker must never be started, stopped, restarted or reconfigured.

Stable evidence root: C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction. The executor copies the following complete helper verbatim to check.py in that root, outside the checkout, using explicit UTF-8 and LF. Create no other executable repository file. It is verification/application tooling, not new production/test infrastructure. Preserve prior evidence: an existing before.json stops execution rather than overwriting it. Retain exact command stdout/stderr/exit codes and collection node IDs in evidence files at this root and link them from Plan.md. No nested fenced-code extraction or one giant encoded command is needed; write the helper as a file before invocation.

```python
import ast
from copy import deepcopy
import difflib
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration")
EVIDENCE = Path(r"C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\011-catalog-correction")
TARGET = "tests/test_voice_enrollment.py"
QUALITY = "tests/test_enrollment_quality.py"
OLD_HASH = "54e7b44af2f1b7addf12bda786eff7ffbb62f2363d6a126a295c88f0a6d88970"
QUALITY_HASH = "2ef07c8eb2f5a4af22c4ed95192a1a63244f3089688a9d561b8acff2825010b1"
INSERT_AFTER = '        return deepcopy(self.cap)\n'
INSERT = ('\n    def list_capabilities(self):\n'
          '        # Synthetic enabled/approved catalog records for this isolated test only.\n'
          '        # This does not grant production model or calibration approval.\n'
          '        return [deepcopy(self.cap)] if self.model_ready else []\n')
OLD_CALL = '                              capability=catalog.capability, policy_snapshot=catalog.snapshot,\n'
NEW_CALL = ('                              capability=catalog.capability,\n'
            '                              list_capabilities=catalog.list_capabilities,\n'
            '                              policy_snapshot=catalog.snapshot,\n')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inventory():
    excluded = {".git", ".venv", ".pytest_cache", "__pycache__"}
    return {p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
            for p in sorted(ROOT.rglob("*"))
            if p.is_file() and not excluded.intersection(p.relative_to(ROOT).parts)
            and p.suffix != ".pyc"}

def expected(before):
    text = before.decode("utf-8")
    assert "\r" not in text and text.count(INSERT_AFTER) == 1
    assert text.count(OLD_CALL) == 1 and "def list_capabilities(" not in text
    result = text.replace(INSERT_AFTER, INSERT_AFTER + INSERT).replace(OLD_CALL, NEW_CALL)
    ast.parse(result)
    return result.encode("utf-8")

def reviewed_diff(before, after):
    actual = "".join(difflib.unified_diff(before.decode("utf-8").splitlines(True),
                                        after.decode("utf-8").splitlines(True),
                                        fromfile="a/" + TARGET, tofile="b/" + TARGET))
    proposal = (ROOT / "docs/.ai/initial-build/Enrollment-Catalog-Seam-Correction-Proposal.md").read_text(encoding="utf-8")
    approved = proposal.split("```diff\n", 1)[1].split("\n```", 1)[0] + "\n"
    assert actual == approved, "Delta differs from approved proposal"
    return actual

mode = sys.argv[1]
assert Path.cwd() == ROOT
if mode == "baseline":
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    assert not (EVIDENCE / "before.json").exists(), "Preserve prior evidence; stop for review"
    before = (ROOT / TARGET).read_bytes()
    assert digest(before) == OLD_HASH
    assert digest((ROOT / QUALITY).read_bytes()) == QUALITY_HASH
    old_plan = (ROOT / "docs/.ai/initial-build/010_Implementation_Plan_Voice_Enrollment_RED.md").read_text(encoding="utf-8")
    marker = '"""Real owner boundaries and measurements; test-only evidence, no model-quality claim."""\n'
    historical = marker + old_plan.split(marker, 1)[1].split("\n```", 1)[0] + "\n"
    assert historical.encode("utf-8") == before
    tree = ast.parse(before)
    catalog = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "TestCatalog")
    assert all(getattr(n, "name", None) != "list_capabilities" for n in catalog.body)
    assert not any(isinstance(n, ast.keyword) and n.arg == "list_capabilities" for n in ast.walk(tree))
    assert not (ROOT / "voice_narration/voices/quality.py").exists()
    assert not (ROOT / "voice_narration/artifacts/application.py").exists()
    delta = reviewed_diff(before, expected(before))
    (EVIDENCE / "before-test.py.txt").write_bytes(before)
    (EVIDENCE / "authorized.diff").write_bytes(delta.encode("utf-8"))
    (EVIDENCE / "before.json").write_text(json.dumps(inventory(), indent=2, sort_keys=True), encoding="utf-8")
    print("Baseline exact 010 test/hash, quality hash, absent enumeration seam and intended modules confirmed")
    print("Preservation manifest and authorized diff:", EVIDENCE)
elif mode in {"apply", "verify"}:
    before = (EVIDENCE / "before-test.py.txt").read_bytes()
    assert digest(before) == OLD_HASH
    after = expected(before)
    delta = reviewed_diff(before, after)
    assert (EVIDENCE / "authorized.diff").read_bytes() == delta.encode("utf-8")
    baseline = json.loads((EVIDENCE / "before.json").read_text(encoding="utf-8"))
    current = inventory()
    assert set(current) == set(baseline), "Unexpected file addition/removal"
    changed = {p for p in current if current[p] != baseline[p]}
    if mode == "apply":
        assert not changed
        assert (ROOT / TARGET).read_bytes() == before
        (ROOT / TARGET).write_bytes(after)
    else:
        assert changed == {TARGET}, changed
        assert (ROOT / TARGET).read_bytes() == after
        before_ast, after_ast = ast.parse(before), ast.parse(after)
        assert [ast.dump(n) for n in ast.walk(before_ast) if isinstance(n, ast.Assert)] == [ast.dump(n) for n in ast.walk(after_ast) if isinstance(n, ast.Assert)]
        assert [n.name for n in before_ast.body if isinstance(n, ast.FunctionDef)] == [n.name for n in after_ast.body if isinstance(n, ast.FunctionDef)]
        (EVIDENCE / "after.json").write_text(json.dumps(current, indent=2, sort_keys=True), encoding="utf-8")
    print(mode, "exact authorized diff; assertion and file preservation OK")
elif mode == "catalog":
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "tests"))
    module = importlib.import_module("test_voice_enrollment")
    catalog = module.TestCatalog()
    original = deepcopy(catalog.cap)
    ready = catalog.list_capabilities()
    assert ready == [original] and ready is not catalog.cap
    assert ready[0] is not catalog.cap
    ready[0]["model"]["version"] = "mutated-copy"
    ready[0]["languages"].append("mutated-copy")
    ready.append({"mutated": True})
    assert catalog.cap == original
    assert catalog.list_capabilities() == [original]
    assert catalog.capability(module.MODEL) == original
    catalog.model_ready = False
    empty = catalog.list_capabilities()
    assert empty == []
    empty.append(original)
    assert catalog.list_capabilities() == [] and catalog.cap == original
    catalog.model_ready = True
    assert catalog.list_capabilities() == [original]
    print("Actual TestCatalog: ready, empty, nested defensive copy, fresh list and keyed lookup preserved")
elif mode == "diagnostics":
    commands = [["docker", "context", "show"], ["docker", "version"],
                ["docker", "compose", "version"],
                ["docker", "info", "--format", "{{.ServerVersion}}"]]
    failed = False
    for args in commands:
        process = subprocess.Popen(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        try:
            out, err = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            out, err = process.communicate()
            print(args, "TIMEOUT diagnostic PID", process.pid, out, err)
            raise SystemExit(1)
        print(args, "PID", process.pid, "exit", process.returncode, out.strip(), err.strip())
        failed = failed or process.returncode != 0
    raise SystemExit(1 if failed else 0)
else:
    raise SystemExit("Unknown mode")
```

Run each command separately, retaining real outputs and exit statuses. Python helper process failures stop the sequence. For pytest, no skip/xfail/error/failure is accepted; inspect actual counts and collection node IDs, not just exit zero. Capture git status before baseline and after verification to preserve unrelated edits.

```powershell
git status --short
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py baseline
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py diagnostics
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py apply
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py verify
.\.venv\Scripts\python.exe -m pytest -p no:anyio --collect-only tests/test_enrollment_quality.py tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py catalog
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py catalog
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py
.\.venv\Scripts\python.exe C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/011-catalog-correction/check.py verify
git diff --check
git status --short
```

Diagnostics are individually bounded to 15 seconds, killing/reaping only the timed-out diagnostic PID. Require actual desktop-linux context, server 29.3.1 and Compose 5.6.0 output consistent with carried-forward prerequisites; do not infer availability from process names. Each pytest invocation is an independent existing regression run. Run the baseline and postchange suites without manual cleanup between them; this repeats the same persistent-store checks across the correction and verifies existing fixture isolation. The active task limits broad regressions to this proportional before/after pair. Do not add fresh broad readiness/browser/audio/build checks for this narrow correction unless an unresolved failure returns this plan for review. Never rerun a failed test until it happens to pass.

Collection must report the same six quality and fifteen enrollment case node IDs as the original 010 test source (parameterizations unchanged, checked through exact source/diff preservation). The helper imports the actual test module with tests and repository roots on sys.path; it does not invoke enrollment_system, postgres, quality fixtures or missing production factories, and does not replace TestCatalog with a reimplementation or provide fake quality results. Its fresh-copy mutations check nested dict/list isolation, both ready/empty states and preserved keyed lookup. No product assertion is weakened.

After each regression run, inspect fixture project names/output and teardown; use bounded read-only exact-project Docker ps/network/volume label queries as in 010 if cleanup is uncertain. No manual/global cleanup or access to unrelated containers is authorized. Any unexpected error, unrelated failure, skip/xfail, teardown failure, drift, missing expected case or required runtime discrepancy stops execution and returns the evidence for review. The expected absence of feature modules is recorded read-only by baseline and not exercised as a failing verification command.

## Acceptance / Completion Criteria

- Fresh pre-edit baseline confirms exact historical 010 target/quality source hashes, absent enumeration seam, unchanged current files and 57 preserved cases passing before editing.
- Exactly the proposal diff is applied to the sole executable file. All other checkout source, tests, configurations, dependencies, requirements, contract, completed artifacts and evidence remain byte-identical to the captured inventory. Assert nodes and module-level test functions remain identical. Only verified PDD bookkeeping is excluded, performed after final preservation verification.
- Collection passes with six quality and fifteen enrollment cases and unchanged case identities. Actual TestCatalog ready/empty/nested defensive-copy checks pass twice without fixture/database/missing-module execution. No model, calibration, enrollment runtime success or new RED revalidation is claimed.
- All 57 existing persistence and authentication/consent regressions pass after the change without manual cleanup between baseline and postchange invocations; no failure/skip/xfail/error is accepted. User Docker remains running and unmodified; executor-owned fixture resources/processes are cleaned up by existing teardown and evidence confirms that cleanup.
- Record the complete required internal factory keyword/signature documented above as a constraint for separately reviewed GREEN planning. Complete only milestone 11 with real command outputs, hashes and preservation evidence; stop before GREEN. Future GREEN must actually pass all 78 cases, not substitute this correction's checks for feature execution.

## Expected Evidence

Expected / Predicted — Not Yet Verified: baseline/verify exact-byte and AST checks pass; diagnostics succeed; preserved suite yields 57/57 on both baseline and postchange invocations; collection yields 21 unchanged node IDs; both actual collaborator checks pass; no unrelated checkout changes occur. No failing missing-feature invocation is part of OTHER completion. Every result remains predicted until actual postapproval execution supports it.

## Planning-Time Dry Run

The active task prohibits test, application, Docker, database and package operations during planning, including a disposable copy. Therefore no runtime dry run, baseline regression run, collection or collaborator execution was performed. This is an explicit task restriction, not a claim that a disposable copy would modify the checkout. Static-only review parses the original/proposed test and embedded helper without imports, validates the complete proposal diff/context and exact bytes, and checks assertion/test-name preservation. Static evidence is planning evidence only, not milestone completion or runtime soundness. No new runtime failure was observed. Any future baseline failure must be reported for human disposition before execution continues; no nonblocking failure allowance is introduced.

Actual static-only planning result: current target equals historical 010 content including final LF and recorded SHA256; the complete two-hunk diff equals the approved proposal and a freshly generated current-source diff. Original/proposed test and complete helper parse successfully; every assertion AST and module-level test name is preserved. No Ellipsis placeholder or HTML template comment was found; exactly one approval field exists. The only trailing spaces are the two required unified-diff blank-context prefixes. No product/test module was imported and no runtime verification was run. An initial static comparison found a missing final LF in historical-block reconstruction; that helper expression was corrected and affected checks then passed. A subsequent overly broad whitespace check flagged the valid diff context prefixes; it did not identify a source defect. These are planning-helper findings, not runtime failures. git diff --check exited 0 with existing LF-to-CRLF notices for pre-existing files; direct checks cover this untracked artifact. No scratch file was created.

## Risks

No identity, role or ownership comparison is added by this delta. Preserved 010 comparisons retain delivered Auth/_sql.identity canonical lowercase UUID validation for authenticated user versus consent/sample/profile owner and requested owner IDs, consent links, model/artifact/profile/assessment/grant IDs; malformed case/whitespace forms are invalid. Exact User/Administrator roles remain insufficient for private access; existing email trim/lowercase belongs only to Auth. Regression tests remain actual delivered boundaries.

The synthetic enabled/approved capability is a test input, never production registry approval. Fixture checks prove fixture copying/enumeration only. Actual authenticated pagination/serialization, catalog-owner transport and acoustic behavior require later implementation and tests under existing gates. Disk hashes prove preservation within the captured inventory, excluding transient .git/.venv/pytest/bytecode caches; they do not establish unseen runtime behavior. Do not overwrite or normalize unrelated LF/CRLF files. Missing production modules stay missing here; adding them would violate this OTHER scope.

## Pre-authorized Contingencies

Only diagnostic-context contingency: exact trigger is denied/missing dockerDesktopLinuxEngine named pipe in restricted execution while the pre-existing user engine is usable in ordinary host context. Files changed: none. Rerun the same diagnostics and the same approved regression commands in the permitted host context, with diagnostics bounded to 15 seconds each and observation/handoff bounded to 120 seconds. Record original denial, actual host results and deviation. No start/stop/restart, context/settings change, dependency fallback, alternate detector, assertion change or criterion waiver. If still unavailable, stop for user-provided working engine/context. Report whether this sole trigger occurred/applied. Unexpected failures have no retry-to-pass contingency.

## Rollback / Recovery

On failure retain evidence and mark no completion. Reverse only this delta in tests/test_voice_enrollment.py by restoring before-test.py.txt after verifying the current bytes equal the exact proposed result; if different, stop for review rather than overwriting. Preserve every unrelated file. No reset/clean/checkout operation. Existing fixtures own cleanup only for their unique resources. Do not stop user Docker.

## Explicitly Out of Scope

Production code, requirements/contract/Plan scope changes, previous 010 edits, dependencies/build/runtime configuration, Docker lifecycle operations, calibration/model enablement, assertion weakening, new RED execution, GREEN implementation, commits, pushes, publication and next-milestone approval.

## Exact-Code / Authority Self-Check

| File / review item | Result |
| --- | --- |
| tests/test_voice_enrollment.py | Complete two-hunk unified diff; no pseudocode, placeholders or omitted changed lines. Matches Proposed Changes 1–2 and approved proposal exactly. No dependency/plugin/configuration setting introduced. |
| This document's internal factory interface | Proposed Change 3 explicitly records only required list_capabilities, zero-argument data semantics and complete keyword-only factory signature; 010 remains historical. No public endpoint or product requirement added. |
| External evidence helper check.py | Complete content provided above, all modes/paths/commands explicit; verification-only, outside checkout. Reuses existing standard library/project environment, no package/configuration mutation. |

No new requirement/criterion/decision/contingency identifier family is introduced; milestone numbers, artifact names and existing contract labels are references rather than redefinitions. No HTML template comment remains. Only Human Review below contains this artifact's approval status.

## Human Review

Status: Executed — Enrollment Catalog Test-Wiring Correction OTHER Complete on 2026-10-26 under avinash2196 approval recorded 2026-10-26T16:54:05Z. Exact two-hunk test-only diff; baseline57/57 (103.16s), postchange57/57 (85.94s),21 unchanged collected identities, actual catalog ready/empty/deepcopy checks twice and exact preservation passed. See Plan.md Enrollment Catalog Test-Wiring Correction 011 execution evidence and its linked actual commands/outputs/hashes/cleanup. Restricted named-pipe denial triggered only the approved host-context contingency; incidental helper extraction parsing failure before checks was mechanically corrected without logic changes. No new RED, product/model/calibration success or next milestone authorized.
