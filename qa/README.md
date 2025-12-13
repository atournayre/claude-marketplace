# Plugin QA

Quality assurance : PHPStan, tests, linters.

## Installation

```bash
/plugin install qa@atournayre
```

## Commandes

### `/qa:cs-fixer`

**🔹 Skill disponible : `cs-fixer`**

Analyse et corrige automatiquement le style de code PHP avec PHP-CS-Fixer.

**Usage :**
```bash
# Analyser tout le projet
/qa:cs-fixer

# Analyser un fichier ou dossier spécifique
/qa:cs-fixer src/Domain/
```

**Workflow :**
1. Vérifie l'environnement (PHP-CS-Fixer installé, config présente)
2. Exécute dry-run pour lister les violations
3. Demande confirmation avant modification
4. Applique les corrections automatiques
5. Génère rapport détaillé des règles appliquées

**Règles supportées :**
- `@Symfony` - Règles officielles Symfony (par défaut)
- `@PSR12` - Standard PSR-12
- `@PhpCsFixer` - Règles supplémentaires PHP-CS-Fixer

**Types de corrections :**

**Imports :**
```php
// Avant
use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use App\Repository\UserRepository;

// Après (triés alphabétiquement)
use App\Entity\User;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
```

**Syntaxe array :**
```php
// Avant
$data = array('key' => 'value');

// Après
$data = ['key' => 'value'];
```

**Espacement :**
```php
// Avant
function test($a,$b){return $a+$b;}

// Après
function test($a, $b)
{
    return $a + $b;
}
```

**Rapport :**
```
📊 Rapport des corrections:

📝 src/Entity/User.php
   Règles appliquées: ordered_imports, array_syntax, trailing_comma_in_multiline

📝 src/Service/UserService.php
   Règles appliquées: single_quote, no_unused_imports

📈 Règles les plus appliquées:
  - ordered_imports: 15 fois
  - trailing_comma_in_multiline: 12 fois
  - no_unused_imports: 8 fois

═══════════════════════════════════════════════
📋 Résumé PHP-CS-Fixer
═══════════════════════════════════════════════

   Fichiers analysés: 45
   Fichiers corrigés: 12
   Durée: 3s

💡 Conseil: Vérifiez les modifications avec 'git diff'
```

---

### `/qa:phpstan`

**🔹 Skill disponible : `phpstan-resolver`**

Résout les erreurs PHPStan en utilisant l'agent `phpstan-error-resolver`.

**Usage :**
```bash
/qa:phpstan
```

**Workflow :**
1. Exécute PHPStan niveau 9 (format JSON)
2. Parse et groupe les erreurs par fichier
3. Boucle de résolution (max 10 itérations) :
   - Batch de 5 erreurs par fichier par itération
   - Délégation à agent `@phpstan-error-resolver`
   - Corrections via Edit tool
   - Re-exécution PHPStan pour vérification
4. Détection de stagnation (erreurs qui ne diminuent plus)
5. Rapport final avec :
   - Nombre erreurs initial/final
   - Erreurs corrigées
   - Taux de succès
   - Fichiers avec erreurs restantes

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

---

### `/qa:elegant-objects`

**🔹 Skill disponible : `elegant-objects`**

Vérifie la conformité du code PHP aux principes Elegant Objects de Yegor Bugayenko.

**Usage :**
```bash
/qa:elegant-objects [fichier.php]
```

**Arguments :**
- `fichier.php` (optionnel) : Fichier spécifique à analyser
- Sans argument : analyse tous les fichiers PHP modifiés dans la branche

**Exemples :**
```bash
# Fichier spécifique
/qa:elegant-objects src/Domain/User.php

# Tous les fichiers modifiés
/qa:elegant-objects
```

**Règles vérifiées :**

**Conception des classes :**
- Classes `final` (sauf abstraites)
- Max 4 attributs par classe
- Pas de getters/setters
- Pas de méthodes statiques
- Pas de noms en -er (Manager, Handler, Helper...)
- Constructeur unique avec affectations simples

**Méthodes :**
- Pas de retour `null`
- Pas d'argument `null`
- Corps sans lignes vides ni commentaires inline
- Séparation CQRS (commandes void / queries avec retour)

**Style :**
- Messages d'erreur sans point final
- Fail fast (exceptions au plus tôt)

**Tests :**
- Une assertion par test
- Pas de setUp/tearDown
- Noms français décrivant le comportement

**Rapport :**
```
## Score de conformité Elegant Objects

Score global: 75/100

## Violations critiques (bloquantes)

### Classes non-final
- **Fichier:** src/User.php:12
- **Problème:** Classe User non déclarée final
- **Suggestion:** final class User

## Statistiques

- Fichiers analysés: 5
- Classes analysées: 8
- Total violations: 12
```

## Skills Disponibles

### `cs-fixer`

**Localisation :** `skills/cs-fixer/`

Skill spécialisé pour l'analyse et la correction automatique du style de code PHP avec PHP-CS-Fixer.

**Fonctionnalités :**
- Analyse dry-run avant modification
- Support des règles @Symfony, @PSR12, @PhpCsFixer
- Demande de confirmation avant correction
- Rapport détaillé des règles appliquées
- Statistiques des règles les plus utilisées
- Support des configurations personnalisées

**Configuration :**
- `CS_FIXER_BIN`: ./vendor/bin/php-cs-fixer
- `CS_FIXER_CONFIG`: .php-cs-fixer.dist.php ou .php-cs-fixer.php

**Modèle :** sonnet

**Outils :** Bash, Read, Grep, Glob, TodoWrite

---

### `phpstan-resolver`

**Localisation :** `skills/phpstan-resolver/`

Skill spécialisé pour la résolution automatique des erreurs PHPStan. Utilisé automatiquement par `/qa:phpstan`.

**Fonctionnalités :**
- Boucle de résolution itérative (max 10 itérations)
- Batch processing (5 erreurs/fichier/itération)
- Détection de stagnation automatique
- Rapport détaillé avec taux de succès
- Support PHPStan format JSON
- Délégation à agent `@phpstan-error-resolver` pour corrections

**Configuration :**
- `ERROR_BATCH_SIZE`: 5
- `MAX_ITERATIONS`: 10
- `PHPSTAN_CONFIG`: phpstan.neon ou phpstan.neon.dist

**Modèle :** opus-4

**Outils :** Task, Bash, Read, Edit, Grep, Glob, TodoWrite

---

### `elegant-objects`

**Localisation :** `skills/elegant-objects/`

Skill spécialisé pour vérifier la conformité aux principes Elegant Objects de Yegor Bugayenko.

**Fonctionnalités :**
- Analyse fichier spécifique ou fichiers modifiés dans la branche
- Règles de conception (final, max 4 attributs, pas de getters/setters)
- Règles de méthodes (pas de null, CQRS)
- Règles de style (messages, fail fast)
- Règles de tests (une assertion, noms français)
- Score de conformité sur 100
- Rapport détaillé avec suggestions de correction

**Calcul du score :**
- Violation critique : -10 points
- Violation majeure : -5 points
- Recommandation : -2 points
- Score de base : 100

**Modèle :** sonnet

**Outils :** Bash, Read, Grep, Glob

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

## Configuration PHP-CS-Fixer

`.php-cs-fixer.dist.php` recommandé :
```php
<?php

$finder = (new PhpCsFixer\Finder())
    ->in(__DIR__)
    ->exclude('var')
    ->exclude('vendor')
    ->exclude('node_modules')
;

return (new PhpCsFixer\Config())
    ->setRules([
        '@Symfony' => true,
        '@Symfony:risky' => true,
        'array_syntax' => ['syntax' => 'short'],
        'declare_strict_types' => true,
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
        'trailing_comma_in_multiline' => true,
        'phpdoc_order' => true,
        'strict_param' => true,
        'strict_comparison' => true,
    ])
    ->setFinder($finder)
    ->setRiskyAllowed(true)
;
```

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
- Psalm integration
- Rector suggestions

## Licence

MIT
