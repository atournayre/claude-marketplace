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
  - content: "Générer description PR intelligente"
    status: "pending"
    activeForm: "Génération de la description PR intelligente"
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

### 8. Génération description intelligente

- Marquer todo "Générer description PR intelligente" in_progress

EXÉCUTER pour récupérer les informations :
```bash
BRANCH_NAME=$(git branch --show-current)
echo "=== COMMITS ==="
git log $BRANCH_BASE..$BRANCH_NAME --oneline
echo ""
echo "=== DIFF STAT ==="
git diff $BRANCH_BASE..$BRANCH_NAME --stat
echo ""
echo "=== FICHIERS MODIFIÉS ==="
git diff $BRANCH_BASE..$BRANCH_NAME --name-only
```

LIRE le template PR avec Read tool : `$PR_TEMPLATE_PATH`

**GÉNÉRER LA DESCRIPTION** en tant que Claude :
1. Analyser les commits et le diff
2. Remplir intelligemment chaque section du template :
   - **Bug fix** : supprimer si pas de fix, sinon lier l'issue
   - **Description** : résumer les changements basé sur les commits
   - **Type de changement** : cocher (✔️) les types appropriés basé sur les commits
   - **Tests** : indiquer si tests ajoutés/modifiés
   - **Checklist** : cocher ce qui s'applique
   - **Actions** : cocher ce qui est nécessaire
3. Sauvegarder dans `/tmp/pr_body_generated.md` avec Write tool

### 9. Création PR

EXÉCUTER :
```bash
PR_NUMBER=$(bash $SCRIPTS_DIR/create_pr.sh "$BRANCH_BASE" "/tmp/pr_body_generated.md")
```

- Exit 0 → stocker PR_NUMBER, marquer todo "Générer description PR intelligente" completed, puis marquer todo "Push et création PR" completed
- Exit 1 → ARRÊT

### 10. Milestone

- Marquer todo "Assigner milestone" in_progress

Si MILESTONE fourni :
```bash
python3 $SCRIPTS_DIR/assign_milestone.py $PR_NUMBER --milestone "$MILESTONE"
```

Sinon :
```bash
python3 $SCRIPTS_DIR/assign_milestone.py $PR_NUMBER
```

Si needs_user_input: true → utiliser AskUserQuestion avec milestones disponibles

- Marquer todo "Assigner milestone" completed (même si échec, non bloquant)

### 11. Projet

- Marquer todo "Assigner projet GitHub" in_progress

Si PROJECT_NAME fourni :
```bash
python3 $SCRIPTS_DIR/assign_project.py $PR_NUMBER --project "$PROJECT_NAME"
```

Sinon :
```bash
python3 $SCRIPTS_DIR/assign_project.py $PR_NUMBER
```

Si needs_user_input: true → utiliser AskUserQuestion avec projets disponibles

- Marquer todo "Assigner projet GitHub" completed (même si échec, non bloquant)

### 12. Review intelligente (si pas --no-review)

- Marquer todo "Code review automatique" in_progress

EXÉCUTER pour récupérer les données :
```bash
PR_DATA=$(bash $SCRIPTS_DIR/auto_review.sh $PR_NUMBER)
```

**ANALYSER EN TANT QUE CLAUDE** les données JSON retournées et générer une review intelligente :

1. **Conformité template PR** :
   - Vérifier que toutes les sections requises sont remplies
   - Signaler les sections manquantes ou incomplètes

2. **Qualité du code** :
   - Patterns suspects (code dupliqué, fonctions trop longues)
   - Problèmes de sécurité potentiels (injections, données sensibles)
   - Respect des conventions du projet

3. **Tests** :
   - Tests manquants pour les nouvelles fonctionnalités
   - Couverture des cas limites

4. **Documentation** :
   - Commentaires nécessaires absents
   - Mise à jour README si API modifiée

5. **Suggestions d'amélioration** :
   - Refactorisation possible
   - Performance
   - Lisibilité

**GÉNÉRER le commentaire de review** avec structure :
```markdown
## 🔍 Code Review Automatique

### ✅ Points positifs
- [ce qui est bien fait]

### ⚠️ Points d'attention
- [problèmes potentiels à vérifier]

### 💡 Suggestions
- [améliorations possibles]

### 📋 Checklist conformité
- [ ] Template PR complet
- [ ] Tests présents
- [ ] Documentation à jour

---
*Review générée par git-pr skill*
```

EXÉCUTER pour poster le commentaire :
```bash
gh pr comment $PR_NUMBER --body "$REVIEW_COMMENT"
```

- Marquer todo "Code review automatique" completed

### 13. Nettoyage

- Marquer todo "Nettoyage branche locale" in_progress

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/cleanup_branch.sh "$BRANCH_BASE" "$BRANCH_NAME" $DELETE_FLAG
```

Si needs_user_input: true → utiliser AskUserQuestion pour confirmer suppression

- Marquer todo "Nettoyage branche locale" completed

### 14. Rapport final

EXÉCUTER :
```bash
bash $SCRIPTS_DIR/final_report.sh $PR_NUMBER $START_TIME
```

Afficher le rapport YAML généré.
