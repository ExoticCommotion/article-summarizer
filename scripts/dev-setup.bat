@echo off
echo 🛠️ Setting up Windows development environment...

REM Install uv if missing
where uv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing uv...
    python -m pip install --upgrade pip
    pip install uv
)

set PYTHONPATH=src
echo PYTHONPATH set to: %PYTHONPATH%

REM Create virtual environment with uv
IF NOT EXIST ".venv" (
    echo 🐍 Creating virtual environment with uv...
    uv venv .venv
)

call .venv\Scripts\activate

REM Sync dependencies using uv
echo 📦 Syncing dependencies...
uv sync --all-extras --all-packages --group dev

@REM Install pre-commit hooks
@REM echo ✅ Installing pre-commit hooks...
@REM uv run pre-commit install

echo 🚀 Environment ready. You can now run:
echo    uv run pytest
