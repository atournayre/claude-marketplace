---
name: dev:refactor-safe
description: Refactoring autonome piloté par tests — boucle refactor/test/ajust
argument-hint: <fichier-ou-dossier> [description-refactoring]
model: opus
allowed-tools: [Task, Bash, Read, Write, Edit, Grep, Glob, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Refactoring autonome en boucle piloté par les tests. Les tests DOIVENT rester verts à chaque itération.

# Cible

$ARGUMENTS

# Workflow

## 1. Snapshot : établir la baseline

Lancer tests + linting pour établir une baseline verte :

```bash
# Lancer les tests
vendor/bin/phpunit 2>&1 || true

# Lancer PHPStan
vendor/bin/phpstan analyse --no-progress 2>&1 || true

# Lancer CS-Fixer en mode dry-run
vendor/bin/php-cs-fixer fix --dry-run 2>&1 || true
```

**Si la baseline n'est PAS verte :**
- Logger les erreurs existantes
- Continuer le refactoring MAIS ne pas aggraver la situation
- Le refactoring ne doit pas introduire de NOUVELLES erreurs

Stocker les résultats :

```
baseline_test_failures: X
baseline_phpstan_errors: Y
baseline_cs_errors: Z
```

## 2. Plan : identifier les transformations

Lire les fichiers cibles et identifier les transformations à appliquer :

- Extractions de méthodes
- Renommages
- Simplifications de conditions
- Extraction de classes
- Suppression de code mort
- Amélioration de typage

Créer une tâche par transformation :

```
TaskCreate : "Extraire méthode calculateTotal depuis OrderService"
TaskCreate : "Renommer $tmp en $formattedDate dans DateHelper"
TaskCreate : "Simplifier condition imbriquée dans UserValidator"
```

## 3. Boucle de refactoring (max 5 itérations par fichier)

Pour chaque transformation :

### a. Appliquer la transformation

`TaskUpdate` → tâche en `in_progress`

Effectuer la modification via Edit.

### b. Lancer les vérifications

```bash
# Tests
vendor/bin/phpunit 2>&1

# PHPStan
vendor/bin/phpstan analyse --no-progress 2>&1
```

### c. Évaluer le résultat

- **Tests verts + PHPStan OK** : `TaskUpdate` → tâche en `completed`, passer au suivant
- **Tests cassés** : analyser l'échec
  - Si corrigeable rapidement : ajuster la correction
  - Sinon : `git checkout -- <fichier>` (revert) et passer au fichier suivant
- **Nouvelles erreurs PHPStan** : corriger ou revert

**Règle absolue :** les tests DOIVENT rester verts après chaque itération. Si un test casse et ne peut pas être corrigé, REVERT le fichier et passer au suivant.

## 4. Rapport final

```
✅ Refactoring terminé

  Transformations appliquées : X/Y
  Tests : ✅ verts (avant et après)
  PHPStan : Z erreurs avant → W erreurs après

  Transformations réussies :
  - ✅ Extraction méthode calculateTotal (OrderService.php)
  - ✅ Renommage $tmp → $formattedDate (DateHelper.php)

  Transformations revertées :
  - ⚠️ Simplification condition (UserValidator.php) : test UserValidatorTest::testEdgeCase cassé

  Fichiers modifiés :
  - src/Service/OrderService.php
  - src/Helper/DateHelper.php
```

# Règles

- **Tests VERTS obligatoires** à chaque itération
- **Max 5 itérations** par fichier
- **Revert** si tests cassés et non corrigeables
- **Pas de `@phpstan-ignore*`** dans les corrections
- **Rapport avant/après** obligatoire
- **Restriction** : ne JAMAIS créer de commits Git
