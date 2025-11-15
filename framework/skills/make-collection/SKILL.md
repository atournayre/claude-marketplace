---
name: framework:make:collection
description: Génère classe Collection typée avec traits Atournayre
license: MIT
version: 1.0.0
---

# Framework Make Collection Skill

## Description
Génère une classe Collection typée pour gérer des ensembles d'entités avec les traits et interfaces Atournayre.

La Collection offre des méthodes pour manipuler des ensembles d'objets de manière type-safe et respectant les principes Elegant Objects.

## Usage
```
Use skill framework:make:collection

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
```

## Templates
- `Collection/UtilisateurCollection.php` - Template de classe Collection

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Requiert que l'entité existe dans `src/Entity/{EntityName}.php`
- Requiert framework `atournayre/framework`

## Outputs
- `src/Collection/{EntityName}Collection.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Générer la classe Collection depuis le template :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
4. Afficher le fichier créé

## Patterns appliqués

### Classe Collection
- Classe `final`
- Implémente interfaces Atournayre :
  - AsListInterface
  - ToArrayInterface
  - CountInterface
  - CountByInterface
  - AtLeastOneElementInterface
  - HasSeveralElementsInterface
  - HasNoElementInterface
  - HasOneElementInterface
  - HasXElementsInterface
  - LoggableInterface
- Utilise traits Atournayre :
  - Collection
  - Collection\ToArray
  - Collection\Countable
- Méthode statique `asList(array $collection)`
- Méthode `toLog()` pour logging

## Exemple

```bash
Use skill framework:make:collection

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Collection/ProductCollection.php
```

Fichier généré :
```php
<?php

declare(strict_types=1);

namespace App\Collection;

use App\Entity\Product;
use Atournayre\Contracts\Collection\AsListInterface;
use Atournayre\Contracts\Collection\AtLeastOneElementInterface;
use Atournayre\Contracts\Collection\CountByInterface;
use Atournayre\Contracts\Collection\CountInterface;
use Atournayre\Contracts\Collection\HasNoElementInterface;
use Atournayre\Contracts\Collection\HasOneElementInterface;
use Atournayre\Contracts\Collection\HasSeveralElementsInterface;
use Atournayre\Contracts\Collection\HasXElementsInterface;
use Atournayre\Contracts\Collection\ToArrayInterface;
use Atournayre\Contracts\Log\LoggableInterface;
use Atournayre\Primitives\Collection as PrimitiveCollection;
use Atournayre\Primitives\Traits\Collection;

final class ProductCollection implements AsListInterface, ToArrayInterface, CountInterface, CountByInterface, AtLeastOneElementInterface, HasSeveralElementsInterface, HasNoElementInterface, HasOneElementInterface, HasXElementsInterface, LoggableInterface
{
    use Collection;
    use Collection\ToArray;
    use Collection\Countable;

    public static function asList(array $collection): self
    {
        return new self(PrimitiveCollection::of($collection));
    }

    /**
     * @return array<string, mixed>
     */
    public function toLog(): array
    {
        return [
            'count' => $this->count()->value(),
            'items' => $this->collection->map(fn (Product $item) => $item->toLog()),
        ];
    }

    // UNIQUEMENT les méthodes EXPLICITEMENT demandées par l'utilisateur
    // PAS d'anticipation de besoins futurs
    // PAS de méthodes génériques (add, remove, filter, map, etc.)
}
```

## Usage

### Création d'une collection

```php
$products = ProductCollection::asList([
    $product1,
    $product2,
    $product3,
]);
```

### Méthodes disponibles (via traits)

```php
// Comptage
$count = $products->count(); // Atournayre\Primitives\Number
$hasElements = $products->hasNoElement(); // bool
$hasOne = $products->hasOneElement(); // bool
$hasSeveral = $products->hasSeveralElements(); // bool
$hasAtLeastOne = $products->hasAtLeastOneElement(); // bool
$hasX = $products->hasXElements(5); // bool

// Conversion
$array = $products->toArray(); // array

// Comptage personnalisé
$activeCount = $products->countBy(fn (Product $p) => $p->isActive());
```

### Ajout de méthodes métier (YAGNI)

N'ajouter que les méthodes **explicitement demandées** :

```php
final class ProductCollection implements ...
{
    // ... traits ...

    public function active(): self
    {
        return new self(
            $this->collection->filter(fn (Product $p) => $p->isActive())
        );
    }

    public function totalPrice(): float
    {
        return $this->collection
            ->map(fn (Product $p) => $p->price())
            ->reduce(fn (float $sum, float $price) => $sum + $price, 0.0);
    }
}
```

## Notes
- Respect du principe YAGNI : pas de méthodes génériques anticipées
- Seules les méthodes explicitement demandées doivent être ajoutées
- Les traits fournissent déjà beaucoup de fonctionnalités
- La collection est type-safe (typage sur l'entité)
- LoggableInterface permet le logging automatique
