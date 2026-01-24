---
name: dev:auto:plan
description: Générer plan d'implémentation automatiquement - Mode AUTO (Phase 5)
model: claude-sonnet-4-5-20250929
allowed-tools:
  - Write
  - Read
  - Glob
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Phase 5 du workflow automatisé : générer un plan d'implémentation détaillé basé sur l'architecture choisie **SANS interaction**.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour récupérer :
  - La feature description
  - Les décisions de clarification (Phase 3)
  - L'architecture choisie (Phase 4)
- Si phases précédentes non complétées, exit avec erreur code 1

## 2. Générer le plan

Créer le fichier `docs/specs/feature-{nom-kebab-case}.md` avec le contenu suivant :

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

...

## Tests

### Tests unitaires
- [ ] {test 1}
- [ ] {test 2}

### Tests d'intégration
- [ ] {test 1}
```

## 3. Sauvegarder le chemin du plan

Mettre à jour le workflow state :

```json
{
  "currentPhase": 5,
  "phases": {
    "5": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée},
      "planPath": "docs/specs/feature-{nom-kebab-case}.md",
      "components": ["{liste des composants}"],
      "implementationSteps": {nombre}
    }
  }
}
```

# Règles

- ✅ **Mode automatique** : aucune interaction
- ✅ **Générer le plan** basé sur les phases précédentes
- ✅ **Créer le fichier** `docs/specs/` avec chemin correct
- ✅ **Documenter chaque étape** d'implémentation
- ❌ **Jamais demander confirmation**
- ✅ **Exit 1 si phases précédentes manquantes**
