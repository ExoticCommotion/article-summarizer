# Unified Python app tooling using uv
# Project: Devin Template

# ✅ Use src as the root of truth
export PYTHONPATH := src
EXCLUDES := --exclude reference_projects

# Default branch to compare against
BASE_BRANCH := main

.PHONY: setup sync sync-dev format lint typecheck test coverage \
        test-unit test-integration test-cli \
        snapshots-fix snapshots-create \
        build-docs build-full-docs serve-docs deploy-docs \
        check clean reset help dev sanity \
		unhook-precommit verify get-pr-diff

# ========== 👶 Zero-Onboarding Setup ==========
setup:  ## One-command project bootstrap: installs uv, creates .venv, syncs dev deps
	pip install --upgrade pip uv
	uv venv .venv
	source .venv/bin/activate && make sync-dev

# ========== 🔁 Dependency Management ==========
sync:
	uv sync --all-extras

sync-dev:  ## Sync all deps including dev tools
	uv sync --all-extras --all-packages --group dev

# ========== 💄 Code Quality ==========
format:  ## Format and fix code with Ruff
	uv run ruff format src $(EXCLUDES)
	uv run ruff check src $(EXCLUDES) --fix

lint:  ## Lint code (no fixing)
	uv run ruff check src $(EXCLUDES)

typecheck:  ## Type check with mypy
	uv run mypy src --config-file pyproject.toml

# ========== ✅ Tests ==========
test:  ## Run all tests with pytest
	uv run pytest src

test-unit:  ## Run only unit tests
	uv run pytest src/backend/tests/unit

test-integration:  ## Run only integration tests
	uv run pytest src/backend/tests/integration

test-cli:  ## Run CLI-level tests
	uv run pytest src/backend/tests/cli

verify:  ## Run full pre-commit suite for local validation
	uv run pre-commit run --all-files

# ========== 📈 Coverage & Snapshots ==========
coverage:  ## Run coverage and fail if <60%
	uv run coverage run -m pytest
	uv run coverage xml -o coverage.xml
	uv run coverage report -m --fail-under=60

# ========== 🧪 Combined Dev Check ==========
check: format lint typecheck coverage  ## Run all quality checks (use before commit)


snapshots-fix:  ## Fix failing inline snapshots
	uv run pytest --inline-snapshot=fix

snapshots-create:  ## Create initial inline snapshots
	uv run pytest --inline-snapshot=create

restore:
	make clean
	uv run scripts/dev-setup.bat
	make check

unhook-precommit:  ## Remove pre-commit hook as a last resort
	pre-commit uninstall
	rm -f .git/hooks/pre-commit

# ========== 📘 Docs ==========
build-docs:  ## Build documentation site
	uv run mkdocs build

build-full-docs:  ## Build full docs (with i18n translation)
	uv run docs/scripts/translate_docs.py
	uv run mkdocs build

serve-docs:  ## Serve docs locally
	uv run mkdocs serve

deploy-docs:  ## Deploy docs to GitHub Pages
	uv run mkdocs gh-deploy --force --verbose

# ========== 🧪 Combined Dev Check ==========
dev: check  ## Alias for day-to-day dev check

# ========== 🧹 Cleanup ==========
clean:  ## Delete caches and lockfile
	rm -rf .venv .ruff_cache .mypy_cache .pytest_cache __pycache__ uv.lock

reset: clean setup  ## Wipe everything and reinitialize

# ========== 📘 Help ==========
help:  ## Show available make commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

sanity:
	uv run python -m src.backend.agent_hello_world


# Default target PR branch, can be overridden from the command line
# Example: make get-pr-diff TARGET_BRANCH_NAME=another/feature-branch
TARGET_BRANCH_NAME ?= devin/1747167891-implement-feedback-synthesizer

# --- Helper variables (still useful for clarity and minor customization) ---
REMOTE_TARGET_BRANCH := origin/$(TARGET_BRANCH_NAME)
FILENAME_TAG := $(shell echo $(TARGET_BRANCH_NAME) | sed 's|/|-|g') # Sanitize for filename
OUTPUT_DIR := outputs
DIFF_FILE := $(OUTPUT_DIR)/pr_diff_$(FILENAME_TAG).txt

# Save PR diff to outputs/<pr>-<timestamp>.patch
# Usage: make pr-diff PR=devin-1747167891-implement-feedback-synthesizer
pr-diff:
	scripts/generate_pr_diffs.sh


e2e:
	uv run python -m src.backend.app.cli summarize https://en.wikipedia.org/wiki/AI_safety

cb:
	@if [ -z "$(BRANCH)" ]; then \
		echo "❌ Please provide BRANCH=<remote-branch-name>"; \
		exit 1; \
	fi
	@LOCAL=$$(echo $(BRANCH) | tr '/' '-'); \
	echo "📥 Fetching from origin/$(BRANCH)..."; \
	git fetch origin $(BRANCH) && \
	echo "🌿 Creating and switching to local branch $$LOCAL..." && \
	git checkout -b $$LOCAL origin/$(BRANCH)