"""Job orchestration, idempotency, quota enforcement and cost tracking."""
from copy import deepcopy
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from voice_narration._enrollment import Pages, owner, principal, query, serializer
from voice_narration._http import bearer, body, closed, install_errors, timestamp
from voice_narration._sql import PersistenceError, fail, identity, instant


STATES = {"pending", "processing", "complete", "failed", "cancelled"}


class AppState:
    """Job orchestration state manager."""
    
    def __init__(self, repository, quota_provider, cost_provider, clock):
        self.repository = repository
        self.quota_provider = quota_provider
        self.cost_provider = cost_provider
        self.clock = clock
        self._idempotency_cache = {}  # In-memory idempotency tracking for 60s TTL
    
    def _clean_idempotency_cache(self):
        """Remove expired entries (>60 seconds old)."""
        now = instant(self.clock())
        expired_keys = [
            key for key, (timestamp_dt, _) in self._idempotency_cache.items()
            if (now - timestamp_dt).total_seconds() > 60
        ]
        for key in expired_keys:
            del self._idempotency_cache[key]
    
    def submit_job(self, account, request_data):
        """Submit a job with idempotency key support."""
        closed(request_data, {"script_body", "profile_id", "model_id", "parameters", "idempotency_key"})
        
        who = owner(account)
        owner_id = who["user_id"]
        idempotency_key = request_data.get("idempotency_key")
        
        # Check idempotency cache
        self._clean_idempotency_cache()
        if idempotency_key:
            cache_key = f"{owner_id}:{idempotency_key}"
            if cache_key in self._idempotency_cache:
                cached_timestamp, job_id = self._idempotency_cache[cache_key]
                if (instant(self.clock()) - cached_timestamp).total_seconds() < 60:
                    # Return cached result with 200 OK (idempotent)
                    with self.repository.transaction():
                        record = self.repository.inspect_private(job_id)
                        if record:
                            return 200, deepcopy(record["payload"]["job"])
        
        # Check quotas before proceeding
        limits = self.quota_provider.get_limits(account)
        current = self.quota_provider.current_usage(account)
        
        # Check concurrent jobs
        if current["concurrent_jobs"] >= limits["max_concurrent_jobs"]:
            fail("QUOTA_EXCEEDED")
        
        # Estimate cost and check budget
        script_body = request_data.get("script_body", "")
        generation_seconds = max(len(script_body) // 100, 1)  # Synthetic: ~1s per 100 chars
        estimated_cost = self.cost_provider("generation_seconds", generation_seconds)
        
        if current["cost_this_month"] + estimated_cost > limits["max_cost_per_month"]:
            fail("PAYMENT_REQUIRED")
        
        # Check generation seconds per month
        if current["generation_seconds_this_month"] + generation_seconds > limits["max_generation_seconds_per_month"]:
            fail("QUOTA_EXCEEDED")
        
        # Create job record
        job_id = str(uuid4())
        now = instant(self.clock())
        
        job = {
            "id": job_id,
            "owner_id": owner_id,
            "profile_id": identity(request_data["profile_id"]),
            "model_id": request_data["model_id"],
            "script_body": script_body,
            "parameters": request_data.get("parameters", {}),
            "state": "pending",
            "attempt": 0,
            "created_at": timestamp(now),
            "started_at": None,
            "completed_at": None,
            "output": None,
            "error": None,
            "estimated_cost": float(estimated_cost),
            "actual_cost": 0.0,
            "retry_count": 0,
            "idempotency_key": idempotency_key,
        }
        
        # Persist to repository
        self.repository.save({
            "id": job_id,
            "owner_id": owner_id,
            "profile_id": request_data["profile_id"],
            "consent_id": request_data.get("consent_id", "00000000-0000-0000-0000-000000000000"),
            "category": "job",
            "created_at": now,
            "payload": {"job": job}
        })
        
        # Cache idempotency key
        if idempotency_key:
            cache_key = f"{owner_id}:{idempotency_key}"
            self._idempotency_cache[cache_key] = (now, job_id)
        
        return 201, deepcopy(job)
    
    def run_pending_jobs(self):
        """Worker seam: deterministic processing of pending jobs."""
        # This is a deterministic seam for testing
        # In production, this would be called by an async background worker
        pass
    
    def job_history(self, account, job_id):
        """Retrieve full job history with attempt details."""
        who = owner(account)
        
        with self.repository.transaction():
            record = self.repository.inspect_private(identity(job_id))
            if record is None or record["category"] != "job":
                fail("NOT_FOUND")
            
            job = record["payload"]["job"]
            if job["owner_id"] != who["user_id"]:
                fail("FORBIDDEN")
            
            return deepcopy(job)
    
    def estimate_cost(self, account, request_data):
        """Estimate cost for a job without submitting."""
        closed(request_data, {"script_body", "profile_id", "model_id", "parameters"})
        
        script_body = request_data.get("script_body", "")
        generation_seconds = max(len(script_body) // 100, 1)
        
        generation_cost = self.cost_provider("generation_seconds", generation_seconds)
        storage_cost = self.cost_provider("storage_days", 30)  # Assume 30-day retention
        retry_cost = self.cost_provider("retries", 0)  # No retries yet
        bandwidth_cost = self.cost_provider("bandwidth_mb", 0)  # No bandwidth yet
        
        total = generation_cost + storage_cost + retry_cost + bandwidth_cost
        
        return {
            "generation_seconds": generation_seconds,
            "generation_cost": float(generation_cost),
            "storage_days": 30,
            "storage_cost": float(storage_cost),
            "retry_attempts": 0,
            "retry_cost": float(retry_cost),
            "bandwidth_mb": 0,
            "bandwidth_cost": float(bandwidth_cost),
            "total_cost": float(total),
            "currency": "USD"
        }
    
    def get_quotas(self, account):
        """Get current quota limits and usage."""
        return {
            "limits": self.quota_provider.get_limits(account),
            "current_usage": self.quota_provider.current_usage(account)
        }
    
    def list_jobs(self, account, parameters):
        """List jobs for authenticated owner."""
        who = principal(account)
        reader = owner(account)
        target = parameters.get("owner_id", who["user_id"])
        
        if "owner_id" in parameters:
            identity(target)
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
        
        def records():
            with self.repository.transaction():
                rows = self.repository.list(reader, owner_id=target, now=instant(self.clock()))
                jobs = [row["payload"]["job"] for row in rows if row["category"] == "job"]
                return sorted(jobs, key=lambda j: (j["created_at"], j["id"]), reverse=True)
        
        # Pagination would go here
        return {
            "items": records(),
            "total": len(records()),
            "limit": parameters.get("limit", 50),
            "offset": parameters.get("offset", 0)
        }
    
    def set_quota_override(self, account, target_owner_id, quotas):
        """Admin endpoint: set per-user quota overrides."""
        who = principal(account)
        if who["role"] != "Administrator":
            fail("FORBIDDEN")
        
        identity(target_owner_id)
        
        # In production, this would persist to a quota_overrides table
        # For tests, we store in memory on the quota provider
        if not hasattr(self.quota_provider, "overrides"):
            self.quota_provider.overrides = {}
        
        self.quota_provider.overrides[target_owner_id] = quotas
        return quotas
    
    def close(self):
        """Cleanup resources."""
        pass


def create_app(*, repository, authenticate, validate_consent, artifacts, voices, capability,
               policy_snapshot, quota_provider, cost_provider, clock):
    """Create FastAPI app for job orchestration."""
    
    if not all(callable(value) for value in (authenticate, validate_consent, capability,
                                             policy_snapshot, clock)):
        fail("INVALID_CONFIGURATION")
    if quota_provider is None or cost_provider is None:
        fail("INVALID_CONFIGURATION")
    
    serialized = serializer()
    state = AppState(repository, quota_provider, cost_provider, clock)
    pages = Pages(None)  # Will be configured with pagination settings
    
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)
    
    @serialized
    def submit_job_handler(account, value):
        status_code, job = state.submit_job(account, value)
        return (status_code, job)
    
    @serialized
    def estimate_cost_handler(account, value):
        return state.estimate_cost(account, value)
    
    @serialized
    def get_quotas_handler(account):
        return state.get_quotas(account)
    
    @serialized
    def list_jobs_handler(account, parameters):
        return state.list_jobs(account, parameters)
    
    @serialized
    def get_job_handler(account, job_id):
        return state.job_history(account, job_id)
    
    @serialized
    def set_quota_handler(account, target_owner_id, value):
        return state.set_quota_override(account, target_owner_id, value)
    
    @app.post("/api/v1/jobs/submit")
    async def submit(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        try:
            status_code, job = await run_in_threadpool(submit_job_handler, account, value)
            return JSONResponse(status_code=status_code, content=job)
        except PersistenceError as exc:
            if exc.code == "QUOTA_EXCEEDED":
                return JSONResponse(status_code=429, content={"error": exc.code})
            elif exc.code == "PAYMENT_REQUIRED":
                return JSONResponse(status_code=402, content={"error": exc.code})
            raise
    
    @app.get("/api/v1/jobs")
    async def list_jobs(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        parameters = query(request, {"cursor", "limit", "owner_id", "state"})
        jobs_page = await run_in_threadpool(list_jobs_handler, account, parameters)
        return jobs_page
    
    @app.get("/api/v1/jobs/{job_id}")
    async def get_job(request: Request, job_id: str):
        account = await run_in_threadpool(authenticate, bearer(request))
        job = await run_in_threadpool(get_job_handler, account, job_id)
        return job
    
    @app.get("/api/v1/cost/estimate")
    async def estimate_cost(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        cost_estimate = await run_in_threadpool(estimate_cost_handler, account, value)
        return cost_estimate
    
    @app.get("/api/v1/config/quotas")
    async def get_quotas(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        quotas = await run_in_threadpool(get_quotas_handler, account)
        return quotas
    
    @app.put("/api/v1/config/quotas/{account_id}")
    async def set_quotas(request: Request, account_id: str):
        admin_account = await run_in_threadpool(authenticate, bearer(request))
        value = await body(request)
        quotas = await run_in_threadpool(set_quota_handler, admin_account, account_id, value)
        return JSONResponse(status_code=200, content=quotas)
    
    app.state = state
    return app
