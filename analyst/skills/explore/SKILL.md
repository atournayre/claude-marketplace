---
name: analyst:explore
description: Explorer le codebase avec agents parallèles - Phase 1 (supporte le mode automatique)
model: sonnet
allowed-tools: [Task, Read, Glob, Grep, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Explorer le codebase (Phase 1)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 1 du workflow de développement : explorer le codebase pour comprendre les patterns existants.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour connaître la feature en cours
- Si le fichier n'existe pas, demander à l'utilisateur de lancer `/analyst:discover` d'abord
  (en mode automatique : exit avec erreur code 1)

## 2. Créer les tâches d'exploration (mode interactif)

En mode interactif, utiliser `TaskCreate` pour chaque agent :

```
TaskCreate #1: Explorer features similaires (explore-codebase)
TaskCreate #2: Mapper architecture et abstractions (explore-codebase)
TaskCreate #3: Analyser intégrations (explore-codebase) - optionnel
TaskCreate #4: Consolider résultats et présenter résumé
```

- Tâche #3 optionnelle selon pertinence de la feature
- Tâche #4 bloquée par les agents 1-3 (utiliser `addBlockedBy`)
- Les agents 1-3 se lancent en parallèle

## 3. Lancer les agents d'exploration

Lancer **2-3 agents en parallèle** avec des focus différents.

**Limites d'exploration :**
- `max_turns: 10` pour chaque agent
- Si un agent atteint sa limite sans résultats, marquer tâche comme completed avec résultats partiels
- Chaque prompt agent doit inclure : "Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite."

### Agent 1 : Features similaires
```
Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite.

Trouve des features similaires à "{feature}" dans le codebase.
Trace leur implémentation de bout en bout.
Retourne les 5-10 fichiers clés à lire.
```

### Agent 2 : Architecture
```
Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite.

Mappe l'architecture et les abstractions pour la zone concernée par "{feature}".
Identifie les patterns utilisés (repositories, services, events, etc.).
Retourne les 5-10 fichiers clés à lire.
```

### Agent 3 : Intégrations (si pertinent)
```
Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite.

Analyse les points d'intégration existants (APIs, events, commands).
Identifie comment les features communiquent entre elles.
Retourne les 5-10 fichiers clés à lire.
```

## 4. Consolider les résultats

- Fusionner les listes de fichiers identifiés
- Lire les fichiers clés pour construire une compréhension profonde
- Identifier les patterns récurrents

## 5. Présenter le résumé

```
Exploration du codebase

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

## 6. Finaliser

Mettre à jour `.claude/data/.dev-workflow-state.json`

```json
{
  "currentPhase": 1,
  "phases": {
    "1": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": "{durée}",
      "keyFiles": ["{liste des fichiers clés}"],
      "patterns": ["{patterns identifiés}"],
      "findings": "{résumé des découvertes}"
    }
  }
}
```

# Règles

- Lancer les agents en parallèle si disponibles
- Documenter les patterns trouvés
- En mode automatique : aucune interaction, exit 1 si erreur
- En mode interactif : utiliser TaskCreate/TaskUpdate pour suivi de progression

# Prochaine étape

```
Exploration terminée

Prochaine étape : /analyst:clarify pour poser les questions de clarification
```
