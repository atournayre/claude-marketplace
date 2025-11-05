#!/usr/bin/env bash
# Configuration authentification GitHub avec tous les scopes requis
# Usage: bash gh_auth_setup.sh

set -e

REQUIRED_SCOPES=(
    "repo"           # Accès complet aux repos (PRs, commits, etc.)
    "read:org"       # Lecture infos organisation
    "read:project"   # Lecture projets GitHub
    "project"        # Écriture/assignation aux projets
    "gist"           # Gestion des gists
)

echo "🔐 Configuration authentification GitHub"
echo ""
echo "Scopes requis:"
for scope in "${REQUIRED_SCOPES[@]}"; do
    echo "  - $scope"
done
echo ""

# Construire la commande avec tous les scopes
CMD="gh auth refresh --hostname github.com"
for scope in "${REQUIRED_SCOPES[@]}"; do
    CMD="$CMD -s $scope"
done

echo "🔄 Exécution: $CMD"
echo ""

eval "$CMD"

echo ""
echo "✅ Authentification configurée avec succès"
echo ""
echo "Vérification des scopes:"
gh auth status
