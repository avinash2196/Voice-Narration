FROM python:3.13-slim

WORKDIR /app

COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r /app/requirements-dev.txt

COPY voice_narration /app/voice_narration

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn voice_narration.inference.application:app --host 0.0.0.0 --port ${PORT:-8080}"]
