#!/usr/bin/env bash
set -euo pipefail

COMPOSER_JSON="composer.json"

if [[ ! -f "$COMPOSER_JSON" ]]; then
    echo "❌ composer.json introuvable" >&2
    exit 1
fi

# Extraire namespace racine
NAMESPACE=$(jq -r '.autoload.psr4 // {} | keys[0] // "App"' "$COMPOSER_JSON" | sed 's/\\\\$//')
export NAMESPACE

# Extraire nom du projet
PROJECT_NAME=$(jq -r '.name // "unknown"' "$COMPOSER_JSON" | cut -d'/' -f2)
export PROJECT_NAME

# Auteur depuis git config
AUTHOR_NAME=$(git config user.name 2>/dev/null || echo "Unknown")
export AUTHOR_NAME

# Date actuelle
DATE=$(date +%Y-%m-%d)
export DATE

echo "✅ Contexte analysé :"
echo "   PROJECT_NAME=$PROJECT_NAME"
echo "   NAMESPACE=$NAMESPACE"
echo "   AUTHOR=$AUTHOR_NAME"
echo "   DATE=$DATE"
