# Usage de la Story générée

## Charger la story dans les tests

```php
use App\Story\ProductStory;

final class ProductTest extends TestCase
{
    protected function setUp(): void
    {
        ProductStory::load();
    }

    public function testProductsAreLoaded(): void
    {
        $products = ProductFactory::repository()->findAll();

        self::assertCount(12, $products); // 1 défaut + 1 spécifique + 10 random
    }
}
```

## Charger toutes les stories

```php
use App\Story\AppStory;

final class IntegrationTest extends TestCase
{
    protected function setUp(): void
    {
        AppStory::load(); // Charge ProductStory + autres
    }
}
```

## Fixture Doctrine

```bash
# Dans config/packages/zenstruck_foundry.yaml
when@dev:
    zenstruck_foundry:
        auto_refresh_proxies: false

# Charger les fixtures
php bin/console doctrine:fixtures:load --append
```

## Enrichissement de la Story

### Scénarios complexes

```php
final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Produits actifs
        ProductFactory::new()
            ->active()
            ->createMany(5);

        // Produits inactifs
        ProductFactory::new()
            ->inactive()
            ->createMany(3);

        // Produits en rupture
        ProductFactory::new()
            ->outOfStock()
            ->createMany(2);

        // Produits premium
        ProductFactory::new()
            ->expensive()
            ->createMany(3);

        // Produit spécifique pour tests
        ProductFactory::createOne([
            'name' => 'Test Product',
            'price' => 99.99,
            'stock' => 10,
        ]);
    }
}
```

### Avec relations

```php
final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Créer catégories d'abord
        CategoryStory::load();

        $electronics = CategoryFactory::find(['name' => 'Electronics']);
        $books = CategoryFactory::find(['name' => 'Books']);

        // Produits électroniques
        ProductFactory::new()
            ->inCategory($electronics)
            ->createMany(5);

        // Livres
        ProductFactory::new()
            ->inCategory($books)
            ->createMany(10);
    }
}
```

### Avec états nommés

```php
final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // États nommés pour réutilisation dans tests
        $this->addState('premium_product', ProductFactory::createOne([
            'name' => 'Premium Product',
            'price' => 999.99,
        ]));

        $this->addState('cheap_product', ProductFactory::createOne([
            'name' => 'Cheap Product',
            'price' => 9.99,
        ]));
    }
}

// Usage dans test
$premium = ProductStory::load()->get('premium_product');
```

## AppStory orchestration

```php
#[AsFixture(name: 'main')]
final class AppStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Ordre important : dépendances d'abord
        CategoryStory::load();
        ProductStory::load();
        UserStory::load();
        OrderStory::load();
    }
}
```

## Notes

- AppStory est le point d'entrée pour charger toutes les fixtures
- Attribut #[AsFixture(name: 'main')] permet de charger via Doctrine Fixtures
- Les Stories peuvent avoir des dépendances (charger d'autres Stories)
- Méthode `addState()` permet de nommer des instances pour les tests
- Respecte le principe DRY : scénarios centralisés
