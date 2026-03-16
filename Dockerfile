# Multi-stage Dockerfile for Healthcare Planning Assistant

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app ./app
COPY .env.example ./env.template

EXPOSE 8000

# Healthcheck hitting FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import sys,urllib.request; \
import os; \
url=f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/health'; \
sys.exit(0 if urllib.request.urlopen(url).getcode()==200 else 1)" || exit 1

ENV PORT=8000

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

