---
name: framework:make:story
description: Génère Story Foundry pour fixtures de tests
license: MIT
version: 1.0.0
---

# Framework Make Story Skill

## Description
Génère une Story Foundry pour créer des fixtures de tests complexes avec des scénarios prédéfinis.

La Story orchestre la création de multiples instances d'entités via les Factories et permet de charger des jeux de données cohérents pour les tests.

## Usage
```
Use skill framework:make:story

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
```

## Templates
- `Story/UtilisateurStory.php` - Template de story pour une entité
- `Story/AppStory.php` - Template de story globale (créé si absent)

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Requiert que l'entité existe dans `src/Entity/{EntityName}.php`
- Appelle automatiquement `framework:make:factory` si la Factory n'existe pas
- Requiert que les Contracts existent (StoryInterface)

## Outputs
- `src/Story/{EntityName}Story.php`
- `src/Story/AppStory.php` (si n'existe pas déjà)

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Vérifier que la Factory existe dans `src/Factory/{EntityName}Factory.php`
   - Si non : appeler `framework:make:factory`
4. Générer la Story depuis le template :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
5. Vérifier si `src/Story/AppStory.php` existe
   - Si non : créer AppStory avec le template
   - Si oui : ajouter `{EntityName}Story::load();` dans la méthode `build()`
6. Afficher les fichiers créés

## Patterns appliqués

### Classe Story
- Extends Story
- Implements StoryInterface
- Classe `final`
- Méthode `build()` créant les fixtures
- Utilise les Factories pour créer les instances
- Scénarios de tests prédéfinis

### Classe AppStory
- Extends Story
- Implements StoryInterface
- Classe `final`
- Attribut #[AsFixture(name: 'main')]
- Méthode `build()` chargeant toutes les stories
- Point d'entrée unique pour charger toutes les fixtures

## Exemple

```bash
Use skill framework:make:story

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Story/ProductStory.php
✓ src/Story/AppStory.php (updated)
```

Fichiers générés :

```php
// src/Story/ProductStory.php
<?php

declare(strict_types=1);

namespace App\Story;

use App\Contracts\Story\StoryInterface;
use App\Factory\ProductFactory;
use Zenstruck\Foundry\Story;

final class ProductStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Produit par défaut
        ProductFactory::createOne();

        // Produits avec IDs spécifiques pour les tests
        ProductFactory::new()
            ->withSpecificId('01234567-89ab-cdef-0123-456789abcdef')
            ->create();

        // Créer plusieurs produits
        ProductFactory::createMany(10);
    }
}

// src/Story/AppStory.php
<?php

namespace App\Story;

use App\Contracts\Story\StoryInterface;
use Zenstruck\Foundry\Attribute\AsFixture;
use Zenstruck\Foundry\Story;

#[AsFixture(name: 'main')]
final class AppStory extends Story implements StoryInterface
{
    public function build(): void
    {
        ProductStory::load();
    }
}
```

## Usage dans les tests

### Charger la story
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

### Charger toutes les stories
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

### Fixture Doctrine
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
