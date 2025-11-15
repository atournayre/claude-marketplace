# Framework Make Entity

Génère une entité Doctrine avec repository selon principes Elegant Objects.

## Vue d'ensemble
Cette skill crée une entité Doctrine complète respectant les principes Elegant Objects, avec son repository et son interface.

## Caractéristiques

### Entité générée
- Constructeur privé + factory statique `create()`
- Classe `final`
- Propriétés privées avec getters uniquement
- Pas de setters (immutabilité encouragée)
- Implémentation des interfaces de contrats
- Traits Atournayre intégrés
- Attributs Doctrine ORM configurés
- Méthode `toLog()` pour LoggableInterface

### Repository généré
- Extends ServiceEntityRepository
- Classe `final`
- Interface dédiée
- Prêt pour méthodes custom

## Utilisation

```bash
Use skill framework:make:entity
```

Vous serez invité à fournir :
1. Nom de l'entité (PascalCase)
2. Liste des propriétés avec types

## Exemple d'utilisation

```bash
EntityName: Product
Properties:
  - name: string
  - description: string
  - price: float
  - stock: int
  - isActive: bool
```

Génère :
```php
// src/Entity/Product.php
final class Product implements LoggableInterface, DatabaseEntityInterface, ...
{
    use DatabaseTrait;
    use NullTrait;
    use DependencyInjectionTrait;

    private function __construct(
        #[ORM\Id]
        #[ORM\Column(type: 'uuid')]
        private Uuid $id,
        #[ORM\Column(type: 'string')]
        private string $name,
        // ...
    ) {}

    public static function create(Uuid $id, string $name, ...): self
    {
        return new self(id: $id, name: $name, ...);
    }

    public function id(): Uuid { return $this->id; }
    public function name(): string { return $this->name; }
    // ...
}
```

## Structure créée

```
src/
├── Entity/
│   └── {EntityName}.php
└── Repository/
    ├── {EntityName}Repository.php
    └── {EntityName}RepositoryInterface.php
```

## Prérequis
- Contracts doivent exister (appelle automatiquement `framework:make:contracts` si absents)
- Projet Symfony avec Doctrine ORM configuré
- Framework `atournayre/framework` installé

## Types de propriétés supportés
- Scalaires : `string`, `int`, `float`, `bool`
- UUID : `Uuid` (Symfony\Component\Uid\Uuid)
- DateTime : `\DateTimeImmutable`
- Arrays : `array`
- Relations Doctrine (à configurer manuellement après génération)

## Principes Elegant Objects appliqués
- Constructeur privé
- Factory statique pour création
- Classe finale (pas d'héritage)
- Pas de setters publics
- Propriétés privées avec getters
- Interfaces pour tous les contrats
- Immutabilité encouragée
