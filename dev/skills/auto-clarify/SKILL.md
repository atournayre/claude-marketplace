---
name: dev:auto:clarify
description: Lever ambiguités avec heuristiques automatiques (Phase 3)
model: sonnet
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Phase 3 du workflow automatisé : identifier et résoudre les ambiguïtés **avec heuristiques prédéfinies**.

Zéro question, zéro AskUserQuestion. Décisions automatiques basées sur les patterns existants.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
# Récupérer issue_number depuis le contexte
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour la feature et les findings de l'exploration (Phase 2)
- Si le fichier n'existe pas ou phase 2 non complétée, exit avec erreur

## 2. Analyser les zones d'ombre

Identifier les aspects sous-spécifiés dans les catégories suivantes.

## 3. Appliquer heuristiques automatiques

**Au lieu de poser des questions, utiliser cette table de décision :**

| Catégorie | Heuristique par défaut |
|-----------|------------------------|
| **Edge cases** | Valeur null/vide → Exception métier explicite (`InvalideXXX` ou `{NomEntité}Invalide`) |
| **Gestion erreurs** | Exceptions métier typées (héritant d'une base commune) + logging PSR-3 niveau ERROR |
| **Intégration** | Réutiliser patterns existants détectés en Phase 1 (patterns de repository, services, DTOs) |
| **Rétrocompatibilité** | Préserver API publique (pas de breaking changes), créer nouvelle méthode si needed |
| **Performance** | Pas de cache prématuré sauf si liste > 1000 items (sinon trop de complexité) |
| **Sécurité** | TOUJOURS valider inputs (whitelist si possible), échapper outputs selon context |

## 4. Documenter les décisions appliquées

Mettre à jour le workflow state avec les décisions **appliquées** (pas des questions) :

```json
{
  "currentPhase": 3,
  "phases": {
    "3": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée},
      "autoDecisions": {
        "edgeCases": "Exception métier InvalideXXX pour valeurs null/vides",
        "errorHandling": "Exceptions typées héritant de DomainException + logging PSR-3 ERROR",
        "integration": "Réutilisation patterns existants Phase 1",
        "compatibility": "Préservation API publique, nouvelle méthode si breaking",
        "performance": "Pas de cache prématuré sauf liste > 1000 items",
        "security": "Validation inputs (whitelist), échappement outputs"
      }
    }
  }
}
```

# Règles

- ❌ **Zéro AskUserQuestion** (pas de questions)
- ✅ **Heuristiques appliquées** directement selon la table
- ❌ **Ne PAS proposer d'architecture**
- ✅ **Documenter les décisions** pour traçabilité
- ✅ **Utiliser les patterns existants** détectés en Phase 1
