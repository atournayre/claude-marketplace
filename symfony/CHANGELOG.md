# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.2.1] - 2026-01-24

### Changed
- Stabilisation des skills suite à migration commands → skills

## [1.2.0] - 2026-01-22

### Changed
- Migration de 3 commands vers le format skills (make, doc:load, doc:question)
- Remplacement des références "SlashCommand" par "Skill"
- Format natif Claude Code avec support complet frontmatter YAML

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [1.0.1] - 2025-12-20

### Changed
- Skill `symfony-skill` : réduction tokens SKILL.md (495→83 lignes)
  - Documentation progressive : essentials en SKILL.md
  - Références existantes : 5 fichiers dans `references/` (doctrine-advanced, security-detailed, api-platform, testing-complete, performance-tuning)

## [1.0.0] - 2025-11-15

### Added
- Skill `symfony:symfony-skill` - Développement Symfony 6.4 (controllers, routing, Doctrine, forms, security, tests)
- Commande `/symfony:make` - Recherche et utilise makers Symfony
- Commande `/symfony:doc:load` - Charge documentation Symfony locale
- Commande `/symfony:doc:question` - Interroge documentation Symfony
