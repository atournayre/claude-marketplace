---
name: framework:make:out
description: Génère classe Out (DTO immuable pour output)
license: MIT
version: 1.0.0
---

# Framework Make Out Skill

## Description
Génère une classe Out (Data Transfer Object) immuable pour représenter les données de sortie d'une entité.

La classe Out est un DTO readonly qui encapsule une entité pour l'exposition vers l'extérieur (API, vues, etc.).

## Usage
```
Use skill framework:make:out

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
```

## Templates
- `Out/UtilisateurOut.php` - Template de classe Out

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Requiert que l'entité existe dans `src/Entity/{EntityName}.php`

## Outputs
- `src/Out/{EntityName}Out.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Générer la classe Out depuis le template :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
4. Afficher le fichier créé

## Patterns appliqués

### Classe Out
- Classe `final readonly`
- Constructeur privé
- Factory statique `new()` pour instanciation
- Propriété privée de type entité
- Objet complètement immuable

## Exemple

```bash
Use skill framework:make:out

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Out/ProductOut.php
```

Fichier généré :
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
    return ProductOut::new(
        product: $this,
    );
}
```

## Notes
- La classe Out peut être enrichie avec des méthodes pour exposer des propriétés calculées
- Elle sert de couche anti-corruption entre le domaine et l'extérieur
- Permet de contrôler finement ce qui est exposé depuis l'entité
- Respecte le principe d'immutabilité (readonly)
