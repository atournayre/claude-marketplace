#!/bin/bash
# Création complète de PR: lit template, génère titre, crée PR
# Usage: create_pr.sh <branch_base> <pr_template_path>
# Output: PR_NUMBER (stdout) ou exit 1

set -euo pipefail

BRANCH_BASE="$1"
PR_TEMPLATE_PATH="$2"
SCRIPTS_DIR="$(dirname "$0")"

# Récupérer branche courante
BRANCH_NAME=$(git branch --show-current)

# Lire template PR
if [ ! -f "$PR_TEMPLATE_PATH" ]; then
    echo "❌ Template PR absent: $PR_TEMPLATE_PATH" >&2
    exit 1
fi
PR_TEMPLATE=$(cat "$PR_TEMPLATE_PATH")

# Détecter issue depuis nom de branche (ex: feat/123-description, fix/456-bug)
ISSUE_NUMBER=$(echo "$BRANCH_NAME" | grep -oE '[0-9]+' | head -1 || echo "")

# Générer titre PR
if [ -n "$ISSUE_NUMBER" ]; then
    # Vérifier que l'issue existe et récupérer son titre
    ISSUE_TITLE=$(gh issue view "$ISSUE_NUMBER" --json title -q '.title' 2>/dev/null || echo "")
    if [ -n "$ISSUE_TITLE" ]; then
        PR_TITLE="$ISSUE_TITLE / Issue #$ISSUE_NUMBER"
        echo "✅ Titre PR basé sur issue #$ISSUE_NUMBER" >&2
    else
        # Issue non trouvée, utiliser nom de branche
        echo "⚠️ Issue #$ISSUE_NUMBER non trouvée" >&2
        # Nettoyer le nom de branche pour créer un titre
        PR_TITLE=$(echo "$BRANCH_NAME" | sed 's|^[^/]*/||' | sed 's/-/ /g' | sed 's/[0-9]* *//')
        PR_TITLE="${PR_TITLE^}"  # Capitalize first letter
    fi
else
    # Pas de numéro d'issue, utiliser nom de branche
    echo "ℹ️ Pas d'issue détectée dans '$BRANCH_NAME'" >&2
    PR_TITLE=$(echo "$BRANCH_NAME" | sed 's|^[^/]*/||' | sed 's/-/ /g')
    PR_TITLE="${PR_TITLE^}"
fi

# Créer fichier temporaire avec le body
PR_BODY_FILE="/tmp/pr_body_$(date +%s).md"
echo "$PR_TEMPLATE" > "$PR_BODY_FILE"

# Appeler le script de push sécurisé
PR_NUMBER=$(bash "$SCRIPTS_DIR/safe_push_pr.sh" "$BRANCH_BASE" "$BRANCH_NAME" "$PR_TITLE" "$PR_BODY_FILE")
EXIT_CODE=$?

# Nettoyer
rm -f "$PR_BODY_FILE"

if [ $EXIT_CODE -ne 0 ]; then
    exit 1
fi

echo "$PR_NUMBER"
