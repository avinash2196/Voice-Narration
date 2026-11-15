FROM python:3.13.17-slim-trixie
WORKDIR /workspace
COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY requirements-evaluator.txt /tmp/requirements-evaluator.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements-dev.txt
RUN python -m pip install --no-cache-dir --no-deps --only-binary=:all: --require-hashes -r /tmp/requirements-evaluator.txt
CMD ["python", "-c", "import fastapi,uvicorn,pytest,httpx,psycopg,numpy,av,playwright,webrtcvad,_webrtcvad; print('dependency image ready')"]
