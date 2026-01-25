# Changelog

Toutes les modifications notables du plugin notifications seront documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2026-01-25

### 🔧 Corrigé

#### Chemins d'installation
- Utilisation de `${CLAUDE_PLUGIN_ROOT}` dans la configuration des hooks pour portabilité
- Utilisation de variables d'environnement `CLAUDE_PLUGIN_ROOT` et `CLAUDE_PLUGIN_DIR` pour imports Python dynamiques
- Fallback sur calcul via `Path(__file__)` si variables absentes
- Fichiers corrigés :
  - `scripts/dispatch-notifications.py` - Import dynamique du module hooks
  - `scripts/mark-notification-read.py` - Import dynamique du module hooks
  - `hooks/notification.py` - Import dynamique des utilitaires
- Configuration hooks corrigée dans README avec syntaxe `${CLAUDE_PLUGIN_ROOT}`
- Compatible installation standard ET développement local

### 🎉 Ajouté

#### Infrastructure
- Système de queue persistante `queue.jsonl` pour toutes les notifications
- Auto-détection multi-projet du fichier queue
- Backend `FileQueueBackend` pour gestion centralisée
- Support statuts `unread` / `read` pour traçabilité

#### Hooks
- `notification.py` : Hook principal pour capture événements
- `write_notification.py` : API Python pour écriture notifications
- Utils complets dans `hooks/utils/notification/` :
  - `backends/file_queue.py` : Backend queue.jsonl
  - `data.py` : Structures de données
  - `desktop.py` : Notifications desktop
  - `factory.py` : Factory backends
  - `formatters.py` : Formatage messages
  - `history.py` : Gestion historique
  - `icons.py` : Icônes système

#### Scripts CLI
- `dispatch-notifications.py` : Dispatcher configurable avec support :
  - `notify-send` : Notifications desktop Linux (auto-read)
  - `phpstorm` : Préparé pour intégration IDE (futur)
  - `custom` : Support dispatchers personnalisés
- `view-notifications.sh` : Visualisation colorée historique
- `mark-notification-read.py` : Marquage manuel read/unread

#### Configuration
- Variables d'environnement :
  - `CLAUDE_FILE_QUEUE_FILE` : Chemin custom queue
  - `CLAUDE_NOTIFICATION_DISPATCHER` : Type dispatcher
- Configuration hooks Claude Code complète
- Système auto-détection intelligent (4 niveaux)

#### Fonctionnalités
- Support priorités : `low`, `normal`, `high`, `critical`
- Support types : `info`, `success`, `warning`, `error`, `permission_prompt`, `task_complete`, `test`
- Métadonnées extensibles par notification
- Emojis et formatage avancé
- Timeouts adaptatifs selon priorité
- Session tracking et project tracking

#### Documentation
- README.md complet avec :
  - Guide installation
  - Exemples utilisation
  - Architecture détaillée
  - Guide migration
  - Troubleshooting
- `docs/notification-system-simple.md` : Architecture système
- Documentation API complète
- Exemples code Python et CLI

### 🔧 Configuration

Configuration minimale requise dans `.claude/settings.json` :

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

Le chemin vers le marketplace garantit la stabilité lors des mises à jour du plugin.

### 📦 Contenu du plugin

```
notifications/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── notification.py
│   ├── write_notification.py
│   └── utils/notification/
│       ├── backends/file_queue.py
│       ├── data.py
│       ├── desktop.py
│       ├── factory.py
│       ├── formatters.py
│       ├── history.py
│       └── icons.py
├── scripts/
│   ├── dispatch-notifications.py
│   ├── mark-notification-read.py
│   └── view-notifications.sh
├── docs/
│   └── notification-system-simple.md
├── README.md
└── CHANGELOG.md
```

### ✨ Avantages

- ✅ Source unique : toutes notifications dans `queue.jsonl`
- ✅ Historique persistant : aucune perte
- ✅ Multi-projet : isolation automatique
- ✅ Extensible : dispatchers custom faciles
- ✅ Traçabilité : statuts et métadonnées
- ✅ Simple : architecture épurée vs ancien système

### 🔄 Migration

Remplace l'ancien hook `customize/hooks/notification.py` (simple logging) par ce système complet.

### 🐛 Bugs connus

Aucun bug connu à cette version.

### 📝 Notes

Cette version 1.0.0 est la première release stable du système de notifications.
Elle remplace l'ancien système basique de `customize` par une architecture complète et extensible.

---

[1.0.0]: https://github.com/atournayre/claude-plugin/releases/tag/notifications-v1.0.0
