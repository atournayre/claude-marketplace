---
title: Créer une Pull Request avec QA automatique
description: Workflow standard pour créer une PR avec PHPStan, tests et review automatique
category: git-workflow
plugins:
  - name: git
    skills: [/git:pr]
  - name: qa
    skills: []
  - name: review
    skills: []
complexity: 2
duration: 15
keywords: [pr, pull-request, qa, phpstan, tests, review]
related:
  - /usecases/git-workflow/fix-pr-comments
  - /usecases/development/code-review-automation
---

# Créer une Pull Request avec QA automatique <Badge type="info" text="★★ Intermédiaire" /> <Badge type="tip" text="~15 min" />

## Contexte

Créer une Pull Request nécessite plusieurs étapes : validation du code, exécution des tests, commit propre et création de la PR sur GitHub. Faire tout ça manuellement est chronophage et source d'erreurs.

## Objectif

Créer une PR complète en une seule commande avec :
- ✅ Validation PHPStan niveau 9
- ✅ Exécution des tests unitaires
- ✅ Commit bien formaté (Conventional Commits + emoji)
- ✅ Titre et description de PR générés automatiquement
- ✅ PR créée sur GitHub

## Prérequis

**Plugins :**
- [git](/plugins/git) - Gestion des commits et PR
- [qa](/plugins/qa) - PHPStan et qualité du code
- [review](/plugins/review) - Code review automatique

**Outils :**
- Git configuré
- GitHub CLI (`gh`) installé et authentifié
- PHPStan configuré dans le projet
- Tests PHPUnit configurés

**Configuration :**
Aucune configuration particulière nécessaire.

## Workflow Étape par Étape

### Phase 1 : Créer la PR avec QA

**Commande :**
```bash
/git:pr
```

**Que se passe-t-il ?**

1. **Analyse des modifications** - Claude scanne les fichiers modifiés avec `git status` et `git diff`
2. **PHPStan niveau 9** - Validation statique stricte du code PHP
3. **Tests unitaires** - Exécution de `vendor/bin/phpunit`
4. **Génération commit** - Création d'un message au format Conventional Commits avec emoji
5. **Génération PR** - Titre et description automatiques basés sur les changements
6. **Push + création** - Push de la branche et création de la PR sur GitHub via `gh pr create`

**Output attendu :**
```
✅ PHPStan: 0 errors
✅ Tests: All passing (42 tests, 187 assertions)
✅ Commit: ✨ feat: add user authentication endpoint
✅ PR créée: https://github.com/user/repo/pull/123
```

## Exemple Complet

### Scénario : Ajouter un endpoint API

**Contexte :** Tu viens de développer un nouvel endpoint `/api/users` avec controller, tests et validation.

**Fichiers modifiés :**
- `src/Controller/UserController.php`
- `tests/Controller/UserControllerTest.php`
- `config/routes.yaml`

**Commande :**
```bash
/git:pr
```

**Résultat :**

Claude va :
1. Analyser les 3 fichiers modifiés
2. Lancer `vendor/bin/phpstan analyse --level=9`
3. Lancer `vendor/bin/phpunit`
4. Créer commit : `✨ feat(api): add user listing endpoint`
5. Créer PR avec titre : `feat(api): Add user listing endpoint`
6. Description générée :
   ```markdown
   ## Summary
   - Add UserController with GET /api/users endpoint
   - Add comprehensive unit tests
   - Configure route in routes.yaml

   ## Test Plan
   - [x] PHPStan level 9 passes
   - [x] Unit tests pass (100% coverage)
   - [ ] Manual testing with Postman
   ```

**URL de la PR :** `https://github.com/user/repo/pull/123`

## Variantes

### PR simple sans QA

Si tu veux skipper la QA (déconseillé) :
```bash
/git:commit
# Puis manuellement
gh pr create
```

### PR avec review multi-agents

Pour une review approfondie avant création :
```bash
/dev:review
/git:pr
```

Voir [Code review automatisé](/usecases/development/code-review-automation).

### PR en mode Continuous Delivery

Pour un workflow CD avec auto-merge :
```bash
/git:git-cd-pr
```

## Troubleshooting

### Erreur PHPStan

**Symptôme :** `PHPStan found 3 errors`

**Solution :**
1. Corriger les erreurs affichées
2. Relancer `/git:pr`

Ou utiliser l'auto-fix :
```bash
/qa:phpstan-resolver
/git:pr
```

Voir [Résoudre erreurs PHPStan](/usecases/development/phpstan-error-resolution).

### Tests en échec

**Symptôme :** `Tests: 2 failures`

**Solution :**
1. Lire les erreurs de test
2. Corriger le code
3. Relancer `/git:pr`

### Conflit avec la branche main

**Symptôme :** `Cannot merge: conflicts detected`

**Solution :**
```bash
/git:conflit
```

Voir [Résoudre les conflits](/usecases/git-workflow/resolve-merge-conflicts).

### GitHub CLI non authentifié

**Symptôme :** `gh: not logged in`

**Solution :**
```bash
gh auth login
```

## Liens Connexes

**Use cases :**
- [Corriger commentaires de review PR](/usecases/git-workflow/fix-pr-comments)
- [Code review automatisé](/usecases/development/code-review-automation)
- [Résoudre conflits merge](/usecases/git-workflow/resolve-merge-conflicts)

**Plugins :**
- [Git](/plugins/git)
- [QA](/plugins/qa)
- [Review](/plugins/review)

**Documentation externe :**
- [GitHub CLI - Pull Requests](https://cli.github.com/manual/gh_pr_create)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [PHPStan](https://phpstan.org/)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Toujours lancer `/git:pr`** plutôt que créer manuellement
- **Petites PR** : idéalement < 400 lignes de diff
- **Tests d'abord** : écrire les tests avant `/git:pr`
- **Rebase régulier** : garder la branche à jour avec main

### 🔍 Optimisations

- **Pre-commit hook** : ajouter PHPStan en pre-commit pour feedback immédiat
- **CI/CD** : GitHub Actions qui re-vérifie PHPStan + tests
- **Templates PR** : ajouter `.github/PULL_REQUEST_TEMPLATE.md`

### 🎯 Métriques de qualité

Une PR de qualité avec `/git:pr` c'est :
- ✅ 0 erreur PHPStan
- ✅ 100% tests passent
- ✅ Couverture de code > 80%
- ✅ Titre clair et descriptif
- ✅ Description avec test plan

## Checklist Validation

Avant de créer la PR :

- [ ] Tous les fichiers modifiés sont intentionnels
- [ ] Code refactorisé et propre (pas de `dump()`, `var_dump()`)
- [ ] Tests unitaires écrits et passent
- [ ] PHPStan niveau 9 validé
- [ ] Pas de conflits avec main
- [ ] GitHub CLI authentifié

Après création :

- [ ] PR visible sur GitHub
- [ ] CI/CD lancé
- [ ] Reviewers assignés (optionnel)
- [ ] Labels ajoutés (optionnel)
