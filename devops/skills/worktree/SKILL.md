---
name: devops:worktree
description: Gestion des git worktrees pour développement parallèle (création, liste, suppression, statut, switch)
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, AskUserQuestion]
argument-hint: <action> [args] | [source-branch] <issue-number-or-text>
version: 1.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git worktree add:*)"
      hooks:
        - type: command
          command: |
            # Hook 1: Bloquer si modifications non commitées
            if ! git diff --quiet || ! git diff --cached --quiet; then
              echo "ERREUR : Modifications non commitées détectées"
              echo ""
              echo "Fichiers modifiés :"
              git status --short
              echo ""
              echo "Vous devez commit ou stash avant de créer un worktree"
              exit 1
            fi
          once: true
  PostToolUse:
    - matcher: "Bash(git worktree add:*)"
      hooks:
        - type: command
          command: |
            # Hook 2: Feedback création
            echo "Worktree créé avec succès"
          once: false
---

# Gestion des git worktrees

Créer et gérer des worktrees Git pour le développement parallèle.

## Configuration

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/../git/skills/branch-core/scripts"
```

> Note : Les scripts partagés sont dans le plugin `git` (déprécié mais disponible).
> Référence : `git/skills/branch-core/scripts/`

## Actions disponibles

### create (mode Git structuré)

Créer un nouveau worktree avec résolution de branche depuis une issue GitHub ou un texte.

**Usage :**
```
/devops:worktree [source-branch] <issue-number-or-text>
```

**Comportement :**
1. Lire `WORKTREE_DIR` et `MAIN_BRANCH` depuis `.env.claude`
2. Parser les arguments (même logique que `devops:branch`)
3. Valider SOURCE_BRANCH avec `validate-source-branch.sh`
4. Mettre à jour via `git fetch origin $SOURCE_BRANCH`
5. Résoudre le nom de branche via `resolve-branch-name.sh`
6. Vérifier que la branche n'existe pas via `check-branch-exists.sh`
7. Calculer le chemin : `$WORKTREE_DIR/$WORKTREE_DIRNAME`
8. Créer : `git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" "origin/$SOURCE_BRANCH"`
9. Afficher résumé avec `cd $WORKTREE_PATH`

### list

Lister tous les worktrees actifs.

**Usage :**
```
/devops:worktree list
```

**Comportement :**
```bash
git worktree list
```

### remove

Supprimer un worktree (après merge ou abandon).

**Usage :**
```
/devops:worktree remove <feature-name>
```

**Comportement :**
1. Vérifier qu'il n'y a pas de modifications non commitées
2. Demander confirmation si des commits non poussés existent
3. Supprimer le worktree avec `git worktree remove`
4. Optionnellement supprimer la branche (demander confirmation)
5. Mettre à jour `.claude/data/.dev-worktrees.json` si présent

### status

Afficher le statut détaillé d'un ou tous les worktrees.

**Usage :**
```
/devops:worktree status [feature-name]
```

### switch

Afficher les commandes pour basculer vers un worktree existant.

**Usage :**
```
/devops:worktree switch <feature-name>
```

## Variables (mode create)
- SOURCE_BRANCH: Branche source (optionnel - défaut: MAIN_BRANCH de .env.claude)
- ISSUE_OR_TEXT: Numéro d'issue GitHub ou texte descriptif

## Relevant Files
- @.git/config
- @.gitignore
- @.env.claude

## Instructions à Exécuter (mode create)

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Lire la configuration depuis .env.claude

- Extrais `WORKTREE_DIR` et `MAIN_BRANCH`
- Si `WORKTREE_DIR` absent, utilise AskUserQuestion :
  ```
  Question: "La variable WORKTREE_DIR n'est pas définie dans .env.claude. Quel répertoire utiliser pour les worktrees ?"
  Options: ["../worktrees", ".worktrees", "Autre"]
  ```
- Vérifie que le répertoire parent de WORKTREE_DIR existe

### 2. Parser les arguments et résoudre SOURCE_BRANCH

**2 arguments :** Premier = SOURCE_BRANCH, Second = ISSUE_OR_TEXT

**1 argument :**
- Entier -> ISSUE_OR_TEXT, SOURCE_BRANCH = MAIN_BRANCH
- Branche locale existante -> SOURCE_BRANCH, ISSUE_OR_TEXT demandé
- Texte -> ISSUE_OR_TEXT, SOURCE_BRANCH = MAIN_BRANCH

**0 argument :** SOURCE_BRANCH = MAIN_BRANCH, ISSUE_OR_TEXT demandé

### 3. Valider SOURCE_BRANCH

```bash
bash "$CORE_SCRIPTS/validate-source-branch.sh" "$SOURCE_BRANCH"
```

### 4. Mettre à jour SOURCE_BRANCH (fetch)

```bash
git fetch origin $SOURCE_BRANCH
```

Note : On utilise `fetch` au lieu de `checkout + pull` pour ne pas changer la branche courante.

### 5. Résoudre le nom de branche

```bash
eval "$(bash "$CORE_SCRIPTS/resolve-branch-name.sh" "$ISSUE_OR_TEXT")"
echo "BRANCH_NAME=$BRANCH_NAME"
echo "WORKTREE_DIRNAME=$WORKTREE_DIRNAME"
```

### 6. Vérifier que la branche n'existe pas

```bash
bash "$CORE_SCRIPTS/check-branch-exists.sh" "$BRANCH_NAME"
```

### 7. Calculer le chemin du worktree

- Chemin complet : `$WORKTREE_DIR/$WORKTREE_DIRNAME`

### 8. Vérifier que le répertoire n'existe pas déjà

```bash
test -d "$WORKTREE_PATH"
```
- Si existe -> erreur et arrêt

### 9. Créer le worktree

```bash
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" "origin/$SOURCE_BRANCH"
```

### 10. Afficher le résumé

```
Worktree créé : $BRANCH_NAME
Répertoire : $WORKTREE_PATH
Préfixe détecté : $PREFIX (source: $PREFIX_SOURCE)
Depuis : $SOURCE_BRANCH
{Si issue} Issue associée : #$ISSUE_NUMBER

Pour travailler dans ce worktree :
   cd $WORKTREE_PATH

Le tracking sera configuré automatiquement au premier push avec :
   git push -u origin $BRANCH_NAME
```

**IMPORTANT - NE PAS configurer de tracking automatiquement**

## Règles de nommage

- **Features** : `feature/<name>` -> worktree dans `$WORKTREE_DIR/feature-<name>`
- **Hotfixes** : `hotfix/<name>` -> worktree dans `$WORKTREE_DIR/hotfix-<name>`
- Remplacer `/` par `-` dans le nom de branche pour le répertoire
- Exemple : `feature/42-login-fix` -> `feature-42-login-fix`

## Examples

```bash
# Créer un worktree avec issue (source = MAIN_BRANCH)
/devops:worktree 123

# Créer un worktree avec texte descriptif
/devops:worktree "user authentication"

# Créer un worktree depuis une branche source explicite
/devops:worktree develop 123

# Lister les worktrees actifs
/devops:worktree list

# Supprimer un worktree
/devops:worktree remove feature-auth

# Voir le statut
/devops:worktree status
```

## Validation
- WORKTREE_DIR doit être défini dans `.env.claude` (ou demandé)
- Le répertoire parent de WORKTREE_DIR doit exister
- SOURCE_BRANCH doit exister localement
- FETCH pour mettre à jour SOURCE_BRANCH (CRITIQUE)
- La nouvelle branche ne doit pas déjà exister
- Le répertoire worktree ne doit pas déjà exister
