#!/bin/bash
# Vérifications sécurité + push + création PR
# Usage: safe_push_pr.sh <branch_base> <branch_name> <pr_title> <pr_body_file>
# Output: PR_NUMBER (stdout) ou exit 1

set -euo pipefail

BRANCH_BASE="$1"
BRANCH_NAME="$2"
PR_TITLE="$3"
PR_BODY_FILE="$4"

# Vérification 1: Branche courante
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
    echo "❌ Branche courante ($CURRENT_BRANCH) != branche attendue ($BRANCH_NAME)" >&2
    exit 1
fi

# Vérification 2: Commits à pousser
COMMITS_TO_PUSH=$(git log --oneline "origin/$BRANCH_BASE..$BRANCH_NAME" 2>/dev/null | wc -l || echo "0")

if [ "$COMMITS_TO_PUSH" -eq 0 ]; then
    echo "❌ Aucun commit à pousser vers $BRANCH_BASE" >&2
    exit 1
fi

# Vérification 3: Afficher commits
echo "📋 Commits à pousser ($COMMITS_TO_PUSH):"
git log --oneline "origin/$BRANCH_BASE..$BRANCH_NAME" | sed 's/^/  /'

# Vérification 4: Vérifier que le fichier body existe
if [ ! -f "$PR_BODY_FILE" ]; then
    echo "❌ Fichier PR body absent: $PR_BODY_FILE" >&2
    exit 1
fi

# Push vers origin
echo "🚀 Push vers origin/$BRANCH_NAME..."
if ! git push -u origin "$BRANCH_NAME"; then
    echo "❌ Échec du push" >&2
    exit 1
fi

# Création PR (draft pour limiter l'exécution de la CI)
echo "📝 Création de la Pull Request (draft)..."
PR_URL=$(gh pr create \
    --base "$BRANCH_BASE" \
    --title "$PR_TITLE" \
    --body-file "$PR_BODY_FILE" \
    --draft \
    2>&1)

if [ $? -ne 0 ]; then
    echo "❌ Échec création PR: $PR_URL" >&2
    exit 1
fi

# Extraire le numéro de PR depuis l'URL
PR_NUMBER=$(echo "$PR_URL" | grep -oP '/pull/\K\d+' || echo "")

if [ -z "$PR_NUMBER" ]; then
    # Fallback: extraire depuis gh pr view
    PR_NUMBER=$(gh pr view --json number -q .number 2>/dev/null || echo "")
fi

if [ -z "$PR_NUMBER" ]; then
    echo "❌ Impossible d'extraire le numéro de PR" >&2
    echo "URL: $PR_URL" >&2
    exit 1
fi

echo "✅ PR #$PR_NUMBER créée: $PR_URL"
echo "$PR_NUMBER"
