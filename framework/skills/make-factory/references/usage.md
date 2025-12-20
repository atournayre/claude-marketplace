# Usage de la Factory générée

## Création simple

```php
// Crée et persiste en DB
$product = ProductFactory::createOne();

// Crée plusieurs instances
$products = ProductFactory::createMany(10);

// Crée sans persister
$product = ProductFactory::new()->withoutPersisting()->create();
```

## Personnalisation

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

## Dans les tests

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
