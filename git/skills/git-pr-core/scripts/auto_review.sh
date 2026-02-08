#!/bin/bash
# Récupère les données de la PR pour analyse intelligente par Claude
# Usage: auto_review.sh <pr_number>
# Sortie: JSON avec toutes les informations nécessaires pour la review
# Exit 0 si OK, Exit 1 si échec

set -euo pipefail

# Vérifier outils requis
command -v gh >/dev/null 2>&1 || { echo "gh CLI requis" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq requis" >&2; exit 1; }

PR_NUMBER="$1"

if [ -z "$PR_NUMBER" ]; then
    echo "❌ PR_NUMBER requis" >&2
    exit 1
fi

# Récupérer les informations de la PR
PR_INFO=$(gh pr view "$PR_NUMBER" --json title,body,files,additions,deletions,commits,baseRefName,headRefName 2>&1) || {
    echo "❌ Impossible de récupérer les informations de la PR #$PR_NUMBER" >&2
    echo "$PR_INFO" >&2
    exit 1
}

if [ -z "$PR_INFO" ]; then
    echo "❌ Informations de la PR #$PR_NUMBER vides" >&2
    exit 1
fi

# Récupérer le diff complet
DIFF=$(gh pr diff "$PR_NUMBER" 2>&1) || {
    echo "WARNING: impossible de récupérer le diff pour PR #$PR_NUMBER" >&2
    DIFF=""
}

if [ -z "$DIFF" ]; then
    echo "WARNING: diff vide pour PR #$PR_NUMBER" >&2
    DIFF="(diff indisponible - review basée sur les métadonnées uniquement)"
fi

# Récupérer le template PR s'il existe
PR_TEMPLATE=""
if [ -f ".github/PULL_REQUEST_TEMPLATE/default.md" ]; then
    PR_TEMPLATE=$(cat .github/PULL_REQUEST_TEMPLATE/default.md)
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
