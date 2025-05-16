# KFP004: Clean Separation of Concerns in Manager Classes

## Context
Manager classes serve as the main entry points and orchestrators in a system. They coordinate the workflow but should delegate implementation details to specialized classes and functions.

## Problem
Manager classes often accumulate raw implementation code that doesn't belong there:
- Data transformation logic
- Complex parsing or processing
- Utility functions
- Type conversion code

This leads to:
- Bloated manager classes that are difficult to maintain
- Reduced testability due to large methods with multiple responsibilities
- Tight coupling between orchestration and implementation details
- Difficulty in reusing code across different parts of the system

## Solution
Apply separation of concerns to manager classes:
- Manager classes should focus on orchestration and workflow coordination
- Implementation details should be delegated to helper modules and service classes
- Data transformation should be handled by specialized functions
- Utility code should be moved to dedicated helper modules

## Benefits
- Cleaner, more maintainable manager classes
- Improved testability through smaller, focused methods
- Enhanced code reusability
- Better separation of concerns
- More intuitive codebase organization

## Implementation Guidelines
1. Identify raw implementation code in manager classes
2. Create appropriate helper modules for different types of functionality
3. Move implementation details to these helper modules
4. Update the manager class to use these helpers
5. Ensure proper error handling and logging in both the manager and helpers

## Example
See the refactoring of `ArticleSummarizerManager._extract_content` method in `src/backend/app/custom_agents/article_summarizer/manager.py` and the creation of helper functions in `src/backend/app/helpers/article_summarizer/parser_helpers.py`.
