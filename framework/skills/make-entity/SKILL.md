---
name: framework:make:entity
description: Génère une entité Doctrine avec repository selon principes Elegant Objects
license: MIT
version: 1.0.0
allowed-tools: [AskUserQuestion, Bash, Read, Write, Skill]
---

# Framework Make Entity Skill

Génère une entité Doctrine complète avec son repository selon les principes Elegant Objects.

## Variables
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: product)
- **{namespace}** - Namespace du projet (défaut: App)
- **{properties}** - Liste des propriétés avec types (name:string, price:float)

## Outputs
- `src/Entity/{EntityName}.php`
- `src/Repository/{EntityName}Repository.php`
- `src/Repository/{EntityName}RepositoryInterface.php`

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Demander le nom de l'entité

- Utilise AskUserQuestion pour demander :
  ```
  Question: "Quel est le nom de l'entité à créer ?"
  Header: "Entité"
  ```
- Valide que le nom est en PascalCase (première lettre majuscule)
- Stocke dans EntityName
- Génère entityName = EntityName en camelCase (première lettre minuscule)

### 2. Demander les propriétés de l'entité

- Utilise AskUserQuestion pour demander :
  ```
  Question: "Quelles sont les propriétés de l'entité ? Format: name:type,email:string,age:int"
  Header: "Propriétés"
  ```
- Parse la liste des propriétés
- Pour chaque propriété, extrais le nom et le type

### 3. Vérifier les contracts

- Exécute `ls src/Contracts/` avec Bash
- Si le répertoire n'existe pas :
  - Affiche : `⚠️  Contracts manquants - Génération automatique`
  - Utilise Skill pour appeler `framework:make:contracts`

### 4. Détecter le namespace du projet

- Lis `composer.json` avec Read
- Extrais le namespace depuis `autoload.psr-4`
- Si non trouvé, utilise `App` par défaut

### 5. Générer l'entité

- Créé le fichier `src/Entity/{EntityName}.php` avec Write
- Structure de classe :
  ```php
  namespace {namespace}\Entity;

  use Doctrine\ORM\Mapping as ORM;
  use {namespace}\Repository\{EntityName}Repository;

  #[ORM\Entity(repositoryClass: {EntityName}Repository::class)]
  final class {EntityName}
  {
      #[ORM\Id]
      #[ORM\Column(type: 'uuid', unique: true)]
      private string $id;

      // Propriétés générées depuis la liste

      private function __construct() {}

      public static function create({params}): self
      {
          $self = new self();
          $self->id = Uuid::v7();
          // Affectations des propriétés
          return $self;
      }

      // Getters pour chaque propriété
  }
  ```

### 6. Générer l'interface du repository

- Créé le fichier `src/Repository/{EntityName}RepositoryInterface.php` avec Write
- Contenu :
  ```php
  namespace {namespace}\Repository;

  interface {EntityName}RepositoryInterface
  {
      public function find(string $id): ?{EntityName};
      public function findAll(): array;
  }
  ```

### 7. Générer le repository

- Créé le fichier `src/Repository/{EntityName}Repository.php` avec Write
- Contenu :
  ```php
  namespace {namespace}\Repository;

  use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
  use Doctrine\Persistence\ManagerRegistry;
  use {namespace}\Entity\{EntityName};

  final class {EntityName}Repository extends ServiceEntityRepository implements {EntityName}RepositoryInterface
  {
      public function __construct(ManagerRegistry $registry)
      {
          parent::__construct($registry, {EntityName}::class);
      }
  }
  ```

### 8. Afficher le résumé

Affiche :
```
✅ Entité {EntityName} générée avec succès

Fichiers créés :
- src/Entity/{EntityName}.php
- src/Repository/{EntityName}Repository.php
- src/Repository/{EntityName}RepositoryInterface.php

Propriétés :
{liste des propriétés}

Prochaines étapes :
- Créer la migration : php bin/console make:migration
- Générer la factory : /framework:make:factory {EntityName}
- Générer la collection : /framework:make:collection {EntityName}
```

## Patterns appliqués

### Entité
- Classe `final`, constructeur privé, factory statique `create()`
- Traits : DatabaseTrait, NullTrait, DependencyInjectionTrait
- Interfaces : LoggableInterface, DatabaseEntityInterface, NullableInterface, DependencyInjectionAwareInterface, OutInterface, HasUrlsInterface, InvalideInterface

### Repository
- Classe `final`, extends ServiceEntityRepository
- Implémente interface du repository

## References

- [Usage](references/usage.md) - Exemples et détails de génération

## Notes
- ID Uuid ajouté automatiquement
- Propriétés privées avec getters (pas de setters)
- Méthode `toLog()` inclut toutes les propriétés
