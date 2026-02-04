---
name: dev:auto:design
description: Choisir architecture automatiquement (Phase 4)
model: sonnet
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
output-style: table-based
version: 1.0.0
license: MIT
---

# Configuration de sortie

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


**IMPORTANT** : Cette commande génère une architecture choisie automatiquement et nécessite un format de sortie structuré.

Lis le frontmatter de cette commande. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Objectif

Phase 4 du workflow automatisé : proposer les architectures **ET choisir automatiquement** (Pragmatic Balance).

Zéro demande de choix à l'utilisateur.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
# Récupérer issue_number depuis le contexte
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour la feature, findings et décisions
- Si phases précédentes non complétées, exit avec erreur

## 2. Évaluer et choisir l'architecture la meilleure

Lancer **1 agent `code-architect`** pour évaluer les approches et recommander la meilleure :

```
Évalue les 3 approches architecturales possibles pour "{feature}" :

**Approche 1 : Minimal Changes**
- Petit changement, réutilisation max, minimum de nouveaux fichiers

**Approche 2 : Clean Architecture**
- Abstractions élégantes, séparation des responsabilités, testabilité optimale

**Approche 3 : Pragmatic Balance**
- Balance rapidité/qualité, bonnes pratiques sans over-engineering

Contexte du codebase :
{keyFiles et patterns de la phase 2}

Décisions prises (Elegant Objects, edge cases, etc.) :
{décisions de la phase 3}

RECOMMANDE la meilleure approche pour CE projet basée sur :
1. Les patterns existants du codebase
2. Les principes Elegant Objects applicables
3. L'absence d'over-engineering
4. La complexité justifiée vs bénéfices

Retourne :
- Approche recommandée + raison précise
- Composants à créer/modifier
- Fichiers impactés
- Diagramme de flux (ASCII)
```

## 3. Présenter l'architecture choisie

```
🏗️ Architecture sélectionnée : {Approche recommandée}

**Description :**
{résumé de l'approche}

**Raison du choix :**
{pourquoi cette approche est la meilleure pour CE projet}

**Composants :**
- {composant 1} : {responsabilité}
- {composant 2} : {responsabilité}

**Fichiers impactés :** {nombre}
- {fichier 1}
- {fichier 2}
```

## 4. Documenter l'architecture choisie

Mettre à jour le workflow state :

```json
{
  "currentPhase": 4,
  "phases": {
    "4": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée},
      "chosenApproach": "Pragmatic Balance",
      "autoChosen": true,
      "reason": "Default pour mode auto (balance rapidité/qualité)",
      "architecture": {
        "components": ["{liste des composants}"],
        "files": ["{liste des fichiers à créer/modifier}"],
        "buildSequence": ["{étapes d'implémentation}"]
      }
    }
  }
}
```

# Règles

- ✅ **Évaluer les 3 approches** (en 1 seul agent, pas 3 agents parallèles)
- ✅ **Recommander la MEILLEURE** pour CE projet (pas toujours la même)
- ✅ **Basée sur :** patterns existants, Elegant Objects, absence d'over-engineering
- ❌ **Zéro demande de choix** à l'utilisateur
- ✅ **Justifier le choix** avec raison précise
- ✅ **Documenter l'architecture** choisie
