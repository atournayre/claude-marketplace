---
title: "notifications"
description: "Système de notifications avancé avec queue persistante, dispatchers multiples et gestion complète"
version: "1.0.3"
---

# notifications <Badge type="info" text="v1.0.3" /> <Badge type="danger" text="Déprécié" />

::: warning Déprécié
Ce plugin est déprécié. Utilise le plugin-persona : infra
:::


Système de notifications avancé pour Claude Code avec queue persistante, dispatchers multiples et gestion complète.

## 📋 Vue d'ensemble

Ce plugin fournit une infrastructure complète de notifications pour Claude Code :

- **Queue persistante** : `queue.jsonl` pour historique et traçabilité
- **Auto-détection multi-projet** : Chaque projet a sa propre queue
- **Dispatchers configurables** : `notify-send`, `phpstorm` (futur), custom
- **Gestion complète** : read/unread, priorités, types, métadonnées
- **Scripts CLI** : Commandes pour visualiser, dispatcher, marquer

## 🚀 Installation

```bash
/plugin install notifications@atournayre-claude-plugin-marketplace
```

## ⚙️ Configuration

### Configuration Minimale

`.claude/settings.json` :

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
            "command": "~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/hooks/notification.py --desktop && ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/dispatch-notifications.py"
          }
        ]
      }
    ]
  }
}
```

> **Note** : Le chemin pointe vers le marketplace plutôt que vers le cache versionné. Cela garantit que les hooks utilisent toujours la version la plus récente du plugin sans nécessiter de mise à jour de configuration lors des upgrades.

### Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `CLAUDE_FILE_QUEUE_FILE` | Chemin custom vers queue.jsonl | Auto-détection |
| `CLAUDE_NOTIFICATION_DISPATCHER` | Type de dispatcher | `notify-send` |

### Auto-détection du fichier queue

Le système cherche le fichier `queue.jsonl` dans cet ordre :

1. `CLAUDE_FILE_QUEUE_FILE` (si configuré)
2. `$CLAUDE_PROJECT_PATH/.claude/notifications/queue.jsonl` (hooks)
3. `.claude/notifications/queue.jsonl` du projet (remontée)
4. `~/.claude/notifications/queue.jsonl` (fallback global)

## 📝 Utilisation

### Écrire une notification

**Programmatique (Python)** :

```python
from write_notification import write_notification

write_notification(
    message="Mon message",
    type="info",
    emoji="📋",
    priority="normal"
)
```

**CLI** :

```bash
python3 ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/hooks/write_notification.py "Message" info 📋 normal
```

### Dispatcher les notifications

```bash
python3 ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/dispatch-notifications.py
```

Le dispatcher :
- Lit toutes les notifications `unread`
- Les affiche via le dispatcher configuré
- Marque comme `read` (comportement configurable)

### Visualiser l'historique

```bash
bash ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/view-notifications.sh
```

Affichage coloré avec :
- Timestamp
- Emoji
- Message
- Priorité

### Marquer comme lu

```bash
# Marquer une notification spécifique
python3 ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/mark-notification-read.py <notification_id>

# Tout marquer comme read
python3 ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/mark-notification-read.py --all
```

**Astuce** : Crée un alias shell pour simplifier :

```bash
# Dans ~/.bashrc ou ~/.zshrc
NOTIF_PLUGIN="$HOME/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications"
alias notif-dispatch="python3 $NOTIF_PLUGIN/scripts/dispatch-notifications.py"
alias notif-view="bash $NOTIF_PLUGIN/scripts/view-notifications.sh"
alias notif-mark="python3 $NOTIF_PLUGIN/scripts/mark-notification-read.py"
```

## 🎨 Format des notifications

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

### Types de notifications

- `info` : Information générale
- `success` : Succès d'opération
- `warning` : Avertissement
- `error` : Erreur
- `permission_prompt` : Demande de permission
- `task_complete` : Tâche terminée
- `test` : Notification de test

### Priorités

- `low` : Priorité basse (timeout 3s)
- `normal` : Priorité normale (timeout 5s)
- `high` : Priorité haute (timeout 10s)
- `critical` : Critique (permanent)

## 🔧 Dispatchers

### notify-send (défaut)

Affiche via les notifications desktop Linux. Marque automatiquement comme `read`.

**Configuration** :

```json
{
  "env": {
    "CLAUDE_NOTIFICATION_DISPATCHER": "notify-send"
  }
}
```

### phpstorm (futur)

Affichera dans PhpStorm via le plugin. Nécessite marquage manuel.

### Custom

Crée ton propre dispatcher en éditant `dispatch-notifications.py` :

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

Configuration :

```json
{
  "env": {
    "CLAUDE_NOTIFICATION_DISPATCHER": "custom"
  }
}
```

## 🏗️ Architecture

```
Hook → write_notification.py → queue.jsonl
    → dispatch-notifications.py → notify-send (ou autre dispatcher)
```

**Avantages** :
- ✅ Source unique : toutes les notifications passent par `queue.jsonl`
- ✅ Historique persistant : jamais de perte
- ✅ Multi-projet : auto-détection du projet courant
- ✅ Extensible : dispatchers configurables
- ✅ Traçabilité : statuts read/unread

## 📂 Structure

```
notifications/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── notification.py           # Hook principal
│   ├── write_notification.py     # Écriture dans queue
│   └── utils/
│       └── notification/
│           ├── __init__.py
│           ├── backends/
│           │   └── file_queue.py  # Backend queue.jsonl
│           ├── data.py            # Structure données
│           ├── desktop.py         # Notifications desktop
│           ├── factory.py         # Factory backends
│           ├── formatters.py      # Formatage messages
│           ├── history.py         # Gestion historique
│           └── icons.py           # Icônes système
├── scripts/
│   ├── dispatch-notifications.py  # Dispatcher
│   ├── mark-notification-read.py  # Marquage read
│   └── view-notifications.sh      # Visualisation
├── docs/
│   └── notification-system-simple.md  # Doc architecture
├── README.md
└── CHANGELOG.md
```

## 🔄 Migration depuis ancien système

Si tu utilisais l'ancien hook `notification.py` de `customize`, voici les changements :

### Avant (customize)

```json
{
  "hooks": {
    "notification": "customize/hooks/notification.py"
  }
}
```

Simple logging JSON, TTS optionnel.

### Après (notifications)

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/hooks/notification.py --desktop && ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/dispatch-notifications.py"
          }
        ]
      }
    ]
  }
}
```

Système complet avec queue, dispatchers, gestion read/unread. Le chemin vers le marketplace assure la stabilité lors des mises à jour.

## 🧪 Tests

Envoyer une notification de test :

```bash
python3 ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/hooks/write_notification.py "Test" test 🧪 normal
python3 ~/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/notifications/scripts/dispatch-notifications.py
```

## 🐛 Troubleshooting

### Notifications pas affichées

- Vérifier `notify-send` installé : `which notify-send`
- Vérifier permissions scripts : `chmod +x scripts/*`
- Vérifier dispatcher configuré : `echo $CLAUDE_NOTIFICATION_DISPATCHER`

### Queue pas trouvée

- Vérifier auto-détection : chercher `.claude/notifications/queue.jsonl`
- Forcer chemin : `CLAUDE_FILE_QUEUE_FILE=/path/to/queue.jsonl`

### Warnings libnotify

```
libnotify-WARNING: Running in confined mode
```

Normal en mode confiné (Snap, Flatpak). Les notifications s'affichent quand même.

## 📄 Licence

MIT

## 👤 Auteur

**Aurélien Tournayre**
- GitHub: [@atournayre](https://github.com/atournayre)
- Email: aurelien.tournayre@gmail.com

## 🔗 Liens

- [Marketplace](https://github.com/atournayre/claude-plugin)
- [Documentation Claude Code](https://code.claude.com/docs)
- [Issues](https://github.com/atournayre/claude-plugin/issues)
