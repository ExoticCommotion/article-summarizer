# ✅ Test-First Development

Writing tests first makes code more reliable, focused, and maintainable. It also prevents regressions and raises confidence in refactors.

## 🚦 When to Use

-   When developing **pure logic** (functions, utilities, classes)
-   When building **API endpoints** or **CLI tools**
-   When fixing bugs (write a failing test first!)

## 🧪 Basic Flow

1. Write a failing test
2. Implement the minimal code to make it pass
3. Refactor the implementation
4. Re-run tests
5. Repeat

## 🧠 Devin's Best Practice

Always define the function signature, expected inputs, and output types before writing implementation.

```python
# tests/unit/test_math_utils.py
def test_adds_two_numbers() -> None:
    assert add(2, 3) == 5
```

Then:

```python
# src/backend/app/utils/math_utils.py
def add(a: int, b: int) -> int:
    return a + b
```

## 🧩 Benefits

-   Ensures **spec clarity** before implementation
-   Improves **test coverage**
-   Reduces time debugging later
-   Naturally documents usage

## 📌 Tips

-   Name test files and functions descriptively
-   Use parametrized tests where appropriate
-   Mock external systems only when needed
