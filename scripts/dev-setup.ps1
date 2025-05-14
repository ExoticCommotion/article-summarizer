Write-Host "🛠️ Setting up Windows development environment..."

# Install uv if not found
if (-Not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing uv..."
    python -m pip install --upgrade pip
    pip install uv
}

# Create virtual environment with uv
if (-Not (Test-Path ".venv")) {
    Write-Host "🐍 Creating virtual environment..."
    uv venv .venv
}

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Sync dependencies
Write-Host "📦 Syncing dependencies..."
uv sync --all-extras --all-packages --group dev

# Install pre-commit hooks
# Write-Host "✅ Installing pre-commit hooks..."
# uv run pre-commit install

Write-Host "`n🚀 Environment ready. You can now run:"
Write-Host "   uv run pytest"
