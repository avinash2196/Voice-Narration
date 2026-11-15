"""Public Auth boundary with explicit owner-local dependencies."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from voice_narration._http import bearer, body, install_errors
from voice_narration._sql import fail
from voice_narration.auth.accounts import Accounts


def create_app(*, database, root, auth_settings, clock, send_verification, administrator):
    if not callable(clock) or not callable(send_verification):
        fail("INVALID_CONFIGURATION")
    accounts = Accounts(database=database, root=root, settings=auth_settings, clock=clock)
    try:
        accounts.initialize()
        accounts.bootstrap(administrator)
    except Exception:
        accounts.close()
        raise
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)
    app.state.effective_target = accounts.effective_target
    app.state.effective_auth_settings = lambda: dict(accounts.settings)
    app.state.verify_token = accounts.verify_token
    app.state.close = accounts.close

    @app.post("/api/v1/auth/register")
    async def register(request: Request):
        value = await body(request)
        await run_in_threadpool(accounts.register, value, send_verification)
        return JSONResponse(status_code=202, content={"verification_required": True})

    @app.post("/api/v1/auth/verify-email")
    async def verify_email(request: Request):
        value = await body(request)
        return await run_in_threadpool(accounts.verify_email, value)

    @app.post("/api/v1/auth/login")
    async def login(request: Request):
        value = await body(request)
        return await run_in_threadpool(accounts.login, value)

    @app.get("/api/v1/auth/me")
    def me(request: Request):
        return accounts.verify_token(bearer(request))

    return app
