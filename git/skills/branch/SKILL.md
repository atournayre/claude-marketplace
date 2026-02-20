---
name: git:branch
description: Création de branche Git avec workflow structuré
model: haiku
allowed-tools: [Bash, Read, AskUserQuestion]
argument-hint: [source-branch] <issue-number-or-text>
version: 2.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git checkout:*)"
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
            echo "✅ Branche créée : $BRANCH"
            echo "📝 Le tracking sera configuré automatiquement au premier commit"
          once: false
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `devops:branch`. Voir le plugin `devops`. Sera supprimée en v3.0.

# Configuration de sortie

**IMPORTANT** : Cette skill effectue une opération Git rapide et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Création de branche Git

Créer une nouvelle branche Git de manière structurée avec support des issues GitHub.

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
- @docs/README.md

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

**🚨 ÉTAPE CRITIQUE : CHECKOUT VERS SOURCE D'ABORD 🚨**

### 1. Lire la configuration depuis .env.claude

- Lis le fichier `.env.claude` à la racine du projet courant (pas celui du plugin, celui du projet utilisateur)
- Extrais la valeur de `MAIN_BRANCH` (fallback pour SOURCE_BRANCH)

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
  Question: "Depuis quelle branche veux-tu créer la nouvelle branche ?"
  Options: ["main", "master", "develop", "Autre"]
  ```

### 3. Valider que SOURCE_BRANCH existe localement

- Exécute avec Bash :
  ```bash
  bash "$CORE_SCRIPTS/validate-source-branch.sh" "$SOURCE_BRANCH"
  ```
- Si le script échoue (exit 1), arrête le workflow

### 4. 🔴 CHECKOUT VERS SOURCE_BRANCH AVANT TOUT 🔴

- Exécute `git checkout $SOURCE_BRANCH` avec Bash
- Exécute `git branch --show-current` pour vérifier qu'on est bien dessus
- **CRITIQUE** : Cette étape garantit qu'on crée depuis un point propre

### 5. 🔴 PULL POUR METTRE À JOUR SOURCE_BRANCH 🔴

- Exécute `git pull origin $SOURCE_BRANCH` avec Bash
- **CRITIQUE** : Garantit qu'on part du dernier commit de origin
- Évite de créer depuis un point obsolète

### 6. Résoudre le nom de la nouvelle branche

**Si ISSUE_OR_TEXT est fourni (résolu à l'étape 2) :**

- Exécute avec Bash :
  ```bash
  eval "$(bash "$CORE_SCRIPTS/resolve-branch-name.sh" "$ISSUE_OR_TEXT")"
  echo "BRANCH_NAME=$BRANCH_NAME"
  echo "PREFIX=$PREFIX"
  echo "PREFIX_SOURCE=$PREFIX_SOURCE"
  ```
- Si le script échoue (exit 1), arrête le workflow
- Les variables `BRANCH_NAME`, `PREFIX`, `PREFIX_SOURCE`, `ISSUE_NUMBER` sont disponibles

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
- La branche est créée depuis SOURCE_BRANCH (car on est dessus)

### 9. Afficher le résumé

Affiche :
```
✅ Branche créée : $BRANCH_NAME
📝 Préfixe détecté : $PREFIX (source: $PREFIX_SOURCE)
📍 Depuis : $SOURCE_BRANCH
{Si issue} 🔗 Issue associée : #$ISSUE_NUMBER

📝 Le tracking sera configuré automatiquement au premier commit avec :
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

## Template
```bash
# Exemple 1 : Issue seule (SOURCE_BRANCH = MAIN_BRANCH de .env.claude)
/git:branch 42
# → Résolution via branch-core : fix/42-login-form-crashes-on-submit

# Exemple 2 : Issue avec branche source explicite
/git:branch develop 42
# → Résolution via branch-core : fix/42-login-form-crashes-on-submit (depuis develop)

# Exemple 3 : Texte descriptif seul (SOURCE_BRANCH = MAIN_BRANCH de .env.claude)
/git:branch "fix login validation"
# → Résolution via branch-core : fix/login-validation

# Exemple 4 : Texte descriptif avec branche source
/git:branch main "Add OAuth support"
# → Résolution via branch-core : feature/add-oauth-support

# Exemple 5 : Sans argument (SOURCE_BRANCH = MAIN_BRANCH, demande issue/texte)
/git:branch
```

## Examples
```bash
# Créer une branche avec issue (source = MAIN_BRANCH de .env.claude)
/git:branch 123

# Créer une branche avec texte descriptif (source = MAIN_BRANCH)
/git:branch "user authentication"

# Créer une branche depuis une branche source explicite avec issue
/git:branch develop 123

# Créer une branche fix avec texte explicite (source = MAIN_BRANCH)
/git:branch "fix login bug"

# Créer une branche hotfix (source = MAIN_BRANCH)
/git:branch "hotfix critical payment issue"

# Créer une branche depuis develop (demande issue/texte)
/git:branch develop

# Créer une branche depuis une branche existante avec issue
/git:branch feature/api-base 456
```

## Report
- Nom de la branche créée
- Préfixe détecté et sa source (label/description/titre/défaut/texte)
- Branche source utilisée
- Issue associée (si applicable)
- Statut du checkout
- Note : Le tracking remote sera configuré lors du premier push avec `git push -u origin $BRANCH_NAME`

## Validation
- ✅ `SOURCE_BRANCH` doit exister localement
- ✅ `SOURCE_BRANCH` optionnel (défaut: MAIN_BRANCH de .env.claude)
- ✅ **CHECKOUT vers SOURCE_BRANCH AVANT création** (CRITIQUE)
- ✅ **PULL pour mettre à jour SOURCE_BRANCH** (CRITIQUE)
- ✅ La nouvelle branche ne doit pas déjà exister
- ✅ Si `ISSUE_OR_TEXT` est un numéro, l'issue doit exister sur GitHub
- ✅ Le nom généré respecte les conventions de nommage
- ✅ Détection automatique entre numéro d'issue et texte descriptif

## Pourquoi checkout + pull vers SOURCE_BRANCH d'abord ?

**Problème 1 évité** :
- Si on est sur `feature/A` et on crée `feature/B` depuis `main`
- Sans checkout vers `main` d'abord, la branche est créée depuis `feature/A`
- Les commits de `feature/A` se retrouvent sur `feature/B`
- Résultat : impossible de créer une PR propre

**Problème 2 évité** :
- Si `main` locale est en retard sur `origin/main`
- Sans pull, on crée depuis un point obsolète
- Résultat : commits manquants, conflits, PR avec historique incorrect

**Solution** :
1. TOUJOURS faire `git checkout $SOURCE_BRANCH`
2. TOUJOURS faire `git pull origin $SOURCE_BRANCH`
3. PUIS créer avec `git checkout -b $BRANCH_NAME`
