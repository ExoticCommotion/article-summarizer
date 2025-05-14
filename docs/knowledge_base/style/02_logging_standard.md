# 📋 Logging Standards

Logging helps us debug, trace, and understand what agents are doing in development and production.

## ✅ Use Our Standard Logger

Use `get_logger(__name__)` from our shared logger utility:

```python
from backend.app.utils.logger import get_logger
logger = get_logger(__name__)
```

## 🧠 Logging Levels

| Level      | Use Case                               |
| ---------- | -------------------------------------- |
| `debug`    | Internal computations, loops, branches |
| `info`     | High-level flow updates                |
| `warning`  | Unexpected but handled states          |
| `error`    | Recoverable issues                     |
| `critical` | Unrecoverable errors (used rarely)     |

## ✅ Good Examples

```python
logger.info("⏳ Starting summarization task...")
logger.debug(f"Prompt payload: {payload}")
logger.error("Failed to parse output from agent")
```

## ❌ Avoid

-   Using `print()` unless in CLI tools
-   Logging secrets or tokens
-   Logging in tight loops without `debug`

## 📦 Where to Log

-   Log **start/end** of functions with important effects
-   Log **error branches** and fallback decisions
-   Log **command-line entrypoints**

## 🧪 Tests and Logs

Use log capture in tests when validating behavior:

```python
caplog.set_level("INFO")
assert "Starting summarization task" in caplog.text
```
