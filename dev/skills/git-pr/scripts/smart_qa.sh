#!/bin/bash
# Détecte les fichiers PHP modifiés et lance make qa si nécessaire
# Usage: smart_qa.sh
# Exit: 0=ok/ignoré, 1=échec QA

set -euo pipefail

# Détecter fichiers PHP modifiés
PHP_FILES=$(git diff --name-only --cached | grep '\.php$' || true)

if [ -z "$PHP_FILES" ]; then
    echo "ℹ️  Aucun fichier PHP modifié - QA ignorée"
    exit 0
fi

echo "🔍 Fichiers PHP détectés - Lancement de make qa..."
echo "$PHP_FILES" | sed 's/^/  - /'

# Lancer QA avec timeout
if timeout 600 make qa; then
    echo "✅ QA passée avec succès"
    exit 0
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        echo "❌ QA timeout (>600s)" >&2
    else
        echo "❌ QA échouée" >&2
    fi
    exit 1
fi
