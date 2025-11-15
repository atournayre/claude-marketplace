# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

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
