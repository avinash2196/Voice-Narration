FROM python:3.13.17-slim-trixie
WORKDIR /workspace
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements-dev.txt
CMD ["python", "-c", "import fastapi,uvicorn,pytest,httpx,psycopg,numpy,av,playwright; print('dependency image ready')"]
