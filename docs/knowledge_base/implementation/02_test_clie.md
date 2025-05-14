# 🧪 CLI Testing

Command-line tools should be easy to verify and test. Our framework supports lightweight, direct CLI tests.

## 📂 File Structure

Place CLI tests in:

```
src/backend/tests/cli/
├── __init__.py
├── cli_test.py
```

## 🧠 How to Write

Use `subprocess`, `click.testing`, or directly invoke the `main()` function.

**Example using direct call:**

```python
from backend.app.cli import app
from typer.testing import CliRunner

runner = CliRunner()

def test_example_cli() -> None:
    result = runner.invoke(app, ["--example", "hello"])
    assert result.exit_code == 0
    assert "hello" in result.stdout
```

## ✅ Coverage & Logging

CLI tools should:

-   Use clear `logger.info()` or `rich.print()`
-   Have visible outputs (not just side effects)
-   Be tested via input args and expected outputs

## 🔍 What Not to Do

-   Don’t rely on `print()` for test output
-   Avoid heavy logic inside CLI — delegate to modules

## 📚 Resources

-   `typer.testing.CliRunner`
-   Use mock patching to simulate external behavior (e.g., API calls)
