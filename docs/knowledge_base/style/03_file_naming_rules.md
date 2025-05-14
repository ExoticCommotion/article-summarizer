# 🏷️ File Naming Rules

Consistent naming makes it easier for agents and humans to navigate and locate logic.

## 🐍 General Rules

-   Use `snake_case` for all Python files
-   Avoid acronyms unless industry standard
-   Be descriptive but concise

✅ Examples:

```
cli_test.py
json_utils.py
audio_converter.py
```

❌ Avoid:

```
CLI.py
JSONHelper.py
convert.py
```

## 🧪 Tests

Test file names should reflect what they test.

-   `test_math_utils.py` → unit test for `math_utils.py`
-   `test_agent_summary.py` → integration test for summary agent

## 🧰 Utilities

If a file is shared across multiple agents:

-   Use a clear noun phrase: `text_cleaner.py`
-   Don't prefix with `util_` — use the domain name instead

## 🚀 CLI / Entrypoints

-   CLI root = `cli.py`
-   CLI tests = `tests/cli/cli_test.py`

## 🧩 Modules

If a folder is a module, include an `__init__.py` and use a descriptive name (e.g., `tools/`, `custom_agents/`)
