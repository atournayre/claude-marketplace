---
name: github:fix
description: Corriger une issue GitHub avec workflow simplifié et efficace
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Task]
argument-hint: [issue-number]
version: 1.0.0
license: MIT
---

# Correction d'Issue GitHub

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


## Purpose
Corriger une issue GitHub de manière structurée et efficace, en se concentrant sur l'essentiel.

## Variables
ISSUE_NUMBER: $1 (obligatoire)

## Instructions
- Utilise les outils Bash pour les opérations Git et GitHub CLI
- Focus sur la résolution rapide et efficace du problème
- Applique les standards du projet NEO

## Relevant Files
- Issues GitHub du repository
- Code source pertinent selon l'issue
- Documentation technique si nécessaire

## Workflow

### Initialisation

**Créer les tâches du workflow :**

Utiliser `TaskCreate` pour chaque phase :

```
TaskCreate #1: Analyse de l'issue
TaskCreate #2: Préparation de l'environnement (branche)
TaskCreate #3: Investigation du code
TaskCreate #4: Implémentation de la solution
TaskCreate #5: Validation et tests
TaskCreate #6: Finalisation (informer utilisateur)
```

**Important :**
- Utiliser `activeForm` (ex: "Analysant l'issue", "Implémentant la solution")
- Chaque tâche doit être marquée `in_progress` puis `completed`

**Pattern d'exécution pour chaque phase :**
1. `TaskUpdate` → tâche en `in_progress`
2. Exécuter la phase
3. `TaskUpdate` → tâche en `completed`

### Phases

### 1. Analyse de l'issue
- Récupérer les détails de l'issue via `gh issue view $ISSUE_NUMBER`
- Analyser le problème : type (bug, feature, enhancement), priorité, description
- Identifier les fichiers/modules concernés
- Vérifier les éventuels liens Sentry pour plus de contexte

### 2. Préparation de l'environnement
- Vérifier le statut git actuel
- S'assurer d'être sur la bonne branche de base (develop/main)
- Créer une branche de travail : `issue/$ISSUE_NUMBER-{description-courte}`
- Exemple : `issue/966-stockage-epuration-historique`

### 3. Investigation du code
- Localiser les fichiers concernés par l'issue
- Comprendre le code existant et identifier la cause du problème
- Analyser l'impact de la modification sur les autres parties du système
- Identifier les dépendances et side-effects potentiels

### 4. Implémentation de la solution
- Implémenter la correction en respectant :
  - Standards PHP 8.2+ avec typage strict
  - Conditions Yoda (`null === $value`)
  - Documentation des exceptions avec `@throws`
  - Conventions de nommage françaises
- Éviter les changements inutiles ou trop larges
- Maintenir la cohérence avec l'architecture existante

### 5. Validation et tests
- Exécuter les tests existants : `make run-unit-php`
- Ajouter des tests si nécessaire pour couvrir le nouveau code
- Vérifier avec PHPStan : ZÉRO erreur acceptée
- Tester la solution manuellement si applicable

### 6. Finalisation
- Informer l'utilisateur
- Ne pas faire de commit

## Task Management

**Progression du workflow :**
- 6 tâches créées à l'initialisation
- Chaque phase suit le pattern : `in_progress` → exécution → `completed`
- Utiliser `TaskList` pour voir la progression
- Les tâches permettent à l'utilisateur de suivre la résolution de l'issue

## Report
- Issue analysée avec titre et type
- Branche créée avec nom approprié
- Fichiers modifiés avec résumé des changements
- Tests exécutés avec résultats

## Validation
- ✅ `ISSUE_NUMBER` doit être fourni et exister sur GitHub
- ✅ Branche de travail créée avec convention de nommage
- ✅ Solution implémentée respectant les standards
- ✅ PHPStan passe sans erreur (CRITIQUE)
- ✅ Tests unitaires passent

## Expertise
Standards de qualité NEO :
- PHP 8.2+ avec typage strict obligatoire
- Conditions Yoda pour toutes les comparaisons
- Exceptions documentées avec `@throws`
- Nommage en français pour les concepts métier
- PHPStan niveau 9 sans erreur
- Tests unitaires pour nouveau code

## Examples
```bash
# Correction d'un bug
/github:fix 966

# Résultat attendu :
# 1. Analyse issue #966 "STOCKAGE - Épuration historique"
# 2. Création branche : issue/966-stockage-epuration-historique
# 3. Investigation du code de gestion des devis/alertes
# 4. Implémentation de l'épuration automatique
# 5. Tests et validation PHPStan
```
