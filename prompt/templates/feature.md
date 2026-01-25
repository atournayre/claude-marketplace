# Feature : {FEATURE_NAME}

**Projet** : {PROJECT_NAME}
**Entité** : {ENTITY_NAME}
**Bounded Context** : {BOUNDED_CONTEXT}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

Développer une nouvelle feature métier pour {ENTITY_NAME} dans le bounded context {BOUNDED_CONTEXT}.

### Besoin Métier

[Décrire le besoin métier en 2-3 phrases]

### Scope

**Inclus** :
- Entité {ENTITY_NAME} avec Repository et Collection
- Messages CQRS (Command + Query si nécessaire)
- Handlers asynchrones
- Tests unitaires avec Foundry
- Validation métier

**Exclus** :
- [Lister ce qui n'est pas dans le scope]

## Architecture

### Pattern DDD

```
{BOUNDED_CONTEXT}/
├── Entity/
│   └── {ENTITY_NAME}.php (final readonly)
├── Repository/
│   ├── {ENTITY_NAME}RepositoryInterface.php
│   └── {ENTITY_NAME}Repository.php
├── Collection/
│   └── {ENTITY_NAME}Collection.php
└── ValueObject/
    └── [Value Objects spécifiques]
```

### Pattern CQRS

```
Application/
├── Message/
│   ├── Command/
│   │   └── Create{ENTITY_NAME}Command.php
│   └── Query/
│       └── Get{ENTITY_NAME}Query.php
└── Handler/
    ├── Command/
    │   └── Create{ENTITY_NAME}Handler.php (async)
    └── Query/
        └── Get{ENTITY_NAME}Handler.php
```

### Elegant Objects Principles

Chaque entité doit respecter :
- Constructeur privé
- Factory statique (ex: `{ENTITY_NAME}::create()`)
- Classes `final readonly`
- Pas de setters (immutabilité)
- Value Objects pour concepts métier

## Plan d'Implémentation

### Phase 1 : Domaine (Entity + Repository)

#### 1.1 Créer l'entité {ENTITY_NAME}

**Fichier** : `src/{BOUNDED_CONTEXT}/Entity/{ENTITY_NAME}.php`

```php
namespace {NAMESPACE}\{BOUNDED_CONTEXT}\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: {ENTITY_NAME}Repository::class)]
final readonly class {ENTITY_NAME}
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private int $id;

    private function __construct(
        // Propriétés ici
    ) {
    }

    public static function create(/* params */): self
    {
        return new self(/* args */);
    }
}
```

#### 1.2 Créer le Repository

**Fichier** : `src/{BOUNDED_CONTEXT}/Repository/{ENTITY_NAME}RepositoryInterface.php`

```php
namespace {NAMESPACE}\{BOUNDED_CONTEXT}\Repository;

interface {ENTITY_NAME}RepositoryInterface
{
    public function save({ENTITY_NAME} $entity): void;
    public function findById(int $id): ?{ENTITY_NAME};
}
```

**Fichier** : `src/{BOUNDED_CONTEXT}/Repository/{ENTITY_NAME}Repository.php`

```php
namespace {NAMESPACE}\{BOUNDED_CONTEXT}\Repository;

use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;

final class {ENTITY_NAME}Repository extends ServiceEntityRepository implements {ENTITY_NAME}RepositoryInterface
{
    // Implémentation
}
```

#### 1.3 Créer la Collection

**Fichier** : `src/{BOUNDED_CONTEXT}/Collection/{ENTITY_NAME}Collection.php`

```php
namespace {NAMESPACE}\{BOUNDED_CONTEXT}\Collection;

use Atournayre\Component\Collection\AbstractTypedCollection;

final class {ENTITY_NAME}Collection extends AbstractTypedCollection
{
    protected static function type(): string
    {
        return {ENTITY_NAME}::class;
    }
}
```

### Phase 2 : Application (CQRS)

#### 2.1 Créer le Command

**Fichier** : `src/Application/Message/Command/Create{ENTITY_NAME}Command.php`

```php
namespace {NAMESPACE}\Application\Message\Command;

final readonly class Create{ENTITY_NAME}Command
{
    private function __construct(
        // Données du command
    ) {
    }

    public static function fromArray(array $data): self
    {
        return new self(/* extract data */);
    }
}
```

#### 2.2 Créer le Handler

**Fichier** : `src/Application/Handler/Command/Create{ENTITY_NAME}Handler.php`

```php
namespace {NAMESPACE}\Application\Handler\Command;

use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final readonly class Create{ENTITY_NAME}Handler
{
    public function __construct(
        private {ENTITY_NAME}RepositoryInterface $repository,
    ) {
    }

    public function __invoke(Create{ENTITY_NAME}Command $command): void
    {
        $entity = {ENTITY_NAME}::create(/* params from command */);
        $this->repository->save($entity);
    }
}
```

### Phase 3 : Tests

#### 3.1 Créer Factory Foundry

**Fichier** : `tests/Factory/{ENTITY_NAME}Factory.php`

```php
namespace {NAMESPACE}\Tests\Factory;

use Zenstruck\Foundry\ModelFactory;

final class {ENTITY_NAME}Factory extends ModelFactory
{
    protected function getDefaults(): array
    {
        return [
            // Defaults
        ];
    }

    protected static function getClass(): string
    {
        return {ENTITY_NAME}::class;
    }
}
```

#### 3.2 Tests Unitaires

**Fichier** : `tests/{BOUNDED_CONTEXT}/Entity/{ENTITY_NAME}Test.php`

Pattern AAA (Arrange-Act-Assert)

### Phase 4 : Intégration

#### 4.1 Déclarer services

**Fichier** : `config/services.yaml`

```yaml
services:
    {NAMESPACE}\{BOUNDED_CONTEXT}\Repository\{ENTITY_NAME}RepositoryInterface:
        alias: {NAMESPACE}\{BOUNDED_CONTEXT}\Repository\{ENTITY_NAME}Repository
```

#### 4.2 Configuration Messenger

**Fichier** : `config/packages/messenger.yaml`

```yaml
framework:
    messenger:
        routing:
            '{NAMESPACE}\Application\Message\Command\Create{ENTITY_NAME}Command': async
```

## Vérification

### Tests Automatisés

```bash
# PHPStan niveau 9
make phpstan

# Tests unitaires
make test

# Coverage
make coverage
```

### Tests Manuels

1. Créer une instance via factory statique
2. Persister via Repository
3. Vérifier en base de données
4. Dispatcher le Command
5. Vérifier traitement asynchrone

### Checklist Qualité

- [ ] Entité en `final readonly`
- [ ] Constructeur privé avec factory statique
- [ ] Repository avec interface
- [ ] Collection typée extends AbstractTypedCollection
- [ ] Command avec factory `fromArray()`
- [ ] Handler async (#[AsMessageHandler])
- [ ] Factory Foundry créée
- [ ] Tests unitaires AAA
- [ ] PHPStan niveau 9 : 0 erreur
- [ ] PSR-12 respecté
- [ ] Conditions Yoda utilisées
- [ ] Pas de setters (immutabilité)

## Points d'Attention

### Standards Qualité

- **PHPStan niveau 9** : Typage strict, annotations Doctrine correctes
- **Elegant Objects** : Pas de getters/setters publics, classes final readonly
- **Conditions Yoda** : `null === $value` au lieu de `$value === null`
- **TDD** : Tests écrits AVANT l'implémentation

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| Entité non immutable | Forcer `final readonly`, pas de setters |
| Handlers synchrones | Vérifier configuration messenger.yaml |
| Tests manquants | TDD obligatoire, coverage minimum 80% |
| Typage faible | PHPStan niveau 9 + annotations Doctrine |

### Patterns à Éviter

- ❌ Setters publics sur entités
- ❌ Constructeur public direct (utiliser factory)
- ❌ Handlers synchrones pour opérations métier
- ❌ Repository sans interface
- ❌ Collections non typées (array brut)

### Patterns Recommandés

- ✅ Factory statique `::create()` ou `::fromArray()`
- ✅ Value Objects pour concepts métier
- ✅ Traits pour comportements réutilisables
- ✅ Events pour communication entre bounded contexts
- ✅ Specification pattern pour requêtes complexes

## Fichiers Créés

- `src/{BOUNDED_CONTEXT}/Entity/{ENTITY_NAME}.php`
- `src/{BOUNDED_CONTEXT}/Repository/{ENTITY_NAME}RepositoryInterface.php`
- `src/{BOUNDED_CONTEXT}/Repository/{ENTITY_NAME}Repository.php`
- `src/{BOUNDED_CONTEXT}/Collection/{ENTITY_NAME}Collection.php`
- `src/Application/Message/Command/Create{ENTITY_NAME}Command.php`
- `src/Application/Handler/Command/Create{ENTITY_NAME}Handler.php`
- `tests/Factory/{ENTITY_NAME}Factory.php`
- `tests/{BOUNDED_CONTEXT}/Entity/{ENTITY_NAME}Test.php`

## Fichiers Modifiés

- `config/services.yaml`
- `config/packages/messenger.yaml`
