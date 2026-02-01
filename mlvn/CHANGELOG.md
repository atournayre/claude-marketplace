# Changelog

Toutes les modifications notables de ce plugin seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-31

### Removed
- **Nettoyage suite à migration vers écosystème** :
  - ❌ Bash Security Validator → migré vers `customize` v1.1.0
  - ❌ skill-creator → migré vers `claude` v1.3.0
  - ❌ memory/CLAUDE.md → migré vers `claude` v1.3.0
  - ❌ make-subagent → migré vers `claude` v1.3.0
  - ❌ fix-pr-comments → migré vers `git` v1.11.0
  - ❌ oneshot → migré vers `dev` v2.5.0
  - ❌ ralph-loop → migré vers `dev` v2.5.0
  - ❌ fix-grammar → migré vers `utils` v1.0.0
  - ❌ action agent → migré vers `utils` v1.0.0
  - ❌ explore-codebase agent → migré vers `utils` v1.0.0
  - ❌ hooks (PreToolUse) → migré vers `customize` v1.1.0
  - ❌ scripts/command-validator → migré vers `customize/validators/bash`

### Conservé
- ✅ Skills Git : git-commit, git-create-pr, git-merge
- ✅ Skills Meta : meta-prompt-creator
- ✅ Skills Workflow : workflow-apex, workflow-apex-free
- ✅ Skills Utils : utils-fix-errors
- ✅ Agents : explore-docs, websearch
- ✅ Scripts : statusline (tracking coûts)

### Changed
- Documentation mise à jour pour refléter la migration
- plugin.json : version bump (1.0.0 → 1.1.0)

### Notes
- Démantelement stratégique : éléments dupliqués migrés vers plugins spécialisés
- Réduction de duplication du code dans l'écosystème
- Éléments migrés disponibles dans les plugins spécialisés (customize, claude, git, dev, utils)
- Voir [Migration Plan](../../CHANGELOG.md#2026-01-31) pour le contexte complet

---

## [1.0.0] - 2026-01-31

### Added
- Intégration complète d'AIBlueprint by Melvynx
  - 4 agents spécialisés (action, explore-codebase, explore-docs, websearch)
  - 4 skills Git (commit, create-pr, fix-pr-comments, merge)
  - 4 skills Meta (claude-memory, prompt-creator, skill-creator, subagent-creator)
  - 3 skills Workflow (ralph-loop, apex, apex-free)
  - 3 skills Utilities (fix-errors, fix-grammar, oneshot)
- Hook de sécurité PreToolUse pour validation de commandes Bash
- Scripts utilitaires
  - command-validator : validation des commandes bash selon règles de sécurité
  - statusline : génération de statusline personnalisée avec contexte session
- Documentation complète en français

### Notes
- Première version du plugin mlvn
- Intégration depuis github.com/melvynx/aiblueprint v1.0.1
- Tous les crédits à Melvyn (Melvynx) pour le projet original
