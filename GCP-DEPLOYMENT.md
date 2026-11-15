# Voice-Narration: GCP Deployment Guide

## Overview

This guide covers deploying Voice-Narration to Google Cloud Platform using:
- **Cloud Run** for backend services (serverless containers)
- **Cloud Storage** for voice files
- **Cloud SQL** for PostgreSQL database
- **Cloud Build** for CI/CD
- **Artifact Registry** for Docker images

---

## Prerequisites

### GCP Account Setup

1. Create GCP Project
```bash
# Set project name
export PROJECT_ID="voice-narration-prod"
export REGION="us-central1"
export ZONE="us-central1-a"

# Create project
gcloud projects create $PROJECT_ID

# Set as default
gcloud config set project $PROJECT_ID
```

2. Enable Required APIs
```bash
gcloud services enable \
  run.googleapis.com \
  sql-component.googleapis.com \
  compute.googleapis.com \
  storage-api.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  containerregistry.googleapis.com
```

3. Create Service Account
```bash
# Create service account for deployment
gcloud iam service-accounts create voice-narration-sa \
  --display-name="Voice Narration Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```

---

## Step 1: Setup Cloud SQL Database

### Create PostgreSQL Instance

```bash
# Create Cloud SQL instance
gcloud sql instances create voice-narration-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --backup \
  --retained-backups-count=30 \
  --enable-bin-log

# Set root password
gcloud sql users set-password postgres \
  --instance=voice-narration-db \
  --password=your_secure_password

# Create application database
gcloud sql databases create voice_narration \
  --instance=voice-narration-db

# Create application user
gcloud sql users create voice_app \
  --instance=voice-narration-db \
  --password=app_secure_password
```

### Get Connection String

```bash
# Get Public IP
CLOUD_SQL_IP=$(gcloud sql instances describe voice-narration-db \
  --format='value(ipAddresses[0].ipAddress)')

# Connection string for environment variable
DATABASE_URL="postgresql://voice_app:app_secure_password@$CLOUD_SQL_IP:5432/voice_narration"
```

### Enable Cloud SQL Proxy for Local Testing

```bash
# Install Cloud SQL Proxy
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
chmod +x cloud_sql_proxy

# Run proxy (in separate terminal)
./cloud_sql_proxy -instances=voice-narration-db=tcp:5432
```

---

## Step 2: Setup Cloud Storage

### Create Storage Buckets

```bash
# Create bucket for voice files
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION \
  gs://voice-narration-voices/

# Create bucket for audio files
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION \
  gs://voice-narration-audio/

# Create bucket for backups
gsutil mb -p $PROJECT_ID -c COLDLINE -l $REGION \
  gs://voice-narration-backups/

# Set lifecycle policy (delete old files after 90 days)
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 90}
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://voice-narration-audio/
```

### Configure Bucket Permissions

```bash
# Grant service account access to buckets
gsutil iam ch \
  serviceAccount:voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com:objectCreator,objectViewer \
  gs://voice-narration-voices/

gsutil iam ch \
  serviceAccount:voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com:objectCreator,objectViewer \
  gs://voice-narration-audio/
```

---

## Step 3: Setup Artifact Registry

### Create Docker Repository

```bash
# Create artifact registry repository
gcloud artifacts repositories create voice-narration \
  --repository-format=docker \
  --location=$REGION \
  --description="Voice Narration Docker Images"

# Configure Docker authentication
gcloud auth configure-docker $REGION-docker.pkg.dev
```

### Build and Push Backend Image

```bash
# Navigate to project root
cd /path/to/Voice-Narration

# Build backend image
docker build \
  --tag $REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest \
  -f Dockerfile .

# Push to Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest
```

### Build and Push Frontend Image

```bash
# Build frontend image
docker build \
  --tag $REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:latest \
  -f Dockerfile.frontend \
  ./frontend

# Push to Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:latest
```

---

## Step 4: Setup Cloud Run Services

### Deploy Backend Services

#### Auth Service (Port 8001)

```bash
gcloud run deploy voice-narration-auth \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest \
  --platform=managed \
  --region=$REGION \
  --memory=1Gi \
  --cpu=1 \
  --timeout=3600 \
  --max-instances=100 \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars=SERVICE_TYPE=auth,DATABASE_URL=$DATABASE_URL,JWT_SECRET_KEY=$JWT_SECRET_KEY \
  --allow-unauthenticated
```

#### Voices Service (Port 8002)

```bash
gcloud run deploy voice-narration-voices \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest \
  --platform=managed \
  --region=$REGION \
  --memory=2Gi \
  --cpu=2 \
  --timeout=3600 \
  --max-instances=50 \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars=SERVICE_TYPE=voices,DATABASE_URL=$DATABASE_URL,STORAGE_BUCKET=gs://voice-narration-voices \
  --allow-unauthenticated
```

#### TTS Service (Port 8003)

```bash
gcloud run deploy voice-narration-tts \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest \
  --platform=managed \
  --region=$REGION \
  --memory=2Gi \
  --cpu=2 \
  --timeout=3600 \
  --max-instances=100 \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars=SERVICE_TYPE=inference,DATABASE_URL=$DATABASE_URL,GOOGLE_TTS_API_KEY=$GOOGLE_TTS_API_KEY,STORAGE_BUCKET=gs://voice-narration-audio \
  --allow-unauthenticated
```

#### Evaluation Service (Port 8006)

```bash
gcloud run deploy voice-narration-eval \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest \
  --platform=managed \
  --region=$REGION \
  --memory=1Gi \
  --cpu=1 \
  --timeout=3600 \
  --max-instances=50 \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars=SERVICE_TYPE=audit,DATABASE_URL=$DATABASE_URL \
  --allow-unauthenticated
```

#### Jobs Service (Port 8007)

```bash
gcloud run deploy voice-narration-jobs \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest \
  --platform=managed \
  --region=$REGION \
  --memory=1Gi \
  --cpu=1 \
  --timeout=3600 \
  --max-instances=20 \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars=SERVICE_TYPE=jobs,DATABASE_URL=$DATABASE_URL \
  --allow-unauthenticated
```

### Deploy Frontend

```bash
gcloud run deploy voice-narration-frontend \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:latest \
  --platform=managed \
  --region=$REGION \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=50 \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars=VITE_API_URL=https://voice-narration-auth-xxxxx.run.app,VITE_ENV=production \
  --allow-unauthenticated
```

---

## Step 5: Setup Cloud Load Balancer

### Create Load Balancer

```bash
# Create backend service
gcloud compute backend-services create voice-narration-backend \
  --global \
  --protocol=HTTP2 \
  --load-balancing-scheme=EXTERNAL

# Create health check
gcloud compute health-checks create http voice-narration-health-check \
  --request-path=/health

# Add backend services to load balancer
gcloud compute backend-services add-backend voice-narration-backend \
  --instance-group=voice-narration-group \
  --global

# Create URL map
gcloud compute url-maps create voice-narration-lb \
  --default-service=voice-narration-backend

# Create HTTPS proxy
gcloud compute ssl-certificates create voice-narration-cert \
  --certificate=path/to/cert.crt \
  --private-key=path/to/private.key

gcloud compute target-https-proxies create voice-narration-https \
  --url-map=voice-narration-lb \
  --ssl-certificates=voice-narration-cert

# Create forwarding rule
gcloud compute forwarding-rules create voice-narration-https-lb \
  --global \
  --target-https-proxy=voice-narration-https \
  --address-region=$REGION \
  --ports=443
```

---

## Step 6: Setup Cloud Build CI/CD

### Create Cloud Build Configuration

Create `cloudbuild.yaml`:

```yaml
steps:
  # Build backend image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:$SHORT_SHA'
      - '-f'
      - 'Dockerfile'
      - '.'

  # Build frontend image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:$SHORT_SHA'
      - '-f'
      - 'Dockerfile.frontend'
      - './frontend'

  # Push backend image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:$SHORT_SHA'

  # Push frontend image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:$SHORT_SHA'

  # Deploy backend to Cloud Run
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=k8s/
      - --image=$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:$SHORT_SHA
      - --location=$_REGION

  # Deploy frontend to Cloud Run
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=k8s/
      - --image=$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:$SHORT_SHA
      - --location=$_REGION

images:
  - '$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:$SHORT_SHA'
  - '$_REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/frontend:$SHORT_SHA'

substitutions:
  _REGION: 'us-central1'

options:
  machineType: 'N1_HIGHCPU_8'
```

### Setup Cloud Build Trigger

```bash
# Connect GitHub repository
gcloud builds connect --name=voice-narration

# Create build trigger
gcloud builds triggers create github \
  --name=voice-narration-deploy \
  --repo-name=Voice-Narration \
  --repo-owner=avinash2196 \
  --branch-pattern=^main$ \
  --build-config=cloudbuild.yaml \
  --service-account=voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com
```

---

## Step 7: Configure Environment Variables

### Create Secret Manager Secrets

```bash
# Store sensitive variables in Secret Manager
echo -n "your_jwt_secret_key" | gcloud secrets create jwt-secret-key \
  --replication-policy="automatic" \
  --data-file=-

echo -n "your_database_password" | gcloud secrets create db-password \
  --replication-policy="automatic" \
  --data-file=-

echo -n "your_google_tts_key" | gcloud secrets create google-tts-key \
  --replication-policy="automatic" \
  --data-file=-

# Grant service account access
gcloud secrets add-iam-policy-binding jwt-secret-key \
  --member=serviceAccount:voice-narration-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

### Update Cloud Run Services with Secrets

```bash
# Update auth service with secret
gcloud run services update voice-narration-auth \
  --region=$REGION \
  --set-env-vars=JWT_SECRET_KEY=sm://jwt-secret-key
```

---

## Step 8: Setup Monitoring & Logging

### Create Monitoring Dashboard

```bash
# View Cloud Run metrics
gcloud monitoring dashboards create --config-from-file=dashboard.json
```

### Setup Cloud Logging

```bash
# View service logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Filter by service
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=voice-narration-auth" --limit 50

# Create log sink for archival
gcloud logging sinks create voice-narration-archive \
  gs://voice-narration-backups/logs \
  --log-filter='resource.type="cloud_run_revision"'
```

### Setup Alerting

```bash
# Create alert policy for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Voice Narration High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=5 \
  --condition-threshold-duration=60s
```

---

## Step 9: Setup Custom Domain

### Map Custom Domain

```bash
# Add Cloud Run service to load balancer
gcloud compute url-maps add-path-rule voice-narration-lb \
  --service=voice-narration-frontend \
  --path-matcher=frontend \
  --new-path-matcher=frontend

# Map custom domain
gcloud run domain-mappings create \
  --service=voice-narration-frontend \
  --domain=api.voice-narration.com \
  --region=$REGION

# Add DNS records (CNAME) pointing to Cloud Run
# api.voice-narration.com CNAME ghs.googleusercontent.com

# Enable SSL certificate
gcloud compute ssl-certificates create voice-narration-custom-cert \
  --domains=api.voice-narration.com \
  --global
```

---

## Step 10: Setup Database Backups

### Automated Backups

```bash
# Create backup schedule
gcloud sql backups create \
  --instance=voice-narration-db \
  --description="Automated backup"

# Enable automatic backups (backup window 2-3 AM UTC)
gcloud sql instances patch voice-narration-db \
  --backup-start-time=02:00 \
  --enable-bin-log
```

### Export Database

```bash
# Export database to Cloud Storage
gcloud sql export sql voice-narration-db \
  gs://voice-narration-backups/voice_narration-$(date +%Y%m%d).sql \
  --database=voice_narration
```

---

## Step 11: Testing Deployment

### Health Checks

```bash
# Test backend services
curl https://voice-narration-auth-xxxxx.run.app/health
curl https://voice-narration-voices-xxxxx.run.app/health
curl https://voice-narration-tts-xxxxx.run.app/health

# Test frontend
curl https://api.voice-narration.com
```

### Load Testing

```bash
# Install load testing tool
go install github.com/rakyll/hey@latest

# Run load test
hey -c 100 -n 10000 https://voice-narration-frontend-xxxxx.run.app
```

---

## Step 12: Scaling Configuration

### Auto-scaling Settings

```bash
# Update service auto-scaling
gcloud run services update voice-narration-tts \
  --region=$REGION \
  --min-instances=2 \
  --max-instances=100 \
  --memory=2Gi \
  --cpu=2 \
  --cpu-throttling
```

### Concurrency Settings

```bash
# Set max concurrent requests per instance
gcloud run services update voice-narration-api \
  --region=$REGION \
  --concurrency=80
```

---

## Deployment Verification Checklist

- [ ] Cloud SQL instance created and accessible
- [ ] Cloud Storage buckets created and configured
- [ ] Artifact Registry repository created
- [ ] Docker images built and pushed
- [ ] Cloud Run services deployed
- [ ] Load balancer configured
- [ ] SSL certificates installed
- [ ] Custom domain mapped
- [ ] Database backups scheduled
- [ ] Monitoring and logging configured
- [ ] Health checks passing
- [ ] Load tests completed successfully

---

## Post-Deployment Monitoring

### Key Metrics to Monitor

```bash
# CPU usage
gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/request_latencies"'

# Request count
gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/request_count"'

# Error rate
gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/request_latencies" AND metric.response_code_class="5xx"'
```

### Cost Optimization

```bash
# View GCP costs
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name=voice-narration-budget \
  --budget-amount=1000 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90

# Analyze Cloud Run costs
gcloud logging read "resource.type=cloud_run_revision" --format="csv(resource.labels.service_name,resource.labels.revision_name)" | uniq -c
```

---

## Quick Commands Reference

```bash
# View deployed services
gcloud run services list --region=$REGION

# View service logs
gcloud logging read "resource.labels.service_name=voice-narration-auth" --limit=50

# Update service
gcloud run services update SERVICE_NAME \
  --region=$REGION \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/voice-narration/backend:latest

# Delete service
gcloud run services delete SERVICE_NAME --region=$REGION

# View database status
gcloud sql instances describe voice-narration-db

# Backup database
gcloud sql backups create --instance=voice-narration-db

# List backups
gcloud sql backups list --instance=voice-narration-db
```

---

## Troubleshooting GCP Deployment

### Service Not Starting

```bash
# Check service logs
gcloud logging read "resource.labels.service_name=voice-narration-auth" --limit=100 --format=json

# Check image exists
gcloud artifacts docker images list $REGION-docker.pkg.dev/$PROJECT_ID/voice-narration
```

### Database Connection Issues

```bash
# Test Cloud SQL connection
gcloud sql connect voice-narration-db --user=postgres

# Check Cloud SQL Proxy status
ps aux | grep cloud_sql_proxy
```

### Load Balancer Issues

```bash
# Check backend status
gcloud compute backend-services get-health voice-narration-backend --global

# View load balancer configuration
gcloud compute forwarding-rules describe voice-narration-https-lb --global
```

---

**Last Updated**: November 1, 2024
**GCP Deployment Guide v1.0**
