# Framework Make Story

Génère une Story Foundry pour fixtures de tests.

## Vue d'ensemble
Cette skill crée une Story Zenstruck Foundry pour orchestrer la création de fixtures de tests cohérentes et réutilisables.

## Caractéristiques

### Classe Story générée
- Extends Story
- Implements StoryInterface
- Classe `final`
- Méthode `build()` avec scénarios
- Utilise Factories pour créer instances
- Scénarios prédéfinis

### Classe AppStory
- Point d'entrée global
- Attribut #[AsFixture(name: 'main')]
- Charge toutes les stories
- Gère les dépendances entre stories

## Utilisation

```bash
Use skill framework:make:story
```

Vous serez invité à fournir le nom de l'entité.

## Exemple d'utilisation

```bash
EntityName: Product
```

Génère :
```php
// src/Story/ProductStory.php
final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Produit par défaut
        ProductFactory::createOne();

        // Produits avec IDs spécifiques
        ProductFactory::new()
            ->withSpecificId('01234567-89ab-cdef-0123-456789abcdef')
            ->create();

        // Plusieurs produits
        ProductFactory::createMany(10);
    }
}

// src/Story/AppStory.php (updated)
#[AsFixture(name: 'main')]
final class AppStory extends Story implements StoryInterface
{
    public function build(): void
    {
        ProductStory::load();
        // ... autres stories
    }
}
```

## Structure créée

```
src/
└── Story/
    ├── {EntityName}Story.php
    └── AppStory.php
```

## Prérequis
- L'entité doit exister
- La Factory doit exister (créée automatiquement si absente)
- StoryInterface doit exister dans Contracts
- Zenstruck Foundry installé

## Usage dans les tests

### Tests unitaires
```php
use App\Story\ProductStory;

final class ProductServiceTest extends TestCase
{
    protected function setUp(): void
    {
        ProductStory::load();
    }

    public function testCalculateTotalPrice(): void
    {
        $products = ProductFactory::repository()->findAll();
        $service = new ProductService();

        $total = $service->calculateTotal($products);

        self::assertGreaterThan(0, $total);
    }
}
```

### Tests fonctionnels
```php
use App\Story\AppStory;

final class ProductControllerTest extends WebTestCase
{
    protected function setUp(): void
    {
        AppStory::load();
    }

    public function testListProducts(): void
    {
        $client = static::createClient();
        $client->request('GET', '/products');

        self::assertResponseIsSuccessful();
        self::assertSelectorExists('.product-item');
    }
}
```

### Fixtures Doctrine
```bash
# Charger toutes les fixtures
php bin/console doctrine:fixtures:load --append

# Ou juste AppStory via attribut #[AsFixture]
```

## Enrichissement (principe YAGNI)

### Scénarios métier
```php
final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Scénario : catalogue actif
        ProductFactory::new()
            ->active()
            ->createMany(20);

        // Scénario : produits en promotion
        ProductFactory::new()
            ->active()
            ->createMany(5, ['price' => 9.99]);

        // Scénario : rupture de stock
        ProductFactory::new()
            ->outOfStock()
            ->createMany(3);

        // Scénario : nouveau produit vedette
        ProductFactory::createOne([
            'name' => 'Featured Product',
            'price' => 199.99,
            'stock' => 100,
            'isActive' => true,
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
        // Charger dépendances
        CategoryStory::load();

        // Récupérer catégories
        $electronics = CategoryFactory::find(['name' => 'Electronics']);
        $books = CategoryFactory::find(['name' => 'Books']);

        // Produits par catégorie
        ProductFactory::new()
            ->inCategory($electronics)
            ->createMany(10);

        ProductFactory::new()
            ->inCategory($books)
            ->createMany(15);
    }
}
```

### États nommés
```php
final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // États nommés pour réutilisation
        $this->addState('premium', ProductFactory::createOne([
            'name' => 'Premium Product',
            'price' => 999.99,
        ]));

        $this->addState('cheap', ProductFactory::createOne([
            'name' => 'Cheap Product',
            'price' => 9.99,
        ]));

        $this->addState('test_product', ProductFactory::createOne([
            'id' => Uuid::fromString('01234567-89ab-cdef-0123-456789abcdef'),
        ]));
    }
}

// Usage
$premium = ProductStory::load()->get('premium');
$cheap = ProductStory::load()->get('cheap');
```

### Scénarios complexes
```php
final class OrderStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Charger dépendances
        UserStory::load();
        ProductStory::load();

        $users = UserFactory::repository()->findAll();
        $products = ProductFactory::repository()->findAll();

        // Commandes par utilisateur
        foreach ($users as $user) {
            OrderFactory::createOne([
                'user' => $user,
                'items' => array_slice($products, 0, rand(1, 5)),
            ]);
        }

        // Commande de test spécifique
        $this->addState('test_order', OrderFactory::createOne([
            'user' => UserStory::load()->get('test_user'),
            'items' => [ProductStory::load()->get('test_product')],
            'status' => 'pending',
        ]));
    }
}
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
        ReviewStory::load();
    }
}
```

## Configuration Foundry

```yaml
# config/packages/zenstruck_foundry.yaml
when@dev:
    zenstruck_foundry:
        auto_refresh_proxies: false

when@test:
    zenstruck_foundry:
        auto_refresh_proxies: false
        make_factory:
            default_namespace: 'App\Factory'
```

## Commandes utiles

```bash
# Charger fixtures
php bin/console doctrine:fixtures:load --append

# Purger DB puis charger
php bin/console doctrine:fixtures:load

# Dans tests
AppStory::load();
ProductStory::load();
```

## Principes Elegant Objects appliqués
- Classe finale
- Implements StoryInterface
- Méthode `build()` claire et concise
- Scénarios nommés explicitement
- DRY : fixtures centralisées
- États nommés pour réutilisation
