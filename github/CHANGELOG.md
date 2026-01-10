# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.3] - 2026-01-10

### Fixed
- Correction du format `argument-hint` dans `/github:fix` pour conformité avec documentation officielle Claude Code

## [1.1.2] - 2025-12-20

### Changed
- Ajout du champ `output-style` dans le frontmatter des commandes pour formatage automatique
  - `github:impact` → `bullet-points`

## [1.1.1] - 2025-12-20

### Changed
- Skill `github-impact` : réduction tokens SKILL.md (443→67 lignes)
  - Externalisation report templates vers `references/`
  - `business-report-template.md` : structure rapport métier
  - `technical-report-template.md` : structure rapport technique
  - Pattern : essentials en SKILL.md, templates en références

## [1.1.0] - 2025-11-16

### Added
- Skill `github-impact` - Skill spécialisé pour analyse d'impact PR
  - Analyse complète modifications (fichiers, dépendances, tests, sécurité)
  - Détection automatique templates (Twig, Blade, Vue, etc.)
  - Analyse styles (CSS, SCSS, SASS, LESS)
  - Détection assets (images, fonts)
  - Génération 2 rapports (métier + technique)
  - Intégration automatique dans description PR
  - Sauvegarde locale `.analysis-reports/`

### Changed
- Commande `/github:impact` convertie en délégation au skill `github-impact`
- Workflow enrichi avec analyse dépendances et templates
- Rapport technique avec métriques détaillées par type de fichier

## [1.0.0] - 2025-11-15

### Added
- Commande `/github:fix` - Corrige issue GitHub avec workflow simplifié
- Commande `/github:impact` - Analyse modifications git et génère rapports d'impact métier/technique
