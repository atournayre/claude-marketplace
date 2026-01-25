# Changelog

## [1.4.1] - 2026-01-26

### Removed
- Commandes legacy : 3 commandes migrées vers plugin centralisé `command`
  - Déplacement vers plugin `command` (workaround issue #15178)
  - Skills restent fonctionnels via le plugin `command`

## [1.4.0] - 2026-01-25

### Added
- Commande `/gemini:analyze` - Analyse une codebase ou documentation avec Gemini (1M tokens)
- Commande `/gemini:search` - Recherche temps réel via Google Search intégré à Gemini
- Commande `/gemini:think` - Délègue un problème complexe à Gemini Deep Think

## [1.3.0] - 2026-01-22

### Changed
- Migration de 3 commands vers le format skills (analyze, search, think)
- Format natif Claude Code avec support complet frontmatter YAML

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [1.0.1] - 2025-12-20

### Changed
- Ajout du champ `output-style` dans le frontmatter des commandes pour formatage automatique
  - `gemini:analyze` → `bullet-points`

## [1.0.0] - 2025-12-16

### Added
- Plugin initial avec intégration Gemini CLI
- Agent `gemini-analyzer` : analyse de contextes ultra-longs (1M tokens)
- Agent `gemini-thinker` : Deep Think pour problèmes complexes (math, logique, architecture)
- Agent `gemini-researcher` : recherche temps réel via Google Search intégré
- Commande `/gemini:analyze <path> <question>`
- Commande `/gemini:think <problem>`
- Commande `/gemini:search <query>`
- Filtrage automatique des fichiers sensibles (.env, credentials)
- Limite de contexte 4MB avec vérification
- Timeout configurable (300s par défaut)
