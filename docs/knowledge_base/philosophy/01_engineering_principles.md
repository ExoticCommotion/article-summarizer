# 🧠 Engineering Principles

These principles exist to guide Devin toward consistent, maintainable, and intelligent development.

## 1. Think Before You Code

Before writing code, clearly define:

-   What you're trying to solve
-   Why it matters
-   What assumptions you're making

## 2. Design for Clarity and Change

-   Code should explain itself through naming and structure
-   Plan for others (or future you) to modify it
-   Prefer explicit logic to clever tricks

## 3. Fail Fast, Fail Loud

-   Validate inputs early
-   Raise precise errors with clear context
-   Don’t silently swallow exceptions—your tests should catch failure, not suppress it

## 4. Optimize for Maintainability

-   Keep functions small, pure, and reusable
-   Separate concerns: I/O, logic, orchestration
-   Write with extensibility in mind (e.g. CLI flags, injection points)

## 5. Integrate Code Quality into the Cycle

-   Test, lint, typecheck, format—these aren't optional
-   Write code that passes checks the first time
-   Never rely on humans to catch what tools can catch

## 6. Do the Next Developer a Favor

-   Leave docstrings, comments where necessary
-   Use logs to surface state in complex flows
-   Leave a traceable commit that explains your intention

## 7. Don’t Just Work—Work Transparently

-   Treat logging and CLI output as UX for developers
-   Emit meaningful status and decisions from agent pipelines
