## [1.1.1] - 2026-02-04

### Changed
- Migrer noms de modèles Claude vers format court (sonnet, haiku, opus)

# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.0] - 2026-01-31

### Added
- **Bash Security Validator** : Validateur de sécurité pour commandes bash (TypeScript/Bun)
  - 100+ patterns de sécurité (commandes critiques, escalade privilèges, attaques réseau)
  - 82+ tests automatisés avec Bun test
  - Détection patterns malveillants (fork bombs, backdoors, exfiltration données)
  - Protection chemins système (/etc, /usr, /bin, /sys, /proc, /dev, /root)
  - Logs sécurité avec traçabilité complète (data/security.log)
  - Hook PreToolUse configuré automatiquement
- Architecture hybride Python + TypeScript
  - Hooks Python pour événements Claude Code
  - Validators TypeScript/Bun pour validation haute performance
- Documentation complète validators/bash/README.md

### Changed
- README.md : Section Bash Security Validator + Architecture Hybride
- Structure du plugin : Ajout dossier validators/

### Migration
- Migré depuis plugin mlvn (AIBlueprint v1.0.0)
- Conservation de tous les tests et règles de sécurité
- Logs sécurité gitignorés pour éviter commit données sensibles

## [1.0.0] - 2025-11-15

### Added
- Plugin vide pour personnalisations utilisateur
- Structure de base pour commandes et skills custom
