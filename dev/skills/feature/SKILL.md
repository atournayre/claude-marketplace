---
name: dev:feature
description: Workflow complet de développement de feature
argument-hint: <description-feature>
model: sonnet
allowed-tools: [Read, Write, Edit, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList, AskUserQuestion, Bash, Skill]
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `orchestrator:feature`. Voir le plugin `orchestrator`. Sera supprimée en v3.0.

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

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Initialisation

### 1. Proposition de worktree (optionnel)

- Utilise AskUserQuestion pour demander à l'utilisateur s'il souhaite créer un worktree pour cette feature :

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

3. **Créer les tâches du workflow**

Utiliser `TaskCreate` pour chaque phase :

```
TaskCreate #0: Discover - Comprendre le besoin
TaskCreate #1: Explore - Explorer codebase
TaskCreate #2: Clarify - Questions clarification
TaskCreate #3: Design - Proposer architectures
TaskCreate #4: Plan - Générer specs
TaskCreate #5: Code - Implémenter
TaskCreate #6: Review - QA complète
TaskCreate #7: Summary - Résumé final
TaskCreate #8: Cleanup - Nettoyer worktree (si créé)
```

**Important :**
- Utiliser `activeForm` (ex: "Comprenant le besoin", "Explorant le codebase")
- Ne créer la tâche #8 que si worktree créé
- Les tâches suivent l'ordre d'exécution (0→7 ou 0→8)

## Gestion du timing et progression

**Avant chaque phase :**
1. Utiliser `TaskUpdate` pour marquer la tâche comme `in_progress`
2. Enregistrer le timestamp de début dans `.claude/data/.dev-workflow-state.json`

**Après chaque phase :**
1. Calculer la durée et mettre à jour le fichier d'état
2. Utiliser `TaskUpdate` pour marquer la tâche comme `completed`

## Phase 0 : Discover

1. `TaskUpdate` → tâche #0 en `in_progress`
2. Exécuter le contenu de `/dev:discover`
3. **Checkpoint :** Confirmer que la compréhension est correcte
4. `TaskUpdate` → tâche #0 en `completed`

## Phase 1 : Explore

1. `TaskUpdate` → tâche #1 en `in_progress`
2. Exécuter le contenu de `/dev:explore`
3. `TaskUpdate` → tâche #1 en `completed`

## Phase 2 : Clarify

1. `TaskUpdate` → tâche #2 en `in_progress`
2. Exécuter le contenu de `/dev:clarify`
3. **Checkpoint :** Attendre toutes les réponses
4. `TaskUpdate` → tâche #2 en `completed`

## Phase 3 : Design

1. `TaskUpdate` → tâche #3 en `in_progress`
2. Exécuter le contenu de `/dev:design`
3. **Checkpoint :** Attendre le choix de l'architecture
4. `TaskUpdate` → tâche #3 en `completed`

## Phase 4 : Plan

1. `TaskUpdate` → tâche #4 en `in_progress`
2. Exécuter le contenu de `/dev:plan`
3. `TaskUpdate` → tâche #4 en `completed`

## Phase 5 : Code

1. **Checkpoint :** Demander approbation avant de commencer
2. `TaskUpdate` → tâche #5 en `in_progress`
3. Exécuter le contenu de `/dev:code`
4. `TaskUpdate` → tâche #5 en `completed`

## Phase 6 : Review

1. `TaskUpdate` → tâche #6 en `in_progress`
2. Exécuter le contenu de `/dev:review`
3. **Checkpoint :** Demander action (fix now / fix later / proceed)
4. `TaskUpdate` → tâche #6 en `completed`

## Phase 7 : Summary

1. `TaskUpdate` → tâche #7 en `in_progress`
2. Exécuter le contenu de `/dev:summary`
3. Calculer le temps total et afficher le récapitulatif des temps
4. `TaskUpdate` → tâche #7 en `completed`

## Phase 8 : Cleanup (optionnel)

1. Si un worktree a été créé :
   - `TaskUpdate` → tâche #8 en `in_progress`
   - Proposer de nettoyer le worktree
   - `TaskUpdate` → tâche #8 en `completed`

# Affichage du statut

**Deux systèmes complémentaires :**

1. **Task Management System** : Utiliser `TaskList` pour afficher l'état des tâches (pending/in_progress/completed)

2. **Affichage manuel avec timings** : À chaque transition de phase, afficher :

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

**Note :** Le task system ne gère pas les timings, donc l'affichage manuel reste nécessaire pour montrer les durées.

# Règles

- **Proposition de worktree** à l'initialisation (optionnel)
- **Checkpoints obligatoires** aux phases 0, 2, 3, 5, 6
- **Ne jamais sauter de phase** (0-7)
- **Phase 8 (Cleanup)** uniquement si un worktree a été créé
- **Task Management** :
  - Créer toutes les tâches à l'initialisation
  - Mettre à jour le statut avant/après chaque phase
  - Utiliser `TaskList` pour afficher la progression
- **Mettre à jour** `.claude/data/.dev-workflow-state.json` après chaque phase (pour les timings)
- **Afficher le statut** à chaque transition (task system + timings)
- Si l'utilisateur interrompt, il peut reprendre avec `/dev:status` + la commande de la phase suivante
- **Worktrees** : Toutes les métadonnées sont dans `.claude/data/.dev-worktrees.json`

# Commande d'aide

Si l'utilisateur tape `/dev:feature` sans arguments, afficher l'aide complète.
