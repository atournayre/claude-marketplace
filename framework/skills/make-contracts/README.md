# Framework Make Contracts

Génère les interfaces de contrats pour une architecture Elegant Objects.

## Vue d'ensemble
Cette skill crée l'ensemble des interfaces nécessaires pour supporter les principes Elegant Objects et DDD dans un projet Symfony.

## Interfaces générées

### Interfaces principales
- **OutInterface** - Pour objets de sortie (DTO immuables)
- **InvalideInterface** - Pour exceptions métier
- **HasUrlsInterface** - Pour objets ayant des URLs générées

### Interfaces de data
- **OutDataInterface** - Pour data classes de sortie
- **InvalideDataInterface** - Pour data classes d'invalidation
- **UrlsDataInterface** - Pour data classes d'URLs

### Interfaces spécialisées
- **StoryInterface** - Pour stories de tests (Foundry)
- **DoctrineMigrationInterface** - Pour migrations Doctrine

## Utilisation

```bash
# Via skill
Use skill framework:make:contracts
```

## Structure créée

```
src/
└── Contracts/
    ├── OutInterface.php
    ├── InvalideInterface.php
    ├── HasUrlsInterface.php
    ├── OutDataInterface.php
    ├── InvalideDataInterface.php
    ├── UrlsDataInterface.php
    ├── Story/
    │   └── StoryInterface.php
    └── Doctrine/
        └── DoctrineMigrationInterface.php
```

## Prérequis
Aucun - C'est la première skill à exécuter dans un nouveau projet.

## Principes Elegant Objects appliqués
- Toutes les interfaces définissent des contrats clairs
- Pas de méthodes statiques
- Chaque interface a une responsabilité unique
- Favorise l'immutabilité et l'encapsulation
