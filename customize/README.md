# Plugin Customize

Personnalise ton expérience Claude Code avec hooks, output styles et status lines sur mesure.

## Installation

```bash
/plugin install customize@atournayre
```

## Fonctionnalités

### Hooks Personnalisés

Scripts Python pour automatiser et personnaliser le comportement de Claude Code à différents moments du cycle de vie.

#### Hooks Disponibles

**`notification.py`**
- Gestion des notifications système
- Alertes visuelles/sonores pour événements importants

**`session_start.py`**
- Exécuté au démarrage de session
- Configuration initiale
- Chargement de contexte

**`user_prompt_submit.py`**
- Exécuté avant traitement du prompt utilisateur
- Validation
- Transformation du prompt

**`pre_tool_use.py`**
- Exécuté avant chaque utilisation d'outil
- Validation des paramètres
- Logging
- Sécurité

**`post_tool_use.py`**
- Exécuté après chaque utilisation d'outil
- Analyse des résultats
- Cleanup
- Métriques

**`pre_compact.py`**
- Exécuté avant compaction du contexte
- Sauvegarde de données importantes
- Archivage

**`stop.py`**
- Exécuté à l'arrêt de session
- Cleanup final
- Sauvegarde d'état

**`subagent_stop.py`**
- Exécuté à l'arrêt d'un sous-agent
- Récupération de résultats
- Cleanup spécifique

### Bash Security Validator ⚡

**Validateur de sécurité pour commandes bash** (TypeScript/Bun)

Protection automatique contre commandes dangereuses via hook PreToolUse :

- ✅ **100+ patterns de sécurité** : Bloque rm -rf /, dd, mkfs, etc.
- ✅ **82+ tests automatisés** : Suite complète de validation
- ✅ **Détection patterns malveillants** : Fork bombs, backdoors, exfiltration
- ✅ **Protection chemins système** : Empêche écritures dans /etc, /usr, /bin
- ✅ **Logs sécurité** : Traçabilité complète des blocages

**Commandes bloquées :**
- Destruction système : `rm -rf /`, `dd if=/dev/zero`, `mkfs`
- Escalade privilèges : `sudo`, `chmod 777`, `passwd`
- Attaques réseau : `nc -l`, `nmap`, `telnet`
- Patterns malveillants : Fork bombs, backdoors, manipulation logs

**Documentation complète** : `validators/bash/README.md`

### Configuration

Les hooks sont automatiquement détectés et chargés depuis `customize/hooks/`.

Pour activer un hook dans ton projet :

```json
{
  "hooks": {
    "session_start": "path/to/customize/hooks/session_start.py",
    "user_prompt_submit": "path/to/customize/hooks/user_prompt_submit.py",
    "pre_tool_use": "path/to/customize/hooks/pre_tool_use.py",
    "post_tool_use": "path/to/customize/hooks/post_tool_use.py",
    "notification": "path/to/customize/hooks/notification.py",
    "pre_compact": "path/to/customize/hooks/pre_compact.py",
    "stop": "path/to/customize/hooks/stop.py",
    "subagent_stop": "path/to/customize/hooks/subagent_stop.py"
  }
}
```

### Cas d'Usage

**Workflow automatisé :**
- Charger contexte projet au démarrage
- Valider commandes avant exécution
- Logger toutes les actions
- Archiver historique à l'arrêt

**Sécurité :**
- Bloquer outils dangereux
- Valider chemins de fichiers
- Auditer les accès

**Métriques :**
- Tracker temps d'exécution
- Compter utilisations d'outils
- Analyser patterns

**Notifications :**
- Alertes pour tâches longues
- Notifications de fin de traitement
- Erreurs critiques

## Structure

```
customize/
├── .claude-plugin/
│   ├── plugin.json
│   └── hooks.json           # Configuration hook PreToolUse (Bash Validator)
├── hooks/                   # Hooks Python
│   ├── notification.py
│   ├── session_start.py
│   ├── user_prompt_submit.py
│   ├── pre_tool_use.py
│   ├── post_tool_use.py
│   ├── pre_compact.py
│   ├── stop.py
│   ├── subagent_stop.py
│   └── utils/
└── validators/              # Validators TypeScript/Bun
    └── bash/                # Bash Security Validator
        ├── src/
        │   ├── cli.ts       # Entry point hook PreToolUse
        │   └── lib/
        │       ├── security-rules.ts  # 100+ patterns sécurité
        │       ├── validator.ts
        │       └── types.ts
        ├── __tests__/       # 82+ tests
        ├── package.json
        └── README.md
```

## Architecture Hybride

Ce plugin utilise une **architecture hybride Python + TypeScript** :

- **Hooks Python** (`hooks/`) : Gestion événements Claude Code (session, prompts, notifications)
- **Validators TypeScript** (`validators/`) : Validation sécurité haute performance avec Bun

**Pourquoi hybride ?**
- Python : Excellent pour scripts hooks, intégration système, flexibilité
- TypeScript/Bun : Performance critique pour validation temps réel, tests robustes (82+)

**Dépendances :**
- Python 3.x (hooks)
- Bun runtime (validators, optionnel si validators non utilisés)

## Développement de Hooks

### Template de Base

```python
#!/usr/bin/env python3
"""
Hook description
"""

def main():
    """Hook entry point"""
    # Your logic here
    pass

if __name__ == "__main__":
    main()
```

### Best Practices

- Hooks légers et rapides
- Gestion d'erreurs robuste
- Logging approprié
- Pas d'effets de bord inattendus
- Documentation claire

## Licence

MIT
