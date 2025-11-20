# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.4.2] - 2025-11-20

### Fixed
- Génération aliases milestone supportant formes courtes ("26" → "26.0.0 (Avenant)")
- Renforcement SKILL.md pour imposer utilisation scripts Python avec cache (milestone/projet)

## [1.4.1] - 2025-11-15

### Fixed
- Corrections mineures et stabilité

## [1.4.0] - 2025-11-15

### Added
- Commande `/git:release-report` - Génère rapports HTML d'analyse d'impact pour releases

## [1.3.0] - Date antérieure

### Added
- Documentation arguments commande `/git:pr`

### Changed
- Amélioration workflow Pull Requests

## [1.2.0] - Date antérieure

### Added
- Cache persistant pour milestones GitHub
- Cache projets GitHub

### Changed
- Réorganisation tests

## [1.1.1] - Date antérieure

### Fixed
- Correction référence skill `git:git-pr`

## [1.1.0] - Date antérieure

### Added
- Skill `git:git-pr` - Workflow création Pull Requests optimisé

### Changed
- Déplacement skill git-pr depuis plugin dev vers git

## [1.0.0] - Version initiale

### Added
- Commande `/git:branch` - Création branches Git structurée
- Commande `/git:commit` - Commits conventional avec emoji
- Commande `/git:conflit` - Résolution conflits git assistée
- Commande `/git:pr` - Création Pull Requests GitHub
