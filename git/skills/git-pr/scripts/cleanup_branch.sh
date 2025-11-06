#!/bin/bash
# Proposer/exécuter suppression branche locale
# Usage: cleanup_branch.sh <branch_base> <branch_name> [--delete]
# Exit: 0=supprimée, 1=conservée

set -euo pipefail

BRANCH_BASE="$1"
BRANCH_NAME="$2"
DELETE_FLAG="${3:-}"

# Si --delete fourni, suppression auto
if [ "$DELETE_FLAG" = "--delete" ]; then
    echo "🗑️  Suppression automatique de la branche $BRANCH_NAME..."
    git checkout "$BRANCH_BASE"
    git branch -D "$BRANCH_NAME"
    echo "✅ Branche $BRANCH_NAME supprimée"
    exit 0
fi

# Sinon, retourner JSON pour AskUserQuestion
cat <<EOF
{
  "branch_name": "$BRANCH_NAME",
  "branch_base": "$BRANCH_BASE",
  "needs_user_input": true
}
EOF
