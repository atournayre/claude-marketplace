# Usage de la classe Collection générée

## Création d'une collection

```php
$products = ProductCollection::asList([
    $product1,
    $product2,
    $product3,
]);
```

## Méthodes disponibles (via traits)

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

## Ajout de méthodes métier (YAGNI)

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

## Interfaces implémentées

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

## Traits utilisés

- Collection
- Collection\ToArray
- Collection\Countable
