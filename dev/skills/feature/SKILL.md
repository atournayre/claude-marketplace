---
name: dev:feature
description: Workflow complet de développement de feature
argument-hint: <description-feature>
model: claude-sonnet-4-5-20250929
allowed-tools: [Read, Write, Edit, Grep, Glob, Task, TodoWrite, AskUserQuestion, Bash]
version: 1.0.0
license: MIT
---

# Objectif

Orchestrateur du workflow de développement en 8 phases. Enchaîne automatiquement toutes les étapes avec des checkpoints utilisateur.

# Feature demandée

$ARGUMENTS

# Prérequis

⚠️ **Plugin feature-dev requis** pour les agents spécialisés.

Si non installé, afficher :
```
⚠️ Pour une expérience optimale, installe le plugin feature-dev :
/plugin install feature-dev@claude-code-plugins

Ce plugin fournit les agents :
- code-explorer (exploration codebase)
- code-architect (design architecture)
- code-reviewer (review qualité)

Continuer sans ces agents ? (Les phases 1, 3, 6 seront simplifiées)
```

# Workflow

## Initialisation

1. **Proposition de worktree** (optionnel)

Demander à l'utilisateur s'il souhaite créer un worktree pour cette feature :

```
📂 Créer un worktree pour cette feature ?

Avantages des worktrees :
  • Garder votre branche main propre
  • Travailler sur plusieurs features en parallèle
  • Préserver le contexte de développement (IDE, serveur, tests)
  • Pas besoin de stash ou de switcher de branche

Le worktree sera créé dans : .worktrees/{feature-slug}

Créer le worktree ? (o/n)
```

Si oui :
- Normaliser le nom de la feature en slug (kebab-case)
- Créer le worktree avec `/dev:worktree create {feature-slug}`
- Informer l'utilisateur du chemin et qu'il doit relancer Claude Code dans le worktree
- **ARRÊTER le workflow** avec un message :
  ```
  ✅ Worktree créé : .worktrees/{feature-slug}

  Pour continuer le workflow :
    1. cd .worktrees/{feature-slug}
    2. Relancer Claude Code
    3. /dev:feature {description}
  ```

Si non : Continuer le workflow normalement.

2. Créer le fichier `.claude/data/.dev-workflow-state.json` (créer le répertoire `.claude/data/` si nécessaire)

3. Créer la todo list avec toutes les phases

## Gestion du timing des phases

**Avant chaque phase :**
Enregistrer le timestamp de début dans `.claude/data/.dev-workflow-state.json`

**Après chaque phase :**
Calculer la durée et mettre à jour le fichier d'état

## Phase 0 : Discover

Exécuter le contenu de `/dev:discover`

**Checkpoint :** Confirmer que la compréhension est correcte.

## Phase 1 : Explore

Exécuter le contenu de `/dev:explore`

## Phase 2 : Clarify

Exécuter le contenu de `/dev:clarify`

**Checkpoint :** Attendre toutes les réponses.

## Phase 3 : Design

Exécuter le contenu de `/dev:design`

**Checkpoint :** Attendre le choix de l'architecture.

## Phase 4 : Plan

Exécuter le contenu de `/dev:plan`

## Phase 5 : Code

**Checkpoint :** Demander approbation avant de commencer.

Exécuter le contenu de `/dev:code`

## Phase 6 : Review

Exécuter le contenu de `/dev:review`

**Checkpoint :** Demander action (fix now / fix later / proceed).

## Phase 7 : Summary

Exécuter le contenu de `/dev:summary`

Calculer le temps total et afficher le récapitulatif des temps

## Phase 8 : Cleanup (optionnel)

Si un worktree a été créé, proposer de le nettoyer

# Affichage du statut

À chaque transition de phase, afficher :

```
🔄 Workflow de développement : {feature}

  ✅ 0. Discover   - Comprendre le besoin        (1m 23s)
  ✅ 1. Explore    - Explorer codebase           (2m 45s)
  🔵 2. Clarify    - Questions clarification  ← En cours
  ⬜ 3. Design     - Proposer architectures
  ⬜ 4. Plan       - Générer specs
  ⬜ 5. Code       - Implémenter
  ⬜ 6. Review     - QA complète
  ⬜ 7. Summary    - Résumé final
  ⬜ 8. Cleanup    - Nettoyer worktree (si créé)
```

# Règles

- **Proposition de worktree** à l'initialisation (optionnel)
- **Checkpoints obligatoires** aux phases 0, 2, 3, 5, 6
- **Ne jamais sauter de phase** (0-7)
- **Phase 8 (Cleanup)** uniquement si un worktree a été créé
- **Mettre à jour** `.claude/data/.dev-workflow-state.json` après chaque phase
- **Afficher le statut** à chaque transition
- Si l'utilisateur interrompt, il peut reprendre avec `/dev:status` + la commande de la phase suivante
- **Worktrees** : Toutes les métadonnées sont dans `.claude/data/.dev-worktrees.json`

# Commande d'aide

Si l'utilisateur tape `/dev:feature` sans arguments, afficher l'aide complète.
