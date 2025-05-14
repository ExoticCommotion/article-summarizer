# 🧠 Devin Agent Template Project

This is a **template repository** for building intelligent agent applications using Python, `uv`, and a fully structured development and quality assurance pipeline.

It provides a ready-to-use scaffold for:

-   🧩 Agent-based backends (`src/backend/app`)
-   🌐 Optional frontends (`src/frontend`)
-   🧪 Integrated testing, linting, typing, and formatting (`pytest`, `ruff`, `mypy`, `pre-commit`)
-   ⚙️ Zero-onboarding setup scripts for fast developer ramp-up

---

## 📁 Project Structure

```txt
.
├── src/
│   ├── backend/
│   │   └── app/
│   │       ├── custom_agents/   # (Optional) Agent logic lives here
│   │       ├── utils/           # Utilities and shared helpers
│   │       ├── cli/             # CLI-based test interfaces
│   │       ├── main.py          # Entrypoint (FastAPI app, CLI tool, etc.)
│   │       └── tests/           # Unit, integration, and CLI tests
│   └── frontend/                # Optional frontend implementation
├── scripts/                     # Bootstrap and utility scripts
├── .devcontainer/               # Devcontainer configs for VS Code or GitHub Codespaces
├── docs/                        # MkDocs documentation
├── outputs/                     # Output artifacts (e.g. TTS, summaries)
├── logs/                        # Logging directory (excluded from version control)
```

---

## 🧰 Built-in Features

-   ✅ `uv` for dependency and environment management
-   ✅ `ruff` for linting + formatting
-   ✅ `mypy` for static type checking
-   ✅ `pytest` with support for `asyncio`, `mock`, and `snapshots`
-   ✅ Git `pre-commit` hooks for hygiene enforcement
-   ✅ CLI testing support out-of-the-box
-   ✅ Cross-platform setup scripts (`.sh`, `.bat`, `.ps1`)
-   ✅ VS Code tasks and launch/debug configs
-   ✅ Optional DevContainer support for reproducible environments

---

# Custom [TEMPLATE] Project instructions:

## 🔍 Agent Patterns Supported

This template supports common intelligent agent patterns:

1. **Single-agent workflows**
2. **Function-calling agents**
3. **Tool-using or self-calling agents**
4. **Multi-agent routing and delegation**
5. **Voice or audio-enabled agents (TTS + ASR)**

You can organize agents under:

```bash
src/backend/app/custom_agents/
```

> 🧠 Use this directory to implement reusable, composable agent logic.

---

## 🚀 Getting Started

For setup instructions and usage walkthroughs, see the [Setup Guide](./SETUP.md).

> Includes one-command bootstrapping for macOS, Linux, and Windows.

---

## IMPORTANT (Especially for Devin!)

-   To validate every changeset run "make check" and "make verify"
-   When you establish relevant knew "knowledge" be sure to reflect that as a change in the doc/knowledge_base as well
-   ✅ Use `make check` to validate all commands (lint, type check, coverage)
-   ✅ Use `make verify` to validate for a commit (runs pre commit)
-   ✅ Use `make test` to run just tests
-   ❌ Use `make unhook-precommit` if you really really cannot get around it and need to commit
-   ❌ Make changes to `reference_projects` subdirectory. This is there for your own reference, not to be touched!

## 🧪 Tests & Code Quality

Run tests and static checks:

```bash
make test         # Run all tests
make lint         # Lint code with ruff
make typecheck    # Static type check with mypy
make coverage     # Run coverage
make check        # Run all QA (coverage + lint + typecheck)
```

Includes:

-   ✅ Full pytest discovery in CLI + VS Code
-   ✅ Pre-commit hooks to block bad commits
-   ✅ Optional snapshot and coverage utilities

---

## 🧩 Extending This Template

Clone this repo to get started on your own project:

```bash
git clone https://github.com/your-org/devin-template.git devin-templatep
cd devin-template
make reset  # Clean start with .venv and all dependencies
```

You can easily rename, reconfigure `src/backend/app/`, and evolve the test scaffold as needed.

---

## 📄 License

This template is licensed under the [MIT License](./LICENSE).

---

### 💡 Tip for Devin Users

If you're assigning tasks to a Devin agent, use GitHub Issues or a ticket system (e.g. Jira), and structure your task prompts clearly. Avoid auto-closing issues prematurely—opt for manual validation or review workflows instead.
