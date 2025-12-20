# Usage - Make Entity

## Templates utilisés

- `Entity/Utilisateur.php` - Template d'entité
- `Repository/UtilisateurRepository.php` - Template de repository
- `Repository/UtilisateurRepositoryInterface.php` - Template d'interface repository

## Exemple d'utilisation

```bash
Use skill framework:make:entity

# Saisies utilisateur :
EntityName: Product
Properties:
  - id: Uuid
  - name: string
  - price: float
  - isActive: bool

# Résultat :
✓ src/Entity/Product.php
✓ src/Repository/ProductRepository.php
✓ src/Repository/ProductRepositoryInterface.php
```

## Génération des propriétés

Dans le workflow de génération :
1. Remplacer `{EntityName}` par le nom fourni
2. Remplacer `{entityName}` par la version camelCase
3. Générer les propriétés dans le constructeur
4. Générer les méthodes getter pour chaque propriété

## Attributs Doctrine

L'entité générée inclut automatiquement :
- `#[ORM\Entity(repositoryClass: ...)]`
- `#[ORM\Id]`
- `#[ORM\Column]` pour chaque propriété
