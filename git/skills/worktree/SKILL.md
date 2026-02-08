---
name: git:worktree
description: Création de worktree Git avec workflow structuré
model: haiku
allowed-tools: [Bash, Read, AskUserQuestion]
argument-hint: [source-branch] <issue-number-or-text>
version: 2.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git worktree add:*)"
      hooks:
        - type: command
          command: |
            # Hook 1: Bloquer si modifications non commitées
            if ! git diff --quiet || ! git diff --cached --quiet; then
              echo "❌ ERREUR : Modifications non commitées détectées"
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
            echo "✅ Worktree créé avec succès"
          once: false
---

# Configuration de sortie

**IMPORTANT** : Cette skill effectue une opération Git rapide et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Création de worktree Git

Créer un nouveau worktree Git de manière structurée avec support des issues GitHub.

## Principe

Un worktree permet de travailler sur plusieurs branches en parallèle sans avoir à stash/commit. Chaque worktree est un répertoire séparé lié au même dépôt Git.

Le répertoire de base des worktrees est défini dans le `.env.claude` du projet utilisateur via la variable `WORKTREE_DIR`.

La convention de nommage du répertoire worktree est de remplacer les `/` du nom de branche par des `-`.
Exemple : branche `feature/ma-fonctionnalite` → répertoire `feature-ma-fonctionnalite`

## Configuration

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/branch-core/scripts"
```

## Variables
- SOURCE_BRANCH: Branche source (optionnel - défaut: MAIN_BRANCH de .env.claude)
- ISSUE_OR_TEXT: Numéro d'issue GitHub ou texte descriptif

## Relevant Files
- @.git/config
- @.gitignore
- @.env.claude

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Lire la configuration depuis .env.claude

- Lis le fichier `.env.claude` à la racine du projet courant (pas celui du plugin, celui du projet utilisateur)
- Extrais les valeurs de :
  - `WORKTREE_DIR` (répertoire de base des worktrees)
  - `MAIN_BRANCH` (fallback pour SOURCE_BRANCH)
- Si `WORKTREE_DIR` n'est pas défini ou est vide, utilise AskUserQuestion pour demander :
  ```
  Question: "La variable WORKTREE_DIR n'est pas définie dans .env.claude. Quel répertoire utiliser pour les worktrees ?"
  Options: ["../worktrees", ".worktrees", "Autre"]
  ```
- Vérifie que le répertoire parent de WORKTREE_DIR existe. Si non, affiche une erreur et arrête.

### 2. Parser les arguments et résoudre SOURCE_BRANCH

**Logique de désambiguisation selon le nombre d'arguments :**

**2 arguments fournis :**
- Premier argument = SOURCE_BRANCH
- Second argument = ISSUE_OR_TEXT

**1 argument fourni :**
- Si c'est un entier → ISSUE_OR_TEXT (numéro d'issue), SOURCE_BRANCH = `MAIN_BRANCH` de .env.claude
- Si ça correspond à une branche locale existante (`git branch --list "$ARG"` non vide) → SOURCE_BRANCH, ISSUE_OR_TEXT non fourni (sera demandé à l'utilisateur)
- Sinon → ISSUE_OR_TEXT (texte descriptif), SOURCE_BRANCH = `MAIN_BRANCH` de .env.claude

**0 argument :**
- SOURCE_BRANCH = `MAIN_BRANCH` de .env.claude
- ISSUE_OR_TEXT non fourni (sera demandé à l'utilisateur)

**Si SOURCE_BRANCH n'est toujours pas résolu** (MAIN_BRANCH absent de .env.claude et pas fourni en argument) :
- Utilise AskUserQuestion pour demander :
  ```
  Question: "Depuis quelle branche veux-tu créer le nouveau worktree ?"
  Options: ["main", "master", "develop", "Autre"]
  ```

### 3. Valider que SOURCE_BRANCH existe localement

- Exécute avec Bash :
  ```bash
  bash "$CORE_SCRIPTS/validate-source-branch.sh" "$SOURCE_BRANCH"
  ```
- Si le script échoue (exit 1), arrête le workflow

### 4. 🔴 METTRE À JOUR SOURCE_BRANCH 🔴

- Exécute `git fetch origin $SOURCE_BRANCH` avec Bash
- **CRITIQUE** : Garantit qu'on part du dernier commit de origin
- Note : On utilise `fetch` au lieu de `checkout + pull` car on ne veut pas changer la branche courante du worktree principal

### 5. Résoudre le nom de la nouvelle branche

- Extrais ISSUE_OR_TEXT depuis $ARGUMENTS (second argument)

**Si ISSUE_OR_TEXT est fourni :**

- Exécute avec Bash :
  ```bash
  eval "$(bash "$CORE_SCRIPTS/resolve-branch-name.sh" "$ISSUE_OR_TEXT")"
  echo "BRANCH_NAME=$BRANCH_NAME"
  echo "PREFIX=$PREFIX"
  echo "PREFIX_SOURCE=$PREFIX_SOURCE"
  echo "WORKTREE_DIRNAME=$WORKTREE_DIRNAME"
  ```
- Si le script échoue (exit 1), arrête le workflow
- Les variables `BRANCH_NAME`, `PREFIX`, `PREFIX_SOURCE`, `ISSUE_NUMBER`, `WORKTREE_DIRNAME` sont disponibles

**Si ISSUE_OR_TEXT n'est pas fourni :**
   - Utilise AskUserQuestion pour demander le nom de branche

### 6. Vérifier que la nouvelle branche n'existe pas

- Exécute avec Bash :
  ```bash
  bash "$CORE_SCRIPTS/check-branch-exists.sh" "$BRANCH_NAME"
  ```
- Si le script échoue (exit 1), arrête le workflow

### 7. Calculer le chemin du worktree

- Le chemin complet est : `$WORKTREE_DIR/$WORKTREE_DIRNAME`
  - Exemple : `/home/user/worktrees/feature-42-login-fix`

### 8. Vérifier que le répertoire worktree n'existe pas déjà

- Vérifie avec `test -d "$WORKTREE_PATH"` via Bash
- Si le répertoire existe, affiche :
  ```
  ❌ ERREUR : Le répertoire worktree '$WORKTREE_PATH' existe déjà

  Supprime-le d'abord ou choisis un autre nom
  ```
  - Arrête le workflow

### 9. Créer le worktree

- Exécute `git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" "origin/$SOURCE_BRANCH"` avec Bash
- Cette commande :
  - Crée le répertoire worktree
  - Crée la branche depuis le dernier état distant de SOURCE_BRANCH
  - Checkout la branche dans le worktree

### 10. Afficher le résumé

Affiche :
```
✅ Worktree créé : $BRANCH_NAME
📁 Répertoire : $WORKTREE_PATH
📝 Préfixe détecté : $PREFIX (source: $PREFIX_SOURCE)
📍 Depuis : $SOURCE_BRANCH
{Si issue} 🔗 Issue associée : #$ISSUE_NUMBER

Pour travailler dans ce worktree :
   cd $WORKTREE_PATH

📝 Le tracking sera configuré automatiquement au premier push avec :
   git push -u origin $BRANCH_NAME
```

**⚠️ IMPORTANT - NE PAS configurer de tracking automatiquement :**
- ❌ **INTERDIT** : `git branch --set-upstream-to=origin/$SOURCE_BRANCH $BRANCH_NAME`
- ✅ Le tracking sera configuré lors du premier push avec `-u`
- **RAISON** : Configurer le tracking vers SOURCE_BRANCH pousse les commits sur la branche parente au lieu de créer une nouvelle branche distante

## Expertise
Conventions de nommage des branches (préfixe détecté automatiquement) :
- `feature/{numéro}-{description}` : Nouvelles fonctionnalités
- `fix/{numéro}-{description}` : Corrections de bugs
- `hotfix/{numéro}-{description}` : Corrections urgentes en production
- `chore/{numéro}-{description}` : Maintenance, refactoring
- `docs/{numéro}-{description}` : Documentation
- `test/{numéro}-{description}` : Tests
- Utilise des tirets, pas d'espaces ni caractères spéciaux

Détection automatique du préfixe (par priorité) :
1. Labels de l'issue GitHub
2. Mots-clés dans la description de l'issue
3. Mots-clés dans le titre de l'issue
4. Défaut : `feature/` si aucun indicateur trouvé

Convention de nommage du répertoire worktree :
- Remplacer `/` par `-` dans le nom de branche
- `feature/ma-fonctionnalite` → `feature-ma-fonctionnalite`
- `fix/42-login-bug` → `fix-42-login-bug`
- `hotfix/critical-payment` → `hotfix-critical-payment`

## Template
```bash
# Exemple 1 : Issue seule (SOURCE_BRANCH = MAIN_BRANCH de .env.claude)
/git:worktree 42
# → Résolution via branch-core : fix/42-login-form-crashes-on-submit
# → Worktree dans: $WORKTREE_DIR/fix-42-login-form-crashes-on-submit

# Exemple 2 : Issue avec branche source explicite
/git:worktree develop 42
# → Résolution via branch-core : fix/42-login-form-crashes-on-submit (depuis develop)
# → Worktree dans: $WORKTREE_DIR/fix-42-login-form-crashes-on-submit

# Exemple 3 : Texte descriptif seul (SOURCE_BRANCH = MAIN_BRANCH de .env.claude)
/git:worktree "fix login validation"
# → Résolution via branch-core : fix/login-validation
# → Worktree dans: $WORKTREE_DIR/fix-login-validation

# Exemple 4 : Texte descriptif avec branche source
/git:worktree main "Add OAuth support"
# → Résolution via branch-core : feature/add-oauth-support
# → Worktree dans: $WORKTREE_DIR/feature-add-oauth-support

# Exemple 5 : Sans argument (SOURCE_BRANCH = MAIN_BRANCH, demande issue/texte)
/git:worktree
```

## Examples
```bash
# Créer un worktree avec issue (source = MAIN_BRANCH de .env.claude)
/git:worktree 123

# Créer un worktree avec texte descriptif (source = MAIN_BRANCH)
/git:worktree "user authentication"

# Créer un worktree depuis une branche source explicite avec issue
/git:worktree develop 123

# Créer un worktree fix avec texte explicite (source = MAIN_BRANCH)
/git:worktree "fix login bug"

# Créer un worktree hotfix (source = MAIN_BRANCH)
/git:worktree "hotfix critical payment issue"

# Créer un worktree depuis develop (demande issue/texte)
/git:worktree develop

# Créer un worktree depuis une branche existante avec issue
/git:worktree feature/api-base 456
```

## Report
- Nom de la branche créée
- Chemin du worktree créé
- Préfixe détecté et sa source (label/description/titre/défaut)
- Branche source utilisée
- Issue associée (si applicable)
- Commande `cd` pour accéder au worktree
- Note : Le tracking remote sera configuré lors du premier push avec `git push -u origin $BRANCH_NAME`

## Validation
- ✅ `WORKTREE_DIR` doit être défini dans `.env.claude` (ou demandé à l'utilisateur)
- ✅ Le répertoire parent de `WORKTREE_DIR` doit exister
- ✅ `SOURCE_BRANCH` doit exister localement
- ✅ `SOURCE_BRANCH` optionnel (défaut: MAIN_BRANCH de .env.claude)
- ✅ **FETCH pour mettre à jour SOURCE_BRANCH** (CRITIQUE)
- ✅ La nouvelle branche ne doit pas déjà exister
- ✅ Le répertoire worktree ne doit pas déjà exister
- ✅ Si `ISSUE_OR_TEXT` est un numéro, l'issue doit exister sur GitHub
- ✅ Le nom généré respecte les conventions de nommage
- ✅ Détection automatique entre numéro d'issue et texte descriptif

## Pourquoi fetch au lieu de checkout + pull ?

**Différence avec git:branch :**
- `git:branch` fait `checkout SOURCE_BRANCH` puis `pull` car il crée la branche depuis le HEAD courant
- `git:worktree` fait `fetch` car `git worktree add -b BRANCH "origin/SOURCE_BRANCH"` crée directement depuis la ref distante
- On ne veut pas changer la branche courante du worktree principal (l'utilisateur peut y travailler)

**Avantage :**
- L'utilisateur reste sur sa branche courante dans le worktree principal
- Le worktree est créé depuis le dernier état distant de SOURCE_BRANCH
- Pas de risque de conflits dans le worktree principal
