# Changelog - Atournayre Claude Plugin Marketplace

Toutes les modifications notables du marketplace seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [Unreleased]

## [2025.11.16] - 2025-11-16

### Skills Added
- **github-impact** (`github` v1.1.0) - Skill spécialisé analyse d'impact PR
  - Analyse complète modifications (fichiers, dépendances, tests, sécurité)
  - Détection automatique templates (Twig, Blade, Vue, etc.)
  - Analyse styles (CSS, SCSS, SASS, LESS) et assets
  - Génération 2 rapports (métier + technique)
  - Intégration automatique description PR
  - Sauvegarde locale `.analysis-reports/`

- **phpstan-resolver** (`qa` v1.1.0) - Skill spécialisé résolution erreurs PHPStan
  - Boucle résolution itérative (max 10 itérations)
  - Batch processing (5 erreurs/fichier/itération)
  - Détection automatique stagnation
  - Support PHPStan format JSON
  - Rapport détaillé avec taux de succès
  - Délégation agent `@phpstan-error-resolver`

- **doc-loader** (`doc` v1.1.0) - Skill générique chargement documentation frameworks
  - Support multi-framework (Symfony, API Platform, Meilisearch, atournayre-framework, Claude Code)
  - Support multi-version (argument optionnel)
  - Cache intelligent 24h (ignore récents, supprime anciens)
  - Délégation agents scraper spécialisés
  - Anti-rate-limiting (délai 2s entre URLs)
  - Statistiques détaillées (couverture, taille, fichiers)

### Commands Updated
- **github** v1.1.0 - `/github:impact` convertie en délégation skill
- **qa** v1.1.0 - `/qa:phpstan` convertie en délégation skill
- **doc** v1.1.0 - `/doc:framework-load`, `/symfony:doc:load`, `/claude:doc:load` converties en délégation skill

### Architecture
- Pattern commande → skill pour tâches complexes orchestrées
- Réduction taille commandes (406 → 6 lignes pour github:impact)
- Meilleure séparation des responsabilités
- TodoWrite systématique dans skills pour suivi progression

## [2025.11.15] - 2025-11-15

### Marketplace
- Ajout CHANGELOG.md pour tous les plugins
- Ajout CHANGELOG.md global marketplace

### Plugins Added
- **framework v1.0.0** - Plugin génération code PHP Elegant Objects
  - 9 skills pour génération automatisée (contracts, entity, out, invalide, urls, collection, factory, story, all)
  - Templates PHP pour chaque type de classe
  - Documentation complète SKILL.md + README.md

### Plugins Updated
- **git v1.4.1** - Corrections mineures
  - Stabilité commandes Git

- **git v1.4.0** - Nouvelle commande release-report
  - Commande `/git:release-report` - Génère rapports HTML d'analyse d'impact

## [2025.11.14] - Version antérieure

### Plugins Updated
- **git v1.3.0** - Documentation PR
  - Documentation arguments `/git:pr`

- **dev v1.1.0** - Nouveaux agents
  - Agent `dev:meta-agent` - Génération config agents
  - Agent `dev:phpstan-error-resolver` - Résolution erreurs PHPStan
  - Agent `dev:elegant-objects-reviewer` - Review conformité Elegant Objects

## [2025.11.01] - Version initiale

### Marketplace
- Structure initiale marketplace
- Configuration plugins système
- Documentation README globale

### Plugins Added
- **git v1.0.0** - Commandes Git workflow
  - `/git:branch`, `/git:commit`, `/git:conflit`, `/git:pr`
  - Skill `git:git-pr`

- **symfony v1.0.0** - Développement Symfony
  - Skill `symfony:symfony-skill`
  - Commandes `/symfony:make`, `/symfony:doc:load`, `/symfony:doc:question`

- **dev v1.0.0** - Développement général
  - Commandes `/dev:code`, `/dev:prepare`, `/dev:question`, `/dev:docker`
  - Agents scrapers documentation

- **qa v1.0.0** - Qualité code
  - Commande `/qa:phpstan`

- **doc v1.0.0** - Documentation
  - Commandes `/doc:adr`, `/doc:framework-load`, `/doc:rtfm`, `/doc:update`

- **github v1.0.0** - Intégration GitHub
  - Commandes `/github:fix`, `/github:impact`

- **output-styles v1.0.0** - Styles sortie
  - 7 commandes styles (bullet-points, genui, html, markdown, table, ultra-concise, yaml)

- **claude v1.0.0** - Meta Claude Code
  - Commandes `/claude:alias:add`, `/claude:challenge`, `/claude:doc:load`, `/claude:make:command`

- **customize v1.0.0** - Personnalisation utilisateur
  - Plugin vide pour extensions custom

---

## Notes de version

Pour les détails complets de chaque plugin, voir les CHANGELOGs individuels:
- [framework/CHANGELOG.md](framework/CHANGELOG.md)
- [git/CHANGELOG.md](git/CHANGELOG.md)
- [symfony/CHANGELOG.md](symfony/CHANGELOG.md)
- [dev/CHANGELOG.md](dev/CHANGELOG.md)
- [qa/CHANGELOG.md](qa/CHANGELOG.md)
- [doc/CHANGELOG.md](doc/CHANGELOG.md)
- [github/CHANGELOG.md](github/CHANGELOG.md)
- [output-styles/CHANGELOG.md](output-styles/CHANGELOG.md)
- [claude/CHANGELOG.md](claude/CHANGELOG.md)
- [customize/CHANGELOG.md](customize/CHANGELOG.md)
