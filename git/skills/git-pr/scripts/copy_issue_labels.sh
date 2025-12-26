#!/bin/bash
# Copie les labels d'une issue vers une PR
# Usage: copy_issue_labels.sh <issue_number> <pr_number>
# Output: Liste des labels appliqués ou message si aucun label

set -euo pipefail

ISSUE_NUMBER="${1:-}"
PR_NUMBER="${2:-}"

# Vérifications
if [ -z "$ISSUE_NUMBER" ]; then
    echo "ℹ️ Pas d'issue référencée, skip labels"
    exit 0
fi

if [ -z "$PR_NUMBER" ]; then
    echo "❌ Numéro de PR requis" >&2
    exit 1
fi

# Récupérer les labels de l'issue
LABELS=$(gh issue view "$ISSUE_NUMBER" --json labels -q '.labels[].name' 2>/dev/null || echo "")

if [ -z "$LABELS" ]; then
    echo "ℹ️ Issue #$ISSUE_NUMBER n'a pas de labels"
    exit 0
fi

# Construire la liste des labels pour gh pr edit
LABEL_ARGS=""
while IFS= read -r label; do
    if [ -n "$label" ]; then
        LABEL_ARGS="$LABEL_ARGS --add-label \"$label\""
    fi
done <<< "$LABELS"

# Appliquer les labels à la PR
if [ -n "$LABEL_ARGS" ]; then
    eval "gh pr edit $PR_NUMBER $LABEL_ARGS"

    # Afficher les labels appliqués
    LABEL_COUNT=$(echo "$LABELS" | wc -l)
    echo "✅ $LABEL_COUNT label(s) copié(s) depuis issue #$ISSUE_NUMBER vers PR #$PR_NUMBER:"
    echo "$LABELS" | sed 's/^/  - /'
fi
