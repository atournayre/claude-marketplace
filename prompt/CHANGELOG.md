## [2.3.1] - 2026-02-08

### Changed
- Agent **prompt-analyst** : extraction obligatoire des contraintes architecturales (CLAUDE.md + .claude/rules/) dans la section `## Contraintes architecturales` du rapport
- Skill **prompt-team** : passage des contraintes du projet cible aux agents en aval

## [2.3.0] - 2026-02-06

### Added
- Nouvel agent **prompt-analyst** : fusion architect + designer (architecture technique + design DDD)
- Nouvel agent **prompt-implementer** : fusion developer + tester (code + tests intégrés)

### Changed
- **prompt-team** v2.0.0 → v2.1.0 : Refonte complète pour gestion optimisée des ressources
  - Architecture multi-agent hybride : 3 agents au lieu de 6 (analyst, challenger, implementer)
  - Fichiers intermédiaires dans le scratchpad pour communication inter-phases (contexte du team lead protégé)
  - Mode Normal (parallèle intra-phase, max 2 agents) avec basculement automatique vers mode Safe si RAM < 4 GB
  - Shutdown par phase : agents d'une même phase communiquent en temps réel avant shutdown
  - Option `--safe` pour forcer le mode séquentiel sur machines contraintes

## [2.2.0] - 2026-02-06

### Changed
- **prompt-team** v2.0.0 : Refonte architecture multi-agent
  - Fusion des agents : 3 agents (analyst, challenger, implementer) au lieu de 6
  - Fichiers intermédiaires dans le scratchpad pour la communication inter-phases (pas dans le contexte du team lead)
  - Mode Normal (parallèle intra-phase, max 2 agents) et mode Safe (séquentiel strict)
  - Shutdown par phase : les agents d'une même phase communiquent en temps réel, puis sont tous shutdown avant la phase suivante
  - Option `--safe` pour forcer le mode séquentiel sur machines contraintes
  - Health check RAM avec basculement automatique Normal -> Safe si RAM < 4 GB
  - `max_turns` obligatoire sur chaque agent (15 analyse, 20 QA, 30 implémentation)

### Added
- Nouvel agent **prompt-analyst** : fusion architect + designer (architecture technique + design DDD)
- Nouvel agent **prompt-implementer** : fusion developer + tester (code + tests)

## [2.1.1] - 2026-02-06

### Changed
- **prompt-qa** : Découverte dynamique des outils QA (Makefile, composer.json, package.json, vendor/bin/)
  - Scanner automatique des sources : Makefile, composer scripts, npm scripts, binaires, fichiers de config
  - Support multi-outil : PHPStan, Rector, PHP CS Fixer, PHPUnit, Biome, ESLint, Stylelint
  - Exécution en mode check/dry-run (jamais de modification)
  - Rapport dynamique basé sur les outils découverts (pas juste 4 outils hardcodés)
  - Notion de criticité : BLOQUANT (erreur = fail) vs INFORMATIF (warnings)
- **prompt-team** : Mise à jour Phase 5 - QA découvre et exécute tous les outils du projet
- **php.md checklist** : Ajout de `rector --dry-run` dans les commandes de vérification

## [2.1.0] - 2026-02-06

### Added
- Nouveau skill `/prompt:team` - Orchestre une équipe d'agents spécialisés via Agent Teams natif
  - Auto-détection du type de tâche (feature/refactor/api/fix)
  - Composition d'équipe automatique selon le type
  - Override possible avec `--agents=architect,developer,qa`
  - Workflow 6 phases : Analyse → Challenge → Synthèse → Implémentation → QA → Rapport
  - Validation utilisateur avant implémentation
  - Gestion d'erreurs avec fallbacks par phase
- 6 agents spécialisés :
  - `prompt-architect` - Architecture, patterns, structure codebase
  - `prompt-designer` - Design DDD, contrats, interfaces, data flow
  - `prompt-challenger` - Avocat du diable, edge cases, sécurité, alternatives
  - `prompt-developer` - Implémentation code selon plan validé
  - `prompt-tester` - Écriture tests PHPUnit (TDD)
  - `prompt-qa` - Lint (PHPStan, CS-Fixer), run tests, Chrome UI testing

### Changed
- Plugin description mise à jour pour inclure Agent Teams
- Keywords étendus avec : `team`, `agents`, `orchestration`, `multi-agent`

## [2.0.0] - 2026-02-04

### Changed
- **BREAKING** : Refonte complète du système de prompts
- Remplacement des templates longs (300+ lignes) par des starters légers (10-15 lignes)
- Nouvelle approche hybride : Starter + Mode Plan + Checklist

### Added
- Nouveau skill `/prompt:start` - Démarre avec un starter et active le mode plan
- Nouveau skill `/prompt:validate` - Vérifie la checklist avant exécution
- 4 starters légers :
  - `starters/feature.md` - Feature métier
  - `starters/refactor.md` - Refactoring
  - `starters/api.md` - API/Intégration
  - `starters/fix.md` - Bug fix
- 3 checklists de validation :
  - `checklists/php.md` - PHPStan, PSR-12, Elegant Objects, tests
  - `checklists/api.md` - Validation, auth, robustesse, logging
  - `checklists/security.md` - OWASP, injections, données sensibles

### Removed
- Template `feature.md` (340 lignes) → remplacé par `starters/feature.md` (20 lignes)
- Template `architecture.md` → supprimé (le mode plan suffit)
- Template `webhook.md` → remplacé par `starters/api.md`
- Template `workflow.md` → supprimé (domaine GitHub Actions séparé)
- Template `configuration.md` → supprimé (cas trop rare)
- Template `generic.md` → supprimé (inutile avec starters ciblés)
- Skills associés aux anciens templates (6 skills supprimés)

### Why this change?
Les anciens templates n'étaient jamais utilisés car :
- Trop longs et intimidants
- Code boilerplate fixe pas adapté au contexte
- Le mode plan faisait déjà le même travail avec plus de flexibilité

La nouvelle approche combine :
- La légèreté des starters (contexte + contraintes)
- La puissance du mode plan (exploration + adaptation)
- La complétude des checklists (validation finale)

## [1.3.1] - 2026-02-04

### Changed
- Migrer noms de modèles Claude vers format court (sonnet, haiku, opus)

# Changelog

Toutes les modifications notables de ce plugin seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.3.0] - 2026-01-28

### Added
- Nouvelle skill `prompt:transform` - Transforme un prompt quelconque en prompt exécutable
  - Compatible avec le Task Management System (TaskCreate/TaskUpdate/TaskList)
  - Analyse et structure les tâches avec content et activeForm
  - Génère des prompts avec phases d'exécution numérotées
  - Écrit les fichiers dans `.claude/prompts/` du projet utilisateur

### Changed
- Plugin description mise à jour pour inclure les capacités de transformation de prompts
- Keywords étendus avec : `transform`, `executable`, `todowrite`

## [1.2.0] - 2026-01-26

### Changed
- Intégration du plugin prompt dans le plugin centralisé `command` (workaround issue #15178)

## [1.1.1] - 2026-01-26

### Removed
- Commandes legacy : 7 commandes migrées vers plugin centralisé `command`
  - Déplacement vers plugin `command` (workaround issue #15178)
  - Skills restent fonctionnels via le plugin `command`

## [1.1.0] - 2026-01-25

### Added
- Commande `/prompt:architecture` - Génère un prompt pour architecture et infrastructure (decorators, cache, patterns)
- Commande `/prompt:configuration` - Génère un prompt pour configuration et feature flags
- Commande `/prompt:feature` - Génère un prompt pour une nouvelle feature métier basé sur les patterns DDD/CQRS
- Commande `/prompt:generic` - Génère un prompt générique personnalisable pour toute tâche
- Commande `/prompt:refactoring` - Génère un prompt pour refactoring et optimisation de code existant
- Commande `/prompt:webhook` - Génère un prompt pour intégration webhook avec services tiers
- Commande `/prompt:workflow` - Génère un prompt pour workflow GitHub Actions et CI/CD

## [1.0.0] - 2026-01-21

### Added

#### Templates de Prompts (8 templates)
- Template `feature.md` - Features métier DDD/CQRS avec Entity, Repository, Collection, CQRS Messages/Handlers
- Template `refactoring.md` - Refactoring et optimisation avec patterns (Decorator, Cache, etc.)
- Template `webhook.md` - Intégration webhooks avec validation HMAC, rate limiting, CQRS async
- Template `architecture.md` - Architecture et infrastructure (decorators, cache, design patterns)
- Template `workflow.md` - GitHub Actions, CI/CD, automation avec matrice de tests
- Template `configuration.md` - Feature flags, configuration dynamique, déploiement progressif
- Template `generic.md` - Template flexible pour tâches personnalisées
- Template `index.md` - Catalogue complet des templates avec cas d'usage

#### Slash Commands (7 skills)
- `/prompt:feature` - Génère prompt pour nouvelle feature métier (DDD/CQRS)
- `/prompt:refactoring` - Génère prompt pour refactoring/optimisation
- `/prompt:webhook` - Génère prompt pour intégration webhook
- `/prompt:architecture` - Génère prompt pour architecture/infrastructure
- `/prompt:workflow` - Génère prompt pour workflow GitHub Actions
- `/prompt:configuration` - Génère prompt pour configuration/feature flags
- `/prompt:generic` - Génère prompt générique personnalisable

#### Scripts de Génération (3 scripts bash)
- `analyze-context.sh` - Analyse automatique du projet (namespace, nom projet, auteur, date)
- `substitute-variables.sh` - Substitution de variables dans templates (15+ variables supportées)
- `validate-prompt.sh` - Validation des prompts générés (variables, sections, longueur)

#### Système de Variables
**Variables automatiques** (détectées depuis le projet) :
- `{PROJECT_NAME}` - Nom du projet (composer.json)
- `{NAMESPACE}` - Namespace racine (composer.json)
- `{AUTHOR}` - Nom de l'auteur (git config)
- `{DATE}` - Date actuelle

**Variables interactives** (demandées ou passées en arguments) :
- Feature : `{ENTITY_NAME}`, `{FEATURE_NAME}`, `{BOUNDED_CONTEXT}`, `{DURATION}`
- Refactoring : `{TARGET_FILE}`, `{OPTIMIZATION_TYPE}`, `{CURRENT_COMPLEXITY}`, `{IMPROVEMENT_TARGET}`
- Webhook : `{SERVICE_NAME}`, `{EVENT_TYPE}`, `{WEBHOOK_URL_VAR}`
- Architecture : `{COMPONENT_NAME}`
- Workflow : `{WORKFLOW_NAME}`
- Configuration : `{CONFIG_NAME}`
- Generic : `{TASK_NAME}`

#### Patterns et Standards
Tous les templates intègrent automatiquement :
- **DDD** : Entity, Repository, Collection, Value Objects
- **CQRS** : Messages + Handlers asynchrones
- **Elegant Objects** : Constructeur privé, factory statique, final readonly
- **Testing** : TDD, Factories Foundry, Pattern AAA
- **Qualité** : PHPStan niveau 9, PSR-12, Conditions Yoda
- **Infrastructure** : Decorators, Traits, Feature Flags

#### Mode Interactif
- Flag `--interactive` disponible sur tous les skills
- Questions avec `AskUserQuestion` pour variables manquantes
- Collecte progressive des informations requises

#### Validation et Qualité
- Validation automatique des prompts générés
- Détection des variables non substituées
- Vérification des sections requises (Objectif, Architecture, Plan, Vérification)
- Limite de longueur (max 2000 lignes)

#### Emplacement des Prompts
- Répertoire `.claude/prompts/` créé automatiquement dans le projet
- Nomenclature : `{type}-{name}-{timestamp}.md`
- Gitignore configuré pour exclure les prompts générés

#### Documentation
- README complet avec exemples d'usage
- README pour chaque skill (7 fichiers)
- Catalogue des templates (index.md)
- CHANGELOG (ce fichier)

### Catégories de Templates

Les templates couvrent 6 catégories de tâches de développement :
1. Architecture & Infrastructure (decorators, cache, design patterns)
2. Refactoring & Optimisation (amélioration code existant)
3. Features Métier (DDD/CQRS)
4. Workflow Automation (GitHub Actions, CI/CD)
5. Webhooks & Intégration (services tiers)
6. Configuration (feature flags, paramètres)

### Patterns et Bonnes Pratiques Intégrés

Les templates appliquent automatiquement :
- DDD avec bounded contexts
- CQRS avec handlers asynchrones
- Doctrine Listeners et Events
- Decorators pour cache/logging
- Value Objects pour concepts métier
- Feature Flags pour déploiement progressif
- Tests TDD avec Foundry Factories

### Standards Qualité

Tous les prompts générés imposent :
- PHPStan niveau 9 (0 erreur toléré)
- PSR-12 pour le code style
- Conditions Yoda (`null === $value`)
- Constructeurs privés avec factories statiques
- Classes `final readonly`
- Tests unitaires TDD avec pattern AAA
- Coverage minimum 80%

## [Unreleased]

### Prévisions v1.1
- Détection automatique du type de tâche depuis description
- Mode `--analyze` : analyser fichier existant et suggérer template
- Catalogue interactif : `/prompt:list` affiche tous templates disponibles

### Prévisions v1.2
- Template pour migrations Doctrine
- Template pour commandes Symfony
- Template pour API Platform resources

### Prévisions v2.0
- Analyse des plans récents pour améliorer templates
- Suggestions de variables basées sur contexte
- Génération de prompts depuis issues GitHub

## Notes de Version

### Compatibilité

- Requiert `jq` pour parser composer.json
- Requiert `git` pour extraction auteur
- Requiert `bash 4.0+` pour scripts
- Compatible Linux/macOS

### Migration

Cette version 1.0.0 est la première release, pas de migration nécessaire.

### Contributeurs

- Aurélien Tournayre (@atournayre) - Création initiale

## Liens

- [Repository GitHub](https://github.com/atournayre/claude-marketplace)
- [Documentation](./README.md)
- [Templates](./templates/)
- [Skills](./skills/)
