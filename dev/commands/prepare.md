---
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory
argument-hint: <requirements>
---

# Plan Mode Workflow

You are about to enter **plan mode** to create a detailed implementation plan.

## Context
User requirements: $ARGUMENTS

## Instructions

1. **Enter Plan Mode** - Use the `EnterPlanMode` tool immediately
2. **Explore the codebase** - Use Glob, Grep, Read to understand existing architecture
3. **Design the solution** - Create a comprehensive implementation approach
4. **Write the plan** to `docs/specs/<descriptive-kebab-case-name>.md` with:
   - Clear problem statement and objectives
   - Technical approach and architecture decisions
   - **Explicit file list** with full paths for each file to create/modify
   - Step-by-step implementation guide with **concrete code** (not pseudo-code)
   - **Actionable todo list** with markdown checkboxes `- [ ]`
   - Testing strategy and success criteria
   - **IMPORTANT**: Plan must be detailed enough for haiku to execute mechanically
5. **Present the plan** for user approval
6. **Exit Plan Mode** with `ExitPlanMode` when approved

## Plan File Requirements

The saved plan in `docs/specs/` must include:
- Complete code snippets with exact method signatures, imports, dependencies
- Exact file paths for all files to create or modify
- Granular, actionable tasks with markdown checkboxes in logical order
- Each task should reference specific file(s) and code to write

## After Approval

Ask the user if they want to:
- Launch a swarm to implement (via ExitPlanMode with launchSwarm: true)
- Use `/dev:code <path-to-plan>` to implement later
- Implement manually
