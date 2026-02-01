---
title: "customize"
description: "Personnalise ton expérience Claude Code avec hooks, output styles et status lines sur mesure"
version: "1.0.0"
---

# customize <Badge type="info" text="v1.0.0" />


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
│   └── plugin.json
└── hooks/
    ├── notification.py
    ├── session_start.py
    ├── user_prompt_submit.py
    ├── pre_tool_use.py
    ├── post_tool_use.py
    ├── pre_compact.py
    ├── stop.py
    ├── subagent_stop.py
    └── utils/
```

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
