---
title: Index des Hooks
---

# Index des Hooks

10 hooks disponibles dans le marketplace.

**Note** : Les hooks sont des scripts Python qui s'exécutent en réponse à des événements (pre_tool_use, post_tool_use, etc.).

| Hook | Plugin | Description |
|------|--------|-------------|
| `notification` | [customize](/plugins/customize) | Determine which TTS script to use - only pyttsx3 is available. |
| `notification` | [notifications](/plugins/notifications) | Determine which TTS script to use - only pyttsx3 is available. |
| `post_tool_use` | [customize](/plugins/customize) | Ajuste les permissions des fichiers et dossiers créés. |
| `pre_compact` | [customize](/plugins/customize) | Log pre-compact event to logs directory. |
| `pre_tool_use` | [customize](/plugins/customize) | Comprehensive detection of dangerous rm commands. |
| `session_start` | [customize](/plugins/customize) | Log session start event to logs directory. |
| `stop` | [customize](/plugins/customize) | Return list of friendly completion messages. |
| `subagent_stop` | [customize](/plugins/customize) | Determine which TTS script to use - only pyttsx3 is available. |
| `user_prompt_submit` | [customize](/plugins/customize) | Log user prompt to logs directory. |
| `write_notification` | [notifications](/plugins/notifications) | Write notification to queue.jsonl. |
