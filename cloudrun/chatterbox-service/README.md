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
