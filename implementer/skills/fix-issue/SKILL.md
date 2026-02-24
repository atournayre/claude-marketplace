---
name: implementer:fix-issue
description: Corriger une issue GitHub avec workflow structuré et efficace
argument-hint: [issue-number]
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Correction d'Issue GitHub

Corriger une issue GitHub de manière structurée et efficace.

## Variables

ISSUE_NUMBER: $ARGUMENTS (obligatoire)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### Initialisation

Créer les tâches du workflow :

```
TaskCreate #1: Analyse de l'issue
TaskCreate #2: Préparation de l'environnement (branche)
TaskCreate #3: Investigation du code
TaskCreate #4: Implémentation de la solution
TaskCreate #5: Validation et tests
TaskCreate #6: Finalisation (informer utilisateur)
```

- Utiliser `activeForm` pour chaque tâche (ex: "Analysant l'issue", "Implémentant la solution")
- Chaque tâche doit être marquée `in_progress` puis `completed`

### Phase 1 : Analyse de l'issue

`TaskUpdate` #1 → `in_progress`

- Récupérer les détails : `gh issue view $ISSUE_NUMBER`
- Analyser le problème : type (bug, feature, enhancement), priorité, description
- Identifier les fichiers/modules concernés

`TaskUpdate` #1 → `completed`

### Phase 2 : Préparation de l'environnement

`TaskUpdate` #2 → `in_progress`

- Vérifier le statut git actuel
- S'assurer d'être sur la bonne branche de base (develop/main)
- Créer une branche de travail : `issue/$ISSUE_NUMBER-{description-courte}`

`TaskUpdate` #2 → `completed`

### Phase 3 : Investigation du code

`TaskUpdate` #3 → `in_progress`

- Localiser les fichiers concernés par l'issue
- Comprendre le code existant et identifier la cause du problème
- Analyser l'impact de la modification sur les autres parties du système
- Identifier les dépendances et side-effects potentiels

`TaskUpdate` #3 → `completed`

### Phase 4 : Implémentation de la solution

`TaskUpdate` #4 → `in_progress`

- Implémenter la correction en respectant :
  - Standards PHP 8.2+ avec typage strict
  - Conventions de nommage du projet
  - Documentation des exceptions avec `@throws`
- Éviter les changements inutiles ou trop larges
- Maintenir la cohérence avec l'architecture existante

`TaskUpdate` #4 → `completed`

### Phase 5 : Validation et tests

`TaskUpdate` #5 → `in_progress`

- Exécuter les tests existants : `make run-unit-php` (ou équivalent)
- Ajouter des tests si nécessaire pour couvrir le nouveau code
- Vérifier avec PHPStan : ZÉRO erreur acceptée
- Tester la solution manuellement si applicable

`TaskUpdate` #5 → `completed`

### Phase 6 : Finalisation

`TaskUpdate` #6 → `in_progress`

- Informer l'utilisateur du résultat
- Ne pas faire de commit

`TaskUpdate` #6 → `completed`

## Rapport

```
Issue #X analysée : {titre} ({type})
Branche créée : issue/$ISSUE_NUMBER-{description}
Fichiers modifiés :
- [fichier] : [résumé des changements]
Tests : verts
PHPStan : 0 erreur
```

## Règles

- `ISSUE_NUMBER` doit être fourni et exister sur GitHub
- Branche de travail créée avec convention de nommage
- Solution respectant les standards du projet
- PHPStan passe sans erreur (CRITIQUE)
- Tests unitaires passent
- Ne JAMAIS créer de commits Git
