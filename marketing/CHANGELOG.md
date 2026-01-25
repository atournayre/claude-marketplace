# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

## [1.2.0] - 2026-01-25

### Added
- Commande `/marketing:linkedin` - Génère un post LinkedIn attractif basé sur les dernières modifications du marketplace

## [1.1.1] - 2026-01-24

### Changed
- Stabilisation des skills suite à migration commands → skills

## [1.1.0] - 2026-01-22

### Changed
- Migration de 1 command vers le format skill (marketing:linkedin)
- Format natif Claude Code avec support complet frontmatter YAML

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [1.0.2] - 2026-01-10

### Fixed
- Correction du format `argument-hint` dans `/marketing:linkedin` pour conformité avec documentation officielle Claude Code

## [1.0.1] - 2025-12-20

### Changed
- Ajout du champ `output-style` dans le frontmatter des commandes pour formatage automatique
  - `marketing:linkedin` → `markdown-focused`

## [1.0.0] - 2025-12-17

### Added
- Nouvelle commande `/linkedin` pour générer du contenu LinkedIn

