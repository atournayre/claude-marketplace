# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.1] - 2026-01-26

### Removed
- Commandes legacy : 9 commandes migrées vers plugin centralisé `command`
  - Déplacement vers plugin `command` (workaround issue #15178)
  - Skills restent fonctionnels via le plugin `command`

## [1.1.0] - 2026-01-25

### Added
- Commande `/framework:make:all` - Génère tous les fichiers pour une entité complète (orchestrateur)
- Commande `/framework:make:collection` - Génère classe Collection typée avec traits Atournayre
- Commande `/framework:make:contracts` - Génère les interfaces de contrats pour une architecture Elegant Objects
- Commande `/framework:make:entity` - Génère une entité Doctrine avec repository selon principes Elegant Objects
- Commande `/framework:make:factory` - Génère Factory Foundry pour tests
- Commande `/framework:make:invalide` - Génère classe Invalide (exceptions métier)
- Commande `/framework:make:out` - Génère classe Out (DTO immuable pour output)
- Commande `/framework:make:story` - Génère Story Foundry pour fixtures de tests
- Commande `/framework:make:urls` - Génère classe Urls + Message CQRS + Handler

## [1.0.3] - 2026-01-24

### Changed
- Stabilisation des skills suite à migration commands → skills

## [1.0.2] - 2026-01-24

### Changed
- Intégration du task management system dans skill framework/ :
  - `framework:make-all` - 10 tâches (orchestration 8 skills séquentiels)
- Ajout de TaskCreate/TaskUpdate pour suivi progression
- Documentation patterns task management et dépendances séquentielles

## [1.0.1] - 2025-12-20

### Changed
- Skills `make-collection`, `make-entity`, `make-out`, `make-factory`, `make-story`, `make-urls`, `make-invalide`, `make-all` : réduction tokens SKILL.md
  - Externalisation templates et exemples vers `references/usage.md`
  - Économie totale tokens: ~16k (72% réduction)
  - Pattern : essentials en SKILL.md, détails en références (progressive disclosure)

## [1.0.0] - 2025-11-15

### Added
- Skill `framework:make:contracts` - Génère interfaces de contrats Elegant Objects
- Skill `framework:make:entity` - Génère entité Doctrine + repository
- Skill `framework:make:out` - Génère DTO immuable pour output
- Skill `framework:make:invalide` - Génère classe exceptions métier
- Skill `framework:make:urls` - Génère classe Urls + Message CQRS + Handler
- Skill `framework:make:collection` - Génère collection typée avec traits Atournayre
- Skill `framework:make:factory` - Génère factory Foundry pour tests
- Skill `framework:make:story` - Génère story Foundry pour fixtures
- Skill `framework:make:all` - Orchestrateur générant stack complète
- Documentation complète pour chaque skill (SKILL.md + README.md)
- Templates PHP pour chaque type de classe
- Configuration plugin framework/.claude-plugin/plugin.json
