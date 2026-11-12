# Implementation Plan — CRM-6 Chatterbox Cloud Run Deployment Document

Revision 2 (2026-11-11), replacing the unapproved revision 1 of 2026-11-10. What changed is listed under "Changes from Revision 1" at the end.

## Milestone

CRM-6 — Chatterbox Cloud Run Deployment Document, work item `chatterbox-cloud-run` (`Plan.md` revision 2, section "CRM-6 — Chatterbox Cloud Run Deployment Document"). Scope as recorded: a deployment document that describes how to build the Chatterbox image; deploy it as a separate Cloud Run service (AGW-011) in project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, on an NVIDIA L4 GPU (CCR-1, CCR-3, CCR-4); make it private, callable only by `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` (CCR-7); scale to zero with at most 1 instance and one request at a time; set a Cloud Run request time limit that accommodates the 10-minute cloning limit (CCR-9); and configure the local inference service with the contract's settings. Container build and deployment artifacts change "only where the documented steps cannot otherwise satisfy these items". Owned: CCR-1, CCR-3, CCR-4, CCR-11, Deployment characteristic.

## Milestone Type

OTHER — as `Plan.md` records ("Milestone type: OTHER"; Execution Status row "CRM-6 … (OTHER) | Pending"). `Plan.md` records the no-behavior-change statement: "the document and any container build or deployment artifact change alter no service's request handling, validation, failure answers or data handling; selecting the GPU device uses the existing device setting (RF-5). All behavior changes are delivered by CRM-3, CRM-5 and CRM-8." This plan changes no file under `voice_narration/` or `tests/`.

## Review Summary

- Behavior change: none. Documentation plus the Chatterbox image's build inputs: base image, a per-Dockerfile ignore file, and a Cloud Build configuration.
- Requirements covered: CCR-1, CCR-3, CCR-4, CCR-7 (Cloud Run side), CCR-9 (platform time limit), CCR-11, Deployment, Consistency and concurrency (platform settings), AC-CCR-8.
- Files: created `cloudrun/chatterbox-service/Dockerfile.dockerignore`, `cloudrun/chatterbox-service/cloudbuild.json`; modified `cloudrun/chatterbox-service/Dockerfile` (line 1), `cloudrun/chatterbox-service/README.md` (replaced); deleted none.
- Tests added: none. Local checks: Cloud Build config structure, pip resolution for Linux CPython 3.13, build-context and secret-exclusion model; no Docker image is built, no container started, no `gcloud` command run (user decisions UD-1, UD-2).
- Verification: `.\.venv\Scripts\python.exe -m pytest tests -ra` — expected `75 passed`; C6-V4 to C6-V6 as listed.
- Needs attention: C6-Q-2 (the approved `Plan.md` CRM-6 completion evidence requires a local image build, which UD-1 forbids; a `Plan.md` revision is needed before approval); C6-D-14 (copy step in Cloud Build); C6-RSK-2 and C6-RSK-12 (image build, deployment and real model load first proven by the user's manual deployment).

## Question for Review Before Approval

C6-Q-2 — The approved Plan requires a local image build that the user's decision forbids.

- `Plan.md` CRM-6 Completion evidence: "… the full suite passes; and, if this milestone changes the container build or the build-context exclusions, the Chatterbox image builds locally and, for an exclusions change, the harness image still builds and runs." `Plan.md` Verification Commands name `docker build -f cloudrun/chatterbox-service/Dockerfile -t chatterbox-model-api:local .` for CRM-6 when it changes the container build.
- This plan changes the container build (Dockerfile line 1; the documented build cannot succeed otherwise, B5). UD-1 says no Docker image is built and no container started, in planning or execution. So C6-AC criteria cannot include the local build the Plan requires, and an Implementation Plan cannot change a Plan's success criteria (`prompt-driven-development` Artifact Authority).
- This plan is written as if the Plan said: "the Chatterbox image build, the deployment and the real model load are first proven by the user's manual Cloud Build deployment; locally, the full suite passes, the image's pinned dependencies resolve for Linux CPython 3.13, and a build-context check without an image build shows that only the files the Dockerfile copies, and no secret, enter the context." The shared `.dockerignore` is not changed, so the harness clause does not apply.

Options (this plan does not choose):

1. Revise `Plan.md` (`create-plan` revision mode, revision 3) to replace that CRM-6 completion-evidence clause and its two CRM-6 Verification Commands with the wording above, then review this plan. Its content is not expected to change.
2. Another direction the user names.

## User Decisions Recorded

- UD-1 [User, 2026-11-11]: "Do NOT build any Docker image and do NOT start any Docker container, in this planning dry run or in the execution steps — the local machine has no L4 GPU and the network is too slow for the ~3 GB+ CUDA/PyTorch downloads." This resolves revision 1's partial dry run: the image build is not run locally at all.
- UD-2 [User, 2026-11-11]: "Do NOT run any gcloud command (no flag checks, no builds, no deploys) in planning or execution. The user will deploy manually on GCP, building the image in the cloud with Cloud Build (gcloud builds submit), and will then share the service URL so an end-to-end cloning test can be run from the local inference service." The document describes the Cloud Build route (C6-D-4). The image build, deployment and real model load are first proven by the user's manual deployment; the end-to-end cloning test is after this milestone and is not one of its criteria (Explicitly Out of Scope).
- UD-3 [User, 2026-11-11]: keep only quick local checks — the 75-test suite, pip dependency resolution, and a build-context/secret-exclusion check that builds no image (C6-V4 to C6-V7).
- C6-Q-1 [User: C6-Q-1, 2026-11-10] (revision 1's question on model loading): option 1 chosen; `Plan.md` revision 2 added CRM-7 and CRM-8, both Complete (commit `29d8a31`). Resolved; no longer blocks this plan.
- The `scribe-*` containers on this machine belong to another project; nothing in this plan touches Docker at all.

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Revision 2 — approved by avinash2196 on 2026-11-10 ("Approve revision 2"). Execution Status: CRM-1 to CRM-5, CRM-7, CRM-8 Complete; CRM-6 Pending |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (CCD-1–CCD-7). Authoritative predecessor; CRM-1 row Complete |
| `001_Implementation_Plan_Chatterbox_Service_RED.md` | Revision 2 approved 2026-11-09; executed |
| `002_Implementation_Plan_Chatterbox_Service_GREEN.md` | Approved 2026-11-09; executed. Carried-forward decisions |
| `003_Implementation_Plan_Inference_Client_RED.md` | Approved 2026-11-09; executed |
| `004_Implementation_Plan_Inference_Client_GREEN.md` | Approved 2026-11-10; executed. Carried-forward decisions |
| `006_Implementation_Plan_Chatterbox_Model_Loading_RED_Chatterbox_Model_Loading_GREEN.md` | Approved 2026-11-10; Human Review "Executed — see Plan.md". Carried-forward decisions |
| `docs/requirements.md` (product level) | Absent |
| `docs/.ai/ai-gateway-multimodel/requirements.md` AGW-011, `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Not re-read; quoted by the approved requirements and `Plan.md`; unchanged constraints |
| `docs/developer-setup.md` | Repository documentation (CPython 3.13.17; verification command) |
| Plugin skills: `implementation-planning`, `prompt-driven-development` (with `templates/Implementation-Plan.md`), `security` | Plugin guidance |

`security` applies because the document configures private access (CCR-7, owned by CRM-5, verified by CRM-4) and the build route must keep the service-account key out of the upload and the image. Identity comparisons: C6-RSK-1.

External sources (cited where used):

| Source | Read | Used for |
| --- | --- | --- |
| `https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit` | 2026-11-11 | `--config` ("The YAML or JSON file to use as the build configuration file"); `--substitutions` keys "must begin with an underscore"; without `.gcloudignore`, "gcloud will use a generated Git-compatible .gcloudignore file that respects your .gitignored files"; `--region` defaults to global |
| `https://docs.cloud.google.com/sdk/gcloud/reference/topic/gcloudignore` | 2026-11-11 | gitignore-like syntax; re-including inside excluded directories is not documented (C6-D-15) |
| `https://docs.cloud.google.com/build/docs/build-config-file-schema` | 2026-11-11 | default build timeout 60 minutes; `images` are pushed to Artifact Registry and the build fails if one is not produced; a missing substitution is an error; default machine `e2-standard-2` |
| `https://github.com/GoogleCloudPlatform/cloud-builders/tree/master/docker` | 2026-11-11 | the builder "may not support the most recent features or versions of Docker"; no version or BuildKit statement (C6-D-14) |
| `https://docs.cloud.google.com/build/docs/cloud-build-service-account-updates`, `https://docs.cloud.google.com/build/docs/cloud-build-service-account` | 2026-11-11 | new projects build as the Compute Engine default service account; `roles/cloudbuild.builds.builder` includes `artifactregistry.repositories.uploadArtifacts` and `logging.logEntries.create` |
| Cloud Run GPU, autoscaling, concurrency, request-timeout, container-contract, service-to-service, deploying pages; Docker build-context page; `devguide.python.org/versions`; PyPI metadata of `numpy 2.5.4`, `av 19.0.2`, `chatterbox-tts 0.1.7`; Hugging Face file listing of `ResembleAI/chatterbox` | 2026-11-10, by revision 1 (URLs and facts unchanged; not re-read) | GPU minimums, L4 in `asia-southeast1`, quota, `429` beyond capacity, timeout max 3600 and `504`, in-memory file system and idle shutdown, token audience and `roles/run.invoker`, Dockerfile-specific ignore file, Python 3.13 supported to 2029-10, Python-version constraints of the pins, 2.99 GiB weights |
| Installed Google Cloud SDK 564.0.0 `--help` | 2026-11-10, by revision 1 | every `gcloud run`, `artifacts`, `services` and `config` flag the document uses printed `ok`. Not re-run (UD-2); `builds submit` flags are from the reference page only |

## Carried-Forward Decisions

- `API-Contract.md`: CCD-4 (identity token for `test-850@…` with audience = base URL; Cloud Run enforces with `401`/`403`; deployment settings belong to "the deployment document of CRM-6"); CCD-6 (`VOICE_CLONING_TIMEOUT_SECONDS`, default `600`); CCD-7 (`VOICE_CLONING_API_BASE_URL`, fallback `CHATTERBOX_API_BASE_URL`; key located as the narration provider does); CCD-9 to CCD-11 (one at a time with waiting; no retention; retries make a new clip).
- `002_…_GREEN.md`: C3-D-3 — one-at-a-time serving with a `threading.Lock` in a thread-pool worker; C3-RSK-3 assigns the instance and per-instance request settings to CRM-6 (here C6-D-6).
- `004_…_GREEN.md`: C5-RSK-1 (base URL used unchanged as call target and audience; trailing `/` mismatch is CFR-7, documented by CRM-6); C5-RSK-2 (documented URL is `https://`); C5-D-2 / C4-D-6 (base URL and timeout read at import, key located at call time, so a `.env` does not set the two).
- `006_…_GREEN.md`: C8-D-1 — the model is loaded with `from_pretrained(device=DEVICE)` (`voice_narration/chatterbox_api/application.py:43`); C8-RSK-1 — `CHATTERBOX_MODEL_VARIANT` is reported by health and metadata but does not select weights. The document's variant row says so.
- Conventions (`Plan.md` execution evidence): files written with LF endings and checked by SHA-256; Git warns `LF will be replaced by CRLF`.

## Preconditions / Predecessor Evidence

- Predecessor CRM-8 (GREEN): `Plan.md` row "CRM-8 — Chatterbox Model Loading GREEN (GREEN) | Complete | … `voice_narration/chatterbox_api/application.py` matches the planned SHA-256 (`a8432b4d…5281`) … 75 of 75 pass in the full run". Committed as `29d8a31` ("CRM-7/CRM-8: fix Chatterbox model loading for chatterbox-tts 0.1.7"), which is `HEAD`.
- CRM-7, CRM-5, CRM-3, CRM-1 are Complete (`Plan.md` Execution Status).
- CRM-6 is Pending. The only Implementation Plan for it is this file, revision 1 unapproved; no approved, unexecuted plan exists. Milestone type check: OTHER in `Plan.md`, OTHER here.
- Baseline evidence `Plan.md` names (read-only on 2026-11-11 at `29d8a31`; re-recorded at execution step 2):
  - B1 — `cloudrun/chatterbox-service/README.md:6-13`: `gcloud builds submit --tag gcr.io/<PROJECT_ID>/chatterbox-model-api -f …`, `--region <REGION>`, `--allow-unauthenticated` (`:11`), `CHATTERBOX_DEVICE=cpu` (`:13`); no GPU, instance-count, concurrency or timeout option.
  - B2 — `cloudrun/chatterbox-service/Dockerfile:1` `FROM python:3.11-slim`; `:14` `ENV CHATTERBOX_DEVICE=cpu`.
  - B3 — `.dockerignore:1-4`: `*`, `!requirements-dev.txt`, `!containers/`, `!containers/harness.Dockerfile`.
  - B4 — full suite: `75 passed` at CRM-8 (C8-V1); re-run at execution step 2.
  - B5 — the documented image cannot build, shown without building: (a) pip resolution of `requirements-dev.txt` for CPython 3.11 fails with `No matching distribution found for numpy==2.5.4` (dry run D2); (b) the root `.dockerignore` admits only `containers/harness.Dockerfile` and `requirements-dev.txt` of the upload set, so `COPY voice_narration` has no source (dry run D6e). Revision 1 observed the matching Docker failure on 2026-11-10 (`"/voice_narration": not found`); that is not re-run (UD-1).
- Pre-existing failures: none. `pytest --co` collects 75 tests at `HEAD`; no test is known to fail.

## Current Repository State

- `HEAD` `29d8a316bb1524713f658a7cd45c2ae472f82fd1`; `git status --short` empty.
- `cloudrun/chatterbox-service/Dockerfile` (committed SHA-256 `3f6bbce3…0a9f`): `:1` base image; `:9-10` installs `requirements-dev.txt`; `:12` `COPY voice_narration /app/voice_narration`; `:14-16` `CHATTERBOX_DEVICE=cpu`, `CHATTERBOX_MODEL_VARIANT=v3`, `PORT=8080`; `:20` uvicorn on 8080.
- `cloudrun/chatterbox-service/README.md` (committed SHA-256 `ad94c378…a8f`, 20 lines) — B1.
- `requirements-dev.txt:7-8,10` pin `numpy==2.5.4`, `av==19.0.2`, `chatterbox-tts==0.1.7`; only CPython 3.13 satisfies them with `torch==2.6.0` (revision 1 PyPI reading; D1, D2).
- `.dockerignore:1-4` (B3) is tracked and not git-ignored, so `gcloud builds submit` uploads it (`.gitignore` has no rule for it).
- `.gitignore:1,5,10-11,16,19` exclude `/.venv/`, `/.env`, `service-account-key.json`, `*-key.json`, `/audio_storage/`, `*.zip`; `.gitignore:6-7` exclude `__pycache__/`, `*.pyc`. The repository root holds the git-ignored `.env`, `service-account-key.json` and `Voice-Narration.zip` (158,841,906 bytes).
- `voice_narration/chatterbox_api/application.py:20-21` `DEVICE`, `MODEL_VARIANT` from the environment; `:43` `from_pretrained(device=DEVICE)`.
- `voice_narration/inference/application.py:28-29`, `:46` read the base URL and timeout at import; `:126-127` locate the key at call time.
- No test references `cloudrun/`, a Dockerfile or an ignore file (search of the repository outside `.venv` and `docs/.ai`: only `.dockerignore`, the README, `.github/workflows/harness.yml:32` and `docs/developer-setup.md:19,30`, all about the harness).

## Files in Scope

### Files to Create

- `cloudrun/chatterbox-service/Dockerfile.dockerignore`
- `cloudrun/chatterbox-service/cloudbuild.json`

### Files to Modify

- `cloudrun/chatterbox-service/Dockerfile` — line 1.
- `cloudrun/chatterbox-service/README.md` — whole file replaced.

### Files to Delete

None.

## Proposed Changes

1. `cloudrun/chatterbox-service/Dockerfile` — line 1 `FROM python:3.11-slim` becomes `FROM python:3.13.17-slim-trixie` (C6-D-2). Why: the image installs `requirements-dev.txt`, whose pins resolve only on CPython 3.13 (B5a, D1). Every other line is unchanged, including `ENV CHATTERBOX_DEVICE=cpu` (C6-D-9).
2. `cloudrun/chatterbox-service/Dockerfile.dockerignore` — new, five rules (C6-D-3): `*`; `!requirements-dev.txt`; `!voice_narration/`; `**/__pycache__`; `**/*.pyc`. Why: the root `.dockerignore` keeps `voice_narration` out of the context (B5b). Docker patterns are matched from the context root, so `requirements-dev.txt` and `voice_narration/` name only root-level paths.
3. `cloudrun/chatterbox-service/cloudbuild.json` — new Cloud Build configuration (C6-D-4, C6-D-14, C6-D-16, C6-D-17) with two steps and one image:
   1. step `use-chatterbox-ignore-file`: image `gcr.io/cloud-builders/docker`, entrypoint `cp`, args `cloudrun/chatterbox-service/Dockerfile.dockerignore` `.dockerignore` — in the Cloud Build workspace copy only;
   2. step `build-image`: image `gcr.io/cloud-builders/docker`, args `build --file cloudrun/chatterbox-service/Dockerfile --tag asia-southeast1-docker.pkg.dev/$PROJECT_ID/chatterbox/chatterbox-model-api:$_TAG .`;
   3. `images`: the same tag, so Cloud Build pushes it to Artifact Registry.
   Why: `gcloud builds submit --tag` runs `docker build -t $TAG .` with the root Dockerfile (reference page), and the Chatterbox Dockerfile is not at the root, so the Cloud Build route (UD-2) needs a configuration file. `$PROJECT_ID` is a built-in substitution; `_TAG` is user-defined and has no default, so a build without it fails (schema: missing substitution is an error).
4. `cloudrun/chatterbox-service/README.md` — replaced by the deployment document (C6-D-1). Sections in order: introduction (separate private service on L4; only voice cloning on Google Cloud; not performed by the repository — AGW-011, CCR-1, CCR-2, CCR-4, CCR-11); "Fixed values" (project, region, service, repository `chatterbox`, image, only caller — CCR-1, CCR-3, CCR-7); "Prerequisites" (`gcloud` with deploy rights, the virtual environment for the local inference service, the key stays local, no local Docker, PowerShell in one session, `gcloud config set project`, `gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com`, automatic L4 quota — C6-D-8, C6-D-12); "1. Build the image with Cloud Build" (`gcloud artifacts repositories create`, `$TAG = git rev-parse --short HEAD`, `gcloud builds submit . --config cloudrun/chatterbox-service/cloudbuild.json --substitutions "_TAG=$TAG"`, `$IMAGE`, clean working tree, what is uploaded and built, no weights in the image, permission-error note — C6-D-4, C6-D-15, C6-RSK-12); "2. Deploy the private service" (the `gcloud run deploy` command and table — C6-D-5 to C6-D-11; variant row per C8-RSK-1); "3. Allow only the service account to call it" (invoker binding, policy check, removal of `allUsers`/`allAuthenticatedUsers`, project-level roles — C6-D-10); "4. Get the service URL" (C5-RSK-1, C5-RSK-2); "5. Configure and start the local inference service" (three settings, process environment only, start command, cloning request contents, `"mode": "voice_cloning"`, `Voice cloning failed:` — CCD-5 to CCD-7, CCD-10, `Plan.md` RSK-8); "One request at a time" (CCD-9, CCD-11, `Plan.md` RSK-2); "Cold start and the time limit" (`Plan.md` RSK-3, RSK-4; C6-D-7); "Runtime endpoints" (carried from the baseline README with the multipart shape, CCD-1). Removed: `gcr.io/<PROJECT_ID>`, `--region <REGION>`, `--allow-unauthenticated`, `CHATTERBOX_DEVICE=cpu` deployment, `gcloud builds submit --tag … -f`.

### Decisions for review

- C6-D-1 — The document replaces `cloudrun/chatterbox-service/README.md` (`Plan.md` Non-Blocking Open Decisions); numbered steps in run order, then three explanatory sections. Alternative: a separate file — not chosen, the public instructions would remain.
- C6-D-2 — Base image `python:3.13.17-slim-trixie`: the project's runtime (`docs/developer-setup.md`) and the harness base (`containers/harness.Dockerfile:1`); Python 3.13 supported to 2029-10 (devguide). Alternatives: 3.12 (cannot install `numpy==2.5.4` with `chatterbox-tts` 0.1.7), 3.14 (pulls `torch>=2.9.0`, a different runtime), an NVIDIA CUDA base (not needed: Cloud Run preinstalls the driver and `torch` ships its CUDA libraries as packages), changing `requirements-dev.txt` (out of scope, `Plan.md` RSK-6).
- C6-D-3 — A Dockerfile-specific ignore file, not a change to the shared `.dockerignore`, so the harness and the excluded inference-service image keep their context. Alternative: add `!voice_narration/` to the root file — not chosen.
- C6-D-4 — Revised for UD-2: Cloud Build builds and pushes the image, configured by `cloudbuild.json`, to Artifact Registry repository `chatterbox` in `asia-southeast1`, tagged with the short commit hash passed as `_TAG`. Alternatives: local `docker build` and `docker push` (revision 1) — excluded by UD-1 and UD-2; `gcloud builds submit --tag` — needs the Dockerfile at the source root; `$SHORT_SHA` — populated only for trigger builds, not manual submits (hypothesis, not read this run; `_TAG` avoids depending on it); tag `latest` — does not identify the source.
- C6-D-5 to C6-D-13 — unchanged from revision 1: `--cpu 4 --memory 16Gi` (GPU minimum); `--concurrency 80` (requests wait on Chatterbox's lock instead of getting Cloud Run's `429`; alternatives `1`, omitted, `40`); `--timeout 600` (equals CCD-6's default; inference limit reached first; alternatives `660`, `3600`); `--no-gpu-zonal-redundancy` (automatic quota, no uptime requirement); GPU through `--set-env-vars CHATTERBOX_DEVICE=cuda`, image default stays `cpu` (RF-5); `--no-allow-unauthenticated` plus one service-level `roles/run.invoker` binding, invoker check left on, no `--service-account`; `--min-instances 0 --max-instances 1`; PowerShell only; service name `chatterbox-model-api`, port `8080`, `CHATTERBOX_MODEL_VARIANT=v3`.
- C6-D-14 — New. A first Cloud Build step copies `Dockerfile.dockerignore` over the uploaded `.dockerignore`, in the build workspace. Why: whether the `gcr.io/cloud-builders/docker` builder honours a Dockerfile-specific ignore file depends on BuildKit, which its README does not document; after the copy, every Docker builder reads the same five rules from the root ignore file. The repository's `.dockerignore` is not changed. Alternatives: rely on `Dockerfile.dockerignore` alone, or set `DOCKER_BUILDKIT=1` — not chosen, both depend on an undocumented builder version; if they failed, the build would stop at `COPY voice_narration` (no leak, but no image).
- C6-D-15 — New. The upload is filtered by gcloud's generated `.gitignore`-based ignore file; no `.gcloudignore` or `--ignore-file` is added. Why: `.gitignore` already excludes the key, `.env`, `.venv`, `audio_storage`, the zip and bytecode (Current Repository State); the remaining upload is 78 files (D6a); the image context is narrowed again by C6-D-14. Alternative: an allowlist `.gcloudignore` — not chosen: gcloudignore's handling of re-included paths inside excluded directories is not documented, and a root `.gcloudignore` would also change uploads of the excluded inference-service artifacts.
- C6-D-16 — New. The configuration is JSON (`cloudbuild.json`), which `--config` accepts ("YAML or JSON"). Why: it can be checked locally with the Python standard library (C6-V4); PyYAML is not installed in `.venv`. Alternative: `cloudbuild.yaml` — more common, but cannot be parsed locally without adding a package.
- C6-D-17 — New. No `timeout`, `options` or `--region` for the build: the default 60-minute timeout and default machine are kept, and the build runs in Cloud Build's global region. Why: no approved artifact sets them; the defaults are documented. Alternative: `"timeout": "3600s"` or a larger machine — not chosen; if the build exceeds 60 minutes, that is reported by the user's deployment (C6-RSK-12).

No dependency or application setting is introduced. The one version choice is C6-D-2. Every setting in `cloudbuild.json` and every `gcloud` flag in the document traces to a decision above or to a requirement.

## Proposed Code / Tests

### `cloudrun/chatterbox-service/Dockerfile` — unified diff against the committed file

```diff
--- a/cloudrun/chatterbox-service/Dockerfile
+++ b/cloudrun/chatterbox-service/Dockerfile
@@ -1,4 +1,4 @@
-FROM python:3.11-slim
+FROM python:3.13.17-slim-trixie
 
 ENV PYTHONDONTWRITEBYTECODE=1
 ENV PYTHONUNBUFFERED=1
```

### `cloudrun/chatterbox-service/Dockerfile` — complete final content (20 lines, LF, SHA-256 `9ce80691dc82b749ba5f7f39da648f0519f475ad1339930124e87ed5a523eeb8`)

```dockerfile
FROM python:3.13.17-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install --upgrade pip && pip install -r /app/requirements-dev.txt

COPY voice_narration /app/voice_narration

ENV CHATTERBOX_DEVICE=cpu
ENV CHATTERBOX_MODEL_VARIANT=v3
ENV PORT=8080

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "voice_narration.chatterbox_api.application:app", "--host", "0.0.0.0", "--port", "8080"]
```

### `cloudrun/chatterbox-service/Dockerfile.dockerignore` — complete content (5 lines, LF, SHA-256 `4ac6d36678cdaa14d904773305614bc57f3035cb7b6e1584c55f0eca98c2bfd7`)

```text
*
!requirements-dev.txt
!voice_narration/
**/__pycache__
**/*.pyc
```

### `cloudrun/chatterbox-service/cloudbuild.json` — complete content (28 lines, LF, SHA-256 `bf50c070d328eca7cd0654132d010b7afb7594f51a1a688efc07a9a9f056092d`)

```json
{
  "steps": [
    {
      "id": "use-chatterbox-ignore-file",
      "name": "gcr.io/cloud-builders/docker",
      "entrypoint": "cp",
      "args": [
        "cloudrun/chatterbox-service/Dockerfile.dockerignore",
        ".dockerignore"
      ]
    },
    {
      "id": "build-image",
      "name": "gcr.io/cloud-builders/docker",
      "args": [
        "build",
        "--file",
        "cloudrun/chatterbox-service/Dockerfile",
        "--tag",
        "asia-southeast1-docker.pkg.dev/$PROJECT_ID/chatterbox/chatterbox-model-api:$_TAG",
        "."
      ]
    }
  ],
  "images": [
    "asia-southeast1-docker.pkg.dev/$PROJECT_ID/chatterbox/chatterbox-model-api:$_TAG"
  ]
}
```

### `cloudrun/chatterbox-service/README.md` — complete final content (261 lines, LF, ASCII, SHA-256 `749ef6bcd17a658cecfed578f634bc70c9d06860a9047bd149b3a24a88802265`)

````markdown
# Chatterbox on Cloud Run (private, NVIDIA L4)

This document describes how to deploy the Chatterbox model API as a separate,
private Cloud Run service on an NVIDIA L4 GPU, and how to point the local
inference service at it. Only voice cloning runs on Google Cloud. The voices
service, the inference service, the frontend and Google TTS narration keep
running locally.

Following these steps is a manual task for an operator. Nothing in this
repository performs the deployment.

## Fixed values

| Item | Value |
| --- | --- |
| Project | `project-84eb579f-1f7b-4f87-838` |
| Region | `asia-southeast1` |
| Cloud Run service | `chatterbox-model-api` |
| Artifact Registry repository | `chatterbox` (Docker format, in `asia-southeast1`) |
| Image | `asia-southeast1-docker.pkg.dev/project-84eb579f-1f7b-4f87-838/chatterbox/chatterbox-model-api`, tagged with the short commit hash (step 1) |
| Only allowed caller | `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` |

## Prerequisites

- The Google Cloud CLI (`gcloud`), signed in with `gcloud auth login` as an
  account that may enable services, create Artifact Registry repositories,
  run Cloud Build builds, deploy Cloud Run services and change their IAM
  policy in the project (for example a project Owner).
- The repository's Python virtual environment, set up as described in
  `docs/developer-setup.md`, for the local inference service (step 5).
- The service-account key file of
  `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` on the
  local machine. It is the same key the local Google TTS narration uses. It is
  never copied into the image and never uploaded.

Docker is not needed on the local machine: Cloud Build builds the image in
Google Cloud.

Run every command below in PowerShell from the repository root, and run steps 1
to 5 in the same PowerShell session: later steps use the `$TAG`, `$IMAGE` and
`$CHATTERBOX_URL` variables that earlier steps set.

Set the project and enable the services once:

```powershell
gcloud config set project project-84eb579f-1f7b-4f87-838
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

GPU quota: on a project's first GPU deployment in a region, Cloud Run
automatically grants a quota of 3 L4 GPUs with zonal redundancy turned off.
This deployment uses at most one GPU instance with zonal redundancy turned off,
so it needs no quota request. If the deployment reports a GPU quota error,
request quota for "L4 GPU with zonal redundancy turned off" in
`asia-southeast1` from the Google Cloud console.

## 1. Build the image with Cloud Build

Create the Artifact Registry repository once:

```powershell
gcloud artifacts repositories create chatterbox `
  --repository-format=docker `
  --location=asia-southeast1
```

Build the image in Cloud Build and push it to the repository, tagged with the
current commit:

```powershell
$TAG = git rev-parse --short HEAD
gcloud builds submit . `
  --config cloudrun/chatterbox-service/cloudbuild.json `
  --substitutions "_TAG=$TAG"
$IMAGE = "asia-southeast1-docker.pkg.dev/project-84eb579f-1f7b-4f87-838/chatterbox/chatterbox-model-api:$TAG"
```

Build from a working tree with no uncommitted changes, so that the tag names
the source that was built.

What is uploaded and built:

- `gcloud builds submit` uploads the repository without the files that
  `.gitignore` lists, so local secrets such as `service-account-key.json` and
  `.env`, the virtual environment and local audio are not uploaded.
- In Cloud Build, `cloudrun/chatterbox-service/cloudbuild.json` first makes
  `cloudrun/chatterbox-service/Dockerfile.dockerignore` the build's ignore
  file, then builds `cloudrun/chatterbox-service/Dockerfile`. The image
  receives only `requirements-dev.txt` and the `voice_narration` package.
- The image holds no model weights; Chatterbox downloads them the first time
  it loads the model (see "Cold start and the time limit").
- The first build downloads PyTorch and its NVIDIA libraries and takes several
  minutes.

If the build stops with a permission error, the service account that runs
the build lacks a role. In new projects Cloud Build runs builds as the Compute
Engine default service account. Grant that account the Cloud Build Service
Account role (`roles/cloudbuild.builds.builder`), which includes uploading to
Artifact Registry and writing build logs, then run the build again.

## 2. Deploy the private service

```powershell
gcloud run deploy chatterbox-model-api `
  --image $IMAGE `
  --region asia-southeast1 `
  --no-allow-unauthenticated `
  --gpu 1 `
  --gpu-type nvidia-l4 `
  --no-gpu-zonal-redundancy `
  --cpu 4 `
  --memory 16Gi `
  --no-cpu-throttling `
  --min-instances 0 `
  --max-instances 1 `
  --concurrency 80 `
  --timeout 600 `
  --port 8080 `
  --set-env-vars CHATTERBOX_DEVICE=cuda,CHATTERBOX_MODEL_VARIANT=v3
```

What each setting does:

| Setting | Effect |
| --- | --- |
| `--region asia-southeast1` | Runs Chatterbox in Singapore. |
| `--no-allow-unauthenticated` | Makes the service private: Cloud Run answers `401` or `403` to any call without a valid identity token of an allowed caller. |
| `--gpu 1`, `--gpu-type nvidia-l4` | Attaches one NVIDIA L4 GPU. Cloud Run installs the GPU driver; the image needs none. |
| `--no-gpu-zonal-redundancy` | Uses the lower-priced GPU capacity that the automatic quota covers. |
| `--cpu 4`, `--memory 16Gi` | The smallest CPU and memory Cloud Run allows with one GPU. |
| `--no-cpu-throttling` | Instance-based billing, which Cloud Run GPU services need. The service still scales to zero. |
| `--min-instances 0` | Scales to zero when idle. |
| `--max-instances 1` | At most one instance runs. |
| `--concurrency 80` | Lets up to 80 requests reach the one instance at once. Chatterbox itself generates one clip at a time; the other requests wait inside Chatterbox for their turn (see "One request at a time"). |
| `--timeout 600` | Cloud Run allows each request up to 600 seconds (10 minutes), the same as the local inference service's default time limit. |
| `--port 8080` | The port the image serves on. |
| `CHATTERBOX_DEVICE=cuda` | Chatterbox runs the model on the GPU. The image's own default is `cpu`. |
| `CHATTERBOX_MODEL_VARIANT=v3` | The model variant that `GET /health` and `GET /v1/metadata` report, as before. It does not select the model weights. |

## 3. Allow only the service account to call it

Grant the Cloud Run Invoker role on this service to the service account:

```powershell
gcloud run services add-iam-policy-binding chatterbox-model-api `
  --region asia-southeast1 `
  --member "serviceAccount:test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com" `
  --role roles/run.invoker
```

Check the service's IAM policy:

```powershell
gcloud run services get-iam-policy chatterbox-model-api --region asia-southeast1
```

The `roles/run.invoker` binding must list only
`serviceAccount:test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`.
If it also lists `allUsers` or `allAuthenticatedUsers` (for example from an
earlier public deployment), remove that member:

```powershell
gcloud run services remove-iam-policy-binding chatterbox-model-api `
  --region asia-southeast1 `
  --member allUsers `
  --role roles/run.invoker
```

Use `--member allAuthenticatedUsers` in the same command for that member.

Principals that hold a project-level role that includes calling Cloud Run
services (for example `roles/owner`, or `roles/run.invoker` granted on the
whole project) can also call the service. To keep the service callable only by
the service account, grant no such project-level role to anyone else.

## 4. Get the service URL

```powershell
$CHATTERBOX_URL = gcloud run services describe chatterbox-model-api `
  --region asia-southeast1 `
  --format "value(status.url)"
$CHATTERBOX_URL
```

The URL starts with `https://` and has no trailing `/`. Use it exactly as
printed. The local inference service uses the same string both to call
Chatterbox and as the audience of the identity token, and Cloud Run rejects a
token whose audience differs from its URL, for example by a trailing `/`.

## 5. Configure and start the local inference service

The inference service reads these settings from its process environment once,
when it starts. A `.env` file does not set them. After a change, restart the
inference service.

| Setting | Value |
| --- | --- |
| `VOICE_CLONING_API_BASE_URL` | The service URL from step 4. When it is not set, `CHATTERBOX_API_BASE_URL` is used. |
| `VOICE_CLONING_TIMEOUT_SECONDS` | Optional. The time limit for one voice cloning request, a positive whole number of seconds. Default `600` (10 minutes). |
| `GOOGLE_APPLICATION_CREDENTIALS` | Optional. The path to the key file of `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`. When it is not set in the process environment, the inference service takes it from the repository-root `.env` file, and otherwise uses `service-account-key.json` at the repository root. |

```powershell
$env:VOICE_CLONING_API_BASE_URL = $CHATTERBOX_URL
$env:VOICE_CLONING_TIMEOUT_SECONDS = "600"
.\.venv\Scripts\python.exe -m voice_narration.inference
```

For every voice cloning request, the inference service sends the voice
sample audio with the request and attaches a Google identity token for the
service account, with the service URL as its audience. The generated audio is
saved by the local inference service; Chatterbox keeps neither the voice
sample nor the generated audio after it answers.

Voice cloning is used for a job created through `POST /inference/jobs` with
`"mode": "voice_cloning"` in its JSON body. The frontend sends no mode, so it
always uses Google TTS narration.

When cloning fails, the inference service answers `503` with a message that
starts with `Voice cloning failed:` and says why, for example that access was
denied (HTTP 401 or 403) or that the service did not respond within the time
limit.

## One request at a time

With `--max-instances 1` there is at most one Chatterbox instance. Chatterbox
generates one clip at a time; a request that arrives while another is being
generated waits inside Chatterbox and is then served. With `--concurrency 80`,
Cloud Run passes up to 80 requests to the instance at once. If more requests
are open at the same time, Cloud Run holds the extra ones briefly and then
answers `429`, which the inference service reports as an error of the voice
cloning service (HTTP 429). Waiting time counts toward the local inference
service's time limit. A retried request produces a new clip; there is no
duplicate detection.

## Cold start and the time limit

When the service has scaled to zero, the next request starts a new instance.
The first request on a new instance also downloads the model weights and loads
the model onto the GPU before it generates audio, and all of this counts toward
the request's time limit. The weights are written to the instance's in-memory
file system and use part of its 16 GiB memory.

If that first request does not finish within the time limit, the inference
service answers that the voice cloning service did not respond in time. The
instance keeps loading the model, so a retry a little later is served by the
loaded model while the instance is still running. Cloud Run may shut down an
idle instance at any time and keeps it idle for at most 15 minutes; the next
request after that starts cold again.

The Cloud Run request timeout (`--timeout`, at most 3600 seconds) must be at
least `VOICE_CLONING_TIMEOUT_SECONDS`. If you raise the local time limit, run
step 2 again with `--timeout` set to the same value.

## Runtime endpoints

- `GET /health`
- `GET /v1/metadata`
- `POST /v1/synthesize` (`multipart/form-data` with `text`, `language` and the
  file part `sample_audio`)

On Cloud Run every endpoint requires the service account's identity token.
````

### Verification tool (not a repository file) — `context_check.py`, written to the session scratchpad at execution (84 lines, LF, SHA-256 `408fc54f49526f8f58b766e3fe0bea16315ccd02bcf20db9f3d4bac9d90a6b2f`)

A model of Docker's ignore rules (moby pattern matcher: last matching rule wins; a rule that matches a parent directory applies to the files in it; `!` re-includes). It is a model, not Docker; Docker itself is not run (UD-1).

```python
"""List the files a Docker build context would receive, and flag secrets.

Reads file paths relative to the repository root, one per line, from stdin.
With a Docker ignore file as the only argument, applies its rules the way
Docker does (the last matching rule wins, a rule that matches a parent
directory also matches the files inside it, "!" re-includes). Without an
argument, applies no rules. Prints the remaining files, a summary line, and
one "LEAK" line per secret or local-only file; exits 1 when there is one.
"""

import re
import sys

LOCAL_ONLY = re.compile(
    r"(^|/)\.env(\.[^/]*)?$"
    r"|(^|/)[^/]*-key\.json$"
    r"|^(\.venv|\.git|audio_storage|\.pytest_cache|\.deepeval)/"
    r"|\.zip$"
)


def to_regex(pattern):
    out = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def load_rules(path):
    rules = []
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            negated = line.startswith("!")
            if negated:
                line = line[1:].strip()
            rules.append((negated, to_regex(line.strip("/"))))
    return rules


def is_excluded(path, rules):
    parts = path.split("/")
    candidates = ["/".join(parts[: i + 1]) for i in range(len(parts))]
    excluded = False
    for negated, regex in rules:
        if negated != excluded:
            continue
        if any(regex.match(candidate) for candidate in candidates):
            excluded = not negated
    return excluded


def main():
    rules = load_rules(sys.argv[1]) if len(sys.argv) > 1 else []
    paths = sorted({line.strip().replace("\\", "/") for line in sys.stdin if line.strip()})
    context = [path for path in paths if not is_excluded(path, rules)]
    leaks = [path for path in context if LOCAL_ONLY.search(path)]
    for path in context:
        print(path)
    print(f"input-files={len(paths)} context-files={len(context)} leaks={len(leaks)}")
    for path in leaks:
        print(f"LEAK {path}")
    return 1 if leaks else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Execution Steps

No Docker image is built, no container is started and no `gcloud` command is run in any step (UD-1, UD-2). Git Bash from the repository root, except C6-V7 (PowerShell). `$S` is a new directory in the session scratchpad.

1. Confirm this plan's Human Review records approval and that C6-Q-2 is resolved as `Plan.md` records.
2. Baseline before any change (C6-AC-1): `git rev-parse HEAD`; `git status --short` (expected empty); B1–B3 with `git show HEAD:cloudrun/chatterbox-service/README.md`, `git show HEAD:cloudrun/chatterbox-service/Dockerfile`, `git show HEAD:.dockerignore`; write `context_check.py` to `$S` from this plan and check its SHA-256; B5a C6-V5b; B5b `git ls-files -co --exclude-standard > "$S/upload-base.txt"; ./.venv/Scripts/python.exe -I "$S/context_check.py" .dockerignore < "$S/upload-base.txt"`; B4 C6-V7.
3. Write the four files from this plan's code blocks with LF endings: create `Dockerfile.dockerignore` and `cloudbuild.json`; overwrite `Dockerfile` and `README.md` under `cloudrun/chatterbox-service/`.
4. Run C6-V1 to C6-V8 in order, each output to a log in `$S`.
5. Report each command with its trimmed output; delete `$S` afterwards.

## Acceptance / Completion Criteria

Subject to C6-Q-2: these criteria match the completion evidence `Plan.md` revision 2 records except its local-build clause.

- C6-AC-1 — Baseline recorded before any change: B1–B3 quoted from `HEAD`; B4 `75 passed`; B5a 3.11 resolution fails on `numpy==2.5.4`; B5b the root `.dockerignore` context lists `containers/harness.Dockerfile` and `requirements-dev.txt` only.
- C6-AC-2 — The four files match this plan (C6-V1: `9ce80691…eeb8`, `4ac6d366…bfd7`, `bf50c070…092d`, `749ef6bc…2265`), and no other file changes: `git status --short` lists only ` M cloudrun/chatterbox-service/Dockerfile`, ` M cloudrun/chatterbox-service/README.md`, `?? cloudrun/chatterbox-service/Dockerfile.dockerignore`, `?? cloudrun/chatterbox-service/cloudbuild.json` and this Implementation Plan's Human Review update (excluding the milestone's Execution Status update in `Plan.md`).
- C6-AC-3 — The document covers every checklist item, shown by C6-V2 with line numbers:

  | Item | Source | Where |
  | --- | --- | --- |
  | Build the Chatterbox image | CRM-6 scope, UD-2 | step 1 (Cloud Build, `cloudbuild.json`) |
  | Separate Cloud Run service | AGW-011 | introduction; step 2 `chatterbox-model-api` |
  | Project | CCR-1 | Fixed values; `gcloud config set project` |
  | Region `asia-southeast1` | CCR-3 | Fixed values; step 2 `--region asia-southeast1` |
  | NVIDIA L4 GPU | CCR-4 | step 2 `--gpu 1`, `--gpu-type nvidia-l4` |
  | Private, only `test-850@…` | CCR-7 | step 2 `--no-allow-unauthenticated`; step 3 binding and check |
  | Scale to zero; at most 1 instance | Deployment | step 2 `--min-instances 0`, `--max-instances 1` |
  | One request at a time | Deployment (AC-CCR-8), Consistency and concurrency | step 2 `--concurrency 80` row; "One request at a time" |
  | Request time limit for 10 minutes | CCR-9 | step 2 `--timeout 600`; "Cold start and the time limit" |
  | Local inference configuration | contract Inference Service Settings | step 5 |
  | Deployment not performed by the repository | CCR-11 | introduction |

- C6-AC-4 — No instruction to deploy publicly remains: C6-V3 prints `public-flag-lines-exit=1`, and `allUsers` appears only on the policy-check sentence and the removal command.
- C6-AC-5 — `cloudbuild.json` is valid JSON with steps `use-chatterbox-ignore-file` then `build-image`, an `images` entry equal to the build tag, only the variables `PROJECT_ID` and `_TAG`, and both referenced files present (C6-V4).
- C6-AC-6 — The image's pinned dependencies resolve without installing for CPython 3.13 on manylinux x86_64 wheels only, with `numpy 2.5.4`, `torch 2.6.0`, `torchaudio 2.6.0`, `chatterbox-tts 0.1.7`, `av 19.0.2` (C6-V5a).
- C6-AC-7 — Build context and secrets, without an image build (C6-V6): the upload set under `.gitignore` rules has `leaks=0`; that set filtered by `Dockerfile.dockerignore` is exactly `requirements-dev.txt` and the 14 tracked `.py` files under `voice_narration/`, `leaks=0`; the whole working tree including ignored files (the real `.env`, `service-account-key.json`, `.venv`, `audio_storage`, the zip, bytecode) filtered by `Dockerfile.dockerignore` gives the same 15 files, `leaks=0`; and the checker, given the whole tree without rules, reports `LEAK .env` and `LEAK service-account-key.json` and exits 1.
- C6-AC-8 — The preserved tests pass: 75 collected, 75 passed, no `FAILED` or `ERROR` line (C6-V7). They are the full suite `Plan.md` names: the four tests of `tests/test_clone_flow.py` and `tests/test_ai_gateway_telemetry_red.py` (as updated by CRM-4), the five in `tests/test_ai_gateway_red.py`, the 17 in `tests/test_chatterbox_service_red.py` (CRM-2, aligned and added by CRM-7) and the 49 cases in `tests/test_inference_client_red.py` (CRM-4).
- C6-AC-9 — No service behavior changes: C6-V8's scoped `git status` prints nothing for `voice_narration`, `tests`, `requirements-dev.txt`, `pytest.ini`, `.dockerignore`, `.gitignore`, `containers`, `cloudrun/inference-service`, `frontend`.

## Verification

### Commands

- C6-V1 — `sha256sum cloudrun/chatterbox-service/Dockerfile cloudrun/chatterbox-service/Dockerfile.dockerignore cloudrun/chatterbox-service/cloudbuild.json cloudrun/chatterbox-service/README.md`
- C6-V2 — checklist:

  ```bash
  grep -nE -- '^## |project-84eb579f-1f7b-4f87-838$|cloudbuild.json|--region asia-southeast1|--gpu 1|--gpu-type nvidia-l4|--no-allow-unauthenticated|--min-instances 0|--max-instances 1|--concurrency 80|--timeout 600|roles/run.invoker|VOICE_CLONING_API_BASE_URL = |VOICE_CLONING_TIMEOUT_SECONDS = |GOOGLE_APPLICATION_CREDENTIALS` \||performs the deployment' cloudrun/chatterbox-service/README.md
  ```

- C6-V3 — no public deployment instruction:

  ```bash
  grep -rn -- 'allow-unauthenticated' cloudrun/chatterbox-service | grep -v -- '--no-allow-unauthenticated'; echo "public-flag-lines-exit=$?"
  grep -n 'allUsers' cloudrun/chatterbox-service/README.md
  ```

- C6-V4 — Cloud Build configuration structure:

  ```bash
  ./.venv/Scripts/python.exe -I - <<'EOF'
  import json, os, re
  with open("cloudrun/chatterbox-service/cloudbuild.json", encoding="utf-8") as handle:
      config = json.load(handle)
  copy_step, build_step = config["steps"]
  args = build_step["args"]
  tag = args[args.index("--tag") + 1]
  print("top-level keys", sorted(config))
  print("step ids", [step["id"] for step in config["steps"]])
  print("copy", copy_step["entrypoint"], copy_step["args"])
  print("build file", args[args.index("--file") + 1], "context", args[-1])
  print("image", tag)
  print("images equal build tag", config["images"] == [tag])
  print("variables", sorted(set(re.findall(r"\$(_?[A-Z][A-Z_]*)", json.dumps(config)))))
  print("referenced files exist", all(os.path.isfile(path) for path in (copy_step["args"][0], args[args.index("--file") + 1])))
  EOF
  ```

- C6-V5 — pip resolution, nothing installed (each takes about two minutes and needs PyPI):

  ```bash
  ./.venv/Scripts/python.exe -m pip install --dry-run --ignore-installed --quiet --report "$S/r313.json" --python-version 3.13 --implementation cp --abi cp313 --platform manylinux_2_28_x86_64 --platform manylinux2014_x86_64 --platform manylinux1_x86_64 --only-binary=:all: -r requirements-dev.txt; echo "resolve-313-exit=$?"
  ./.venv/Scripts/python.exe -I -c "import json,sys; m={i['metadata']['name'].lower(): i['metadata']['version'] for i in json.load(open(sys.argv[1], encoding='utf-8'))['install']}; print(len(m), 'packages'); print(' | '.join(k + ' ' + str(m.get(k)) for k in ['numpy', 'torch', 'torchaudio', 'chatterbox-tts', 'av', 'fastapi', 'starlette', 'anyio']))" "$S/r313.json"
  ```

  C6-V5b (baseline B5a only): the first command with `3.11`, `cp311` and `$S/r311.json`, printing `resolve-311-exit=$?`.

- C6-V6 — build context and secret exclusion, no image built:

  ```bash
  git ls-files -co --exclude-standard > "$S/upload.txt"
  { git ls-files -co; git ls-files -o -i --exclude-standard; } > "$S/all.txt"
  ./.venv/Scripts/python.exe -I "$S/context_check.py" < "$S/upload.txt" | tail -1; echo "upload-exit=${PIPESTATUS[0]}"
  ./.venv/Scripts/python.exe -I "$S/context_check.py" cloudrun/chatterbox-service/Dockerfile.dockerignore < "$S/upload.txt"; echo "context-exit=$?"
  ./.venv/Scripts/python.exe -I "$S/context_check.py" cloudrun/chatterbox-service/Dockerfile.dockerignore < "$S/all.txt" | tail -1; echo "tree-exit=${PIPESTATUS[0]}"
  ./.venv/Scripts/python.exe -I "$S/context_check.py" < "$S/all.txt" | grep -E '^(input|LEAK (\.env|service-account-key\.json)$)'; echo "selftest-exit=${PIPESTATUS[0]}"
  ```

- C6-V7 — full suite (PowerShell, `Plan.md` Verification Commands): `.\.venv\Scripts\python.exe -m pytest tests -ra`
- C6-V8 — scope:

  ```bash
  git status --short
  git status --short -- voice_narration tests requirements-dev.txt pytest.ini .dockerignore .gitignore containers cloudrun/inference-service frontend
  git diff --stat
  ```

### Affected Tests

None. No file under `voice_narration/` or `tests/` changes, and no test references `cloudrun/`, a Dockerfile, an ignore file or the Cloud Build configuration (repository search, Current Repository State). The full suite runs once as the preserved-test check (C6-AC-8).

### Expected Evidence

Expected / Predicted — Not Yet Verified. Each item becomes evidence only when the command has been run at execution and its output supports it.

- C6-V1: the four hashes of C6-AC-2.
- C6-V2: the eleven `## ` headings, line 10 (`repository performs the deployment.`), line 46 (`gcloud config set project …`), lines 73 and 86 (`cloudbuild.json`), lines 106–117 (deploy flags), 126–135 (their rows), 146–172 (step 3), 200 (`GOOGLE_APPLICATION_CREDENTIALS` row), 203–204 (`$env:` lines), 225–227 ("One request at a time").
- C6-V3: `public-flag-lines-exit=1`; `allUsers` on lines 159 and 165 only.
- C6-V4: `top-level keys ['images', 'steps']`; `step ids ['use-chatterbox-ignore-file', 'build-image']`; `images equal build tag True`; `variables ['PROJECT_ID', '_TAG']`; `referenced files exist True`.
- C6-V5: `resolve-313-exit=0`; `125 packages`; `numpy 2.5.4 | torch 2.6.0 | torchaudio 2.6.0 | chatterbox-tts 0.1.7 | av 19.0.2 | fastapi 0.162.0 | starlette 0.52.1 | anyio 4.16.0`. B5a: `resolve-311-exit=1` with `No matching distribution found for numpy==2.5.4`.
- C6-V6: `input-files=78 context-files=78 leaks=0`, `upload-exit=0`; the 15 files of C6-AC-7 then `input-files=78 context-files=15 leaks=0`, `context-exit=0`; `context-files=15 leaks=0`, `tree-exit=0` (input count about 11,900, mostly `.venv`); `LEAK .env`, `LEAK service-account-key.json`, `selftest-exit=1`. B5b: `containers/harness.Dockerfile`, `requirements-dev.txt`, `context-files=2`.
- C6-V7: `collected 75 items`, `75 passed, 1 warning` (the existing `StarletteDeprecationWarning`), no `FAILED` or `ERROR` line.
- C6-V8: the entries of C6-AC-2; the scoped status prints nothing; `git diff --stat` lists only `Dockerfile` and `README.md` under `cloudrun/chatterbox-service/`.

### Planning-Time Dry Run

Planning-time dry run — not milestone evidence. 2026-11-11, at `29d8a31`. Disposable clone `git clone -q --no-hardlinks <repo> $S/copy` in the session scratchpad, with the four proposed files written from this plan's content and dummy files planted (`.env`, `service-account-key.json`, `other-key.json`, `audio_storage/a.wav`, `.venv/f`, `voice_narration/__pycache__/a.cpython-313.pyc`, `voice_narration/stray.pyc`). Interpreter: the repository's `.venv` (read-only use). No Docker and no `gcloud` command was run (UD-1, UD-2).

| Step | Command | Result |
| --- | --- | --- |
| D1 | C6-V5 for 3.13 (run from the repository, read-only) | exit 0 in 2 min 19 s; `125 packages`; `numpy 2.5.4 \| torch 2.6.0 \| torchaudio 2.6.0 \| chatterbox-tts 0.1.7 \| fastapi 0.162.0 \| starlette 0.52.1 \| anyio 4.16.0 \| av 19.0.2`; `nvidia-cuda-runtime-cu12 None` (C6-RSK-13) |
| D2 | C6-V5b for 3.11 | exit 1; `ERROR: Could not find a version that satisfies the requirement numpy==2.5.4 (from versions: … 2.4.6)`; `ERROR: No matching distribution found for numpy==2.5.4` |
| D3 | C6-V1 and the diff | `9ce80691…eeb8`, `4ac6d366…bfd7`, `bf50c070…092d`, `749ef6bc…2265`; README 261 lines; 0 CR bytes and 0 non-ASCII bytes in the four files; `diff -u` from `git show HEAD:…/Dockerfile` equals this plan's diff |
| D4 | C6-V2 | headings and lines as listed under Expected Evidence |
| D5 | C6-V3 | `public-flag-lines-exit=1`; `159:If it also lists \`allUsers\` …`, `165:  --member allUsers \`` |
| D6 | C6-V4 | `top-level keys ['images', 'steps']`; `step ids ['use-chatterbox-ignore-file', 'build-image']`; `copy cp ['cloudrun/chatterbox-service/Dockerfile.dockerignore', '.dockerignore']`; `build file cloudrun/chatterbox-service/Dockerfile context .`; `images equal build tag True`; `variables ['PROJECT_ID', '_TAG']`; `referenced files exist True` |
| D6a | C6-V6 upload set | `input-files=78 context-files=78 leaks=0`, exit 0 |
| D6b | C6-V6 upload set + `Dockerfile.dockerignore` | the 15 files (`requirements-dev.txt`, 14 `voice_narration/**/*.py`), `input-files=78 context-files=15 leaks=0`, exit 0 |
| D6c | C6-V6 whole clone tree incl. ignored + `Dockerfile.dockerignore` | `input-files=85 context-files=15 leaks=0`, exit 0 (planted bytecode excluded) |
| D6d | C6-V6 self-test | `leaks=5`: `.env`, `.venv/f`, `audio_storage/a.wav`, `other-key.json`, `service-account-key.json`; exit 1 |
| D6e | B5b in the clone (root `.dockerignore` over the upload set) | `containers/harness.Dockerfile`, `requirements-dev.txt`, `context-files=2`, exit 0 |
| D7 | `context_check.py` over the real working tree with the proposed ignore file (read-only; the new files not yet present) | `input-files=11892 context-files=15 leaks=0`; without rules it reports `LEAK .env` and `LEAK service-account-key.json` |

Not run: C6-V7 (the full suite runs once, at execution only; no test or code file changes); C6-V8 (depends on the repository state after execution). Created and deleted afterwards: `$S/copy`, `$S/ex` (extracted files and `context_check.py`), `$S/r313.json`, `$S/r311.json`, their logs, `$S/upload.txt`, `$S/all.txt`, `$S/Dockerfile.orig`. The scratchpad folder also holds `base`, `prop`, `suite` and build logs dated 2026-11-10 and 2026-11-11 that this run did not create; they were left in place. Nothing was written to the repository except this Implementation Plan.

## Risks

- C6-RSK-1 — Identity comparisons (`security`). No comparison in code; the document configures the two Cloud Run makes, each in the canonical form the inference service authenticates with (C5-RSK-1): (a) token audience against the service URL — the inference service uses the configured base URL with only surrounding whitespace removed (`voice_narration/inference/application.py:28-29`) as call target and audience; step 4 takes `status.url` (no trailing `/`) and says to use it exactly; a mismatch is CFR-7; (b) caller against the invoker binding — the token is for the key's `client_email` (C5-D-1); the binding names `serviceAccount:test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` exactly as CCR-7 gives it, lowercase as Google issues it. Principals with project-level invoke rights can also call; the document says so. No user identity, role or ownership comparison exists.
- C6-RSK-2 — Image build, deployment and real model load first proven by the user's manual deployment (UD-1, UD-2). Not observed here: the Cloud Build run, the image's installed packages, imports and in-image tests (revision 1's C6-V6, dropped), GPU attachment, `torch 2.6.0`'s CUDA 12.4 libraries on the preinstalled driver (hypothesis), the invoker check, the real `from_pretrained(device="cuda")` load and 16 GiB being enough for 2.99 GiB weights plus the model (hypothesis). Performing the deployment is excluded (CCR-11); failures found by the user's deployment return to planning.
- C6-RSK-3 — Starlette in the image differs from `.venv`: pip resolves `starlette 0.52.1` (D1; through `gradio`), while `.venv` has `starlette 1.10.0`. Revision 1's dry run passed the 13 CRM-2 tests on `starlette 0.52.1` in a scratch environment (2026-11-10); the 4 CRM-7 tests were not run on it. Not re-run (UD-3 keeps only the listed checks). Hypothesis: they pass, because CRM-8 changed only the loader argument.
- C6-RSK-4 — Cold start inside the time limit (`Plan.md` RSK-4): if instance start, weights download and model load exceed 600 s, the first request answers CFR-5; a cold start that cannot fit at all is a replanning question.
- C6-RSK-5 — Waiting requests occupy thread-pool workers (C3-RSK-3); anyio 4.16.0 (D1) has a default limit of 40, so beyond 40 open requests a request first waits for a worker, and `GET /health` may wait under such load.
- C6-RSK-6 — No `--service-account` for the revision; it runs as Cloud Run's default runtime identity. Chatterbox calls no Google API. No approved artifact names a runtime identity.
- C6-RSK-7 — Image size and contents: all of `requirements-dev.txt` (including `pytest`, `playwright`, `psycopg`) plus `torch`; size not measured; dependency declarations are out of scope (`Plan.md` RSK-6). `pip install --upgrade pip` takes whatever pip is current.
- C6-RSK-8 — Mutable base tag `python:3.13.17-slim-trixie` (revision 1 resolved it to `sha256:d98cc29d…0962`).
- C6-RSK-9 — Network-dependent preserved test `test_generation_uses_selected_voice_profile` (C5-RSK-6). If it fails for network or credential reasons, C6-AC-8 is not met; execution stops. No rerun-until-pass.
- C6-RSK-10 — C6-V5 needs PyPI. If resolution fails for a network reason, C6-AC-6 is not met; execution stops and reports it.
- C6-RSK-11 — The upload filter is gcloud's: C6-V6 models the upload with Git's own `.gitignore` matching (`git ls-files --exclude-standard`), on the documented basis that the generated file "respects your .gitignored files". Whether gcloud's matcher gives exactly the same set is a hypothesis; secrets are kept out of the image by a second layer either way (C6-AC-7 whole-tree check). The upload goes to the project's Cloud Build source bucket.
- C6-RSK-12 — Cloud Build environment not exercised: `cp` in `gcr.io/cloud-builders/docker` (hypothesis: the image provides it), the default 60-minute timeout being enough for the PyTorch install and push, the default disk holding the image, and the build service account's permissions (the document's note cites `roles/cloudbuild.builds.builder`). Found only by the user's build; a failure returns to planning.
- C6-RSK-13 — C6-V5 resolves with `--platform` and the Python version for Linux, but pip evaluates environment markers for the running Windows interpreter, so Linux-only dependencies such as `torch`'s `nvidia-*` packages are not in the resolved set (D1: 125 packages; revision 1's in-container resolution on 2026-11-10 had 138, including `nvidia-cuda-runtime-cu12 12.4.127` and `nvidia-cudnn-cu12 9.1.0.70`). C6-V5 proves the pins resolve together on CPython 3.13 wheels; it does not prove the exact Linux set.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

- `git restore -- cloudrun/chatterbox-service/Dockerfile cloudrun/chatterbox-service/README.md`.
- Delete `cloudrun/chatterbox-service/Dockerfile.dockerignore` and `cloudrun/chatterbox-service/cloudbuild.json`; they exist only because of this milestone.
- Delete the session scratchpad directory `$S`. No Docker or cloud object is created.
- No repository-wide reset, clean or checkout.

## Explicitly Out of Scope

- Performing the deployment, running any `gcloud` command, building any Docker image or starting any container (CCR-11; UD-1, UD-2).
- The end-to-end cloning test from the local inference service against the user's deployed URL (UD-2): after this milestone, not one of its criteria; it needs its own authorization when the URL is shared.
- Any service behavior change: no file under `voice_narration/` or `tests/`; the image default device stays `cpu`.
- The shared `.dockerignore`, `.gitignore`, a `.gcloudignore`, `containers/harness.Dockerfile`, `requirements-dev.txt`, `pytest.ini` and dependency declarations.
- The inference-service Cloud Run artifacts (`cloudrun/inference-service/`); moving other services or narration to Google Cloud.
- A Cloud Build trigger, Terraform or other deployment automation beyond `cloudbuild.json`.
- Custom logging, metrics or alerts; duplicate detection; user login or authentication.
- Editing `docs/developer-setup.md` or other documentation.
- Docker objects on this machine, including the `scribe-*` containers of another project.

## Changes from Revision 1

- C6-Q-1 resolved (Plan revision 2; CRM-7, CRM-8 Complete); predecessor CRM-5 replaced by CRM-8 (`29d8a31`); full suite 71 → 75; preserved tests include CRM-7's.
- UD-1 to UD-3 recorded; new C6-Q-2.
- C6-D-4 revised (Cloud Build instead of local build and push); new C6-D-14 to C6-D-17; new file `cloudbuild.json`; README step 1 rewritten for Cloud Build, steps renumbered 1–5 (old 1 and 2 merged), Docker removed from prerequisites, `cloudbuild.googleapis.com` enabled, variant row per C8-RSK-1; README SHA-256 now `749ef6bc…2265`.
- Verification: removed the local image build, in-image checks, harness build and `gcloud` flag check (old C6-V4 to C6-V7, C6-V9); added C6-V4 (config structure), C6-V5 (pip resolution), C6-V6 (context and secret model); B5 now shown without Docker. C6-AC-5 to C6-AC-8 redefined accordingly.
- Risks: C6-RSK-2, -3, -10, -11 rewritten; C6-RSK-12, -13 added; revision 1's C6-RSK-3 (model loading) closed by CRM-8.
- Added Review Summary and Affected Tests sections (template).

## Human Review

Status: Executed — see Plan.md ("CRM-6 Execution Evidence"). Approved by avinash2196 on 2026-11-11 ("Approve both"), with Plan.md revision 3.
