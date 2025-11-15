# Framework Make Collection

Génère une classe Collection typée avec traits Atournayre.

## Vue d'ensemble
Cette skill crée une classe Collection type-safe pour gérer des ensembles d'entités selon les principes Elegant Objects.

## Caractéristiques

### Classe Collection générée
- Classe `final`
- Type-safe (collection d'objets typés)
- Interfaces Atournayre complètes
- Traits pour fonctionnalités de base
- Factory statique `asList()`
- Méthode `toLog()` pour logging

## Utilisation

```bash
Use skill framework:make:collection
```

Vous serez invité à fournir le nom de l'entité.

## Exemple d'utilisation

```bash
EntityName: Product
```

Génère :
```php
// src/Collection/ProductCollection.php
final class ProductCollection implements AsListInterface, ToArrayInterface, CountInterface, ...
{
    use Collection;
    use Collection\ToArray;
    use Collection\Countable;

    public static function asList(array $collection): self
    {
        return new self(PrimitiveCollection::of($collection));
    }

    public function toLog(): array
    {
        return [
            'count' => $this->count()->value(),
            'items' => $this->collection->map(fn (Product $item) => $item->toLog()),
        ];
    }
}
```

## Structure créée

```
src/
└── Collection/
    └── {EntityName}Collection.php
```

## Prérequis
- L'entité doit exister dans `src/Entity/{EntityName}.php`
- Framework `atournayre/framework` installé

## Interfaces implémentées

- **AsListInterface** - Factory `asList()`
- **ToArrayInterface** - Conversion en array
- **CountInterface** - Comptage d'éléments
- **CountByInterface** - Comptage conditionnel
- **AtLeastOneElementInterface** - Vérification présence
- **HasSeveralElementsInterface** - Vérification multiple
- **HasNoElementInterface** - Vérification vide
- **HasOneElementInterface** - Vérification unique
- **HasXElementsInterface** - Vérification nombre exact
- **LoggableInterface** - Support logging

## Méthodes disponibles via traits

```php
// Création
$products = ProductCollection::asList([$product1, $product2]);

// Comptage
$products->count(); // Number
$products->hasNoElement(); // bool
$products->hasOneElement(); // bool
$products->hasSeveralElements(); // bool
$products->hasAtLeastOneElement(); // bool
$products->hasXElements(5); // bool

// Comptage conditionnel
$activeCount = $products->countBy(fn (Product $p) => $p->isActive());

// Conversion
$array = $products->toArray();

// Logging
$log = $products->toLog();
```

## Enrichissement (principe YAGNI)

**IMPORTANT** : N'ajouter que les méthodes **explicitement demandées**.

### Exemple : filtrage
```php
public function active(): self
{
    return new self(
        $this->collection->filter(fn (Product $p) => $p->isActive())
    );
}

public function inStock(): self
{
    return new self(
        $this->collection->filter(fn (Product $p) => $p->stock() > 0)
    );
}
```

### Exemple : calculs
```php
public function totalPrice(): float
{
    return $this->collection
        ->map(fn (Product $p) => $p->price())
        ->reduce(fn (float $sum, float $price) => $sum + $price, 0.0);
}

public function averagePrice(): float
{
    if ($this->hasNoElement()) {
        return 0.0;
    }
    return $this->totalPrice() / $this->count()->value();
}
```

### Exemple : tri
```php
public function sortedByName(): self
{
    return new self(
        $this->collection->sort(fn (Product $a, Product $b) =>
            $a->name() <=> $b->name()
        )
    );
}

public function sortedByPriceDesc(): self
{
    return new self(
        $this->collection->sort(fn (Product $a, Product $b) =>
            $b->price() <=> $a->price()
        )
    );
}
```

### Exemple : recherche
```php
public function findById(Uuid $id): ?Product
{
    return $this->collection
        ->filter(fn (Product $p) => $p->id()->equals($id))
        ->first();
}

public function findByName(string $name): self
{
    return new self(
        $this->collection->filter(fn (Product $p) => $p->name() === $name)
    );
}
```

## Usage dans le code

### Depuis un repository
```php
final class ProductRepository extends ServiceEntityRepository
{
    public function findAllAsCollection(): ProductCollection
    {
        return ProductCollection::asList($this->findAll());
    }

    public function findActiveAsCollection(): ProductCollection
    {
        return ProductCollection::asList(
            $this->createQueryBuilder('p')
                ->where('p.isActive = true')
                ->getQuery()
                ->getResult()
        );
    }
}
```

### Dans un service
```php
final readonly class ProductService
{
    public function calculateTotalStock(ProductCollection $products): int
    {
        return $products->collection
            ->map(fn (Product $p) => $p->stock())
            ->reduce(fn (int $sum, int $stock) => $sum + $stock, 0);
    }
}
```

### Dans un contrôleur
```php
public function index(ProductRepository $repository): Response
{
    $products = $repository->findAllAsCollection();

    return $this->render('product/index.html.twig', [
        'products' => $products->active()->sortedByName(),
        'total' => $products->count()->value(),
    ]);
}
```

## Principes Elegant Objects appliqués
- Classe finale
- Factory statique
- Type-safety
- Immutabilité (nouvelles instances pour transformations)
- Pas de méthodes génériques anticipées (YAGNI)
- LoggableInterface pour observabilité
