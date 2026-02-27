#!/usr/bin/env bash
# Configuration authentification GitHub avec tous les scopes requis
# Usage: bash gh_auth_setup.sh

set -euo pipefail

# Vérifier outils requis
command -v gh >/dev/null 2>&1 || { echo "gh CLI requis" >&2; exit 1; }

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

# Construire les arguments avec un tableau (pas d'eval)
SCOPE_ARGS=()
for scope in "${REQUIRED_SCOPES[@]}"; do
    SCOPE_ARGS+=(-s "$scope")
done

echo "🔄 Exécution: gh auth refresh --hostname github.com ${SCOPE_ARGS[*]}"
echo ""

gh auth refresh --hostname github.com "${SCOPE_ARGS[@]}"

echo ""
echo "✅ Authentification configurée avec succès"
echo ""
echo "Vérification des scopes:"
gh auth status
