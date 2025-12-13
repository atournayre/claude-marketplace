# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.3.0] - 2025-12-13

### Added
- Skill `cs-fixer` - Analyse et correction du style de code PHP via commandes projet
  - Détection automatique des targets Makefile (prioritaire) et scripts composer.json
  - Respect des conventions du projet (ne force jamais de règles arbitraires)
  - Support des patterns courants (cs, cs-fix, lint, style, phpcs, phpcbf)
  - Demande de confirmation avant correction
  - Compatible php-cs-fixer et phpcs/phpcbf
- Commande `/qa:cs-fixer` - Délègue au skill `cs-fixer`
  - Utilise les commandes make ou composer du projet
  - Guide d'installation si aucune commande détectée

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
