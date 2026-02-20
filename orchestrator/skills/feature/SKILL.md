---
name: orchestrator:feature
description: Workflow complet de développement de feature. Mode interactif (description texte) avec 8 phases et checkpoints utilisateur. Mode automatique (numéro issue GitHub) avec 10 phases sans interaction. Utilise worktrees, task management et agents spécialisés.
argument-hint: <description-feature> | <issue-number> [--auto]
model: sonnet
allowed-tools: [Read, Write, Edit, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList, AskUserQuestion, Bash, Skill]
version: 1.0.0
license: MIT
---

# orchestrator:feature

Orchestrateur du workflow de développement. Selon les arguments, lance le mode interactif ou automatique.

## Détection du mode

- Si l'argument est un numéro entier ou contient `--auto` : **mode automatique** (10 phases, 0 interaction)
- Sinon : **mode interactif** (8 phases, checkpoints utilisateur)

## Mode Interactif

Workflow en 8 phases avec checkpoints. Feature décrite en texte libre.

### Initialisation

1. Proposer création d'un worktree (optionnel) via AskUserQuestion
2. Créer `.claude/data/.dev-workflow-state.json`
3. Créer les tâches du workflow via TaskCreate :
   - #0 Discover, #1 Explore, #2 Clarify, #3 Design, #4 Plan, #5 Code, #6 Review, #7 Summary
   - #8 Cleanup (uniquement si worktree créé)

### Phases (0 → 7)

Avant chaque phase : `TaskUpdate` → `in_progress`, enregistrer timestamp.
Après chaque phase : calculer durée, `TaskUpdate` → `completed`.

- **Phase 0 Discover** : Comprendre le besoin. Checkpoint : confirmer compréhension.
- **Phase 1 Explore** : Explorer le codebase.
- **Phase 2 Clarify** : Questions de clarification. Checkpoint : attendre toutes les réponses.
- **Phase 3 Design** : Proposer architectures. Checkpoint : attendre choix d'architecture.
- **Phase 4 Plan** : Générer les specs.
- **Phase 5 Code** : Checkpoint approbation → implémenter.
- **Phase 6 Review** : QA complète. Checkpoint : fix now / fix later / proceed.
- **Phase 7 Summary** : Résumé final avec récapitulatif des temps.
- **Phase 8 Cleanup** (si worktree) : Proposer nettoyage.

### Checkpoints obligatoires

Phases 0, 2, 3, 5, 6. Ne jamais sauter de phase.

## Mode Automatique

Workflow en 10 phases SANS interaction utilisateur. Input : numéro issue GitHub.

### Prérequis

Exécuter `orchestrator:check-prerequisites`. Exit 1 si quelque chose manque.

### Phases (0 → 10)

- **Phase 0** : Vérifier prérequis via `orchestrator:check-prerequisites`
- **Phase 1** : Fetch issue via `orchestrator:fetch-issue $ARGUMENTS`
- **Phase 2** : Worktree OBLIGATOIRE créé automatiquement
- **Phase 3** : Discover (heuristiques, pas d'interaction)
- **Phase 4** : Explore (time-box 5 minutes)
- **Phase 5** : Clarify (heuristiques automatiques)
- **Phase 6** : Design (choisit Pragmatic Balance automatiquement)
- **Phase 7** : Plan (sans interaction)
- **Phase 8** : Code (implémente directement)
- **Phase 9** : Review (boucle auto-fix max 3 tentatives)
- **Phase 10** : Cleanup worktree + créer PR via git:pr

### Règles mode auto

- 0 checkpoints utilisateur
- Worktree OBLIGATOIRE (création + cleanup automatiques)
- CI DOIT PASSER (PHPStan niveau 9, tests)
- Rollback automatique en cas d'erreur bloquante
- PR créée automatiquement

### Gestion des erreurs (mode auto)

Si une phase échoue :
1. Logger dans `.claude/data/workflows/issue-{N}-dev-workflow-state.json`
2. `git reset --hard HEAD@{0}`
3. Supprimer le worktree
4. Exit code 1 avec message explicite

## Affichage du statut

À chaque transition de phase, afficher :

```
🔄 Workflow : {feature}

  ✅ 0. Discover   (1m 23s)
  🔵 1. Explore    ← En cours
  ⬜ 2. Clarify
  ...
```

## Format des durées

- `< 60s` → `{X}s`
- `< 60min` → `{X}m {Y}s`
- `>= 60min` → `{X}h {Y}m`

## Fichier d'état

Mode interactif : `.claude/data/.dev-workflow-state.json`
Mode auto : `.claude/data/workflows/issue-{N}-dev-workflow-state.json`

## Sans arguments

Afficher l'aide complète avec exemples d'utilisation.
