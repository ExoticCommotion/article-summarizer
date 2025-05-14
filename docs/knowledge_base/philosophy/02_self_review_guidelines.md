# 🪞 Self-Review Guidelines

Before submitting or merging your code, conduct a personal code review as if you were someone else inheriting the work.

## ✅ Checklist

### 📦 Structure

-   Are files placed in the right location?
-   Does the module structure make sense?
-   Are tests grouped with their appropriate targets?

### 🧠 Readability

-   Can you understand every function without scrolling?
-   Are variable and function names self-explanatory?
-   Are loops and conditionals clean and readable?

### 🔍 Coverage

-   Have you tested both the happy path and edge cases?
-   Is every conditional branch (if/else) exercised?
-   Do your tests express the intent of the code?

### 🛡️ Correctness

-   Are inputs validated?
-   Do functions behave correctly on invalid or unexpected inputs?
-   Have you run the code against real sample inputs?

### 🧪 Tooling Compliance

-   `make check` passes (format, lint, typecheck, test)
-   No extra logs or TODOs in committed code
-   No skipped or commented-out tests

## 🧘 Questions to Ask Yourself

-   Would I be proud to show this code to another developer?
-   Will this confuse someone in 3 weeks (or me)?
-   Have I automated all the things I can?

Treat self-review as the first line of defense in delivering elite software.
