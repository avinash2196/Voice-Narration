# Developer prerequisites

Use CPython 3.13.17 x64, Docker Linux engine and Compose 5.6.0.
Obtain Python from https://www.python.org/downloads/release/python-31317/
(Windows 64-bit installer) and Docker from docker.com.
Do not use another project's virtual environment. No CUDA or paid cloud is needed.
This special security release includes Windows installers. The Windows launcher
must report this exact runtime before continuing.

Run from the repository root in PowerShell on Windows:

    py -3.13 -c "import sys; assert sys.version_info[:3] == (3,13,17)"
    py -3.13 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
    .\.venv\Scripts\python.exe -m pip check
    .\.venv\Scripts\python.exe -m playwright install chromium
    docker compose version
    docker info
    docker build -f containers/harness.Dockerfile -t vn-harness:foundation .
    docker run --rm vn-harness:foundation
    .\.venv\Scripts\python.exe tools/readiness.py
    .\.venv\Scripts\python.exe -m pip freeze

On Linux with CPython 3.13.17 and Docker/Compose installed:

    python3.13 -m venv .venv
    .venv/bin/python -m pip install -r requirements-dev.txt
    .venv/bin/python -m pip check
    .venv/bin/python -m playwright install --with-deps chromium
    docker build -f containers/harness.Dockerfile -t vn-harness:foundation .
    docker run --rm vn-harness:foundation
    .venv/bin/python tools/readiness.py
    .venv/bin/python -m pip freeze

The readiness command runs two rounds against the same isolated temporary
PostgreSQL container and filesystem root without cleaning between rounds, then
removes both. It allocates loopback ports and synthetic audio, starts and stops
its own HTTP server and browser, and creates no application/domain schema.
An interrupted run prints its container ID/project label before probing; inspect
that container's com.docker.compose.project label and remove only that project's
resources. Never clean a shared development database or unrelated containers.

Future RED commands, once approved tests exist:

    .\.venv\Scripts\python.exe -m pytest tests -ra
    .\.venv\Scripts\python.exe -m pytest tests -ra

Use the corresponding .venv/bin/python on Linux. Never convert pytest exit 5
(no tests collected) to success. FOUNDATION uses runner availability checks;
it does not claim an empty suite passed.

Later service entry points use `python -m` or `python -m uvicorn` with modules
named by approved GREEN plans, separate processes for the nine services, and
loopback-only dynamically allocated local ports. This foundation creates no
entry points. Browser UI uses native HTML/CSS/ES modules, served locally by
the service/static server selected in the frontend GREEN plan; no npm build
is required. Later test code can launch its own stdlib static server.

RED test-isolation convention: use pytest tmp_path for files and unique owner
databases/credentials in a per-run PostgreSQL container, verify current_database,
current_user, effective paths and runtime configuration, and never share state
across cases. Later test code owns fixtures and may create scratch schema only
as test code. GREEN owns domain schema, migrations, durable queue/outbox logic,
artifact storage adapters and service bootstraps. Tests may use stdlib mocks
for boundaries, but mocks must not supply the behavior being proved.

Use HTTPX for in-process ASGI and real loopback/network contract checks; verify
contract error responses through real transport. Python TLS contexts/HTTPX keep
certificate validation enabled for supplied deployed HTTPS environments.
No deployed credentials, URLs or provider resources are supplied by this harness.
Security RED may inspect user-supplied configuration and use isolated transport
fixtures; deployed encryption/IAM/managed-secret acceptance requires later
supplied deployment evidence. Local checks never establish deployed acceptance.

Use Playwright Python's Chromium for browser tests with synthetic microphone
input. Real device usability/listening remains human acceptance. NumPy/PyAV
provide signal and WAV/MP3/M4A tools; use synthetic fixtures until approved
consented corpus input exists. Codec availability is not commercial licensing
approval or narration quality. Do not acquire model weights here. The approved
model prerequisite milestone supplies selected model runtime/assets later.
