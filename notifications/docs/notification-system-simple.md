# Système de notifications simplifié

## Principe

**Source unique** : `queue.jsonl` dans `.claude/notifications/` du projet

**Flux** :
```
Event → queue.jsonl (toujours)
     → dispatcher (lit unread et affiche)
```

Pas de "backend" à choisir, la queue est **obligatoire**.

---

## Configuration minimale

```json
{
  "env": {
    "CLAUDE_FILE_QUEUE_FILE": "",
    "CLAUDE_NOTIFICATION_DISPATCHER": "notify-send"
  },
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notification.py --desktop && ~/.claude/scripts/dispatch-notifications.py"
          }
        ]
      }
    ]
  }
}
```

**Variables** :
- `CLAUDE_FILE_QUEUE_FILE` : Chemin custom (vide = auto-détection)
- `CLAUDE_NOTIFICATION_DISPATCHER` : `notify-send`, `phpstorm` (futur), etc.

---

## Auto-détection du fichier queue

Priorité :
1. `CLAUDE_FILE_QUEUE_FILE` (si configuré)
2. `$CLAUDE_PROJECT_PATH/.claude/notifications/queue.jsonl` (hooks)
3. `.claude/notifications/queue.jsonl` du projet (remontée)
4. `~/.claude/notifications/queue.jsonl` (fallback global)

**Multi-projet** : Chaque projet a son propre `queue.jsonl`.

---

## Format des notifications

```json
{
  "id": "uuid",
  "timestamp": "2026-01-25T17:00:00",
  "status": "unread",
  "title": "🔐 permission_prompt",
  "message": "Demande de permission bash",
  "type": "permission_prompt",
  "emoji": "🔐",
  "priority": "normal",
  "session_title": "...",
  "project_name": "...",
  "metadata": {}
}
```

---

## Écrire une notification (programmatique)

```python
from write_notification import write_notification

write_notification(
    message="Mon message",
    type="info",
    emoji="📋",
    priority="normal"
)
```

Ou en CLI :

```bash
~/.claude/hooks/write_notification.py "Message" info 📋 normal
```

---

## Dispatcher

Le dispatcher lit les notifications `unread` et les affiche :

```bash
~/.claude/scripts/dispatch-notifications.py
```

**Dispatcher `notify-send`** (auto-read) :
- Lit les `unread`
- Affiche via `notify-send`
- Marque automatiquement comme `read`

**Dispatcher `phpstorm`** (futur, manual-read) :
- Lit les `unread`
- Affiche dans l'IDE
- Utilisateur clique → marque comme `read`

---

## Marquage manuel

```bash
# Marquer une notification
~/.claude/scripts/mark-notification-read.py <notification_id>

# Tout marquer comme read
~/.claude/scripts/mark-notification-read.py --all
```

---

## Utilitaires

```bash
# Voir joliment
~/.claude/scripts/view-notifications.sh

# Lister les unread
cat .claude/notifications/queue.jsonl | jq 'select(.status == "unread")'

# Compter unread
cat .claude/notifications/queue.jsonl | jq -r 'select(.status == "unread")' | wc -l
```

---

## Architecture simplifiée

**Avant** (complexe) :
```
Hook → BackendFactory → FileQueueBackend → queue.jsonl
                     → NotifySendBackend → notify-send
                     → TerminalBackend → log
```

**Après** (simple) :
```
Hook → write_notification.py → queue.jsonl
    → dispatch-notifications.py → notify-send (ou autre)
```

**Avantages** :
- ✅ Moins de code (suppression BackendFactory, NotificationData, etc.)
- ✅ Plus clair (un seul chemin : queue obligatoire)
- ✅ Plus flexible (dispatcher séparé, facile à étendre)
- ✅ Multi-projet natif (auto-détection)

---

## Développer un dispatcher custom

Éditer `dispatch-notifications.py` :

```python
def dispatch_custom(notification: Dict[str, Any]) -> bool:
    """Dispatcher custom."""
    # Logique custom
    return True

# Dans main():
elif dispatcher_type == 'custom':
    success = dispatch_custom(notification)
    if success:
        notification['status'] = 'read'  # Auto-read ou pas
```

Configurer :

```json
{
  "env": {
    "CLAUDE_NOTIFICATION_DISPATCHER": "custom"
  }
}
```
