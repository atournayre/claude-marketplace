# Catalogue des Templates de Prompts

Ce catalogue répertorie tous les templates de prompts disponibles avec leurs cas d'usage et variables.

## Templates Disponibles

### 1. Feature (feature.md)

**Cas d'usage** : Développement de nouvelles features métier avec architecture DDD/CQRS

**Variables** :
- `{ENTITY_NAME}` - Nom de l'entité (PascalCase)
- `{FEATURE_NAME}` - Nom de la feature (kebab-case)
- `{BOUNDED_CONTEXT}` - Bounded context DDD
- `{DURATION}` - Estimation en heures

**Patterns inclus** :
- DDD : Entity, Repository, Collection, Value Objects
- CQRS : Messages + Handlers asynchrones
- Elegant Objects : Constructeur privé, factory statique, final readonly
- Testing : TDD, Factories Foundry

### 2. Architecture (architecture.md)

**Cas d'usage** : Infrastructure, décorateurs, cache, patterns techniques

**Variables** :
- `{COMPONENT_NAME}` - Nom du composant
- `{PATTERN_TYPE}` - Type de pattern (Decorator, Cache, etc.)

**Patterns inclus** :
- Decorators
- Cache strategies
- Design patterns

### 3. Refactoring (refactoring.md)

**Cas d'usage** : Optimisation, refactoring de code existant

**Variables** :
- `{TARGET_FILE}` - Fichier à refactorer
- `{OPTIMIZATION_TYPE}` - Type d'optimisation
- `{CURRENT_COMPLEXITY}` - Complexité cyclomatique actuelle
- `{IMPROVEMENT_TARGET}` - Objectif d'amélioration (%)

**Patterns inclus** :
- Analyse de complexité
- Benchmarks
- Refactoring progressif

### 4. Webhook (webhook.md)

**Cas d'usage** : Intégration de webhooks avec services tiers

**Variables** :
- `{SERVICE_NAME}` - Nom du service tiers
- `{EVENT_TYPE}` - Type d'événement
- `{WEBHOOK_URL_VAR}` - Variable d'environnement pour l'URL

**Patterns inclus** :
- Webhook Receiver
- CQRS Async
- Validation HMAC
- Rate limiting

### 5. Workflow (workflow.md)

**Cas d'usage** : GitHub Actions, CI/CD, automation

**Variables** :
- `{WORKFLOW_NAME}` - Nom du workflow
- `{TRIGGER_TYPE}` - Type de déclencheur

**Patterns inclus** :
- GitHub Actions
- CI/CD pipelines
- Automation scripts

### 6. Configuration (configuration.md)

**Cas d'usage** : Feature flags, configuration dynamique

**Variables** :
- `{CONFIG_NAME}` - Nom de la configuration
- `{CONFIG_TYPE}` - Type de configuration

**Patterns inclus** :
- Feature flags
- Configuration dynamique
- Environment variables

### 7. Generic (generic.md)

**Cas d'usage** : Template flexible pour tâches personnalisées

**Variables** :
- `{TASK_NAME}` - Nom de la tâche
- `{TASK_DESCRIPTION}` - Description de la tâche

**Patterns inclus** :
- Structure de base adaptable

## Variables Automatiques

Ces variables sont détectées automatiquement depuis le projet :

- `{PROJECT_NAME}` - Nom du projet (composer.json)
- `{NAMESPACE}` - Namespace racine (composer.json)
- `{AUTHOR}` - Nom de l'auteur (git config)
- `{DATE}` - Date actuelle

## Structure Standard

Tous les templates suivent cette structure :

1. **Objectif** - Description claire du besoin
2. **Architecture** - Patterns et composants
3. **Plan d'Implémentation** - Phases détaillées avec fichiers
4. **Vérification** - Commands make et tests
5. **Points d'Attention** - Standards qualité, risques

## Standards Qualité

Tous les templates intègrent :
- PHPStan niveau 9
- PSR-12
- Conditions Yoda
- TDD
- Elegant Objects principles
