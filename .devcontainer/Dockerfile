# Base image with Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/root/.cache/uv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (universal Python toolchain)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create working directory
WORKDIR /workspace

# Copy project files (can be filtered with .dockerignore)
COPY . .

# Set up Python environment inside container
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv sync --all-extras --all-packages --group dev && \
    uv run pre-commit install

# Default command
CMD [ "uv", "run", "pytest" ]
