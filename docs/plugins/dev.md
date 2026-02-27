---
title: "dev"
description: "Workflow structuré de développement de features en 8 phases avec agents spécialisés, support git worktrees, implémentation forcée et refactoring sûr"
version: "2.6.1"
---

# dev <Badge type="info" text="v2.6.1" /> <Badge type="danger" text="Déprécié" />

::: warning Déprécié
Ce plugin est déprécié. Utilise les plugins-persona : analyst, architect, implementer, orchestrator
:::


Workflow structuré de développement de features avec **deux modes** :
- **Mode interactif** : 8 phases avec checkpoints utilisateur
- **Mode automatisé** : 10 phases entièrement non-interactives (depuis GitHub issues)

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

### Mode Interactif

#### Commande principale

```bash
/dev:feature <description>
```

Lance un workflow interactif en 8 phases avec checkpoints :

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

#### Voir le statut

```bash
/dev:status
```

Affiche l'état actuel du workflow et les commandes disponibles.

### Mode Automatisé

#### Commande principale

```bash
/dev:auto:feature <issue-number>
```

Lance un workflow **entièrement automatisé** en 10 phases :

```
🤖 Workflow automatique

  ⬜ 0. Prérequis  - Vérifier les outils
  ⬜ 1. Fetch      - Récupérer l'issue GitHub
  ⬜ 2. Discover   - Validation spec automatique
  ⬜ 3. Explore    - Explorer codebase
  ⬜ 4. Clarify    - Appliquer heuristiques
  ⬜ 5. Design     - Sélectionner architecture (Pragmatic Balance)
  ⬜ 6. Plan       - Générer specs
  ⬜ 7. Code       - Implémenter
  ⬜ 8. Review     - QA + auto-fix loop (3x max)
  ⬜ 9. Cleanup    - Nettoyer worktree
  ⬜ 10. Create PR - Créer la Pull Request
```

**Caractéristiques :**
- ✅ **Zéro interaction** : toutes les décisions automatisées
- ✅ **Spec depuis GitHub** : récupération automatique depuis issue
- ✅ **Multi-langage** : détection PHP/JavaScript/Go avec QA tools spécifiques
- ✅ **Auto-fix loop** : PHPStan level 9 blocker avec max 3 tentatives
- ✅ **Git worktree obligatoire** : création automatique, cleanup systématique
- ✅ **Rollback automatique** : en cas d'échec bloquant
- ✅ **PR automatique** : création en fin de workflow

**Configuration via `.env.claude` :**
```bash
MAIN_BRANCH=main
REPO=atournayre/claude-marketplace
PROJECT=
```

**Exemple :**
```bash
# Lancer le workflow auto pour issue #123
/dev:auto:feature 123

# Laisse le workflow s'exécuter jusqu'au bout
# Une PR sera créée automatiquement à la fin
```

## Task Management System

**Nouveauté v2.3.2** : Les skills de workflow intègrent le task management system de Claude Code pour un suivi en temps réel.

### Skills avec task management

| Skill | Nombre de tâches | Type de workflow |
|-------|------------------|------------------|
| `dev:feature` | 9 tâches | Phases séquentielles avec checkpoints |
| `dev:auto:feature` | 11 tâches | Phases automatiques complètes |
| `dev:review` | 4 tâches | 3 reviews parallèles + consolidation |
| `dev:explore` | 4 tâches | 3 agents parallèles + consolidation |
| `dev:plan` | 5 tâches | Étapes séquentielles de planification |

### Fonctionnalités

- **Progression visible** : Utilise `TaskList` pour voir l'état en temps réel
- **Statuts clairs** : pending → in_progress → completed
- **Dépendances** : Certaines tâches bloquent d'autres (ex: consolidation bloquée par agents)
- **Agents parallèles** : Suivi des agents qui s'exécutent en parallèle
- **Spinner actif** : Affichage du nom de la tâche en cours via `activeForm`

### Exemple d'utilisation

```bash
# Lancer un workflow
/dev:feature "Ajouter authentication"

# Dans un autre terminal/session, voir la progression
TaskList

# Output:
# #1 [completed] Discover - Comprendre le besoin
# #2 [completed] Explore - Explorer codebase
# #3 [in_progress] Clarify - Questions clarification
# #4 [pending] Design - Proposer architectures
# ...
```

## Phases individuelles (Mode Interactif)

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

# Le worktree est créé dans : .worktrees/oauth-auth
# Branche créée : feature/oauth-auth

# Basculer vers le worktree
cd .worktrees/oauth-auth

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
├── skills/                    # Skills au format Claude Code natif
│   ├── feature/              # Orchestrateur mode interactif
│   ├── status/               # Affiche plan
│   ├── discover/             # Phase 0 (interactif)
│   ├── explore/              # Phase 1 (interactif)
│   ├── clarify/              # Phase 2 (interactif)
│   ├── design/               # Phase 3 (interactif)
│   ├── plan/                 # Phase 4 (interactif)
│   ├── code/                 # Phase 5 (interactif)
│   ├── review/               # Phase 6 (interactif)
│   ├── summary/              # Phase 7 (interactif)
│   ├── debug/                # Utilitaire
│   ├── log/                  # Utilitaire
│   ├── worktree/             # Gestion worktrees
│   └── auto-*/               # Skills mode automatisé (10 skills)
│       ├── auto-feature/              # Orchestrateur (Phases 0-10)
│       ├── auto-check-prerequisites/  # Phase 0
│       ├── auto-fetch-issue/          # Phase 1
│       ├── auto-discover/             # Phase 2
│       ├── auto-explore/              # Phase 3
│       ├── auto-clarify/              # Phase 4
│       ├── auto-design/               # Phase 5
│       ├── auto-plan/                 # Phase 6
│       ├── auto-code/                 # Phase 7
│       └── auto-review/               # Phase 8
├── agents/                   # Agents spécialisés (deprecated - voir skills)
├── README.md
└── CHANGELOG.md
```

## Checkpoints (Mode Interactif Uniquement)

Le workflow interactif inclut des checkpoints aux phases critiques :

- **Phase 0** : Confirmation de la compréhension
- **Phase 2** : Attente des réponses aux questions
- **Phase 3** : Choix de l'architecture
- **Phase 5** : Approbation avant implémentation
- **Phase 6** : Décision sur les corrections (fix now / fix later / proceed)

**Note :** Le mode automatisé `/dev:auto:feature` n'a aucun checkpoint - toutes les décisions sont prises automatiquement via heuristiques.

## Fichiers Générés

### Mode Interactif
- `.claude/data/.dev-workflow-state.json` : État du workflow en cours (non versionné)
- `docs/specs/feature-*.md` : Plans d'implémentation

### Mode Automatisé
- `.claude/data/workflows/issue-{number}-dev-workflow-state.json` : État complet du workflow avec timing et décisions (non versionné)
- `docs/specs/feature-*.md` : Plans d'implémentation générés automatiquement

## Licence

MIT
