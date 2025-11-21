#!/bin/bash
# Récupère les données de la PR pour analyse intelligente par Claude
# Usage: auto_review.sh <pr_number>
# Sortie: JSON avec toutes les informations nécessaires pour la review
# Exit 0 si OK, Exit 1 si échec

set -euo pipefail

PR_NUMBER="$1"

if [ -z "$PR_NUMBER" ]; then
    echo "❌ PR_NUMBER requis" >&2
    exit 1
fi

# Récupérer les informations de la PR
PR_INFO=$(gh pr view "$PR_NUMBER" --json title,body,files,additions,deletions,commits,baseRefName,headRefName 2>/dev/null)

if [ -z "$PR_INFO" ]; then
    echo "❌ Impossible de récupérer les informations de la PR" >&2
    exit 1
fi

# Récupérer le diff complet
DIFF=$(gh pr diff "$PR_NUMBER" 2>/dev/null || echo "")

# Récupérer le template PR s'il existe
PR_TEMPLATE=""
if [ -f ".github/pull_request_template.md" ]; then
    PR_TEMPLATE=$(cat .github/pull_request_template.md)
fi

# Générer sortie JSON pour Claude
cat <<EOF
{
  "pr_number": $PR_NUMBER,
  "pr_info": $PR_INFO,
  "diff": $(echo "$DIFF" | jq -Rs .),
  "template": $(echo "$PR_TEMPLATE" | jq -Rs .)
}
EOF
