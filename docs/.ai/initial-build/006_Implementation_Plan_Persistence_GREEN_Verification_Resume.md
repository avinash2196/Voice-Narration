# Implementation Plan — Persistence & Storage GREEN verification resume

## Milestone and Type

Existing initial-build milestone 5, Persistence & Storage GREEN. This is recovery of its unfinished verification, not a new milestone. No implementation changes.

## Authoritative References

All paths below are relative to this repository. Requirements and contract decisions remain unchanged.

| Inspected reference | Authority / disposition |
| --- | --- |
| requirements.md; contract/API-Contract.md in this work-item folder | Human-approved requirements and contract. |
| Plan.md | Approved Plan; milestone 5 now Blocked. Its GREEN 005 stopped execution evidence records applied files, readiness failure and cleanup. Retry disposition must be recorded by the main conversation only after human review. |
| 001_Implementation_Plan_Foundation.md | Approved/executed foundation, preserved versions, nine prerequisite files and isolation mechanisms. |
| 002_Implementation_Plan_Model_Feasibility.md | Approved/executed assessment; no commercial/model enablement inferred. |
| 003_Implementation_Plan_Persistence_RED.md | Approved/stopped history; preserved interfaces and test intent. |
| 004_Implementation_Plan_Persistence_RED_Recovery.md; 004-red-run2.txt | Approved/executed RED; two 33-case missing-module failures after successful real isolated PostgreSQL fixtures. |
| 005_Implementation_Plan_Persistence_GREEN.md | Human-approved exact 18 production files; execution stopped at a blocker, not verified GREEN. Exact content remains implementation authority. |
| voice_narration_PDD_requirements.md | Read-only non-conflicting baseline context. |
| tests/test_persistence.py; voice_narration/; requirements-dev.txt; pytest.ini; compose.harness.yaml | Delivered implementation/tests/prerequisites; not new approval authority. |
| Plugin commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; its templates/Implementation-Plan.md; skills/security/SKILL.md | Process guidance read from C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0. |

No product-level docs/requirements.md exists. No new requirement, normative identifier or architecture decision is introduced. 006 is the next artifact number.

## Current State and Predecessor Evidence

Plan.md GREEN 005 stopped evidence establishes that all 18 exact approved production files were applied and compared, the existing test matches 004, and the nine foundation files are preserved. Its 120-second readiness window did not produce a successful engine diagnostic; neither pytest invocation ran. Cleanup stopped owned Docker processes. Read-only host logs later show DockerAPI running at 03:28:45Z, followed by requested shutdown at 03:28:50Z. This is not proof of readiness within the window or a startup crash. Cause remains unknown; settings, dependencies and WSL are not established causes.

Branch inspection shows codex/foundation-harness with existing documentation, tests and package changes. Preserve this work and 005's stopped history. Do not reapply, remove or redesign its files.

## Carried-Forward Decisions and Files in Scope

Preserve all exact 005 implementation, 004 tests/assertions/helper, foundation settings and versions, eight isolated owner databases and filesystem roots, canonical identity rules, actual live authorization and command-only `-p no:anyio`. No new dependency/version/configuration is selected.

Files to create, modify or delete during execution: **none** in production, tests, build, dependency, runtime or deployment configuration. Only this artifact's execution disposition and milestone 5 Execution Status/evidence in Plan.md may be updated as PDD bookkeeping. Exact-code review is vacuous for implementation files: zero changed files, no code blocks to replace. The 18 unchanged files need no repeated content listing.

## Proposed Recovery and Verification

Execute only after this exact 006 has human approval and Plan.md records the reviewed retry disposition for this same GREEN. Work from `C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration` throughout. Any incompatible drift stops execution.

First run the four git checks and interpreter/plugin metadata check exactly as 005 Verification Commands records, including its explicit nine-file foundation preservation diff. Then compare the 18 actual files with the complete approved 005 blocks using this read-only PowerShell block; it prints actual per-file hashes and fails on any mismatch. Run before and after verification.

```powershell
$greenText = Get-Content -Raw -Encoding UTF8 docs/.ai/initial-build/005_Implementation_Plan_Persistence_GREEN.md
$greenBlocks = [regex]::Matches($greenText, '(?ms)^### (voice_narration/[^\r\n]+)\r?\n\r?\n```python\r?\n(.*?)```')
if ($greenBlocks.Count -ne 18) { throw 'Expected exactly 18 approved blocks' }
foreach ($greenBlock in $greenBlocks) {
    $greenPath = $greenBlock.Groups[1].Value
    $greenExpected = $greenBlock.Groups[2].Value.Replace("`r`n", "`n")
    $greenActual = [IO.File]::ReadAllText((Join-Path $PWD $greenPath)).Replace("`r`n", "`n")
    if ($greenActual -cne $greenExpected) { throw "Approved-content mismatch: $greenPath" }
    Get-FileHash -Algorithm SHA256 -LiteralPath $greenPath | Select-Object Path,Hash
}
$redText = Get-Content -Raw -Encoding UTF8 docs/.ai/initial-build/004_Implementation_Plan_Persistence_RED_Recovery.md
$redBlock = [regex]::Match($redText, '(?ms)```python\r?\n(.*?)```')
if (-not $redBlock.Success) { throw '004 complete test block missing' }
$redActual = [IO.File]::ReadAllText((Join-Path $PWD 'tests/test_persistence.py')).Replace("`r`n", "`n")
if ($redActual -cne $redBlock.Groups[1].Value.Replace("`r`n", "`n")) { throw '004 test mismatch' }
```

Run these diagnostics separately, retaining actual output and exit codes:

```powershell
docker context show
docker version
docker compose version
docker info --format '{{.ServerVersion}}'
```

Require desktop-linux, Docker client/server29.3.1, Compose5.6.0 and the unchanged Python3.13.17/pytest9.1.1 environment from 005. If engine is stopped/missing pipe, launch the already-installed approved Desktop once:

```powershell
Start-Process -FilePath 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -WindowStyle Hidden
```

Allow at most 300 seconds elapsed from this first launch to successful readiness, including any host-context handoff. Poll the same diagnostics at intervals up to15 seconds. Bound each diagnostic process to15 seconds using the execution facility's process timeout/termination, preserve partial output and record timeout. Returning a tool session is not process termination: terminate its exact diagnostic PID on timeout. Do not accumulate hanging diagnostics. Tool waits must remain at most60 seconds; give a meaningful user update at least every60 seconds. This procedure changes the readiness observation window only; it does not change the test fixture's Compose timeout or any file. Success requires actual engine/server output, not only a running process or host log. Exhaustion or an unexpected diagnostic failure stops verification; no restart loop.

Once ready, run these separately in the successful diagnostic execution context, unchanged environment/cwd:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py -ra --tb=short
```

Second invocation is authorized only after first passes all33 cases with successful teardown; no manual cleanup between runs. No anyio plugin in either header. A failure/error/skip/xfail, failed teardown or incompatible prerequisite stops execution without fixes or extra suite retries. Preserve real outputs, exit codes, durations and printed random Compose project IDs. Recheck exact files/tests/foundation and scope afterward.

## Pre-authorized Contingencies

Exact trigger: sandbox Desktop launch does not persist, or diagnostics explicitly deny access to dockerDesktopLinuxEngine. Files: none. Exact change: execute the identical hidden launch (only if the first did not persist), diagnostic commands and, after successful readiness, identical two pytest commands through the existing approved host execution facility with unchanged cwd/environment and the same total300-second deadline. Record observed trigger and application. This is a reviewed execution-context contingency, not permission to change settings or bypass automatic approval review. If automatic review rejects execution, record its stated reason and stop.

## Acceptance / Completion Criteria

All 005 criteria remain: exact18 production files, exact004 tests, nine foundation files unchanged; two actual33/33-pass runs without manual cleanup, no errors/skips/xfails, real PostgreSQL18.6 and effective isolation/roles/roots/reopen/grants/retention/fencing/purge/audit assertions passing. All owned resources/processes stopped before reporting. A successful startup, static comparison or one pass is insufficient. No pre-existing failure is waived. Record actual commands/output, deviations, contingency use/nonuse and cleanup in Plan.md before marking this same GREEN complete. No later milestone is authorized.

Expected / Predicted — Not Yet Verified: the longer bounded observation and unchanged host-context contingency may establish readiness, followed by two33-case passes. Neither readiness nor test success is claimed observed by this plan.

## Cleanup, Recovery and Risks

Use 005's exact fixture-owned project cleanup only, preserving its printed random IDs and original fixture environment. No global prune/reset/clean. Stop only Desktop started by this execution with `docker desktop stop`; bound cleanup diagnostics as above. Verify `docker desktop status` and `Get-Process -Name 'Docker Desktop','com.docker.backend','com.docker.build' -ErrorAction SilentlyContinue | Select-Object ProcessName,Id`; record actual output and account for every started diagnostic/pytest process. Incomplete cleanup is incomplete evidence. No implementation rollback is proposed; retain the already-applied approved files and stopped history.

Canonical comparisons remain those reviewed in 005: actor/resource/list owner, grant owner/administrator/scope, exact Administrator role, cleanup owner and profile/consent links use canonical lowercase UUIDs/exact enums from Auth; no email/trim/case-fold substitute. This plan changes no authorization logic. Distributed transport, scheduling, deployed protection and real model adapters remain later milestones. Unknown startup cause may recur; a longer bound is a hypothesis to test, never a claim that dependencies/settings need repair.

## Planning-Time Dry Run and Exact-Code Review

No runtime dry run: this planning task permits documentation and read-only static checks only, with no Docker launch, pytest, dependency install or executable mutation. Existing005 hashes/stopped diagnostics and004 RED are actual predecessor evidence, not successful recovery evidence. No additional baseline runtime failure has been established. No new implementation file or code/configuration setting is proposed, so per-file complete-code replacement review does not apply. Verification commands above are exact; their results remain unverified until approved execution. No template comments or new normative identifiers are introduced.

Actual planning checks: the comparator structure above returned `PASS: exact 18 approved files and exact004 test; no runtime probe`; `git diff --check` exited0 with existing001/Plan LF-to-CRLF notices only. No runtime command ran. These are static observations, not GREEN evidence.

## Explicitly Out of Scope

Any code/test/assertion/helper/dependency/configuration/WSL/settings change, installation, restart loop, extra failed-suite retry, production-data operation, new milestone, cloud/model work, commit/push/publish or approval by the planner.

## Human Review

Status: Approved by avinash2196 on 2026-10-24 (recorded 2026-10-25T03:32:49Z), in response to review of this exact verification-resume plan and retry disposition.

Execution status: Complete — verified this same GREEN milestone under 006. Both exact suites passed 33/33 (36.31s and 29.52s), exact 18 production files/004 test and nine foundation files preserved. Observed nonpersisting sandbox launch activated approved host contingency. Owned runtime and diagnostic/pytest processes stopped; cleanup details, actual outputs/hashes and passing-output capture limitation recorded in Plan.md verification resume 006 execution evidence. No executable changes, extra suite retry, next milestone, commit or push.
