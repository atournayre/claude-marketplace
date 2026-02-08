---
name: git:ci-autofix
description: Parse les logs CI et corrige automatiquement les erreurs
argument-hint: [pr-number]
model: opus
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, SendMessage, Bash, Read, Write, Edit, Grep, Glob]
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Parser les logs d'échec CI GitHub Actions et lancer des agents correcteurs pour résoudre automatiquement les erreurs.

# PR cible

$ARGUMENTS (numéro de PR, ou la PR courante si non spécifié)

# Workflow

## 1. Identifier la PR et les runs CI

```bash
# Si PR number fourni
PR_NUMBER=${ARGUMENTS:-$(gh pr view --json number -q '.number')}

# Récupérer les derniers runs CI en échec
gh run list --branch "$(gh pr view $PR_NUMBER --json headRefName -q '.headRefName')" --status failure --limit 5
```

## 2. Récupérer les logs d'échec

Utiliser le script `scripts/parse_ci_logs.sh` :

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/ci-autofix/scripts/parse_ci_logs.sh" "$PR_NUMBER"
```

## 3. Catégoriser les erreurs

Grouper les erreurs par type :

| Catégorie | Exemples | Agent correcteur |
|-----------|----------|-----------------|
| **Linting** | PHPStan, CS-Fixer, ESLint | `@phpstan-error-resolver` ou Edit direct |
| **Tests** | PHPUnit failures | Analyse + correction du code testé |
| **Build** | Composer install, npm build | Correction de config |
| **Types** | Type errors, missing imports | Edit direct |

## 4. Créer les tâches de correction

```
TaskCreate : "Corriger erreurs linting (X erreurs)"
TaskCreate : "Corriger erreurs tests (Y tests en échec)"
TaskCreate : "Corriger erreurs build (Z erreurs)"
```

## 5. Lancer les corrections

Pour chaque catégorie d'erreurs :

### Linting (PHPStan, CS-Fixer)
- Lancer `@phpstan-error-resolver` si erreurs PHPStan
- Lancer `vendor/bin/php-cs-fixer fix` si erreurs de style

### Tests
- Lire les tests en échec
- Analyser la cause (code ou test)
- Corriger via Edit

### Build
- Analyser les erreurs de dépendances
- Corriger composer.json / package.json si nécessaire

## 6. Re-commit et re-push

Après toutes les corrections :

```bash
git add -A
git commit -m "fix: corrections automatiques CI"
git push
```

## 7. Boucle de vérification (max 3 tentatives)

Attendre le résultat CI :

```bash
# Attendre que le dernier run termine
gh run watch --exit-status
```

- Si CI passe : terminé
- Si CI échoue encore : retour à l'étape 2 (max 3 tentatives)
- Si max tentatives atteint : rapport d'échec

# Rapport final

```
✅ CI corrigée (tentative X/3)

  Erreurs corrigées :
  - PHPStan : X erreurs
  - Tests : Y tests
  - Build : Z erreurs

  Commits ajoutés : N
  CI status : ✅ passing
```

Ou en cas d'échec :

```
❌ CI non résolue après 3 tentatives

  Erreurs restantes :
  - {liste des erreurs non résolues}

  Action requise : correction manuelle
```

# Règles

- **Max 3 tentatives** de correction
- **Ne pas supprimer de tests** pour faire passer la CI
- **Ne pas ajouter** `@phpstan-ignore*` (utiliser les vraies corrections)
- **Committer uniquement** les corrections, pas de changements non liés
- **Restriction** : demander confirmation avant le premier push
