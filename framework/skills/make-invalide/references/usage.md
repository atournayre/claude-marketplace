# Usage de la classe Invalide générée

## Implémentation dans l'entité

L'entité doit implémenter la méthode `invalide()` :

```php
public function invalide(): ProductInvalide
{
    return ProductInvalide::new(
        product: $this,
    );
}
```

## Enrichissement avec exceptions métier

Ajouter des méthodes factory pour les cas d'erreur spécifiques :

```php
final class ProductInvalide
{
    private function __construct(
        private Product $product,
    ) {}

    public static function new(Product $product): self
    {
        return new self(product: $product);
    }

    public static function carPrixNegatif(): \InvalidArgumentException
    {
        return new \InvalidArgumentException(
            'Le prix du produit ne peut pas être négatif'
        );
    }

    public static function carStockInsuffisant(int $demande, int $disponible): \DomainException
    {
        return new \DomainException(
            sprintf(
                'Stock insuffisant: %d demandé, %d disponible',
                $demande,
                $disponible
            )
        );
    }

    public static function carNomVide(): \InvalidArgumentException
    {
        return new \InvalidArgumentException(
            'Le nom du produit ne peut pas être vide'
        );
    }
}
```

## Usage des exceptions

```php
final class Product
{
    public static function create(Uuid $id, string $name, float $price): self
    {
        if ('' === $name) {
            throw ProductInvalide::carNomVide();
        }
        if ($price < 0) {
            throw ProductInvalide::carPrixNegatif();
        }
        return new self(id: $id, name: $name, price: $price);
    }

    public function decreaseStock(int $quantity): void
    {
        if ($this->stock < $quantity) {
            throw ProductInvalide::carStockInsuffisant(
                demande: $quantity,
                disponible: $this->stock
            );
        }
        // ...
    }
}
```

## Conventions

- Les méthodes factory d'exceptions commencent par `car` (convention)
- Les messages d'exception ne finissent pas par un point
- Les messages doivent inclure le maximum de contexte
- Privilégier les exceptions standard PHP (\InvalidArgumentException, \DomainException)
- Respecter le principe "fail fast"
