---
name: framework:make:factory
description: Génère Factory Foundry pour tests
license: MIT
version: 1.0.0
---

# Framework Make Factory Skill

## Description
Génère une Factory Foundry pour créer facilement des instances d'entités dans les tests.

La Factory utilise Zenstruck Foundry et respecte les principes Elegant Objects en utilisant la factory statique `create()` de l'entité.

## Usage
```
Use skill framework:make:factory

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
```

## Templates
- `Factory/UtilisateurFactory.php` - Template de factory Foundry

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)
- **{properties}** - Liste des propriétés de l'entité pour `defaults()`

## Dépendances
- Requiert que l'entité existe dans `src/Entity/{EntityName}.php`
- Requiert Zenstruck Foundry installé

## Outputs
- `src/Factory/{EntityName}Factory.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Lire l'entité pour détecter les propriétés du constructeur `create()`
4. Générer la factory depuis le template :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
   - Générer `defaults()` avec valeurs par défaut pour chaque propriété
   - Générer `instantiateWith()` appelant `Entity::create()`
5. Afficher le fichier créé

## Patterns appliqués

### Classe Factory
- Extends PersistentObjectFactory
- Classe `final`
- Méthode statique `class()` retournant le FQCN de l'entité
- Méthode `defaults()` avec valeurs par défaut des propriétés
- Méthode `initialize()` avec `instantiateWith()` appelant `Entity::create()`
- Méthodes custom (ex: `withSpecificId()`)

## Exemple

```bash
Use skill framework:make:factory

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Factory/ProductFactory.php
```

Fichier généré :
```php
<?php

declare(strict_types=1);

namespace App\Factory;

use App\Entity\Product;
use Symfony\Component\Uid\Uuid;
use Zenstruck\Foundry\Persistence\PersistentObjectFactory;

/**
 * @extends PersistentObjectFactory<Product>
 */
final class ProductFactory extends PersistentObjectFactory
{
    public static function class(): string
    {
        return Product::class;
    }

    protected function defaults(): array|callable
    {
        return [
            'id' => Uuid::v4(),
            'name' => self::faker()->words(3, true),
            'price' => self::faker()->randomFloat(2, 10, 1000),
            'stock' => self::faker()->numberBetween(0, 100),
            'isActive' => true,
        ];
    }

    protected function initialize(): static
    {
        return $this
            ->instantiateWith(function (array $attributes) {
                return Product::create(
                    id: $attributes['id'],
                    name: $attributes['name'],
                    price: $attributes['price'],
                    stock: $attributes['stock'],
                    isActive: $attributes['isActive'],
                );
            })
        ;
    }

    public function withSpecificId(string $uuid): self
    {
        return $this->with([
            'id' => Uuid::fromString($uuid),
        ]);
    }

    public function inactive(): self
    {
        return $this->with(['isActive' => false]);
    }

    public function outOfStock(): self
    {
        return $this->with(['stock' => 0]);
    }
}
```

## Usage dans les tests

### Création simple
```php
// Crée et persiste en DB
$product = ProductFactory::createOne();

// Crée plusieurs instances
$products = ProductFactory::createMany(10);

// Crée sans persister
$product = ProductFactory::new()->withoutPersisting()->create();
```

### Personnalisation
```php
// Override propriétés
$product = ProductFactory::createOne([
    'name' => 'Custom Product',
    'price' => 99.99,
]);

// Méthodes custom
$product = ProductFactory::new()
    ->withSpecificId('018d5e5e-5e5e-7e5e-ae5e-5e5e5e5e5e5e')
    ->inactive()
    ->createOne();

$product = ProductFactory::new()->outOfStock()->createOne();
```

### Dans les tests
```php
final class ProductTest extends TestCase
{
    public function testCannotDecreaseStockWhenOutOfStock(): void
    {
        $product = ProductFactory::new()->outOfStock()->createOne();

        $this->expectException(\DomainException::class);
        $product->decreaseStock(1);
    }

    public function testInactiveProductsCannotBePurchased(): void
    {
        $product = ProductFactory::new()->inactive()->createOne();

        $this->expectException(\DomainException::class);
        $product->purchase(1);
    }
}
```

## Valeurs par défaut recommandées

### Types courants
```php
// Strings
'name' => self::faker()->words(3, true),
'email' => self::faker()->email(),
'description' => self::faker()->paragraph(),

// Nombres
'price' => self::faker()->randomFloat(2, 10, 1000),
'quantity' => self::faker()->numberBetween(1, 100),
'stock' => self::faker()->numberBetween(0, 50),

// Booleans
'isActive' => true,
'isPublished' => self::faker()->boolean(),

// Dates
'createdAt' => \DateTimeImmutable::createFromMutable(self::faker()->dateTime()),

// UUID
'id' => Uuid::v4(),
```

## Méthodes custom recommandées

```php
// Par ID spécifique
public function withSpecificId(string $uuid): self
{
    return $this->with(['id' => Uuid::fromString($uuid)]);
}

// États métier
public function active(): self
{
    return $this->with(['isActive' => true]);
}

public function inactive(): self
{
    return $this->with(['isActive' => false]);
}

// Valeurs spécifiques
public function expensive(): self
{
    return $this->with(['price' => self::faker()->randomFloat(2, 500, 2000)]);
}

public function cheap(): self
{
    return $this->with(['price' => self::faker()->randomFloat(2, 1, 50)]);
}
```

## Notes
- Utilise `instantiateWith()` pour appeler la factory statique `create()` de l'entité
- Respecte le principe Elegant Objects (pas de `new Entity()` direct)
- Faker disponible via `self::faker()`
- Méthodes custom uniquement si demandées explicitement (YAGNI)
- Factory persiste par défaut, utiliser `withoutPersisting()` si besoin
