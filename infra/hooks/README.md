# Hooks - Plugin infra

Les hooks Claude Code ne sont pas inclus directement dans ce plugin.

## Emplacement des hooks

Les hooks disponibles se trouvent dans les plugins suivants (dépréciés mais non supprimés) :

### Plugin `customize/`

Hooks de personnalisation Claude Code :

- `hooks/pre_tool_use.py` : Validation avant utilisation d'un outil (sécurité shell, Bash)
- `hooks/post_tool_use.py` : Actions après utilisation d'un outil
- `hooks/user_prompt_submit.py` : Traitement au moment de la soumission d'un prompt
- `hooks/session_start.py` : Actions au démarrage d'une session
- `hooks/stop.py` : Actions à l'arrêt de Claude Code
- `hooks/subagent_stop.py` : Actions à l'arrêt d'un sous-agent
- `hooks/pre_compact.py` : Actions avant la compaction du contexte
- `hooks/notification.py` : Notifications génériques

### Plugin `notifications/`

Système de notifications desktop :

- `hooks/notification.py` : Hook de notification principal
- `hooks/write_notification.py` : Écriture des notifications dans la file

## Utilisation

Pour utiliser ces hooks, configurer dans `.claude/settings.json` :

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 /path/to/customize/hooks/pre_tool_use.py" }
        ]
      }
    ]
  }
}
```

Référence : documentation Claude Code sur les hooks.
