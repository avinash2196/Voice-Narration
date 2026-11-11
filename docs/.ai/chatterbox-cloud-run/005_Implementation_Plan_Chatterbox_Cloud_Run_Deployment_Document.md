# Implementation Plan — CRM-6 Chatterbox Cloud Run Deployment Document

## Milestone

CRM-6 — Chatterbox Cloud Run Deployment Document, work item `chatterbox-cloud-run` (`docs/.ai/chatterbox-cloud-run/Plan.md`, section "CRM-6 — Chatterbox Cloud Run Deployment Document").

Purpose as recorded in `Plan.md`: "A how-to for deploying Chatterbox privately to Cloud Run as the requirements specify, and for configuring the local inference service to call it." Scope: a deployment document "that describes how to: build the Chatterbox image; deploy it as a separate Cloud Run service (AGW-011) in project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, on an NVIDIA L4 GPU (CCR-1, CCR-3, CCR-4); make it private, callable only by `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` (CCR-7); let it scale to zero with at most 1 instance and one request at a time (Deployment, Consistency and concurrency); set a Cloud Run request time limit that accommodates the 10-minute cloning limit (CCR-9); and configure the local inference service with the settings the contract defines. Changes to the existing Chatterbox container build and deployment artifacts are included only where the documented steps cannot otherwise satisfy these items." Owned: CCR-1; CCR-3; CCR-4; CCR-11; Deployment characteristic (scale to zero, at most 1 instance).

## Milestone Type

OTHER — as recorded in `Plan.md` ("Milestone type: OTHER") and in its Execution Status row "CRM-6 — Chatterbox Cloud Run Deployment Document (OTHER) | Pending".

`Plan.md` records why no owned requirement changes behavior: "the document and any container build or deployment artifact change alter no service's request handling, validation, failure answers or data handling; selecting the GPU device uses the existing device setting (RF-5). All behavior changes are delivered by CRM-3 and CRM-5." This plan keeps to that: it changes one documentation file and the Chatterbox image's build inputs (base image and build-context file list), and no file under `voice_narration/` or `tests/`. The GPU device is selected at deployment through the existing `CHATTERBOX_DEVICE` setting; the image's default stays `cpu`.

Baseline evidence and preserved tests are recorded under Preconditions / Predecessor Evidence and Acceptance / Completion Criteria.

## Question for Review Before Approval

C6-Q-1 — The deployed Chatterbox cannot load its model, so a deployment that follows this document cannot clone voices. This needs the user's decision before this plan is approved.

Evidence:

- The application loads the model with `ChatterboxMultilingualTTS.from_pretrained(device=DEVICE, t3_model=MODEL_VARIANT)` (`voice_narration/chatterbox_api/application.py:43`). The call has been there since commit `6d56d1e` (`git log -S t3_model`), before this work item. CRM-3 kept it as the baseline's own call (C2-D-1, C3-RSK-1).
- `requirements-dev.txt:10` pins `chatterbox-tts==0.1.7`. In that release the method is `def from_pretrained(cls, device: torch.device)` (`chatterbox/mtl_tts.py:201-202`), with no `t3_model` parameter and no `**kwargs`. The same signature is in `0.1.4`, `0.1.5` and `0.1.6` (Planning-Time Dry Run, step 6).
- Consequence, derived from the code and not observed at runtime, because the model runtime was not run: Python raises `TypeError` for the unexpected keyword. `_get_model()` runs before the generation `try` (`application.py:52-53` against `:58-61`), so `POST /v1/synthesize` answers `500` (contract failure 7), and `GET /v1/metadata` answers `500` too (`:140`). The inference service then answers every voice cloning job with CFR-8, `HTTP 500`. `GET /health` is not affected.
- Why no test caught it: the CRM-2 stand-in is `from_pretrained(cls, device, **kwargs)` (`tests/test_chatterbox_service_red.py:104`), which accepts any keyword.

Impact on this milestone: CRM-6's own completion evidence can still be produced (document, build, preserved tests). But AC-CCR-1, "Voice cloning requests from the local inference service are served by Chatterbox on Cloud Run ... when deployed as documented", cannot hold until the call changes. Changing it changes production behavior (`500` becomes a generated clip), so it cannot be done in this OTHER milestone (`implementation-planning` OTHER: "if a production behavior change turns out to be needed, stop and return to planning for RED and GREEN").

Options for the user (this plan does not choose):

1. Revise `Plan.md` (`create-plan` revision mode) to add a RED milestone and a GREEN milestone for Chatterbox model loading before CRM-6. Then review this plan again; its content is not expected to change, apart from this question and C6-RSK-3.
2. Approve CRM-6 as planned, and record the defect as a known finding. The document stays as written, Final Review records AC-CCR-1 as not demonstrated, and the fix is left for later work.
3. Another direction the user names.

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 (its Status section) |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Approved by avinash2196 on 2026-11-09 (its Status section). Execution Status: CRM-1 to CRM-5 Complete, CRM-6 Pending |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (accepts CCD-1–CCD-7). Authoritative predecessor delivered by CRM-1; the `Plan.md` CRM-1 row is Complete and points to it |
| `docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md` (revision 2) | Human Review: revision 2 approved by avinash2196 on 2026-11-09; executed, RED established |
| `docs/.ai/chatterbox-cloud-run/002_Implementation_Plan_Chatterbox_Service_GREEN.md` | Human Review: approved by avinash2196 on 2026-11-09; executed, GREEN verified. Source of carried-forward decisions |
| `docs/.ai/chatterbox-cloud-run/003_Implementation_Plan_Inference_Client_RED.md` | Human Review: approved by avinash2196 on 2026-11-09; executed, RED established |
| `docs/.ai/chatterbox-cloud-run/004_Implementation_Plan_Inference_Client_GREEN.md` | Human Review: approved by avinash2196 on 2026-11-10; executed, GREEN verified. Direct predecessor; source of carried-forward decisions |
| `docs/requirements.md` (product level) | Absent — `docs/` holds only `.ai/` and `developer-setup.md` |
| `docs/.ai/ai-gateway-multimodel/requirements.md` AGW-011 | Not re-read; quoted by the approved requirements ("Chatterbox must run as a separate self-hosted Cloud Run service exposing an API consumed by the AI Gateway") |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Not re-read; unchanged constraint (approved 2026-11-08). This milestone changes no gateway code or contract |
| `docs/developer-setup.md` | Repository documentation, not a PDD artifact. Source of the Python runtime (CPython 3.13.17), the harness commands and the verification commands named in `Plan.md` |
| Plugin skills read: `implementation-planning`, `prompt-driven-development` (with `templates/Implementation-Plan.md`), `security` | Plugin guidance, not project artifacts |

`security` is applied because the document configures private access (CCR-7) and handles a service-account key. CCR-7 is owned by CRM-5 and verified by CRM-4; this OTHER milestone documents the Cloud Run side. The identity comparisons are listed in Risks (C6-RSK-1).

External sources read on 2026-11-10 for platform and version facts (cited where used):

| Source | Used for |
| --- | --- |
| `https://docs.cloud.google.com/run/docs/configuring/services/gpu` | L4 regions include `asia-southeast1`; minimum 4 CPU and 16 GiB with one L4; instance-based billing required; automatic quota of 3 L4 GPUs with zonal redundancy off on the first deployment in a region; max instances must stay below the quota; driver "580.x.x (13.0)" preinstalled; `GPU_TYPE` `nvidia-l4` |
| `https://docs.cloud.google.com/run/docs/about-instance-autoscaling` | Requests beyond capacity pend for "up to 3.5 times average startup time ... or 10 seconds", then "fail with a `429` error code" |
| `https://docs.cloud.google.com/run/docs/about-concurrency` | Concurrency maximum 1,000; console default 80 |
| `https://docs.cloud.google.com/run/docs/configuring/request-timeout` | Default timeout 300 s, maximum 3600 s; a request over the timeout gets `504` |
| `https://docs.cloud.google.com/run/docs/container-contract` | In-memory file system ("writing to it uses the instance's memory"); an idle instance "won't be kept idle for longer than 15 minutes" and "can be shut down at any time" |
| `https://docs.cloud.google.com/run/docs/authenticating/service-to-service` | Token `aud` must be the receiving service's URL; caller needs `roles/run.invoker`; `gcloud run services add-iam-policy-binding` form |
| `https://docs.cloud.google.com/run/docs/deploying` | "Google recommends the use of Artifact Registry"; `--no-allow-unauthenticated` disallows public access |
| `https://docs.cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling` | `gcloud auth configure-docker LOCATION-docker.pkg.dev`; image name `LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG`; `docker tag`, `docker push` |
| `https://docs.docker.com/build/concepts/context/` | Dockerfile-specific ignore file: same directory as the Dockerfile, named after it, "takes precedence over the `.dockerignore` file"; `**` and `!` rules |
| `https://devguide.python.org/versions/` | Python 3.13: status "security", end of life 2029-10 |
| `https://pypi.org/pypi/numpy/2.5.4/json`, `https://pypi.org/pypi/av/19.0.2/json`, `https://pypi.org/pypi/chatterbox-tts/0.1.7/json` | `numpy 2.5.4` and `av 19.0.2` require Python `>=3.12`; `chatterbox-tts 0.1.7` requires `numpy<2.0.0` below Python 3.13 and `numpy>=2.0.0` from 3.13, `torch==2.6.0` below 3.14 |
| `chatterbox-tts` 0.1.4–0.1.7 wheels from PyPI (read as zip files, not installed) | `ChatterboxMultilingualTTS.from_pretrained(cls, device)` signature and its `snapshot_download` of six files (C6-Q-1, C6-RSK-3) |
| `https://huggingface.co/api/models/ResembleAI/chatterbox/tree/main` | Sizes of the six files the loader downloads (2.99 GiB in total) |
| Installed Google Cloud SDK 564.0.0, `gcloud <command> --help` | Every `gcloud` flag the document uses (C6-V4) |

## Carried-Forward Decisions

From the approved contract (`API-Contract.md`), which this document describes and does not change:

- CCD-4 — the caller identity is a Google-signed identity token for `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` with audience = the base URL in effect; Cloud Run enforces it with `401` or `403`; the application performs no identity check. The contract's Out of Scope assigns "the Cloud Run deployment settings themselves (GPU, region, instance counts, per-instance request limit, platform request time limit)" to "the deployment document of CRM-6".
- CCD-6 — `VOICE_CLONING_TIMEOUT_SECONDS`, a positive whole number of seconds, default `600`, read at service start.
- CCD-7 — `VOICE_CLONING_API_BASE_URL` with fallback `CHATTERBOX_API_BASE_URL` (carried over, RF-9), also the token audience; the key file named by `GOOGLE_APPLICATION_CREDENTIALS`, located as the narration provider locates it (process environment, then the repository-root `.env`, then `service-account-key.json`).
- CCD-9, CCD-10, CCD-11 — one generation at a time with others waiting; no retention; every retry produces a new clip.

From `002_Implementation_Plan_Chatterbox_Service_GREEN.md` (approved 2026-11-09):

- C3-D-3 — one-at-a-time serving uses a module `threading.Lock` held in a thread-pool worker; waiting requests wait on the lock and are never rejected by Chatterbox. Its C3-RSK-3 records that waiting requests occupy worker threads and that "`Plan.md` RSK-2 records that CRM-6 documents instance and per-instance request settings consistent with one-at-a-time serving". This plan does so in C6-D-6.

From `004_Implementation_Plan_Inference_Client_GREEN.md` (approved 2026-11-10):

- C5-RSK-1 — the base URL is used unchanged (surrounding whitespace removed only) both to call Chatterbox and as the token audience; "A configured URL that differs from it, for example by a trailing `/`, is rejected there and answered as CFR-7. That is deployment behavior, documented by CRM-6." The document's step 5 states it.
- C5-RSK-2 — "The documented Cloud Run service URL is `https://` (CRM-6 scope)." The document's step 5 states it.
- C5-D-2 and C4-D-6 — the key file is located at call time, while `VOICE_CLONING_API_BASE_URL` and `VOICE_CLONING_TIMEOUT_SECONDS` are read at import (`voice_narration/inference/application.py:28-29`, `:46`; `_load_local_env()` runs only inside `_voice_cloning_identity_token`, `:126`, and in `GoogleVoiceProvider.__init__`, `providers/google.py:40`). The document therefore tells the operator to set those two in the process environment, and says a `.env` file does not set them.

Conventions carried from the executions of CRM-3 to CRM-5 (`Plan.md` evidence): files are written with LF line endings (Git then warns `LF will be replaced by CRLF`, since `core.autocrlf` is `true`); the planning-time dry run runs the suite in a disposable `tar` copy that includes the git-ignored `.env` and `service-account-key.json`, which the preserved narration test needs.

Repository facts carried from the baseline artifacts (not decisions of an earlier Implementation Plan): service name `chatterbox-model-api` (`cloudrun/chatterbox-service/README.md:7`), port `8080` (`Dockerfile:16-20`), `CHATTERBOX_MODEL_VARIANT=v3` (`Dockerfile:15`, `README.md:13`), local inference entry point `python -m voice_narration.inference` on port 8003 (`voice_narration/inference/__main__.py`), and the harness base image `python:3.13.17-slim-trixie` (`containers/harness.Dockerfile:1`).

## Preconditions / Predecessor Evidence

- Predecessor CRM-5 (GREEN): `Plan.md` Execution Status row "CRM-5 — Inference Client GREEN (GREEN) | Complete | GREEN verified on 2026-11-10 by `004_Implementation_Plan_Inference_Client_GREEN.md`: C5-AC-1–C5-AC-4 met; `voice_narration/inference/application.py` matches the planned content (SHA-256 `4a98dafc…1088`); 71 of 71 tests pass in two consecutive full runs". Its evidence section "CRM-5 Execution Evidence" records C5-V2 and C5-V3 `71 passed, 1 warning`.
- CRM-3 (GREEN) is Complete: Chatterbox takes the `sample_audio` upload, keeps no data and serves one request at a time (`Plan.md` "CRM-3 Execution Evidence").
- CRM-1 (CONTRACT) is Complete, pointing to the approved `API-Contract.md`.
- CRM-6 is Pending. No Implementation Plan for CRM-6 exists: the work-item folder holds `requirements.md`, `Plan.md`, `API-Contract.md` and Implementation Plans `001` to `004`. This plan is numbered `005`.
- Milestone type check: `Plan.md` records CRM-6 as OTHER; this plan is OTHER.
- Baseline evidence `Plan.md` names, observed on 2026-11-10 at commit `9be9ca8` (read-only) and re-recorded at execution step 2 before any change:
  - B1 — `cloudrun/chatterbox-service/README.md:5-14` deploys with placeholder values `gcr.io/<PROJECT_ID>/...` and `--region <REGION>`, with `--allow-unauthenticated` (`:11`), and sets `CHATTERBOX_DEVICE=cpu` (`:13`). It sets no GPU, instance-count, concurrency or request-timeout option. Its build step passes `-f` to `gcloud builds submit` (`:6`); the installed `gcloud builds submit --help` lists no Dockerfile option, only `--config`, `--pack` and `--tag`.
  - B2 — `cloudrun/chatterbox-service/Dockerfile:1` `FROM python:3.11-slim`; `:14` `ENV CHATTERBOX_DEVICE=cpu`.
  - B3 — `.dockerignore:1-4`: `*`, `!requirements-dev.txt`, `!containers/`, `!containers/harness.Dockerfile`.
  - B4 — the full suite passes: CRM-5 recorded `71 passed`; re-run at execution step 2.
  - B5 — the documented image does not build. Planning-time observation (disposable copy, Planning-Time Dry Run steps 1 and 2): the build stops at `COPY voice_narration /app/voice_narration` with `"/voice_narration": not found`, because `.dockerignore` admits only `requirements-dev.txt` and `containers/`. With that step removed in a scratch-only probe, `pip install -r /app/requirements-dev.txt` on `python:3.11-slim` fails with `No matching distribution found for numpy==2.5.4`, because `numpy 2.5.4` requires Python `>=3.12`.
- Pre-existing failures: no test fails. The suite passed twice in the dry-run copy, and the failing image build (B5) is this milestone's subject. One pre-existing defect outside this milestone's scope was found by reading the released model loader, and is raised as C6-Q-1 below.

## Current Repository State

Inspected on 2026-11-10.

- `git rev-parse HEAD`: `9be9ca823bc8fc4c84c47197594622b97731855a` ("CRM-5 GREEN: inference client sends sample upload with identity token"). `git status --short` printed nothing.
- `cloudrun/chatterbox-service/` holds `Dockerfile` (20 lines, committed SHA-256 `3f6bbce3353759af4b185ef0d8fe05fb4d6013ce2247895b90fc420154450a9f`) and `README.md` (20 lines, committed SHA-256 `ad94c3782318f713c59ca0f9caa2325b751fe84d8ae9723fffe64cd3b00dba8f`). `git ls-files --eol` shows `i/lf w/crlf` for both and for `.dockerignore`.
- `Dockerfile`: `python:3.11-slim`; installs `requirements-dev.txt` (`:9-10`); copies `voice_narration` (`:12`); `CHATTERBOX_DEVICE=cpu`, `CHATTERBOX_MODEL_VARIANT=v3`, `PORT=8080` (`:14-16`); runs `uvicorn voice_narration.chatterbox_api.application:app` on port 8080 (`:20`).
- `requirements-dev.txt` pins `numpy==2.5.4` (`:7`), `av==19.0.2` (`:8`) and `chatterbox-tts==0.1.7` (`:10`). By PyPI metadata (Authoritative References), only Python 3.13 satisfies all three together with `torch==2.6.0`: below 3.12 `numpy 2.5.4` and `av 19.0.2` cannot install, on 3.12 `chatterbox-tts 0.1.7` requires `numpy<2.0.0`, and from 3.14 it requires `torch>=2.9.0` instead of `2.6.0`.
- `.dockerignore` (shared, at the repository root) admits only `requirements-dev.txt` and `containers/harness.Dockerfile`. `containers/harness.Dockerfile` copies only `requirements-dev.txt`. `cloudrun/inference-service/Dockerfile` also copies `voice_narration`; it is excluded from this work item (`Plan.md` CRM-6 exclusions) and is not changed.
- The repository root holds git-ignored `.env` and `service-account-key.json` (`.gitignore:5`, `:10`). `voice_narration/` holds git-ignored `__pycache__` directories only (`git status --short --ignored voice_narration`; every ignored file found is a `.pyc` under `__pycache__`).
- Chatterbox application (CRM-3): model loaded lazily into a module global under `_generation_lock` (`voice_narration/chatterbox_api/application.py:36-44`, `:51-53`); `DEVICE` from `CHATTERBOX_DEVICE` (`:20`); generation in the thread pool through `run_in_threadpool` (`:132`). In the local `.venv`, `run_in_threadpool` calls `anyio.to_thread.run_sync` (`starlette/concurrency.py:32-34`), whose default limiter is `CapacityLimiter(40)` (`anyio/_backends/_asyncio.py:3257`, anyio 4.16.0).
- Inference service (CRM-5): reads `CHATTERBOX_API_BASE_URL`, `VOICE_CLONING_API_BASE_URL` (`application.py:28-29`) and `VOICE_CLONING_TIMEOUT_SECONDS` (`:46`) at import; locates the key at call time (`:126-127`).
- Tools present locally: Docker 29.3.1 with buildx 0.32.1; Google Cloud SDK 564.0.0. No deployment is performed and no cloud API is called by this plan or its verification.

## Files in Scope

### Files to Create

- `cloudrun/chatterbox-service/Dockerfile.dockerignore` — complete content under Proposed Code / Tests.

### Files to Modify

- `cloudrun/chatterbox-service/Dockerfile` — unified diff and complete final content under Proposed Code / Tests.
- `cloudrun/chatterbox-service/README.md` — complete final content under Proposed Code / Tests (the whole file is replaced).

### Files to Delete

None.

## Proposed Changes

1. `cloudrun/chatterbox-service/Dockerfile` — line 1 only: `FROM python:3.11-slim` becomes `FROM python:3.13.17-slim-trixie` (C6-D-2). Why: the documented build step cannot succeed on Python 3.11, because the image installs `requirements-dev.txt` and its pins need Python 3.13 (B5, Current Repository State). Every other line stays as it is, including `ENV CHATTERBOX_DEVICE=cpu` (C6-D-9).
2. `cloudrun/chatterbox-service/Dockerfile.dockerignore` — new file with five lines (C6-D-3). Why: the documented build step cannot succeed while the shared `.dockerignore` keeps `voice_narration` out of the build context (B5):
   1. `*` — exclude everything;
   2. `!requirements-dev.txt` — admit the dependency list the Dockerfile copies (`Dockerfile:9`);
   3. `!voice_narration/` — admit the application package the Dockerfile copies (`Dockerfile:12`);
   4. `**/__pycache__` — exclude local bytecode directories;
   5. `**/*.pyc` — exclude stray bytecode files.
3. `cloudrun/chatterbox-service/README.md` — replace the whole file with the deployment document (C6-D-1). Sections, in order:
   1. title and introduction: a separate private Cloud Run service on an NVIDIA L4 GPU (AGW-011, CCR-1, CCR-4); only voice cloning on Google Cloud, the other services and narration local (CCR-1, CCR-2); the document does not perform the deployment (CCR-11, requirements Explicit Exclusions);
   2. "Fixed values": project, region, service name, Artifact Registry repository `chatterbox`, image name, the only allowed caller (CCR-1, CCR-3, CCR-7; C6-D-4, C6-D-13);
   3. "Prerequisites": Docker and the virtual environment per `docs/developer-setup.md`; `gcloud` signed in with deploy permissions; the `test-850` key stays local; PowerShell from the repository root in one session; `gcloud config set project`; `gcloud services enable run.googleapis.com artifactregistry.googleapis.com`; the automatic L4 quota with zonal redundancy off (C6-D-8, C6-D-12);
   4. "1. Build the image": `docker build -f cloudrun/chatterbox-service/Dockerfile -t chatterbox-model-api:local .` (the `Plan.md` verification command); what the build context holds; no weights in the image;
   5. "2. Push the image to Artifact Registry": `gcloud artifacts repositories create chatterbox --repository-format=docker --location=asia-southeast1`; `gcloud auth configure-docker asia-southeast1-docker.pkg.dev`; `$TAG = git rev-parse --short HEAD`; `$IMAGE`; `docker tag`; `docker push` (C6-D-4);
   6. "3. Deploy the private service": one `gcloud run deploy chatterbox-model-api` command with `--image $IMAGE`, `--region asia-southeast1`, `--no-allow-unauthenticated`, `--gpu 1`, `--gpu-type nvidia-l4`, `--no-gpu-zonal-redundancy`, `--cpu 4`, `--memory 16Gi`, `--no-cpu-throttling`, `--min-instances 0`, `--max-instances 1`, `--concurrency 80`, `--timeout 600`, `--port 8080`, `--set-env-vars CHATTERBOX_DEVICE=cuda,CHATTERBOX_MODEL_VARIANT=v3`, and a table of what each setting does (CCR-3, CCR-4, CCR-7, CCR-9, Deployment, Consistency and concurrency; C6-D-5 to C6-D-10);
   7. "4. Allow only the service account to call it": `gcloud run services add-iam-policy-binding` with `serviceAccount:test-850@...` and `roles/run.invoker`; `gcloud run services get-iam-policy` and what it must list; `gcloud run services remove-iam-policy-binding` for `allUsers` or `allAuthenticatedUsers` if an earlier public deployment left them; project-level roles (CCR-7; C6-D-10);
   8. "5. Get the service URL": `gcloud run services describe ... --format "value(status.url)"`; `https://`, no trailing `/`, used exactly (CCD-4, C5-RSK-1, C5-RSK-2);
   9. "6. Configure and start the local inference service": the three contract settings with their defaults and fallbacks; that they are read from the process environment at start and a `.env` does not set them; `$env:` assignments and `.\.venv\Scripts\python.exe -m voice_narration.inference`; what each cloning request carries; local saving and no retention; how voice cloning is selected (`"mode": "voice_cloning"`) and that the frontend sends no mode (`Plan.md` RSK-8); the `Voice cloning failed:` answer (CCD-5, CCD-6, CCD-7, CCD-10);
   10. "One request at a time": Chatterbox serializes generation; Cloud Run passes up to 80 requests to the one instance; beyond that, Cloud Run's `429`; waiting counts toward the time limit; retries make a new clip (CCD-9, CCD-11; `Plan.md` RSK-2);
   11. "Cold start and the time limit": cold start and first model load count toward the limit; weights in the in-memory file system; a timed-out first request keeps loading the model; idle shutdown; `--timeout` at least `VOICE_CLONING_TIMEOUT_SECONDS`, at most 3600 (`Plan.md` RSK-3, RSK-4; C6-D-7);
   12. "Runtime endpoints": the three operations, carried over from the baseline README (`:16-20`), with the multipart shape (CCD-1), and that on Cloud Run every endpoint needs the identity token (contract Compatibility Notes).
   The baseline instructions (`gcr.io/<PROJECT_ID>`, `--region <REGION>`, `--allow-unauthenticated`, `CHATTERBOX_DEVICE=cpu`, `gcloud builds submit ... -f`) are removed.

### Decisions for review

- C6-D-1 — Document location and organization. The document replaces `cloudrun/chatterbox-service/README.md`, as `Plan.md` Non-Blocking Open Decisions records ("the document lives with the existing Chatterbox Cloud Run deployment artifacts and replaces their current deployment instructions"), and leaves "Its section organization ... to the CRM-6 Implementation Plan". Organization: numbered steps in the order an operator runs them, then three explanatory sections. Alternative: a separate file next to the README. Not chosen: two documents would keep the public instructions unless the README were also changed.
- C6-D-2 — Base image `python:3.13.17-slim-trixie`. Why: the image installs `requirements-dev.txt`, and only Python 3.13 satisfies its pins together with `chatterbox-tts 0.1.7` and `torch==2.6.0` (Current Repository State, PyPI). CPython 3.13.17 is the project's runtime (`docs/developer-setup.md:3`) and the harness image's base (`containers/harness.Dockerfile:1`). Python 3.13 is supported (status "security", end of life 2029-10, `devguide.python.org/versions`). The tag exists: the dry-run build resolved it to `sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962`. Alternatives: `python:3.12-slim` — cannot install (`chatterbox-tts` needs `numpy<2` there, against `numpy==2.5.4`); `python:3.14-slim` (bugfix status) — pulls `torch>=2.9.0` instead of the `2.6.0` that `chatterbox-tts` pins below 3.14, a different model runtime from every other environment of the project; an NVIDIA CUDA base image — not needed, because Cloud Run preinstalls the driver and `torch 2.6.0` installs its CUDA libraries as packages (pip resolves `nvidia-cuda-runtime-cu12 12.4.127` and `nvidia-cudnn-cu12 9.1.0.70`, dry run step 2); changing `requirements-dev.txt` — dependency declarations are out of scope (`Plan.md` RSK-6).
- C6-D-3 — A Dockerfile-specific ignore file instead of a change to the shared `.dockerignore`. Why: Docker uses `cloudrun/chatterbox-service/Dockerfile.dockerignore` for this Dockerfile only, in place of the root file (Docker build-context documentation); the harness build context and the excluded inference-service image stay as they are. The file admits only what the Dockerfile copies, so `.env`, `service-account-key.json`, `.venv`, `audio_storage` and bytecode stay out (dry run step 3). Alternative: add `!voice_narration/` to the root `.dockerignore`. Not chosen: it changes the context of every image built from the repository root, including the out-of-scope inference-service image. Consequence: the per-Dockerfile file is read by BuildKit, the default builder of the installed Docker 29.3.1; the documented build uses the local Docker (C6-D-4). The harness build is still run (C6-V7) to show the shared context is unaffected.
- C6-D-4 — Build locally and push to Artifact Registry repository `chatterbox` in `asia-southeast1`, tagged with the short commit hash. Why: Google recommends Artifact Registry (Cloud Run deploying documentation); a regional repository in the service's region keeps the image next to it; `gcloud builds submit --tag` builds only a Dockerfile at the source root (installed help lists `--config`, `--pack`, `--tag` and no Dockerfile option), so Cloud Build would need a new build-configuration file, which the documented steps do not need. The commit tag ties a deployed image to its source. Alternatives: Cloud Build with a new `cloudbuild.yaml` — not chosen, it adds a deployment artifact the steps do not need; `gcr.io` as in the baseline — not chosen; repository name `voice-narration` as in the excluded `cloudrun/inference-service/deployment.yaml:15` — not chosen, because that file belongs to the excluded inference-service artifacts; tag `latest` — not chosen, it does not identify the source.
- C6-D-5 — `--cpu 4 --memory 16Gi`. Why: the minimum Cloud Run allows with one L4 (GPU documentation; installed help: "1 gpu also requires a minimum 4 --cpu value and a minimum 16Gi --memory value"). No scale or latency target is required (requirements Operational Characteristics). Alternative: 8 CPU and 32 GiB, which the GPU documentation recommends. Not chosen: no approved artifact asks for it, and it costs more per instance-second. Whether 16 GiB holds the downloaded weights and the loaded model together is a hypothesis (C6-RSK-3).
- C6-D-6 — `--concurrency 80`. Why: with `--max-instances 1`, a request that finds the instance at its concurrency limit pends for about 10 seconds or more and then gets `429` (autoscaling documentation). With concurrency `1`, every request that arrives during a generation would get `429` instead of waiting, which contradicts "other requests wait their turn within the time limit" (requirements Consistency and concurrency) and CCD-9. With concurrency above 1, requests reach the instance and wait on Chatterbox's own lock (C3-D-3), so one clip is generated at a time and the others wait. `80` is Cloud Run's documented console default (concurrency documentation). Alternatives: `1` — not chosen, for the reason above; leaving the flag out — not chosen, because the documentation gives the `gcloud` default as 80 times the vCPU count (320 here), and an explicit value makes the document state its behavior; a smaller value such as `40` (the thread limiter observed locally, C6-RSK-5) — not chosen, because no approved artifact names a limit and both values satisfy the requirement. The reviewer may prefer another value; any value from 2 to 1000 keeps the documented behavior apart from where `429` starts.
- C6-D-7 — `--timeout 600`. Why: 600 seconds equals the default of `VOICE_CLONING_TIMEOUT_SECONDS` (CCD-6), so Cloud Run does not end a request before the inference service's own limit; the inference service starts timing when it starts sending (contract Inference Service Voice Cloning Call), which is before Cloud Run receives the request, so the inference service's limit is reached first and it answers CFR-5. The document tells the operator to raise `--timeout` with the local limit, up to 3600 (request-timeout documentation). Alternative: a margin such as `660` or the maximum `3600`. Not chosen: no approved artifact asks for a margin; a longer platform limit lets abandoned requests hold the instance longer.
- C6-D-8 — `--no-gpu-zonal-redundancy`. Why: the automatically granted quota is for L4 "zonal redundancy off", and zonal-off increases "are more likely to be granted" (GPU documentation); the requirements state no uptime expectation. Alternative: `--gpu-zonal-redundancy`. Not chosen: it needs a quota request and costs more, for availability no requirement asks for.
- C6-D-9 — GPU device through `--set-env-vars CHATTERBOX_DEVICE=cuda` at deployment; the image's `ENV CHATTERBOX_DEVICE=cpu` stays. Why: `Plan.md` says "selecting the GPU device uses the existing device setting (RF-5)", and the application passes the value to the model loader unchanged (`application.py:20`, `:43`). Keeping the image default leaves local runs of the image on CPU. Alternative: change the image default to `cuda`. Not chosen: it is a Dockerfile change the documented steps do not need.
- C6-D-10 — Private access through `--no-allow-unauthenticated` and one service-level `roles/run.invoker` binding for `serviceAccount:test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`, with Cloud Run's invoker IAM check left at its default (enabled). Why: CCR-7, CCD-4, and the service-to-service documentation. The document also tells the operator to check the policy and remove `allUsers` or `allAuthenticatedUsers` left by the baseline's public deployment (RF-7). The runtime service account of the revision is not set, so Cloud Run uses its default (C6-RSK-6). Alternative: `--no-invoker-iam-check` or `--allow-unauthenticated` with an application check. Not chosen: the contract assigns the check to Cloud Run.
- C6-D-11 — `--min-instances 0 --max-instances 1`. Why: requirements Deployment ("may scale to zero when idle, with at most 1 instance running"); 1 is below the automatic quota of 3 (GPU documentation: max instances must stay below the quota). No alternative meets the requirement.
- C6-D-12 — Commands for PowerShell on Windows, run from the repository root. Why: the baseline README uses PowerShell line continuations (`` ` ``) and `docs/developer-setup.md` gives PowerShell first. Alternative: also give Linux shell forms. Not chosen: no approved artifact asks for them, and two forms double what must be kept correct.
- C6-D-13 — Service name `chatterbox-model-api`, port `8080`, `CHATTERBOX_MODEL_VARIANT=v3`, carried from the baseline README and Dockerfile. No alternative is proposed.

No dependency, package version or application setting is introduced. The one version choice is the base image tag of C6-D-2, which repeats the project's existing runtime. Every `gcloud` flag and value in the document traces to a requirement, the contract, or a decision above (C6-D-4 to C6-D-11), and every flag exists in the installed `gcloud` (C6-V4).

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

### `cloudrun/chatterbox-service/Dockerfile` — complete final content (20 lines, LF, ASCII, SHA-256 `9ce80691dc82b749ba5f7f39da648f0519f475ad1339930124e87ed5a523eeb8`)

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

### `cloudrun/chatterbox-service/Dockerfile.dockerignore` — complete content (5 lines, LF, ASCII, SHA-256 `4ac6d36678cdaa14d904773305614bc57f3035cb7b6e1584c55f0eca98c2bfd7`)

```text
*
!requirements-dev.txt
!voice_narration/
**/__pycache__
**/*.pyc
```

### `cloudrun/chatterbox-service/README.md` — complete final content (246 lines, LF, ASCII, SHA-256 `fa5235a15daac35c539109313144751067fb8d29ff84fa64bd8ccffdb7929fc7`)

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
| Image | `asia-southeast1-docker.pkg.dev/project-84eb579f-1f7b-4f87-838/chatterbox/chatterbox-model-api`, tagged with the short commit hash (step 2) |
| Only allowed caller | `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` |

## Prerequisites

- Docker and the repository's Python virtual environment, set up as described
  in `docs/developer-setup.md`.
- The Google Cloud CLI (`gcloud`), signed in with `gcloud auth login` as an
  account that may enable services, create Artifact Registry repositories,
  push images, deploy Cloud Run services and change their IAM policy in the
  project (for example a project Owner).
- The service-account key file of
  `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` on the
  local machine. It is the same key the local Google TTS narration uses. It is
  never copied into the image and never uploaded.

Run every command below in PowerShell from the repository root, and run steps 2
to 6 in the same PowerShell session: later steps use the `$IMAGE` and
`$CHATTERBOX_URL` variables that earlier steps set.

Set the project and enable the services once:

```powershell
gcloud config set project project-84eb579f-1f7b-4f87-838
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
```

GPU quota: on a project's first GPU deployment in a region, Cloud Run
automatically grants a quota of 3 L4 GPUs with zonal redundancy turned off.
This deployment uses at most one GPU instance with zonal redundancy turned off,
so it needs no quota request. If the deployment reports a GPU quota error,
request quota for "L4 GPU with zonal redundancy turned off" in
`asia-southeast1` from the Google Cloud console.

## 1. Build the image

```powershell
docker build -f cloudrun/chatterbox-service/Dockerfile -t chatterbox-model-api:local .
```

The build reads `cloudrun/chatterbox-service/Dockerfile.dockerignore`, which
sends only `requirements-dev.txt` and the `voice_narration` package to Docker.
Local secrets such as `service-account-key.json` and `.env` stay out of the
image. The image holds no model weights; Chatterbox downloads them the first
time it loads the model (see "Cold start and the time limit").

## 2. Push the image to Artifact Registry

Create the repository once:

```powershell
gcloud artifacts repositories create chatterbox `
  --repository-format=docker `
  --location=asia-southeast1
```

Let Docker push to it, tag the image with the current commit, and push:

```powershell
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
$TAG = git rev-parse --short HEAD
$IMAGE = "asia-southeast1-docker.pkg.dev/project-84eb579f-1f7b-4f87-838/chatterbox/chatterbox-model-api:$TAG"
docker tag chatterbox-model-api:local $IMAGE
docker push $IMAGE
```

## 3. Deploy the private service

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
| `CHATTERBOX_MODEL_VARIANT=v3` | The model variant, as before. |

## 4. Allow only the service account to call it

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

## 5. Get the service URL

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

## 6. Configure and start the local inference service

The inference service reads these settings from its process environment once,
when it starts. A `.env` file does not set them. After a change, restart the
inference service.

| Setting | Value |
| --- | --- |
| `VOICE_CLONING_API_BASE_URL` | The service URL from step 5. When it is not set, `CHATTERBOX_API_BASE_URL` is used. |
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
step 3 again with `--timeout` set to the same value.

## Runtime endpoints

- `GET /health`
- `GET /v1/metadata`
- `POST /v1/synthesize` (`multipart/form-data` with `text`, `language` and the
  file part `sample_audio`)

On Cloud Run every endpoint requires the service account's identity token.
````

## Execution Steps

1. Confirm this plan's Human Review status records approval.
2. Record the baseline before any change (C6-AC-1), from the repository root:
   1. B1–B3: `git show HEAD:cloudrun/chatterbox-service/README.md`, `git show HEAD:cloudrun/chatterbox-service/Dockerfile`, `git show HEAD:.dockerignore`, quoting the lines listed under Preconditions / Predecessor Evidence;
   2. `git status --short` (expected: no output) and `git rev-parse HEAD`;
   3. B5: C6-V5 on the unmodified repository, tagged `chatterbox-model-api:baseline` instead of `:local` (expected: fails at `COPY voice_narration`; a failed build creates no image);
   4. B4: C6-V8 (expected: `71 passed`).
3. Write the three files from this plan's code blocks with LF endings: create `cloudrun/chatterbox-service/Dockerfile.dockerignore`; overwrite `cloudrun/chatterbox-service/Dockerfile` and `cloudrun/chatterbox-service/README.md`.
4. Run C6-V1 to C6-V10 in order.
5. Report each command with its trimmed output, and each started container as stopped.

## Acceptance / Completion Criteria

- C6-AC-1 — The baseline is recorded before any change: B1–B3 quoted from `HEAD`, B4 `71 passed`, B5 the unmodified image build failing.
- C6-AC-2 — The three files match this plan exactly (C6-V1 hashes `9ce80691…eeb8`, `4ac6d366…bfd7`, `fa5235a1…9fc7`), and no other file changes: `git status --short` lists only ` M cloudrun/chatterbox-service/Dockerfile`, ` M cloudrun/chatterbox-service/README.md`, `?? cloudrun/chatterbox-service/Dockerfile.dockerignore` and this Implementation Plan (excluding the milestone's own Execution Status update in `Plan.md`).
- C6-AC-3 — The document covers every completion-checklist item (`Plan.md` CRM-6 completion evidence), shown by C6-V2 with the line where each appears:

  | Item | Source | Where in the document |
  | --- | --- | --- |
  | Build the Chatterbox image | CRM-6 scope | step 1 |
  | Separate Cloud Run service | AGW-011 | introduction; step 3 (own service `chatterbox-model-api`) |
  | Project `project-84eb579f-1f7b-4f87-838` | CCR-1 | Fixed values; Prerequisites (`gcloud config set project`) |
  | Region `asia-southeast1` | CCR-3 | Fixed values; step 3 `--region asia-southeast1` |
  | NVIDIA L4 GPU | CCR-4 | step 3 `--gpu 1`, `--gpu-type nvidia-l4` |
  | Private, callable only by `test-850@…` | CCR-7 | step 3 `--no-allow-unauthenticated`; step 4 binding and check |
  | Scale to zero | Deployment | step 3 `--min-instances 0` |
  | At most 1 instance | Deployment | step 3 `--max-instances 1` |
  | One request at a time | Deployment (AC-CCR-8), Consistency and concurrency | step 3 `--concurrency 80` row; "One request at a time" |
  | Request time limit accommodating 10 minutes | CCR-9 | step 3 `--timeout 600`; "Cold start and the time limit" |
  | Local inference configuration | contract Inference Service Settings | step 6 (three settings) |
  | Deployment not performed by this work item | CCR-11 | introduction |

- C6-AC-4 — No instruction to deploy publicly remains: C6-V3 finds no `--allow-unauthenticated` other than `--no-allow-unauthenticated` under `cloudrun/chatterbox-service/`, and `allUsers` appears only in the policy check and its removal command.
- C6-AC-5 — Every `gcloud` flag the document uses exists in the installed `gcloud` (C6-V4 prints no `MISSING`).
- C6-AC-6 — The documented build command builds the image from the repository (C6-V5, exit 0). The image runs Python 3.13.17, holds under `/app` only `requirements-dev.txt` and `.py` files (no `.env`, key file or bytecode), imports the Chatterbox application (`cpu v3`), passes the 13 CRM-2 Chatterbox tests on its own installed packages, and answers `GET /health` with `200` and `{"status":"ok","service":"chatterbox_api","model_variant":"v3","device":"cpu"}` on a dynamically allocated loopback port; every container is stopped afterwards (C6-V6).
- C6-AC-7 — The harness image still builds and runs, printing `dependency image ready` (C6-V7).
- C6-AC-8 — The preserved tests pass in two consecutive full runs without cleaning: 71 collected, 71 passed, no `FAILED` or `ERROR` line (C6-V8, C6-V9). They are the full suite `Plan.md` names: `test_voice_enrollment_creates_profile`, `test_generation_uses_selected_voice_profile`, `test_voice_cloning_returns_guidance_when_clone_backend_unavailable` and `test_gateway_execution_returns_non_placeholder_telemetry` (as updated by CRM-4), the five tests in `tests/test_ai_gateway_red.py`, the 13 tests in `tests/test_chatterbox_service_red.py` (CRM-2) and the 49 cases in `tests/test_inference_client_red.py` (CRM-4).
- C6-AC-9 — No service behavior changes: C6-V10 shows no change under `voice_narration/`, `tests/`, `requirements-dev.txt`, `pytest.ini`, `.dockerignore`, `containers/`, `cloudrun/inference-service/` or `frontend/`.

## Verification

### Commands

C6-V1, C6-V2, C6-V3, C6-V4, C6-V6, C6-V7 and C6-V10 run in Git Bash from the repository root. C6-V5 runs in either shell. C6-V8 and C6-V9 are the `Plan.md` PowerShell commands.

- C6-V1 — exact content:

  ```bash
  sha256sum cloudrun/chatterbox-service/Dockerfile cloudrun/chatterbox-service/Dockerfile.dockerignore cloudrun/chatterbox-service/README.md
  ```

- C6-V2 — completion checklist, with line numbers:

  ```bash
  grep -nE -- '^## |project-84eb579f-1f7b-4f87-838$|--region asia-southeast1|--gpu 1|--gpu-type nvidia-l4|--no-allow-unauthenticated|--min-instances 0|--max-instances 1|--concurrency 80|--timeout 600|roles/run.invoker|VOICE_CLONING_API_BASE_URL = |VOICE_CLONING_TIMEOUT_SECONDS = |GOOGLE_APPLICATION_CREDENTIALS` \||performs the deployment' cloudrun/chatterbox-service/README.md
  ```

- C6-V3 — no public deployment instruction:

  ```bash
  grep -rn -- 'allow-unauthenticated' cloudrun/chatterbox-service | grep -v -- '--no-allow-unauthenticated'; echo "public-flag-lines-exit=$?"
  grep -n 'allUsers' cloudrun/chatterbox-service/README.md
  ```

- C6-V4 — every `gcloud` flag exists in the installed `gcloud`:

  ```bash
  check() { cmd="$1"; shift; help=$(gcloud $cmd --help 2>&1); for f in "$@"; do base="${f#--}"; base="${base#no-}"; if printf '%s' "$help" | grep -qE -- "(^|[[ ])--(\[no-\])?${base}([]=, ]|$)"; then echo "ok   $cmd $f"; else echo "MISSING $cmd $f"; fi; done; }
  check "run deploy" --image --region --no-allow-unauthenticated --gpu --gpu-type --no-gpu-zonal-redundancy --cpu --memory --no-cpu-throttling --min-instances --max-instances --concurrency --timeout --port --set-env-vars
  check "run services add-iam-policy-binding" --region --member --role
  check "run services remove-iam-policy-binding" --region --member --role
  check "run services get-iam-policy" --region
  check "run services describe" --region --format
  check "artifacts repositories create" --repository-format --location
  gcloud auth configure-docker --help > /dev/null 2>&1 && echo "ok   auth configure-docker"
  gcloud services enable --help > /dev/null 2>&1 && echo "ok   services enable"
  gcloud config set --help > /dev/null 2>&1 && echo "ok   config set"
  ```

- C6-V5 — the documented build (`Plan.md` Verification Commands):

  ```
  docker build -f cloudrun/chatterbox-service/Dockerfile -t chatterbox-model-api:local .
  ```

- C6-V6 — image contents, runtime versions, import, the CRM-2 Chatterbox tests on the image's own packages, and health over loopback:

  ```bash
  docker run --rm chatterbox-model-api:local sh -c 'python --version; find /app -type f ! -name "*.py" ! -path /app/requirements-dev.txt; echo end-of-list'
  docker run --rm chatterbox-model-api:local python -c "import fastapi, starlette, anyio, torch; print(fastapi.__version__, starlette.__version__, anyio.__version__, torch.__version__, torch.version.cuda)"
  docker run --rm chatterbox-model-api:local python -c "import voice_narration.chatterbox_api.application as a; print(a.DEVICE, a.MODEL_VARIANT)"
  MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W)/tests:/app/tests:ro" -v "$(pwd -W)/pytest.ini:/app/pytest.ini:ro" chatterbox-model-api:local python -m pytest tests/test_chatterbox_service_red.py -q -p no:cacheprovider
  cid=$(docker run -d --rm -p 127.0.0.1::8080 chatterbox-model-api:local); port=$(docker port "$cid" 8080/tcp | head -1 | sed 's/.*://'); curl -s -w ' HTTP %{http_code}\n' --retry 60 --retry-connrefused --retry-delay 1 "http://127.0.0.1:$port/health"; docker stop "$cid"
  ```

  The fourth command mounts the repository's `tests/` and `pytest.ini` read-only into a throw-away container; nothing is added to the image or the repository. `test_chatterbox_service_red.py` replaces the model runtime with its own stand-ins (`tests/test_chatterbox_service_red.py:174-180`), so it runs on the image's web framework without loading the model.

- C6-V7 — the harness image (`Plan.md` Verification Commands, `docs/developer-setup.md`):

  ```
  docker build -f containers/harness.Dockerfile -t vn-harness:foundation .
  docker run --rm vn-harness:foundation
  ```

- C6-V8 — full suite (PowerShell, `Plan.md` Verification Commands): `.\.venv\Scripts\python.exe -m pytest tests -ra`
- C6-V9 — full suite again, without cleaning: `.\.venv\Scripts\python.exe -m pytest tests -ra`
- C6-V10 — scope of the change:

  ```bash
  git status --short
  git status --short -- voice_narration tests requirements-dev.txt pytest.ini .dockerignore containers cloudrun/inference-service frontend
  git diff --stat
  ```

### Expected Evidence

Expected / Predicted — Not Yet Verified. Each item becomes evidence only when the command has been run at execution and its output supports it.

- C6-V1 prints the three hashes listed in C6-AC-2.
- C6-V2 prints the section headings (`## Fixed values` to `## Runtime endpoints`), the project line, and the lines of each flag and setting in the C6-AC-3 table.
- C6-V3 prints `public-flag-lines-exit=1` (no line) and `allUsers` only on the two lines of step 4 (the policy check sentence and `--member allUsers`).
- C6-V4 prints `ok` for every flag and command and no `MISSING`.
- B5 (step 2) ends with `"/voice_narration": not found` at `COPY voice_narration /app/voice_narration`, exit 1.
- C6-V5 exits 0. The installation step downloads `torch-2.6.0-cp313-cp313-manylinux1_x86_64.whl` and its NVIDIA libraries and takes several minutes on first build.
- C6-V6 prints `Python 3.13.17` then `end-of-list` with no file between them; `0.162.0 0.52.1 4.16.0 2.6.0+cu124 12.4` (the versions pip resolved in dry run step 2; the exact `torch` version string is a prediction); `cpu v3`; `13 passed`; and `{"status":"ok","service":"chatterbox_api","model_variant":"v3","device":"cpu"} HTTP 200`; `docker stop` prints the container ID.
- C6-V7 prints `dependency image ready`.
- C6-V8 and C6-V9: `collected 71 items`, `71 passed, 1 warning` (the existing `StarletteDeprecationWarning`), no `FAILED` or `ERROR` line.
- C6-V10: `git status --short` lists exactly the entries in C6-AC-2; the scoped `git status` prints nothing; `git diff --stat` lists only the two modified files under `cloudrun/chatterbox-service/` (the new file is untracked).
- Preserved tests: the full suite listed in C6-AC-8, expected to pass at baseline and after the change.

### Planning-Time Dry Run

Planning-time dry run — not milestone evidence. Run on 2026-11-10 in disposable copies under `C:\Users\avina\AppData\Local\Temp\claude\dd431ff1ad187051\a64835d9-b6b8-4c46-a2ab-81eb4d20b4b6\scratchpad`. Copies for the image builds were made with `git archive HEAD` (commit `9be9ca8`, no git-ignored files); the copy for the suite was made with `tar` from the working tree, excluding `.venv`, `.git`, `frontend`, `audio_storage`, `__pycache__`, `.pytest_cache`, `.deepeval` and `*.zip`, and including the git-ignored `.env` and `service-account-key.json` that the preserved narration test needs (as for CRM-5). The proposed files were written into the copies from this plan's content. The dry run is partial: the proposed image build did not finish (step 3), so C6-V5's completion, C6-V6 and C6-V7 were not run.

1. B5, the unmodified image build (copy of `HEAD`):

   ```
   $ docker build --progress=plain -f cloudrun/chatterbox-service/Dockerfile -t crm6-dryrun-baseline:local .        (exit 1)
   #2 [internal] load metadata for docker.io/library/python:3.11-slim
   #8 [5/5] COPY voice_narration /app/voice_narration
   #8 ERROR: failed to calculate checksum of ref ...: "/voice_narration": not found
   ERROR: failed to build: failed to solve: failed to compute cache key: ... "/voice_narration": not found
   ```

2. Python version (scratch-only probes; the probe Dockerfile is the committed one without its `COPY voice_narration` line):

   ```
   $ docker build --progress=plain -f probe.Dockerfile -t crm6-probe-py311:local .        (exit 1, python:3.11-slim)
   ERROR: Ignored the following versions that require a different python version: ... 2.5.4 Requires-Python >=3.12
   ERROR: Could not find a version that satisfies the requirement numpy==2.5.4 (from versions: ... 2.4.6)
   ERROR: No matching distribution found for numpy==2.5.4

   $ docker run -i --rm python:3.13.17-slim-trixie sh -c 'cat > /tmp/req.txt; python --version; pip --version; pip install --dry-run --ignore-installed --quiet --report /tmp/r.json -r /tmp/req.txt; ...' < requirements-dev.txt
   Python 3.13.17
   pip 26.2.2 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
   pip-exit=0
   138 packages
   numpy 2.5.4 | torch 2.6.0 | torchaudio 2.6.0 | chatterbox-tts 0.1.7 | transformers 5.2.0 | gradio 6.8.0
   fastapi 0.162.0 | starlette 0.52.1 | anyio 4.16.0 | librosa 0.11.0 | numba 0.68.1 | av 19.0.2
   nvidia-cudnn-cu12 9.1.0.70 | nvidia-cuda-runtime-cu12 12.4.127 | diffusers 0.29.0 | s3tokenizer 0.3.0 | resemble-perth 1.0.1
   ```

   (The version list is printed one per line; it is joined here.)

3. The proposed build (C6-V5) in a copy with the three proposed files, and a build-context probe:

   ```
   $ docker build --progress=plain -f cloudrun/chatterbox-service/Dockerfile -t chatterbox-model-api:local .
   #2 [internal] load metadata for docker.io/library/python:3.13.17-slim-trixie
   #4 [1/5] FROM docker.io/library/python:3.13.17-slim-trixie@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962
   #3 transferring context: 36.49kB 0.4s done
   #6 [3/5] COPY requirements-dev.txt /app/requirements-dev.txt
   #6 DONE 0.2s
   #7 [4/5] RUN pip install --upgrade pip && pip install -r /app/requirements-dev.txt
   #7 105.1 Downloading torch-2.6.0-cp313-cp313-manylinux1_x86_64.whl (766.6 MB)
   ```

   pip finished resolving and was downloading the wheels when the build was stopped after 43 minutes (its client processes, `docker.exe` and `docker-buildx.exe`, were ended). The download rate measured from the host at the same time was `speed=161801 B/s` (`curl` of the first 20 MB of the same `torch` wheel), so the remaining downloads of about 3 GB (`torch` and the `nvidia-*` packages) would have taken hours. The build therefore did not reach `COPY voice_narration`, and no image was produced. Whether the full build, the image's imports and the in-image tests succeed is shown only at execution (C6-V5, C6-V6).

   Build-context probe: in a third copy, dummy `service-account-key.json`, `.env`, `.venv/f`, `audio_storage/clip.wav`, `voice_narration/__pycache__/a.cpython-313.pyc`, `voice_narration/inference/__pycache__/b.pyc` and `voice_narration/stray.pyc` were added, and a scratch `probe.Dockerfile` (`FROM alpine:latest`, `COPY . /ctx`, `CMD find /ctx -type f`) was built with this plan's ignore file copied to `probe.Dockerfile.dockerignore` next to it:

   ```
   $ docker build -q -f cloudrun/chatterbox-service/probe.Dockerfile -t crm6-ctxprobe:local . && docker run --rm crm6-ctxprobe:local | sort
   /ctx/requirements-dev.txt
   /ctx/voice_narration/__init__.py
   /ctx/voice_narration/chatterbox_api/__init__.py
   /ctx/voice_narration/chatterbox_api/__main__.py
   /ctx/voice_narration/chatterbox_api/application.py
   /ctx/voice_narration/inference/__init__.py
   /ctx/voice_narration/inference/__main__.py
   /ctx/voice_narration/inference/application.py
   /ctx/voice_narration/inference/providers/__init__.py
   /ctx/voice_narration/inference/providers/base.py
   /ctx/voice_narration/inference/providers/google.py
   /ctx/voice_narration/inference/providers/mock.py
   /ctx/voice_narration/simple_voices/__init__.py
   /ctx/voice_narration/simple_voices/__main__.py
   /ctx/voice_narration/simple_voices/application.py
   ```

   Only `requirements-dev.txt` and the package's `.py` files enter the context; the dummy secrets, `.venv`, `audio_storage` and bytecode do not.

4. C6-V8 and C6-V9 in the suite copy with the three proposed files applied (`-p no:cacheprovider` added so the copy gets no cache directory):

   ```
   $ python -m pytest tests -ra -p no:cacheprovider        (exit 0)
   collected 71 items
   ======================= 71 passed, 1 warning in 49.81s ========================
   $ python -m pytest tests -ra -p no:cacheprovider        (exit 0, second run, no cleaning)
   collected 71 items
   ======================= 71 passed, 1 warning in 36.69s ========================
   ```

   `FAILED`/`ERROR` line count `0` in both. The warning is the existing `StarletteDeprecationWarning` from `fastapi/testclient.py:1`.

5. The CRM-2 Chatterbox tests on the image's Starlette version, in a scratch virtual environment (`py -3.13 -m venv`) with `fastapi==0.162.0 starlette==0.52.1 uvicorn==0.54.0 python-multipart==0.0.32 pytest==9.1.1 httpx==0.28.1 anyio==4.16.0`, run from the suite copy:

   ```
   $ python -m pytest tests/test_chatterbox_service_red.py -q -p no:cacheprovider        (exit 0)
   .............                                                            [100%]
   13 passed, 1 warning in 3.03s
   ```

   The warning is `DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated` from `starlette/testclient.py:45`.

6. The released model loader (read-only; the `chatterbox-tts 0.1.7` wheel, 108,543 bytes, SHA-256 `83782500e3ad4e7c919132e9d7eb8755f29f57c5bde5ec48c655ca23a4eb113c`, downloaded from PyPI and opened as a zip; nothing installed):

   ```
   chatterbox/mtl_tts.py:201  @classmethod
   chatterbox/mtl_tts.py:202  def from_pretrained(cls, device: torch.device) -> 'ChatterboxMultilingualTTS':
   chatterbox/mtl_tts.py:211-219  ckpt_dir = Path(snapshot_download(repo_id=REPO_ID, repo_type="model", revision="main", allow_patterns=[...six files...], token=os.getenv("HF_TOKEN")))
   chatterbox/mtl_tts.py:220  return cls.from_local(ckpt_dir, device)
   ```

   The same signature, `def from_pretrained(cls, device: torch.device)`, is in the `0.1.4`, `0.1.5` and `0.1.6` wheels; none contains `t3_model`. This is the finding C6-Q-1.

7. C6-V1 to C6-V4 against the proposed files:
   - The four code blocks were extracted from this plan: `Dockerfile` `9ce80691dc82b749ba5f7f39da648f0519f475ad1339930124e87ed5a523eeb8` (20 lines), `Dockerfile.dockerignore` `4ac6d36678cdaa14d904773305614bc57f3035cb7b6e1584c55f0eca98c2bfd7` (5 lines), `README.md` `fa5235a15daac35c539109313144751067fb8d29ff84fa64bd8ccffdb7929fc7` (246 lines), all ASCII. The diff applied with `patch -p1` to `git show HEAD:cloudrun/chatterbox-service/Dockerfile` (`patching file cloudrun/chatterbox-service/Dockerfile`) gives `9ce80691…eeb8`.
   - C6-V2 printed lines 10 (`repository performs the deployment.`), 12–239 for the eleven `## ` headings, 43 (`gcloud config set project project-84eb579f-1f7b-4f87-838`), 91–102 (the deploy flags), 111–120 (their table rows), 131–157 (`--region` and `roles/run.invoker` in step 4), 185 (`GOOGLE_APPLICATION_CREDENTIALS` row), 188–189 (the two `$env:` lines), 210–212 ("One request at a time").
   - C6-V3 printed `public-flag-lines-exit=1`, then `144:If it also lists `allUsers` or `allAuthenticatedUsers` (for example from an` and `150:  --member allUsers ``.
   - C6-V4 printed `ok` for all 28 flag and command checks and no `MISSING`. As a check of the checker, `--gpu-count`, `--allow-gpu` and `--no-zonal` against `gcloud run deploy --help` each printed `MISSING`.

8. Not run in the dry run: C6-V5 to completion and C6-V6 (step 3); C6-V7, because the harness build installs the same `requirements-dev.txt`, including the same downloads, so it would take as long; C6-V10, which depends on the repository's Git state after execution.

9. Created during the dry run and deleted afterwards: under the scratchpad, `base\`, `prop\`, `ctxprobe\` and `suite\` (the disposable copies), `ex\` (the blocks extracted from this plan and the patch check), `venv-st052\` (step 5), `cbwheel\` (the four wheels of step 6), `probe.Dockerfile`, `Dockerfile.orig`, `deploy-help.txt`, `j.json` and the logs `baseline-build.log`, `probe311.log`, `prop-build.log`, `resolve.log`, `suite1.log`, `suite2.log`. Docker objects: image `crm6-ctxprobe:local` and the pulled base image `python:3.13.17-slim-trixie` were removed; the failed and stopped builds produced no image; their build-cache entries remain in Docker's build cache (not pruned, because pruning would also remove unrelated cache). Nothing was written to the repository except this Implementation Plan.

## Risks

- C6-RSK-1 — Identity comparisons (`security`). This milestone adds no comparison in code; it configures the two that Cloud Run makes, and the document keeps each in the same canonical form as the inference service's authentication (C5-RSK-1):
  - Token audience against the service URL. The inference service uses the configured base URL with surrounding whitespace removed and nothing else changed, both to call Chatterbox and as the audience (`application.py:28-29`). The document's step 5 takes the URL from `status.url`, which has no trailing `/`, and tells the operator to use it exactly; Cloud Run requires `aud` to be the service URL (service-to-service documentation). A mismatch is rejected by Cloud Run and answered as CFR-7.
  - Caller identity against the invoker binding. The token is issued for the key file's `client_email` (C5-D-1); the binding names `serviceAccount:test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`, written exactly as CCR-7 gives it, in lowercase as Google issues service-account emails. Cloud Run makes the comparison.
  - Other principals. Principals with a project-level role that includes invoking (for example `roles/owner`) can also call the service; the document states this and tells the operator to grant no such role to others. Whether the project already grants such roles to other principals is not visible from the repository.
  - No user identity, role or ownership comparison exists (login and authentication of application users are excluded).
- C6-RSK-2 — Deployment not exercised. Nothing here runs on Cloud Run: GPU attachment, the L4 driver with the image's CUDA libraries, the invoker check and the platform answers are taken from Google's documentation and the installed `gcloud` help, not observed. That `torch 2.6.0` with its CUDA 12.4 runtime packages (dry run step 2) works with the preinstalled driver 580 (CUDA 13.0) is a hypothesis based on that driver being newer than the runtime. Performing the deployment is excluded (CCR-11); AC-CCR-1 is demonstrated "when deployed as documented" by Final Review inspection (`Plan.md` Final Acceptance Criteria).
- C6-RSK-3 — Real model not exercised (carried from C3-RSK-1). The image's model runtime is not loaded in verification, because loading downloads the model weights, which `docs/developer-setup.md` says not to acquire here. The released loader's source was read instead (dry run step 6): `ChatterboxMultilingualTTS.from_pretrained` calls `huggingface_hub.snapshot_download(repo_id="ResembleAI/chatterbox", ...)` for six files and then `from_local(ckpt_dir, device)` (`chatterbox/mtl_tts.py:201-220` in `chatterbox-tts 0.1.7`), and those six files total 3,208,951,748 bytes (2.99 GiB, Hugging Face file listing). This supports the document's statements that the weights are downloaded on first load into the container's file system. Whether 16 GiB holds them plus the loaded model is a hypothesis. The same reading found that the application's call does not match the loader's signature: see C6-Q-1, which blocks approval.
- C6-RSK-4 — Cold start inside the time limit (`Plan.md` RSK-4). The first request after scale to zero includes the instance start, the weights download and the model load. If that does not fit in 600 seconds, the first request answers CFR-5; the document says so and that a later retry is served by the loaded model while the instance runs. If a cold start cannot fit within CCR-9's limit at all, that is a replanning question (`Plan.md` RSK-4), not a change made here.
- C6-RSK-5 — Waiting requests occupy threads (carried from C3-RSK-3). With `--concurrency 80`, up to 80 requests can be open on the instance. Each waiting request holds a thread-pool worker while it waits for the lock; locally the default limit is 40 workers (anyio 4.16.0, Current Repository State), so beyond 40 a request first waits for a worker. It still waits and is then served. A side effect: `GET /health` and `GET /v1/metadata` also need a worker and may wait under such load. pip resolves the same anyio 4.16.0 for the image (dry run step 2); that the image's copy has the same limit line is checked only through the version, not by reading its source.
- C6-RSK-11 — The image's packages differ from the local `.venv`. The local `.venv` does not have `chatterbox-tts` installed (`Plan.md` Current State), so its packages were never resolved together with it. For the image, pip resolves 138 packages, and `gradio 6.8.0` (a `chatterbox-tts` requirement) brings `starlette 0.52.1`, while the local `.venv` has `starlette 1.10.0`, the version CRM-2 and CRM-3 were verified on (dry run step 2). In the dry run, the 13 CRM-2 tests passed against `starlette 0.52.1` in a scratch environment (dry run step 5), and C6-V6 runs them inside the image at execution. Pinning `starlette` or changing dependency declarations is out of scope (`Plan.md` RSK-6); if C6-V6's in-image test run fails, execution stops and returns to planning.
- C6-RSK-6 — Runtime service account. The document does not set `--service-account`, so the revision runs as Cloud Run's default runtime identity, whose project permissions depend on the project's configuration. Chatterbox calls no Google API; it downloads model weights over the internet. No approved artifact names a runtime identity, so this plan adds none; a dedicated identity with no roles would need new scope.
- C6-RSK-7 — Image size and contents. The image installs all of `requirements-dev.txt`, including test and browser tooling (`pytest`, `playwright`, `psycopg`), together with `torch` and its NVIDIA libraries (138 packages, dry run step 2). Its size was not measured, because the dry-run build did not finish (dry run step 3). `Plan.md` keeps dependency declarations out of scope (RSK-6). `pip install --upgrade pip` (unchanged `Dockerfile:10`) installs whatever pip is current at build time, so two builds may differ in pip version.
- C6-RSK-8 — Mutable base tag. `python:3.13.17-slim-trixie` can be rebuilt by its publisher with operating-system updates, as for the harness image; the dry run resolved it to `sha256:d98cc29d…0962`.
- C6-RSK-9 — Network-dependent preserved test (carried from C5-RSK-6). `test_generation_uses_selected_voice_profile` calls Google TTS with the local key. If it fails at execution for network or credential reasons, C6-AC-8 is not met; execution stops and reports it. No rerun-until-pass, skip or change is authorized.
- C6-RSK-10 — Build needs the network. C6-V5 and C6-V7 download packages from PyPI and the base image from Docker Hub. If a download fails at execution, the criterion is not met; execution stops and reports it.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

- `git restore -- cloudrun/chatterbox-service/Dockerfile cloudrun/chatterbox-service/README.md`.
- Delete `cloudrun/chatterbox-service/Dockerfile.dockerignore`; it exists only because of this milestone.
- Local images created by verification: `docker image rm chatterbox-model-api:local`. `vn-harness:foundation` is the harness image `docs/developer-setup.md` builds; leave it.
- Do not use repository-wide reset, clean or checkout operations.

## Explicitly Out of Scope

- Performing the deployment or calling any Google Cloud API (CCR-11, requirements Explicit Exclusions).
- Any service behavior change: no file under `voice_narration/` or `tests/` changes; the image default device stays `cpu`.
- The shared `.dockerignore`, `containers/harness.Dockerfile`, `requirements-dev.txt`, `pytest.ini` and dependency declarations.
- The inference-service Cloud Run artifacts (`cloudrun/inference-service/`), and moving the voices service, inference service, frontend or narration to Google Cloud.
- A Cloud Build configuration, Terraform or other deployment automation.
- Custom logging, metrics or alerts; duplicate detection; user login or authentication.
- Editing `docs/developer-setup.md` or any other documentation.
- Changing the model-loading call of C6-Q-1, or the CRM-2 stand-in that accepts any keyword; either is a production or test change that needs its own milestone.

## Human Review

Status: Awaiting human approval
