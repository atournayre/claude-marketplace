#!/bin/bash
# Vérifie que tous les scopes GitHub requis sont présents
# Exit 0 si OK, Exit 1 si scopes manquants

set -e

REQUIRED_SCOPES=(repo read:org project gist)

# Récupérer scopes actuels
CURRENT_SCOPES=$(gh auth status 2>&1 | grep "Token scopes" | sed 's/.*Token scopes: //' | tr -d "'" | tr ',' ' ')

if [ -z "$CURRENT_SCOPES" ]; then
    echo "❌ Impossible de récupérer les scopes GitHub"
    echo "   Vérifier l'authentification avec: gh auth status"
    exit 1
fi

# Vérifier chaque scope requis
MISSING_SCOPES=()
for scope in "${REQUIRED_SCOPES[@]}"; do
    if ! echo "$CURRENT_SCOPES" | grep -qw "$scope"; then
        MISSING_SCOPES+=("$scope")
    fi
done

# Rapport
if [ ${#MISSING_SCOPES[@]} -gt 0 ]; then
    echo "❌ Scopes GitHub manquants: ${MISSING_SCOPES[*]}"
    echo ""
    echo "🔄 Pour renouveler l'authentification:"
    echo "   bash $(dirname "$0")/gh_auth_setup.sh"
    exit 1
fi

echo "✅ Scopes GitHub valides"
exit 0
