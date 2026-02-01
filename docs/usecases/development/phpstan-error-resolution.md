---
title: Résoudre erreurs PHPStan niveau 9
description: Agent spécialisé avec auto-fix loop pour corriger automatiquement les erreurs PHPStan strictes
category: development
plugins:
  - name: qa
    skills: [/qa:phpstan-resolver]
complexity: 3
duration: 15
keywords: [phpstan, static-analysis, auto-fix, types, generics]
related:
  - /usecases/development/code-review-automation
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/development/full-feature-workflow
---

# Résoudre erreurs PHPStan niveau 9 <Badge type="info" text="★★★ Avancé" /> <Badge type="tip" text="~15 min" />

## Contexte

PHPStan niveau 9 est le niveau d'analyse statique le plus strict pour PHP. Il détecte des erreurs subtiles (types, generics, array shapes, nullabilité) mais les corriger manuellement est fastidieux et source d'erreurs.

## Objectif

Corriger automatiquement les erreurs PHPStan niveau 9 avec :

- ✅ Analyse complète du projet
- ✅ Auto-fix automatique des erreurs courantes
- ✅ Loop jusqu'à 0 erreur ou max iterations
- ✅ Préservation de la logique métier
- ✅ Tests de non-régression

## Prérequis

**Plugins :**
- [qa](/plugins/qa) - PHPStan resolver

**Outils :**
- PHPStan ≥ 1.10 installé
- Configuration `phpstan.neon` niveau 9
- Tests PHPUnit

**Configuration :**

`phpstan.neon` :
```yaml
parameters:
    level: 9
    paths:
        - src
        - tests
    ignoreErrors: []
```

## Workflow Étape par Étape

### Phase 1 : Analyser et corriger automatiquement

**Commande :**
```bash
/qa:phpstan-resolver
```

**Que se passe-t-il ?**

Claude lance un loop d'auto-fix :

1. **Analyse** - Lance `vendor/bin/phpstan analyse --level=9`
2. **Regroupement** - Groupe erreurs par type
3. **Auto-fix** - Applique corrections automatiques
4. **Validation** - Relance PHPStan pour vérifier
5. **Loop** - Répète jusqu'à 0 erreur ou 10 itérations max
6. **Tests** - Lance tests pour vérifier non-régression

**Output attendu :**
```
🔍 PHPStan Resolver - Analyse niveau 9

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Itération 1/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Erreurs détectées : 28

Regroupement par type :
- Missing type hints : 12 erreurs
- Nullable without check : 8 erreurs
- Array shape violations : 5 erreurs
- Generic type missing : 3 erreurs

🔧 Auto-fixes appliqués : 20/28

Corrections :
✅ UserRepository.php:42 - Ajout type hint
✅ OrderService.php:67 - Null check ajouté
✅ ProductController.php:24 - Array shape annotation
... (17 autres)

⚠️  Manuel requis : 8 erreurs complexes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Itération 2/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Erreurs restantes : 8

🔧 Auto-fixes appliqués : 5/8

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Itération 3/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Erreurs restantes : 3

⚠️  Erreurs complexes (intervention manuelle) :

1. UserRepository.php:125
   Error: Method return type has no value type specified in iterable type array

   Code actuel :
   public function findActive(): array

   Suggestion :
   /**
    * @return array<User>
    */
   public function findActive(): array

2. OrderService.php:89
   Error: Property OrderService::$cache has generic class Cache but does not specify its types

   Code actuel :
   private Cache $cache;

   Suggestion :
   /** @var Cache<string, Order> */
   private Cache $cache;

3. ProductController.php:156
   Error: Parameter #1 $data of method save() expects array{name: string, price: float}, array given

   Code actuel :
   $this->service->save($request->toArray());

   Suggestion : Valider shape avec assert ou créer DTO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RÉSULTAT FINAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Erreurs initiales : 28
Erreurs corrigées : 25 (89%)
Erreurs restantes : 3 (requièrent intervention manuelle)

✅ Tests : All passing (142 tests)
✅ Pas de régression détectée

Fichiers modifiés : 18
Corrections appliquées : 25

Rapport détaillé : docs/specs/phpstan-resolution-2026-02-01.md
```

## Exemple Complet

### Scénario : Projet avec 42 erreurs PHPStan niveau 9

**Erreurs initiales :**

```bash
$ vendor/bin/phpstan analyse --level=9
 42/42 [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100%

 ------ -------------------------------------------------------------------
  Line   src/Repository/UserRepository.php
 ------ -------------------------------------------------------------------
  42     Method findByEmail() has no return type specified
  67     Method findActive() return type has no value type in iterable
  89     Parameter $id has no type specified
  125    Method save() has parameter $user with generic type but no types
 ------ -------------------------------------------------------------------

 ------ -------------------------------------------------------------------
  Line   src/Service/OrderService.php
 ------ -------------------------------------------------------------------
  24     Property $repository has no type specified
  56     Method calculate() has no return type specified
  78     Parameter #1 expects Order|null, Order given (missing null check)
  102    Property $cache has generic class but does not specify types
 ------ -------------------------------------------------------------------

... (34 autres erreurs)

[ERROR] Found 42 errors
```

**Commande :**
```bash
/qa:phpstan-resolver
```

**Corrections automatiques appliquées :**

### 1. Type hints manquants (15 erreurs)

**Avant :**
```php
public function findByEmail($email)
{
    return $this->repository->findOneBy(['email' => $email]);
}
```

**Après :**
```php
public function findByEmail(string $email): ?User
{
    return $this->repository->findOneBy(['email' => $email]);
}
```

### 2. Generics manquants (8 erreurs)

**Avant :**
```php
public function findActive(): array
{
    return $this->repository->findBy(['active' => true]);
}
```

**Après :**
```php
/**
 * @return array<User>
 */
public function findActive(): array
{
    return $this->repository->findBy(['active' => true]);
}
```

### 3. Null checks manquants (12 erreurs)

**Avant :**
```php
public function process(int $orderId): void
{
    $order = $this->repository->find($orderId);
    $this->validator->validate($order); // Crash si null
}
```

**Après :**
```php
public function process(int $orderId): void
{
    $order = $this->repository->find($orderId);

    if (!$order) {
        throw new OrderNotFoundException($orderId);
    }

    $this->validator->validate($order);
}
```

### 4. Array shapes (5 erreurs)

**Avant :**
```php
public function create(array $data): Product
{
    return new Product(
        $data['name'],
        $data['price']
    );
}
```

**Après :**
```php
/**
 * @param array{name: string, price: float, active?: bool} $data
 */
public function create(array $data): Product
{
    return new Product(
        $data['name'],
        $data['price'],
        $data['active'] ?? true
    );
}
```

### 5. Collections Doctrine (2 erreurs)

**Avant :**
```php
class Order
{
    private Collection $items;
}
```

**Après :**
```php
class Order
{
    /** @var Collection<int, OrderItem> */
    private Collection $items;
}
```

**Résultat final :**
```bash
$ vendor/bin/phpstan analyse --level=9
 42/42 [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100%

 [OK] No errors

$ vendor/bin/phpunit
OK (142 tests, 487 assertions)
```

## Variantes

### Analyse d'un seul fichier

```bash
/qa:phpstan-resolver --path=src/Service/OrderService.php
```

### Mode dry-run

```bash
/qa:phpstan-resolver --dry-run
```

Affiche les corrections qui seraient appliquées sans les appliquer.

### Avec baseline

```bash
/qa:phpstan-resolver --generate-baseline
```

Génère une baseline pour ignorer temporairement les erreurs non critiques.

## Troubleshooting

### Erreurs qui reviennent après correction

**Symptôme :** Erreur corrigée à l'itération 2 mais réapparaît à l'itération 3

**Solution :**
Conflit entre corrections. Vérifier manuellement le fichier concerné.

### Tests en échec après corrections

**Symptôme :** `Tests: 3 failures after PHPStan fixes`

**Solution :**
1. Analyser les erreurs de test
2. Les corrections ont peut-être changé le comportement
3. Ajuster les tests ou les corrections

### Max iterations atteint

**Symptôme :** `Max iterations (10) reached, still 5 errors`

**Solution :**

Erreurs trop complexes pour auto-fix. Corriger manuellement :
```bash
vendor/bin/phpstan analyse --error-format=table
```

### Erreur "PHPStan not found"

**Symptôme :** `Command 'phpstan' not found`

**Solution :**
```bash
composer require --dev phpstan/phpstan
```

## Liens Connexes

**Use cases :**
- [Code review automatisé](/usecases/development/code-review-automation)
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)
- [Workflow feature complet](/usecases/development/full-feature-workflow)

**Plugins :**
- [QA](/plugins/qa)

**Documentation :**
- [PHPStan Documentation](https://phpstan.org/)
- [PHPStan Generics](https://phpstan.org/blog/generics-in-php-using-phpdocs)
- [PHPStan Baseline](https://phpstan.org/user-guide/baseline)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Niveau progressif** : commencer niveau 5, puis 7, puis 9
- **Baseline** : utiliser baseline pour legacy code
- **Tests** : toujours lancer tests après corrections
- **CI/CD** : ajouter PHPStan en CI pour prévenir régressions

### 🔍 Optimisations

**PHPStan config optimale :**
```yaml
# phpstan.neon
parameters:
    level: 9
    paths:
        - src
        - tests

    # Extensions utiles
    symfony:
        container_xml_path: var/cache/dev/App_KernelDevDebugContainer.xml

    doctrine:
        repositoryClass: App\Repository\BaseRepository

    # Ignorer vendor
    excludePaths:
        - vendor
        - var

    # Strictness
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
```

**Pre-commit hook :**
```bash
#!/bin/bash
# .git/hooks/pre-commit

vendor/bin/phpstan analyse --level=9 --no-progress

if [ $? -ne 0 ]; then
    echo "❌ PHPStan failed"
    echo "Run: /qa:phpstan-resolver"
    exit 1
fi
```

**CI/CD GitHub Actions :**
```yaml
name: PHPStan
on: [push, pull_request]

jobs:
  phpstan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: php-actions/composer@v6
      - name: PHPStan
        run: vendor/bin/phpstan analyse --level=9 --error-format=github
```

### 🎯 Métriques de qualité

Un code PHPStan niveau 9 compliant c'est :
- ✅ 0 erreur PHPStan
- ✅ Tous les types explicites
- ✅ Generics sur collections
- ✅ Array shapes documentés
- ✅ Null checks systématiques

### 📊 Types d'erreurs courants

**Fréquence des erreurs :**
- Type hints manquants : 35%
- Generics manquants : 25%
- Null checks manquants : 20%
- Array shapes : 10%
- Autres : 10%

**Temps de résolution moyen :**
- 10 erreurs : ~2 min
- 50 erreurs : ~10 min
- 100 erreurs : ~20 min
- 500+ erreurs : utiliser baseline + résolution progressive

## Checklist Validation

Avant de lancer :

- [ ] PHPStan installé
- [ ] phpstan.neon configuré niveau 9
- [ ] Tests écrits et passent
- [ ] Commit récent (pour rollback si besoin)

Pendant la résolution :

- [ ] Loop d'auto-fix lancé
- [ ] Corrections appliquées progressivement
- [ ] Tests lancés après chaque itération
- [ ] Pas de régression détectée

Après résolution :

- [ ] PHPStan niveau 9 : 0 erreurs
- [ ] Tests passent
- [ ] Pas de régression
- [ ] Commit des corrections
- [ ] CI/CD vert
