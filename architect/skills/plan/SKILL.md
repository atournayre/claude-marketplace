---
name: architect:plan
description: Générer plan d'implémentation détaillé dans docs/specs/ - Phase 4 (supporte le mode automatique)
model: sonnet
allowed-tools: [Write, Read, Glob, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Générer le plan d'implémentation (Phase 4)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 4 du workflow de développement : générer un plan d'implémentation détaillé basé sur l'architecture choisie.

# Instructions

## 1. Créer les tâches de planification (mode interactif)

En mode interactif, utiliser `TaskCreate` pour chaque étape :

```
TaskCreate #1: Lire le contexte du workflow
TaskCreate #2: Créer le répertoire docs/specs
TaskCreate #3: Générer le plan d'implémentation
TaskCreate #4: Afficher le résumé
TaskCreate #5: Mettre à jour le workflow state
```

## 2. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer :
  - La feature description
  - Les décisions de clarification (phase 2)
  - L'architecture choisie (phase 3)
- Si phases précédentes non complétées, rediriger ou exit 1 (mode automatique)

## 3. Créer le répertoire si nécessaire

```bash
mkdir -p docs/specs
```

## 4. Générer le plan

Créer le fichier `docs/specs/feature-{nom-kebab-case}.md` avec la structure suivante :

```markdown
# Plan d'implémentation : {Feature Name}

## Résumé

**Feature :** {description}
**Approche :** {nom de l'approche choisie}
**Date :** {date du jour}

## Contexte

### Problème résolu
{description du problème}

### Décisions prises
- {décision 1}
- {décision 2}

## Architecture

### Composants
| Composant | Responsabilité | Fichier |
|-----------|---------------|---------|
| {nom} | {description} | `{chemin}` |

### Diagramme de flux
```
{représentation ASCII du flux}
```

## Plan d'implémentation

### Étape 1 : {titre}
- [ ] {tâche 1}
- [ ] {tâche 2}

**Fichiers :**
- `{chemin}` : {description}

### Étape 2 : {titre}
- [ ] {tâche 1}
- [ ] {tâche 2}

**Fichiers :**
- `{chemin}` : {description}

## Tests

### Tests unitaires
- [ ] {test 1}
- [ ] {test 2}

### Tests d'intégration
- [ ] {test 1}
```

## 5. Mettre à jour le workflow state

```json
{
  "currentPhase": 4,
  "phases": {
    "4": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": "{durée}",
      "planPath": "docs/specs/feature-{nom-kebab-case}.md",
      "components": ["{liste des composants}"],
      "implementationSteps": "{nombre}"
    }
  }
}
```

# Règles

- Le plan doit être **actionnable** (pas de descriptions vagues)
- Chaque étape doit avoir des **fichiers** et des **tâches** clairs
- Les tests doivent être **spécifiés** avant l'implémentation
- Respecter les **conventions du projet** (CLAUDE.md)
- En mode automatique : aucune interaction, exit 1 si phases précédentes manquantes

# Prochaine étape

```
Plan généré : docs/specs/feature-{nom}.md

Prochaine étape : implémenter selon le plan

L'implémentation nécessite ton approbation explicite.
```
