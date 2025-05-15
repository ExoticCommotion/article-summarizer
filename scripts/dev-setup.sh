#!/usr/bin/env bash
set -e

echo "🛠️ Setting up Python development environment..."

# Install uv if not available
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    pip install uv
fi

export PYTHONPATH=src
echo "PYTHONPATH set to: $PYTHONPATH"

# Create and activate uv virtual environment
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment with uv..."
    uv venv .venv
fi

source .venv/bin/activate

# Sync all dependencies (dev + extras)
echo "📦 Syncing dependencies..."
uv sync --all-extras --all-packages --group dev

# Install pre-commit hooks
# echo "✅ Installing pre-commit hooks..."
# uv run pre-commit install

echo "🚀 Environment setup complete! You can now run:"
echo "   uv run pytest"
