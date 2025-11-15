# Framework Make Factory

Génère une Factory Foundry pour tests.

## Vue d'ensemble
Cette skill crée une Factory Zenstruck Foundry pour générer facilement des instances d'entités dans les tests selon les principes Elegant Objects.

## Caractéristiques

### Classe Factory générée
- Extends PersistentObjectFactory
- Classe `final`
- Méthode `class()` retournant le FQCN
- Méthode `defaults()` avec valeurs Faker
- Méthode `initialize()` utilisant `instantiateWith()`
- Appelle la factory statique `Entity::create()`
- Méthode `withSpecificId()` par défaut

## Utilisation

```bash
Use skill framework:make:factory
```

Vous serez invité à fournir le nom de l'entité.

## Exemple d'utilisation

```bash
EntityName: Product
```

Génère :
```php
// src/Factory/ProductFactory.php
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
                );
            });
    }

    public function withSpecificId(string $uuid): self
    {
        return $this->with([
            'id' => Uuid::fromString($uuid),
        ]);
    }
}
```

## Structure créée

```
src/
└── Factory/
    └── {EntityName}Factory.php
```

## Prérequis
- L'entité doit exister dans `src/Entity/{EntityName}.php`
- Zenstruck Foundry installé

## Usage dans les tests

### Création basique
```php
use App\Factory\ProductFactory;

// Créer et persister une instance
$product = ProductFactory::createOne();

// Créer plusieurs instances
$products = ProductFactory::createMany(10);

// Créer sans persister
$product = ProductFactory::new()->withoutPersisting()->create();
```

### Personnalisation
```php
// Override propriétés
$product = ProductFactory::createOne([
    'name' => 'Mon Produit',
    'price' => 99.99,
]);

// Enchaînement
$product = ProductFactory::new()
    ->withSpecificId('018d5e5e-5e5e-7e5e-ae5e-5e5e5e5e5e5e')
    ->with(['name' => 'Custom'])
    ->createOne();
```

### Tests unitaires
```php
final class ProductTest extends TestCase
{
    public function testProductCanBeCreated(): void
    {
        $product = ProductFactory::createOne([
            'name' => 'Test Product',
            'price' => 50.0,
        ]);

        self::assertSame('Test Product', $product->name());
        self::assertSame(50.0, $product->price());
    }

    public function testCannotHaveNegativePrice(): void
    {
        $this->expectException(\InvalidArgumentException::class);

        ProductFactory::createOne(['price' => -10.0]);
    }
}
```

### Tests fonctionnels
```php
final class ProductControllerTest extends WebTestCase
{
    public function testListProducts(): void
    {
        ProductFactory::createMany(5);

        $client = static::createClient();
        $client->request('GET', '/products');

        self::assertResponseIsSuccessful();
        self::assertSelectorTextContains('h1', 'Products');
    }
}
```

## Enrichissement (principe YAGNI)

Ajouter méthodes custom **uniquement si demandées** :

```php
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
    return $this->with([
        'price' => self::faker()->randomFloat(2, 500, 2000)
    ]);
}

public function outOfStock(): self
{
    return $this->with(['stock' => 0]);
}

// Relations
public function withCategory(Category $category): self
{
    return $this->with(['category' => $category]);
}
```

## Valeurs par défaut Faker

```php
protected function defaults(): array|callable
{
    return [
        // UUID
        'id' => Uuid::v4(),

        // Strings
        'name' => self::faker()->words(3, true),
        'email' => self::faker()->email(),
        'description' => self::faker()->paragraph(),
        'slug' => self::faker()->slug(),

        // Nombres
        'price' => self::faker()->randomFloat(2, 10, 1000),
        'quantity' => self::faker()->numberBetween(1, 100),
        'stock' => self::faker()->numberBetween(0, 50),

        // Booleans
        'isActive' => true,
        'isPublished' => self::faker()->boolean(70), // 70% true

        // Dates
        'createdAt' => \DateTimeImmutable::createFromMutable(
            self::faker()->dateTimeBetween('-1 year')
        ),

        // Arrays
        'tags' => self::faker()->words(5),

        // Relations (avec autre Factory)
        'category' => CategoryFactory::new(),
    ];
}
```

## Patterns avancés

### Factory avec relations
```php
protected function defaults(): array|callable
{
    return [
        'id' => Uuid::v4(),
        'name' => self::faker()->words(3, true),
        'category' => CategoryFactory::new(),
    ];
}

public function inCategory(Category $category): self
{
    return $this->with(['category' => $category]);
}
```

### Factory avec états complexes
```php
public function published(): self
{
    return $this
        ->with(['isPublished' => true])
        ->with(['publishedAt' => new \DateTimeImmutable()]);
}

public function draft(): self
{
    return $this
        ->with(['isPublished' => false])
        ->with(['publishedAt' => null]);
}
```

## Principes Elegant Objects appliqués
- Classe finale
- Utilise `instantiateWith()` pour appeler `Entity::create()`
- Pas de `new Entity()` direct
- Méthodes custom uniquement si demandées (YAGNI)
- Type-safe avec générique PHPDoc
