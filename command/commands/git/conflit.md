---
description: Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape.
argument-hint: "<branche-destination>"
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git merge:*)
  - Bash(git rebase:*)
  - Bash(git checkout:*)
  - Bash(git add:*)
  - Read
  - Edit
---
# git:conflit

Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape.

---

**IMPORTANT**: Use the Skill tool to invoke the skill `git:conflit` with arguments: $ARGUMENTS.

Execute the skill immediately. Do not explain or describe what you will do - just invoke the skill using the Skill tool.

---

**Note**: This slash command was auto-generated to workaround Claude Code bug #15178.
Once fixed, this workaround can be removed.
