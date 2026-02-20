---
name: devops:branch
description: Création de branche Git avec workflow structuré
model: haiku
allowed-tools: [Bash, Read, AskUserQuestion]
argument-hint: [source-branch] <issue-number-or-text>
version: 1.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git checkout:*)"
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
              echo "Vous devez commit ou stash avant de créer une branche"
              exit 1
            fi
          once: true
  PostToolUse:
    - matcher: "Bash(git checkout -b:*)"
      hooks:
        - type: command
          command: |
            # Hook 2: Feedback création
            BRANCH=$(git branch --show-current)
            echo "Branche créée : $BRANCH"
            echo "Le tracking sera configuré automatiquement au premier commit"
          once: false
---

# Création de branche Git

Créer une nouvelle branche Git de manière structurée avec support des issues GitHub.

## Configuration

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/../git/skills/branch-core/scripts"
```

> Note : Les scripts partagés sont dans le plugin `git` (déprécié mais disponible).
> Référence : `git/skills/branch-core/scripts/`

## Variables
- SOURCE_BRANCH: Branche source (optionnel - défaut: MAIN_BRANCH de .env.claude)
- ISSUE_OR_TEXT: Numéro d'issue GitHub ou texte descriptif

## Relevant Files
- @.git/config
- @.gitignore
- @.env.claude
- @docs/README.md

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

**ÉTAPE CRITIQUE : CHECKOUT VERS SOURCE D'ABORD**

### 1. Lire la configuration depuis .env.claude

- Lis le fichier `.env.claude` à la racine du projet courant
- Extrais la valeur de `MAIN_BRANCH` (fallback pour SOURCE_BRANCH)

### 2. Parser les arguments et résoudre SOURCE_BRANCH

**Logique de désambiguisation selon le nombre d'arguments :**

**2 arguments fournis :**
- Premier argument = SOURCE_BRANCH
- Second argument = ISSUE_OR_TEXT

**1 argument fourni :**
- Si c'est un entier -> ISSUE_OR_TEXT (numéro d'issue), SOURCE_BRANCH = `MAIN_BRANCH` de .env.claude
- Si ça correspond à une branche locale existante (`git branch --list "$ARG"` non vide) -> SOURCE_BRANCH, ISSUE_OR_TEXT non fourni (sera demandé à l'utilisateur)
- Sinon -> ISSUE_OR_TEXT (texte descriptif), SOURCE_BRANCH = `MAIN_BRANCH` de .env.claude

**0 argument :**
- SOURCE_BRANCH = `MAIN_BRANCH` de .env.claude
- ISSUE_OR_TEXT non fourni (sera demandé à l'utilisateur)

**Si SOURCE_BRANCH n'est toujours pas résolu** :
- Utilise AskUserQuestion pour demander :
  ```
  Question: "Depuis quelle branche veux-tu créer la nouvelle branche ?"
  Options: ["main", "master", "develop", "Autre"]
  ```

### 3. Valider que SOURCE_BRANCH existe localement

- Exécute avec Bash :
  ```bash
  bash "$CORE_SCRIPTS/validate-source-branch.sh" "$SOURCE_BRANCH"
  ```
- Si le script échoue (exit 1), arrête le workflow

### 4. CHECKOUT VERS SOURCE_BRANCH AVANT TOUT

- Exécute `git checkout $SOURCE_BRANCH` avec Bash
- Exécute `git branch --show-current` pour vérifier
- **CRITIQUE** : Cette étape garantit qu'on crée depuis un point propre

### 5. PULL POUR METTRE À JOUR SOURCE_BRANCH

- Exécute `git pull origin $SOURCE_BRANCH` avec Bash
- **CRITIQUE** : Garantit qu'on part du dernier commit de origin

### 6. Résoudre le nom de la nouvelle branche

**Si ISSUE_OR_TEXT est fourni :**

- Exécute avec Bash :
  ```bash
  eval "$(bash "$CORE_SCRIPTS/resolve-branch-name.sh" "$ISSUE_OR_TEXT")"
  echo "BRANCH_NAME=$BRANCH_NAME"
  echo "PREFIX=$PREFIX"
  echo "PREFIX_SOURCE=$PREFIX_SOURCE"
  ```
- Si le script échoue (exit 1), arrête le workflow

**Si ISSUE_OR_TEXT n'est pas fourni :**
   - Utilise AskUserQuestion pour demander le nom de branche

### 7. Vérifier que la nouvelle branche n'existe pas

- Exécute avec Bash :
  ```bash
  bash "$CORE_SCRIPTS/check-branch-exists.sh" "$BRANCH_NAME"
  ```
- Si le script échoue (exit 1), arrête le workflow

### 8. Créer et checkout la nouvelle branche

- Exécute `git checkout -b $BRANCH_NAME` avec Bash

### 9. Afficher le résumé

Affiche :
```
Branche créée : $BRANCH_NAME
Préfixe détecté : $PREFIX (source: $PREFIX_SOURCE)
Depuis : $SOURCE_BRANCH
{Si issue} Issue associée : #$ISSUE_NUMBER

Le tracking sera configuré automatiquement au premier commit avec :
   git push -u origin $BRANCH_NAME
```

**IMPORTANT - NE PAS configurer de tracking automatiquement :**
- INTERDIT : `git branch --set-upstream-to=origin/$SOURCE_BRANCH $BRANCH_NAME`
- Le tracking sera configuré lors du premier push avec `-u`

## Expertise

Conventions de nommage des branches (préfixe détecté automatiquement) :
- `feature/{numéro}-{description}` : Nouvelles fonctionnalités
- `fix/{numéro}-{description}` : Corrections de bugs
- `hotfix/{numéro}-{description}` : Corrections urgentes en production
- `chore/{numéro}-{description}` : Maintenance, refactoring
- `docs/{numéro}-{description}` : Documentation
- `test/{numéro}-{description}` : Tests

Détection automatique du préfixe (par priorité) :
1. Labels de l'issue GitHub
2. Mots-clés dans la description de l'issue
3. Mots-clés dans le titre de l'issue
4. Défaut : `feature/` si aucun indicateur trouvé

## Désambiguisation des arguments

SOURCE_BRANCH est **optionnel** et défaut à `MAIN_BRANCH` de `.env.claude`.

| Argument | Type détecté | SOURCE_BRANCH | ISSUE_OR_TEXT |
|----------|-------------|---------------|---------------|
| `42` | Entier | MAIN_BRANCH (.env.claude) | `42` (issue) |
| `develop` | Branche locale existante | `develop` | Non fourni (demander) |
| `"fix login bug"` | Texte | MAIN_BRANCH (.env.claude) | `"fix login bug"` |

## Examples

```bash
# Créer une branche avec issue (source = MAIN_BRANCH de .env.claude)
/devops:branch 123

# Créer une branche avec texte descriptif (source = MAIN_BRANCH)
/devops:branch "user authentication"

# Créer une branche depuis une branche source explicite avec issue
/devops:branch develop 123

# Créer une branche fix avec texte explicite (source = MAIN_BRANCH)
/devops:branch "fix login bug"

# Créer une branche depuis develop (demande issue/texte)
/devops:branch develop
```

## Validation
- SOURCE_BRANCH doit exister localement
- SOURCE_BRANCH optionnel (défaut: MAIN_BRANCH de .env.claude)
- CHECKOUT vers SOURCE_BRANCH AVANT création (CRITIQUE)
- PULL pour mettre à jour SOURCE_BRANCH (CRITIQUE)
- La nouvelle branche ne doit pas déjà exister
- Le nom généré respecte les conventions de nommage
