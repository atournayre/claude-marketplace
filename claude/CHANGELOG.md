# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.0] - 2025-01-22

### Changed
- Migration de toutes les commands vers le format skills
- Conversion de 5 commands en 5 skills avec support natif Claude Code
- Remplacement des références "SlashCommand" par "Skill"

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [1.0.0] - 2025-11-15

### Added
- Commande `/claude:alias:add` - Crée alias commande déléguant à slash command
- Commande `/claude:challenge` - Évalue réponse, note sur 10, propose améliorations
- Commande `/claude:doc:load` - Charge documentation Claude Code locale
- Commande `/claude:doc:question` - Interroge documentation Claude Code
- Commande `/claude:make:command` - Générateur slash commands avec workflow structuré
