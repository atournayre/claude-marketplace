---
name: framework:make:entity
description: Génère une entité Doctrine avec repository selon principes Elegant Objects
license: MIT
version: 1.0.0
---

# Framework Make Entity Skill

## Description
Génère une entité Doctrine complète avec son repository selon les principes Elegant Objects.

L'entité générée inclut :
- Constructeur privé avec factory statique `create()`
- Traits Elegant Objects (DatabaseTrait, NullTrait, DependencyInjectionTrait)
- Implémentation des interfaces de contrats
- Repository avec interface

## Usage
```
Use skill framework:make:entity

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
- Les propriétés avec leurs types (ex: name:string, email:string, isActive:bool)
```

## Templates
- `Entity/Utilisateur.php` - Template d'entité
- `Repository/UtilisateurRepository.php` - Template de repository
- `Repository/UtilisateurRepositoryInterface.php` - Template d'interface repository

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)
- **{properties}** - Liste des propriétés avec types (array)

## Dépendances
- Requiert que les Contracts soient présents
- Appelle automatiquement `framework:make:contracts` si les interfaces n'existent pas

## Outputs
- `src/Entity/{EntityName}.php`
- `src/Repository/{EntityName}Repository.php`
- `src/Repository/{EntityName}RepositoryInterface.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Demander les propriétés (nom, type, nullable)
3. Vérifier si `src/Contracts/` existe
   - Si non : appeler `framework:make:contracts`
4. Générer l'entité depuis le template :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
   - Générer les propriétés dans le constructeur
   - Générer les méthodes getter pour chaque propriété
5. Générer le repository et son interface
6. Afficher le résumé des fichiers créés

## Patterns appliqués

### Entité
- Classe `final`
- Constructeur privé
- Factory statique `create()` pour instanciation
- Traits : DatabaseTrait, NullTrait, DependencyInjectionTrait
- Attributs Doctrine ORM (#[ORM\Entity], #[ORM\Id], #[ORM\Column])
- Implémentation des interfaces :
  - LoggableInterface
  - DatabaseEntityInterface
  - NullableInterface
  - DependencyInjectionAwareInterface
  - OutInterface
  - HasUrlsInterface
  - InvalideInterface

### Repository
- Classe `final`
- Extends ServiceEntityRepository
- Implémente l'interface du repository
- Constructeur avec ManagerRegistry uniquement

## Exemple

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

## Notes
- L'ID de type Uuid est ajouté automatiquement
- Les propriétés sont toujours privées avec getters
- Pas de setters (immutabilité)
- La méthode `toLog()` inclut automatiquement toutes les propriétés
