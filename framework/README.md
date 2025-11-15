# Framework Plugin

Plugin pour [atournayre/framework](https://github.com/atournayre/framework).

## Description

Fournit des skills de génération de code PHP respectant les principes Elegant Objects et DDD pour Symfony.

## Installation

Le plugin est automatiquement disponible via le marketplace atournayre-claude-plugin-marketplace.

## Skills disponibles

### Génération de code PHP Elegant Objects

- **framework:make:contracts** - Génère interfaces de contrats (OutInterface, InvalideInterface, etc.)
- **framework:make:entity** - Génère entité Doctrine + repository
- **framework:make:out** - Génère DTO immuable pour output
- **framework:make:invalide** - Génère classe exceptions métier
- **framework:make:urls** - Génère classe Urls + Message CQRS + Handler
- **framework:make:collection** - Génère collection typée
- **framework:make:factory** - Génère factory Foundry pour tests
- **framework:make:story** - Génère story Foundry pour fixtures
- **framework:make:all** - Génère stack complète pour une entité

Voir `/framework/skills/` pour documentation détaillée de chaque skill.

## Usage

```bash
# Générer une stack complète
Use skill framework:make:all

# Générer uniquement une entité
Use skill framework:make:entity

# Générer uniquement les contracts
Use skill framework:make:contracts
```

## Architecture générée

Chaque skill génère du code respectant :
- Principes Elegant Objects (Yegor Bugayenko)
- Domain-Driven Design (DDD)
- CQRS pour les queries
- Immutabilité encouragée
- Type-safety maximale

## Prérequis

Les skills génèrent du code utilisant les classes et traits de `atournayre/framework`.

Voir la documentation officielle du framework pour les dépendances exactes.

## Licence

MIT
