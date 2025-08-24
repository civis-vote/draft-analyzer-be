FROM python:3.13-slim AS base

# System deps for WeasyPrint & Cairo
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libffi-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

# Copy only dependency files first (caches layers)
COPY pyproject.toml uv.lock ./

# Install only runtime deps (skip dev/test)
RUN uv sync --frozen --no-dev

# Copy application source
COPY src ./src

# Copy templates
COPY templates templates

# Ensure src is in PYTHONPATH
ENV PYTHONPATH=/app/src

# Default run command
CMD ["uv", "run", "uvicorn", "civis_backend_policy_analyser.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

