#!/bin/bash
# Création complète de PR: lit template, génère titre, crée PR
# Usage: create_pr.sh <branch_base> <pr_template_path>
# Output: PR_NUMBER (stdout) ou exit 1

set -euo pipefail

BRANCH_BASE="$1"
PR_TEMPLATE_PATH="$2"
SCRIPTS_DIR="$(dirname "$0")"

# Charger le script centralisé pour les emojis
EMOJI_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/commit-emoji.sh"
if [ -f "$EMOJI_SCRIPT" ]; then
    source "$EMOJI_SCRIPT"
else
    echo "⚠️ Script commit-emoji.sh non trouvé, utilisation du fallback" >&2
    get_commit_emoji() { echo "🔧"; }
fi

# Récupérer branche courante
BRANCH_NAME=$(git branch --show-current)

# Lire template PR
if [ ! -f "$PR_TEMPLATE_PATH" ]; then
    echo "❌ Template PR absent: $PR_TEMPLATE_PATH" >&2
    exit 1
fi
PR_TEMPLATE=$(cat "$PR_TEMPLATE_PATH")

# Détecter le type conventional commit depuis le nom de branche
# Formats supportés: type/description, type/123-description, type/scope/description
COMMIT_TYPE=$(echo "$BRANCH_NAME" | grep -oE '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)' || echo "")

# Détecter scope optionnel (format: type/scope/description)
SCOPE=""
if echo "$BRANCH_NAME" | grep -qE '^[^/]+/[^/]+/'; then
    SCOPE=$(echo "$BRANCH_NAME" | sed -E 's|^[^/]+/([^/]+)/.*|\1|')
fi

# Détecter issue depuis nom de branche (ex: feat/123-description, fix/456-bug)
ISSUE_NUMBER=$(echo "$BRANCH_NAME" | grep -oE '[0-9]+' | head -1 || echo "")

# Générer description du titre
DESCRIPTION=""
if [ -n "$ISSUE_NUMBER" ]; then
    # Vérifier que l'issue existe et récupérer son titre
    ISSUE_TITLE=$(gh issue view "$ISSUE_NUMBER" --json title -q '.title' 2>/dev/null || echo "")
    if [ -n "$ISSUE_TITLE" ]; then
        DESCRIPTION="$ISSUE_TITLE"
        echo "✅ Description basée sur issue #$ISSUE_NUMBER" >&2
    fi
fi

# Si pas de description depuis l'issue, extraire du nom de branche
if [ -z "$DESCRIPTION" ]; then
    if [ -n "$ISSUE_NUMBER" ]; then
        echo "⚠️ Issue #$ISSUE_NUMBER non trouvée" >&2
    else
        echo "ℹ️ Pas d'issue détectée dans '$BRANCH_NAME'" >&2
    fi
    # Nettoyer le nom de branche pour créer une description
    # Retirer le type et scope, puis nettoyer
    DESCRIPTION=$(echo "$BRANCH_NAME" | sed -E 's|^[^/]+/||' | sed -E 's|^[^/]+/||' | sed 's/-/ /g' | sed 's/[0-9]* *//')
fi

# Construire le titre au format Conventional Commits avec emoji
if [ -n "$COMMIT_TYPE" ]; then
    EMOJI=$(get_commit_emoji "$COMMIT_TYPE")
    if [ -n "$SCOPE" ]; then
        PR_TITLE="${EMOJI} ${COMMIT_TYPE}(${SCOPE}): ${DESCRIPTION}"
    else
        PR_TITLE="${EMOJI} ${COMMIT_TYPE}: ${DESCRIPTION}"
    fi
    echo "✅ Titre au format Conventional Commits avec emoji" >&2
else
    # Fallback: utiliser 'chore' par défaut
    echo "⚠️ Type non détecté dans '$BRANCH_NAME', utilisation de 'chore' par défaut" >&2
    PR_TITLE="$(get_commit_emoji chore) chore: ${DESCRIPTION}"
fi

# Suffixer avec le numéro d'issue si détecté
if [ -n "$ISSUE_NUMBER" ]; then
    PR_TITLE="${PR_TITLE} / Issue #${ISSUE_NUMBER}"
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
