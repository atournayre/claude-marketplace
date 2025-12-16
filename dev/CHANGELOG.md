# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.2] - 2025-12-16

### Changed
- Commande `/dev:code` : modèle sonnet → haiku (exécution mécanique de plans détaillés)
- Skill `prepare` : plans plus détaillés et exécutables (fichiers explicites, code concret, signatures exactes)

## [1.1.1] - 2025-12-14

### Changed
- Commande `/dev:question` : modèle sonnet → haiku (recherche simple, plus rapide/économique)

## [1.1.0] - 2025-11-15

### Added
- Agent `dev:meta-agent` - Génère configuration agents Claude Code
- Agent `dev:phpstan-error-resolver` - Résout erreurs PHPStan niveau 9
- Agent `dev:elegant-objects-reviewer` - Vérifie conformité principes Elegant Objects
- Commandes de chargement documentation (API Platform, Symfony, Meilisearch, Claude Code)

## [1.0.0] - Version initiale

### Added
- Commande `/dev:code` - Code codebase selon plan
- Commande `/dev:prepare` - Crée plan d'implémentation engineering
- Commande `/dev:question` - Répond questions sans coder
- Commande `/dev:docker` - Utilise Docker pour actions
- Commande `/dev:context:load` - Charge preset contexte session
- Commande `/dev:debug:error` - Analyse et résout erreurs
- Agents scrapers documentation divers frameworks
