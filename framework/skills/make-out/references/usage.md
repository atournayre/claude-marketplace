# Usage - Make Out

## Template utilisé

- `Out/UtilisateurOut.php` - Template de classe Out

## Exemple d'utilisation

```bash
Use skill framework:make:out

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Out/ProductOut.php
```

## Structure générée

```php
<?php

declare(strict_types=1);

namespace App\Out;

use App\Entity\Product;

final readonly class ProductOut
{
    private function __construct(
        private Product $product,
    ) {
    }

    public static function new(
        Product $product,
    ): self {
        return new self(
            product: $product,
        );
    }
}
```

## Usage dans l'entité

L'entité doit implémenter la méthode `out()` :

```php
public function out(): ProductOut
{
    return ProductOut::new($this);
}
```

## Enrichissement

La classe Out peut être enrichie avec des propriétés calculées :

```php
public function fullName(): string
{
    return $this->product->firstName() . ' ' . $this->product->lastName();
}
```
