# Framework Make Out

Génère une classe Out (DTO immuable pour output).

## Vue d'ensemble
Cette skill crée une classe Out qui sert de Data Transfer Object immuable pour exposer les données d'une entité vers l'extérieur.

## Caractéristiques

### Classe Out générée
- Classe `final readonly` (PHP 8.2+)
- Constructeur privé
- Factory statique `new()`
- Encapsule l'entité
- Complètement immuable
- Couche anti-corruption

## Utilisation

```bash
Use skill framework:make:out
```

Vous serez invité à fournir le nom de l'entité.

## Exemple d'utilisation

```bash
EntityName: Product
```

Génère :
```php
// src/Out/ProductOut.php
final readonly class ProductOut
{
    private function __construct(
        private Product $product,
    ) {}

    public static function new(Product $product): self
    {
        return new self(product: $product);
    }
}
```

## Structure créée

```
src/
└── Out/
    └── {EntityName}Out.php
```

## Prérequis
- L'entité doit exister dans `src/Entity/{EntityName}.php`
- PHP 8.2+ pour readonly classes

## Usage recommandé

### Dans l'entité
```php
final class Product implements OutInterface
{
    public function out(): ProductOut
    {
        return ProductOut::new(product: $this);
    }
}
```

### Dans un contrôleur
```php
#[Route('/api/products/{id}', methods: ['GET'])]
public function show(Product $product): JsonResponse
{
    return $this->json($product->out());
}
```

### Ajout de méthodes exposées
```php
final readonly class ProductOut
{
    private function __construct(
        private Product $product,
    ) {}

    public static function new(Product $product): self
    {
        return new self(product: $product);
    }

    public function id(): string
    {
        return $this->product->id()->toRfc4122();
    }

    public function name(): string
    {
        return $this->product->name();
    }

    public function formattedPrice(): string
    {
        return number_format($this->product->price(), 2) . ' €';
    }
}
```

## Principes Elegant Objects appliqués
- Classe finale
- Constructeur privé
- Factory statique
- Immutabilité totale (readonly)
- Encapsulation de l'entité
- Pas de getters bruts, méthodes métier
