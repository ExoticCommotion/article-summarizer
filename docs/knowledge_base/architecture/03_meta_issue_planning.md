# 🧠 Meta Issue Planning for Agents

All issues assigned to Devin should include more than just task output. They should be a **plan** for how to solve the problem.

## 🧭 Issue Fields Devin Relies On

Each issue should include:

-   🧠 **Goal**: What the feature or bug fix achieves
-   🔍 **Input/Output Expectations**: CLI args, API behavior, files touched
-   🧪 **How It Will Be Verified**: Test names, command output, pass/fail signals
-   🧱 **Design Constraints**: Which files must remain unchanged, etc.
-   💡 **Hints or Pitfalls**: Tricky behaviors or things not to assume

## ✅ High-Quality Example

```yaml
title: Add agent output summarizer

goal: Create a utility to summarize JSON agent output into 3-sentence summaries using OpenAI.

input: JSON output file from any agent
output: stdout + written markdown

verify:
    - test passes in tests/unit/test_summary_utils.py
    - summary is deterministic (mocked)

notes:
    - Do not call OpenAI in real tests (use fixtures)
    - Log progress with get_logger
```

## 💬 Agent’s Internal Planning

Upon seeing an issue, Devin should:

1. Validate: "Is this issue specific, testable, and clear?"
2. Draft plan: What files are touched? What functions are created?
3. Sketch tests: Which are needed? What coverage will look like?
4. Only then: begin implementation.

All of this should be reproducible in the issue history.
