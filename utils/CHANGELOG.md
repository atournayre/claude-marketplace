# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2026-01-31

### Added
- **Skill `/fix-grammar`** - Correction grammaire et orthographe
  - Single mode : fichier unique
  - Multi mode : plusieurs fichiers simultanément
  - Détection automatique langue (FR/EN)
  - Préservation formatage Markdown
  - Batch processing
  - Affichage diff avant/après
  - Migré depuis mlvn plugin (AIBlueprint v1.0.0)

- **Agent `action`** - Validation conditionnelle avant exécution
  - Valide prérequis avant action
  - Execute seulement si conditions remplies
  - Workflows conditionnels
  - Migré depuis mlvn plugin (AIBlueprint v1.0.0)

- **Agent `explore-codebase`** - Exploration avec imports chains
  - Explore structure projet
  - Trace chaînes d'imports
  - Identifie dépendances
  - Map architecture
  - Migré depuis mlvn plugin (AIBlueprint v1.0.0)

### Migration
- Nouveau plugin créé pour héberger skills/agents génériques
- Migration depuis mlvn plugin (AIBlueprint v1.0.0)
- Conservation de toutes les fonctionnalités
