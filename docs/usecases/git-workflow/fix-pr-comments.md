---
title: Corriger les commentaires de review PR
description: Skill avancée pour corriger tous les commentaires d'une PR en batch avec MultiEdit
category: git-workflow
plugins:
  - name: git
    skills: [/git:fix-pr-comments]
  - name: github
    skills: []
complexity: 3
duration: 10
keywords: [pr, review, comments, multi-edit, batch]
related:
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/development/code-review-automation
---

# Corriger les commentaires de review PR <Badge type="info" text="★★★ Avancé" /> <Badge type="tip" text="~10 min" />

## Contexte

Après une review de PR, il y a souvent plusieurs commentaires à corriger dans différents fichiers. Faire ces corrections manuellement prend du temps et on risque d'oublier certains commentaires.

## Objectif

Corriger automatiquement tous les commentaires de review d'une PR en une seule commande avec :

- ✅ Récupération automatique des commentaires GitHub
- ✅ Analyse et regroupement par fichier
- ✅ Corrections en batch avec MultiEdit
- ✅ Commit automatique des changements
- ✅ Push vers la PR

## Prérequis

**Plugins :**
- [git](/plugins/git) - Gestion des commits et PR
- [github](/plugins/github) - Interaction avec GitHub

**Outils :**
- GitHub CLI (`gh`) authentifié
- Git configuré
- PR existante avec commentaires

**Configuration :**
Aucune configuration particulière nécessaire.

## Workflow Étape par Étape

### Phase 1 : Récupérer et corriger les commentaires

**Commande :**
```bash
/git:fix-pr-comments 123
```

Où `123` est le numéro de la PR.

**Que se passe-t-il ?**

1. **Récupération des commentaires** - Via `gh pr view 123 --comments`
2. **Analyse** - Regroupement par fichier et type de correction
3. **MultiEdit** - Corrections en batch sur tous les fichiers
4. **Validation** - Vérification que tout compile
5. **Commit** - Commit avec message descriptif
6. **Push** - Push automatique vers la PR

**Output attendu :**
```
✅ 8 commentaires récupérés depuis PR #123

Corrections à appliquer :
- src/Controller/UserController.php : 3 corrections
- src/Service/EmailService.php : 2 corrections
- tests/Controller/UserControllerTest.php : 3 corrections

✅ Corrections appliquées avec MultiEdit
✅ Tests passent
✅ Commit: 🔧 fix(review): address PR #123 comments
✅ Push vers origin/feature-branch

Résumé :
- 8/8 commentaires corrigés
- 3 fichiers modifiés
- PR prête pour re-review
```

## Exemple Complet

### Scénario : PR avec 5 commentaires de review

**Contexte :** PR #87 "Add user authentication" avec commentaires sur :
1. Typo dans le nom de variable
2. Méthode trop longue à refactorer
3. Test manquant pour cas d'erreur
4. Import inutilisé à supprimer
5. Documentation à ajouter

**Commentaires GitHub :**
```
@reviewer:
src/Security/Authenticator.php:42
"Rename $usr to $user for clarity"

@reviewer:
src/Security/Authenticator.php:58
"Extract validation logic to private method"

@reviewer:
tests/Security/AuthenticatorTest.php:24
"Add test for invalid credentials case"

@reviewer:
src/Controller/AuthController.php:12
"Remove unused import Symfony\Component\HttpFoundation\Response"

@reviewer:
src/Security/Authenticator.php:15
"Add PHPDoc for authenticate() method"
```

**Commande :**
```bash
/git:fix-pr-comments 87
```

**Corrections appliquées automatiquement :**

**1. Renommage variable :**
```php
// Avant
private function validateUser($usr): bool

// Après
private function validateUser(User $user): bool
```

**2. Extraction méthode :**
```php
// Avant
public function authenticate(): Token
{
    if (!$credentials) throw new AuthException();
    if (!$this->validator->validate($credentials)) throw new AuthException();
    if (!$user = $this->repository->findByEmail($credentials->email())) {
        throw new AuthException();
    }
    // ... 10 more lines
}

// Après
public function authenticate(): Token
{
    $this->validateCredentials($credentials);
    $user = $this->findUser($credentials);
    return $this->createToken($user);
}

private function validateCredentials(Credentials $credentials): void
{
    if (!$credentials) throw new AuthException();
    if (!$this->validator->validate($credentials)) throw new AuthException();
}

private function findUser(Credentials $credentials): User
{
    $user = $this->repository->findByEmail($credentials->email());
    if (!$user) throw new AuthException();
    return $user;
}
```

**3. Test ajouté :**
```php
public function testAuthenticateWithInvalidCredentials(): void
{
    $credentials = new Credentials('invalid@example.com', 'wrong');

    $this->expectException(AuthException::class);

    $this->authenticator->authenticate($credentials);
}
```

**4. Import supprimé :**
```php
// Avant
use Symfony\Component\HttpFoundation\Response; // unused

// Après
// (supprimé)
```

**5. PHPDoc ajouté :**
```php
/**
 * Authentifie un utilisateur avec ses credentials
 *
 * @throws AuthException Si les credentials sont invalides
 */
public function authenticate(Credentials $credentials): Token
```

**Résultat :**
```
✅ 5/5 commentaires corrigés
✅ 3 fichiers modifiés
✅ Tests passent (12 tests, 42 assertions)
✅ PHPStan niveau 9 : 0 errors
✅ Commit: 🔧 fix(review): address PR #87 comments

  - Rename variable for clarity
  - Extract validation logic
  - Add missing test case
  - Remove unused import
  - Add PHPDoc

✅ Push vers origin/feature/user-auth
```

**Sur GitHub :**
```
Reviewer: @reviewer
✅ All comments addressed! LGTM 👍
```

## Variantes

### Corriger seulement certains commentaires

```bash
/git:fix-pr-comments 87 --filter="src/Security"
```

Corrige uniquement les commentaires dans `src/Security/`.

### Mode interactif

```bash
/git:fix-pr-comments 87 --interactive
```

Claude propose chaque correction et attend validation avant de l'appliquer.

### Dry-run

```bash
/git:fix-pr-comments 87 --dry-run
```

Affiche les corrections qui seraient appliquées sans les appliquer.

## Troubleshooting

### Erreur "No comments found"

**Symptôme :** `No review comments found on PR #123`

**Solution :**
1. Vérifier que la PR existe : `gh pr view 123`
2. Vérifier qu'il y a des commentaires de review (pas juste conversation)
3. S'assurer d'être authentifié : `gh auth status`

### Erreur lors de l'application

**Symptôme :** `Failed to apply correction in UserController.php:42`

**Solution :**
1. Le fichier a peut-être changé depuis le commentaire
2. Appliquer manuellement cette correction
3. Relancer avec `--skip-failed`

### Conflit après correction

**Symptôme :** `git push failed: conflicts detected`

**Solution :**
```bash
git pull --rebase origin main
# Résoudre conflits
/git:conflit
git push --force-with-lease
```

### Tests en échec après correction

**Symptôme :** `Tests: 2 failures after applying corrections`

**Solution :**
1. Analyser les erreurs de test
2. Les corrections ont peut-être cassé quelque chose
3. Ajuster manuellement
4. Ou utiliser `/dev:review` pour identifier le problème

## Liens Connexes

**Use cases :**
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)
- [Code review automatisé](/usecases/development/code-review-automation)
- [Résoudre conflits](/usecases/git-workflow/resolve-merge-conflicts)

**Plugins :**
- [Git](/plugins/git)
- [GitHub](/plugins/github)

**Documentation :**
- [GitHub CLI - PR Comments](https://cli.github.com/manual/gh_pr_comment)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Review avant merge** : toujours vérifier les corrections appliquées
- **Tests** : s'assurer que les tests passent après corrections
- **Commit message** : inclure référence à la PR (`fix(review): address PR #123 comments`)
- **Force push** : utiliser `--force-with-lease` plutôt que `--force`

### 🔍 Optimisations

**Workflow optimal :**
1. `/git:fix-pr-comments 123`
2. Review manuelle rapide des changements
3. Tests locaux : `vendor/bin/phpunit`
4. PHPStan : `vendor/bin/phpstan analyse`
5. Push si tout est vert

**GitHub Actions :**
Ajouter un workflow qui re-vérifie après corrections :
```yaml
name: Re-review after fixes
on:
  push:
    branches:
      - 'feature/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: vendor/bin/phpunit
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse
```

### 🎯 Métriques de qualité

Une correction de review réussie c'est :
- ✅ 100% des commentaires adressés
- ✅ Tests passent
- ✅ PHPStan niveau 9 vert
- ✅ Pas de régression
- ✅ Reviewer satisfait (LGTM)

## Checklist Validation

Avant de lancer :

- [ ] PR existante avec commentaires
- [ ] GitHub CLI authentifié
- [ ] Branch à jour
- [ ] Pas de changements non commités

Pendant la correction :

- [ ] Tous les commentaires récupérés
- [ ] Corrections appliquées sans erreur
- [ ] Tests passent
- [ ] PHPStan vert

Après correction :

- [ ] Commit descriptif créé
- [ ] Push réussi
- [ ] PR updated sur GitHub
- [ ] Reviewer notifié
- [ ] Ready for re-review
