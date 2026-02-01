---
title: "framework"
description: "Plugin pour atournayre/framework avec commandes et intégrations"
version: "1.1.1"
---

# framework <Badge type="info" text="v1.1.1" />


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

## Task Management System

**Nouveauté v1.0.2** : Le skill orchestrateur intègre le task management system.

### Skill avec task management

| Skill | Nombre de tâches | Type de workflow |
|-------|------------------|------------------|
| `framework:make:all` | 10 tâches | Orchestration séquentielle de 8 skills |

### Fonctionnalités

- **Progression visible** : Suivi de chaque skill généré (contracts, entity, out, etc.)
- **Statuts clairs** : pending → in_progress → completed
- **Dépendances respectées** : Ordre d'exécution garanti (contracts → entity → out/invalide → etc.)
- **Workflow complet** : De la création des contracts jusqu'aux tests (factory + story)

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
