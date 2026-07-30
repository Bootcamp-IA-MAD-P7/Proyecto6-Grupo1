FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home appuser

# Copy dependency files first (better layer caching)
COPY pyproject.toml /app/

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pydantic \
    pydantic-settings \
    httpx \
    joblib \
    scikit-learn \
    numpy \
    optuna \
    xgboost \
    lightgbm \
    matplotlib \
    psycopg2-binary \
    PyJWT

# Copy application code
COPY app/api/ /app/app/api/
COPY src/ml/ /app/src/ml/
COPY src/__init__.py /app/src/__init__.py

# Copy model artifact (if available at build time)
COPY models/cfpb_baseline.pkl /app/models/cfpb_baseline.pkl

# Copy config (needed for canonical classes)
COPY config/cfpb_target_contract.json /app/config/cfpb_target_contract.json

# Switch to non-root user
USER appuser

# Environment
ENV APP_MODEL_PATH=/app/models/cfpb_baseline.pkl
ENV APP_SERVICE_VERSION=0.1.0
ENV PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
