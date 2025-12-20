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

## Git Worktrees

Le plugin supporte les git worktrees pour permettre le développement de plusieurs features en parallèle.

### Qu'est-ce qu'un worktree ?

Un git worktree permet d'avoir plusieurs répertoires de travail pour un même dépôt. Au lieu de faire des `git checkout` qui changent les fichiers dans votre dossier actuel, vous avez plusieurs dossiers, chacun sur une branche différente.

**Avantages :**
- Travailler sur plusieurs features simultanément
- Pas besoin de stash ou de switcher de branche
- Préserver le contexte (IDE, serveur de dev, tests)
- Garder la branche main propre

### Commande /dev:worktree

Gestion complète des worktrees :

| Commande | Description |
|----------|-------------|
| `/dev:worktree create <name> [base]` | Créer un worktree pour une feature |
| `/dev:worktree list` | Lister tous les worktrees actifs |
| `/dev:worktree status [name]` | Afficher le statut d'un worktree |
| `/dev:worktree remove <name>` | Supprimer un worktree |
| `/dev:worktree switch <name>` | Basculer vers un worktree |

**Exemple :**
```bash
# Créer un worktree pour une feature OAuth
/dev:worktree create oauth-auth

# Le worktree est créé dans : ../claude-marketplace-oauth-auth
# Branche créée : feature/oauth-auth

# Basculer vers le worktree
cd ../claude-marketplace-oauth-auth

# Travailler sur la feature...

# Supprimer le worktree une fois mergé
/dev:worktree remove oauth-auth
```

### Intégration avec /dev:feature

Le workflow `/dev:feature` propose automatiquement de créer un worktree à l'initialisation :

```bash
/dev:feature Ajouter OAuth

# 📂 Créer un worktree pour cette feature ?
#
# Avantages des worktrees :
#   • Garder votre branche main propre
#   • Travailler sur plusieurs features en parallèle
#   • Préserver le contexte de développement
#
# Créer le worktree ? (o/n)
```

Si vous acceptez :
1. Un worktree est créé automatiquement
2. Vous êtes invité à changer de répertoire
3. Le workflow continue dans le nouveau worktree

À la fin du workflow (Phase 8), le nettoyage du worktree est proposé.

## Commandes utilitaires

| Commande | Description |
|----------|-------------|
| `/dev:debug <error>` | Analyser et résoudre une erreur |
| `/dev:log <fichier>` | Ajouter `LoggableInterface` à un fichier PHP |
| `/dev:worktree <action>` | Gérer les git worktrees (voir section ci-dessus) |

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
