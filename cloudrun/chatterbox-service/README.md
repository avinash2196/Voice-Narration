# Chatterbox Cloud Run Model Service

## Build and deploy

```powershell
gcloud builds submit --tag gcr.io/<PROJECT_ID>/chatterbox-model-api -f cloudrun/chatterbox-service/Dockerfile .
gcloud run deploy chatterbox-model-api `
  --image gcr.io/<PROJECT_ID>/chatterbox-model-api `
  --platform managed `
  --region <REGION> `
  --allow-unauthenticated `
  --port 8080 `
  --set-env-vars CHATTERBOX_DEVICE=cpu,CHATTERBOX_MODEL_VARIANT=v3
```

## Runtime endpoints

- `GET /health`
- `GET /v1/metadata`
- `POST /v1/synthesize`
