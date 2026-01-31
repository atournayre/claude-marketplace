# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.3.0] - 2026-01-31

### Added
- **Skill `/skill-creator`** - Créateur de skills complet avec progressive disclosure
  - 6 fichiers références (progressive disclosure, workflows, examples, patterns, XML guide, output patterns)
  - 3 scripts TypeScript (init-skill.ts, package-skill.ts, validate.ts)
  - Bundled resources (scripts/, references/, assets/)
  - Progressive disclosure pattern (docs chargées à la demande)
  - Basé sur doc officielle https://code.claude.com/docs/llms.txt
  - **Supérieur à 100%** par rapport à l'ancien make-command

- **Skill `/memory`** - Gestion CLAUDE.md avec 4-level hierarchy
  - Hiérarchie 4 niveaux (global, workspace, package, directory)
  - Path-scoped memory (workspace, package, directory)
  - Fusion automatique des niveaux
  - Patterns de projet (monorepo, microservices)
  - 5 fichiers références (project patterns, prompting techniques, section templates, rules directory, comprehensive example)

- **Skill `/make-subagent`** - Créateur de subagents avec YAML
  - Configuration YAML complète (.claude/agents/)
  - Tool restrictions appropriées
  - Context management patterns
  - Error handling et recovery
  - Orchestration patterns (pipeline, parallel, conditional, retry)
  - 7 fichiers références (orchestration, debugging, error handling, writing prompts, subagents, evaluation, context management)

### Removed
- **Skill `/claude:make:command`** - Remplacé par `/skill-creator` (supérieur)
  - Migration vers approche progressive disclosure
  - Bundled resources non supportés dans make-command
  - Scripts d'automatisation absents dans make-command

### Migration
- Migré depuis plugin mlvn (AIBlueprint v1.0.0)
- Conservation de tous les fichiers références et scripts
- Aucune régression fonctionnelle

## [1.2.1] - 2026-01-26

### Removed
- Commandes legacy : 5 commandes migrées vers plugin centralisé `command`
  - Déplacement vers plugin `command` (workaround issue #15178)
  - Skills restent fonctionnels via le plugin `command`

## [1.2.0] - 2026-01-25

### Added
- Commande `/claude:alias:add` - Crée alias commande déléguant à autre slash command
- Commande `/claude:challenge` - Évalue réponse, note sur 10, propose améliorations
- Commande `/claude:doc:load` - Charge documentation Claude Code locale
- Commande `/claude:doc:question` - Interroge documentation Claude Code
- Commande `/claude:make:command` - Générateur slash commands avec workflow structuré

## [1.1.1] - 2026-01-24

### Changed
- Maintenance : mise à jour mineure des skills suite à migration commands → skills

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
