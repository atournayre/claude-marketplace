## [1.0.1] - 2026-02-04

### Changed
- Migrer noms de modèles Claude vers format court (sonnet, haiku, opus)

# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2025-12-17

### Added
- Plugin initial avec 4 agents de code review spécialisés
- Agent `code-reviewer` : review complète (conformité CLAUDE.md, détection bugs, qualité code)
- Agent `silent-failure-hunter` : détection catch vides, erreurs silencieuses, fallbacks non justifiés
- Agent `test-analyzer` : analyse couverture PHPUnit, tests manquants, edge cases
- Agent `git-history-reviewer` : contexte historique git (blame, PRs, TODOs)
- Intégration avec skill `/git:pr` du plugin git
- Scoring de confiance 0-100 avec seuil de rapport >= 80
- Support spécifique PHP/Symfony (PHPStan niveau 9, conditions Yoda, conventions françaises)
