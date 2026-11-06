# Implementation Plan — Enrollment Playback Link Test-Wiring Correction

## Milestone, type and status

initial-build milestone14, **OTHER**. **Approved by avinash2196; recorded 2026-10-27T05:28:04Z. Complete — verified exact OTHER execution on 2026-10-27.** Plan revision approved by avinash2196 on2026-10-26 America/Chicago, recorded2026-10-27T04:35:33Z. The playback proposal approval was recorded2026-10-27T04:26:57Z. The user approved this exact artifact in the main conversation. The approved Implementation Plan has now been executed and verified; actual execution evidence is recorded below. Predecessor Enrollment Interface Completion RED is Complete; GREEN is now milestone15 and remains Pending.

## Authoritative References

Paths below are relative to docs/.ai/initial-build unless otherwise indicated.

| Read reference | Status / authority |
| --- | --- |
| requirements.md | Q12 approved2026-10-26T17:12:20Z; retained FR-010–013 and consent/privacy rules. |
| Plan.md | Playback correction revision approved2026-10-27T04:35:33Z; milestone14 OTHER scope, exclusions and verification govern. |
| contract/API-Contract.md | Q12 approved2026-10-26T17:39:41Z; unchanged public base/prefix and Artifact Link/access constraints. |
| Enrollment-Playback-Link-Test-Correction-Proposal.md | Approved2026-10-27T04:26:57Z; exact test-only correction. |
| 001_Implementation_Plan_Foundation.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 002_Implementation_Plan_Model_Feasibility.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 003_Implementation_Plan_Persistence_RED.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 004_Implementation_Plan_Persistence_RED_Recovery.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 005_Implementation_Plan_Persistence_GREEN.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 006_Implementation_Plan_Persistence_GREEN_Verification_Resume.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 007_Implementation_Plan_Authentication_Consent_RED.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 008_Implementation_Plan_Authentication_Consent_GREEN.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 010_Implementation_Plan_Voice_Enrollment_RED.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 011_Implementation_Plan_Enrollment_Catalog_Test_Wiring_Correction.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 012_Implementation_Plan_Enrollment_Interface_Completion_RED.md | Approved historical artifact; completed or recovery evidence retained in Plan.md. |
| 013_Implementation_Plan_Voice_Enrollment_GREEN.md | Blocked, unapproved GREEN draft; planning evidence only. |
| tests/test_voice_enrollment.py; tests/test_enrollment_quality.py; tests/test_persistence.py; tests/test_authentication_consent.py | Inspected current tests/fixtures; repository evidence, not new requirements. |
| voice_narration/**/*.py; compose.harness.yaml; pytest.ini; requirements-dev.txt; requirements-evaluator.txt; containers/harness.Dockerfile; tools/*.py; .dockerignore; .github/workflows/harness.yml | Current preserved source/configuration/prerequisites. |
| Installed production-engineering-standards0.15.0 commands/create-implementation-plan.md; agents/planner.md; skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/testing/SKILL.md | Applied process and testing guidance. |

No workspace AGENTS.md or product-level docs/requirements.md exists. Product baseline voice_narration_PDD_requirements.md remains subordinate read-only context already carried by the approved requirements; no new product decision is made here.

## Current repository state and baseline evidence

The branch is codex/foundation-harness and contains existing modified/untracked user-retained production and documentation work. Do not assume a clean tree or revert it. The current target SHA256 is73164c87ce95cfb90d7c081b355d88644fefdf27c393ab4f9635e9278aad119e. Its two playback bodies pass returned URL paths back to an HTTPX client whose base already includes/api/v1. Current Artifact/Voices routes and returned playback URL include/api/v1; source is retained unverified GREEN input, not completed GREEN evidence. Capture its actual bytes before execution and preserve them.

Completed012 records40 intended missing-production setup errors twice and57 preserved passes before/after. The later unapproved013 disposable dry run records95 passed/2 failed in422.15s, with precisely the two playback assertions receiving404; all57 preserved cases passed. Earlier RED stopped at imports and did not exercise this transport seam. These historical observations are not rerun milestone14 or GREEN results.

An actual HTTPX build_request diagnostic in013 demonstrates that a path/api/v1/artifacts/example/content becomes/api/v1/api/v1/artifacts/example/content under this client. Standard URL joining first produces a complete same-origin URL that HTTPX leaves intact. The isolated helper checks this actual transformation without a server or fabricated production result. It also checks that signed query bytes remain intact and external origins fail before network access.

Current inventory:97 cases=40 enrollment feature cases+57 delivered regressions. This OTHER does not run the unfinished feature suite or count an expected feature failure as passing evidence. The full97 success gate remains owned by GREEN.

## Carried-forward decisions

001 retains project CPython3.13.17/.venv, pytest9.1.1, HTTPX0.28.1, PostgreSQL18.6/Psycopg3.3.6, NumPy/PyAV and unique loopback/container/database/root isolation. 004 retains command-only-p no:anyio. 003–006 retain eight separately credentialed owned stores, actual effective-isolation assertions and precise preservation. 007/008 retain real HTTP authentication/consent tests, canonical identities and live consent/grants. 009 retains installed decoder/resampler/native VAD and separate evaluator manifest. 010/011/012 retain the current feature inventory, all original assertions, selected-stream/original-byte and authentication behavior. 002 keeps model investigation/calibration/commercial/runtime gates separate. No dependency/version/tool/configuration selection occurs.

The existing pytest postgres fixture creates a fresh vnred+UUID Compose project, random password, dynamic127.0.0.1 port, temporary owner databases/roles/roots and verifies effective isolation. Its finally removes only that exact owned project. The user's running Docker engine/Desktop and pre-existing resources must remain untouched.

## Files in scope and ordered proposed changes

Files to create/delete in the repository: none. File to modify: tests/test_voice_enrollment.py only. PDD status/evidence updates in this014 artifact and milestone14's Plan.md execution row are bookkeeping after verified execution, not additional implementation scope.

1. Establish current hashes/routes,97-case collection and passing57-case baseline before changing the target.
2. Add urljoin to the existing stdlib import and add returned_link_url(system,value), which uses standard joining against the fixture client base, asserts the same origin and returns the absolute URL.
3. Use that URL at exactly three existing GET request sites across two playback tests. Preserve the authenticated headers, the request deliberately lacking credentials, original-byte/MIME/disposition checks, selected-stream comparison and every other assertion.
4. Verify exact diff, unchanged inventory, all original assertion ASTs plus exactly the helper's new origin assertion, actual URL/client transformation and preserved source/configuration hashes. Run the57-case regression suite again without manual cleanup between the two persistent runs.
5. Record actual evidence and owned cleanup; stop before GREEN.

No owned requirement adds or changes production behavior. No production alias, URL format rule, schema, source fix or capability change is introduced.

## Exact proposed diff — not applied

```diff
--- a/tests/test_voice_enrollment.py
+++ b/tests/test_voice_enrollment.py
@@ -5,7 +5,7 @@
 import hashlib
 import importlib
 import json
-from urllib.parse import urlsplit
+from urllib.parse import urljoin, urlsplit
 
 import numpy as np
 import pytest
@@ -190,6 +190,14 @@
     return result
 
 
+def returned_link_url(system, value):
+    base = str(system["media"].base_url)
+    resolved = urljoin(base, value)
+    expected, actual = urlsplit(base), urlsplit(resolved)
+    assert (actual.scheme, actual.netloc) == (expected.scheme, expected.netloc), "Playback stays on the fixture origin"
+    return resolved
+
+
 def create_profile(system, samples, **changes):
     body = {"name": "मेरा निजी स्वर", "language": "hi",
             "consent_id": system["consent_record"]["consent_id"],
@@ -246,13 +254,13 @@
                                    headers=headers(s["token"]))
         assert result.status_code == 200, result.text
         link = result.json()
-        parts = urlsplit(link["url"])
-        content = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
+        playback_url = returned_link_url(s, link["url"])
+        content = s["media"].get(playback_url, headers=headers(s["token"]))
         assert content.status_code == 200 and content.content == data
         assert "inline" in content.headers["content-disposition"]
         assert content.headers["content-type"].split(";")[0] == {
             "wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
-        error(s["media"].get(parts.path + "?" + parts.query), 401, "UNAUTHENTICATED")
+        error(s["media"].get(playback_url), 401, "UNAUTHENTICATED")
         error(s["media"].get("/artifacts/" + sample["artifact_id"] + "/download-url?format=wav",
                                headers=headers(s["token"])), 400, "UNSUPPORTED_FORMAT")
     for data, fmt, code in [(b"", "wav", "INVALID_AUDIO"), (b"not audio", "wav", "INVALID_AUDIO"),
@@ -508,7 +516,7 @@
     response = s["media"].get("/artifacts/" + sample["artifact_id"] + "/preview-url",
                                  headers=headers(s["token"]))
     assert response.status_code == 200, response.text
-    parts = urlsplit(response.json()["url"])
-    playback = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
+    playback_url = returned_link_url(s, response.json()["url"])
+    playback = s["media"].get(playback_url, headers=headers(s["token"]))
     assert playback.status_code == 200 and playback.content == data
     assert independent_decode(playback.content)["stream_index"] == captured["stream_index"]
```

## Acceptance / Completion Criteria

- Only the exact approved target diff is applied; all original assertions remain unchanged and one origin assertion is added. No production, dependency, configuration, infrastructure or unrelated test byte changes.
- Baseline/postchange collection each reports the same97 test identities. Six acoustic cases and all34 HTTP enrollment cases remain present alongside57 regressions.
- Isolated checks pass twice: API-prefixed origin-relative and same-origin absolute URLs resolve once through actual HTTPX request construction, signed query remains exact, three external origins are rejected, and all three request sites retain their existing authentication behavior.
- The57 delivered persistence/Auth/Consent tests pass before and after the change, with no failure/error/skip/xfail and successful fixture teardown. These two runs repeat the same unchanged persistent tests without manual cleanup; no additional redundant pair is required. The changed test transport is separately checked twice after application.
- All tracked snapshot files except the one approved target remain byte-identical. Existing user work and completed milestone histories are preserved. Fixture-owned processes/connections/projects terminate through their existing finally blocks; no user Docker lifecycle action.

## Exact temporary verification helper — not a repository deliverable

The executor writes the following complete content to verify.py in a new temporary task directory under the approved visualization root. It is an execution helper, never a new permanent test/build artifact. Its capture mode saves the original target and source/test/configuration hashes before application; check mode reads that evidence. No production module is imported or mocked.

```python
import ast
from collections import Counter
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urljoin, urlsplit
import httpx

root = Path.cwd()
evidence = Path(sys.argv[1]) if len(sys.argv) > 1 else root
if len(sys.argv) > 2 and sys.argv[2] == '--capture':
    evidence.mkdir(parents=True, exist_ok=False)
    paths = [p for top in ('voice_narration', 'tests', 'containers', 'tools')
             for p in root.joinpath(top).rglob('*')
             if p.is_file() and '__pycache__' not in p.parts]
    paths += [root / n for n in ('compose.harness.yaml', 'pytest.ini', 'requirements-dev.txt',
              'requirements-evaluator.txt', '.dockerignore', '.github/workflows/harness.yml')]
    manifest = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    evidence.joinpath('manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    evidence.joinpath('before-test.bin').write_bytes(root.joinpath('tests/test_voice_enrollment.py').read_bytes())
    print(f'Captured {len(manifest)} source/test/configuration files and original enrollment test')
    raise SystemExit(0)
before = evidence.joinpath('before-test.bin').read_text(encoding='utf-8')
after = root.joinpath('tests/test_voice_enrollment.py').read_text(encoding='utf-8')
a, b = ast.parse(before), ast.parse(after)
asserts = lambda tree: Counter(ast.dump(n, include_attributes=False) for n in ast.walk(tree) if isinstance(n, ast.Assert))
old, new = asserts(a), asserts(b)
def test_signatures(tree):
    return [(n.name, ast.dump(n.args, include_attributes=False),
             [ast.dump(d, include_attributes=False) for d in n.decorator_list])
            for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]
assert test_signatures(a) == test_signatures(b), 'Test identities or parametrization changed'
assert not old - new, 'An original assertion changed or disappeared'
helper = next(n for n in b.body if isinstance(n, ast.FunctionDef) and n.name == 'returned_link_url')
added = asserts(ast.Module(body=[helper], type_ignores=[]))
assert sum(added.values()) == 1 and new == old + added
namespace = {'urljoin': urljoin, 'urlsplit': urlsplit}
exec(compile(ast.Module(body=[helper], type_ignores=[]), '<returned_link_url-only>', 'exec'), namespace)
resolve = namespace['returned_link_url']
with httpx.Client(base_url='http://127.0.0.1:1234/api/v1') as client:
    system = {'media': client}
    path = '/api/v1/artifacts/example/content?signature=opaque%2Btoken&expires_at=2030-01-01T00%3A00%3A00Z'
    expected = 'http://127.0.0.1:1234' + path
    for value in (path, expected):
        result = resolve(system, value)
        assert result == expected
        assert str(client.build_request('GET', result).url) == expected
    for value in ('https://example.invalid/content', '//example.invalid/content', 'http://127.0.0.1:1235/content'):
        try:
            resolve(system, value)
        except AssertionError:
            pass
        else:
            raise AssertionError('An external origin was accepted')
    assert '/api/v1/api/v1/' in str(client.build_request('GET', path).url)
expected_calls = {'test_guidance_formats_playback_admission_and_originals': 2,
                  'test_multistream_metadata_playback_and_conditioning': 1}
for node in b.body:
    if isinstance(node, ast.FunctionDef) and node.name in expected_calls:
        calls = [n for n in ast.walk(node) if isinstance(n, ast.Call) and
                 isinstance(n.func, ast.Attribute) and n.func.attr == 'get' and n.args and
                 isinstance(n.args[0], ast.Name) and n.args[0].id == 'playback_url']
        assert len(calls) == expected_calls[node.name]
        authenticated = [any(k.arg == 'headers' for k in n.keywords) for n in calls]
        assert sorted(authenticated) == ([False, True] if len(calls) == 2 else [True])
manifest = json.loads(evidence.joinpath('manifest.json').read_text())
for name, digest in manifest.items():
    if name != 'tests/test_voice_enrollment.py':
        assert hashlib.sha256(root.joinpath(name).read_bytes()).hexdigest() == digest, name
print(f'PASS: {sum(old.values())} original assertions preserved; one origin assertion added; 3 request sites retain auth behavior')
print('PASS: origin-relative/absolute links resolve once, signed query preserved, 3 external origins rejected; real HTTPX request construction checked')
print(f'PASS: {len(manifest)-1} other captured source/test/configuration files unchanged')
```powershell
$taskRoot = 'C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46'
$taskRun = Join-Path $taskRoot ('014-execution-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $taskRun | Out-Null
$verificationFile = Join-Path $taskRun 'verify.py'
$patchFile = Join-Path $taskRun 'approved.diff'
$evidenceDirectory = Join-Path $taskRun 'evidence'
```

Write the two exact blocks to the designated temporary files before these commands. Check every exit status immediately; a failed behavioral verification stops execution and returns to planning.

```powershell
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory --capture
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object (Join-Path $taskRun 'collection-before.txt')
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -q -rA
git apply --ignore-space-change --check $patchFile
git apply --ignore-space-change $patchFile
.\.venv\Scripts\python.exe -m py_compile tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object (Join-Path $taskRun 'collection-after.txt')
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -q -rA
git diff --check
git status --short
$beforeIds = @(Get-Content (Join-Path $taskRun 'collection-before.txt') | Where-Object { $_ -like 'tests/*::*' })
$afterIds = @(Get-Content (Join-Path $taskRun 'collection-after.txt') | Where-Object { $_ -like 'tests/*::*' })
if ($beforeIds.Count -ne 97 -or $afterIds.Count -ne 97 -or @(Compare-Object $beforeIds $afterIds).Count) { throw 'Test inventory changed' }
```

Compare the two collected case lists, not just the count; record actual output/hashes in014 and the Plan execution evidence. The helper verifies39 other captured files and each original assertion. Record the exact target diff and resulting target SHA256. The temporary evidence may be retained until trimmed evidence is written into014/Plan, then remove only its verified-contained task directory. No git reset/clean/checkout, commit/push or publication.

## Expected / Predicted — Not Yet Verified milestone evidence

Expected:97 identities unchanged; exact patch applies; compilation succeeds; helper passes twice with all original assertions plus one origin assertion, correct three-site auth behavior and39 other hashes unchanged; baseline57 and post57 pass; diff check succeeds except informational existing LF/CRLF notices; owned fixture teardown succeeds. Planning results below never substitute for execution after human approval.

## Pre-authorized Contingencies

Observable Docker named-pipe permission denial from the intended verification or read-only docker info check, or loopback bind permission denial, permits only the identical verification command in normal host context after normal approval review. No code/file/dependency/default/criterion change. This permits existing fixtures to create/remove only their own fresh random projects, not Docker engine/Desktop/user resource lifecycle. Report trigger and use. Any other runtime failure stops and returns to planning.

## Rollback / recovery

Use the captured original target bytes to restore only tests/test_voice_enrollment.py if rollback is directed and its current hash still matches this milestone's recorded postchange hash; preserve subsequent external edits instead of overwriting them. No database/schema/production change is introduced. Fixture finally performs owned teardown even on failure; do not delete unrelated containers/volumes/networks or change Docker settings.

## Risks, exclusions and review exactness

This is a test wiring correction; isolated URL checks do not claim real playback, calibrated audio/model quality or a passing enrollment feature suite. The preserved assertions and later97-case GREEN gate remain required. The origin assertion compares parsed scheme/netloc with the same local fixture base before any request; it adds no public authorization policy. Authentication/role/owner logic is untouched; existing requests retain their bearer header or deliberate absence exactly. Signed query parameters are not reconstructed or normalized by the helper.

Exclude all production/contract/requirement/configuration/dependency/test-infrastructure/model/calibration/user-enablement changes, assertion weakening, unrelated test edits, commits and publication. Current external source changes remain retained inputs, never assumed approved GREEN.

Per-file review: tests/test_voice_enrollment.py has a complete mechanically applicable unified diff, matches every Proposed Change, contains no placeholder/pseudocode and adds only stdlib URL joining already authorized in the proposal. Temporary verify.py has complete code and no permanent scope; its HTTPX dependency is the approved001 pin. No new configuration/default/plugin/requirement identifier.014 is the next artifact number; its name does not rename completed milestones.

## Planning-time dry run — not milestone evidence

The dry run uses only the disposable copy at `C:\Users\avina\.codex\visualizations\2026\10\24\01a16f65-73ce-7d12-81f7-d277e8480e46\014-playback-planning-dd05bc941d9b445eb9d4937444568d43`. It contains selected source/tests/containers/tools/configuration, source hashes/original-test snapshots, copied proposal diff, temporary verify.py, collection evidence, bytecode and pytest cache. No .git/.venv/secrets/model/private voice was copied; the existing repository interpreter was used with scratch CWD. Working source/tests were never patched.

Planning baseline production hashes (current retained inputs, not approved GREEN):

| File | SHA256 |
| --- | --- |
| voice_narration/_http.py | bf50672f5d2a7625882e013f22c98513d369e90732a0d53b4446d0e7332bd252 |
| voice_narration/voices/persistence.py | b69f0512890ebb03f8829ad0318de086f62ae5d6838a58acb8a135aed55935ad |
| voice_narration/_enrollment.py | aef31c9b0b3cece39fa703be3fa79ca036dde837d935de0811d6e1baf4541885 |
| voice_narration/ai/enrollment.py | b3790e2e8515ddf6392614d8d3961db5d187462347cc6c0632ca3fb3c646dc90 |
| voice_narration/artifacts/application.py | 490390b2b8967ea8b0d73f85110a838f212826b3207284cea80e26f891e15032 |
| voice_narration/voices/application.py | db628224427e18c95fc167ff63b183d7389c876d8e41cbd71acba2beac323678 |
| voice_narration/voices/quality.py | 208c4014a27095e306f699c2d261efd827851a9b2324133162ebf45fe5b29a81 |

Actual commands below used this scratch CWD unless noted. The absolute interpreter path is verbatim; equivalent project-relative commands above apply only after human approval to actual repository execution.

```powershell
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q
```

Exit0: `97 tests collected in11.46s`. From the real working directory, read-only `docker info --format '{{.ServerVersion}}'` exited1: `permission denied while trying to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`. This triggered the exact host-context contingency. The normal review approved the existing fixture-owned test lifecycle; no bypass or Docker engine lifecycle operation.

```powershell
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -q -rA
```

Baseline host exit0: `57 passed in240.30s (0:04:00)`,33 persistence+24 Auth/Consent, no error/skip/xfail. Captured fixture projects: vnred02f1708af2b84340bb377025ca7b1b18 / ea0f5ad656b43ad801d1e27cda1fd6b53b73e6763fe7e8302d2499dda9aeda8b and vnredd21cb7aa5ec4416182a118a242eb8b83 / 5e42c34bcc5723bc939205ff4ee64542e70e7d919313291438e0ff4806340349. Teardown succeeded.

```powershell
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe verify.py execution-evidence --capture
git apply --ignore-space-change --check approved.diff
```

Capture exit0: `Captured40 source/test/configuration files and original enrollment test`. Initial patch check exited128, `error: corrupt patch at line54`, before applying anything. Inspection established the approved proposal's last hunk declares8 old/new lines but contains7 each. Only that header is corrected in this014 diff, from `@@ -508,8 +516,8 @@` to `@@ -508,7 +516,7 @@`; no proposed code/assertion changes. The approved historical proposal is untouched. This is a mechanical planning-time correction explicitly driven by the dry run.

The corrected check, apply and compilation exited0 with no output:

```powershell
git apply --ignore-space-change --check approved.diff
git apply --ignore-space-change approved.diff
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe -m py_compile tests/test_voice_enrollment.py
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe verify.py execution-evidence
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe verify.py execution-evidence
```

Both isolated-helper invocations exit0 with the same output:

```text
PASS: 127 original assertions preserved; one origin assertion added; 3 request sites retain auth behavior
PASS: origin-relative/absolute links resolve once, signed query preserved, 3 external origins rejected; real HTTPX request construction checked
PASS: 39 other captured source/test/configuration files unchanged
```

An additional explicit test-name/argument/decorator AST-equality assertion was added to the temporary verification helper to make inventory preservation directly checked; the helper was rerun twice and produced the same passing output. This changed no permanent test/source code or criterion.

```powershell
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q
```

Postchange exit0: `97 tests collected in7.55s`. The first tool-output export was truncated, so a bounded scratch-only evidence-capture helper re-collected both snapshots to compare full node lists. It restored only the copied target to original bytes for collection, restored the patched bytes in finally, ran no feature body and never touched working source. The exact capture code was:

```python
from pathlib import Path
import subprocess,sys,hashlib
root=Path.cwd(); target=root/'tests/test_voice_enrollment.py'; original=(root/'before-test.bin').read_bytes(); patched=target.read_bytes()
command=[sys.executable,'-m','pytest','-p','no:anyio','tests/test_enrollment_quality.py','tests/test_voice_enrollment.py','tests/test_persistence.py','tests/test_authentication_consent.py','--collect-only','-q']
try:
 target.write_bytes(original)
 before=subprocess.run(command,check=True,capture_output=True,text=True,timeout=120).stdout
 target.write_bytes(patched)
 after=subprocess.run(command,check=True,capture_output=True,text=True,timeout=120).stdout
finally:
 target.write_bytes(patched)
ids=lambda output:[line for line in output.splitlines() if line.startswith('tests/') and '::' in line]
assert len(ids(before))==97 and ids(before)==ids(after)
(root/'collection-before.txt').write_text(before,encoding='utf8');(root/'collection-after.txt').write_text(after,encoding='utf8')
print(before.splitlines()[-1]);print(after.splitlines()[-1]);print('PASS: all 97 baseline/postchange node IDs match in order')
print('Patched target SHA256:',hashlib.sha256(patched).hexdigest())
```

Run via the existing interpreter's stdin in scratch; exit0: baseline collection12.07s,post8.19s, all97 IDs matched in order. Patched target SHA25610599b90047abc322a40835b568887f9f1fd5bc4edb73f39e3070aed14d86eea. The execution protocol above captures both collection outputs directly, avoiding the export helper. `git diff --no-index -- before-test.bin tests/test_voice_enrollment.py` printed exactly the approved logical changes and exit1 (normal differing-files diagnostic), with only LF/CRLF notices.

The identical57-case host command was run after the scratch patch, with no manual cleanup between persistent runs:

```powershell
C:/Users/avina/Downloads/avinash-repo/v11/Voice-Narration/.venv/Scripts/python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -q -rA
```

Postchange host exit0: `57 passed in329.77s (0:05:29)`,33 persistence+24 Auth/Consent, no errors/skips/xfails and complete teardown. Owned projects: vnred283e4e503bcb4bc0baa8774ed355cbd0 /22f1100e93c2d0ae26a680ed38b707cad0a002b0e3fcb9268a07e4a05a89fffa and vnrede4bf20a514b1477086c262eb6e5a33d7 /da024592b42f01d171225a08c06000745062dfb43ebfaf4c38b12a9154ffe2d3. No manual cleanup occurred between baseline and postchange.

No full feature run is part of this OTHER dry run; no expected failure is accepted as passing verification. These observations remain planning evidence only. Actual milestone execution still requires the human to approve014 and then run its commands against the repository.

Final read-only host verification listed containers/networks/volumes with exact com.docker.compose.project labels for the four recorded project IDs. Every one of12 checks exited0 with empty results. `docker info --format '{{.ServerVersion}}'` exited0 and printed29.3.1; the user's engine stayed running. No cleanup/lifecycle action on user resources. Final comparison against the captured manifest verified all40 working source/test/configuration files byte-identical, including the original target. Only014 is this planning task's new repository artifact; Plan/requirements/contract/previous evidence were not edited.

The disposable copy and its temporary original bytes/hash manifests, helper, diff, collection outputs and caches were deleted after absolute-path containment verification under the explicit visualization root, together with the temporary014-active-scratch.txt marker. No temporary server/process remains; both pytest sessions exited after successful teardown. Planning results are complete and review-ready; milestone14 remains Pending until a separate human approval and repository execution.



Final working-directory documentation checks: git diff --check exited0 (only existing LF/CRLF informational notices for _http.py and voices/persistence.py); git status --short confirmed the pre-existing modified/untracked groups plus the new014 artifact. No working source/test/configuration or prior approval/evidence file was changed by this task.


### Enrollment Playback Link Test-Wiring Correction 014 execution evidence — 2026-10-27

Executed the exact approved OTHER 014 after approval recorded2026-10-27T05:28:04Z. This is actual repository execution evidence, distinct from 014's earlier disposable planning evidence. Only the approved enrollment test patch and PDD execution bookkeeping were applied by this executor. No production/dependency/configuration changes, full feature execution, model/calibration/enablement, commit or push were performed by this executor. GREEN remains Pending.

Task directory was `C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/014-execution-1e4b2ca89c1348d8baf3d1c3a506f042`. The exact approved diff and complete temporary helper were extracted using line-anchored fence boundaries and written UTF8 without BOM. The helper block's next language fence supplied its ending boundary; no helper/code change was made. Original target and40 source/test/configuration hashes plus authority/document snapshots were captured before application. All runtime invocations used the repository CWD and its existing interpreter.

Actual commands, in approved order, with temporary variables pointing into that task directory:

```powershell
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory --capture
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object (Join-Path $taskRun 'collection-before.txt')
docker info --format '{{.ServerVersion}}'
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -q -rA
git apply --ignore-space-change --check $patchFile
git apply --ignore-space-change $patchFile
.\.venv\Scripts\python.exe -m py_compile tests/test_voice_enrollment.py
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_enrollment_quality.py tests/test_voice_enrollment.py tests/test_persistence.py tests/test_authentication_consent.py --collect-only -q | Tee-Object (Join-Path $taskRun 'collection-after.txt')
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory
.\.venv\Scripts\python.exe $verificationFile $evidenceDirectory
.\.venv\Scripts\python.exe -m pytest -p no:anyio tests/test_persistence.py tests/test_authentication_consent.py -q -rA
git diff --check
git status --short
$beforeIds = @(Get-Content (Join-Path $taskRun 'collection-before.txt') | Where-Object { $_ -like 'tests/*::*' })
$afterIds = @(Get-Content (Join-Path $taskRun 'collection-after.txt') | Where-Object { $_ -like 'tests/*::*' })
if ($beforeIds.Count -ne 97 -or $afterIds.Count -ne 97 -or @(Compare-Object $beforeIds $afterIds).Count) { throw 'Test inventory changed' }
```

Capture exit0: `Captured 40 source/test/configuration files and original enrollment test`. Baseline collection exit0: `97 tests collected in 3.66s`. Restricted read-only Docker info exit1: `permission denied while trying to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`. This observed trigger applied the pre-authorized normal host-context contingency for the identical two pytest regression commands. Normal approval review approved both; no bypass and no Docker Desktop/engine lifecycle change. No loopback denial occurred and no other contingency was applied.

Baseline host session6149 exited0: `57 passed in 162.79s (0:02:42)`;33 persistence+24 Auth/Consent. Both fixture setup/isolation assertions and finally teardown completed with no error/skip/xfail. Exact patch check/application and compile each exited0 with no output. Postchange collection exit0: `97 tests collected in 5.62s`.

Both helper invocations exited0 with identical real output:

```text
PASS: 127 original assertions preserved; one origin assertion added; 3 request sites retain auth behavior
PASS: origin-relative/absolute links resolve once, signed query preserved, 3 external origins rejected; real HTTPX request construction checked
PASS: 39 other captured source/test/configuration files unchanged
```

Postchange host session88151 exited0: `57 passed in 197.26s (0:03:17)`; the same33+24 inventory, no failure/error/skip/xfail and successful teardown. No manual cleanup occurred between baseline and postchange. The two unchanged persistent runs and repeated isolated changed-transport checks satisfy the approved repeat protocol; no extra runtime rerun or expected feature failure was used.

Final diff check and status each exited0 with empty output before this bookkeeping. The two full collection files compared equal: all97 identities and their order are unchanged. Final manifest comparison verified39 other captured files byte-identical. Requirements, contract, blocked013 and approved proposal hashes also remained unchanged; Plan and approved014 bytes matched their pre-execution snapshots before these narrowly scoped status/evidence edits.

External working-tree activity was observed during verification: HEAD became `546df09` (`Milestone 013 GREEN: Complete voice enrollment with artifacts, voices, quality assessment, and AI enrollment modules`). That commit was not created by this executor and its label is not evidence of verified GREEN; Plan GREEN remains Pending. It incorporated the current test change, explaining the empty git status before bookkeeping. No commit was reset, reverted or pushed. Preservation was checked against the captured original bytes rather than inferred from git status.

The original target SHA256 was73164c87ce95cfb90d7c081b355d88644fefdf27c393ab4f9635e9278aad119e (756 LF,0 CRLF). Actual final target SHA256 is3fd25eebb6d90cbfe43e17a5d749af060543b7fd9243f19b245cc1b511001db7 (764 LF,764 CRLF); its normalized-LF SHA256 isbecd858b18467f79cb6ff671c45e5099cd2f67aac429f24bf2300973eed33aed. A read-only whole-file patch reconstruction from the captured original and exact approved diff verified the entire normalized final content equals that reconstruction. The actual authorized git-apply mechanics preserved exact approved code while applying Windows newline conventions; no extra code, formatting-independent structural change or assertion change exists. The planning representation hash is not substituted for actual execution bytes. `git diff --no-index` against the captured original printed exactly the approved import/helper/three-site changes, exit1 as expected for differing files, with an informational LF/CRLF notice.

Current production observation corrects a stale current-state sentence in approved014 without changing its scope/body: Artifact and Voices route declarations include `/api/v1`; the retained Artifact generated link still begins `/artifacts/`. This unfinished production discrepancy remains GREEN work. The test-only OTHER checks are explicitly independent of missing enrollment behavior, and no production fix or full feature pass is claimed here.

Owned projects were identified from each run's captured `isolated persistence project` stdout, not from all similarly named Docker resources:

| Run/module | Exact project | Container |
| --- | --- | --- |
| Baseline persistence | vnred6f16620b07904c5aa5d0956f6d1fc810 | 9b91d2e3c08556ddc8600cef6177e06eff8024e40d29409331252413e025b939 |
| Baseline Auth/Consent | vnredb6e80819c8e74787aa6685a7c8b90037 | 27f5b81a7045b2ae8c2659859337e9d552814fd3925f9943ff6b31143fadf4dc |
| Post persistence | vnred25d30026b4b54a05be46a3f6c0fe1287 | f116bfb92df457afe30491f3a43e482b450b2ec441e8fedf2b496eb2ed79ccba |
| Post Auth/Consent | vnredda9477c099a245eca486ef280e61a1c0 | 6b4d3d787aaeae7ff25cd0dc890496d9ff919b9a6a7b248a249fb409ce5ad508 |

For each exact project the following bounded read-only checks ran in approved host context:

```powershell
docker ps -a --filter ('label=com.docker.compose.project='+$project) --format '{{.ID}}'
docker network ls --filter ('label=com.docker.compose.project='+$project) --format '{{.ID}}'
docker volume ls --filter ('label=com.docker.compose.project='+$project) --format '{{.Name}}'
```

All12 checks exited0 with empty results. Final read-only `docker info --format '{{.ServerVersion}}'` exited0 and printed29.3.1. An earlier read-only service-label observation also saw pre-existing/parallel projects; they were never treated as owned or altered. Both pytest processes and the compile/collection/helper session exited; existing fixtures closed their own server threads, connections, databases/roles and random-project resources. User Docker remained running. No manual resource cleanup, global prune or unrelated lifecycle operation.

Deviations: no approved code, criterion, approach or verification command changed. The named Docker contingency was applied only after its actual trigger. Read-only exact-content/newline and external-commit observations provided preservation evidence; they did not authorize extra changes or reruns. Temporary evidence is removed only after this durable record is saved and the explicit task path's containment is verified.

#### Actual execution baseline preservation manifest

All entries except the approved target remained byte-identical. Target before/after and full-code comparison are recorded above.

| Captured path | Baseline SHA256 |
| --- | --- |
| .dockerignore | 37549f9cb3356952d07214273ed5e2fd98fe43faec132dd2b23039af640adf28 |
| .github/workflows/harness.yml | 532648b73020192444e61eb414f10affa16b7472abf0f365171185ab2bba79f0 |
| compose.harness.yaml | fac0c98fc3ef7e955cf3e52caf0f6ff62b3df561851f32fde410d61629172699 |
| containers/harness.Dockerfile | 06724a16480bd9f4ae2b9ad54d8bb95029843fb92439d31d81dd06f71687a38a |
| pytest.ini | 8ddeb7c45d2ab502c036d3c69ebfd45e82e79b796ac75b7c94af713956345bd7 |
| requirements-dev.txt | 47749870bd64d5c8399c02460eac6c0b81195ff8b16083054b24441a6da0a4aa |
| requirements-evaluator.txt | 612d628b604d266160cb19cf3de077123df5210dc46ed0593aab00409512ef56 |
| tests/test_authentication_consent.py | 2753e2dcedc5e585bb243fc467b56fd11fd7909b7f76b51c5d822468ca8c94ba |
| tests/test_enrollment_quality.py | 2ef07c8eb2f5a4af22c4ed95192a1a63244f3089688a9d561b8acff2825010b1 |
| tests/test_persistence.py | 47acbe6332947a21b693d77145eae0a6e69fb5fc26775fe62a80f1dbfb5d0a20 |
| tests/test_voice_enrollment.py | 73164c87ce95cfb90d7c081b355d88644fefdf27c393ab4f9635e9278aad119e |
| tools/evaluator_readiness.py | 08304bb62000defb653a6194d29fbff93b1cb986e9e4931ff03873afb93803c7 |
| tools/readiness.py | 249c3fbbb769578c63e70124d873a746527749da67fb1e487059bac95e85dedf |
| voice_narration/__init__.py | 228ccac3cc279f36bab313c47fa528b60f654ad8c338373e304862537fbad402 |
| voice_narration/_enrollment.py | aef31c9b0b3cece39fa703be3fa79ca036dde837d935de0811d6e1baf4541885 |
| voice_narration/_http.py | bf50672f5d2a7625882e013f22c98513d369e90732a0d53b4446d0e7332bd252 |
| voice_narration/_sql.py | a1c0436967508a56cb0ee8e68b4e0618e4beb4f6d0a33b192e82a795c2f6f7ac |
| voice_narration/ai/__init__.py | a5405078859bb3c31c35af431055de99392d3c6e18d8b572a349aa5a2ae2f94b |
| voice_narration/ai/enrollment.py | b3790e2e8515ddf6392614d8d3961db5d187462347cc6c0632ca3fb3c646dc90 |
| voice_narration/ai/persistence.py | d35617c38c237a793eeeb2efb509b37ee00157cd094304e7c85d4cf52aab9f7d |
| voice_narration/artifacts/__init__.py | e08de26e4e2d1c822ce358c2e36db380a90581e328e8c7d1656bf7cd718661b2 |
| voice_narration/artifacts/application.py | 490390b2b8967ea8b0d73f85110a838f212826b3207284cea80e26f891e15032 |
| voice_narration/artifacts/persistence.py | 42cffa83fca36acfa9883267d581ae6ecb0c5f7d81c18cc74b66d126fbd303b2 |
| voice_narration/audit/__init__.py | ddd47817b3bc7efb57b4769a5b5218f304a2444519e44d4b7adb25ab7fc1560b |
| voice_narration/audit/persistence.py | b8f2149fcbd5fef4d2a6fb58c86946d9bd74f07287ade872dbb2e843035a38c7 |
| voice_narration/auth/__init__.py | 05e38574f2fff4330aacd072c2367dbba611ab5a407b7dc2e559b19301024cce |
| voice_narration/auth/accounts.py | 5dbd8fec4104a7bf71c8375085b9c3059d70aeae8292dad48d8ecb9dfb86a3a5 |
| voice_narration/auth/application.py | 44438e6db640073f0ae9b07a009a0db7c68d3a443b6196f15a1997d9b08f09d4 |
| voice_narration/auth/persistence.py | 6fccb75784400bd3142e46999bd326d88a125584d1fc7743bf5e014574b02789 |
| voice_narration/consent/__init__.py | 33028d1c8feb70537e86aa20a4987d69e1f849eb7610373fe140b4297d46e95f |
| voice_narration/consent/application.py | 754e3b6008c3e28faeff64c30d7fd52b8118b146511f8b51b3aa0db5fd22f000 |
| voice_narration/consent/persistence.py | ba29e912a91d8759cf798db2ead56075fac564768dff71f5376004f407e81034 |
| voice_narration/jobs/__init__.py | 5364300b0c8943f7d3f0d38aabba69fc17126ffbf033d3f2d55df25dd975f7cd |
| voice_narration/jobs/persistence.py | 47e7097c63ab31b0a16b3ed424df1cdb1f4af2f1c41d925924ff46d02d9c6ae6 |
| voice_narration/policy/__init__.py | cd2ef341b82381e068f541528ccd78a51fa9025db9c387ba326576aa0ee2f778 |
| voice_narration/policy/persistence.py | e28f5f9ebcfdea76414df62b8ebd76694d1cc51948b00ca6ecd25491aaf8d8af |
| voice_narration/voices/__init__.py | d3c434dc3016c501bdfd549db6c756a5e8a3a048bcbf1a882b222ef1f0b39521 |
| voice_narration/voices/application.py | db628224427e18c95fc167ff63b183d7389c876d8e41cbd71acba2beac323678 |
| voice_narration/voices/persistence.py | b69f0512890ebb03f8829ad0318de086f62ae5d6838a58acb8a135aed55935ad |
| voice_narration/voices/quality.py | 208c4014a27095e306f699c2d261efd827851a9b2324133162ebf45fe5b29a81 |


Final temporary cleanup: the exact execution directory and marker were removed in one PowerShell session after resolving and verifying absolute containment under the explicit visualization root; both paths were then confirmed absent. All executor-started processes had already exited, owned runtime checks were empty, and no unrelated files/resources were removed.
