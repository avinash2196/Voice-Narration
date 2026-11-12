# Implementation Plan — CRM-9 Chatterbox Image Watermarker Dependency

## Milestone

CRM-9 — Chatterbox Image Watermarker Dependency, work item `chatterbox-cloud-run` (`Plan.md` revision 4, section "CRM-9 — Chatterbox Image Watermarker Dependency"). Scope as recorded: "Declare, in the dependency list the Chatterbox image installs, the packaging-tools release that Current State (Deployed Chatterbox after CRM-6) records as still providing the module and as verified on Cloud Run by the user". That release is `setuptools==80.10.2` (`Plan.md` Current State, "Fix verified on GCP by the user").

## Milestone Type

OTHER, as `Plan.md` records ("Milestone type: OTHER"; Execution Status row "CRM-9 … (OTHER) | Pending"). `Plan.md` gives the no-behavior-change statement: "no production source, test, contract or contracted answer changes; the declaration only constrains which packaging-tools release the image installs … No requirement CRM-9 owns adds or changes behavior; no local test can fail first, because the model runtime is not installed locally". This plan changes one line in `requirements-dev.txt` and no other file.

## Review Summary

- Behavior change: none. The image's dependency list pins `setuptools==80.10.2`, so the image installs a release that still ships `pkg_resources`.
- Requirements covered: the `Plan.md` traceability row "Chatterbox image's dependency set provides the model runtime's watermarker import (deployment defect, revision 4; needed for AC-CCR-1)".
- Files: created none. Modified `requirements-dev.txt` (one line added). Deleted none.
- Tests added: none. The preserved tests are the full suite (75 tests).
- Verification: C9-V (pip resolution for CPython 3.13 Linux, nothing installed) is expected to select `setuptools 80.10.2` with the other 124 packages unchanged. `./.venv/Scripts/python.exe -m pytest tests -ra` is expected to give `75 passed`.
- Needs attention: C9-D-1 (no explanatory comment line); C9-RSK-1 (the file is shared, so harness CI, the harness image, the inference-service image and local setup also get setuptools 80.10.2); C9-RSK-2 (80.10.2 is not the latest release, and setuptools publishes no support policy for older lines); C9-F-1 (a `Plan.md` Current State detail is inaccurate, which does not affect this change).

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 (its Status section) |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Revision 4, approved by avinash2196 on 2026-11-11 ("Approve revision 4"). Execution Status: CRM-1 to CRM-8 Complete, CRM-9 Pending |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (CCD-1 to CCD-7). CRM-1 row Complete. Constraint only: `Plan.md` External Contract Requirements says "The dependency fix of CRM-9 (revision 4) changes no contract" |
| `001_Implementation_Plan_Chatterbox_Service_RED.md` to `004_Implementation_Plan_Inference_Client_GREEN.md` | Approved and executed (Human Review sections). Read for Carried-Forward Decisions only; none touches `requirements-dev.txt` |
| `005_Implementation_Plan_Chatterbox_Cloud_Run_Deployment_Document.md` | Revision 2, approved by avinash2196 on 2026-11-11 ("Approve both"); executed. Source of the resolution command and the UD-1 and UD-2 decisions |
| `006_Implementation_Plan_Chatterbox_Model_Loading_RED_Chatterbox_Model_Loading_GREEN.md` | Approved 2026-11-10; executed. Carried-forward decision C8-D-1 |
| `docs/requirements.md` (product level) | Absent |
| `docs/developer-setup.md` | Repository documentation. Lines 14 and 27 install `requirements-dev.txt` locally |
| Plugin skills `implementation-planning` and `prompt-driven-development` (with `templates/Implementation-Plan.md`) | Plugin guidance. `security` does not apply, because CRM-9 neither owns nor verifies an authentication or authorization requirement. There are no identity comparisons |

External sources, read on 2026-11-11:

| Source | Used for |
| --- | --- |
| `https://pypi.org/pypi/setuptools/80.10.2/json` | Not yanked; `requires_python >=3.9`; no runtime `requires_dist`; wheel `setuptools-80.10.2-py3-none-any.whl`, SHA-256 `95b30ddf…0173`, uploaded 2026-01-25 |
| `https://pypi.org/pypi/setuptools/json` | Latest release is 84.2.1 (2026-10-20). Releases 80.10.1, 80.10.2 and 81.0.0 exist |
| `https://pypi.org/pypi/resemble-perth/1.0.1/json` | Latest release is 1.0.1; `requires_dist` is empty |
| Wheels downloaded to the planning scratchpad, inspected as zip files, not installed: setuptools 80.10.2 (`95b30ddf…0173`), 81.0.0 and 84.2.1 (`ca140b45…89c2`); resemble-perth 1.0.1 (`65e9c375…9342`) | `pkg_resources/__init__.py` is present in 80.10.2 and 81.0.0 and absent in 84.2.1. In perth: `perth/__init__.py:13-15` imports `PerthImplicitWatermarker` inside `try`, and `except ImportError:` sets it to `None`; `perth/perth_net/__init__.py:1` reads `from pkg_resources import resource_filename`. In setuptools 80.10.2, `pkg_resources/__init__.py` warns: "The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81." |
| `https://setuptools.pypa.io/en/latest/history.html` (first 100,000 characters) | v82.0.0 (2026-02-08): "`pkg_resources` has been removed from Setuptools." The page states no support or LTS policy for older release lines |

## Carried-Forward Decisions

- `005_…` UD-1 and UD-2 (kept by `Plan.md` revision 4 and by the user for this run): no local Docker image build, no container, and no `gcloud` command in planning or execution.
- `005_…` C6-V5 resolution command (`Plan.md` Verification Commands, CRM-6): pip `install --dry-run --ignore-installed` for CPython 3.13 `cp313` manylinux x86_64, binary only. `Plan.md` CRM-9 adds `--report`. C9-V reuses the command unchanged and adds only `--report`.
- `005_…`: base image `python:3.13.17-slim-trixie` (`cloudrun/chatterbox-service/Dockerfile:1`). `006_…` C8-D-1: the model is loaded with `from_pretrained(device=DEVICE)`. Neither changes here.
- Execution convention (`Plan.md` CRM-6 evidence): commands run from Git Bash as `./.venv/Scripts/python.exe …`, with output written to log files and only summaries recorded.

## Preconditions / Predecessor Evidence

- Predecessor CRM-6 (OTHER) is Complete (`Plan.md` row: "C6-AC-1–C6-AC-9 met … 75 of 75 pass"). It is committed as `26c01e3` ("CRM-6: private Cloud Run deployment document and Cloud Build image"), which is `HEAD` (`26c01e373c69fe907e5a85cf16f50611370fdd6e`).
- CRM-9 is Pending. No other Implementation Plan exists for it. The milestone type is OTHER in `Plan.md` and OTHER here.
- `git status --short` on 2026-11-11: ` M docs/.ai/chatterbox-cloud-run/Plan.md` only, which is the approved revision 4 under `docs/.ai/<work-item>/` and so expected.
- Manual-deployment baseline and completion evidence (`Plan.md` Current State, "Deployed Chatterbox after CRM-6", reported by the user and not produced by this milestone): revision `chatterbox-model-api-00001-8j8` returned `/v1/metadata` 500 with `TypeError: 'NoneType' object is not callable` at `chatterbox/mtl_tts.py:155`. With `setuptools==80.10.2`, revision `chatterbox-model-api-00002-vqx` returned metadata 200, and a voice_cloning job completed with a 200 answer.
- Pre-existing failures: none known. The last full run was `75 passed` at CRM-6 (C6-V7). The suite was not re-run during planning (see Planning-Time Dry Run).

## Current Repository State

- `requirements-dev.txt:1-10` holds ten pins and ends with `chatterbox-tts==0.1.7` (`:10`). It has no `setuptools` line. The index stores it with LF and the working tree with CRLF (`git ls-files --eol`: `i/lf w/crlf`; `core.autocrlf=true`). SHA-256 with CR removed: `ab1f38b2081693fea2aaf2e8dd34afba950bb772a58fc58a8ab799278f0ea989`.
- `cloudrun/chatterbox-service/Dockerfile:1` `FROM python:3.13.17-slim-trixie`; `:9-10` copies and installs `requirements-dev.txt`.
- Other consumers of `requirements-dev.txt`: `.github/workflows/harness.yml:12,15-16` (Python `3.13.17`, `pip install -r`, `pip check`), `containers/harness.Dockerfile:1,4`, `cloudrun/inference-service/Dockerfile:1,6` and `docs/developer-setup.md:14,27`.
- No Python, TOML, CFG, INI or YAML file outside `.venv` references `setuptools` or `pkg_resources`; a repository search returned no output. No test reads `requirements-dev.txt`.
- The local `.venv` has setuptools 84.2.1 and no `pkg_resources`, and the model runtime is not installed (`Plan.md` Current State). Nothing in this plan installs anything.

## Files in Scope

### Files to Create

None.

### Files to Modify

- `requirements-dev.txt`

### Files to Delete

None.

## Proposed Changes

1. `requirements-dev.txt`: add one line, `setuptools==80.10.2`, as a new line 11 after `chatterbox-tts==0.1.7`. This is required by `Plan.md` CRM-9 Scope. With it, pip resolves the image's unpinned `setuptools` requirement (from `torch==2.6.0`, `setuptools ; python_version >= "3.12"`, shown in the dry-run report) to 80.10.2, which ships `pkg_resources/__init__.py`. perth's `perth/perth_net/__init__.py:1` imports from that module. No other line changes.

Decision for review:

- C9-D-1: the pin is a bare line with no comment, and it is placed last. `Plan.md` CRM-9 Completion evidence says "the dependency list declares the verified packaging-tools release and nothing else changes". Alternative: add a comment line above the pin naming its reason (perth's `pkg_resources` import). That is clearer for maintainers, but it adds a second changed line, which needs your explicit approval.

## Proposed Code / Tests

`requirements-dev.txt`, unified diff against `HEAD` (LF, as stored in the index):

```diff
--- a/requirements-dev.txt
+++ b/requirements-dev.txt
@@ -8,3 +8,4 @@
 av==19.0.2
 playwright==1.64.1
 chatterbox-tts==0.1.7
+setuptools==80.10.2
```

Complete final content (11 lines; SHA-256 with CR removed `513993f80e763fce9a60a74fe3f0689055b8c24692793fdd4db6d7c8d0e41df1`; working-tree CRLF form `7e1b438b7224c76eff1807d196d36590953e83a35aab2fc45a5c4f28887b1ce5`):

```text
fastapi==0.162.0
uvicorn==0.54.0
python-multipart==0.0.32
pytest==9.1.1
httpx==0.28.1
psycopg[binary]==3.3.6
numpy==2.5.4
av==19.0.2
playwright==1.64.1
chatterbox-tts==0.1.7
setuptools==80.10.2
```

Verification helper, written by each verification block into its own `mktemp -d` directory and never into the repository (`read_report.py`, 24 lines, SHA-256 `44fa439383581611e2b661a9150bec62977765c8a5220d5a5158ef85ecfc580b`):

```python
import hashlib
import json
import re
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    report = json.load(handle)
packages = {item["metadata"]["name"].lower(): item for item in report["install"]}
setuptools = packages.get("setuptools")
others = sorted(
    f"{name}=={item['metadata']['version']}"
    for name, item in packages.items()
    if name != "setuptools"
)
print("packages", len(packages))
print("setuptools", setuptools["metadata"]["version"] if setuptools else "absent")
print("setuptools requested", setuptools["requested"] if setuptools else "absent")
print("others", len(others), hashlib.sha256("\n".join(others).encode("utf-8")).hexdigest())
for name, item in sorted(packages.items()):
    for requirement in item["metadata"].get("requires_dist") or []:
        if re.match(r"setuptools\b", requirement) and "extra ==" not in requirement:
            print("requires setuptools:", f"{name}=={item['metadata']['version']}", "|", requirement)
for name in ("torch", "chatterbox-tts", "resemble-perth"):
    print(name, packages[name]["metadata"]["version"] if name in packages else "absent")
```

The `others` digest covers every resolved package except setuptools. It lets the baseline and after-change runs, which happen in separate invocations, be compared without sharing a file.

## Execution Steps

1. Confirm that this plan's Human Review records approval and that `git status --short` shows only `docs/.ai/chatterbox-cloud-run/` changes.
2. Run C9-B (baseline) as one Git Bash invocation, in the background with a completion notice, and record its summary lines before any change (C9-AC-1).
3. Apply the change, preserving the working tree's CRLF ending: `printf 'setuptools==80.10.2\r\n' >> requirements-dev.txt` from the repository root.
4. Run C9-V (verification) as one Git Bash invocation, in the background, and record its summary lines (C9-AC-2 to C9-AC-5).
5. Record the evidence in `Plan.md` Execution Status and update this plan's Human Review.

## Acceptance / Completion Criteria

- C9-AC-1: the baseline is recorded before the change. `requirements-dev.txt` has no `setuptools` line, and its SHA-256 with CR removed is `ab1f38b2…a989`. The C9-B resolution exits 0 and selects a setuptools release other than 80.10.2 that was not requested. The full suite gives 75 collected, 75 passed. The manual-deployment evidence of `chatterbox-model-api-00001-8j8` is cited from `Plan.md` Current State.
- C9-AC-2: `requirements-dev.txt` has SHA-256 with CR removed `513993f8…1df1`. `git diff -- requirements-dev.txt` is the single hunk `+setuptools==80.10.2` with no removed line.
- C9-AC-3: no other file changes outside `docs/.ai/chatterbox-cloud-run/`. This excludes this milestone's own `Plan.md` Execution Status update.
- C9-AC-4: the C9-V resolution exits 0. It selects `setuptools 80.10.2` with `setuptools requested True`, and its `others` count and digest equal C9-B's.
- C9-AC-5: the full suite gives 75 collected, 75 passed, with no `FAILED` or `ERROR` line.
- C9-AC-6: no Docker image is built, no container is started, no `gcloud` command is run and nothing is installed into `.venv`. The completion evidence of `chatterbox-model-api-00002-vqx` is cited from `Plan.md` Current State as evidence the user obtained, not produced here.

## Verification

### Commands

C9-B, baseline (before step 3):

```bash
cd "$(git rev-parse --show-toplevel)"
SCRATCH="$(mktemp -d)"
echo "scratch=$SCRATCH"
git rev-parse HEAD
git status --short
grep -ci '^setuptools' requirements-dev.txt; echo "setuptools-lines-exit=$?"
tr -d '\r' < requirements-dev.txt | sha256sum
cat > "$SCRATCH/read_report.py" <<'EOF'
import hashlib
import json
import re
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    report = json.load(handle)
packages = {item["metadata"]["name"].lower(): item for item in report["install"]}
setuptools = packages.get("setuptools")
others = sorted(
    f"{name}=={item['metadata']['version']}"
    for name, item in packages.items()
    if name != "setuptools"
)
print("packages", len(packages))
print("setuptools", setuptools["metadata"]["version"] if setuptools else "absent")
print("setuptools requested", setuptools["requested"] if setuptools else "absent")
print("others", len(others), hashlib.sha256("\n".join(others).encode("utf-8")).hexdigest())
for name, item in sorted(packages.items()):
    for requirement in item["metadata"].get("requires_dist") or []:
        if re.match(r"setuptools\b", requirement) and "extra ==" not in requirement:
            print("requires setuptools:", f"{name}=={item['metadata']['version']}", "|", requirement)
for name in ("torch", "chatterbox-tts", "resemble-perth"):
    print(name, packages[name]["metadata"]["version"] if name in packages else "absent")
EOF
sha256sum "$SCRATCH/read_report.py"
./.venv/Scripts/python.exe -m pip install --dry-run --ignore-installed --quiet --python-version 3.13 --implementation cp --abi cp313 --platform manylinux_2_28_x86_64 --platform manylinux2014_x86_64 --platform manylinux1_x86_64 --only-binary=:all: -r requirements-dev.txt --report "$SCRATCH/report.json" > "$SCRATCH/resolve.log" 2>&1; echo "resolve-exit=$?"
./.venv/Scripts/python.exe -I "$SCRATCH/read_report.py" "$SCRATCH/report.json"
./.venv/Scripts/python.exe -m pytest tests -ra > "$SCRATCH/pytest.log" 2>&1; echo "pytest-exit=$?"
grep -E '^collected|^=+ .*(passed|failed|error)|^(FAILED|ERROR)' "$SCRATCH/pytest.log"
rm -rf "$SCRATCH"
```

C9-V, verification (after step 3). This block is the same as C9-B except for its first checks:

```bash
cd "$(git rev-parse --show-toplevel)"
SCRATCH="$(mktemp -d)"
echo "scratch=$SCRATCH"
tr -d '\r' < requirements-dev.txt | sha256sum
git diff -- requirements-dev.txt
git status --short
git status --short -- voice_narration tests cloudrun containers frontend .github .dockerignore .gitignore pytest.ini docs/developer-setup.md
cat > "$SCRATCH/read_report.py" <<'EOF'
import hashlib
import json
import re
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    report = json.load(handle)
packages = {item["metadata"]["name"].lower(): item for item in report["install"]}
setuptools = packages.get("setuptools")
others = sorted(
    f"{name}=={item['metadata']['version']}"
    for name, item in packages.items()
    if name != "setuptools"
)
print("packages", len(packages))
print("setuptools", setuptools["metadata"]["version"] if setuptools else "absent")
print("setuptools requested", setuptools["requested"] if setuptools else "absent")
print("others", len(others), hashlib.sha256("\n".join(others).encode("utf-8")).hexdigest())
for name, item in sorted(packages.items()):
    for requirement in item["metadata"].get("requires_dist") or []:
        if re.match(r"setuptools\b", requirement) and "extra ==" not in requirement:
            print("requires setuptools:", f"{name}=={item['metadata']['version']}", "|", requirement)
for name in ("torch", "chatterbox-tts", "resemble-perth"):
    print(name, packages[name]["metadata"]["version"] if name in packages else "absent")
EOF
sha256sum "$SCRATCH/read_report.py"
./.venv/Scripts/python.exe -m pip install --dry-run --ignore-installed --quiet --python-version 3.13 --implementation cp --abi cp313 --platform manylinux_2_28_x86_64 --platform manylinux2014_x86_64 --platform manylinux1_x86_64 --only-binary=:all: -r requirements-dev.txt --report "$SCRATCH/report.json" > "$SCRATCH/resolve.log" 2>&1; echo "resolve-exit=$?"
./.venv/Scripts/python.exe -I "$SCRATCH/read_report.py" "$SCRATCH/report.json"
./.venv/Scripts/python.exe -m pytest tests -ra > "$SCRATCH/pytest.log" 2>&1; echo "pytest-exit=$?"
grep -E '^collected|^=+ .*(passed|failed|error)|^(FAILED|ERROR)' "$SCRATCH/pytest.log"
rm -rf "$SCRATCH"
```

If `resolve-exit` is not 0, record the last lines of `resolve.log` before the block deletes the directory. A non-zero exit stops execution.

### Affected Tests

None. No test reads `requirements-dev.txt`, and no repository code references `setuptools` or `pkg_resources`; repository search on 2026-11-11 found none. Nothing is installed into `.venv`, so the test environment does not change. The full suite (75 tests, the `Plan.md` CRM-9 Preserved tests) runs once before and once after the change.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- C9-B: `setuptools-lines-exit=1` (count `0`); hash `ab1f38b2…a989`; `resolve-exit=0`; `packages 125`; `setuptools 84.2.1` (or whichever release is latest at execution; anything other than 80.10.2), `setuptools requested False`; `others 124 f68588d1aa5a92d5faa51fd0c1c329ca2ae660a9552e1a99fd07bb7541f64818`; `requires setuptools: torch==2.6.0 | setuptools ; python_version >= "3.12"`; `torch 2.6.0`, `chatterbox-tts 0.1.7`, `resemble-perth 1.0.1`; `collected 75 items`, `75 passed`.
- C9-V: hash `513993f8…1df1`; the diff has one hunk with the single added line `+setuptools==80.10.2`; `git status --short` shows ` M requirements-dev.txt` plus `docs/.ai/chatterbox-cloud-run/` files; the scoped status prints nothing; `resolve-exit=0`; `packages 125`; `setuptools 80.10.2`, `setuptools requested True`; `others 124 f68588d1…4818`, the same as C9-B; `collected 75 items`, `75 passed`.
- Preserved-behavior tests (expected to pass at RED): not applicable (OTHER).

### Planning-Time Dry Run

This is not milestone evidence. It was run on 2026-11-11 in `…/scratchpad/c9/` (session scratchpad), outside the repository:

- `git show HEAD:requirements-dev.txt > applycopy/requirements-dev.txt; git apply --check -v ../c9.patch; git apply ../c9.patch` (the diff above): `Checking patch requirements-dev.txt...`, applied. Result: 11 lines, SHA-256 with CR removed `513993f8…1df1`.
- `printf 'setuptools==80.10.2\r\n' >> copy/requirements-dev.txt` (step 3 on a copy of the working-tree file): CRLF SHA-256 `7e1b438b…1ce5`, CR removed `513993f8…1df1`.
- The resolution command above, with `-r requirements-dev.txt` (repository, unmodified) and `--report report-base.json`: `resolve-base-exit=0`; reader: `packages 125`, `setuptools 84.2.1`, `requested False`, `others 124 f68588d1…4818`, `requires setuptools: torch==2.6.0 | setuptools ; python_version >= "3.12"`.
- The same command with `-r copy/requirements-dev.txt` and `--report report-after.json`: `resolve-after-exit=0`; `packages 125`, `setuptools 80.10.2`, `requested True`, `others 124 f68588d1…4818`. Comparing the two reports: `diff [('setuptools', '84.2.1', '80.10.2')]`.
- Wheel inspection (see External sources): `pkg_resources/__init__.py` is present in 80.10.2 and absent in 84.2.1.
- Not run: pytest, because the Affected Tests list is empty and an OTHER dry run runs only new and affected tests. The full suite runs once before and once after at execution. No image build, container or `gcloud` command was run (UD-1, UD-2).
- Files created: only the scratchpad's `c9/` folder (`meta/`, `whl/`, `copy/`, `applycopy/`, `c9.patch`, `read_report.py`, reports and logs). It is deleted after this plan is written.

## Risks

- C9-RSK-1, shared dependency file: `requirements-dev.txt` is also installed by harness CI (`.github/workflows/harness.yml:15`), the harness image (`containers/harness.Dockerfile:4`), the inference-service image (`cloudrun/inference-service/Dockerfile:6`) and local setup (`docs/developer-setup.md:14,27`). All of them will now install setuptools 80.10.2; the local `.venv` currently has 84.2.1. No repository code uses setuptools (Current Repository State). C9-V shows the full pin set still resolves for CPython 3.13 with no other version change. CI, the harness image and the inference image are not run by this milestone (UD-1).
- C9-RSK-2, release support: setuptools 80.10.2 is not the latest release (84.2.1). The setuptools history page states no support policy for older lines, so maintainer support for 80.10.2 cannot be shown. The version is fixed by approved `Plan.md` CRM-9 Scope and Current State, and `Plan.md` RSK-11 records the residual risk. The setuptools 80.10.2 warning text recommends "pin to Setuptools<81". At runtime that `UserWarning` will appear in the Cloud Run log when perth imports `pkg_resources`. This is a hypothesis; it was not observed here.
- C9-F-1, finding with no change needed: `Plan.md` Current State says "current `setuptools` releases (81 and later, latest 84.2.1) no longer ship `pkg_resources`". The 81.0.0 wheel does contain `pkg_resources/__init__.py`, and the history page records the removal in v82.0.0. The verified release, 80.10.2, is unaffected. Correcting that sentence is a `Plan.md` matter for the user.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Remove only the added last line of `requirements-dev.txt`, so that the CR-removed hash returns to `ab1f38b2…a989`. Do not use repository-wide reset, checkout or clean operations.

## Explicitly Out of Scope

These are excluded, as `Plan.md` CRM-9 lists:

- Any change to production source, tests, the contract, `cloudrun/chatterbox-service/Dockerfile`, `cloudbuild.json`, `Dockerfile.dockerignore`, `.dockerignore` or the deployment document.
- Any other dependency declaration or version change, including a `resemble-perth` change.
- Documenting the `gcloud run deploy --source` route (a follow-up).
- Building an image, starting a container, running `gcloud`, or performing or repeating the deployment.
- Installing the model runtime, setuptools or anything else into `.venv`, and acquiring model weights.
- Custom logging, metrics or alerts.

## Human Review

Status: Executed on 2026-11-11 (approved by avinash2196 on 2026-11-11, "Approve plan", including C9-D-1 and accepting C9-RSK-1 and C9-RSK-2) — see `Plan.md` "CRM-9 Execution Evidence".
