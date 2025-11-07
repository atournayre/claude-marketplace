# Plugin QA

Quality assurance : PHPStan, tests, linters.

## Installation

```bash
/plugin install qa@atournayre
```

## Commandes

### `/qa:phpstan`

Résout les erreurs PHPStan en utilisant l'agent `phpstan-error-resolver`.

**Usage :**
```bash
/qa:phpstan
```

**Workflow :**
1. Exécute PHPStan niveau 9
2. Parse les erreurs
3. Catégorise par type :
   - Types stricts
   - Annotations generics
   - Array shapes
   - Collections Doctrine
   - Null safety
4. Résout automatiquement chaque erreur
5. Vérifie corrections avec nouveau run PHPStan
6. Crée tests si nécessaire

**Types d'erreurs résolues :**

**Types stricts :**
```php
// Avant
public function process($data) { }

// Après
public function process(array $data): void { }
```

**Annotations generics :**
```php
// Avant
/** @var Collection */
private Collection $items;

// Après
/** @var Collection<int, Item> */
private Collection $items;
```

**Array shapes :**
```php
// Avant
/** @return array */
public function getData(): array { }

// Après
/** @return array{id: int, name: string} */
public function getData(): array { }
```

**Collections Doctrine :**
```php
// Avant
/** @var Collection */
private Collection $users;

// Après
/**
 * @var Collection<int, User>
 * @phpstan-var Collection<int, User>
 */
private Collection $users;
```

**Null safety :**
```php
// Avant
public function getName(): ?string
{
    return $this->user->getName();
}

// Après
public function getName(): ?string
{
    if ($this->user === null) {
        return null;
    }

    return $this->user->getName();
}
```

**Rapport :**
```
🔍 Analyse PHPStan

Erreurs trouvées : 15
- Types stricts : 5
- Generics : 4
- Array shapes : 3
- Null safety : 3

Résolution :
✅ 15/15 erreurs corrigées

Vérification :
✅ PHPStan niveau 9 passe
```

## Agent Spécialisé

### `phpstan-error-resolver`

Agent proactif qui :
- Parse output PHPStan
- Identifie patterns d'erreurs
- Applique corrections appropriées
- Vérifie conformité Elegant Objects
- Respecte immutabilité et types stricts

**Outils disponibles :**
- Read
- Edit
- Grep
- Glob
- Bash (phpstan)

## Configuration PHPStan

`phpstan.neon` recommandé :
```neon
parameters:
    level: 9
    paths:
        - src
    strictRules:
        disallowedLooseComparison: true
        booleansInConditions: true
        uselessCast: true
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
```

## Workflow Recommandé

```bash
# 1. Run PHPStan
vendor/bin/phpstan analyse

# 2. Si erreurs
/qa:phpstan

# 3. Vérification automatique
# Agent run PHPStan à nouveau

# 4. Commit
/git:commit "refactor: fix PHPStan level 9 errors"
```

## Best Practices

**Avant correction :**
- Comprendre l'erreur
- Vérifier impact
- Tests existants passent

**Pendant correction :**
- Corrections minimales
- Respect Elegant Objects
- Types stricts
- Pas de `@phpstan-ignore`

**Après correction :**
- PHPStan niveau 9 passe
- Tests passent
- Code review

## Extensions Futures

- PHPUnit coverage
- PHP-CS-Fixer
- Psalm integration
- Rector suggestions

## Licence

MIT
