---
name: dev:auto:explore
description: Explorer le codebase automatiquement - Mode AUTO (Phase 2)
model: sonnet
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
output-style: bullet-points
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Phase 2 du workflow automatisé : explorer le codebase pour comprendre les patterns existants **SANS interaction**.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour connaître la feature en cours
- Si le fichier n'existe pas, exit avec erreur code 1

## 2. Lancer les agents d'exploration

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

## 4. Mettre à jour le workflow state

```json
{
  "currentPhase": 2,
  "phases": {
    "2": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée},
      "keyFiles": ["{liste des fichiers clés}"],
      "patterns": ["{patterns identifiés}"],
      "findings": "{résumé des découvertes}"
    }
  }
}
```

# Règles

- ✅ **Mode automatique** : aucune interaction
- ✅ **Lancer agents en parallèle** si disponibles
- ✅ **Documenter les patterns** trouvés
- ❌ **Jamais demander confirmation** (exit 1 si erreur, continuer sinon)
- ✅ **Consolider les résultats** pour Phase 3
