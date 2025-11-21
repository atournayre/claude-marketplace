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

# Git PR Skill - Checklist d'exécution

## Configuration

```bash
SCRIPTS_DIR="/home/atournayre/.claude/plugins/marketplaces/atournayre-claude-plugin-marketplace/git/skills/git-pr/scripts"
PR_TEMPLATE_PATH=".github/pull_request_template.md"
```

## Checklist d'exécution

### 1. Initialisation

EXÉCUTER :
```bash
START_TIME=$(date +%s)
```

EXÉCUTER TodoWrite avec ces todos exacts :
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

### 2. Parsing arguments

EXÉCUTER ce bloc pour parser $ARGUMENTS :
```bash
ARGS=($ARGUMENTS)
BRANCH_BASE=""
MILESTONE=""
PROJECT_NAME=""
DELETE_FLAG=""
NO_REVIEW_FLAG=""

for arg in "${ARGS[@]}"; do
    case "$arg" in
        --delete) DELETE_FLAG="--delete" ;;
        --no-review) NO_REVIEW_FLAG="--no-review" ;;
        *)
            if [ -z "$BRANCH_BASE" ]; then
                BRANCH_BASE="$arg"
            elif [ -z "$MILESTONE" ]; then
                MILESTONE="$arg"
            elif [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$arg"
            fi
            ;;
    esac
done
```

### 3. Vérification scopes GitHub

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/check_scopes.sh
```

- Exit 0 → continuer
- Exit 1 → ARRÊT, afficher message du script

### 4. Template PR

- Marquer todo #1 in_progress

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/verify_pr_template.sh "$PR_TEMPLATE_PATH"
```

- Exit 0 → marquer todo #1 completed
- Exit 1 → ARRÊT

### 5. QA (si pas --no-review)

- Marquer todo #2 in_progress

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/smart_qa.sh
```

- Exit 0 → marquer todo #2 completed
- Exit 1 → ARRÊT

### 6. Analyse changements

- Marquer todo #3 in_progress

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/analyze_changes.sh
```

- Stocker sortie JSON
- Marquer todo #3 completed

### 7. Branche de base

- Marquer todo #4 in_progress

Si BRANCH_BASE fourni :
```bash
python3 $SCRIPTS_DIR/confirm_base_branch.py --branch "$BRANCH_BASE"
```

Sinon :
```bash
python3 $SCRIPTS_DIR/confirm_base_branch.py
```

Si needs_user_input: true → utiliser AskUserQuestion :
```yaml
questions:
  - question: "Quelle branche de base pour la PR ?"
    header: "Branche"
    multiSelect: false
    options:
      - label: "develop"
        description: "Branche développement"
      - label: "main"
        description: "Branche production"
```

- Marquer todo #4 completed

### 8. Création PR

- Marquer todo #5 in_progress

EXÉCUTER :
```bash
PR_NUMBER=$(bash $SCRIPTS_DIR/create_pr.sh "$BRANCH_BASE" "$PR_TEMPLATE_PATH")
```

- Exit 0 → stocker PR_NUMBER, marquer todo #5 completed
- Exit 1 → ARRÊT

### 9. Milestone

- Marquer todo #6 in_progress

Si MILESTONE fourni :
```bash
python3 $SCRIPTS_DIR/assign_milestone.py $PR_NUMBER --milestone "$MILESTONE"
```

Sinon :
```bash
python3 $SCRIPTS_DIR/assign_milestone.py $PR_NUMBER
```

Si needs_user_input: true → utiliser AskUserQuestion avec milestones disponibles

- Marquer todo #6 completed (même si échec, non bloquant)

### 10. Projet

- Marquer todo #7 in_progress

Si PROJECT_NAME fourni :
```bash
python3 $SCRIPTS_DIR/assign_project.py $PR_NUMBER --project "$PROJECT_NAME"
```

Sinon :
```bash
python3 $SCRIPTS_DIR/assign_project.py $PR_NUMBER
```

Si needs_user_input: true → utiliser AskUserQuestion avec projets disponibles

- Marquer todo #7 completed (même si échec, non bloquant)

### 11. Review (si pas --no-review)

- Marquer todo #8 in_progress

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/auto_review.sh $PR_NUMBER
```

- Marquer todo #8 completed

### 12. Nettoyage

- Marquer todo #9 in_progress

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/cleanup_branch.sh "$BRANCH_BASE" "$BRANCH_NAME" $DELETE_FLAG
```

Si needs_user_input: true → utiliser AskUserQuestion pour confirmer suppression

- Marquer todo #9 completed

### 13. Rapport final

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/final_report.sh $PR_NUMBER $START_TIME
```

Afficher le rapport YAML généré.
