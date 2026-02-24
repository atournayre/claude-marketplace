---
name: architect:design
description: Designer des approches architecturales et choisir la meilleure - Phase 3 (supporte le mode automatique)
model: sonnet
allowed-tools: [Task, Read, Glob, Grep, AskUserQuestion, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Design architectural (Phase 3)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 3 du workflow de développement : proposer plusieurs approches architecturales et aider l'utilisateur à choisir (ou choisir automatiquement).

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour la feature, les findings et les décisions
- Si phases précédentes non complétées, rediriger vers la phase manquante
  (en mode automatique : exit avec erreur)

## 2. Évaluer les approches architecturales

Évaluer **3 approches** pour la feature en cours :

### Approche 1 : Minimal Changes
- Petit changement, réutilisation maximale du code existant
- Minimum de nouveaux fichiers
- Convient si la feature s'intègre naturellement dans l'existant

### Approche 2 : Clean Architecture
- Abstractions élégantes, séparation des responsabilités
- Testabilité optimale
- Convient si la feature introduit un nouveau domaine métier

### Approche 3 : Pragmatic Balance
- Balance rapidité/qualité
- Bonnes pratiques sans over-engineering
- Convient dans la majorité des cas

## 3. Mode interactif : présenter et demander le choix

Présenter les 3 approches de manière comparative (table ou liste structurée).

**CRITIQUE : Attendre le choix de l'utilisateur avant de passer à la phase suivante.**

Utiliser `AskUserQuestion` pour demander le choix.

## 4. Mode automatique : choisir automatiquement

Lancer **1 agent** pour évaluer les approches et recommander la meilleure :

```
Évalue les 3 approches architecturales possibles pour "{feature}" :

Approche 1 : Minimal Changes - réutilisation max, minimum de nouveaux fichiers
Approche 2 : Clean Architecture - abstractions élégantes, testabilité optimale
Approche 3 : Pragmatic Balance - balance rapidité/qualité

Contexte du codebase : {keyFiles et patterns de la phase 1}
Décisions prises : {décisions de la phase 2}
Contraintes architecturales : {phases.1.constraints du workflow state}

CHAQUE composant proposé DOIT respecter ces contraintes.

RECOMMANDE la meilleure approche pour CE projet basée sur :
1. Les patterns existants du codebase
2. Les principes Elegant Objects applicables
3. L'absence d'over-engineering
4. La complexité justifiée vs bénéfices
5. Le respect des contraintes architecturales du projet

Retourne :
- Approche recommandée + raison précise
- Composants à créer/modifier
- Fichiers impactés
- Diagramme de flux (ASCII)
```

**Zéro demande de choix à l'utilisateur en mode automatique.**

## 5. Documenter l'architecture choisie

Présenter l'architecture sélectionnée :

```
Architecture sélectionnée : {Approche recommandée}

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

Mettre à jour `.claude/data/.dev-workflow-state.json` :

```json
{
  "currentPhase": 3,
  "phases": {
    "3": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": "{durée}",
      "chosenApproach": "{nom de l'approche}",
      "autoChosen": false,
      "reason": "{justification du choix}",
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

- Évaluer les 3 approches avant de recommander
- Justifier le choix avec une raison précise
- Baser la recommandation sur les patterns existants du codebase
- En mode automatique : zéro interaction, recommander la meilleure pour CE projet
- En mode interactif : attendre le choix explicite de l'utilisateur

# Prochaine étape

```
Architecture choisie

Prochaine étape : /architect:plan pour générer le plan d'implémentation
```
