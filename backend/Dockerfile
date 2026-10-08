# =============================================================================
# STAGE 1: Builder (Compiles & installs dependencies into virtual environment)
# =============================================================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create isolated virtualenv for easy transfer
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/requirements.txt /build/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: Runner (Lean production runtime environment)
# =============================================================================
FROM python:3.11-slim AS runner

# Security: Create non-root user
RUN groupadd -g 10001 cropfit && \
    useradd -u 10001 -g cropfit -m -s /bin/bash appuser

# Set runtime environment flags
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DISABLE_SQLALCHEMY_CEXT=1 \
    PATH="/opt/venv/bin:$PATH" \
    DATABASE_URL="sqlite:////app/data/cropfit.db" \
    MODELS_DIR="/app/ml_experiments/models"

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create persistent data directory and assign ownership
RUN mkdir -p /app/data && chown -R appuser:cropfit /app

# Copy application source code
COPY --chown=appuser:cropfit backend/app /app/backend/app
COPY --chown=appuser:cropfit pyproject.toml /app/backend/pyproject.toml

# Copy serialized Machine Learning and Computer Vision models
COPY --chown=appuser:cropfit ml_experiments/models /app/ml_experiments/models

# Switch to non-root user
USER appuser

# Working directory where Python can resolve backend packages
WORKDIR /app/backend

# Container health check testing /api/v1/health
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/api/v1/health').getcode() == 200 else 1)"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
