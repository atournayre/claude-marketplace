---
title: "prompt"
description: "Générateur et transformateur de prompts structurés pour développement - Templates DDD/CQRS, refactoring, webhooks, architecture, transformation en prompts exécutables"
version: "1.3.1"
---

# prompt <Badge type="info" text="v1.3.1" />


Générateur de prompts structurés pour accélérer le développement de projets PHP/Symfony.

## Description

Ce plugin génère des templates de prompts détaillés pour différents types de tâches de développement :
- Nouvelles features (DDD/CQRS)
- Refactoring et optimisation
- Webhooks et intégrations
- Architecture et infrastructure
- Workflows et automation
- Configuration et feature flags

## Installation

Le plugin est automatiquement disponible via le marketplace.

## Slash Commands Disponibles

| Command | Description | Usage |
|---------|-------------|-------|
| `/prompt:feature` | Génère un prompt pour une feature métier DDD/CQRS | `/prompt:feature [EntityName] [FeatureName]` |
| `/prompt:architecture` | Génère un prompt pour architecture/infrastructure | `/prompt:architecture [ComponentName]` |
| `/prompt:refactoring` | Génère un prompt pour refactoring/optimisation | `/prompt:refactoring [TargetFile]` |
| `/prompt:webhook` | Génère un prompt pour intégration webhook | `/prompt:webhook [ServiceName] [EventType]` |
| `/prompt:workflow` | Génère un prompt pour workflow automation | `/prompt:workflow [WorkflowName]` |
| `/prompt:configuration` | Génère un prompt pour configuration/feature flags | `/prompt:configuration [ConfigName]` |
| `/prompt:generic` | Génère un prompt générique personnalisable | `/prompt:generic [TaskName]` |

## Exemples d'Utilisation

### Feature Métier
```bash
/prompt:feature DeclarationDeBug declaration-bug --bounded-context=Support --duration=8
```

### Refactoring
```bash
/prompt:refactoring MenuBuilder --optimization-type=cache-decorator
```

### Webhook
```bash
/prompt:webhook GitHub issue.created --webhook-url-var=GITHUB_WEBHOOK_SECRET
```

### Mode Interactif
```bash
/prompt:feature --interactive
```

## Variables de Substitution

### Automatiques (détectées depuis le projet)
- `{PROJECT_NAME}` - Nom du projet (depuis composer.json)
- `{NAMESPACE}` - Namespace racine (depuis composer.json)
- `{AUTHOR}` - Nom de l'auteur (depuis git config)
- `{DATE}` - Date actuelle

### Interactives (demandées si absentes)
- `{ENTITY_NAME}` - Nom de l'entité (PascalCase)
- `{FEATURE_NAME}` - Nom de la feature (kebab-case)
- `{BOUNDED_CONTEXT}` - Bounded context DDD
- `{DURATION}` - Estimation en heures
- `{TARGET_FILE}` - Fichier à refactorer
- `{OPTIMIZATION_TYPE}` - Type d'optimisation
- `{SERVICE_NAME}` - Nom du service tiers
- `{EVENT_TYPE}` - Type d'événement

## Structure des Prompts Générés

Les prompts générés suivent une structure standardisée :

1. **Objectif** - Description claire du besoin
2. **Architecture** - Patterns et composants (DDD, CQRS, Decorators, etc.)
3. **Plan d'Implémentation** - Phases détaillées avec fichiers à créer/modifier
4. **Vérification** - Commands make et tests manuels
5. **Points d'Attention** - Standards qualité, risques, patterns

## Patterns Inclus

Les templates intègrent automatiquement :
- **DDD** : Entity, Repository, Collection, Value Objects
- **CQRS** : Messages + Handlers asynchrones
- **Elegant Objects** : Constructeur privé, factory statique, final readonly
- **Testing** : TDD, Factories Foundry, Pattern AAA
- **Qualité** : PHPStan niveau 9, PSR-12, Conditions Yoda
- **Infrastructure** : Decorators, Traits, Feature Flags

## Emplacement des Prompts

Les prompts générés sont écrits dans `.claude/prompts/` du projet courant :
- `.claude/prompts/feature-{name}-{timestamp}.md`
- `.claude/prompts/refactoring-{name}-{timestamp}.md`
- etc.

## Licence

MIT
