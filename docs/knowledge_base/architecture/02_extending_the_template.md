# 🧩 Extending the Devin Template

This template is built to scale—but extensions must follow structure and quality practices.

## 🧱 When to Add a New Module

You should create a new module when:

-   Logic is clearly separate from existing features
-   The concern is reusable (e.g., formatting, validation)
-   The logic is a first-class concept (not glue)

Example:

```
src/backend/app/agents/calendar_agent/
```

## 🧪 When to Add a New Test Suite

Split out a new test file when:

-   The logic has branching behavior
-   Tests exceed 30 lines or span multiple test cases
-   You’re testing a different layer (e.g., CLI vs pure logic)

Use `unit/` for small logic, `integration/` for flows, and `cli/` for tooling validation.

## 🛠️ Adding a CLI Tool

1. Add a function to `cli.py` using `@app.command()`
2. Include minimal argument parsing and logging
3. Test it in `tests/cli/` with sample calls and expected behavior

```python
@app.command()
def ping(msg: str = "pong"):
    print(f"Ping received: {msg}")
```

## 🧩 When to Add New Utilities

Create files under `utils/` only if:

-   Logic will be reused
-   It has zero domain specificity
-   It improves clarity and reduces duplication

Don’t put domain logic (e.g., "email cleaner") in `utils/`. Create a module for it.
