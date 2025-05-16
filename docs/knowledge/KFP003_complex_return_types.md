# KFP003: Complex Return Types as Named Models

## Context
When developing Python applications, function signatures can become unwieldy with complex nested types. This is especially common in data processing functions that return multiple pieces of information.

## Problem
Consider this function signature:

```python
def extract_article_text(html_content: str) -> tuple[
    str,
    list[dict[str, str]],
    dict[str, str | list[str]],
    dict[str, list[dict[str, str | int | list[str]]]],
]:
```

This signature has several issues:
- It's difficult to read and understand
- It's error-prone when using the returned values
- It lacks meaningful names for the returned data
- It complicates type checking

## Solution
Extract complex return types into dedicated, well-named Pydantic models in a types directory:

```python
def extract_article_text(html_content: str) -> ExtractedArticleContent:
```

Where `ExtractedArticleContent` is a Pydantic model that clearly defines all the returned data with proper names and types.

## Benefits
- Improved code readability and maintainability
- Better type safety with explicit field names
- Easier to extend with new fields
- Self-documenting through descriptive model and field names
- Simplified function signatures
- Better IDE support for autocomplete and type hints

## Implementation Guidelines
1. Create a dedicated types directory at the app level
2. Design models that clearly represent the data structure
3. Use descriptive names for models and fields
4. Add proper docstrings to all models and fields
5. Update function signatures to use these models
6. Update all code that uses these functions

## Example
See the implementation of `ExtractedArticleContent` in `src/backend/app/types/article_summarizer/parser_types.py` for a complete example.
