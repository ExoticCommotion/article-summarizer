# 🧱 Project Layout Overview

This repository follows a scalable layout that supports CLI tools, backend agents, and optional frontend interfaces.

```
src/
├── backend/
│   └── app/
│       ├── cli/             # Typer-based CLI commands
│       ├── custom_agents/   # Agent classes or flows
│       ├── utils/           # Shared utilities, loggers, adapters
│       └── main.py          # API or CLI entrypoint
│
│   └── tests/
│       ├── cli/             # CLI integration or validation
│       ├── integration/     # Flow-level or end-to-end tests
│       ├── unit/            # Pure logic tests
│       └── conftest.py      # Fixtures for all test layers
│
├── frontend/                # Optional client code
├── scripts/                 # Setup utilities
├── docs/knowledge_base/     # Living guidance for agents and contributors
└── .devcontainer/           # VS Code remote config
```

## ✅ Layout Goals

-   Clear entrypoints (`main.py`, `cli.py`)
-   Distinct separation of responsibilities (logic, glue, tests, interface)
-   Expandable without fragmentation

## 🔁 When You Should Modify Layout

-   Adding a major subsystem? Create a folder under `app/` or `custom_agents/`
-   Need to share logic across flows? Place in `utils/`
-   Writing CLI utilities? Extend `cli.py` and test in `tests/cli/`

Use existing structure unless you can justify an improvement.
