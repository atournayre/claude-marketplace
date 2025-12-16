# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.1] - 2025-12-14

### Changed
- Commande `/doc:adr` : modèle opus → sonnet (ADR moins complexe)
- Commande `/doc:framework-question` : modèle sonnet → haiku (lookup documentation, plus rapide)
- Commande `/doc:rtfm` : modèle sonnet → haiku (fetch documentation, plus rapide)

## [1.1.0] - 2025-11-16

### Added
- Skill `doc-loader` - Skill générique pour chargement documentation frameworks
  - Support multi-framework (Symfony, API Platform, Meilisearch, atournayre-framework, Claude Code)
  - Support multi-version (argument optionnel)
  - Cache intelligent 24h (ignore récents, supprime anciens)
  - Délégation aux agents scraper spécialisés
  - Anti-rate-limiting (délai 2s entre URLs)
  - Statistiques détaillées (couverture, taille, fichiers)

### Changed
- Commande `/doc:framework-load` convertie en délégation au skill `doc-loader`
- Commande `/symfony:doc:load` convertie en délégation au skill `doc-loader` avec argument "symfony"
- Commande `/claude:doc:load` convertie en délégation au skill `doc-loader` avec argument "claude"
- Workflow unifié pour tous les frameworks
- Gestion cache améliorée

## [1.0.0] - 2025-11-15

### Added
- Commande `/doc:adr` - Génère Architecture Decision Record formaté
- Commande `/doc:framework-load` - Charge documentation framework depuis site web
- Commande `/doc:framework-question` - Interroge documentation framework locale
- Commande `/doc:rtfm` - Lit documentation technique (Read The Fucking Manual)
- Commande `/doc:update` - Crée et met à jour documentation projet
