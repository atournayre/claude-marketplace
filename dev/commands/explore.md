---
description: Explorer le codebase avec agents parallèles (Phase 1)
model: claude-sonnet-4-5-20250929
allowed-tools: Task, Read, Glob, Grep
output-style: bullet-points
---

# Configuration de sortie

**IMPORTANT** : Cette commande génère un résumé d'exploration structuré et nécessite un format de sortie spécifique.

Lis le frontmatter de cette commande. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Objectif

Phase 1 du workflow de développement : explorer le codebase pour comprendre les patterns existants.

# Prérequis

⚠️ **Plugin feature-dev requis** pour les agents `code-explorer`.

Si non installé :
```
/plugin install feature-dev@claude-code-plugins
```

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour connaître la feature en cours
- Si le fichier n'existe pas, demander à l'utilisateur de lancer `/dev:discover` d'abord

## 2. Lancer les agents code-explorer

Lancer **2-3 agents `code-explorer` en parallèle** avec des focus différents :

### Agent 1 : Features similaires
```
Trouve des features similaires à "{feature}" dans le codebase.
Trace leur implémentation de bout en bout.
Retourne les 5-10 fichiers clés à lire.
```

### Agent 2 : Architecture
```
Mappe l'architecture et les abstractions pour la zone concernée par "{feature}".
Identifie les patterns utilisés (repositories, services, events, etc.).
Retourne les 5-10 fichiers clés à lire.
```

### Agent 3 : Intégrations (si pertinent)
```
Analyse les points d'intégration existants (APIs, events, commands).
Identifie comment les features communiquent entre elles.
Retourne les 5-10 fichiers clés à lire.
```

## 3. Consolider les résultats

- Fusionner les listes de fichiers identifiés
- Lire les fichiers clés pour construire une compréhension profonde
- Identifier les patterns récurrents

## 4. Présenter le résumé

```
🔍 Exploration du codebase

**Features similaires trouvées :**
- {feature 1} ({chemin}) : {description courte}
- {feature 2} ({chemin}) : {description courte}

**Patterns architecturaux identifiés :**
- {pattern 1} : utilisé dans {fichiers}
- {pattern 2} : utilisé dans {fichiers}

**Fichiers clés à connaître :**
1. `{fichier}:{ligne}` - {rôle}
2. `{fichier}:{ligne}` - {rôle}
...

**Points d'attention :**
- {observation 1}
- {observation 2}
```

## 5. Mettre à jour le workflow state

```json
{
  "currentPhase": 1,
  "phases": {
    "1": {
      "status": "completed",
      "completedAt": "{timestamp}",
      "keyFiles": ["{liste des fichiers}"],
      "patterns": ["{liste des patterns}"]
    }
  }
}
```

# Prochaine étape

```
✅ Exploration terminée

Prochaine étape : /dev:clarify pour poser les questions de clarification
```
