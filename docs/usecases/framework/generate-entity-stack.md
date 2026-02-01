---
title: Générer une stack entité complète
description: Génération orchestrée de Entity + Repository + Factory + Story + Tests en une commande
category: framework
plugins:
  - name: framework
    skills: [/framework:make-all, /framework:make-entity, /framework:make-factory, /framework:make-story]
  - name: qa
    skills: []
complexity: 3
duration: 10
keywords: [entity, doctrine, foundry, tests, tdd, orchestrateur]
related:
  - /usecases/framework/create-cqrs-workflow
  - /usecases/development/full-feature-workflow
---

# Générer une stack entité complète <Badge type="info" text="★★★ Avancé" /> <Badge type="tip" text="~10 min" />

## Contexte

Créer une entité Doctrine complète nécessite plusieurs fichiers : l'entité elle-même, son repository, sa factory Foundry pour les tests, sa story pour les fixtures et les tests unitaires. Faire tout ça manuellement est long et source d'oublis.

## Objectif

Générer tous les fichiers nécessaires pour une entité en une seule commande :

- ✅ Entity Doctrine avec principes Elegant Objects
- ✅ Repository avec interface
- ✅ Factory Foundry pour tests
- ✅ Story Foundry pour fixtures
- ✅ Tests unitaires (Entity + Repository)
- ✅ Configuration automatique (ORM mapping)

## Prérequis

**Plugins :**
- [framework](/plugins/framework) - Générateurs d'entités
- [qa](/plugins/qa) - Validation PHPStan

**Outils :**
- Doctrine ORM configuré
- Foundry installé (`zenstruck/foundry`)
- PHPUnit configuré

**Configuration :**
```yaml
# config/packages/doctrine.yaml
doctrine:
    orm:
        auto_mapping: true
        mappings:
            App:
                is_bundle: false
                dir: '%kernel.project_dir%/src/Entity'
                prefix: 'App\Entity'
```

## Workflow Étape par Étape

### Phase 1 : Générer la stack complète

**Commande :**
```bash
/framework:make-all Product
```

**Que se passe-t-il ?**

Claude lance un orchestrateur qui exécute 10 tâches en parallèle :

1. **Créer Entity** - `src/Entity/Product.php` avec Elegant Objects
2. **Créer Repository** - `src/Repository/ProductRepository.php`
3. **Créer RepositoryInterface** - `src/Repository/ProductRepositoryInterface.php`
4. **Créer Factory** - `tests/Factory/ProductFactory.php`
5. **Créer Story** - `tests/Story/ProductStory.php`
6. **Créer EntityTest** - `tests/Entity/ProductTest.php`
7. **Créer RepositoryTest** - `tests/Repository/ProductRepositoryTest.php`
8. **Configurer ORM** - Ajouter mapping si nécessaire
9. **Générer migration** - `bin/console make:migration`
10. **Lancer tests** - Vérifier que tout compile

**Output attendu :**
```
✅ Task 1/10 : Entity créée (src/Entity/Product.php)
✅ Task 2/10 : Repository créé (src/Repository/ProductRepository.php)
✅ Task 3/10 : RepositoryInterface créé
✅ Task 4/10 : Factory créée (tests/Factory/ProductFactory.php)
✅ Task 5/10 : Story créée (tests/Story/ProductStory.php)
✅ Task 6/10 : EntityTest créé
✅ Task 7/10 : RepositoryTest créé
✅ Task 8/10 : ORM configuré
✅ Task 9/10 : Migration générée (Version20260201120000.php)
✅ Task 10/10 : Tests passent (8 tests, 24 assertions)

📦 Stack Product complète générée !
```

### Phase 2 : Personnaliser l'entité

Les fichiers générés utilisent des propriétés par défaut. Tu dois les personnaliser :

**Éditer `src/Entity/Product.php` :**
```php
<?php

namespace App\Entity;

use App\Repository\ProductRepositoryInterface;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ProductRepository::class)]
class Product
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private string $name;

    #[ORM\Column(type: 'decimal', precision: 10, scale: 2)]
    private string $price;

    #[ORM\Column]
    private bool $active = true;

    public function __construct(string $name, string $price)
    {
        $this->name = $name;
        $this->price = $price;
    }

    public function id(): ?int
    {
        return $this->id;
    }

    public function name(): string
    {
        return $this->name;
    }

    public function price(): string
    {
        return $this->price;
    }

    public function isActive(): bool
    {
        return $this->active;
    }

    public function activate(): void
    {
        $this->active = true;
    }

    public function deactivate(): void
    {
        $this->active = false;
    }
}
```

**Éditer `tests/Factory/ProductFactory.php` :**
```php
<?php

namespace App\Tests\Factory;

use App\Entity\Product;
use Zenstruck\Foundry\ModelFactory;

final class ProductFactory extends ModelFactory
{
    protected function getDefaults(): array
    {
        return [
            'name' => self::faker()->productName(),
            'price' => self::faker()->randomFloat(2, 1, 1000),
        ];
    }

    protected static function getClass(): string
    {
        return Product::class;
    }
}
```

### Phase 3 : Valider avec PHPStan

**Commande :**
```bash
vendor/bin/phpstan analyse src/ tests/ --level=9
```

**Output attendu :**
```
[OK] No errors
```

### Phase 4 : Lancer les tests

**Commande :**
```bash
vendor/bin/phpunit tests/Entity/ProductTest.php tests/Repository/ProductRepositoryTest.php
```

**Output attendu :**
```
OK (8 tests, 24 assertions)
```

## Exemple Complet

### Scénario : Créer entité Order avec relations

**Besoin :** Entité `Order` avec relation ManyToOne vers `User`.

**Commande :**
```bash
/framework:make-all Order
```

**Fichiers générés :**
```
src/Entity/Order.php
src/Repository/OrderRepository.php
src/Repository/OrderRepositoryInterface.php
tests/Factory/OrderFactory.php
tests/Story/OrderStory.php
tests/Entity/OrderTest.php
tests/Repository/OrderRepositoryTest.php
migrations/Version20260201120000.php
```

**Personnaliser l'entité :**

```php
#[ORM\Entity]
class Order
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(targetEntity: User::class)]
    #[ORM\JoinColumn(nullable: false)]
    private User $user;

    #[ORM\Column(type: 'decimal', precision: 10, scale: 2)]
    private string $total;

    #[ORM\Column(length: 50)]
    private string $status = 'pending';

    public function __construct(User $user, string $total)
    {
        $this->user = $user;
        $this->total = $total;
    }

    // ... getters
}
```

**Mettre à jour la Factory :**

```php
final class OrderFactory extends ModelFactory
{
    protected function getDefaults(): array
    {
        return [
            'user' => UserFactory::new(),
            'total' => self::faker()->randomFloat(2, 10, 1000),
        ];
    }

    protected static function getClass(): string
    {
        return Order::class;
    }
}
```

**Utiliser la Story dans les tests :**

```php
class OrderControllerTest extends WebTestCase
{
    public function testListOrders(): void
    {
        OrderStory::load(); // Charge 10 orders

        $client = static::createClient();
        $client->request('GET', '/api/orders');

        $this->assertResponseIsSuccessful();
        $this->assertCount(10, json_decode($client->getResponse()->getContent(), true));
    }
}
```

**Lancer les tests :**
```bash
vendor/bin/phpunit
```

**Output :**
```
OK (15 tests, 42 assertions)
```

## Variantes

### Générer seulement l'entité

```bash
/framework:make-entity Product
```

Génère uniquement `src/Entity/Product.php`.

### Générer seulement la Factory

```bash
/framework:make-factory Product
```

Génère uniquement `tests/Factory/ProductFactory.php`.

### Générer avec Collection typée

Pour une entité avec collection (ex: Order avec OrderItems) :

```bash
/framework:make-all Order
/framework:make-collection OrderItems
```

Voir [Workflow CQRS](/usecases/framework/create-cqrs-workflow).

## Troubleshooting

### Erreur "Entity already exists"

**Symptôme :** `Entity Product already exists at src/Entity/Product.php`

**Solution :**
1. Supprimer l'entité existante
2. Ou renommer l'entité : `/framework:make-all ProductV2`

### Erreur migration

**Symptôme :** `bin/console make:migration failed`

**Solution :**
1. Vérifier que Doctrine est configuré
2. Vérifier que la database existe
3. Lancer manuellement :
   ```bash
   bin/console doctrine:migrations:diff
   ```

### Tests en échec

**Symptôme :** `ProductTest::testConstructor failed`

**Solution :**
1. Vérifier que la Factory est bien configurée
2. Vérifier que les propriétés de l'entité sont correctes
3. Relancer les tests

### PHPStan erreurs

**Symptôme :** `Property Product::$name is never read`

**Solution :**

Ajouter un getter :
```php
public function name(): string
{
    return $this->name;
}
```

Ou utiliser `/qa:phpstan-resolver` pour auto-fix.

## Liens Connexes

**Use cases :**
- [Workflow CQRS](/usecases/framework/create-cqrs-workflow)
- [Module DDD](/usecases/framework/setup-ddd-module)
- [Workflow feature complet](/usecases/development/full-feature-workflow)

**Plugins :**
- [Framework](/plugins/framework)
- [QA](/plugins/qa)

**Documentation externe :**
- [Doctrine ORM](https://www.doctrine-project.org/projects/doctrine-orm/en/latest/)
- [Foundry](https://symfony.com/bundles/ZenstruckFoundryBundle/current/index.html)
- [Elegant Objects](https://www.elegantobjects.org/)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Elegant Objects** : pas de setters, constructeur avec tous les required fields
- **Immutabilité** : préférer méthodes `with*()` plutôt que setters
- **Value Objects** : utiliser des VO pour `price`, `email`, etc.
- **Repository Interface** : toujours injecter l'interface, pas la classe concrète

### 🔍 Optimisations

**Factory avancée avec états :**
```php
final class ProductFactory extends ModelFactory
{
    public function active(): self
    {
        return $this->addState(['active' => true]);
    }

    public function inactive(): self
    {
        return $this->addState(['active' => false]);
    }

    public function expensive(): self
    {
        return $this->addState(['price' => self::faker()->randomFloat(2, 500, 1000)]);
    }
}

// Usage
ProductFactory::new()->active()->expensive()->create();
```

**Story réutilisable :**
```php
final class ProductStory extends Story
{
    public function build(): void
    {
        ProductFactory::new()->active()->createMany(5);
        ProductFactory::new()->inactive()->createMany(3);
    }
}
```

### 🎯 Métriques de qualité

Une entité de qualité c'est :
- ✅ PHPStan niveau 9 vert
- ✅ 100% coverage sur Entity + Repository
- ✅ Factory avec états métiers
- ✅ Story pour fixtures réalistes
- ✅ Pas de setters (Elegant Objects)

## Checklist Validation

Avant de générer :

- [ ] Nom de l'entité en PascalCase (ex: `Product`, `OrderItem`)
- [ ] Doctrine ORM configuré
- [ ] Foundry installé
- [ ] Database créée

Après génération :

- [ ] Entity créée avec constructeur
- [ ] Repository + Interface créés
- [ ] Factory créée avec defaults
- [ ] Story créée
- [ ] Tests unitaires créés
- [ ] Migration générée
- [ ] PHPStan niveau 9 vert
- [ ] Tests passent

Avant PR :

- [ ] Factory personnalisée avec vraies données
- [ ] Story avec scénarios réalistes
- [ ] Tests couvrant tous les cas métiers
- [ ] Documentation entité à jour
