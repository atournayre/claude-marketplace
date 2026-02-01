---
title: Setup module DDD Bounded Context
description: Architecture complète avec prompts pour créer un module DDD isolé
category: framework
plugins:
  - name: framework
    skills: []
  - name: prompt
    skills: []
complexity: 4
duration: 30
keywords: [ddd, bounded-context, architecture, hexagonal]
related:
  - /usecases/framework/generate-entity-stack
  - /usecases/framework/create-cqrs-workflow
---

# Setup module DDD Bounded Context <Badge type="info" text="★★★★ Expert" /> <Badge type="tip" text="~30 min" />

## Contexte

Domain-Driven Design (DDD) organise le code en Bounded Contexts isolés. Créer toute l'architecture (layers, ports, adapters) manuellement est long.

## Objectif

Générer un module DDD complet avec :

- ✅ Domain layer (Entities, Value Objects, Aggregates)
- ✅ Application layer (Use Cases, Commands, Queries)
- ✅ Infrastructure layer (Repositories, Adapters)
- ✅ Presentation layer (Controllers, DTOs)
- ✅ Tests pour chaque layer

## Prérequis

**Plugins :**
- [framework](/plugins/framework) - Générateurs
- [prompt](/plugins/prompt) - Templates DDD

**Outils :**
- Symfony
- Doctrine ORM

## Workflow

**Commande :**
```bash
/prompt:architecture Catalog
```

**Structure générée :**
```
src/Catalog/
├── Domain/
│   ├── Model/
│   │   ├── Product.php
│   │   └── Category.php
│   ├── ValueObject/
│   │   ├── ProductName.php
│   │   └── Price.php
│   └── Repository/
│       └── ProductRepositoryInterface.php
├── Application/
│   ├── Command/
│   │   └── CreateProductCommand.php
│   ├── Query/
│   │   └── FindProductQuery.php
│   └── Handler/
│       ├── CreateProductHandler.php
│       └── FindProductHandler.php
├── Infrastructure/
│   ├── Persistence/
│   │   └── DoctrineProductRepository.php
│   └── Adapter/
│       └── ElasticsearchProductAdapter.php
└── Presentation/
    ├── Controller/
    │   └── ProductController.php
    └── DTO/
        └── ProductDto.php
```

## Principes DDD appliqués

- **Ubiquitous Language** : termes métier partout
- **Aggregates** : cohérence transactionnelle
- **Value Objects** : immutabilité
- **Repositories** : interfaces dans Domain
- **Hexagonal Architecture** : ports & adapters

## Liens Connexes

**Use cases :**
- [Stack entité](/usecases/framework/generate-entity-stack)
- [Workflow CQRS](/usecases/framework/create-cqrs-workflow)

**Plugins :**
- [Framework](/plugins/framework)
- [Prompt](/plugins/prompt)
