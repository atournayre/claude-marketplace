---
model: claude-haiku-4-5-20251001
description: Code the codebase based on the plan
argument-hint: [path-to-plan]
allowed-tools: Read, Write, Bash
---

# Code
Follow the `Workflow` to implement the `PATH_TO_PLAN` then `Report` the completed work.

## Variables
PATH_TO_PLAN: $ARGUMENTS

## Workflow

- If no `PATH_TO_PLAN` is provided, STOP immediately and ask the user to provide it.
- Read the plan at `PATH_TO_PLAN`. Think hard about the plan and implement it into the codebase.

## Quality Assurance
- Run all quality checks (linters, static analysis, tests)
- Fix ALL errors and warnings until all checks pass
- Ensure the code is error-free before considering the task complete
- DO NOT proceed to reporting until all quality checks are green

# Report
- Confirm all quality checks have passed
- Summarize the work you've just done in a concise bullet point list.
- Report the files and total lines changed with `git diff —-stat`
