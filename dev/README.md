# Plugin Dev v2.0.0

Workflow structuré de développement de features en 8 phases avec agents spécialisés.

## Installation

```bash
/plugin install dev@atournayre-claude-plugin-marketplace
```

### Dépendance recommandée

Pour une expérience optimale, installe également le plugin `feature-dev` :

```bash
/plugin install feature-dev@claude-code-plugins
```

Ce plugin fournit les agents :
- `code-explorer` (exploration codebase)
- `code-architect` (design architecture)
- `code-reviewer` (review qualité)

## Workflow de développement

### Commande principale

```bash
/dev:feature <description>
```

Lance un workflow complet en 8 phases :

```
🔄 Workflow de développement

  ⬜ 0. Discover   - Comprendre le besoin
  ⬜ 1. Explore    - Explorer codebase
  ⬜ 2. Clarify    - Questions clarification
  ⬜ 3. Design     - Proposer architectures
  ⬜ 4. Plan       - Générer specs
  ⬜ 5. Code       - Implémenter
  ⬜ 6. Review     - QA complète
  ⬜ 7. Summary    - Résumé final
```

### Voir le statut

```bash
/dev:status
```

Affiche l'état actuel du workflow et les commandes disponibles.

## Phases individuelles

Tu peux exécuter chaque phase individuellement :

| Commande | Phase | Description |
|----------|-------|-------------|
| `/dev:discover <desc>` | 0 | Comprendre le besoin |
| `/dev:explore` | 1 | Explorer le codebase avec agents |
| `/dev:clarify` | 2 | Questions de clarification |
| `/dev:design` | 3 | Proposer 2-3 architectures |
| `/dev:plan` | 4 | Générer le plan dans `docs/specs/` |
| `/dev:code [plan]` | 5 | Implémenter selon le plan |
| `/dev:review` | 6 | QA complète (PHPStan + EO + review) |
| `/dev:summary` | 7 | Résumé final |

## Commandes utilitaires

| Commande | Description |
|----------|-------------|
| `/dev:debug <error>` | Analyser et résoudre une erreur |
| `/dev:log <fichier>` | Ajouter `LoggableInterface` à un fichier PHP |

## Exemple d'utilisation

### Workflow complet

```bash
# Lancer le workflow
/dev:feature Ajouter authentification OAuth

# Le workflow guide à travers les 8 phases
# avec des checkpoints pour validation
```

### Phases individuelles

```bash
# Comprendre le besoin
/dev:discover Refactorer le module de paiement

# Explorer le codebase
/dev:explore

# Poser les questions
/dev:clarify

# Designer l'architecture
/dev:design

# Générer le plan
/dev:plan

# Implémenter
/dev:code docs/specs/feature-paiement.md

# Review
/dev:review

# Résumé
/dev:summary
```

### Debug

```bash
# Analyser une erreur PHP
/dev:debug "Fatal error: Call to undefined method User::getName()"

# Analyser un fichier log
/dev:debug /var/log/app.log
```

## Agents spécialisés

### QA & Review

| Agent | Description |
|-------|-------------|
| `phpstan-error-resolver` | Résout erreurs PHPStan niveau 9 (types stricts, generics, array shapes) |
| `elegant-objects-reviewer` | Vérifie conformité Elegant Objects (final, immuable, pas de null) |
| `meta-agent` | Génère configuration d'agents Claude Code |

### Documentation Scrapers

| Agent | Description |
|-------|-------------|
| `symfony-docs-scraper` | Extrait documentation Symfony |
| `api-platform-docs-scraper` | Extrait documentation API Platform |
| `claude-docs-scraper` | Extrait documentation Claude Code |
| `meilisearch-docs-scraper` | Extrait documentation Meilisearch |
| `atournayre-framework-docs-scraper` | Extrait documentation atournayre-framework |

## Structure

```
dev/
├── commands/
│   ├── feature.md      # Orchestrateur
│   ├── status.md       # Affiche plan
│   ├── discover.md     # Phase 0
│   ├── explore.md      # Phase 1
│   ├── clarify.md      # Phase 2
│   ├── design.md       # Phase 3
│   ├── plan.md         # Phase 4
│   ├── code.md         # Phase 5
│   ├── review.md       # Phase 6
│   ├── summary.md      # Phase 7
│   ├── debug.md        # Utilitaire
│   └── log.md          # Utilitaire
├── agents/
│   ├── phpstan-error-resolver.md
│   ├── elegant-objects-reviewer.md
│   ├── meta-agent.md
│   ├── symfony-docs-scraper.md
│   ├── api-platform-docs-scraper.md
│   ├── claude-docs-scraper.md
│   ├── meilisearch-docs-scraper.md
│   └── atournayre-framework-docs-scraper.md
├── README.md
└── CHANGELOG.md
```

## Checkpoints

Le workflow inclut des checkpoints aux phases critiques :

- **Phase 0** : Confirmation de la compréhension
- **Phase 2** : Attente des réponses aux questions
- **Phase 3** : Choix de l'architecture
- **Phase 5** : Approbation avant implémentation
- **Phase 6** : Décision sur les corrections (fix now / fix later / proceed)

## Fichiers générés

- `.claude/data/.dev-workflow-state.json` : État du workflow en cours (non versionné)
- `docs/specs/feature-*.md` : Plans d'implémentation

## Licence

MIT
