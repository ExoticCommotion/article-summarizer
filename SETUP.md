# 🛠️ Project Template - Developer Setup Guide

This guide explains how to get started with a structured Python project that uses:

-   `uv` for dependency management
-   `pre-commit` for code quality
-   `pytest`, `mypy`, `ruff` for testing and linting
-   A standardized `src/backend/app` and `src/frontend` layout

---

## ✅ Prerequisites

-   Python **3.10 or 3.11** (recommended)
-   Git
-   (Optional) [`pyenv`](https://github.com/pyenv/pyenv) to manage Python versions

---

## 🚀 Zero-Onboarding Setup

The quickest way to bootstrap the full environment is:

### 🐧 Linux / macOS

```bash
bash scripts/dev-setup.sh
```

### 🔧 Commit as last resort

If you cannot get past the precommit stage despite trying, temporarily disable with this command.

```bash
make unhook-precommit
```
