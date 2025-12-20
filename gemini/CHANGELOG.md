# Changelog

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
