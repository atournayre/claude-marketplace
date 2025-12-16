---
name: prepare
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory
allowed-tools: [Read, Write, Edit, Grep, Glob, MultiEdit]
model: claude-opus-4-1-20250805
---


# Quick Plan
Create a detailed implementation plan based on the user's requirements provided through the `USER_PROMPT` variable. Analyze the request, think through the implementation approach, and save a comprehensive specification document to `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that can be used as a blueprint for actual development work.

## Variables
USER_PROMPT: $ARGUMENTS
PLAN_OUTPUT_DIRECTORY: `docs/specs/`

## Instructions
- Carefully user's requirements provided in the USER_PROMPT variable
- Think deeply about the best approach to implement the requested functionality or solve the problem
- Create a **highly detailed, executable** implementation plan that includes:
- Clear problem statement and objectives
- Technical approach and architecture decisions
- **Explicit file list** with full paths for each file to create/modify
- Step-by-step implementation guide with **concrete code** (not pseudo-code)
- **Actionable todo list** with markdown checkboxes that can be tracked and updated during implementation
- Potential challenges and solutions
- Testing strategy
- Success criteria
- Generate a descriptive, kebab-case filename based on the main topic of the plan
- Save the complete implementation plan to `PLAN_OUTPUT_DIRECTORY/<descriptive-name>.md`
  - **IMPORTANT**: The plan must be detailed enough for a fast model (haiku) to execute mechanically without interpretation
  - Include **complete code snippets** with exact method signatures, imports, and dependencies
  - Specify **exact file paths** for all files to create or modify
  - The todo list must use markdown checkboxes `- [ ]` with granular, actionable tasks in logical implementation order
  - Each task should reference the specific file(s) and code to write
- Consider edge cases, error handling, and scalability concerns
- Structure the document with clear sections and proper markdown formatting

## Workflow

1. Analyze Requirements - THINK HARD and parse the USER_PROMPT to understand the core problem and desired outcome
2. Design Solution - Develop technical approach including architecture decisions and implementation strategy
3. Document Plan - Structure a comprehensive markdown document with problem statement, implementation steps, and testing approach
4. Generate Filename - Create a descriptive kebab-case filename based on the plan's main topic
5. Save & Report - Write the plan to `PLAN_OUTPUT_DIRECTORY/<filename>.md` and provide a summary of key components

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```
✅ Implementation Plan Created

File: PLAN_OUTPUT_DIRECTORY/<filename>.md

Topic: <brief description of what the plan covers>

Key Components:
- <main component 1>
- <main component 2>
- <main component 3>
```
