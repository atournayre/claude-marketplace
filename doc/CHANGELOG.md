# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.6.0] - 2026-01-25

### Added
- Commande `/doc:adr` - Génère un Architecture Decision Record (ADR) formaté et structuré
- Commande `/doc:doc-loader` - Charge la documentation d'un framework depuis son site web dans des fichiers markdown locaux. Supporte Symfony, API Platform, Meilisearch, atournayre-framework et Claude Code.
- Commande `/doc:rtfm` - Lit la documentation technique - RTFM (Read The Fucking Manual)
- Commande `/doc:update` - Crées la documentation pour la fonctionnalité en cours. Mets à jour le readme global du projet si nécessaire. Lie les documents entre eux pour ne pas avoir de documentation orpheline. La documentation est générée dans les répertoire de documentation du projet.

## [1.5.1] - 2026-01-24

### Changed
- Stabilisation des skills suite à migration commands → skills

## [1.5.0] - 2026-01-22

### Changed
- Migration de 3 commands vers le format skills (adr, rtfm, update)
- Format natif Claude Code avec support complet frontmatter YAML
- Support output-style avec workaround pour skills concernées

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [1.1.3] - 2025-12-20

### Changed
- Ajout du champ `output-style` dans le frontmatter des commandes pour formatage automatique
  - `doc:adr` → `markdown-focused`
  - `doc:rtfm` → `markdown-focused`

## [1.1.2] - 2025-12-20

### Changed
- Skill `doc-loader` : réduction tokens SKILL.md (85→53 lignes)
  - Externalisation workflow détaillé vers `references/workflow-scripts.md`
  - Documentation progressive : essentials en SKILL.md, détails en références

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
