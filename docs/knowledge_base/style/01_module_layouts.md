# 📦 Module Layout Conventions

To keep the codebase maintainable and readable, we follow a consistent pattern when designing Python modules.

## ✅ Good Module Layout

Each module should:

-   Export a small number of well-named public functions
-   Be under 100 lines unless justified
-   Group related logic into reusable components

**Example**:

```
utils/
├── logger.py          # get_logger() and setup logic
├── audio_utils.py     # convert_to_mp3(), trim_audio()
├── file_io.py         # read_file(), write_file()
```

## 🔍 Where to Place Logic

-   Logic that interacts with **external services** → `utils/` or `adapters/`
-   Logic that encapsulates **domain-specific features** → in its own module (`agents/`, `tools/`, etc.)
-   Helper logic that supports **only one agent** → keep it near the agent logic

## ❌ Anti-Patterns

-   Huge "helper.py" files with unrelated utilities
-   Overuse of `__init__.py` to re-export deeply nested APIs
-   Duplicated utility functions scattered across folders

## 📁 When to Split a File

Split a file when:

-   You have 2+ classes or 5+ public functions
-   Logic spans multiple domains
-   Coverage gets messy across unrelated responsibilities
