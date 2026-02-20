---
name: php:make-invalide
description: Génère classe Invalide (exceptions métier)
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
version: 1.0.0
license: MIT
---

# PHP Make Invalide Skill

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


## Description
Génère une classe Invalide pour gérer les exceptions métier d'une entité avec factory methods.

## Usage
```
Use skill php:make-invalide
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Entité dans `src/Entity/{EntityName}.php`

## Outputs
- `src/Invalide/{EntityName}Invalide.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Générer la classe Invalide depuis le template `templates/Invalide/`
4. Afficher le fichier créé

## Patterns appliqués

- Classe `final`
- Constructeur privé
- Factory statique `new()` pour instanciation
- Propriété privée de type entité
- Méthodes factory statiques pour exceptions (préfixe `car`)

## References

- [Usage](references/usage.md) - Exemples d'implémentation et enrichissement

## Notes
- Les méthodes factory d'exceptions commencent par `car` (convention)
- Messages d'exception sans point final
- Messages avec maximum de contexte
- Exceptions standard PHP (\InvalidArgumentException, \DomainException)
- Principe "fail fast"
