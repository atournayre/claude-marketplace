---
name: git-pr
description: >
  Automatise la création de Pull Requests GitHub avec workflow complet incluant:
  QA intelligente (PHP), commits structurés, assignation milestone et projet,
  code review automatique. Utilisable via /git:pr ou invocation automatique
  quand l'utilisateur demande à créer/ouvrir/faire une PR.
allowed-tools: [Bash, Read, Write, TodoWrite, AskUserQuestion]
model: claude-sonnet-4-5-20250929
---

# Git Pull Request Automation Skill

## Variables

```bash
ARGUMENTS="$ARGUMENTS"  # Arguments passés par la slash command
PR_TEMPLATE_PATH=".github/pull_request_template.md"
SCRIPTS_DIR="./scripts"
REQUIRED_GH_SCOPES="repo read:org read:project project gist"
```

## Prérequis: Authentification GitHub

**IMPORTANT**: Avant d'utiliser ce skill, vérifier que l'authentification GitHub dispose de TOUS les scopes requis.

### Scopes Requis
- `repo`: Accès complet aux repos (PRs, commits, branches)
- `read:org`: Lecture informations organisation
- `read:project`: Lecture projets GitHub
- `project`: Écriture/assignation aux projets
- `gist`: Gestion des gists

### Vérification Automatique

Au début du workflow, TOUJOURS vérifier les scopes:

```bash
# Vérifier scopes actuels
CURRENT_SCOPES=$(gh auth status 2>&1 | grep "Token scopes" | cut -d: -f2 | tr -d "'")

# Vérifier si tous les scopes requis sont présents
MISSING_SCOPES=()
for scope in repo read:org read:project project gist; do
    if ! echo "$CURRENT_SCOPES" | grep -q "$scope"; then
        MISSING_SCOPES+=("$scope")
    fi
done

# Si scopes manquants, renouveler l'authentification
if [ ${#MISSING_SCOPES[@]} -gt 0 ]; then
    echo "⚠️  Scopes manquants: ${MISSING_SCOPES[*]}"
    echo "🔄 Renouvellement authentification..."
    bash $SCRIPTS_DIR/gh_auth_setup.sh
fi
```

### Script de Configuration

Un script `gh_auth_setup.sh` est disponible pour configurer automatiquement TOUS les scopes requis:

```bash
bash $SCRIPTS_DIR/gh_auth_setup.sh
```

Ce script garantit la constance des scopes à chaque renouvellement d'authentification.

## Workflow

### Étape 0: Timing

```bash
START_TIME=$(date +%s)
date  # Afficher timestamp début
```

### Étape 1: Parsing Arguments

Parser `$ARGUMENTS` pour extraire:
- `BRANCH_BASE`: Branche de destination (1er arg)
- `MILESTONE`: Milestone à assigner (2e arg, optionnel)
- `PROJECT_NAME`: Nom du projet (3e arg, optionnel)
- `DELETE_FLAG`: `--delete` présent ou non
- `NO_REVIEW_FLAG`: `--no-review` présent ou non

```bash
# Exemple parsing
ARGS=($ARGUMENTS)
BRANCH_BASE="${ARGS[0]}"
MILESTONE="${ARGS[1]}"
PROJECT_NAME="${ARGS[2]}"
DELETE_FLAG=""
NO_REVIEW_FLAG=""

for arg in "${ARGS[@]}"; do
    if [ "$arg" = "--delete" ]; then DELETE_FLAG="--delete"; fi
    if [ "$arg" = "--no-review" ]; then NO_REVIEW_FLAG="--no-review"; fi
done
```

### Étape 1.5: Vérification Scopes GitHub

**OBLIGATOIRE** : Vérifier les scopes GitHub avant toute opération.

```bash
# Vérifier scopes actuels
CURRENT_SCOPES=$(gh auth status 2>&1 | grep "Token scopes" | cut -d: -f2 | tr -d "'" | tr ',' ' ')

# Scopes requis
REQUIRED_SCOPES=(repo read:org read:project project gist)

# Vérifier si tous les scopes requis sont présents
MISSING_SCOPES=()
for scope in "${REQUIRED_SCOPES[@]}"; do
    if ! echo "$CURRENT_SCOPES" | grep -q "$scope"; then
        MISSING_SCOPES+=("$scope")
    fi
done

# Si scopes manquants, ARRÊT et demande renouvellement
if [ ${#MISSING_SCOPES[@]} -gt 0 ]; then
    echo "❌ Scopes GitHub manquants: ${MISSING_SCOPES[*]}"
    echo ""
    echo "🔄 Pour renouveler l'authentification avec TOUS les scopes requis:"
    echo "   bash ./scripts/gh_auth_setup.sh"
    echo ""
    exit 1
fi

echo "✅ Scopes GitHub valides: $CURRENT_SCOPES"
```

### Étape 2: TodoWrite Initialisation

```yaml
todos:
  - content: "Vérifier template PR"
    status: "pending"
    activeForm: "Vérification du template PR"
  - content: "Lancer QA intelligente"
    status: "pending"
    activeForm: "Lancement de la QA intelligente"
  - content: "Analyser changements git"
    status: "pending"
    activeForm: "Analyse des changements git"
  - content: "Confirmer branche de base"
    status: "pending"
    activeForm: "Confirmation de la branche de base"
  - content: "Push et création PR"
    status: "pending"
    activeForm: "Push et création de la PR"
  - content: "Assigner milestone"
    status: "pending"
    activeForm: "Assignation du milestone"
  - content: "Assigner projet GitHub"
    status: "pending"
    activeForm: "Assignation du projet GitHub"
  - content: "Code review automatique"
    status: "pending"
    activeForm: "Code review automatique"
  - content: "Nettoyage branche locale"
    status: "pending"
    activeForm: "Nettoyage de la branche locale"
```

### Étape 3: Vérification Template PR

Marquer todo #1 `in_progress`.

```bash
bash $SCRIPTS_DIR/verify_pr_template.sh "$PR_TEMPLATE_PATH"
```

Si exit code != 0: ARRÊT avec message d'erreur.

Marquer todo #1 `completed`.

### Étape 4: QA Intelligente

Marquer todo #2 `in_progress`.

```bash
bash $SCRIPTS_DIR/smart_qa.sh
```

Si exit code == 1: ARRÊT avec message d'erreur (QA échouée).
Si exit code == 0: Continuer (QA passée ou ignorée).

Marquer todo #2 `completed`.

### Étape 5: Analyse Changements

Marquer todo #3 `in_progress`.

```bash
STATS=$(bash $SCRIPTS_DIR/analyze_changes.sh)
```

Parser le JSON retourné pour obtenir:
- `files_changed`
- `additions`
- `deletions`
- `modified_files`
- `has_php_files`

Marquer todo #3 `completed`.

### Étape 6: Confirmation Branche de Base

Marquer todo #4 `in_progress`.

```bash
# Si BRANCH_BASE fourni en argument
if [ -n "$BRANCH_BASE" ]; then
    RESULT=$(python3 $SCRIPTS_DIR/confirm_base_branch.py --branch "$BRANCH_BASE")
    if [ $? -ne 0 ]; then
        echo "❌ Branche '$BRANCH_BASE' invalide"
        exit 1
    fi
    BRANCH_BASE="$RESULT"
else
    # Sinon, demander à l'utilisateur
    RESULT=$(python3 $SCRIPTS_DIR/confirm_base_branch.py)
    # Parser JSON
    # Utiliser AskUserQuestion avec les branches disponibles
    # Stocker la réponse dans BRANCH_BASE
fi
```

Exemple AskUserQuestion:
```yaml
questions:
  - question: "Quelle branche de base pour la PR ?"
    header: "Branche base"
    multiSelect: false
    options:
      - label: "develop"
        description: "Branche de développement principale"
      - label: "main"
        description: "Branche de production"
```

Marquer todo #4 `completed`.

### Étape 7: Push et Création PR

Marquer todo #5 `in_progress`.

```bash
# Récupérer branche courante
BRANCH_NAME=$(git branch --show-current)

# Lire le template PR du projet
PR_TEMPLATE=$(cat "$PR_TEMPLATE_PATH")

# Générer titre PR
# - Si issue liée: "[Titre issue] / Issue #XX"
# - Sinon: Titre métier descriptif

PR_TITLE="[TITRE_GÉNÉRÉ]"

# Créer fichier temporaire avec le body
PR_BODY_FILE="/tmp/pr_body_$(date +%s).md"
echo "$PR_TEMPLATE" > "$PR_BODY_FILE"
# Remplir les placeholders du template avec les infos réelles

# Appeler le script de push sécurisé
PR_NUMBER=$(bash $SCRIPTS_DIR/safe_push_pr.sh "$BRANCH_BASE" "$BRANCH_NAME" "$PR_TITLE" "$PR_BODY_FILE")

if [ $? -ne 0 ]; then
    echo "❌ Échec création PR"
    rm "$PR_BODY_FILE"
    exit 1
fi

# Nettoyer
rm "$PR_BODY_FILE"

echo "✅ PR #$PR_NUMBER créée"
```

Marquer todo #5 `completed`.

### Étape 8: Assignation Milestone

Marquer todo #6 `in_progress`.

```bash
# Si MILESTONE fourni en argument
if [ -n "$MILESTONE" ]; then
    RESULT=$(python3 $SCRIPTS_DIR/assign_milestone.py "$PR_NUMBER" --milestone "$MILESTONE")
    if [ $? -ne 0 ]; then
        echo "⚠️ Échec assignation milestone (non bloquant)"
    else
        echo "✅ Milestone '$MILESTONE' assigné"
    fi
else
    # Sinon, demander à l'utilisateur
    RESULT=$(python3 $SCRIPTS_DIR/assign_milestone.py "$PR_NUMBER")
    # Si needs_user_input: true
    # Parser JSON et utiliser AskUserQuestion
    # Rappeler le script avec --milestone après réponse
fi
```

Exemple AskUserQuestion:
```yaml
questions:
  - question: "Assigner un milestone à la PR ?"
    header: "Milestone"
    multiSelect: false
    options:
      - label: "1.0.0"
        description: "Version 1.0.0 (suggéré)"
      - label: "1.1.0"
        description: "Version 1.1.0"
```

Marquer todo #6 `completed`.

### Étape 9: Assignation Projet

Marquer todo #7 `in_progress`.

```bash
# Si PROJECT_NAME fourni en argument
if [ -n "$PROJECT_NAME" ]; then
    RESULT=$(python3 $SCRIPTS_DIR/assign_project.py "$PR_NUMBER" --project "$PROJECT_NAME")
    if [ $? -ne 0 ]; then
        echo "⚠️ Échec assignation projet (non bloquant)"
    else
        echo "✅ Projet '$PROJECT_NAME' assigné"
    fi
else
    # Sinon, demander à l'utilisateur
    RESULT=$(python3 $SCRIPTS_DIR/assign_project.py "$PR_NUMBER")
    # Si needs_user_input: true
    # Parser JSON et utiliser AskUserQuestion
    # Rappeler le script avec --project après réponse
fi
```

Marquer todo #7 `completed`.

### Étape 10: Code Review

Marquer todo #8 `in_progress`.

```bash
if [ -n "$NO_REVIEW_FLAG" ]; then
    echo "ℹ️ Review automatique ignorée (--no-review)"
else
    echo "🔍 Lancement code review automatique..."
    # Utiliser la commande /review ou analyser les changements
    # et poster un commentaire de review sur la PR
    # Via: gh pr comment $PR_NUMBER --body "[REVIEW]"
    echo "✅ Review complétée"
fi
```

Marquer todo #8 `completed`.

### Étape 11: Nettoyage Branche

Marquer todo #9 `in_progress`.

```bash
if [ -n "$DELETE_FLAG" ]; then
    bash $SCRIPTS_DIR/cleanup_branch.sh "$BRANCH_BASE" "$BRANCH_NAME" --delete
    echo "✅ Branche locale supprimée"
else
    RESULT=$(bash $SCRIPTS_DIR/cleanup_branch.sh "$BRANCH_BASE" "$BRANCH_NAME")
    # Si needs_user_input: true
    # Utiliser AskUserQuestion pour confirmer suppression
fi
```

Marquer todo #9 `completed`.

### Étape 12: Rapport Final

```yaml
task: "Pull Request créée avec succès"
status: "completed"

details:
  pr_number: $PR_NUMBER
  pr_title: "$PR_TITLE"
  pr_url: "[URL récupérée via gh pr view]"
  branch_source: $BRANCH_NAME
  branch_base: $BRANCH_BASE
  milestone: $MILESTONE
  project: $PROJECT_NAME

stats:
  files_changed: [VALUE]
  additions: [VALUE]
  deletions: [VALUE]

qa_status: "[PASSÉE/IGNORÉE/ÉCHEC]"
review_status: "[COMPLÉTÉE/IGNORÉE]"
branch_cleanup: "[SUPPRIMÉE/CONSERVÉE]"

timing:
  start: "[TIMESTAMP_START]"
  end: "[TIMESTAMP_END via date]"
  duration: "[DURÉE_CALCULÉE]"
```

Calculer durée:
```bash
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Formater durée
if [ $DURATION -lt 60 ]; then
    DURATION_STR="${DURATION}s"
elif [ $DURATION -lt 3600 ]; then
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${MINUTES}m ${SECONDS}s"
else
    HOURS=$((DURATION / 3600))
    MINUTES=$(((DURATION % 3600) / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${HOURS}h ${MINUTES}m ${SECONDS}s"
fi

echo "⏱️ Durée: $DURATION_STR"
```

## Error Handling

- Template PR absent → ARRÊT immédiat (exit 1)
- QA échec → ARRÊT immédiat (exit 1)
- Branche invalide → ARRÊT immédiat (exit 1)
- Push échec → ARRÊT immédiat (exit 1)
- Milestone/Projet échec → WARNING (non bloquant)

## Notes

- Tous les scripts sont dans `./scripts/` relatif au SKILL.md
- Utiliser `bash` pour les scripts .sh
- Utiliser `python3` pour les scripts .py
- Parser JSON via `jq` ou équivalent
- Marquer CHAQUE todo completed immédiatement après succès
