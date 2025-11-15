---
name: framework:make:invalide
description: Génère classe Invalide (exceptions métier)
license: MIT
version: 1.0.0
---

# Framework Make Invalide Skill

## Description
Génère une classe Invalide pour gérer les exceptions métier d'une entité.

La classe Invalide encapsule l'entité et fournit des factory methods pour créer des exceptions spécifiques au contexte métier.

## Usage
```
Use skill framework:make:invalide

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
```

## Templates
- `Invalide/UtilisateurInvalide.php` - Template de classe Invalide

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Requiert que l'entité existe dans `src/Entity/{EntityName}.php`

## Outputs
- `src/Invalide/{EntityName}Invalide.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Générer la classe Invalide depuis le template :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
4. Afficher le fichier créé

## Patterns appliqués

### Classe Invalide
- Classe `final`
- Constructeur privé
- Factory statique `new()` pour instanciation
- Propriété privée de type entité
- Méthodes factory statiques pour exceptions spécifiques

## Exemple

```bash
Use skill framework:make:invalide

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Invalide/ProductInvalide.php
```

Fichier généré :
```php
<?php

declare(strict_types=1);

namespace App\Invalide;

use App\Entity\Product;

final class ProductInvalide
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

## Notes
- Les méthodes factory d'exceptions doivent commencer par `car` (convention)
- Les messages d'exception ne doivent pas finir par un point
- Les messages doivent inclure le maximum de contexte
- Privilégier les exceptions standard PHP (\InvalidArgumentException, \DomainException)
- Respecte le principe "fail fast"
