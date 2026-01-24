---
name: dev:worktree
description: Gestion des git worktrees pour développement parallèle
argument-hint: <action> [args]
model: claude-sonnet-4-5-20250929
allowed-tools: [Bash, Read, Write, Edit, Grep, TodoWrite, AskUserQuestion]
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Gérer les git worktrees pour permettre le développement de plusieurs features en parallèle sans conflits.

# Actions disponibles

## create

Créer un nouveau worktree pour une feature.

**Usage :**
```
/dev:worktree create <feature-name> [base-branch]
```

**Arguments :**
- `feature-name` : Nom de la feature (ex: "oauth-auth", "refactor-payment")
- `base-branch` : Branche de base (défaut: main ou master)

**Exemple :**
```
/dev:worktree create oauth-auth
/dev:worktree create hotfix-payment main
```

**Comportement :**
1. Détecter la branche principale (main/master)
2. Normaliser le nom de la feature (kebab-case)
3. Créer la branche `feature/<feature-name>` ou `hotfix/<feature-name>`
4. Créer le worktree dans `.worktrees/<feature-name>`
5. Mettre à jour `.claude/data/.dev-worktrees.json` avec les métadonnées
6. Afficher les instructions pour basculer vers le worktree

## list

Lister tous les worktrees actifs.

**Usage :**
```
/dev:worktree list
```

## remove

Supprimer un worktree (après merge ou abandon).

**Usage :**
```
/dev:worktree remove <feature-name>
```

**Comportement :**
1. Vérifier qu'il n'y a pas de modifications non commitées
2. Demander confirmation si des commits non poussés existent
3. Supprimer le worktree avec `git worktree remove`
4. Optionnellement supprimer la branche (demander confirmation)
5. Mettre à jour `.claude/data/.dev-worktrees.json`

## status

Afficher le statut détaillé d'un ou tous les worktrees.

**Usage :**
```
/dev:worktree status [feature-name]
```

## switch

Basculer vers un worktree existant (utilitaire de navigation).

**Usage :**
```
/dev:worktree switch <feature-name>
```

**Comportement :**
Afficher les commandes pour changer de répertoire

# Règles de nommage

- **Features** : `feature/<name>` → worktree dans `.worktrees/<name>`
- **Hotfixes** : `hotfix/<name>` → worktree dans `.worktrees/<name>`
- **Nom normalisé** : kebab-case uniquement (convertir espaces et caractères spéciaux)
