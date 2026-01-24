# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.2.3] - 2026-01-24

### Fixed
- Correction version plugin après migration commands → skills (régression 1.1.0 → 1.2.3)

## [1.1.0] - 2026-01-22

### Changed
- Skills elegant-objects et phpstan-resolver maintenues et validées
- Support complet du format skills natif Claude Code

## [1.2.2] - 2026-01-10

### Fixed
- Correction du format `argument-hint` dans `/qa:elegant-objects` pour conformité avec documentation officielle Claude Code

## [1.2.1] - 2025-12-20

### Changed
- Skills `elegant-objects`, `phpstan-resolver` : réduction tokens SKILL.md
  - Externalisation patterns et workflows vers `references/`
  - `elegant-objects` : detection patterns (lignes: 159→59)
  - `phpstan-resolver` : workflow scripts (lignes: 250→63)

## [1.2.0] - 2025-11-25

### Added
- Skill `elegant-objects` - Vérifie la conformité aux principes Elegant Objects de Yegor Bugayenko
  - Analyse fichier spécifique ou fichiers modifiés dans la branche
  - Règles de conception des classes (final, max 4 attributs, pas de getters/setters)
  - Règles de méthodes (pas de null, corps sans lignes vides)
  - Règles de style (messages sans point final, fail fast)
  - Règles de tests (une assertion par test, noms français)
  - Score de conformité sur 100
  - Rapport détaillé avec suggestions
- Commande `/qa:elegant-objects` - Délègue au skill `elegant-objects`

## [1.1.0] - 2025-11-16

### Added
- Skill `phpstan-resolver` - Skill spécialisé pour résolution automatique erreurs PHPStan
  - Boucle de résolution itérative (max 10 itérations)
  - Batch processing (5 erreurs/fichier/itération)
  - Détection automatique de stagnation
  - Support PHPStan format JSON
  - Rapport détaillé avec taux de succès
  - Délégation à agent `@phpstan-error-resolver`

### Changed
- Commande `/qa:phpstan` convertie en délégation au skill `phpstan-resolver`
- Workflow avec boucle de vérification après chaque correction
- Configuration paramétrable (batch size, max iterations)

## [1.0.0] - 2025-11-15

### Added
- Commande `/qa:phpstan` - Résout erreurs PHPStan avec agent phpstan-error-resolver
