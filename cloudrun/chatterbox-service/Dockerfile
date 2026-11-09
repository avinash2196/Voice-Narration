FROM python:3.11-slim

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
