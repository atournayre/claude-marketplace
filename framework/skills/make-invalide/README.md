# Framework Make Invalide

Génère une classe Invalide pour exceptions métier d'une entité.

## Vue d'ensemble
Cette skill crée une classe Invalide qui encapsule les exceptions métier spécifiques à une entité selon les principes Elegant Objects.

## Caractéristiques

### Classe Invalide générée
- Classe `final`
- Constructeur privé
- Factory statique `new()`
- Encapsule l'entité
- Base pour méthodes factory d'exceptions

## Utilisation

```bash
Use skill framework:make:invalide
```

Vous serez invité à fournir le nom de l'entité.

## Exemple d'utilisation

```bash
EntityName: Product
```

Génère :
```php
// src/Invalide/ProductInvalide.php
final class ProductInvalide
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
└── Invalide/
    └── {EntityName}Invalide.php
```

## Prérequis
- L'entité doit exister dans `src/Entity/{EntityName}.php`

## Usage recommandé

### Dans l'entité
```php
final class Product implements InvalideInterface
{
    public function invalide(): ProductInvalide
    {
        return ProductInvalide::new(product: $this);
    }
}
```

### Enrichissement avec exceptions métier

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

    // Exceptions de validation
    public static function carNomVide(): \InvalidArgumentException
    {
        return new \InvalidArgumentException(
            'Le nom du produit ne peut pas être vide'
        );
    }

    public static function carPrixNegatif(): \InvalidArgumentException
    {
        return new \InvalidArgumentException(
            'Le prix ne peut pas être négatif'
        );
    }

    // Exceptions métier
    public static function carStockInsuffisant(
        int $demande,
        int $disponible
    ): \DomainException {
        return new \DomainException(
            sprintf(
                'Stock insuffisant: %d demandé, %d disponible',
                $demande,
                $disponible
            )
        );
    }

    public static function carProduitInactif(string $id): \DomainException
    {
        return new \DomainException(
            sprintf('Le produit %s est inactif', $id)
        );
    }
}
```

### Utilisation dans le code

```php
// Validation dans factory
public static function create(
    Uuid $id,
    string $name,
    float $price
): self {
    if ('' === $name) {
        throw ProductInvalide::carNomVide();
    }
    if ($price < 0) {
        throw ProductInvalide::carPrixNegatif();
    }
    return new self(id: $id, name: $name, price: $price);
}

// Validation métier
public function decreaseStock(int $quantity): void
{
    if (!$this->isActive) {
        throw ProductInvalide::carProduitInactif($this->id->toRfc4122());
    }
    if ($this->stock < $quantity) {
        throw ProductInvalide::carStockInsuffisant(
            demande: $quantity,
            disponible: $this->stock
        );
    }
    $this->stock -= $quantity;
}
```

## Conventions de nommage

### Méthodes factory
- Préfixe : `car` (français)
- Format : `carRaisonDeLErreur`
- Exemples :
  - `carNomVide()`
  - `carEmailInvalide()`
  - `carStockInsuffisant()`
  - `carProduitInactif()`

### Messages d'exception
- Pas de point final
- Inclure le contexte maximum
- Une seule phrase sans points internes
- Exemples :
  - ✅ `'Le nom du produit ne peut pas être vide'`
  - ✅ `'Stock insuffisant: 5 demandé, 2 disponible'`
  - ❌ `'Erreur.'`
  - ❌ `'Le nom est vide. Veuillez le renseigner.'`

## Types d'exceptions recommandés

- `\InvalidArgumentException` - Validation d'arguments
- `\DomainException` - Règles métier
- `\LogicException` - État incohérent
- `\RuntimeException` - Erreur runtime

## Principes Elegant Objects appliqués
- Classe finale
- Constructeur privé
- Factory statiques
- Fail fast
- Messages d'erreur avec contexte
- Exceptions spécifiques au domaine
